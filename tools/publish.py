#!/usr/bin/env python3
"""Publish a research note (and any exported chart data) to GitHub Pages.

Copies the markdown into data/<today>/<type>.md, stamps a ts into the
frontmatter, rebuilds data/index.json from the filesystem, commits and pushes.
Run with no --md to publish chart data alone.

Usage:
  publish.py --type morning --md /tmp/report.md
  publish.py                       # charts-only / reindex + push
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime

SITE = os.path.expanduser("~/finance/site")
TYPES = ["usclose", "morning", "open", "midday", "close", "evening", "usopen", "special"]


def rebuild_index() -> int:
    items = []
    data_dir = f"{SITE}/data"
    for date in os.listdir(data_dir):
        if not re.match(r"\d{4}-\d{2}-\d{2}$", date):
            continue
        for f in os.listdir(f"{data_dir}/{date}"):
            path = f"{data_dir}/{date}/{f}"
            if f.endswith(".md"):
                rtype = f[:-3]
                ts = ""
                head = open(path).read(400)
                m = re.search(r"^ts:\s*(.+)$", head, re.M)
                if m:
                    ts = m.group(1).strip()
                items.append({"kind": "report", "date": date, "type": rtype,
                              "ts": ts or "—",
                              "order": TYPES.index(rtype) if rtype in TYPES else 9})
            elif f.startswith("charts_") and f.endswith(".json"):
                gen = json.load(open(path)).get("generated", "")
                items.append({"kind": "charts", "date": date, "file": f[:-5],
                              "scope": f[7:-5], "ts": gen[11:16] or "—", "order": 99})
    items.sort(key=lambda x: (x["date"], x["ts"] if x["ts"] != "—" else "00:00"),
               reverse=True)
    for it in items:
        it.pop("order", None)
    with open(f"{data_dir}/index.json", "w") as fh:
        json.dump({"updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                   "items": items}, fh, ensure_ascii=False, indent=1)
    return len(items)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", choices=TYPES)
    ap.add_argument("--md", help="markdown file to publish")
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = ap.parse_args()

    if args.md:
        if not args.type:
            raise SystemExit("--md requires --type")
        os.makedirs(f"{SITE}/data/{args.date}", exist_ok=True)
        text = open(os.path.expanduser(args.md)).read()
        if not text.startswith("---"):
            text = f"---\nts: {datetime.now():%H:%M}\n---\n" + text
        with open(f"{SITE}/data/{args.date}/{args.type}.md", "w") as fh:
            fh.write(text)
        print(f"placed data/{args.date}/{args.type}.md")

    n = rebuild_index()
    print(f"index rebuilt: {n} items")

    subprocess.run(["git", "-C", SITE, "add", "-A"], check=True)
    diff = subprocess.run(["git", "-C", SITE, "diff", "--cached", "--quiet"])
    if diff.returncode != 0:
        subprocess.run(["git", "-C", SITE, "commit", "-q", "-m",
                        f"publish: {datetime.now():%Y-%m-%d %H:%M}"], check=True)
        subprocess.run(["git", "-C", SITE, "push", "-q"], check=True)
        print("pushed -> https://fengjh97.github.io/market-daily/")
    else:
        print("nothing to publish")


if __name__ == "__main__":
    main()
