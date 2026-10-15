"""Builds public/ from tools.py.  Usage: BASE=https://your-site python3 build.py
Pages: index, /best-ai-<category>-tools.html, /tools/<slug>.html, /compare/<slug>.html, sitemap, robots, tools.json"""
import os, re, html, json, shutil
from tools import CATEGORIES, CHECKED, COMPARISONS, PRICE_TABLE, JOBS, SPONSOR_TIERS
BASE = os.environ.get("BASE", "https://toolpick-ai-alhamdaniali10-7277.vercel.app").rstrip("/")
e = html.escape
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#0f1117;color:#e7e9ee;line-height:1.55}
a{color:#7cc4ff}header,main,footer{max-width:1080px;margin:0 auto;padding:18px 20px}h1{margin:.2em 0;font-size:2rem}.tag{color:#9aa3b2}nav a{margin-right:14px}
.needs{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.needs button{background:#1a1e29;color:#e7e9ee;border:1px solid #2c3242;border-radius:999px;padding:10px 18px;font-size:1rem;cursor:pointer}
.needs button.on{background:#3b82f6;border-color:#3b82f6}.tabs section{display:none}.tabs section.on{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}.card{background:#171b25;border:1px solid #262c3a;border-radius:12px;padding:16px}
.card h3{margin:0 0 4px}.best{border:2px solid #22c55e}.badge{display:inline-block;font-size:.75rem;font-weight:700;padding:2px 8px;border-radius:6px;margin-right:6px}
.b-best{background:#22c55e;color:#06210f}.b-free{background:#facc15;color:#2a2200}.price{font-weight:600}.check{color:#fb923c}.small{font-size:.85rem;color:#9aa3b2}
.pick{background:#122119;border:1px solid #1f5133;border-radius:12px;padding:14px;margin:12px 0}.freealt{background:#211e10;border:1px solid #4d4313;border-radius:12px;padding:14px;margin:12px 0}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #2c3242;padding:10px;text-align:left;vertical-align:top}th{background:#1a1e29}.tw{overflow-x:auto}.sponsor{border:1px dashed #6b7280;border-radius:12px;padding:14px;margin:12px 0;color:#9aa3b2}.finder{background:#171b25;border:1px solid #262c3a;border-radius:12px;padding:16px;margin:16px 0}.finder input,.finder select{background:#0f1117;color:#e7e9ee;border:1px solid #2c3242;border-radius:8px;padding:10px;font-size:1rem;margin:4px 6px 4px 0}.finder input[type=text]{width:100%}.res{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:12px}@media(max-width:600px){h1{font-size:1.5rem}nav a{display:inline-block;margin:4px 10px 4px 0}.finder select{width:100%}td,th{padding:6px;font-size:.9rem}}.btn{display:inline-block;background:#3b82f6;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none}"""
FOOT = f"""<footer class="small"><p><a href="/sponsor.html">Sponsor ToolPick</a> · <a href="/newsletter.html">Newsletter</a> · <a href="/llms.txt">llms.txt</a></p>Some links may become affiliate links in future; that never changes our picks. Prices copied from each tool's official pricing page on {CHECKED} (USD unless shown; yearly-billing prices in parentheses). "check site" = we could not verify the price, so we don't guess. Prices change — always confirm on the official page.</footer>"""
def page(path, title, desc, body, ld=None):
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    full = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>{lds}</head><body><header><nav><a href="/"><b>ToolPick</b></a>{''.join(f'<a href="/best-ai-{c["id"]}-tools.html">{e(c["name"])}</a>' for c in CATEGORIES)}</nav></header>
<main>{body}</main>{FOOT}</body></html>"""
    fp = "public" + (path if not path.endswith("/") else path + "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, "w").write(full); URLS.append(path)
def crumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}
def proscons(t, c):
    pros, cons = [t["about"]], []
    f = t["free"].lower(); p = t["price"]
    if f == "check site": cons.append("Free-tier details not verified — check the official site")
    elif f.startswith("no free"): cons.append("No free plan listed")
    elif "trial" in f and "free plan" not in f and "free:" not in f: pros.append(t["free"]); cons.append("No permanent free plan, trial only")
    else: pros.append("Has a free option: " + t["free"])
    if p == "check site": cons.append("Price could not be verified on the pricing page")
    if t["name"] == c["best"]: pros.append("ToolPick best-value pick for " + c["name"].lower())
    return pros, cons
URLS = []
for _c in CATEGORIES:
    for _t in _c['tools']:
        _t.setdefault('affiliate', '')
        m,a,po = PRICE_TABLE.get(_t['name'], (None,None,None)); _t['monthly'],_t['annual'],_t['per_output'] = m,a,po
fmt = lambda v: '—' if v is None else (v if isinstance(v,str) else f'${v:g}')
shutil.rmtree("public", ignore_errors=True); os.makedirs("public")
tool_pages = {}
for c in CATEGORIES:
    for t in c["tools"]: tool_pages.setdefault(t["name"], []).append(c)
def turl(n): return f"/tools/{slug(n)}.html"
def card(t, c):
    best = t["name"] == c["best"]; free = t["name"] in c["free"]
    badges = ("<span class='badge b-best'>BEST VALUE</span>" if best else "") + ("<span class='badge b-free'>FREE OPTION</span>" if free else "")
    pc = "price check" if t["price"] == "check site" else "price"
    return f"""<div class="card{' best' if best else ''}">{badges}<h3><a href="{turl(t['name'])}">{e(t['name'])}</a></h3><p>{e(t['about'])}</p>
<p class="{pc}">💲 {e(t['price'])}</p><p>🆓 {e(t['free'])}</p>
<p class="small"><a href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Official site</a> · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Pricing page</a> · checked {CHECKED}</p></div>"""
def picks(c):
    b = next(t for t in c["tools"] if t["name"] == c["best"])
    return f"""<div class="pick"><span class="badge b-best">BEST VALUE</span><b><a href="{turl(b['name'])}">{e(b['name'])}</a></b> — {e(b.get('why',''))}</div>
<div class="freealt"><span class="badge b-free">FREE ALTERNATIVES</span>{', '.join(f'<a href="{turl(n)}">{e(n)}</a>' for n in c['free'])}</div>"""
def comps_for(names): return [x for x in COMPARISONS if x[2] in names or x[3] in names]
def complinks(lst): return ("<h2>Comparisons</h2><ul>" + "".join(f'<li><a href="/compare/{s}.html">{e(ti)}</a></li>' for s,ti,*_ in lst) + "</ul>") if lst else ""
total_tools = len(tool_pages)
# index
FDATA = json.dumps([dict(n=t["name"],c=c["id"],cn=c["name"],u=turl(t["name"]),p=t["price"],f=t["free"],a=t["about"]+" "+c["need"],
    m=min([v for v in (t["monthly"],t["annual"]) if isinstance(v,(int,float))],default=None),b=t["name"]==c["best"],fr=t["name"] in c["free"]) for c in CATEGORIES for t in c["tools"]])
FOPTS = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)
FINDER = ('''<div class="finder"><h2 style="margin-top:0">What do you need?</h2><input type="text" id="q" placeholder="e.g. turn my podcast into short clips, cheap voiceover, pitch deck for investors">
<div><select id="cat"><option value="">Any use case</option>''' + FOPTS + '''</select>
<select id="budget"><option value="any">Any budget</option><option value="0">Free only</option><option value="15">Up to $15/mo</option><option value="30">Up to $30/mo</option><option value="100">Up to $100/mo</option></select>
<select id="skill"><option value="beginner">Beginner</option><option value="pro">Pro / power user</option></select></div><div id="out"></div></div>
<script>const D=''' + FDATA.replace("</", "<\\/") + r''';
const SW=new Set('the and for with into turn make want need some best good cheap free tool tools that this from your using use help'.split(' '));const hasFree=t=>t.fr||(/free|\$0/i.test(t.f)&&!/^(no free|check site)/i.test(t.f)&&!/trial/i.test(t.f));
function run(){const q=document.getElementById('q').value.toLowerCase().split(/\W+/).filter(w=>w.length>2&&!SW.has(w)),c=document.getElementById('cat').value,bu=document.getElementById('budget').value,sk=document.getElementById('skill').value;
let L=D.filter(t=>!c||t.c==c).map(t=>{let s=0;const h=(t.n+' '+t.a+' '+t.cn+' '+t.c).toLowerCase();q.forEach(w=>{if(h.includes(w))s+=3;else if(h.includes(w.slice(0,5)))s+=1});if(t.b)s+=2;if(hasFree(t)&&sk=='beginner')s+=1.5;if(t.m!=null&&sk=='pro')s+=0.5;return Object.assign({s},t)});
if(q.length&&!c){const mx=Math.max(...L.map(t=>t.s));if(mx>2)L=L.filter(t=>t.s>=2)}
if(bu=='0')L=L.filter(hasFree);else if(bu!='any')L=L.filter(t=>hasFree(t)||(t.m!=null&&t.m<=+bu));
L.sort((x,y)=>y.s-x.s);const seen=new Set();L=L.filter(t=>!seen.has(t.n)&&seen.add(t.n));
const top=L.slice(0,3),bv=L.filter(t=>t.b)[0]||L.filter(t=>t.m!=null).sort((x,y)=>x.m-y.m)[0],fo=L.filter(hasFree)[0];
const card=(t,lab)=>t?`<div class="card"><span class="badge ${lab=='FREE OPTION'?'b-free':'b-best'}">${lab}</span><h3><a href="${t.u}">${t.n}</a></h3><p class="small">${t.cn}</p><p class="price">💲 ${t.p}</p><p>🆓 ${t.f}</p></div>`:'';
document.getElementById('out').innerHTML=L.length?`<h3>Top matches</h3><div class="res">${top.map((t,i)=>card(t,'#'+(i+1))).join('')}</div><h3>Best value &amp; free option</h3><div class="res">${card(bv,'BEST VALUE')}${card(fo,'FREE OPTION')}</div>`:'<p>No match, try a broader budget or use case.</p>'}
['q','cat','budget','skill'].forEach(i=>document.getElementById(i).addEventListener('input',run));run();</script>''')
desc = f"Tell us what you need and compare {total_tools} AI tools across {len(CATEGORIES)} categories — prices checked on official pages, a best-value pick and a free option."
body = f"""<h1>Find the right AI tool for your need</h1><p class="tag">{e(desc)}</p>{FINDER}
<div class="needs">{''.join(f'<button data-id="{c["id"]}" class="{"on" if i==0 else ""}">{e(c["name"])}</button>' for i,c in enumerate(CATEGORIES))}</div><div class="tabs">
{''.join(f'<section id="{c["id"]}" class="{"on" if i==0 else ""}"><h2>{e(c["need"])}</h2>{picks(c)}<div class="grid">{"".join(card(t,c) for t in c["tools"])}</div><p><a href="/best-ai-{c["id"]}-tools.html">Full guide: best AI {e(c["name"].lower())} tools →</a></p></section>' for i,c in enumerate(CATEGORIES))}</div>
{complinks(COMPARISONS)}<h2>Best AI tool for…</h2><ul>{"".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS)}</ul>
<script>const b=document.querySelectorAll('.needs button');function show(id){{b.forEach(x=>x.classList.toggle('on',x.dataset.id==id));document.querySelectorAll('.tabs section').forEach(s=>s.classList.toggle('on',s.id==id));}}
b.forEach(x=>x.onclick=()=>{{show(x.dataset.id);history.replaceState(null,'','#'+x.dataset.id)}});if(location.hash)show(location.hash.slice(1));</script>"""
page("/", "ToolPick — find the right AI tool for your need (verified prices)", desc, body,
     [{"@context":"https://schema.org","@type":"WebSite","name":"ToolPick","url":BASE+"/"}])
# category pages
for c in CATEGORIES:
    path = f"/best-ai-{c['id']}-tools.html"; n = c["name"]
    title = f"Best AI {n} Tools ({CHECKED[:4]}): Prices, Free Plans & Best Value"
    d = f"{len(c['tools'])} AI {n.lower()} tools compared with prices checked {CHECKED}. Best value: {c['best']}. Free options: {', '.join(c['free'])}."
    rows = "".join(f"<tr><td><a href='{turl(t['name'])}'>{e(t['name'])}</a></td><td>{fmt(t['monthly'])}</td><td>{fmt(t['annual'])}</td><td>{e(t['per_output'] or '—')}</td><td>{e(t['price'])}</td><td>{e(t['free'])}</td><td>{CHECKED}</td></tr>" for t in c["tools"])
    body = f"""<h1>Best AI {e(n.lower())} tools</h1><p class="tag">{e(d)}</p>{picks(c)}
<div class="sponsor">Sponsored slot available for this category — <a href="/sponsor.html">sponsor ToolPick</a></div>
<h2>Price table</h2><p class="small">Entry paid plan. Monthly = billed monthly; Annual = per-month cost when billed yearly. "—" = not shown/verified on the official page.</p>
<div class="tw"><table><tr><th>Tool</th><th>Monthly</th><th>Annual (per mo)</th><th>Cost per output</th><th>All plans</th><th>Free tier</th><th>Checked</th></tr>{rows}</table></div><h2>All tools</h2><div class="grid">{''.join(card(t,c) for t in c['tools'])}</div>
{complinks(comps_for([t['name'] for t in c['tools']]))}"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(c["tools"])]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Best AI {n} tools",path)])])
# tool pages
for name, cats in tool_pages.items():
    c = cats[0]; t = next(x for x in c["tools"] if x["name"] == name); path = turl(name)
    pros, cons = proscons(t, c)
    title = f"{name} Pricing & Free Plan ({CHECKED[:7]}) — Pros, Cons, Alternatives"
    d = f"{name} pricing checked {CHECKED}: {t['price']}. Free tier: {t['free']}. Pros, cons and alternatives."[:300]
    alts = [x["name"] for cc in cats for x in cc["tools"] if x["name"] != name]
    body = f"""<h1>{e(name)} pricing &amp; review</h1><p class="tag">{e(t['about'])}</p>
<table><tr><th>Price</th><td class="{'check' if t['price']=='check site' else ''}">{e(t['price'])}</td></tr><tr><th>Free tier</th><td>{e(t['free'])}</td></tr>
<tr><th>Categories</th><td>{', '.join(f'<a href="/best-ai-{cc["id"]}-tools.html">{e(cc["name"])}</a>' for cc in cats)}</td></tr><tr><th>Checked</th><td>{CHECKED} on the <a href="{e(t['pricing'])}" rel="noopener">official pricing page</a></td></tr></table>
<h2>Pros</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in pros)}</ul><h2>Cons</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in cons) or '<li>Paid features require a subscription — compare plans on the official page</li>'}</ul>
<p><a class="btn" href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Visit {e(name)} official site</a></p>
<h2>Alternatives</h2><ul>{''.join(f'<li><a href="{turl(a)}">{e(a)}</a></li>' for a in dict.fromkeys(alts))}</ul>{complinks(comps_for([name]))}"""
    sw = {"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"applicationCategory":"BusinessApplication","operatingSystem":"Web","url":t["url"],"description":t["about"]}
    page(path, title, d, body, [sw, crumbs([("ToolPick","/"),(f"Best AI {c['name']} tools",f"/best-ai-{c['id']}-tools.html"),(name,path)])])
# comparison pages
def find(n): return next(x for c in CATEGORIES for x in c["tools"] if x["name"] == n)
for s, title0, a, b, cid in COMPARISONS:
    A, B = find(a), find(b); path = f"/compare/{s}.html"; c = next(x for x in CATEGORIES if x["id"] == cid)
    title = f"{title0} ({CHECKED[:4]}): Price, Free Plan & Which to Pick"
    d = f"{a} vs {b} compared with prices checked {CHECKED} on official pricing pages: plans, free tiers and which is better value."
    verdict = f"ToolPick's best-value pick for {c['name'].lower()} is <a href='{turl(c['best'])}'>{e(c['best'])}</a>." 
    if c["best"] not in (a, b): verdict += f" Between these two, compare the entry prices above; pick the one whose free tier lets you test your exact use case."
    body = f"""<h1>{e(title0)}</h1><p class="tag">{e(d)}</p><table><tr><th></th><th><a href="{turl(a)}">{e(a)}</a></th><th><a href="{turl(b)}">{e(b)}</a></th></tr>
<tr><th>What it is</th><td>{e(A['about'])}</td><td>{e(B['about'])}</td></tr><tr><th>Price</th><td>{e(A['price'])}</td><td>{e(B['price'])}</td></tr>
<tr><th>Free tier</th><td>{e(A['free'])}</td><td>{e(B['free'])}</td></tr><tr><th>Official</th><td><a href="{e(A['pricing'])}" rel="noopener">pricing page</a></td><td><a href="{e(B['pricing'])}" rel="noopener">pricing page</a></td></tr></table>
<h2>Verdict</h2><p>{verdict}</p><p>See all <a href="/best-ai-{cid}-tools.html">best AI {e(c['name'].lower())} tools</a>.</p>{complinks([x for x in COMPARISONS if x[0]!=s])}"""
    page(path, title, d, body, [crumbs([("ToolPick","/"),(title0,path)])])
# best AI tool for [job] pages
for js, job, cid, ranked in JOBS:
    path = f"/best-ai-tool-for-{js}.html"; c = next(x for x in CATEGORIES if x["id"] == cid)
    title = f"Best AI Tool for {job[0].upper()+job[1:]} ({CHECKED[:4]}) — Top 3 with Prices"
    d = f"The top 3 AI tools for {job}: {', '.join(ranked)}. Prices checked {CHECKED} on official pricing pages."
    items = "".join(f"<li><h3><a href='{turl(n)}'>{e(n)}</a></h3><p>{e(find(n)['about'])}</p><p class='price'>💲 {e(find(n)['price'])}</p><p>🆓 {e(find(n)['free'])}</p></li>" for n in ranked)
    body = f"""<h1>Best AI tool for {e(job)}</h1><p class="tag">{e(d)}</p><ol>{items}</ol><div class="sponsor">Sponsored slot available — <a href="/sponsor.html">sponsor ToolPick</a></div>
<p>More options: <a href="/best-ai-{cid}-tools.html">all AI {e(c['name'].lower())} tools</a>.</p>{complinks(comps_for(ranked))}
<h2>Other jobs</h2><ul>{''.join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS if j[0]!=js)}</ul>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(n),"name":n} for i,n in enumerate(ranked)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Best AI tool for {job}",path)])])
# sponsor + newsletter
tiers = "".join(f"<div class='card'><h3>{e(a)}</h3><p>{e(b)}</p><p class='price'>{e(p)}</p></div>" for a,b,p in SPONSOR_TIERS)
page("/sponsor.html", "Sponsor ToolPick — reach people choosing AI tools", "Sponsorship options on ToolPick: category spotlight, sitewide banner and newsletter feature. Sponsored placements are always labelled.",
     f"<h1>Sponsor ToolPick</h1><p>Reach people at the moment they pick an AI tool. Sponsored placements are always labelled and never change our best-value picks or prices.</p><div class='grid'>{tiers}</div><h2>Contact</h2><p>Sponsorship contact: <b>coming soon</b> (contact details will be added here).</p>")
page("/newsletter.html", "ToolPick newsletter — AI tool price changes (coming soon)", "A weekly email with AI tool price changes and new free tiers. Coming soon.",
     "<h1>ToolPick newsletter</h1><p>Weekly: AI tool price changes, new free tiers and best-value picks. <b>Coming soon. Nothing is collected yet.</b></p><form onsubmit='return false'><input type='email' placeholder='you@example.com' disabled style='padding:10px;border-radius:8px'> <button disabled class='btn'>Coming soon</button></form>")
# llms.txt
ll = [f"# ToolPick", f"> Needs-based AI tool finder. {total_tools} tools, prices copied from official pricing pages on {CHECKED}. 'check site' means unverified.", "", "## Categories"]
ll += [f"- [{c['name']}]({BASE}/best-ai-{c['id']}-tools.html): best value {c['best']}; free options {', '.join(c['free'])}" for c in CATEGORIES]
ll += ["", "## Tools"] + [f"- [{n}]({BASE}{turl(n)}): {find(n)['price']} | free: {find(n)['free']}" for n in tool_pages]
ll += ["", "## Comparisons"] + [f"- [{t}]({BASE}/compare/{s}.html)" for s,t,*_ in COMPARISONS] + ["", "## Best tool for a job"] + [f"- [{j[1]}]({BASE}/best-ai-tool-for-{j[0]}.html)" for j in JOBS]
ll += ["", f"Data: {BASE}/tools.json"]
open("public/llms.txt","w").write("\n".join(ll)+"\n")
# OG image
try:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB",(1200,630),"#0f1117"); dr = ImageDraw.Draw(im)
    def F(sz):
        for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","DejaVuSans-Bold.ttf"]:
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
        return ImageFont.load_default()
    dr.rectangle([0,0,1200,12],fill="#3b82f6"); dr.text((80,180),"ToolPick",font=F(120),fill="#e7e9ee")
    dr.text((80,340),f"Find the right AI tool. {total_tools} tools, verified prices.",font=F(40),fill="#9aa3b2")
    dr.text((80,420),"Best-value pick + free alternative for every need",font=F(36),fill="#22c55e"); im.save("public/og.png")
except Exception as ex:
    import base64
    from og_data import OG_PNG
    open("public/og.png","wb").write(base64.b64decode(OG_PNG)); print("OG image from og_data.py (PIL unavailable)")
open("public/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open("public/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{CHECKED}</lastmod></url>" for u in URLS) + "</urlset>")
open("public/tools.json","w").write(json.dumps({"checked":CHECKED,"categories":CATEGORIES},indent=1))
print("pages:", len(URLS), "unique tools:", total_tools, {c["id"]:len(c["tools"]) for c in CATEGORIES})
