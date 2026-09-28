#!/usr/bin/env python3

import json
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
    files = []
    for name in components:
        component = plugin / name
        if component.is_symlink():
            raise ValueError(f"Symlinks cannot be packaged: {component}")
        paths = sorted(component.rglob("*")) if component.is_dir() else [component]
        for path in paths:
            if path.is_symlink():
                raise ValueError(f"Symlinks cannot be packaged: {path}")
            if path.is_file():
                files.append(path)

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
