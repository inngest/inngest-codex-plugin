#!/usr/bin/env python3
"""Portable prompt runner for the Inngest Codex plugin eval catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only in broken envs.
    raise SystemExit("PyYAML is required to run eval prompts") from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = REPO_ROOT / "eval"
CATALOG_PATH = EVAL_ROOT / "prompts" / "catalog.yaml"
RUNS_ROOT = EVAL_ROOT / "runs"
PLUGIN_ROOT = REPO_ROOT / "plugins" / "inngest"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Inngest plugin eval prompts")
    parser.add_argument(
        "selection",
        nargs="*",
        help="Prompt id(s), slug(s), or 'all'. Defaults to all in prepare-only mode.",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Create run directories and prompt files without invoking the subject command.",
    )
    parser.add_argument(
        "--run-id",
        help="Run id directory name. Defaults to UTC timestamp.",
    )
    parser.add_argument(
        "--mode",
        choices=("context", "off-only"),
        default=os.environ.get("CODEX_EVAL_MODE", "context"),
        help="context creates on/off prompts; off-only creates only unassisted prompts.",
    )
    return parser.parse_args()


def load_catalog() -> dict[str, Any]:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def select_prompts(catalog: dict[str, Any], selections: list[str]) -> list[dict[str, Any]]:
    prompts = catalog["prompts"]
    if not selections or selections == ["all"] or "all" in selections:
        return prompts

    by_id = {str(prompt["id"]): prompt for prompt in prompts}
    by_slug = {prompt["slug"]: prompt for prompt in prompts}
    selected: list[dict[str, Any]] = []

    for selection in selections:
        prompt = by_id.get(selection) or by_slug.get(selection)
        if not prompt:
            known = ", ".join(sorted(by_id.keys()))
            raise SystemExit(f"Unknown prompt '{selection}'. Known ids: {known}")
        selected.append(prompt)

    return selected


def plugin_context() -> str:
    skill_paths = sorted((PLUGIN_ROOT / "skills").glob("*/SKILL.md"))
    example_paths = sorted(
        path
        for path in (PLUGIN_ROOT / "examples").rglob("*")
        if path.suffix in {".md", ".ts", ".tsx", ".json"} and path.is_file()
    )
    chunks = [
        "# Installed Inngest Codex Plugin Context",
        "",
        "Use these local plugin skills when they are relevant. Prefer the workflow,",
        "guardrails, and anti-patterns in these skills over generic background-job",
        "advice.",
        "",
    ]

    for path in skill_paths:
        chunks.append(f"## {path.parent.name}")
        chunks.append(path.read_text(encoding="utf-8"))
        chunks.append("")

    if example_paths:
        chunks.append("# Copyable Examples")
        chunks.append("")
        chunks.append(
            "Use these examples as local patterns when creating a new durable workflow "
            "or agent. Adapt names, events, and services to the target repository."
        )
        chunks.append("")
        for path in example_paths:
            chunks.append(f"## example/{path.relative_to(PLUGIN_ROOT / 'examples')}")
            chunks.append(path.read_text(encoding="utf-8"))
            chunks.append("")

    references_dir = PLUGIN_ROOT / "references"
    if references_dir.exists():
        for path in sorted(references_dir.glob("*.md")):
            chunks.append(f"## reference/{path.name}")
            chunks.append(path.read_text(encoding="utf-8"))
            chunks.append("")

    return "\n".join(chunks)


def prompt_text(prompt: dict[str, Any], side: str, context: str | None) -> str:
    header = [
        "You are an AI coding agent being evaluated on a developer request.",
        "Work from repository evidence, make code changes when appropriate,",
        "and report what you verified.",
        "",
    ]

    if side == "on" and context:
        header.extend(
            [
                "<installed_plugin_context>",
                context,
                "</installed_plugin_context>",
                "",
            ]
        )

    header.extend(
        [
            "<developer_request>",
            prompt["prompt"].strip(),
            "</developer_request>",
            "",
        ]
    )
    return "\n".join(header)


def resolve_fixture(prompt: dict[str, Any]) -> Path | None:
    fixture = os.environ.get("CODEX_EVAL_FIXTURE_DIR") or prompt.get("fixture")
    if not fixture:
        return None

    fixture_path = Path(fixture).expanduser()
    if not fixture_path.is_absolute():
        fixture_path = (EVAL_ROOT / fixture_path).resolve()
    else:
        fixture_path = fixture_path.resolve()

    if not fixture_path.exists():
        raise SystemExit(f"Fixture does not exist: {fixture_path}")
    return fixture_path


def copy_fixture(destination: Path, prompt: dict[str, Any]) -> str | None:
    fixture_path = resolve_fixture(prompt)
    if not fixture_path:
        return None

    def ignore(_directory: str, names: list[str]) -> set[str]:
        ignored = {".git", "node_modules", ".next", "dist", "build", "coverage"}
        return {name for name in names if name in ignored}

    shutil.copytree(fixture_path, destination, dirs_exist_ok=True, ignore=ignore)
    return str(fixture_path)


def list_files(directory: Path) -> str:
    paths: list[str] = []
    for path in sorted(directory.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(directory)
        if relative.parts and relative.parts[0] in {".git", "node_modules"}:
            continue
        paths.append(str(relative))
    return "\n".join(paths) + ("\n" if paths else "")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare_side(
    run_dir: Path,
    prompt: dict[str, Any],
    side: str,
    context: str | None,
    catalog: dict[str, Any],
) -> Path:
    side_dir = run_dir / f"{prompt['id']}-{prompt['slug']}" / side
    side_dir.mkdir(parents=True, exist_ok=True)
    fixture = copy_fixture(side_dir, prompt)
    text = prompt_text(prompt, side, context)

    (side_dir / "prompt.md").write_text(text, encoding="utf-8")
    write_json(
        side_dir / "metadata.json",
        {
            "catalog_version": catalog.get("version"),
            "subject_model": catalog.get("subject_model"),
            "judge_model": catalog.get("judge_model"),
            "prompt_id": prompt["id"],
            "prompt_slug": prompt["slug"],
            "side": side,
            "mode": "plugin-context" if side == "on" else "baseline",
            "fixture_dir": fixture,
        },
    )
    (side_dir / "files-before.txt").write_text(list_files(side_dir), encoding="utf-8")
    return side_dir


def run_subject(side_dir: Path, timeout: int) -> int:
    command = os.environ.get("CODEX_EVAL_SUBJECT_CMD", "codex")
    argv = shlex.split(command)
    if not argv:
        raise SystemExit("CODEX_EVAL_SUBJECT_CMD must not be empty")

    prompt = (side_dir / "prompt.md").read_text(encoding="utf-8")
    try:
        completed = subprocess.run(
            argv,
            input=prompt,
            cwd=side_dir,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except FileNotFoundError as exc:
        exit_code = 127
        stdout = ""
        stderr = f"Subject command not found: {argv[0]}\n{exc}\n"
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + f"\nTimed out after {timeout}s\n"

    (side_dir / "stdout.txt").write_text(stdout, encoding="utf-8")
    (side_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    (side_dir / "exit-code.txt").write_text(f"{exit_code}\n", encoding="utf-8")
    (side_dir / "files-after.txt").write_text(list_files(side_dir), encoding="utf-8")
    return exit_code


def main() -> int:
    args = parse_args()
    catalog = load_catalog()
    prompts = select_prompts(catalog, args.selection)
    run_id = args.run_id or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    context = plugin_context() if args.mode == "context" else None
    sides = ["off"] if args.mode == "off-only" else ["on", "off"]
    timeout = int(os.environ.get("CODEX_EVAL_TIMEOUT", "1800"))

    write_json(
        run_dir / "run.json",
        {
            "run_id": run_id,
            "mode": args.mode,
            "selection": args.selection or ["all"],
            "subject_command": os.environ.get("CODEX_EVAL_SUBJECT_CMD", "codex"),
            "timeout_seconds": timeout,
            "prepare_only": args.prepare_only,
        },
    )

    prepared: list[Path] = []
    for prompt in prompts:
        for side in sides:
            prepared.append(prepare_side(run_dir, prompt, side, context, catalog))

    print(f"Prepared {len(prepared)} side(s) under {run_dir.relative_to(REPO_ROOT)}")
    if args.prepare_only:
        return 0

    failures = 0
    for side_dir in prepared:
        print(f"Running subject in {side_dir.relative_to(REPO_ROOT)}")
        exit_code = run_subject(side_dir, timeout)
        if exit_code != 0:
            failures += 1
            print(f"  exit {exit_code}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
