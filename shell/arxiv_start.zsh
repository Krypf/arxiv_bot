#!/usr/bin/env zsh
# arxiv_start.zsh
# Setup launcher for arxiv posting session:
#   1. Open log.txt in VSCode
#   2. Open $HOME/arxiv_bot in Finder
#   3. Open arxiv_poster.html in Safari
#   4. Run arxiv_batch_post.zsh

# ---------- config ----------
ARXIV_DIR="$HOME/arxiv_bot"
LOG_FILE="${ARXIV_DIR}/log.txt"
HTML_FILE="${ARXIV_DIR}/src/arxiv_poster.html"
# SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BATCH_SCRIPT="${ARXIV_DIR}/shell/arxiv_batch_post.zsh"
# ----------------------------

# Check files exist
if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: log.txt not found at '${LOG_FILE}'"
  exit 1
fi

if [[ ! -f "$HTML_FILE" ]]; then
  echo "Error: arxiv_poster.html not found at '${HTML_FILE}'"
  exit 1
fi

if [[ ! -f "$BATCH_SCRIPT" ]]; then
  echo "Error: arxiv_batch_post.zsh not found at '${BATCH_SCRIPT}'"
  exit 1
fi

# 1. Open log.txt in VSCode
echo "[1/4] Opening log.txt in VSCode..."
code "$LOG_FILE"

# 2. Open arxiv_bot directory in Finder
echo "[2/4] Opening Finder at ${ARXIV_DIR}..."
open "$ARXIV_DIR/data"

# 3. Open arxiv_poster.html in Safari
echo "[3/4] Opening arxiv_poster.html in Safari..."
open -a Safari "$HTML_FILE"
open -a Safari "https://x.com/home"

# 4. Copy batch script
echo "[4/4] Copying batch post script command to clipboard..."
COMMAND="sh shell/arxiv_batch_post.zsh"
echo "$COMMAND"
echo "$COMMAND" | pbcopy
echo "Get ready to change your account on the browser !"