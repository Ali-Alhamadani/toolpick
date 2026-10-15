"""Usage: python3 snapshot.py [YYYY-MM-DD]. Run after editing prices in tools.py: records today's CHECKED snapshot into price_history.json (commit it)."""
import json, sys
from tools import CATEGORIES, CHECKED
h = json.load(open("price_history.json"))
D = sys.argv[1] if len(sys.argv) > 1 else CHECKED
h[D] = {t["name"]: {"price": t["price"], "free": t["free"]} for c in CATEGORIES for t in c["tools"]}
json.dump(dict(sorted(h.items())), open("price_history.json", "w"), indent=1, ensure_ascii=False)
print("snapshot", D, len(h[D]), "tools;", len(h), "snapshots")
