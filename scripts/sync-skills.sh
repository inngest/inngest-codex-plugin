#!/usr/bin/env bash
# Sync skills from inngest/inngest-skills into this Codex plugin repo.
#
# Source of truth: https://github.com/inngest/inngest-skills
# Usage:
#   ./scripts/sync-skills.sh           # sync from main
#   ./scripts/sync-skills.sh <ref>     # sync from a tag, branch, or SHA

set -euo pipefail

REF="${1:-main}"
TMPDIR="$(mktemp -d)"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_ROOT="$REPO_ROOT/plugins/inngest"

trap 'rm -rf "$TMPDIR"' EXIT

echo "Cloning inngest-skills@$REF..."
git clone --depth 1 --branch "$REF" https://github.com/inngest/inngest-skills.git "$TMPDIR/inngest-skills" 2>&1 | tail -3

echo "Syncing skills/ -> $PLUGIN_ROOT/skills/"
rm -rf "$PLUGIN_ROOT/skills"
cp -R "$TMPDIR/inngest-skills/skills" "$PLUGIN_ROOT/skills"

UPSTREAM_SHA="$(cd "$TMPDIR/inngest-skills" && git rev-parse HEAD)"
echo "Done. Synced from inngest-skills@$UPSTREAM_SHA"
echo ""
echo "Next: git add plugins/inngest/skills && git commit -m \"chore: sync skills from inngest-skills@${UPSTREAM_SHA:0:7}\""
