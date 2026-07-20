#!/usr/bin/env python3
"""Export chart data JSON for the static charts.html template.

This is the zero-token data producer: OHLCV series, dashboard metrics and
bootstrap scenario cones, written to site/data/<date>/charts_<scope>.json.
The rendering logic lives once in assets/app.js — this ships numbers only.

Usage:
  ~/.claude/venvs/finance/bin/python ~/finance/site/tools/export_charts.py --scope full
  (scopes: full | asia | us)
"""

import argparse
import json
import os
import warnings
from datetime import datetime

import numpy as np
import yfinance as yf

warnings.filterwarnings("ignore")

SITE = os.path.expanduser("~/finance/site")

ASIA = [("日本", "^N225", "日经225"), ("日本", "1306.T", "TOPIX ETF"),
        ("日本", "7203.T", "丰田"), ("日本", "285A.T", "铠侠"),
        ("日本", "9984.T", "软银G"), ("日本", "8035.T", "东京电子"),
        ("日本", "6857.T", "Advantest"),
        ("韩国", "^KS11", "KOSPI"), ("韩国", "000660.KS", "SK海力士")]
US = [("美国", "SPY", "标普500 ETF"), ("美国", "QQQ", "纳指100 ETF"),
      ("美国", "SMH", "费半 ETF"), ("美国", "NVDA", "英伟达"),
      ("美国", "MU", "美光"), ("美国", "TSM", "台积电")]
MACRO = [("宏观", "JPY=X", "USDJPY"), ("宏观", "GC=F", "黄金"), ("宏观", "BZ=F", "Brent原油")]

SCOPES = {
    "full": {"title": "全市场 · 日韩美+宏观", "rows": ASIA + US + MACRO,
             "scenarios": ["^N225", "SMH", "JPY=X", "GC=F"]},
    "asia": {"title": "亚洲 · 日韩", "rows": ASIA + MACRO[:1],
             "scenarios": ["^N225", "285A.T"]},
    "us":   {"title": "美股", "rows": US + MACRO,
             "scenarios": ["SMH", "QQQ"]},
}


def rsi14(c: np.ndarray):
    if len(c) < 20:
        return None
    d = np.diff(c)
    up, dn = np.where(d > 0, d, 0.0), np.where(d < 0, -d, 0.0)
    a = 1 / 14
    au, ad = up[0], dn[0]
    for i in range(1, len(d)):
        au = a * up[i] + (1 - a) * au
        ad = a * dn[i] + (1 - a) * ad
    return None if ad == 0 else 100 - 100 / (1 + au / ad)


def r(x, nd=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), nd)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=list(SCOPES), default="full")
    args = ap.parse_args()
    cfg = SCOPES[args.scope]

    today = datetime.now().strftime("%Y-%m-%d")
    outdir = f"{SITE}/data/{today}"
    os.makedirs(outdir, exist_ok=True)

    events = []
    ev_path = f"{SITE}/data/events.json"
    if os.path.exists(ev_path):
        events = json.load(open(ev_path))

    dashboard, charts, scenarios = [], [], []
    for group, ticker, name in cfg["rows"]:
        h = yf.Ticker(ticker).history(period="6mo", interval="1d")
        if h.empty:
            continue
        h = h.dropna(subset=["Close"])
        c = h["Close"].values
        last = c[-1]
        ma50 = c[-50:].mean() if len(c) >= 50 else None
        ma200 = c[-200:].mean() if len(c) >= 120 else None
        bb_m, bb_s = c[-20:].mean(), c[-20:].std()
        dashboard.append({
            "group": group, "name": name, "ticker": ticker, "last": r(last, 2),
            "d1": r((last / c[-2] - 1) * 100, 2) if len(c) > 1 else None,
            "w1": r((last / c[-6] - 1) * 100, 2) if len(c) > 6 else None,
            "m1": r((last / c[-22] - 1) * 100, 2) if len(c) > 22 else None,
            "rsi": r(rsi14(c), 1),
            "vs50": r((last / ma50 - 1) * 100, 2) if ma50 else None,
            "vs200": r((last / ma200 - 1) * 100, 2) if ma200 else None,
            "bbz": r((last - bb_m) / bb_s, 2) if bb_s else None,
            "dd": r((last / c.max() - 1) * 100, 2),
        })
        charts.append({
            "name": name, "ticker": ticker,
            "dates": [d.strftime("%Y-%m-%d") for d in h.index],
            "o": [r(x, 3) for x in h["Open"]], "h": [r(x, 3) for x in h["High"]],
            "l": [r(x, 3) for x in h["Low"]], "c": [r(x, 3) for x in h["Close"]],
            "v": [int(x) for x in h["Volume"].fillna(0)],
        })
        if ticker in cfg["scenarios"]:
            h2 = yf.Ticker(ticker).history(period="2y", interval="1d")["Close"].dropna()
            rets = h2.pct_change().dropna().values
            rng = np.random.default_rng(42)
            paths = h2.iloc[-1] * np.cumprod(1 + rng.choice(rets, size=(500, 10)), axis=1)
            import pandas as pd
            days = pd.bdate_range(h2.index[-1] + pd.Timedelta(days=1), periods=10)
            pct = {p: np.percentile(paths, p, axis=0) for p in (5, 25, 50, 75, 95)}
            scenarios.append({
                "name": name, "ticker": ticker,
                "histDates": [d.strftime("%Y-%m-%d") for d in h2.index[-40:]],
                "histClose": [r(x, 3) for x in h2.iloc[-40:]],
                "days": [d.strftime("%Y-%m-%d") for d in days],
                **{f"p{p}": [r(x, 3) for x in pct[p]] for p in (5, 25, 50, 75, 95)},
                "events": events,
                "range": [r((pct[5][-1] / h2.iloc[-1] - 1) * 100, 1),
                          r((pct[95][-1] / h2.iloc[-1] - 1) * 100, 1)],
            })

    out = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
           "scope": args.scope, "title": cfg["title"],
           "dashboard": dashboard, "charts": charts, "scenarios": scenarios}
    path = f"{outdir}/charts_{args.scope}.json"
    with open(path, "w") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"exported {path} ({os.path.getsize(path)/1e3:.0f} KB, "
          f"{len(charts)} charts, {len(scenarios)} scenarios)")


if __name__ == "__main__":
    main()
