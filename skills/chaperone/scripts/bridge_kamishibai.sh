#!/usr/bin/env bash
# Loose-coupled bridge: evops MCP → kamishibai (CLI only, no import)
# Usage: bash bridge.sh <episode.json> <output.mp4>

set -euo pipefail

EPISODE="${1:-/tmp/episode.json}"
OUTPUT="${2:-/tmp/kamishibai.mp4}"

# 1. Ensure episode exists (from evops/sf-paper-comic)
if [ ! -f "$EPISODE" ]; then
  echo "Episode JSON missing: $EPISODE" >&2
  exit 1
fi

# 2. Invoke kamishibai CLI independently (no Python import)
# kamishibai is a separate repo with its own node scripts
KAMISHIBAI_DIR="${KAMISHIBAI_DIR:-/home/bons/kamishibai}"

if ! command -v node >/dev/null 2>&1; then
  echo "node not found; installing kamishibai dependencies..." >&2
fi

# Call render.js with the JSON episode
node "$KAMISHIBAI_DIR/cli/render.js" "$EPISODE" "$OUTPUT"

echo "Kamishibai rendered (loose): $OUTPUT"
