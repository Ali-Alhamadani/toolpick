# ToolPick
Needs-based AI tool finder: 83 tools in 11 categories, prices copied from official pricing pages, a best-value pick and a free option.
Live: https://toolpick-ai.vercel.app

- `tools.py`: all data. Tool fields: name/url/pricing/price/free/about/why/affiliate (empty = official link). `PRICE_TABLE` holds the entry-plan monthly/annual price and cost per output; also `COMPARISONS`, `JOBS`, `SPONSOR_TIERS`, `CHECKED` date. Never invent prices; write "check site" when unverified.
- `build.py`: `python3 build.py` writes `public/` (index + finder, category pages, /tools/, /compare/, best-ai-tool-for-*, sponsor, newsletter, sitemap, robots, llms.txt, tools.json, og.png).
- `price_history.json` + `snapshot.py`: run `python3 snapshot.py` after each price re-check (after updating CHECKED) to log changes on /price-changes.html.
- `og_data.py`: base64 OG image, used when PIL is missing (e.g. in the Vercel build).
- `affiliates.md`, `growth.md`: monetization research and traffic plan.

## Deploy
Vercel project `toolpick-ai` runs `python3 build.py` itself (install `echo skip`, output `public`). Deploy with the Vercel MCP `create_deployment`, target production, `files` = build.py, tools.py, og_data.py, price_history.json (the MCP allows 4 `$file:` files per call) (inline via `$file:`). Always pass `projectSettings` {framework null, buildCommand `python3 build.py`, installCommand `echo skip`, outputDirectory `public`} plus `skipAutoDetectionConfirmation` 1: on 2026-10-19 a deploy without them skipped the build and served 404 until redeployed.

## AI price changes tracker (/price-changes.html, /price-changes.xml)
Generated automatically by build.py from `price_history.json` snapshots — no manual page edits.
1. Daily-ops edits a price in tools.py (verified on the official pricing page, with `checked` date).
2. Run `python3 snapshot.py YYYY-MM-DD` to add that day's snapshot to price_history.json.
3. Run `python3 build.py`. Any tool whose price text differs from the previous snapshot becomes a card
   (newest first), a "Recent price changes" box on its tool page, and an Atom feed entry. Tools that are
   new in a snapshot (no old value) are not shown as changes.
4. Optional: add a plain-English summary and tag in `PRICE_NOTES` in tools.py, keyed `"YYYY-MM-DD|Tool"`
   (tags: up, down, newplan, correction, currency, changed). Without a note the tag is guessed from the
   highest $ amount (up/down/changed) and a generic summary is used. Notes must only restate the
   documented old/new text. Snapshot artifacts go in `PRICE_SKIP` with a reason.
