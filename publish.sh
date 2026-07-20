#!/bin/bash
# Publish market reports to GitHub Pages.
# Copies every HTML from ~/finance/reports into the site, rebuilds the index,
# refreshes latest.html, commits and pushes. Idempotent — safe to run per cycle.
set -e
SITE="$HOME/finance/site"
cp -f "$HOME"/finance/reports/*.html "$SITE/reports/" 2>/dev/null || true

"$HOME/.claude/venvs/finance/bin/python" - <<'EOF'
import json, os, re, shutil

site = os.path.expanduser("~/finance/site")
items = []
for f in os.listdir(f"{site}/reports"):
    m = re.match(r"(report|us_session)_(\d{8})_(\d{4})\.html$", f)
    if m:
        kind, d, t = m.groups()
        items.append({"file": f, "type": kind,
                      "ts": f"{d[:4]}-{d[4:6]}-{d[6:]} {t[:2]}:{t[2:]}"})
items.sort(key=lambda x: x["ts"], reverse=True)
with open(f"{site}/reports/index.json", "w") as fh:
    json.dump(items, fh, ensure_ascii=False, indent=1)
if items:
    shutil.copy(f"{site}/reports/{items[0]['file']}", f"{site}/latest.html")
print(f"indexed {len(items)} reports; latest = {items[0]['file'] if items else 'none'}")
EOF

cd "$SITE"
git add -A
git diff --cached --quiet || git commit -q -m "report: $(date '+%Y-%m-%d %H:%M')"
git push -q origin main 2>/dev/null || git push -qu origin main
echo "published -> https://fengjh97.github.io/market-daily/"
