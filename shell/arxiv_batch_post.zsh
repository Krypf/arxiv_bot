#!/usr/bin/env zsh
# arxiv_batch_post.zsh
# Run arxiv_sequence.applescript N times in Safari (macOS)
#
# Usage:
#   chmod +x arxiv_batch_post.zsh
#   ./arxiv_batch_post.zsh       # prompt for count
#   ./arxiv_batch_post.zsh 10    # pass count as argument
#
# Setup:
#   System Settings > Privacy & Security > Accessibility
#   -> enable Terminal / iTerm2

# ---------- config ----------
SAFARI_DELAY=2  # seconds to wait after Safari is focused
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APPLESCRIPT="${SCRIPT_DIR}/arxiv_sequence.applescript"
LOG="$HOME/arxiv_bot/log.txt"

# ----------------------------

# Check AppleScript file exists
if [[ ! -f "$APPLESCRIPT" ]]; then
  echo "Error: AppleScript not found at '${APPLESCRIPT}'"
  exit 1
fi

# Get count from argument or stdin
if [[ -n "$1" ]]; then
  N=$1
else
  echo "***Get ready to change your account on the browser !***"
  echo -n "How many posts? > "
  read N
fi

# Validate: must be an integer greater than 0
if ! [[ "$N" =~ ^[0-9]+$ ]] || (( N <= 0 )); then
  echo "Error: please enter a positive integer (got: '$N')"
  exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting sequence ${N} times." >> "$LOG"

# Activate Safari
echo "Activating Safari..."
osascript -e 'tell application "Safari" to activate'
sleep $SAFARI_DELAY

echo ""
echo "Running sequence x${N}:"
echo "  T -> Ctrl+Tab -> N -> Cmd+V -> Cmd+Enter -> Ctrl+Shift+Tab"
echo ""

# Main loop
for i in $(seq 1 $N); do
  osascript "$APPLESCRIPT"
  # Generate 0 or 1
  # wait_times=(0.25 0.5 0.75 1.0)
  # wait_time=${wait_times[$((RANDOM % 4))]}  # 0.25, 0.5, 0.75, or 1.0
  echo "  [${i}/${N}] sequence sent at $(date '+%H:%M:%S'); $((N - i)) remaining."
  # sleep $wait_time
done

echo ""
echo "Done: ran sequence ${N} times."
