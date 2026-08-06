#!/bin/bash
# Zero-LLM auto refresh: re-export chart JSONs and push to Pages.
# Runs from system crontab every 5 min; exits fast outside market hours.
# Sessions (JST): Asia 08:55-15:40 Mon-Fri / US 22:25-23:59 Mon-Fri + 00:00-05:10 Tue-Sat.
set -e
PY="$HOME/.claude/venvs/finance/bin/python"
SITE="$HOME/finance/site"
DOW=$(date +%u)   # 1=Mon .. 7=Sun
HM=$(date +%H%M)

in_asia() { [ "$DOW" -le 5 ] && [ "$HM" -ge 0855 ] && [ "$HM" -le 1540 ]; }
in_us()   { { [ "$DOW" -le 5 ] && [ "$HM" -ge 2225 ]; } ||
            { [ "$DOW" -ge 2 ] && [ "$DOW" -le 6 ] && [ "$HM" -le 0510 ]; }; }

if in_asia; then SCOPES="asia full"
elif in_us; then SCOPES="us full"
else exit 0; fi

DATE=$(date +%Y-%m-%d)
CHANGED_FILES=()
for s in $SCOPES; do
  F="$SITE/data/$DATE/charts_$s.json"
  [ -f "$F" ] && cp "$F" "/tmp/prev_$s.json"
  "$PY" "$SITE/tools/export_charts.py" --scope "$s" >/dev/null
  # 与上一版比较(忽略 generated 时间戳),午休/静止时段不产生垃圾提交
  if [ -f "/tmp/prev_$s.json" ]; then
    if "$PY" - "$F" "/tmp/prev_$s.json" <<'EOF'
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
a.pop("generated", None); b.pop("generated", None)
sys.exit(0 if a == b else 1)   # 相同→exit0→还原文件
EOF
    then git -C "$SITE" checkout -q -- "data/$DATE/charts_$s.json" 2>/dev/null || true
    else CHANGED_FILES+=("data/$DATE/charts_$s.json"); fi
  else CHANGED_FILES+=("data/$DATE/charts_$s.json"); fi
done

if [ "${#CHANGED_FILES[@]}" -gt 0 ]; then
  cd "$SITE"
  # 保证自动提交只包含行情 JSON，让 Pages 的 paths-ignore 稳定生效。
  git add -- "${CHANGED_FILES[@]}"
  git diff --cached --quiet -- "${CHANGED_FILES[@]}" || {
    git commit -q -m "auto: quotes $(date '+%m-%d %H:%M')" -- "${CHANGED_FILES[@]}"
    git push -q
    echo "$(date '+%F %T') pushed ($SCOPES)"
  }
fi

# 点位监视(与行情刷新同频,盘中才会执行到这里)
"$PY" "$SITE/tools/level_watch.py" 2>/dev/null || true
