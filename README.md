# ToolPick
Needs-based AI tool finder: 80 tools in 11 categories, prices copied from official pricing pages, a best-value pick and a free option.
Live: https://toolpick-ai.vercel.app

- `tools.py`: all data. Tool fields: name/url/pricing/price/free/about/why/affiliate (empty = official link). `PRICE_TABLE` holds the entry-plan monthly/annual price and cost per output; also `COMPARISONS`, `JOBS`, `SPONSOR_TIERS`, `CHECKED` date. Never invent prices; write "check site" when unverified.
- `build.py`: `python3 build.py` writes `public/` (index + finder, category pages, /tools/, /compare/, best-ai-tool-for-*, sponsor, newsletter, sitemap, robots, llms.txt, tools.json, og.png).
- `price_history.json` + `snapshot.py`: run `python3 snapshot.py` after each price re-check (after updating CHECKED) to log changes on /price-changes.html.
- `og_data.py`: base64 OG image, used when PIL is missing (e.g. in the Vercel build).
- `affiliates.md`, `growth.md`: monetization research and traffic plan.

## Deploy
Vercel project `toolpick-ai` runs `python3 build.py` itself (install `echo skip`, output `public`). Deploy with the Vercel MCP `create_deployment`, target production, `files` = build.py, tools.py, og_data.py, price_history.json (the MCP allows 4 `$file:` files per call) (inline via `$file:`).
