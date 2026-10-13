#!/usr/bin/env bash
# Render any bpy-gen model via Windows Blender.
# Usage: ./render.sh <model_name>
#   model_name: doraemon | pagoda | bear | salmon
set -euo pipefail

SCRIPT_NAME="${1:-doraemon}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RENDER_DIR="$HOME/bpy-gen/outputs"
mkdir -p "$RENDER_DIR"

# Map aliases to script files
case "$SCRIPT_NAME" in
  doraemon|ドラえもん) SCRIPT="tools/doraemon_bpy.py" ;;
  pagoda|五重塔)        SCRIPT="tools/pagoda_bpy.py" ;;
  bear|クマ|木彫り)     SCRIPT="tools/bear_bpy.py" ;;
  salmon|鮭|salmon_bear) SCRIPT="tools/salmon_bear_bpy.py" ;;
  *)
    echo "Unknown model: $SCRIPT_NAME"
    echo "Available: doraemon, pagoda, bear, salmon"
    exit 1
    ;;
esac

# bpy-gen is now at /home/bons/evops/mcp/bpy-gen (not ~/.skills/bpy-gen)
SKILL_DIR="/home/bons/evops/mcp/bpy-gen"
WIN_RENDER_DIR=$(wslpath -w "$RENDER_DIR")
WIN_SCRIPT=$(wslpath -w "$SKILL_DIR/$SCRIPT")
BLENDER="/mnt/c/Program Files/Blender Foundation/Blender 5.0/blender.exe"

OUTPUT_NAME="${TIMESTAMP}_${SCRIPT_NAME}.png"
OUTPUT_FILE="${WIN_RENDER_DIR}\\${OUTPUT_NAME}"

"$BLENDER" --background --python "$WIN_SCRIPT" -- --output "$OUTPUT_FILE"

# Sidecar metadata
SIDECAR="$RENDER_DIR/${TIMESTAMP}_${SCRIPT_NAME}.json"
python3 -c "
import json, datetime, os, sys
meta = {
    'model': '$SCRIPT_NAME',
    'timestamp': '$TIMESTAMP',
    'output': '$OUTPUT_NAME',
    'blender': '5.0',
    'engine': 'BLENDER_WORKBENCH',
    'status': 'ok',
    'created': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
with open('$SIDECAR', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
"

# Log to local JSONL ledger
python3 "$SKILL_DIR/tools/log_render.py" "$SCRIPT_NAME" "$RENDER_DIR/$OUTPUT_NAME" "ok"

# DB lineage log (now writes to main evops database at mcp/db/sotsusei.db)
GEN_ID=$(python3 -c "
import sys
sys.path.insert(0, '$SKILL_DIR')
from tools.db import list_generations
gens = list_generations('$SCRIPT_NAME')
print(gens[-1]['id'] if gens else '')
" 2>/dev/null || echo "")
if [ -n "$GEN_ID" ]; then
    python3 "$SKILL_DIR/tools/db.py" log_render "$GEN_ID" "$RENDER_DIR/$OUTPUT_NAME" "WORKBENCH"
fi

# MEGA sync via MEGAsync local folder
MEGA_DIR="/mnt/c/Users/dance/Documents/MEGA/bpy-gen/outputs"
mkdir -p "$MEGA_DIR"
cp "$RENDER_DIR/$OUTPUT_NAME" "$MEGA_DIR/"
cp "$SIDECAR" "$MEGA_DIR/"
echo "Synced to MEGA (via MEGAsync): bpy-gen/outputs/$OUTPUT_NAME"

echo "Saved: $RENDER_DIR/$OUTPUT_NAME"
echo "Sidecar: $SIDECAR"