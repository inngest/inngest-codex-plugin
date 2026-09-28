#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def main():
    repository = Path(__file__).resolve().parent.parent
    plugin = repository / "plugins" / "inngest"
    manifest = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text())
    version = manifest["version"]
    allowed = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-+"
    if not version or any(char not in allowed for char in version):
        raise ValueError("Invalid plugin version")

    required = [".codex-plugin/plugin.json", ".mcp.json", "README.md", "LICENSE"]
    for name in required:
        if not (plugin / name).is_file():
            raise ValueError(f"Missing required file: {name}")
    if not list((plugin / "skills").glob("*/SKILL.md")):
        raise ValueError("No skills found")

    components = [
        ".codex-plugin", ".mcp.json", "skills", "references",
        "examples", "assets", "README.md", "LICENSE",
    ]
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--", *components],
        cwd=plugin, check=True, capture_output=True,
    ).stdout.decode().split("\0")
    files = []
    for name in filter(None, tracked):
        path = plugin / name
        relative = path.relative_to(plugin)
        if any((plugin / parent).is_symlink() for parent in [relative, *relative.parents]):
            raise ValueError(f"Symlinks cannot be packaged: {path}")
        if not path.is_file():
            raise ValueError(f"Tracked file is missing or not regular: {path}")
        files.append(path)
    packaged = {path.relative_to(plugin).as_posix() for path in files}
    if not set(required).issubset(packaged):
        raise ValueError("Required plugin files must be tracked by Git")
    if not any(name.startswith("skills/") and name.endswith("/SKILL.md") for name in packaged):
        raise ValueError("Skills must be tracked by Git")

    output = repository / "dist" / f"inngest-{version}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            entry = ZipInfo(path.relative_to(plugin).as_posix(), (2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    print(f"Packaged {len(files)} files: {output}")


if __name__ == "__main__":
    main()
