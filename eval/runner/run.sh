#!/usr/bin/env bash
# Run Inngest plugin subject eval prompts.
#
# Usage:
#   eval/runner/run.sh --prepare-only 12
#   eval/runner/run.sh 01
#   eval/runner/run.sh all
#
# Environment:
#   CODEX_EVAL_SUBJECT_CMD  Command that reads prompt text on stdin.
#                           Default: codex
#   CODEX_EVAL_MODE         "context" (default) or "off-only".
#   CODEX_EVAL_FIXTURE_DIR  Optional repo fixture copied into every side.
#   CODEX_EVAL_TIMEOUT      Per-side timeout in seconds. Default: 1800.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/run.py" "$@"
