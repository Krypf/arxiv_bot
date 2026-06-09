#!/usr/bin/env zsh
# open_json.zsh
# Read a JSON file, log its filename and item count, then open arxiv_poster.html in Safari
#
# Usage (from $HOME/arxiv_bot in VSCode terminal):
#   ./shell/open_json.zsh gr-qc-2026-06-03        # no extension
#   ./shell/open_json.zsh gr-qc-2026-06-03.json   # with extension

# ---------- config ----------
ARXIV_DIR="$HOME/arxiv_bot"
HTML_FILE="${ARXIV_DIR}/src/arxiv_poster.html"
LOG="${ARXIV_DIR}/log.txt"
# ----------------------------

# ---------- argument ----------
if [[ -z "$1" ]]; then
  ARG=$(osascript shell/check_category.applescript)
  if [[ -z "$ARG" ]]; then
    echo "Error: could not read filename from Safari tab"
    exit 1
  fi
  echo "  (read from Safari: ${ARG})"
else
  ARG="$1" # Normalize input to absolute path
fi
# 1. Strip .json if present, then re-add
ARG="${ARG%.json}.json"
# 2. Extract basename (strip any directory prefix)
BASENAME_ARG="$(basename "$ARG" .json)"
# 3. Extract category (e.g. gr-qc from gr-qc-2026-06-03)
CATEGORY="${BASENAME_ARG%%-[0-9]*}"
# 4. Build absolute path
JSON_FILE="${ARXIV_DIR}/data/${CATEGORY}/${BASENAME_ARG}.json"

if [[ ! -f "$JSON_FILE" ]]; then
  echo "Error: file not found: '$JSON_FILE'"
  exit 1
fi

if [[ ! -f "$HTML_FILE" ]]; then
  echo "Error: arxiv_poster.html not found at '${HTML_FILE}'"
  exit 1
fi

# ---------- parse JSON ----------
BASENAME="$(basename "$JSON_FILE" .json)"

ITEM_COUNT=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    d = json.load(f)
print(len(d))
" "$JSON_FILE" 2>/dev/null)

if [[ -z "$ITEM_COUNT" ]]; then
  echo "Error: failed to parse JSON"
  exit 1
fi

# ---------- output ----------
echo ""
echo "  file   : $BASENAME.json"
echo "  items  : $ITEM_COUNT"
echo ""

# ---------- log ----------
mkdir -p "$(dirname "$LOG")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] open_json: file=${BASENAME}.json items=${ITEM_COUNT}" >> "$LOG"

# ---------- confirm ----------
echo -n "  ${BASENAME_ARG}.json (${ITEM_COUNT} items) — continue? (y/n/number): "
read user_input
if [[ "$user_input" =~ ^[0-9]+$ ]]; then
  ITEM_COUNT=$user_input
elif [[ "$user_input" != "y" ]]; then
  exit 1
fi

# ---------- open in Safari ----------
sh shell/arxiv_batch_post.zsh "$ITEM_COUNT"