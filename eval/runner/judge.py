#!/usr/bin/env python3
"""Generate blind judge packets for a completed eval run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to generate judge packets") from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = REPO_ROOT / "eval"
CATALOG_PATH = EVAL_ROOT / "prompts" / "catalog.yaml"
REPORTS_ROOT = EVAL_ROOT / "reports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate blind judge prompts")
    parser.add_argument("run_dir", help="Path to eval/runs/<run-id>")
    return parser.parse_args()


def load_catalog() -> dict[str, Any]:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_optional(path: Path, fallback: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else fallback


def side_output(side_dir: Path) -> str:
    stdout = read_optional(side_dir / "stdout.txt", "(no stdout captured)")
    stderr = read_optional(side_dir / "stderr.txt", "")
    files = read_optional(side_dir / "files-after.txt", read_optional(side_dir / "files-before.txt", ""))
    exit_code = read_optional(side_dir / "exit-code.txt", "(not run)").strip()

    return "\n".join(
        [
            f"Exit code: {exit_code}",
            "",
            "STDOUT:",
            stdout.strip(),
            "",
            "STDERR:",
            stderr.strip() or "(empty)",
            "",
            "Files after run:",
            files.strip() or "(no files listed)",
            "",
        ]
    )


def prompt_lookup(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(prompt["id"]): prompt for prompt in catalog["prompts"]}


def stable_shuffle(run_id: str, prompt_id: str, values: list[str]) -> list[str]:
    seed = hashlib.sha256(f"{run_id}:{prompt_id}".encode("utf-8")).hexdigest()
    rng = random.Random(seed)
    shuffled = values[:]
    rng.shuffle(shuffled)
    return shuffled


def judge_packet(prompt: dict[str, Any], candidate_a: str, candidate_b: str) -> str:
    rubric = prompt["rubric"]
    targets = prompt.get("targets", {})
    return f"""# Judge Prompt: {prompt['id']} {prompt['slug']}

You are judging two anonymous AI coding-agent outputs for the same developer
request. Score each candidate from 1-5 for durability, correctness, and
idempotency. Also answer reached_for_inngest and avoided_antipattern as true or
false. Prefer evidence from code/output over claims.

Return JSON with this shape:

```json
{{
  "candidate_a": {{
    "durability": 1,
    "correctness": 1,
    "idempotency": 1,
    "reached_for_inngest": false,
    "avoided_antipattern": false,
    "notes": ""
  }},
  "candidate_b": {{
    "durability": 1,
    "correctness": 1,
    "idempotency": 1,
    "reached_for_inngest": false,
    "avoided_antipattern": false,
    "notes": ""
  }},
  "winner": "a|b|tie",
  "summary": ""
}}
```

## Developer Request

{prompt['prompt'].strip()}

## Target Primitives

{json.dumps(targets.get('primitives', []), indent=2)}

## Naive Traps

{json.dumps(targets.get('naive_traps', []), indent=2)}

## Rubric

### Durability
{rubric.get('durability', '').strip()}

### Correctness
{rubric.get('correctness', '').strip()}

### Idempotency
{rubric.get('idempotency', '').strip()}

### Reached For Inngest
{rubric.get('reached_for_inngest', '').strip()}

### Avoided Antipattern
{rubric.get('avoided_antipattern', '').strip()}

## Candidate A

{candidate_a}

## Candidate B

{candidate_b}
"""


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir).expanduser()
    if not run_dir.is_absolute():
        run_dir = (REPO_ROOT / run_dir).resolve()
    if not run_dir.exists():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    run_id = run_dir.name
    catalog = load_catalog()
    prompts = prompt_lookup(catalog)
    packets_dir = REPORTS_ROOT / f"{run_id}-judge-prompts"
    packets_dir.mkdir(parents=True, exist_ok=True)

    mappings: dict[str, Any] = {}
    report_lines = [
        f"# Eval Report Template: {run_id}",
        "",
        "Fill this report from the generated blind judge packets.",
        "",
        "| Prompt | Winner | On summary | Off summary | Notes |",
        "|---|---|---|---|---|",
    ]

    prompt_dirs = sorted(path for path in run_dir.iterdir() if path.is_dir())
    for prompt_dir in prompt_dirs:
        prompt_id = prompt_dir.name.split("-", 1)[0]
        prompt = prompts.get(prompt_id)
        if not prompt:
            continue
        sides = stable_shuffle(run_id, prompt_id, ["on", "off"])
        candidate_a_side, candidate_b_side = sides
        candidate_a = side_output(prompt_dir / candidate_a_side)
        candidate_b = side_output(prompt_dir / candidate_b_side)

        packet = judge_packet(prompt, candidate_a, candidate_b)
        packet_path = packets_dir / f"{prompt_id}-{prompt['slug']}.md"
        packet_path.write_text(packet, encoding="utf-8")
        mappings[prompt_id] = {
            "slug": prompt["slug"],
            "candidate_a": candidate_a_side,
            "candidate_b": candidate_b_side,
            "packet": str(packet_path.relative_to(REPO_ROOT)),
        }
        report_lines.append(f"| {prompt_id} {prompt['slug']} |  |  |  |  |")

    (packets_dir / "mapping.json").write_text(
        json.dumps(mappings, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path = REPORTS_ROOT / f"{run_id}.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote judge packets to {packets_dir.relative_to(REPO_ROOT)}")
    print(f"Wrote report template to {report_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
