"""Builds public/ from tools.py.  Usage: BASE=https://your-site python3 build.py"""
import os, html, json, shutil
from tools import CATEGORIES, CHECKED
BASE = os.environ.get("BASE", "https://toolpick-ai-alhamdaniali10-7277.vercel.app").rstrip("/")
e = html.escape
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#0f1117;color:#e7e9ee;line-height:1.5}
a{color:#7cc4ff}header,main,footer{max-width:1080px;margin:0 auto;padding:20px}h1{margin:.2em 0;font-size:2.2rem}.tag{color:#9aa3b2}
.needs{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.needs button{background:#1a1e29;color:#e7e9ee;border:1px solid #2c3242;border-radius:999px;padding:10px 18px;font-size:1rem;cursor:pointer}
.needs button.on{background:#3b82f6;border-color:#3b82f6}section{display:none}section.on{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}.card{background:#171b25;border:1px solid #262c3a;border-radius:12px;padding:16px}
.card h3{margin:0 0 4px}.best{border:2px solid #22c55e}.badge{display:inline-block;font-size:.75rem;font-weight:700;padding:2px 8px;border-radius:6px;margin-right:6px}
.b-best{background:#22c55e;color:#06210f}.b-free{background:#facc15;color:#2a2200}.price{font-weight:600}.check{color:#fb923c}.small{font-size:.85rem;color:#9aa3b2}
.pick{background:#122119;border:1px solid #1f5133;border-radius:12px;padding:14px;margin:12px 0}.freealt{background:#211e10;border:1px solid #4d4313;border-radius:12px;padding:14px;margin:12px 0}"""
def card(t, c):
    best = t["name"] == c["best"]; free = t["name"] in c["free"]
    badges = ("<span class='badge b-best'>BEST VALUE</span>" if best else "") + ("<span class='badge b-free'>FREE OPTION</span>" if free else "")
    pc = "price check" if t["price"] == "check site" else "price"
    return f"""<div class="card{' best' if best else ''}">{badges}<h3>{e(t['name'])}</h3><p>{e(t['about'])}</p>
<p class="{pc}">💲 {e(t['price'])}</p><p>🆓 {e(t['free'])}</p>
<p class="small"><a href="{e(t['url'])}" rel="noopener" target="_blank">Official site</a> · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Pricing page</a> · checked {CHECKED}</p></div>"""
def section(c, i):
    b = next(t for t in c["tools"] if t["name"] == c["best"])
    return f"""<section id="{c['id']}" class="{'on' if i==0 else ''}"><h2>{e(c['need'])}</h2>
<div class="pick"><span class="badge b-best">BEST VALUE</span><b>{e(b['name'])}</b> — {e(b.get('why',''))}</div>
<div class="freealt"><span class="badge b-free">FREE ALTERNATIVES</span>{', '.join(e(n) for n in c['free'])}</div>
<div class="grid">{''.join(card(t,c) for t in c['tools'])}</div></section>"""
total = sum(len(c["tools"]) for c in CATEGORIES)
desc = f"Pick what you need (video, writing, coding, images, audio) and see {total} AI tools with verified prices, a best-value pick and free alternatives."
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ToolPick — find the right AI tool for your need</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}/">
<style>{CSS}</style></head><body><header><h1>ToolPick</h1><p class="tag">{e(desc)}</p>
<div class="needs" role="tablist">{''.join(f'<button data-id="{c["id"]}" class="{"on" if i==0 else ""}">{e(c["name"])}</button>' for i,c in enumerate(CATEGORIES))}</div></header>
<main>{''.join(section(c,i) for i,c in enumerate(CATEGORIES))}</main>
<footer class="small">Prices copied from each tool's official pricing page on {CHECKED} (USD; yearly-billing prices in parentheses). "check site" = we could not verify the price, so we don't guess. Prices change — always confirm on the official page. No affiliate links.</footer>
<script>const b=document.querySelectorAll('.needs button');function show(id){{b.forEach(x=>x.classList.toggle('on',x.dataset.id==id));document.querySelectorAll('section').forEach(s=>s.classList.toggle('on',s.id==id));}}
b.forEach(x=>x.onclick=()=>{{show(x.dataset.id);history.replaceState(null,'','#'+x.dataset.id)}});if(location.hash)show(location.hash.slice(1));</script></body></html>"""
shutil.rmtree("public", ignore_errors=True); os.makedirs("public")
open("public/index.html","w").write(page)
open("public/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open("public/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}/</loc><lastmod>{CHECKED}</lastmod></url></urlset>')
open("public/tools.json","w").write(json.dumps({"checked":CHECKED,"categories":CATEGORIES},indent=1))
print("built", total, "tools:", {c["id"]:len(c["tools"]) for c in CATEGORIES})
