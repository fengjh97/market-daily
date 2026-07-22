#!/bin/bash
# Headless Claude report dispatcher — invoked by launchd at scheduled times.
# Usage: report_cron.sh <usclose|morning|open|midday|close|evening|usopen>
# Runs a fresh `claude -p` with the corresponding self-contained prompt.
set -e
TYPE="$1"
TOOLS="$HOME/finance/site/tools"
LOG="$TOOLS/claude_cron.log"
DOW=$(date +%u)   # 1=Mon .. 7=Sun

# Weekend gating: usclose covers the prior US session (runs Tue-Sat);
# everything else follows the Asia/US weekday (Mon-Fri).
case "$TYPE" in
  usclose) [ "$DOW" -ge 2 ] && [ "$DOW" -le 6 ] || exit 0 ;;
  *)       [ "$DOW" -le 5 ] || exit 0 ;;
esac

PROMPT_FILE="$TOOLS/prompts/$TYPE.txt"
[ -f "$PROMPT_FILE" ] || { echo "$(date '+%F %T') missing prompt $TYPE" >> "$LOG"; exit 1; }

echo "$(date '+%F %T') start $TYPE" >> "$LOG"
cd "$HOME/finance"
/opt/homebrew/bin/claude -p "$(cat "$PROMPT_FILE")" \
  --dangerously-skip-permissions \
  --max-turns 40 \
  >> "$LOG" 2>&1
echo "$(date '+%F %T') done $TYPE (exit $?)" >> "$LOG"
