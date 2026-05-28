#!/usr/bin/env bash
# Generate blind judge packets for a completed eval run.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/judge.py" "$@"
