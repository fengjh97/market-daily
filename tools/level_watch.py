#!/usr/bin/env python3
"""Zero-LLM level watcher: checks configured price levels every launchd cycle.

On a NEW breach (state transition only, with hysteresis re-arm):
  1. macOS desktop notification (instant, no tokens)
  2. append to breaches.log (a Monitor in the Claude session picks this up
     and delivers the interpretation)

State in level_state.json maps "ticker|level" -> true while breached.
"""

import json
import os
import subprocess
import warnings
from datetime import datetime

import yfinance as yf

warnings.filterwarnings("ignore")

TOOLS = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(f"{TOOLS}/levels.json"))
STATE_PATH = f"{TOOLS}/level_state.json"
LOG_PATH = f"{TOOLS}/breaches.log"

state = json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {}
hyst = CFG.get("hysteresis_pct", 0.4) / 100

prices = {}
for lv in CFG["levels"]:
    t = lv["ticker"]
    if t in prices:
        continue
    try:
        h = yf.Ticker(t).history(period="1d", interval="5m")["Close"]
        if len(h):
            prices[t] = float(h.iloc[-1])
    except Exception:
        pass

now = datetime.now().strftime("%Y-%m-%d %H:%M")
for lv in CFG["levels"]:
    t, level, direction = lv["ticker"], lv["level"], lv["direction"]
    key = f"{t}|{level}|{direction}"
    px = prices.get(t)
    if px is None:
        continue
    breached = px < level if direction == "below" else px > level
    if breached and not state.get(key):
        state[key] = True
        arrow = "下破" if direction == "below" else "上破"
        line = (f"{now} | {lv['name']} {px:,.1f} {arrow} {level:,} "
                f"| {lv['tag']} | {lv['note']}")
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
        subprocess.run(["osascript", "-e",
            f'display notification "{lv["name"]} {px:,.0f} {arrow} {level:,} — {lv["tag"]}" '
            f'with title "⚠ 点位警报" sound name "Glass"'], capture_output=True)
    elif not breached and state.get(key):
        # 带滞后的重新武装:回到点位0.4%以外才解除,防反复横跳
        rearm = (px > level * (1 + hyst)) if direction == "below" \
            else (px < level * (1 - hyst))
        if rearm:
            state[key] = False

json.dump(state, open(STATE_PATH, "w"))
