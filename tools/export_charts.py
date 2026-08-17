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
import re
import warnings
from datetime import datetime
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

SITE = os.path.expanduser("~/finance/site")

ASIA = [
    ("日本", "^N225", "日经225", "点"),
    ("日本", "1306.T", "TOPIX ETF", "日元"),
    ("日本", "7203.T", "丰田", "日元"),
    ("日本", "285A.T", "铠侠", "日元"),
    ("日本", "9984.T", "软银集团", "日元"),
    ("日本", "8035.T", "东京电子", "日元"),
    ("日本", "6857.T", "Advantest", "日元"),
    ("韩国", "^KS11", "KOSPI", "点"),
    ("韩国", "000660.KS", "SK海力士", "韩元"),
]
US = [
    ("美国", "SPY", "标普500 ETF", "美元"),
    ("美国", "QQQ", "纳指100 ETF", "美元"),
    ("美国", "SMH", "半导体 ETF", "美元"),
    ("美国", "NVDA", "英伟达", "美元"),
    ("美国", "MU", "美光", "美元"),
    ("美国", "TSM", "台积电ADR", "美元"),
]
MACRO = [
    ("宏观", "JPY=X", "USDJPY", "日元/美元"),
    ("宏观", "^VIX", "VIX恐慌指数", "点"),
    ("宏观", "^TNX", "美国10年期国债收益率", "%"),
    ("宏观", "DX-Y.NYB", "美元指数DXY", "点"),
    ("期货", "ES=F", "标普500期货", "点"),
    ("期货", "NQ=F", "纳斯达克100期货", "点"),
    ("期货", "NKD=F", "日经225美元期货", "点"),
    ("宏观", "GC=F", "黄金", "美元/盎司"),
    ("宏观", "BZ=F", "Brent原油", "美元/桶"),
]
ASIA_MACRO_TICKERS = {"JPY=X", "^VIX", "NKD=F", "GC=F", "BZ=F"}
ASIA_MACRO = [row for row in MACRO if row[1] in ASIA_MACRO_TICKERS]

SCOPES = {
    "full": {"title": "全市场 · 日韩美+宏观", "rows": ASIA + US + MACRO,
             "scenarios": ["^N225", "SMH", "JPY=X", "GC=F"]},
    "asia": {"title": "亚洲 · 日韩", "rows": ASIA + ASIA_MACRO,
             "scenarios": ["^N225", "285A.T"]},
    "us":   {"title": "美股", "rows": US + MACRO,
             "scenarios": ["SMH", "QQQ"]},
}


YAHOO_JP_LIVE = {"^N225": "998407.O", "1306.T": "1306.T", "7203.T": "7203.T",
                 "285A.T": "285A.T", "9984.T": "9984.T", "8035.T": "8035.T",
                 "6857.T": "6857.T"}
NAVER_LIVE = {
    "^KS11": "https://polling.finance.naver.com/api/realtime/domestic/index/KOSPI",
    "000660.KS": "https://polling.finance.naver.com/api/realtime/domestic/stock/000660",
}


def _number(value):
    if value is None:
        return None
    value = str(value).replace(",", "").replace(" ", "")
    if value in {"", "---", "--:--"}:
        return None
    return float(value)


def parse_yahoo_jp_live(html: str):
    """Parse the server-rendered Yahoo Japan quote summary without JavaScript."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    quote = re.search(
        r"(?:ポートフォリオに追加|日経平均株価)\s+([\d,.]+)\s+前日比\s+"
        r"([+\-]?\s?[\d,.]+)\s+\(\s*([+\-]?\s?[\d,.]+)\s*%\s*\).*?"
        r"(\d{1,2}:\d{2})", text)
    if not quote:
        return None
    fields = {}
    for key in ("前日終値", "始値", "高値", "安値", "出来高"):
        match = re.search(key + r"\s+用語\s+([\d,.-]+)\s+\(\s*([^)]*)\)", text)
        fields[key] = _number(match.group(1)) if match else None
    return {
        "close": _number(quote.group(1)), "change": _number(quote.group(2)),
        "change_pct": _number(quote.group(3)), "time": quote.group(4),
        "previous_close": fields["前日終値"], "open": fields["始値"],
        "high": fields["高値"], "low": fields["安値"],
        "volume": int(fields["出来高"] or 0),
    }


def parse_naver_live(payload: dict):
    rows = payload.get("datas") or []
    if not rows or rows[0].get("marketStatus") not in {"OPEN", "CLOSE"}:
        return None
    row = rows[0]
    stamp = row.get("localTradedAt") or payload.get("time", "")
    close = _number(row.get("closePriceRaw") or row.get("closePrice"))
    change = _number(row.get("compareToPreviousClosePriceRaw") or row.get("compareToPreviousClosePrice"))
    return {
        "close": close, "change": change,
        "change_pct": _number(row.get("fluctuationsRatioRaw") or row.get("fluctuationsRatio")),
        "previous_close": close - change if close is not None and change is not None else None,
        "date": stamp[:10] if "T" in stamp else None,
        "time": stamp[11:16] if "T" in stamp else stamp[8:12],
        "open": _number(row.get("openPriceRaw") or row.get("openPrice")),
        "high": _number(row.get("highPriceRaw") or row.get("highPrice")),
        "low": _number(row.get("lowPriceRaw") or row.get("lowPrice")),
        "volume": int(_number(row.get("accumulatedTradingVolumeRaw") or row.get("accumulatedTradingVolume")) or 0),
    }


def fetch_asia_live(ticker: str):
    """Return a current Tokyo/Seoul bar when Yahoo's daily feed lags the open."""
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    if now.weekday() >= 5 or not (9 <= now.hour < 17):
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "identity"}
        if ticker in YAHOO_JP_LIVE:
            url = f"https://finance.yahoo.co.jp/quote/{YAHOO_JP_LIVE[ticker]}"
            html = urlopen(Request(url, headers=headers), timeout=8).read().decode("utf-8", "ignore")
            live = parse_yahoo_jp_live(html)
            source = "Yahoo! Finance Japan realtime"
        elif ticker in NAVER_LIVE:
            url = NAVER_LIVE[ticker]
            payload = json.loads(urlopen(Request(url, headers=headers), timeout=8).read())
            live = parse_naver_live(payload)
            source = "Naver Finance realtime"
        else:
            return None
        if not live or live.get("close") is None:
            return None
        live.update({"date": live.get("date") or datetime.now().strftime("%Y-%m-%d"),
                     "source": source})
        return live
    except Exception as exc:
        print(f"live fallback unavailable for {ticker}: {exc}")
        return None


def merge_live_bar(history: pd.DataFrame, live: dict):
    index = pd.Timestamp(live["date"])
    if history.index.tz is not None:
        index = index.tz_localize(history.index.tz)
    if history.index[-1].date() > index.date():
        return history
    if history.index[-1].date() == index.date():
        history = history.iloc[:-1]
    close = live["close"]
    row = pd.DataFrame({
        "Open": [live.get("open") or close], "High": [live.get("high") or close],
        "Low": [live.get("low") or close], "Close": [close],
        "Volume": [live.get("volume") or 0],
    }, index=[index])
    return pd.concat([history, row])


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
    for group, ticker, name, unit in cfg["rows"]:
        h_all = yf.Ticker(ticker).history(period="1y", interval="1d")
        if h_all.empty:
            continue
        h_all = h_all.dropna(subset=["Close"])
        live = fetch_asia_live(ticker) if args.scope in {"asia", "full"} else None
        if live and live["date"] >= h_all.index[-1].strftime("%Y-%m-%d"):
            h_all = merge_live_bar(h_all, live)
        h = h_all.tail(126)
        c = h_all["Close"].values
        c6 = h["Close"].values
        last = c[-1]
        ma50 = c[-50:].mean() if len(c) >= 50 else None
        ma200 = c[-200:].mean() if len(c) >= 200 else None
        bb_m, bb_s = c[-20:].mean(), c[-20:].std()
        bb_upper = bb_m + 2 * bb_s
        bb_lower = bb_m - 2 * bb_s
        dashboard.append({
            "group": group, "name": name, "ticker": ticker, "unit": unit,
            "source": live["source"] if live else "Yahoo Finance via yfinance",
            "price_date": h_all.index[-1].strftime("%Y-%m-%d"),
            "last": r(last, 3),
            "change1_abs": r(live["change"], 3) if live and live.get("change") is not None else (r(last - c[-2], 3) if len(c) > 1 else None),
            "d1": r(live["change_pct"], 2) if live and live.get("change_pct") is not None else (r((last / c[-2] - 1) * 100, 2) if len(c) > 1 else None),
            "w1": r((last / c[-6] - 1) * 100, 2) if len(c) > 6 else None,
            "m1": r((last / c[-22] - 1) * 100, 2) if len(c) > 22 else None,
            "rsi": r(rsi14(c), 1),
            "ma50": r(ma50, 3), "ma200": r(ma200, 3),
            "vs50": r((last / ma50 - 1) * 100, 2) if ma50 else None,
            "vs200": r((last / ma200 - 1) * 100, 2) if ma200 else None,
            "bb_upper": r(bb_upper, 3), "bb_lower": r(bb_lower, 3),
            "bbz": r((last - bb_m) / bb_s, 2) if bb_s else None,
            "high_6m": r(c6.max(), 3), "low_6m": r(c6.min(), 3),
            "dd": r((last / c6.max() - 1) * 100, 2),
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
           "data_source": "Yahoo Finance via yfinance; Tokyo/Seoul realtime fallback when daily bars lag",
           "scope": args.scope, "title": cfg["title"],
           "dashboard": dashboard, "charts": charts, "scenarios": scenarios}
    path = f"{outdir}/charts_{args.scope}.json"
    with open(path, "w") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"exported {path} ({os.path.getsize(path)/1e3:.0f} KB, "
          f"{len(charts)} charts, {len(scenarios)} scenarios)")


if __name__ == "__main__":
    main()
