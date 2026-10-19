"""Builds public/ from tools.py.  Usage: BASE=https://your-site python3 build.py
Pages: index, /best-ai-<category>-tools.html, /tools/<slug>.html, /compare/<slug>.html, sitemap, robots, tools.json"""
import os, re, html, json, shutil
from tools import CATEGORIES, CHECKED, COMPARISONS, PRICE_TABLE, JOBS, SPONSOR_TIERS, FREE_ALT_FOR, REDIRECTS
BASE = os.environ.get("BASE", "https://toolpick-ai.vercel.app").rstrip("/")
e = html.escape
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
CSS = """:root{--bg:#f7f8fa;--sf:#fff;--sf2:#f1f3f6;--tx:#111827;--mu:#4b5563;--bd:#e3e6eb;--ac:#2563eb;--acs:#e8efff;--ok:#15803d;--okt:#fff;--fr:#fef3c7;--frt:#78350f;--warn:#b45309;--sh:0 1px 2px rgba(16,24,40,.05),0 4px 12px rgba(16,24,40,.06);--r:14px;--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:48px}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--sf:#161b22;--sf2:#1c232c;--tx:#e6edf3;--mu:#a3adb8;--bd:#2d3540;--ac:#7cb7ff;--acs:#15253d;--ok:#1f7a3a;--okt:#fff;--fr:#4a3a0c;--frt:#fde68a;--warn:#fbbf24;--sh:0 1px 2px rgba(0,0,0,.4),0 6px 16px rgba(0,0,0,.35)}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;font-size:16px;overflow-wrap:break-word}
a{color:var(--ac);text-underline-offset:2px}a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--ac);outline-offset:2px;border-radius:6px}
.skip{position:absolute;left:-999px;top:0;background:var(--ac);color:#fff;padding:var(--s3)}.skip:focus{left:var(--s3);top:var(--s3);z-index:9}
.wrap,main{max-width:1120px;margin:0 auto;padding:0 var(--s4)}main{padding-top:var(--s5);padding-bottom:var(--s7)}
header.site{background:var(--sf);border-bottom:1px solid var(--bd)}header.site .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s2) var(--s4);padding-top:var(--s2);padding-bottom:var(--s2)}
.brand{font-weight:800;font-size:1.15rem;color:var(--tx);text-decoration:none;display:inline-flex;align-items:center;gap:var(--s2);min-height:44px}.brand i{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:8px;background:var(--ac);color:var(--sf);font-style:normal;font-size:.9rem}
nav.top{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s1);margin-left:auto}nav.top>a,nav.top summary{display:inline-flex;align-items:center;min-height:44px;padding:0 var(--s3);border-radius:10px;color:var(--tx);text-decoration:none;font-weight:500;cursor:pointer}nav.top>a:hover,nav.top summary:hover{background:var(--sf2)}
nav.top details{position:relative}nav.top summary{list-style:none}nav.top summary::-webkit-details-marker{display:none}nav.top summary::after{content:"▾";margin-left:6px;font-size:.8em}
.menu{position:absolute;right:0;top:100%;z-index:20;background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s2);min-width:240px;display:grid}.menu a{display:flex;align-items:center;min-height:44px;padding:0 var(--s3);border-radius:8px;color:var(--tx);text-decoration:none}.menu a:hover{background:var(--sf2)}
h1{font-size:clamp(1.7rem,4.5vw,2.6rem);line-height:1.15;letter-spacing:-.02em;margin:0 0 var(--s3)}h2{font-size:1.35rem;line-height:1.3;margin:var(--s7) 0 var(--s4);letter-spacing:-.01em}h3{font-size:1.05rem;margin:var(--s5) 0 var(--s2)}p{margin:0 0 var(--s3)}
.tag{color:var(--mu);font-size:1.05rem;max-width:70ch}.small{font-size:.875rem;color:var(--mu)}.price{font-weight:600}.check{color:var(--warn)}
ul,ol{padding-left:1.3em}li{margin:var(--s2) 0}main li>a{display:inline-block;padding:6px 0}
.grid,.res{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr));gap:var(--s4);margin:var(--s4) 0}
.card{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:var(--s5);box-shadow:var(--sh);display:flex;flex-direction:column;gap:var(--s1);min-width:0}.card p{margin:0}.card h3{margin:0;font-size:1.1rem}.card h3 a{color:var(--tx);text-decoration:none}.card h3 a:hover{color:var(--ac);text-decoration:underline}
.th{display:flex;align-items:center;gap:var(--s3);margin-bottom:var(--s2)}.logo{width:40px;height:40px;flex:none;border-radius:10px;background:var(--sf2);border:1px solid var(--bd);display:grid;place-items:center;overflow:hidden;font-weight:700;color:var(--mu)}.logo img{width:28px;height:28px}
.best{border:2px solid var(--ok)}.badges{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:var(--s1)}.badge{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.03em;padding:3px 9px;border-radius:999px;margin-right:4px}.b-best{background:var(--ok);color:var(--okt)}.b-free{background:var(--fr);color:var(--frt)}.b-rank{background:var(--acs);color:var(--tx)}
.meta{margin-top:auto;padding-top:var(--s2);border-top:1px solid var(--bd)}
.pick,.freealt,.sponsor{border-radius:var(--r);padding:var(--s4) var(--s5);margin:var(--s4) 0;background:var(--sf);border:1px solid var(--bd);box-shadow:var(--sh)}.pick{border-left:4px solid var(--ok)}.freealt{border-left:4px solid #d97706}.sponsor{border-style:dashed;box-shadow:none;color:var(--mu)}
.tw{overflow-x:auto;border:1px solid var(--bd);border-radius:var(--r);background:var(--sf);box-shadow:var(--sh);margin:var(--s4) 0}table{border-collapse:collapse;width:100%;font-size:.95rem}td,th{border-bottom:1px solid var(--bd);padding:var(--s3) var(--s4);text-align:left;vertical-align:top}th{background:var(--sf2);font-weight:600}tr:last-child td{border-bottom:0}main>table{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);display:block;overflow-x:auto}
.hero{text-align:center;padding:var(--s6) 0 var(--s4)}.hero .tag{margin:0 auto var(--s5)}
.finder{max-width:820px;margin:0 auto}.sbar{display:flex;gap:var(--s2);background:var(--sf);border:1px solid var(--bd);border-radius:999px;padding:6px 6px 6px var(--s5);box-shadow:var(--sh)}.sbar:focus-within{outline:3px solid var(--ac);outline-offset:2px}.sbar input{flex:1;min-width:0;border:0;background:transparent;color:var(--tx);font-size:1.1rem;min-height:48px;outline:none}.sbar button{min-height:48px;padding:0 var(--s5);border:0;border-radius:999px;background:var(--ac);color:var(--sf);font-weight:700;font-size:1rem;cursor:pointer}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:var(--s2);margin:var(--s4) 0}.chip,.needs button,.seg label{display:inline-flex;align-items:center;min-height:44px;padding:0 var(--s4);border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-size:.95rem;cursor:pointer;font-family:inherit}.chip:hover,.needs button:hover{border-color:var(--ac)}
.filters{display:flex;flex-wrap:wrap;gap:var(--s2);justify-content:center;align-items:center;margin-bottom:var(--s4)}.filters select{min-height:44px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s4);font-size:.95rem;font-family:inherit;max-width:100%}
.seg{display:inline-flex;gap:4px;padding:4px;background:var(--sf2);border-radius:999px;border:0;margin:0}.seg legend{position:absolute;left:-999px}.seg input{position:absolute;opacity:0}.seg label{border:0;background:transparent;min-height:44px}.seg input:checked+label{background:var(--sf);box-shadow:var(--sh);font-weight:600}.seg input:focus-visible+label{outline:3px solid var(--ac)}
#out{text-align:left}#out>h2{font-size:1.1rem;margin:var(--s5) 0 var(--s2)}
.needs{display:flex;flex-wrap:wrap;gap:var(--s2);margin:var(--s4) 0}.needs button.on{background:var(--ac);border-color:var(--ac);color:var(--sf)}.tabs section{display:none}.tabs section.on{display:block}
.finderbox,.free-filter{margin:var(--s4) 0}.free-filter select{min-height:44px;border-radius:10px;padding:0 var(--s3);background:var(--sf);color:var(--tx);border:1px solid var(--bd)}
.btn{display:inline-flex;align-items:center;min-height:44px;background:var(--ac);color:var(--sf);padding:0 var(--s5);border-radius:999px;text-decoration:none;font-weight:600}
footer.site{border-top:1px solid var(--bd);background:var(--sf);margin-top:var(--s7)}footer.site .wrap{padding-top:var(--s6);padding-bottom:var(--s6)}footer.site a{display:inline-flex;align-items:center;min-height:44px;margin-right:var(--s4)}
input,select,button{font:inherit}th{white-space:nowrap}td,th{vertical-align:middle}#out,#out>h2{scroll-margin-top:96px}.card h3 a,td a,th a,.pick a,.freealt a,.sponsor a{display:inline-flex;align-items:center;min-height:44px}
@media(max-width:640px){main{padding-top:var(--s4)}.hero{padding-top:var(--s4)}.hstick{position:sticky;top:0;z-index:15;background:var(--bg);padding:var(--s2) 0}.sbar{padding-left:var(--s4)}.sbar button{padding:0 var(--s4)}nav.top{margin-left:0;width:100%}.menu{left:0;right:auto}.card{padding:var(--s4)}}
@media(prefers-reduced-motion:no-preference){.card{transition:box-shadow .15s,transform .15s}.card:hover{transform:translateY(-1px)}}
.builder{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s5);margin:var(--s4) 0}#calc-out .tw table{min-width:640px}.cform{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--s4)}.cform label{font-weight:600;display:block}.cform select,.cform input[type=number]{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3)}.cform fieldset{border:0;padding:0;margin:0}.cform legend{font-weight:600;margin-bottom:var(--s2)}@media(max-width:760px){.cform{grid-template-columns:1fr}}.bform{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)}.bform label{font-weight:600;display:block}.bform select{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);max-width:100%}.bactions{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4);align-items:center}.bbtn{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--s5);border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-weight:600;cursor:pointer}.bbtn.primary{background:var(--ac);color:var(--sf);border-color:var(--ac)}.bstatus{min-height:1.5em}.bnote{background:var(--sf2);border-radius:10px;padding:var(--s3) var(--s4);margin:var(--s4) 0}@media(max-width:760px){.bform{grid-template-columns:1fr}.builder{padding:var(--s4)}}.dform{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)}.dform label{font-weight:600;display:block}.dform select{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);max-width:100%}@media(max-width:760px){.dform{grid-template-columns:1fr}}.tray{position:sticky;bottom:12px;z-index:10;background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s3) var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin:var(--s4) 0}.tray .bbtn{min-height:44px}.addbtn{margin-top:auto}.wizprog{height:10px;background:var(--sf2);border-radius:999px;overflow:hidden;margin:var(--s4) 0}.wizprog i{display:block;height:100%;background:var(--ac)}.opts{display:grid;gap:var(--s2);margin:var(--s4) 0}.opts label{display:flex;gap:var(--s3);align-items:flex-start;background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:var(--s4);cursor:pointer;min-height:44px}.opts label:hover{border-color:var(--ac)}.opts input{margin-top:4px;flex:none}.opts input:focus-visible+span{outline:3px solid var(--ac);outline-offset:2px}.wstep fieldset{border:0;padding:0;margin:0}.wstep legend{font-size:1.25rem;font-weight:700;line-height:1.3}.wnav{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4);align-items:center}
"""
FOOT = f"""<footer class="site small"><div class="wrap"><p><a href="/sponsor.html">Sponsor ToolPick</a> · <a href="/newsletter.html">Newsletter</a> · <a href="/llms.txt">llms.txt</a></p>Some links may become affiliate links in future; that never changes our picks. Prices copied from each tool's official pricing page on {CHECKED} (USD unless shown; yearly-billing prices in parentheses). "check site" = we could not verify the price, so we don't guess. Prices change — always confirm on the official page.</div></footer>"""
def page(path, title, desc, body, ld=None):
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    full = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>{lds}<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script><script defer src="/_vercel/insights/script.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site"><div class="wrap"><a class="brand" href="/"><i aria-hidden="true">T</i>ToolPick</a><nav class="top" aria-label="Main"><details><summary>Categories</summary><div class="menu">{''.join(f'<a href="/best-ai-{c["id"]}-tools.html">{e(c["name"])}</a>' for c in CATEGORIES)}</div></details><a href="/tools.html">Browse all tools</a><a href="/free.html">Free tools</a><a href="/price-changes.html">Price changes</a><a href="/guides.html">Guides</a><a href="/compare-builder.html">Compare builder</a></nav></div></header>
<main id="main">{body}</main>{FOOT}</body></html>"""
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
DISCLOSURE = '<p class="small disc">Disclosure: this is an affiliate link. ToolPick may earn a commission at no extra cost to you; it never changes our picks or prices.</p>'
def faq(qas):
    html_ = "<h2>FAQ</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in qas)
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in qas]}
    return html_, ld
def tool_qas(t):
    ck = t.get('checked', CHECKED)
    return [(f"How much does {t['name']} cost?", f"Per its official pricing page (checked {ck}): {t['price']}."),
            (f"Does {t['name']} have a free plan?", f"{t['free']} (checked {ck}).")]
import re as _re
NOT_FREE = _re.compile(r"trial|one-time|free (api )?credit|in free credits|start (for )?free|^no free|^check site", _re.I)
def realfree(t):
    f = t["free"]
    return bool(_re.search(r"free|\$0", f, _re.I)) and not NOT_FREE.search(f)
for _c in CATEGORIES:
    _c["free"] = [n for n in _c["free"] if any(x["name"] == n and realfree(x) for x in _c["tools"])]
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
from urllib.parse import urlparse
def dom(u): return urlparse(u).netloc.replace("www.","")
def logo(t):
    return f'<span class="logo" aria-hidden="false"><img src="https://www.google.com/s2/favicons?domain={dom(t["url"])}&amp;sz=64" alt="{e(t["name"])} logo" width="28" height="28" loading="lazy" decoding="async" onerror="this.replaceWith(document.createTextNode(\'{e(t["name"][0])}\'))"></span>'
def turl(n): return f"/tools/{slug(n)}.html"
def card(t, c):
    best = t["name"] == c["best"]; free = t["name"] in c["free"]
    badges = ("<span class='badge b-best'>BEST VALUE</span>" if best else "") + ("<span class='badge b-free'>FREE OPTION</span>" if free else "")
    pc = "price check" if t["price"] == "check site" else "price"
    return f"""<article class="card{' best' if best else ''}"><div class="th">{logo(t)}<div><div class="badges">{badges}</div><h3><a href="{turl(t['name'])}">{e(t['name'])}</a></h3></div></div><p>{e(t['about'])}</p>
<p class="{pc}">{e(t['price'])}</p><p class="small">{e(t["free"])}</p>
<p class="small meta"><a href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Official site</a> · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Pricing page</a> · checked {t.get('checked', CHECKED)}</p>{DISCLOSURE if t.get('affiliate') else ''}</article>"""
def picks(c):
    b = next(t for t in c["tools"] if t["name"] == c["best"])
    return f"""<div class="pick"><span class="badge b-best">BEST VALUE</span><b><a href="{turl(b['name'])}">{e(b['name'])}</a></b> — {e(b.get('why',''))}</div>
<div class="freealt"><span class="badge b-free">FREE ALTERNATIVES</span>{', '.join(f'<a href="{turl(n)}">{e(n)}</a>' for n in c['free'])}</div>"""
def comps_for(names): return [x for x in COMPARISONS if set(x[2] if isinstance(x[2], list) else [x[2], x[3]]) & set(names)]
def complinks(lst): return ("<h2>Comparisons</h2><ul>" + "".join(f'<li><a href="/compare/{s}.html">{e(ti)}</a></li>' for s,ti,*_ in lst) + "</ul>") if lst else ""
total_tools = len(tool_pages)
# v13 SEO pages (preview): free alternatives that do not already exist + video under $20.
# 'free alternative to Cursor' already exists at /free-alternative-to-cursor.html, so it is not rebuilt.
SEO_FREE_ALT = ["Recraft", "Rytr"]
SEO_VIDEO_PATH = "/best-ai-video-tools-under-20.html"
def _entry_num(t):
    vals = [v for v in (t.get("monthly"), t.get("annual")) if isinstance(v, (int, float))]
    return min(vals) if vals else None
# index
FDATA = json.dumps([dict(n=t["name"],c=c["id"],cn=c["name"],u=turl(t["name"]),p=t["price"],f=t["free"],k=t.get("checked",CHECKED),d=t["about"],dm=dom(t["url"]),a=t["about"]+" "+c["need"],
    m=min([v for v in (t["monthly"],t["annual"]) if isinstance(v,(int,float))],default=None),b=t["name"]==c["best"],fr=realfree(t)) for c in CATEGORIES for t in c["tools"]])
FOPTS = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)
FINDER = ('''<div class="finder" role="search"><form class="hstick" id="ff" onsubmit="event.preventDefault();run();document.getElementById('out').scrollIntoView({behavior:'smooth'})"><label for="q" class="skip">Describe what you need</label><div class="sbar"><input type="search" id="q" autocomplete="off" placeholder="What do you need help with?"><button type="submit">Find</button></div></form>
<div class="chips" aria-label="Example searches"><button type="button" class="chip" data-q="turn my podcast into short clips">turn my podcast into short clips</button><button type="button" class="chip" data-q="cheap voiceover">cheap voiceover</button><button type="button" class="chip" data-q="pitch deck for investors">pitch deck for investors</button><button type="button" class="chip" data-q="AI coding assistant">AI coding assistant</button><button type="button" class="chip" data-q="meeting notes">meeting notes</button><button type="button" class="chip" data-q="logo with text">logo with text</button><button type="button" class="chip" data-q="research papers">research papers</button></div>
<div class="filters"><fieldset class="seg"><legend>Price</legend><input type="radio" name="pf" id="pf-all" value="all" checked><label for="pf-all">All</label><input type="radio" name="pf" id="pf-free" value="free"><label for="pf-free">Free plan</label><input type="radio" name="pf" id="pf-paid" value="paid"><label for="pf-paid">Paid</label></fieldset>
<label class="skip" for="cat">Category</label><select id="cat"><option value="">All categories</option>''' + FOPTS + '''</select>
<label class="skip" for="budget">Budget</label><select id="budget"><option value="any">Any budget</option><option value="0">Free only</option><option value="15">Up to $15/mo</option><option value="30">Up to $30/mo</option><option value="100">Up to $100/mo</option></select>
<label class="skip" for="skill">Experience</label><select id="skill"><option value="beginner">Beginner</option><option value="pro">Pro / power user</option></select></div><div id="out" aria-live="polite"></div></div>
<script>const D=''' + FDATA.replace("</", "<\\/") + r''';
const SW=new Set('the and for with into turn make want need some best good cheap free tool tools that this from your using use help'.split(' '));const hasFree=t=>t.fr;
function run(){const q=document.getElementById('q').value.toLowerCase().split(/\W+/).filter(w=>w.length>2&&!SW.has(w)),c=document.getElementById('cat').value,bu=document.getElementById('budget').value,sk=document.getElementById('skill').value;
let L=D.filter(t=>!c||t.c==c).map(t=>{let s=0;const h=(t.n+' '+t.a+' '+t.cn+' '+t.c).toLowerCase();q.forEach(w=>{if(h.includes(w))s+=3;else if(h.includes(w.slice(0,5)))s+=1});const ms=s;if(t.b)s+=2;if(hasFree(t)&&sk=='beginner')s+=1.5;if(t.m!=null&&sk=='pro')s+=0.5;return Object.assign({s,ms},t)});
let nm=false;if(q.length){const mx=Math.max(0,...L.map(t=>t.ms));if(mx>0)L=L.filter(t=>t.ms>0);else nm=true}
const pf=(document.querySelector('input[name=pf]:checked')||{}).value||'all';if(pf=='free')L=L.filter(hasFree);if(pf=='paid')L=L.filter(t=>!hasFree(t));if(bu=='0')L=L.filter(hasFree);else if(bu!='any')L=L.filter(t=>hasFree(t)||(t.m!=null&&t.m<=+bu));
L.sort((x,y)=>y.s-x.s);const seen=new Set();L=L.filter(t=>!seen.has(t.n)&&seen.add(t.n));
const top=L.slice(0,3),bv=L.filter(t=>t.b&&(!L[0]||t.c==L[0].c))[0]||L.filter(t=>t.m!=null&&t.c==L[0].c).sort((x,y)=>x.m-y.m)[0]||L.filter(t=>t.m!=null).sort((x,y)=>x.m-y.m)[0],fo=L.filter(hasFree)[0];
const X=v=>String(v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));const card=(t,lab)=>t?`<article class="card${lab=='BEST VALUE'?' best':''}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${t.dm}&amp;sz=64" alt="${X(t.n)} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${X(t.n[0])}'))"></span><div><div class="badges"><span class="badge ${lab=='FREE OPTION'?'b-free':lab=='BEST VALUE'?'b-best':'b-rank'}">${lab}</span></div><h3><a href="${t.u}">${X(t.n)}</a></h3></div></div><p>${X(t.d)}</p><p class="price">${X(t.p)}</p><p class="small">${X(t.f)}</p><p class="small meta">${X(t.cn)} · checked ${t.k}</p></article>`:'';
document.getElementById('out').innerHTML=L.length?`${nm?'<p class="small">No close match for those words, so here are our overall picks. Try other words or pick a use case.</p>':''}<h2>${nm?'Popular picks':'Top matches'}</h2><div class="res">${top.map((t,i)=>card(t,'#'+(i+1))).join('')}</div><h2>Best value &amp; free option</h2><div class="res">${card(bv,'BEST VALUE')}${card(fo,'FREE OPTION')}</div>`:'<p>No match, try a broader budget or use case.</p>'}
['q','cat','budget','skill','pf-all','pf-free','pf-paid'].forEach(i=>{const el=document.getElementById(i);el.addEventListener('input',run);el.addEventListener('change',run)});document.querySelectorAll('.chip').forEach(b=>b.addEventListener('click',()=>{const q=document.getElementById('q');q.value=b.dataset.q;run();q.focus()}));run();</script>''')
desc = f"Tell us what you need and compare {total_tools} AI tools across {len(CATEGORIES)} categories — prices checked on official pages, a best-value pick and a free option."
body = f"""<section class="hero"><h1>Find the right AI tool for your need</h1><p class="tag">{e(desc)}</p></section>{FINDER}<div class="pick"><span class="badge b-best">NEW</span> <b>Compare any 2–3 tools side by side</b> — pick tools from different categories, see verified prices and free plans, then share the link. <a href="/compare-builder.html">Open the compare builder →</a> · <a href="/compare-builder.html?tools=elevenlabs,descript,heygen">Try ElevenLabs vs Descript vs HeyGen</a></div><div class="pick"><span class="badge b-best">NEW</span> <b>Help me choose in 5 quick steps</b> — answer questions about your task, budget, billing, seats and must-haves and get a ranked shortlist with verified prices. <a href="/help-me-choose.html">Start the wizard →</a> · <a href="/help-me-choose.html?category=audio&amp;budget=10&amp;billing=monthly&amp;seats=1&amp;free=any&amp;annual=any">Try Audio under $10</a></div><div class="pick"><span class="badge b-best">NEW</span> <b>What will it really cost?</b> — pick a tool or category, seats and monthly or annual billing to see the true monthly and yearly cost from verified entry prices. <a href="/cost-calculator.html">Open the cost calculator →</a> · <a href="/cost-calculator.html?tool=elevenlabs&seats=1&billing=monthly">Try ElevenLabs</a> · <a href="/cost-calculator.html?category=audio&seats=5&billing=annual">Audio tools for 5 seats, annual</a></div><div class="pick"><span class="badge b-best">NEW</span> <b>Browse all AI tools in one directory</b> — filter all 82 tools by category, free plan, verified starting price, billing availability and per-seat pricing, sort them, and add up to 3 to compare. <a href="/tools.html">Browse the full directory →</a> · <a href="/tools.html?category=audio&amp;free=yes&amp;sort=price">Try Audio tools with a free plan</a></div><h2>Browse by category</h2>
<div class="needs">{''.join(f'<button data-id="{c["id"]}" class="{"on" if i==0 else ""}">{e(c["name"])}</button>' for i,c in enumerate(CATEGORIES))}</div><div class="tabs">
{''.join(f'<section id="{c["id"]}" class="{"on" if i==0 else ""}"><h2>{e(c["need"])}</h2>{picks(c)}<div class="grid">{"".join(card(t,c) for t in c["tools"])}</div><p><a href="/best-ai-{c["id"]}-tools.html">Full guide: best AI {e(c["name"].lower())} tools →</a></p></section>' for i,c in enumerate(CATEGORIES))}</div>
{complinks(COMPARISONS)}<p><a href="/guides.html">All guides →</a> · <a href="/price-changes.html">Price changes log</a></p><h2>Best AI tool for…</h2><ul>{"".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS)}</ul>
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
{complinks(comps_for([t['name'] for t in c['tools']]))}<p><a href="/compare-builder.html">Build your own comparison →</a> Pick any 2–3 tools and share the result.</p><p><a href="/tools.html?category={c['id']}">Browse {e(n.lower())} tools in the full directory →</a> Filter by free plan, verified price, billing and seat pricing.</p><p><a href="/help-me-choose.html?category={c['id']}">Help me choose {e(n.lower())} tools →</a> Answer 5 quick questions and get a ranked shortlist for this category.</p>{'<p><a href="/best-ai-video-tools-under-20.html">Best AI video tools under $20 →</a> Every video tool with a verified entry price under $20/mo, ranked cheapest first.</p>' if c['id']=='video' else ''}{'<p><a href="/free-alternative-to-recraft.html">Free alternatives to Recraft →</a> Images tools with a verified real free plan.</p>' if c['id']=='images' else ''}{'<p><a href="/free-alternative-to-rytr.html">Free alternatives to Rytr →</a> Writing tools with a verified real free plan.</p>' if c['id']=='writing' else ''}"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(c["tools"])]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Best AI {n} tools",path)])])
# tool pages
for name, cats in tool_pages.items():
    c = cats[0]; t = next(x for x in c["tools"] if x["name"] == name); path = turl(name)
    pros, cons = proscons(t, c)
    title = f"{name} Pricing & Free Plan ({CHECKED[:7]}) — Pros, Cons, Alternatives"
    d = f"{name} pricing checked {t.get('checked', CHECKED)}: {t['price']}. Free tier: {t['free']}. Pros, cons and alternatives."[:300]
    alts = [x["name"] for cc in cats for x in cc["tools"] if x["name"] != name]
    body = f"""<h1>{e(name)} pricing &amp; review</h1><p class="tag">{e(t['about'])}</p>
<table><tr><th>Price</th><td class="{'check' if t['price']=='check site' else ''}">{e(t['price'])}</td></tr><tr><th>Free tier</th><td>{e(t['free'])}</td></tr>
<tr><th>Categories</th><td>{', '.join(f'<a href="/best-ai-{cc["id"]}-tools.html">{e(cc["name"])}</a>' for cc in cats)}</td></tr><tr><th>Checked</th><td>{t.get('checked', CHECKED)} on the <a href="{e(t['pricing'])}" rel="noopener">official pricing page</a></td></tr></table>
<h2>Pros</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in pros)}</ul><h2>Cons</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in cons) or '<li>Paid features require a subscription — compare plans on the official page</li>'}</ul>
<p><a class="btn" href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Visit {e(name)} official site</a></p>{DISCLOSURE if t.get('affiliate') else ''}
<p><a href="/cost-calculator.html?tool={slug(name)}&amp;seats=1&amp;billing=monthly">What will {e(name)} really cost? →</a> See its true monthly and yearly cost by seats and billing period in the cost calculator.</p>{'<p><a href="/free-alternative-to-recraft.html">Free alternatives to Recraft →</a> Compare Images tools with a verified real free plan.</p>' if name=='Recraft' else ''}{'<p><a href="/free-alternative-to-rytr.html">Free alternatives to Rytr →</a> Compare Writing tools with a verified real free plan.</p>' if name=='Rytr' else ''}{'<p><a href="/best-ai-video-tools-under-20.html">Best AI video tools under $20 →</a> This tool is in our verified under-$20 video list.</p>' if (cats[0]['id']=='video' and _entry_num(t) is not None and _entry_num(t) < 20) else ''}
<h2>Alternatives</h2><ul>{''.join(f'<li><a href="{turl(a)}">{e(a)}</a></li>' for a in dict.fromkeys(alts))}</ul>{complinks(comps_for([name]))}"""
    sw = {"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"applicationCategory":"BusinessApplication","operatingSystem":"Web","url":t["url"],"description":t["about"]}
    fh, fl = faq(tool_qas(t)); body += fh
    page(path, title, d, body, [sw, fl, crumbs([("ToolPick","/"),(f"Best AI {c['name']} tools",f"/best-ai-{c['id']}-tools.html"),(name,path)])])
# comparison pages
def find(n): return next(x for c in CATEGORIES for x in c["tools"] if x["name"] == n)
def cnames(x): return x[2] if isinstance(x[2], list) else [x[2], x[3]]
for x in COMPARISONS:
    s_, title0, cid = x[0], x[1], x[4]; N = cnames(x); TT = [find(n) for n in N]
    path = f"/compare/{s_}.html"; c = next(y for y in CATEGORIES if y["id"] == cid)
    title = f"{title0} ({CHECKED[:4]}): Price, Free Plan & Which to Pick"
    d = f"{' vs '.join(N)} compared with prices checked {CHECKED} on official pricing pages: plans, free tiers and which is better value."
    verdict = f"ToolPick's best-value pick for {c['name'].lower()} is <a href='{turl(c['best'])}'>{e(c['best'])}</a>."
    if c["best"] not in N: verdict += " Among these, compare the entry prices above and pick the one whose free tier lets you test your exact use case."
    if any(t["price"] == "check site" for t in TT): verdict += " Some prices here could not be verified; check the official pricing pages."
    row = lambda lab, f: f"<tr><th>{lab}</th>" + "".join(f"<td>{f(t)}</td>" for t in TT) + "</tr>"
    body = (f'<h1>{e(title0)}</h1><p class="tag">{e(d)}</p><div class="tw"><table><tr><th></th>' + "".join(f'<th><a href="{turl(n)}">{e(n)}</a></th>' for n in N) + "</tr>"
      + row("What it is", lambda t: e(t["about"])) + row("Price", lambda t: e(t["price"])) + row("Free tier", lambda t: e(t["free"]))
      + row("Official", lambda t: f'<a href="{e(t["pricing"])}" rel="noopener">pricing page</a>') + "</table></div>"
      + f'<h2>Verdict</h2><p>{verdict}</p><p>See all <a href="/best-ai-{cid}-tools.html">best AI {e(c["name"].lower())} tools</a>.</p><p><a href="/compare-builder.html?tools={",".join(slug(n) for n in N)}">Open these tools in the compare builder →</a> Add a third tool or swap one and share the link.</p><p><a href="/cost-calculator.html?category={cid}&amp;seats=1&amp;billing=monthly">What will these really cost? →</a> Compare true monthly and yearly costs for this category in the cost calculator.</p><p><a href="/tools.html?category={cid}">Browse all {e(c["name"].lower())} tools in the directory →</a></p>{complinks([y for y in COMPARISONS if y[0]!=s_])}')
    il = {"@context":"https://schema.org","@type":"ItemList","name":title0,"itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(n),"name":n} for k,n in enumerate(N)]}
    qas = [q for t in TT for q in tool_qas(t)] + [(f"What is ToolPick's best-value pick for {c['name'].lower()}?", f"{c['best']}: {find(c['best']).get('why','')}".strip())]
    fh, fl = faq(qas)
    page(path, title, d, body + fh, [il, fl, crumbs([("ToolPick","/"),(title0,path)])])

# --- Custom comparison builder (v9 preview) ---
# Unique tools by slug, reusing only existing verified fields.
_bmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _bmap:
            _bmap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"],
                             m=min([v for v in (_t["monthly"], _t["annual"]) if isinstance(v, (int, float))], default=None),
                             b=False, fr=realfree(_t), cats=[])
        if _c["name"] not in _bmap[_k]["cats"]: _bmap[_k]["cats"].append(_c["name"])
        if _t["name"] == _c["best"]: _bmap[_k]["b"] = True
BDATA = json.dumps(sorted(_bmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
BOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])} — {e(", ".join(v["cats"]))}</option>' for v in sorted(_bmap.values(), key=lambda x: x["n"].lower()))
builder_body = f"""<h1>Compare any AI tools side by side</h1><p class="tag">Pick 2 or 3 tools from ToolPick's verified list and compare what they do, what they cost, and whether they have a free plan. Prices are copied from official pricing pages — checked dates are shown on every card. Nothing here is invented or re-priced.</p>
<div class="builder"><form id="bform"><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-bottom:12px">Choose 2–3 tools to compare</legend><div class="bform">
<div><label for="tool1">Tool 1 (required)</label><select id="tool1" name="tool1"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool2">Tool 2 (required)</label><select id="tool2" name="tool2"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool3">Tool 3 (optional)</label><select id="tool3" name="tool3"><option value="">Select a tool…</option>{BOPTS}</select></div>
</div></fieldset><div class="bactions"><button type="submit" class="bbtn primary">Compare tools</button><button type="button" class="bbtn" id="copyBtn">Copy share link</button><button type="button" class="bbtn" id="clearBtn">Clear</button><span class="small bstatus" id="bstatus" role="status"></span></div></form></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How the Best Value badge is chosen</h2><p class="small" style="margin:0">First, if one of your picks is already ToolPick's Best Value pick for its category (the same pick shown on our category pages), it gets the badge. Otherwise, the badge goes to the lowest verified entry price among your picks that have a verified free plan; if none has a free plan, it goes to the lowest verified entry price overall. Tools priced “check site” are excluded from the price ranking because we could not verify their price. Entry price means the lowest monthly or yearly-billing figure already listed in our verified price table.</p><p class="small" style="margin:12px 0 0">Want true monthly and yearly totals by seats and billing period? <a href="/cost-calculator.html">Open the “What will it really cost?” calculator →</a></p><p class="small" style="margin:12px 0 0">Or <a href="/tools.html">browse the full directory of all tools →</a> and add tools to compare from there.</p></div>
<div id="builder-out" aria-live="polite" aria-atomic="false"><p class="small">Pick at least 2 different tools above to see your comparison. You can also try <a href="/compare-builder.html?tools=elevenlabs,descript,heygen">ElevenLabs vs Descript vs HeyGen</a>.</p></div>
<script>const BD={BDATA};
const bySlug={{}};BD.forEach(t=>bySlug[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
const sels=()=>['tool1','tool2','tool3'].map(id=>document.getElementById(id));
function selected(){{const seen=new Set(),out=[];sels().forEach(s=>{{if(s.value&&!seen.has(s.value)&&bySlug[s.value]){{seen.add(s.value);out.push(bySlug[s.value])}}}});return out}}
function bestValue(list){{if(list.length<2)return null;const catBest=list.filter(t=>t.b);const pool=catBest.length?catBest:list;const freePriced=pool.filter(t=>t.fr&&t.m!=null).sort((a,b)=>a.m-b.m);if(freePriced.length)return freePriced[0];const priced=pool.filter(t=>t.m!=null).sort((a,b)=>a.m-b.m);if(priced.length)return priced[0];if(catBest.length)return catBest[0];return null}}
function entry(t){{return t.m==null?'Entry price not verified (“check site”)':'Lowest verified entry: $'+t.m+'/mo (monthly or yearly billing, from our price table)'}}
function render(push=true){{const list=selected();const out=document.getElementById('builder-out');const st=document.getElementById('bstatus');
if(list.length<2){{out.innerHTML='<div class="pick"><b>Pick at least 2 different tools to compare.</b><p class="small" style="margin-bottom:0">You have selected '+list.length+' tool'+(list.length==1?'':'s')+'. Choose '+(2-list.length)+' more above — comparisons work with 2 or 3 tools.</p></div>';if(push)history.replaceState(null,'',list.length?('?tools='+list.map(t=>t.s).join(',')):'/compare-builder.html');return}}
const bv=bestValue(list);
const cards=list.map(t=>`<article class="card${{bv&&t.s==bv.s?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{bv&&t.s==bv.s?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p><p class="small">${{X(t.f)}}</p><p class="small">${{entry(t)}}</p><p class="small meta">${{X(t.cats.join(', '))}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p></article>`).join('');
const row=(lab,fn)=>'<tr><th scope="row">'+lab+'</th>'+list.map(t=>`<td>${{fn(t)}}</td>`).join('')+'</tr>';
out.innerHTML=`<h2>Your comparison (${{list.length}} tools)</h2>${{bv?`<div class="pick"><span class="badge b-best">BEST VALUE</span> <b><a href="${{bv.u}}">${{X(bv.n)}}</a></b> — see the rule above. ${{entry(bv)}}.</div>`:''}}<div class="grid">${{cards}}</div><div class="tw"><table><caption class="small" style="text-align:left;padding:12px 16px">Side-by-side details. Prices checked on official pages; confirm before buying.</caption><tr><th scope="col">Tool</th>${{list.map(t=>`<th scope="col"><a href="${{t.u}}">${{X(t.n)}}</a>${{bv&&t.s==bv.s?' ★':''}}</th>`).join('')}}</tr>${{row('What it is',t=>X(t.d))}}${{row('Starting price (as listed)',t=>X(t.p))}}${{row('Lowest verified entry',t=>entry(t))}}${{row('Free plan / free option',t=>X(t.f))}}${{row('Categories',t=>X(t.cats.join(', ')))}}${{row('Price checked',t=>t.k+' · <a href="'+X(t.pr)+'" rel="noopener" target="_blank">pricing page</a>')}}</table></div><p class="small">Share this comparison: <a href="?tools=${{list.map(t=>t.s).join(',')}}">${{location.origin}}/compare-builder.html?tools=${{list.map(t=>t.s).join(',')}}</a></p>`;
if(push)history.replaceState(null,'','?tools='+list.map(t=>t.s).join(','));
st.textContent=list.length+' tools compared. Share link updated in the address bar.';}}
document.getElementById('bform').addEventListener('submit',ev=>{{ev.preventDefault();render();document.getElementById('builder-out').scrollIntoView({{behavior:'smooth',block:'start'}})}});
sels().forEach(s=>s.addEventListener('change',()=>render()));
document.getElementById('clearBtn').addEventListener('click',()=>{{sels().forEach(s=>s.value='');render();document.getElementById('bstatus').textContent='Cleared. Pick at least 2 tools.';sels()[0].focus()}});
document.getElementById('copyBtn').addEventListener('click',async()=>{{const list=selected();const st=document.getElementById('bstatus');if(list.length<2){{st.textContent='Pick at least 2 tools before copying a share link.';return}}const url=location.origin+'/compare-builder.html?tools='+list.map(t=>t.s).join(',');try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
(function init(){{const q=new URLSearchParams(location.search).get('tools');if(q){{const wanted=q.split(',').map(x=>x.trim()).filter(x=>bySlug[x]).slice(0,3);wanted.forEach((v,i)=>{{if(sels()[i])sels()[i].value=v}})}}render(false);if(q)render(true);}})();
</script>"""
page("/compare-builder.html", "Compare AI Tools Side by Side — Build Your Own Comparison | ToolPick", "Pick any 2–3 AI tools and compare verified prices, free plans and categories side by side. Shareable link, Best Value badge explained, prices checked on official pages.", builder_body,
     [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick compare builder","url":BASE+"/compare-builder.html","description":"Build a side-by-side comparison of any 2-3 AI tools with verified prices."}, crumbs([("ToolPick","/"),("Compare builder","/compare-builder.html")])])


# --- Cost calculator (v10 preview) ---
# Only existing verified fields: PRICE_TABLE monthly/annual entry rates, price/free text, checked, pricing URL.
# Per-seat math ONLY when the entry plan segment itself says /seat, /user, /member or per person (or a trailing "per seat" note, e.g. Gamma).
import re as _cre
def _perseat(t):
    _first = t["price"].split(";")[0]
    if _cre.search(r"/seat|per seat|/user|per user|/member|per member|per person", _first, _cre.I): return True
    _parts = t["price"].split(";")
    if len(_parts) > 1 and _cre.search(r"^\s*per seat\b", _parts[-1], _cre.I): return True
    return False
_cmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _cmap:
            _cmap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"],
                             ps=_perseat(_t), fr=realfree(_t), cats=[], bestFor=[])
        if _c["id"] not in [x["id"] for x in _cmap[_k]["cats"]]: _cmap[_k]["cats"].append(dict(id=_c["id"], name=_c["name"]))
        if _t["name"] == _c["best"] and _c["id"] not in _cmap[_k]["bestFor"]: _cmap[_k]["bestFor"].append(_c["id"])
CDATA = json.dumps(sorted(_cmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
CATDATA = json.dumps([dict(id=c["id"], name=c["name"], best=slug(c["best"]), bestName=c["best"], tools=[slug(t["name"]) for t in c["tools"]]) for c in CATEGORIES]).replace("</", "<\\/")
CTOOLOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])} — {e(", ".join(x["name"] for x in v["cats"]))}</option>' for v in sorted(_cmap.values(), key=lambda x: x["n"].lower()))
CCATOPTS = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)
calc_body = f"""<h1>What will it really cost?</h1><p class="tag">Pick a specific tool — or a whole category — then seats and monthly or annual billing. We multiply only the verified entry prices already in ToolPick's price table (checked on official pricing pages) and show the true monthly and yearly totals. Nothing is invented: no new prices, plan names, limits or features.</p>
<div class="builder"><form id="cform"><div class="cform">
<div><label for="cc-tool">Specific tool (optional)</label><select id="cc-tool" name="tool"><option value="">No specific tool — use category below</option>{CTOOLOPTS}</select></div>
<div><label for="cc-cat">Category (used when no tool is picked)</label><select id="cc-cat" name="category"><option value="">Select a category…</option>{CCATOPTS}</select></div>
<div><label for="cc-seats">Seats / users (1–50)</label><input type="number" id="cc-seats" name="seats" min="1" max="50" step="1" value="1" inputmode="numeric"><p class="small" style="margin:6px 0 0">Seats only change the total where the verified entry price itself is stated per seat / per user / per member. Otherwise we say so and seats don't change the listed price.</p></div>
<div><fieldset><legend>Billing period</legend><div class="seg" style="display:inline-flex"><input type="radio" name="cc-billing" id="cc-bill-m" value="monthly" checked><label for="cc-bill-m">Monthly billing</label><input type="radio" name="cc-billing" id="cc-bill-a" value="annual"><label for="cc-bill-a">Annual billing</label></div><p class="small" style="margin:6px 0 0">Annual means the per-month rate when billed yearly, from our table; the yearly total is that rate × 12.</p></fieldset></div>
</div><div class="bactions"><button type="submit" class="bbtn primary">Calculate cost</button><button type="button" class="bbtn" id="ccCopy">Copy share link</button><button type="button" class="bbtn" id="ccClear">Clear</button><span class="small bstatus" id="ccStatus" role="status"></span></div></form></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How we work this out — and what we don't claim</h2><p class="small" style="margin:0"><b>True monthly cost</b> is the verified entry rate for your billing choice (× seats only for a clearly per-seat entry price). <b>True yearly cost</b> is that monthly total × 12. <b>Cheapest verified plan we can price</b> means the lowest verified entry rate in our table for that tool — we only hold entry-tier rates, so we don't name plans or claim usage limits fit you; check the official pricing page for limits and higher tiers. Tools with no verified numeric entry price (“check site” or no rate in our table) are shown for reference, excluded from cheapest rankings, and never guessed. <b>Category Best Value rule:</b> first ToolPick's existing Best Value pick for that category if it has a verified price for your billing choice; otherwise the lowest verified entry with a verified free plan; otherwise the lowest verified entry. Free options use only our verified free-plan field — full free-tier limits are on the official pricing page.</p></div>
<div id="calc-out" aria-live="polite" aria-atomic="false"><div class="pick"><b>Pick a tool or a category to calculate.</b><p class="small" style="margin-bottom:0">Try <a href="/cost-calculator.html?tool=elevenlabs&amp;seats=1&amp;billing=monthly">ElevenLabs, 1 seat, monthly</a>, <a href="/cost-calculator.html?tool=clickup&amp;seats=10&amp;billing=annual">ClickUp, 10 seats, annual</a> (per-user entry), or <a href="/cost-calculator.html?category=audio&amp;seats=5&amp;billing=annual">all Audio tools, 5 seats, annual</a>.</p></div></div>
<p class="small">Browse first? <a href="/tools.html">Open the full tools directory →</a> · Compare tools instead? <a href="/compare-builder.html">Open the compare builder →</a> Prices change — always confirm on the official pricing page linked with every result.</p>
<script>const CD={CDATA};const CC={CATDATA};
const byS={{}};CD.forEach(t=>byS[t.s]=t);const catBy={{}};CC.forEach(c=>catBy[c.id]=c);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function pv(v){{if(v==null)return null;if(typeof v=='number')return{{amt:v,cur:'$'}};const m=String(v).match(/([€$£])\\s*([\\d.]+)/);if(m)return{{amt:parseFloat(m[2]),cur:m[1]}};const n=String(v).match(/([\\d.]+)/);return n?{{amt:parseFloat(n[1]),cur:'$'}}:null}}
function money(amt,cur){{const r=Math.round(amt*100)/100;return cur+(Number.isInteger(r)?String(r):r.toFixed(2))}}
function cost(t,billing,seats){{const rate=pv(billing=='annual'?t.a:t.m);if(!rate)return null;const f=t.ps?seats:1;return{{rate:rate,monthly:rate.amt*f,yearly:rate.amt*f*12,cur:rate.cur,factor:f}}}}
function basis(t,seats){{return t.ps?('Per-seat entry price × '+seats+' seat'+(seats==1?'':'s')):('Seats don’t change the listed price — seat basis not stated for the verified entry price (per-plan price as listed)')}} 
function freeBlock(t){{return `<p class="small">${{t.fr?'<span class="badge b-free">FREE PLAN</span> ':''}}${{X(t.f)}}<br>Free info is shown exactly as verified on the official page. We don't state free-tier limits that aren't in our data — full limits are listed on the <a href="${{X(t.pr)}}" rel="noopener" target="_blank">official pricing page</a>.</p>`}}
function cheapest(t,seats){{const opts=['monthly','annual'].map(b=>({{b:b,c:cost(t,b,seats)}})).filter(x=>x.c);if(!opts.length)return null;opts.sort((x,y)=>x.c.yearly-y.c.yearly);return opts[0]}}
function toolView(t,seats,billing){{const c=cost(t,billing,seats);const ch=cheapest(t,seats);const other=billing=='monthly'?'annual':'monthly';const co=cost(t,other,seats);
let h=`<h2>${{X(t.n)}} — true cost</h2><article class="card${{t.bestFor.length?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{t.bestFor.length?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p>${{freeBlock(t)}}<p class="small meta">${{X(t.cats.map(x=>x.name).join(', '))}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p></article>`;
if(!c&&!ch){{h+=`<div class="pick"><b>No verified numeric entry price for ${{X(t.n)}} in our price table, so we can't calculate a true cost and it is not ranked.</b><p class="small" style="margin-bottom:0">Listed price as verified: ${{X(t.p)}} (checked ${{t.k}}). We don't guess — see the <a href="${{X(t.pr)}}" rel="noopener" target="_blank">official pricing page</a> for current prices.</p></div>`;return h}}
if(!c){{h+=`<div class="pick"><b>No verified ${{billing}} entry rate for ${{X(t.n)}} in our table.</b><p class="small" style="margin-bottom:0">Switch billing above or see the priced option below. Listed price: ${{X(t.p)}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">official pricing page</a>.</p></div>`}}
else{{h+=`<div class="tw"><table><caption class="small" style="text-align:left;padding:12px 16px">${{X(t.n)}} at ${{seats}} seat${{seats==1?'':'s'}}, ${{billing}} billing. Checked ${{t.k}}.</caption><tr><th scope="col">Billing</th><th scope="col">Verified entry rate</th><th scope="col">True monthly cost</th><th scope="col">True yearly cost</th><th scope="col">Seat basis</th></tr><tr><td>${{billing=='annual'?'Annual (per-month rate, billed yearly)':'Monthly'}}</td><td>${{money(c.rate.amt,c.cur)}}/mo</td><td><b>${{money(c.monthly,c.cur)}}/mo</b></td><td><b>${{money(c.yearly,c.cur)}}/yr</b></td><td class="small">${{basis(t,seats)}}</td></tr>${{co?`<tr><td>${{other=='annual'?'Annual (for comparison)':'Monthly (for comparison)'}}</td><td>${{money(co.rate.amt,co.cur)}}/mo</td><td>${{money(co.monthly,co.cur)}}/mo</td><td>${{money(co.yearly,co.cur)}}/yr</td><td class="small">${{basis(t,seats)}}</td></tr>`:''}}</table></div>`}}
if(ch){{h+=`<div class="pick"><span class="badge b-best">CHEAPEST VERIFIED WE CAN PRICE</span> <b>${{money(ch.c.monthly,ch.c.cur)}}/mo (${{money(ch.c.yearly,ch.c.cur)}}/yr)</b> on ${{ch.b}} billing for ${{seats}} seat${{seats==1?'':'s'}}. <span class="small">This is the lowest verified entry rate in our table for this tool (${{basis(t,seats).toLowerCase()}}). We hold only entry-tier rates, so we don't name a plan or claim usage limits fit you — confirm limits and higher tiers on the <a href="${{X(t.pr)}}" rel="noopener" target="_blank">official pricing page</a> (checked ${{t.k}}).</span></div>`}}
return h}}
function catView(cat,seats,billing){{const rows=cat.tools.map(s=>byS[s]).filter(Boolean).map(t=>({{t:t,c:cost(t,billing,seats)}}));const priced=rows.filter(x=>x.c).sort((x,y)=>x.c.monthly-y.c.monthly);const unpriced=rows.filter(x=>!x.c);const bvT=priced.find(x=>x.t.s==cat.best);const bv=bvT||priced.filter(x=>x.t.fr).sort((x,y)=>x.c.monthly-y.c.monthly)[0]||priced[0]||null;const rule=bvT?'ToolPick’s existing Best Value pick for this category, with a verified price for your billing choice.':(bv&&bv.t.fr?'No priced category Best Value for this billing choice, so: lowest verified entry with a verified free plan.':'Lowest verified entry price for your billing choice.');
let h=`<h2>${{X(cat.name)}} — true costs (${{seats}} seat${{seats==1?'':'s'}}, ${{billing}} billing)</h2>`;
if(bv){{h+=`<div class="pick"><span class="badge b-best">BEST VALUE</span> <b><a href="${{bv.t.u}}">${{X(bv.t.n)}}</a></b> — ${{rule}} True cost: <b>${{money(bv.c.monthly,bv.c.cur)}}/mo · ${{money(bv.c.yearly,bv.c.cur)}}/yr</b>. <span class="small">${{basis(bv.t,seats)}} · checked ${{bv.t.k}} · <a href="${{X(bv.t.pr)}}" rel="noopener" target="_blank">official pricing page</a></span></div>`}}
else{{h+=`<div class="pick"><b>No verified numeric entry prices in this category for ${{billing}} billing, so nothing is ranked.</b><p class="small" style="margin-bottom:0">Try the other billing period, or check the official pricing pages linked below. We don't guess prices.</p></div>`}}
h+=`<div class="tw"><table><caption class="small" style="text-align:left;padding:12px 16px">Cheapest verified first. Tools with no verified rate for this billing choice are listed last and not ranked.</caption><tr><th scope="col">Tool</th><th scope="col">Listed price (as verified)</th><th scope="col">True monthly</th><th scope="col">True yearly</th><th scope="col">Free option</th><th scope="col">Checked</th></tr>`;
priced.concat(unpriced).forEach(x=>{{const t=x.t;h+=`<tr><td><a href="${{t.u}}">${{X(t.n)}}</a>${{bv&&t.s==bv.t.s?' <span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?' <span class="badge b-free">FREE PLAN</span>':''}}<br><span class="small">${{basis(t,seats)}}</span></td><td class="small">${{X(t.p)}}</td><td>${{x.c?('<b>'+money(x.c.monthly,x.c.cur)+'/mo</b>'):'<span class="check">No verified rate — not ranked</span>'}}</td><td>${{x.c?('<b>'+money(x.c.yearly,x.c.cur)+'/yr</b>'):'—'}}</td><td class="small">${{X(t.f)}}</td><td class="small">${{t.k}}<br><a href="${{X(t.pr)}}" rel="noopener" target="_blank">Pricing page</a></td></tr>`}});
h+=`</table></div><p class="small">Free-tier limits aren't stated beyond the verified free text above — full limits are on each official pricing page. Entry rates only; higher tiers are on the official pages.</p>`;return h}}
function vals(){{let seats=parseInt(document.getElementById('cc-seats').value,10);if(isNaN(seats))seats=1;seats=Math.min(50,Math.max(1,seats));const billing=(document.querySelector('input[name=cc-billing]:checked')||{{}}).value||'monthly';return{{tool:document.getElementById('cc-tool').value,cat:document.getElementById('cc-cat').value,seats:seats,billing:billing}}}}
function shareURL(v){{const q=new URLSearchParams();if(v.tool)q.set('tool',v.tool);else if(v.cat)q.set('category',v.cat);q.set('seats',String(v.seats));q.set('billing',v.billing);return location.origin+'/cost-calculator.html?'+q.toString()}}
function render(push=true){{const v=vals();document.getElementById('cc-seats').value=v.seats;const out=document.getElementById('calc-out');const st=document.getElementById('ccStatus');
if(v.tool&&byS[v.tool]){{out.innerHTML=toolView(byS[v.tool],v.seats,v.billing);st.textContent=byS[v.tool].n+' cost calculated. Share link updated.'}}
else if(v.cat&&catBy[v.cat]){{out.innerHTML=catView(catBy[v.cat],v.seats,v.billing);st.textContent=catBy[v.cat].name+' costs calculated, cheapest verified first. Share link updated.'}}
else{{out.innerHTML='<div class="pick"><b>Pick a tool or a category to calculate.</b><p class="small" style="margin-bottom:0">Choose a specific tool above, or choose a category (it is used when no tool is picked), set seats and billing, then Calculate. If a tool has no verified numeric price we will say so plainly instead of guessing.</p></div>';st.textContent='Nothing selected yet.';if(push)history.replaceState(null,'','/cost-calculator.html');return}}
if(push)history.replaceState(null,'',shareURL(v).replace(location.origin,''));}}
document.getElementById('cform').addEventListener('submit',ev=>{{ev.preventDefault();render();document.getElementById('calc-out').scrollIntoView({{behavior:'smooth',block:'start'}})}});
['cc-tool','cc-cat','cc-seats'].forEach(id=>document.getElementById(id).addEventListener('change',()=>render()));
document.querySelectorAll('input[name=cc-billing]').forEach(r=>r.addEventListener('change',()=>render()));
document.getElementById('ccClear').addEventListener('click',()=>{{document.getElementById('cc-tool').value='';document.getElementById('cc-cat').value='';document.getElementById('cc-seats').value='1';document.getElementById('cc-bill-m').checked=true;render();document.getElementById('ccStatus').textContent='Cleared. Pick a tool or category.';document.getElementById('cc-tool').focus()}});
document.getElementById('ccCopy').addEventListener('click',async()=>{{const v=vals();const st=document.getElementById('ccStatus');if(!v.tool&&!v.cat){{st.textContent='Pick a tool or category before copying a share link.';return}}const url=shareURL(v);try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
(function init(){{const q=new URLSearchParams(location.search);const t=q.get('tool'),c=q.get('category'),s=q.get('seats'),b=q.get('billing');if(t&&byS[t])document.getElementById('cc-tool').value=t;if(c&&catBy[c])document.getElementById('cc-cat').value=c;if(s)document.getElementById('cc-seats').value=s;if(b=='annual')document.getElementById('cc-bill-a').checked=true;render(!!(t||c));}})();
</script>"""
page("/cost-calculator.html", "What Will It Really Cost? AI Tool Cost Calculator — True Monthly & Yearly Cost | ToolPick", "Pick a tool or category, seats and monthly or annual billing to see true monthly and yearly cost from verified entry prices, with checked dates and official pricing links.", calc_body,
     [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick cost calculator","url":BASE+"/cost-calculator.html","description":"Calculate true monthly and yearly AI tool cost by seats and billing period from verified entry prices."}, crumbs([("ToolPick","/"),("Cost calculator","/cost-calculator.html")])])


# --- Help me choose wizard (v11 preview) ---
# Steps use only fields present for all tools: category membership, PRICE_TABLE monthly/annual,
# per-seat wording in the verified price text (same rule as cost calculator), free text via realfree(),
# category best pick, and verified annual<monthly availability in PRICE_TABLE.
_wmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _wmap:
            _wmap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"],
                             ps=_perseat(_t), fr=realfree(_t), cats=[], bestFor=[])
        if _c["id"] not in _wmap[_k]["cats"]: _wmap[_k]["cats"].append(_c["id"])
        if _t["name"] == _c["best"] and _c["id"] not in _wmap[_k]["bestFor"]: _wmap[_k]["bestFor"].append(_c["id"])
WDATA = json.dumps(sorted(_wmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
WCATS = json.dumps([dict(id=c["id"], name=c["name"], need=c["need"], best=slug(c["best"]), bestName=c["best"], tools=[slug(t["name"]) for t in c["tools"]]) for c in CATEGORIES]).replace("</", "<\\/")
WCATOPTS = "".join(f'<label><input type="radio" name="wcat" value="{c["id"]}"><span><b>{e(c["name"])}</b> — {e(c["need"])}</span></label>' for c in CATEGORIES)
wizard_body = f"""<h1>Help me choose an AI tool</h1><p class="tag">Answer 5 quick questions — what you need, your budget, billing and seats, and two must-haves we can actually verify — and get a ranked shortlist of 3–5 tools with verified prices, checked dates and a plain reason for each pick. We only ask about things in our verified data, so we don't ask about API access, commercial-use rights, privacy terms or skill level.</p>
<div class="builder"><p class="small" id="wprog-label" role="status">Step 1 of 5</p><div class="wizprog" aria-hidden="true"><i id="wbar" style="width:20%"></i></div>
<form id="wform">
<section class="wstep" data-step="1"><fieldset><legend>1. What are you trying to do?</legend><div class="opts">{WCATOPTS}</div></fieldset></section>
<section class="wstep" data-step="2" hidden><fieldset><legend>2. What is your monthly budget?</legend><div class="opts">
<label><input type="radio" name="wbudget" value="free"><span><b>Free only</b> — I want to use a verified free plan ($0)</span></label>
<label><input type="radio" name="wbudget" value="10"><span><b>Under $10/mo</b> — verified entry cost up to $10/mo for my billing and seats</span></label>
<label><input type="radio" name="wbudget" value="25"><span><b>Under $25/mo</b> — verified entry cost up to $25/mo for my billing and seats</span></label>
<label><input type="radio" name="wbudget" value="any" checked><span><b>Any budget</b> — show the best fits regardless of verified entry price</span></label>
</div></fieldset></section>
<section class="wstep" data-step="3" hidden><fieldset><legend>3. Billing period and seats</legend><div class="opts">
<label><input type="radio" name="wbilling" value="monthly" checked><span><b>Monthly billing</b></span></label>
<label><input type="radio" name="wbilling" value="annual"><span><b>Annual billing</b> — per-month rate when billed yearly</span></label>
</div><label for="wseats" style="font-weight:600;display:block;margin-top:16px">Seats / users (1–50)</label><input type="number" id="wseats" name="wseats" min="1" max="50" step="1" value="1" inputmode="numeric" style="width:100%;min-height:48px;margin-top:8px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px"><p class="small" style="margin:6px 0 0">Seats only multiply the cost where the verified entry price itself says per seat / per user / per member / per person — the same rule as our cost calculator.</p></fieldset></section>
<section class="wstep" data-step="4" hidden><fieldset><legend>4. Must it have a real free plan?</legend><div class="opts">
<label><input type="radio" name="wfree" value="any" checked><span><b>No preference</b></span></label>
<label><input type="radio" name="wfree" value="required"><span><b>Must have a real free plan</b> — verified free plan only; free trials and one-time credits don't count</span></label>
</div></fieldset></section>
<section class="wstep" data-step="5" hidden><fieldset><legend>5. Must annual billing be verified cheaper?</legend><div class="opts">
<label><input type="radio" name="wannual" value="any" checked><span><b>No preference</b></span></label>
<label><input type="radio" name="wannual" value="required"><span><b>Must have a verified annual saving</b> — both monthly and annual rates verified, and annual is cheaper</span></label>
</div></fieldset></section>
<div class="wnav"><button type="button" class="bbtn" id="wBack">Back</button><button type="button" class="bbtn primary" id="wNext">Next</button><button type="button" class="bbtn" id="wCopy">Copy share link</button><span class="small bstatus" id="wStatus" role="status"></span></div>
</form></div>
<p class="small">Prefer to browse? <a href="/tools.html">See the full directory of all 82 tools with filters →</a></p><div id="wiz-out" aria-live="polite" aria-atomic="false"></div>
<script>const WD={WDATA};const WC={WCATS};
const byS={{}};WD.forEach(t=>byS[t.s]=t);const catBy={{}};WC.forEach(c=>catBy[c.id]=c);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function pv(v){{if(v==null)return null;if(typeof v=='number')return{{amt:v,cur:'$'}};const m=String(v).match(/([€$£])\\s*([\\d.]+)/);if(m)return{{amt:parseFloat(m[2]),cur:m[1]}};const n=String(v).match(/([\\d.]+)/);return n?{{amt:parseFloat(n[1]),cur:'$'}}:null}}
function money(amt,cur){{const r=Math.round(amt*100)/100;return cur+(Number.isInteger(r)?String(r):r.toFixed(2))}}
function eff(t,billing,seats){{const rate=pv(billing=='annual'?t.a:t.m);if(!rate)return null;const f=t.ps?seats:1;return{{amt:rate.amt*f,cur:rate.cur,rate:rate.amt,factor:f}}}}
function annualSave(t){{const m=pv(t.m),a=pv(t.a);return (m&&a&&m.cur==a.cur&&a.amt<m.amt)?{{m:m,a:a}}:null}}
let step=1;
function vals(){{let seats=parseInt(document.getElementById('wseats').value,10);if(isNaN(seats))seats=1;seats=Math.min(50,Math.max(1,seats));const g=n=>{{const el=document.querySelector('input[name='+n+']:checked');return el?el.value:''}};return{{category:g('wcat'),budget:g('wbudget')||'any',billing:g('wbilling')||'monthly',seats:seats,free:g('wfree')||'any',annual:g('wannual')||'any'}}}}
function shareURL(v){{const q=new URLSearchParams();if(v.category)q.set('category',v.category);q.set('budget',v.budget);q.set('billing',v.billing);q.set('seats',String(v.seats));q.set('free',v.free);q.set('annual',v.annual);return location.origin+'/help-me-choose.html?'+q.toString()}}
function showStep(n){{step=Math.min(5,Math.max(1,n));document.querySelectorAll('.wstep').forEach(s=>s.hidden=+s.dataset.step!=step);document.getElementById('wbar').style.width=(step*20)+'%';document.getElementById('wprog-label').textContent='Step '+step+' of 5';document.getElementById('wBack').disabled=step==1;document.getElementById('wNext').textContent=step==5?'See my shortlist':'Next';const first=document.querySelector('.wstep[data-step="'+step+'"] input');if(first&&document.activeElement&&document.activeElement.id!='wseats'){{/* keep focus natural on button click */}}}}
function fitsBudget(t,v,e){{if(v.budget=='any')return true;if(v.budget=='free')return t.fr;return !!(e&&e.cur=='$'&&e.amt<=parseFloat(v.budget))}}
function card(t,v,e,opts){{const isBV=opts.bv&&t.s==opts.bv.s;const reasons=[];
if(t.bestFor.includes(v.category))reasons.push('ToolPick’s existing Best Value pick for '+catBy[v.category].name);
if(opts.lowest&&t.s==opts.lowest.t.s&&e)reasons.push('Lowest verified price in '+catBy[v.category].name+' at '+money(e.amt,e.cur)+'/mo');
if(t.fr)reasons.push('Has a verified free plan');
const sv=annualSave(t);if(sv&&v.billing=='annual')reasons.push('Annual billing saves '+money(sv.m.amt-sv.a.amt,sv.a.cur)+'/mo vs monthly per verified rates ('+money(sv.a.amt,sv.a.cur)+' vs '+money(sv.m.amt,sv.m.cur)+')');
if(e&&t.ps&&v.seats>1)reasons.push('Per-seat entry price × '+v.seats+' seats');
if(opts.over&&e)reasons.push('Closest verified option at '+money(e.amt,e.cur)+'/mo — over your '+(v.budget=='free'?'free-only':('$'+v.budget+'/mo'))+' budget');
else if(e&&v.budget!='any'&&v.budget!='free')reasons.push('Verified entry '+money(e.amt,e.cur)+'/mo fits your $'+v.budget+' budget');
if(!opts.over&&v.budget=='free'&&t.fr)reasons.push('Fits free-only using its verified free plan');
if(!e)reasons.push('Price not verified in our table — shown unranked, never assumed to fit a budget');
const uniq=[...new Set(reasons)].slice(0,3);
return `<article class="card${{isBV?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{opts.over?'<span class="badge" style="background:var(--warn);color:#fff">OVER BUDGET</span>':''}}${{isBV?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}${{!e&&!opts.over?'<span class="badge b-rank">PRICE NOT VERIFIED</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p>${{e?`<p><b>${{money(e.amt,e.cur)}}/mo</b> <span class="small">true entry cost at ${{v.seats}} seat${{v.seats==1?'':'s'}}, ${{v.billing}} billing${{t.ps?' (per-seat price × seats)':' (seats don’t change the listed price)'}}</span></p>`:`<p class="small check">No verified numeric entry rate for ${{v.billing}} billing — not ranked by price.</p>`}}<p class="small">${{X(t.f)}}</p>${{uniq.length?`<p class="small"><b>Why this pick:</b> ${{uniq.map(X).join(' · ')}}</p>`:''}}<p class="small meta">${{catBy[v.category].name}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p><p class="small"><a href="${{t.u}}">Tool page →</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=${{v.seats}}&amp;billing=${{v.billing}}">Cost calculator for ${{X(t.n)}} →</a></p></article>`}}
function results(push=true){{const v=vals();const out=document.getElementById('wiz-out');const st=document.getElementById('wStatus');if(!v.category){{st.textContent='Pick what you are trying to do first.';showStep(1);return}}
const cat=catBy[v.category];let cand=cat.tools.map(s=>byS[s]).filter(Boolean).map(t=>({{t:t,e:eff(t,v.billing,v.seats)}}));
cand=cand.filter(x=>(v.free!='required'||x.t.fr)&&(v.annual!='required'||annualSave(x.t)));
const fitting=cand.filter(x=>fitsBudget(x.t,v,x.e));
const priced=fitting.filter(x=>x.e&&x.e.cur=='$').sort((a,b)=>a.e.amt-b.e.amt);
const lowest=priced[0]||null;
let bv=null;const catBest=fitting.find(x=>x.t.s==cat.best);if(catBest)bv=catBest.t;else if(priced.length){{const wf=priced.filter(x=>x.t.fr);bv=(wf[0]||priced[0]).t}}
const ranked=fitting.slice().sort((a,b)=>{{const ab=a.t.s==cat.best?0:1,bb=b.t.s==cat.best?0:1;if(ab!=bb)return ab-bb;const ae=a.e?a.e.amt:1e12,be=b.e?b.e.amt:1e12;if(ae!=be)return ae-be;if(a.t.fr!=b.t.fr)return a.t.fr?-1:1;return a.t.n.localeCompare(b.t.n)}});
const short=ranked.slice(0,5);
let h=`<h2>Your shortlist for ${{X(cat.name)}}</h2><p class="small">Budget: ${{v.budget=='free'?'Free only':v.budget=='any'?'Any':('Under $'+v.budget+'/mo')}} · ${{v.billing}} billing · ${{v.seats}} seat${{v.seats==1?'':'s'}}${{v.free=='required'?' · real free plan required':''}}${{v.annual=='required'?' · verified annual saving required':''}}. Prices checked on official pages — confirm before buying.</p>`;
if(short.length){{h+=`<div class="grid">${{short.map(x=>card(x.t,v,x.e,{{bv:bv,lowest:lowest}})).join('')}}</div><p><a class="btn" href="/compare-builder.html?tools=${{short.slice(0,3).map(x=>x.t.s).join(',')}}">Compare the top 3 of this shortlist side by side →</a></p><p class="small"><a href="/cost-calculator.html?category=${{v.category}}&amp;seats=${{v.seats}}&amp;billing=${{v.billing}}">See true costs for all ${{X(cat.name)}} tools →</a> · Share link: <a href="${{shareURL(v)}}">${{shareURL(v)}}</a></p><p><button type="button" class="bbtn" onclick="document.getElementById('wiz-out').innerHTML='';showStep(1);document.querySelector('input[name=wcat]').focus()">Start again</button></p>`}}
else{{const closest=cand.filter(x=>x.e&&x.e.cur=='$').sort((a,b)=>a.e.amt-b.e.amt).slice(0,3);h+=`<div class="pick"><b>Nothing in ${{X(cat.name)}} fits those answers — we haven't relaxed your budget.</b><p class="small" style="margin-bottom:0">Try a higher budget, the other billing period, or drop a must-have. ${{closest.length?'The closest verified options are below, clearly labelled over budget.':'No verified numeric prices are available for the remaining tools, so we can’t rank closest options.'}}</p></div>`;if(closest.length){{h+=`<div class="grid">${{closest.map(x=>card(x.t,v,x.e,{{bv:null,lowest:null,over:true}})).join('')}}</div>`}}h+=`<p class="small"><a href="/cost-calculator.html?category=${{v.category}}&amp;seats=${{v.seats}}&amp;billing=${{v.billing}}">See true costs for all ${{X(cat.name)}} tools →</a></p>`}}
out.innerHTML=h;st.textContent=short.length?(short.length+' tools in your shortlist. Share link updated.'):'No fitting tools — closest options shown over budget.';
if(push)history.replaceState(null,'',shareURL(v).replace(location.origin,''));
out.scrollIntoView({{behavior:'smooth',block:'start'}});}}
document.getElementById('wNext').addEventListener('click',()=>{{const v=vals();if(step==1&&!v.category){{document.getElementById('wStatus').textContent='Pick what you are trying to do to continue.';return}}if(step<5){{showStep(step+1);const f=document.querySelector('.wstep[data-step="'+step+'"] input, .wstep[data-step="'+step+'"] button');if(f)f.focus()}}else results()}});
document.getElementById('wBack').addEventListener('click',()=>{{if(step>1){{showStep(step-1);const f=document.querySelector('.wstep[data-step="'+step+'"] input');if(f)f.focus()}}}});
document.getElementById('wCopy').addEventListener('click',async()=>{{const v=vals();const st=document.getElementById('wStatus');if(!v.category){{st.textContent='Pick a category before copying a share link.';showStep(1);return}}const url=shareURL(v);try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
(function init(){{const q=new URLSearchParams(location.search);const set=(name,val)=>{{if(!val)return;const el=document.querySelector('input[name='+name+'][value="'+val+'"]');if(el)el.checked=true}};set('wcat',q.get('category'));set('wbudget',q.get('budget'));set('wbilling',q.get('billing'));set('wfree',q.get('free'));set('wannual',q.get('annual'));if(q.get('seats'))document.getElementById('wseats').value=q.get('seats');showStep(1);if(q.get('category'))results(false);}})();
</script>"""
page("/help-me-choose.html", "Help Me Choose an AI Tool — 5-Step Wizard with Verified Prices | ToolPick", "Answer 5 quick questions about your task, budget, billing, seats and must-haves to get a ranked shortlist of AI tools with verified prices, checked dates, official pricing links and a Best Value pick.", wizard_body,
     [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick Help me choose wizard","url":BASE+"/help-me-choose.html","description":"Guided wizard that returns a ranked shortlist of AI tools from verified prices."}, crumbs([("ToolPick","/"),("Help me choose","/help-me-choose.html")])])


# --- Browse all tools directory (v12 preview) ---
# Filters use only verified fields already in tools.py/PRICE_TABLE: category membership,
# realfree(), PRICE_TABLE monthly/annual availability, lowest numeric entry rate,
# and _perseat() wording in the verified entry price text. No usage-based, team-plan,
# skill or use-case fields exist across tools, so none are offered (category is labelled category).
_dmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _dmap:
            _dmap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"],
                             ps=_perseat(_t), fr=realfree(_t), cats=[], bestFor=[])
        if _c["id"] not in [x["id"] for x in _dmap[_k]["cats"]]: _dmap[_k]["cats"].append(dict(id=_c["id"], name=_c["name"]))
        if _t["name"] == _c["best"] and _c["id"] not in _dmap[_k]["bestFor"]: _dmap[_k]["bestFor"].append(_c["id"])
DDATA = json.dumps(sorted(_dmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
DCATOPTS = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)
directory_body = f"""<h1>Browse all AI tools</h1><p class="tag">Every tool on ToolPick — {total_tools} tools across {len(CATEGORIES)} categories — with filters that only use verified data: category, a real free plan, the lowest verified entry price in our price table, whether a monthly or annual-billing entry rate is verified, and whether that entry price itself is stated per seat / per user / per member / per person. Prices show their checked date and link to the official pricing page.</p>
<div class="builder"><h2 style="margin-top:0;font-size:1.05rem">Filter and sort tools</h2><form id="dform"><div class="dform">
<div><label for="d-cat">Category</label><select id="d-cat" name="category"><option value="">All categories</option>{DCATOPTS}</select></div>
<div><label for="d-free">Free plan</label><select id="d-free" name="free"><option value="any">Any</option><option value="yes">Has a real free plan</option><option value="no">No real free plan</option></select></div>
<div><label for="d-price">Starting price (verified entry)</label><select id="d-price" name="price"><option value="any">Any price</option><option value="free">Free to start (verified free plan)</option><option value="u10">Under $10/mo</option><option value="10-25">$10–$25/mo</option><option value="over25">Over $25/mo</option><option value="unverified">Price not verified (no numeric entry rate)</option></select></div>
<div><label for="d-billing">Billing availability (verified)</label><select id="d-billing" name="billing"><option value="any">Any</option><option value="monthly">Has verified monthly rate</option><option value="annual">Has verified annual rate</option><option value="both">Both monthly &amp; annual verified</option></select></div>
<div><label for="d-seat">Seat pricing</label><select id="d-seat" name="seat"><option value="any">Any</option><option value="perseat">Per-seat entry price only</option><option value="flat">Not stated per-seat for entry price</option></select></div>
<div><label for="d-sort">Sort by</label><select id="d-sort" name="sort"><option value="value">Best Value</option><option value="price">Lowest verified starting price</option><option value="name">Name A–Z</option></select></div>
</div><div class="bactions"><button type="button" class="bbtn primary" id="dCopy">Copy share link</button><button type="button" class="bbtn" id="dClear">Clear all filters</button><span class="small bstatus" id="dStatus" role="status"></span></div></form>
<p class="small" style="margin:12px 0 0">How prices are bucketed: the lowest verified monthly or annual-billing entry rate in ToolPick's price table. Tools with no numeric entry rate there (“check site”, custom or usage-only with no entry rate in our table) only appear under <b>Price not verified</b> — they are never assumed into a price range, and they sort last by price. We don't offer usage-based, team-plan or use-case filters because those fields aren't verified across our tools; category above is the category, nothing more.</p></div>
<h2>Results</h2><p id="dir-count" role="status" aria-live="polite"></p>
<div class="tray" id="dir-tray"><span id="tray-count"><b>Compare tray: 0 of 3 selected</b></span><span id="tray-list" class="small">Add up to 3 tools from the cards below.</span><a class="bbtn primary" id="dir-go" href="/compare-builder.html">Compare these tools →</a><button type="button" class="bbtn" id="tray-clear">Clear compare tray</button></div>
<div id="dir-out"></div>
<p class="small">Found a shortlist? <a href="/help-me-choose.html">Help me choose in 5 steps →</a> · <a href="/cost-calculator.html">What will it really cost? →</a> Prices change — always confirm on the official pricing page linked on every card.</p>
<script>const DD={DDATA};
const byS={{}};DD.forEach(t=>byS[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function pv(v){{if(v==null)return null;if(typeof v=='number')return{{amt:v,cur:'$'}};const m=String(v).match(/([€$£])\\s*([\\d.]+)/);if(m)return{{amt:parseFloat(m[2]),cur:m[1]}};const n=String(v).match(/([\\d.]+)/);return n?{{amt:parseFloat(n[1]),cur:'$'}}:null}}
function entry(t){{const vals=[pv(t.m),pv(t.a)].filter(Boolean);if(!vals.length)return null;vals.sort((a,b)=>a.amt-b.amt);return vals[0]}}
function money(amt,cur){{const r=Math.round(amt*100)/100;return cur+(Number.isInteger(r)?String(r):r.toFixed(2))}}
let compareSel=[];
const ids={{cat:'d-cat',free:'d-free',price:'d-price',billing:'d-billing',seat:'d-seat',sort:'d-sort'}};
function vals(){{return{{category:document.getElementById(ids.cat).value,free:document.getElementById(ids.free).value,price:document.getElementById(ids.price).value,billing:document.getElementById(ids.billing).value,seat:document.getElementById(ids.seat).value,sort:document.getElementById(ids.sort).value}}}}
function sharePath(v){{const q=new URLSearchParams();if(v.category)q.set('category',v.category);if(v.free!='any')q.set('free',v.free);if(v.price!='any')q.set('price',v.price);if(v.billing!='any')q.set('billing',v.billing);if(v.seat!='any')q.set('seat',v.seat);if(v.sort!='value')q.set('sort',v.sort);const s=q.toString();return '/tools.html'+(s?('?'+s):'')}}
function matches(t,v){{const en=entry(t);
if(v.category&&!t.cats.some(c=>c.id==v.category))return false;
if(v.free=='yes'&&!t.fr)return false; if(v.free=='no'&&t.fr)return false;
if(v.price=='free'&&!t.fr)return false;
if(v.price=='u10'&&!(en&&en.amt<10))return false;
if(v.price=='10-25'&&!(en&&en.amt>=10&&en.amt<=25))return false;
if(v.price=='over25'&&!(en&&en.amt>25))return false;
if(v.price=='unverified'&&en)return false;
if(v.billing=='monthly'&&t.m==null)return false;
if(v.billing=='annual'&&t.a==null)return false;
if(v.billing=='both'&&(t.m==null||t.a==null))return false;
if(v.seat=='perseat'&&!t.ps)return false;
if(v.seat=='flat'&&t.ps)return false;
return true}}
function isBV(t,v){{return v.category?t.bestFor.includes(v.category):t.bestFor.length>0}}
function sortList(list,v){{const en=t=>entry(t);
if(v.sort=='name')return list.sort((a,b)=>a.n.localeCompare(b.n));
if(v.sort=='price')return list.sort((a,b)=>{{const ea=en(a),eb=en(b);if(ea&&eb&&ea.amt!=eb.amt)return ea.amt-eb.amt;if(ea&&!eb)return -1;if(!ea&&eb)return 1;return a.n.localeCompare(b.n)}});
return list.sort((a,b)=>{{const ba=isBV(a,v)?0:1,bb=isBV(b,v)?0:1;if(ba!=bb)return ba-bb;const ea=en(a),eb=en(b);const ga=ea?(a.fr?0:1):2,gb=eb?(b.fr?0:1):2;if(ga!=gb)return ga-gb;if(ea&&eb&&ea.amt!=eb.amt)return ea.amt-eb.amt;if(ea&&!eb)return -1;if(!ea&&eb)return 1;return a.n.localeCompare(b.n)}})}}
function tray(){{const tc=document.getElementById('tray-count'),tl=document.getElementById('tray-list'),go=document.getElementById('dir-go');
tc.innerHTML='<b>Compare tray: '+compareSel.length+' of 3 selected</b>';
tl.innerHTML=compareSel.length?compareSel.map(s=>'<span>'+X(byS[s].n)+' <button type="button" class="bbtn" data-rm="'+X(s)+'" aria-label="Remove '+X(byS[s].n)+' from compare">Remove</button></span>').join(' · '):'Add up to 3 tools from the cards below.';
go.href=compareSel.length>=2?('/compare-builder.html?tools='+compareSel.join(',')):'/compare-builder.html';
go.textContent=compareSel.length>=2?('Compare '+compareSel.length+' tools →'):'Compare these tools → (pick 2–3)';
tl.querySelectorAll('[data-rm]').forEach(b=>b.addEventListener('click',()=>{{compareSel=compareSel.filter(x=>x!=b.dataset.rm);tray();render(false);document.getElementById('dStatus').textContent=byS[b.dataset.rm].n+' removed from compare tray.'}}))}}
function card(t,v){{const en=entry(t);const bv=isBV(t,v);const added=compareSel.includes(t.s);
return `<article class="card${{bv?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{bv?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}${{!en?'<span class="badge b-rank">PRICE NOT VERIFIED</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p>${{en?`<p class="small">Lowest verified entry: <b>${{money(en.amt,en.cur)}}/mo</b> (monthly or annual billing, from our price table)${{t.ps?' · per-seat entry price as listed':''}}</p>`:`<p class="small check">No verified numeric entry rate in our price table — not placed in a price range.</p>`}}<p class="small">${{X(t.f)}}</p><p class="small meta">${{X(t.cats.map(c=>c.name).join(', '))}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p><p class="small"><a href="${{t.u}}">Tool page →</a></p><button type="button" class="bbtn addbtn" data-add="${{t.s}}" ${{added?'disabled':''}}>${{added?'Added to compare ✓':'Add to compare'}}</button></article>`}}
function render(push=true){{const v=vals();const list=sortList(DD.filter(t=>matches(t,v)),v);const out=document.getElementById('dir-out');
document.getElementById('dir-count').textContent=list.length+' of '+DD.length+' tools shown';
out.innerHTML=list.length?('<div class="grid">'+list.map(t=>card(t,v)).join('')+'</div>'):'<div class="pick"><b>No tools match those filters.</b><p class="small" style="margin-bottom:0">Try a wider price range or another category. Tools with no verified numeric entry price only appear under “Price not verified”.</p></div>';
out.querySelectorAll('[data-add]').forEach(b=>b.addEventListener('click',()=>{{const s=b.dataset.add;if(compareSel.includes(s))return;if(compareSel.length>=3){{document.getElementById('dStatus').textContent='Compare holds a maximum of 3 tools. Remove one from the tray first.';return}}compareSel.push(s);b.disabled=true;b.textContent='Added to compare ✓';tray();document.getElementById('dStatus').textContent=byS[s].n+' added to compare ('+compareSel.length+' of 3).'}}));
if(push)history.replaceState(null,'',sharePath(v));}}
Object.values(ids).forEach(id=>document.getElementById(id).addEventListener('change',()=>render()));
document.getElementById('dCopy').addEventListener('click',async()=>{{const v=vals();const url=location.origin+sharePath(v);const st=document.getElementById('dStatus');try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
document.getElementById('dClear').addEventListener('click',()=>{{document.getElementById(ids.cat).value='';document.getElementById(ids.free).value='any';document.getElementById(ids.price).value='any';document.getElementById(ids.billing).value='any';document.getElementById(ids.seat).value='any';document.getElementById(ids.sort).value='value';render();document.getElementById('dStatus').textContent='All filters cleared.';document.getElementById(ids.cat).focus()}});
document.getElementById('tray-clear').addEventListener('click',()=>{{compareSel=[];tray();render(false);document.getElementById('dStatus').textContent='Compare tray cleared.'}});
(function init(){{const q=new URLSearchParams(location.search);const set=(id,val)=>{{if(!val)return;const el=document.getElementById(id);if([...el.options].some(o=>o.value==val))el.value=val}};set(ids.cat,q.get('category'));set(ids.free,q.get('free'));set(ids.price,q.get('price'));set(ids.billing,q.get('billing'));set(ids.seat,q.get('seat'));set(ids.sort,q.get('sort'));tray();render(false);}})();
</script>"""
page("/tools.html", "Browse All AI Tools — Filter by Category, Free Plan & Verified Price | ToolPick", f"Browse all {total_tools} AI tools with filters for category, real free plans, verified starting price, monthly/annual billing availability and per-seat pricing. Add up to 3 tools to compare, with checked dates and official pricing links.", directory_body,
     [{"@context":"https://schema.org","@type":"ItemList","name":"All AI tools on ToolPick","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+v["u"],"name":v["n"]} for i,v in enumerate(sorted(_dmap.values(), key=lambda x: x["n"].lower()))]}, crumbs([("ToolPick","/"),("Browse all tools","/tools.html")])])


# best AI tool for [job] pages
for js, job, cid, ranked in JOBS:
    path = f"/best-ai-tool-for-{js}.html"; c = next(x for x in CATEGORIES if x["id"] == cid)
    title = f"Best AI Tool for {job[0].upper()+job[1:]} ({CHECKED[:4]}) — Top 3 with Prices"
    d = f"The top 3 AI tools for {job}: {', '.join(ranked)}. Prices checked {CHECKED} on official pricing pages."
    items = "".join(f"<li><h3><a href='{turl(n)}'>{e(n)}</a></h3><p>{e(find(n)['about'])}</p><p class='price'>💲 {e(find(n)['price'])}</p><p>🆓 {e(find(n)['free'])}</p><p class='small'>checked {find(n).get('checked', CHECKED)}</p></li>" for n in ranked)
    body = f"""<h1>Best AI tool for {e(job)}</h1><p class="tag">{e(d)}</p><ol>{items}</ol><div class="sponsor">Sponsored slot available — <a href="/sponsor.html">sponsor ToolPick</a></div>
<p>More options: <a href="/best-ai-{cid}-tools.html">all AI {e(c['name'].lower())} tools</a> · <a href="/tools.html?category={cid}">browse them in the full directory with price and free-plan filters</a>.</p>{complinks(comps_for(ranked))}
<h2>Other jobs</h2><ul>{''.join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS if j[0]!=js)}</ul>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(n),"name":n} for i,n in enumerate(ranked)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Best AI tool for {job}",path)])])

# free alternative pages
def hasfree(t, c):
    f = t["free"].lower()
    return realfree(t)
FREE_ALT_URLS = []
for name in FREE_ALT_FOR:
    cats = tool_pages[name]; t = find(name)
    alts = list(dict.fromkeys(x["name"] for c in cats for x in c["tools"] if x["name"] != name and hasfree(x, c)))
    if not alts: continue
    path = f"/free-alternative-to-{slug(name)}.html"; FREE_ALT_URLS.append((name, path))
    title = f"Free Alternatives to {name} ({CHECKED[:4]}) — {len(alts)} Options with Free Plans"
    d = f"{name} costs {t['price']}. Free alternatives with a verified free tier: {', '.join(alts[:5])}. Checked {CHECKED}."[:300]
    items = "".join(f"<li><h3><a href='{turl(a)}'>{e(a)}</a></h3><p>{e(find(a)['about'])}</p><p>🆓 {e(find(a)['free'])}</p><p class='price'>💲 Paid: {e(find(a)['price'])}</p><p class='small'>checked {find(a).get('checked', CHECKED)}</p></li>" for a in alts)
    body = f"""<h1>Free alternatives to {e(name)}</h1><p class="tag">{e(d)}</p><p><a href="{turl(name)}">{e(name)}</a>: {e(t['price'])}. Free tier: {e(t['free'])}.</p><ol>{items}</ol>
<p class="small">Only tools whose official pricing page showed a free plan on {CHECKED} are listed.</p><p>See all <a href="/best-ai-{cats[0]['id']}-tools.html">AI {e(cats[0]['name'].lower())} tools</a>.</p>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(a),"name":a} for i,a in enumerate(alts)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Free alternatives to {name}",path)])])


# --- v13 SEO pages: free alternatives (Recraft, Rytr) + best AI video tools under $20 ---
# Only verified tools.py data: price text, free text via realfree(), PRICE_TABLE entry rates, checked dates, pricing URLs.
# Ranking follows existing site logic: category Best Value pick first, then lowest verified entry, then name.
# Free-alternative alternatives must be same-category and realfree(). Video list: verified entry < $20/mo exactly
# (entry = lowest numeric monthly/annual rate in PRICE_TABLE); title therefore says "under $20", never "$20 or less".
def _seo_rank(tools, cat):
    def key(t):
        is_best = 0 if t["name"] == cat["best"] else 1
        en = _entry_num(t)
        return (is_best, en if en is not None else 1e12, t["name"].lower())
    return sorted(tools, key=key)
def _seo_card(t, cat, rank, best_name, lowest_name):
    en = _entry_num(t)
    is_best = t["name"] == best_name
    badges = (f"<span class='badge b-rank'>#{rank}</span>" if True else "") + ("<span class='badge b-best'>BEST VALUE</span>" if is_best else "") + ("<span class='badge b-free'>FREE PLAN</span>" if realfree(t) else "")
    reasons = []
    if is_best: reasons.append(f"ToolPick's Best Value pick for {cat['name']}")
    if lowest_name and t["name"] == lowest_name and en is not None: reasons.append(f"Lowest verified entry on this page at ${en:g}/mo")
    if realfree(t): reasons.append("Has a verified real free plan (trials and one-time credits do not count)")
    if en is not None: reasons.append(f"Verified entry ${en:g}/mo from our price table")
    else: reasons.append("No verified numeric entry rate in our price table")
    reason_txt = " · ".join(dict.fromkeys(reasons))
    entry_line = f"Lowest verified entry: ${en:g}/mo (monthly or annual billing, from our price table)" if en is not None else "Entry price not verified in our price table"
    return f"""<article class="card{' best' if is_best else ''}"><div class="th">{logo(t)}<div><div class="badges">{badges}</div><h3><a href="{turl(t['name'])}">{e(t['name'])}</a></h3></div></div><p>{e(t['about'])}</p>
<p class="price">{e(t['price'])}</p><p class="small">{e(entry_line)}</p><p class="small">{e(t['free'])}</p><p class="small"><b>Why this pick:</b> {e(reason_txt)}.</p>
<p class="small meta">{e(cat['name'])} · checked {t.get('checked', CHECKED)} · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Official pricing page</a></p></article>"""
def _seo_table(rows_tools, cat):
    rows = ""
    for i, t in enumerate(rows_tools, 1):
        en = _entry_num(t)
        rows += f"<tr><td>{i}</td><td><a href='{turl(t['name'])}'>{e(t['name'])}</a>{' <span class=\"badge b-best\">BEST VALUE</span>' if t['name']==cat['best'] else ''}</td><td>{('$'+format(en,'g')+'/mo') if en is not None else '—'}</td><td>{e(t['price'])}</td><td>{e(t['free'])}</td><td>{t.get('checked', CHECKED)}<br><a href=\"{e(t['pricing'])}\" rel=\"noopener\" target=\"_blank\">Pricing page</a></td></tr>"
    return f"<div class='tw'><table><caption class='small' style='text-align:left;padding:12px 16px'>Verified prices from official pricing pages. Confirm before buying.</caption><tr><th>#</th><th>Tool</th><th>Verified entry</th><th>All plans (as listed)</th><th>Free plan</th><th>Checked</th></tr>{rows}</table></div>"

SEO_URLS = []
for _target in SEO_FREE_ALT:
    _cats = tool_pages[_target]; _cat = _cats[0]; _tgt = find(_target)
    _alts = list(dict.fromkeys(x["name"] for cc in _cats for x in cc["tools"] if x["name"] != _target and hasfree(x, cc)))
    _alt_tools = _seo_rank([find(a) for a in _alts], _cat)
    _path = f"/free-alternative-to-{slug(_target)}.html"; SEO_URLS.append(_path)
    _best_name = _cat["best"] if any(t["name"] == _cat["best"] for t in _alt_tools) else None
    _priced = [( _entry_num(t), t) for t in _alt_tools if _entry_num(t) is not None]
    _lowest_name = min(_priced, key=lambda x: x[0])[1]["name"] if _priced else None
    _title = f"Free Alternatives to {_target} ({CHECKED[:4]}) — {len(_alt_tools)} {_cat['name']} Tools with Real Free Plans"
    _d = f"Free alternatives to {_target} in {_cat['name'].lower()}: {', '.join(t['name'] for t in _alt_tools)} — each with a verified real free plan, entry price, checked date and official pricing link."
    _cards = "".join(_seo_card(t, _cat, i+1, _best_name, _lowest_name) for i, t in enumerate(_alt_tools))
    _top3 = ",".join(slug(t["name"]) for t in _alt_tools[:3])
    _qas = [
        (f"Does {_target} have a free plan?", f"Per its official pricing page (checked {_tgt.get('checked', CHECKED)}): {_tgt['free']}. Paid entry as listed: {_tgt['price']}."),
        (f"What is the Best Value free alternative to {_target}?", f"{_cat['best']} is ToolPick's Best Value pick for {_cat['name'].lower()} and is listed first here. " + (find(_cat['best']).get('why','') if any(t['name']==_cat['best'] for t in _alt_tools) else "")),
        (f"Which free alternative to {_target} has the lowest verified entry price?", f"{_lowest_name} at ${_entry_num(find(_lowest_name)):g}/mo (lowest verified entry in our price table among these alternatives, checked {find(_lowest_name).get('checked', CHECKED)})." if _lowest_name else "None of these alternatives has a verified numeric entry price in our price table."),
    ]
    _fh, _fl = faq(_qas)
    _body = f"""<h1>Free alternatives to {e(_target)}</h1><p class="tag">Looking for a free alternative to {e(_target)}? These {_cat['name'].lower()} tools each have a verified real free plan — free trials and one-time credits do not count. Every price below was copied from the tool's official pricing page and shows its checked date.</p>
<p><a href="{turl(_target)}">{e(_target)}</a> itself: {e(_tgt['price'])}. Free: {e(_tgt['free'])} (checked {_tgt.get('checked', CHECKED)} · <a href="{e(_tgt['pricing'])}" rel="noopener" target="_blank">official pricing page</a>). The alternatives below are ranked with ToolPick's existing logic: the category Best Value pick first, then the lowest verified entry price.</p>
<h2>Ranked free alternatives</h2><div class="grid">{_cards}</div>{_seo_table(_alt_tools, _cat)}
<p><a class="btn" href="/compare-builder.html?tools={_top3}">Compare the top 3 side by side →</a></p>
<p><a href="/cost-calculator.html?category={_cat['id']}&amp;seats=1&amp;billing=monthly">What will {_cat['name'].lower()} tools really cost? →</a> See true monthly and yearly costs in the cost calculator.</p>
<p>More: <a href="/best-ai-{_cat['id']}-tools.html">best AI {_cat['name'].lower()} tools</a> · <a href="/best-free-ai-{_cat['id']}-tools.html">best free AI {_cat['name'].lower()} tools</a> · <a href="/tools.html?category={_cat['id']}&amp;free=yes">browse {_cat['name'].lower()} tools with a free plan</a> · <a href="/tools/{slug(_target)}.html">{e(_target)} pricing &amp; review</a></p>{_fh}"""
    _il = {"@context":"https://schema.org","@type":"ItemList","name":_title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(_alt_tools)]}
    page(_path, _title, _d[:300], _body, [_il, _fl, crumbs([("ToolPick","/"),(f"Best AI {_cat['name']} tools",f"/best-ai-{_cat['id']}-tools.html"),(f"Free alternatives to {_target}",_path)])])

# Video under $20: entry < $20 exactly.
_vcat = next(c for c in CATEGORIES if c["id"] == "video")
_video_tools_all = [t for t in _vcat["tools"]]
_video_under = [t for t in _video_tools_all if _entry_num(t) is not None and _entry_num(t) < 20]
_video_under_sorted = sorted(_video_under, key=lambda t: (_entry_num(t), t["name"].lower()))
_vbest = _vcat["best"] if any(t["name"] == _vcat["best"] for t in _video_under_sorted) else None
_vlowest = _video_under_sorted[0]["name"] if _video_under_sorted else None
_vtitle = f"Best AI Video Tools Under $20 ({CHECKED[:4]}) — {len(_video_under_sorted)} Tools with Verified Entry Under $20/mo"
_vd = f"{len(_video_under_sorted)} AI video tools with a verified entry price under $20/mo (lowest monthly or annual rate in our price table): {', '.join(t['name'] for t in _video_under_sorted)}. Prices, free plans, checked dates and official pricing links."
_vcards = "".join(_seo_card(t, _vcat, i+1, _vbest, _vlowest) for i, t in enumerate(_video_under_sorted))
_vtop3 = ",".join(slug(t["name"]) for t in _video_under_sorted[:3])
_vqas = [
    ("What does “under $20” mean on this page?", "It means the tool's lowest verified entry rate in ToolPick's price table — the lower of its monthly rate and its per-month rate when billed yearly — is under $20/mo (less than $20, not $20 or less). Tools at exactly $20/mo or with no verified numeric entry rate are not included."),
    (f"What is the cheapest AI video tool under $20 here?", f"{_video_under_sorted[0]['name']} at ${_entry_num(_video_under_sorted[0]):g}/mo verified entry (checked {_video_under_sorted[0].get('checked', CHECKED)}): {_video_under_sorted[0]['price']}."),
    ("What is the Best Value pick among these video tools?", f"{_vcat['best']} is ToolPick's Best Value pick for video and carries the badge on this page. " + find(_vcat['best']).get('why','')),
]
_vfh, _vfl = faq(_vqas)
_vbody = f"""<h1>Best AI video tools under $20</h1><p class="tag">Every AI video tool on ToolPick whose verified entry price is <b>under $20/mo</b> — that means less than $20, using the lowest verified monthly or annual-billing rate in our price table. Sorted cheapest first. Prices were copied from official pricing pages; each tool shows its checked date and pricing link.</p>
<p>Threshold stated plainly: a tool is included only if its verified entry rate is &lt; $20/mo. A tool listed at exactly $20/mo, or with no verified numeric entry rate (“check site”), is excluded — never guessed in. The Best Value badge follows ToolPick's existing rule: the category Best Value pick for video ({e(_vcat['best'])}) when it is on this list.</p>
<h2>Ranked cheapest first</h2><div class="grid">{_vcards}</div>{_seo_table(_video_under_sorted, _vcat)}
<p><a class="btn" href="/compare-builder.html?tools={_vtop3}">Compare the 3 cheapest side by side →</a></p>
<p><a href="/cost-calculator.html?category=video&amp;seats=1&amp;billing=monthly">What will video tools really cost? →</a> See true monthly and yearly costs by seats and billing in the cost calculator.</p>
<p>More: <a href="/best-ai-video-tools.html">best AI video tools</a> · <a href="/best-free-ai-video-tools.html">best free AI video tools</a> · <a href="/tools.html?category=video">browse all video tools in the directory</a> · <a href="/help-me-choose.html?category=video">help me choose a video tool</a></p>{_vfh}"""
_vil = {"@context":"https://schema.org","@type":"ItemList","name":_vtitle,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(_video_under_sorted)]}
page(SEO_VIDEO_PATH, _vtitle, _vd[:300], _vbody, [_vil, _vfl, crumbs([("ToolPick","/"),("Best AI video tools","/best-ai-video-tools.html"),("Best AI video tools under $20",SEO_VIDEO_PATH)])])
SEO_URLS.append(SEO_VIDEO_PATH)

# /free and best-free pages
FREE_LIST = [(c, t) for c in CATEGORIES for t in c["tools"] if hasfree(t, c)]
fcards = "".join(f'<article class="card" data-c="{c["id"]}"><div class="th">{logo(t)}<div><div class="badges"><span class="badge b-free">FREE PLAN</span></div><h3><a href="{turl(t["name"])}">{e(t["name"])}</a></h3></div></div><p>{e(t["about"])}</p><p class="small">{e(t["free"])}</p><p class="price">Paid: {e(t["price"])}</p><p class="small meta">{e(c["name"])} · checked {t.get("checked", CHECKED)}</p></article>' for c, t in FREE_LIST)
page("/free.html", f"Free AI Tools ({CHECKED[:4]}): {len({t['name'] for _,t in FREE_LIST})} Tools with a Confirmed Free Plan", "Every AI tool on ToolPick with a free plan confirmed on its official pricing page, filterable by category.",
  f"""<h1>Free AI tools</h1><p class="tag">Tools whose official pricing page showed a free plan on {CHECKED}. Free trials are not counted.</p>
<select id="fc" class="finder" style="padding:10px"><option value="">All categories</option>{''.join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)}</select>
<p>{''.join(f'<a href="/best-free-ai-{c["id"]}-tools.html">Best free {e(c["name"].lower())}</a> · ' for c in CATEGORIES)}</p><div class="grid" id="fl">{fcards}</div>
<script>document.getElementById('fc').onchange=function(){{var v=this.value;document.querySelectorAll('#fl .card').forEach(function(x){{x.style.display=!v||x.dataset.c==v?'':'none'}})}}</script>""",
  [{"@context":"https://schema.org","@type":"ItemList","name":"Free AI tools","itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,(c,t) in enumerate(FREE_LIST)]}])
for c in CATEGORIES:
    L = [t for cc, t in FREE_LIST if cc is c]
    if not L: continue
    path = f"/best-free-ai-{c['id']}-tools.html"; n = c["name"]
    title = f"Best Free AI {n} Tools ({CHECKED[:4]}) — {len(L)} with Free Plans"
    d = f"{len(L)} free AI {n.lower()} tools with a free plan confirmed on the official pricing page ({CHECKED}): {', '.join(t['name'] for t in L[:5])}."
    body = f"""<h1>Best free AI {e(n.lower())} tools</h1><p class="tag">{e(d)}</p><ol>{''.join(f"<li><h3><a href='{turl(t['name'])}'>{e(t['name'])}</a></h3><p>{e(t['about'])}</p><p>🆓 {e(t['free'])}</p><p class='price'>💲 Paid: {e(t['price'])}</p><p class='small'>checked {t.get('checked', CHECKED)}</p></li>" for t in L)}</ol>
<p>Compare paid options: <a href="/best-ai-{c['id']}-tools.html">all AI {e(n.lower())} tools</a> · <a href="/free.html">all free AI tools</a></p>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,t in enumerate(L)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),("Free AI tools","/free.html"),(f"Best free AI {n} tools",path)])])

# guides hub
page("/guides.html", "AI tool guides: best tool for every job & free alternatives", "Every ToolPick guide: best AI tool for a job, free alternatives and head-to-head comparisons.",
  "<h1>Guides</h1><h2>New guides</h2><ul><li><a href='/free-alternative-to-recraft.html'>Free alternative to Recraft</a></li><li><a href='/free-alternative-to-rytr.html'>Free alternative to Rytr</a></li><li><a href='/best-ai-video-tools-under-20.html'>Best AI video tools under $20</a></li></ul><h2>Best AI tool for…</h2><ul>" + "".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS) + "</ul><h2>Free tools</h2><ul>" + "".join(f'<li><a href="/best-free-ai-{c["id"]}-tools.html">Best free AI {e(c["name"].lower())} tools</a></li>' for c in CATEGORIES) + "</ul><h2>Free alternatives</h2><ul>" +
  "".join(f'<li><a href="{p}">Free alternative to {e(n)}</a></li>' for n,p in FREE_ALT_URLS) + "</ul>" + complinks(COMPARISONS))
# price changes log
hist = json.load(open("price_history.json")) if os.path.exists("price_history.json") else {}
dates = sorted(hist); rows = []
for a, b in zip(dates, dates[1:]):
    for n in sorted(set(hist[a]) | set(hist[b])):
        o, nw = hist[a].get(n), hist[b].get(n)
        if o == nw: continue
        what = "added" if o is None else "removed" if nw is None else "changed"
        rows.append(f"<tr><td>{b}</td><td>{e(n)}</td><td>{what}</td><td>{e((o or {}).get('price','—'))}</td><td>{e((nw or {}).get('price','—'))}</td></tr>")
def difftable(rs): return "<div class='tw'><table><tr><th>Date</th><th>Tool</th><th>Change</th><th>Before</th><th>After</th></tr>" + "".join(rs) + "</table></div>"
latest = ""
if len(dates) >= 2:
    lr = [r for r in rows if r.startswith(f"<tr><td>{dates[-1]}")]
    latest = f"<div class='pick'><h2 style='margin-top:0'>Latest check: {dates[-2]} → {dates[-1]}</h2>" + (f"<p><b>{len(lr)}</b> change(s).</p>" + difftable(lr) if lr else "<p>No price changes in the latest check.</p>") + "</div>"
elif dates:
    latest = f"<div class='pick'><h2 style='margin-top:0'>Latest check: {dates[-1]}</h2><p>Baseline snapshot of {len(hist[dates[-1]])} tools. The first weekly diff will appear here after the next re-check.</p></div>"
full = "<h2>Full history</h2>" + (difftable(list(reversed(rows))) if rows else "<p>No changes recorded yet.</p>")
page("/price-changes.html", "AI tool price changes log — weekly updates", "Weekly log of AI tool price changes, based on snapshots of official pricing pages.",
  f"<h1>AI tool price changes</h1><p class='tag'>We re-check official pricing pages weekly and log every change here. Snapshots: {len(dates)} ({', '.join(dates)}).</p>{latest}{full}")
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
ll += ["", "## New SEO guides", "- [Free alternatives to Recraft]({BASE}/free-alternative-to-recraft.html)", "- [Free alternatives to Rytr]({BASE}/free-alternative-to-rytr.html)", "- [Best AI video tools under $20]({BASE}/best-ai-video-tools-under-20.html): verified entry under $20/mo, cheapest first", "", "## Help me choose", f"- [Help me choose wizard]({BASE}/help-me-choose.html): 5-step guided shortlist, e.g. ?category=audio&budget=10&billing=monthly&seats=1&free=any&annual=any", "", "## Compare builder", f"- [Compare builder]({BASE}/compare-builder.html): pick any 2-3 tools, e.g. ?tools=elevenlabs,descript,heygen", "", "## Cost calculator", f"- [Cost calculator]({BASE}/cost-calculator.html): true monthly/yearly cost by tool or category, seats and billing period, from verified entry prices, e.g. ?tool=elevenlabs&seats=1&billing=monthly", "", "## Browse all tools", f"- [Browse all tools directory]({BASE}/tools.html): filter all tools by category, free plan, verified price, billing and seat pricing, e.g. ?category=audio&free=yes&sort=price", "", f"Data: {BASE}/tools.json"]
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
for old, new in REDIRECTS.items():
    fp = "public" + old; os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{BASE}{new}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={new}"><script>location.replace("{new}")</script></head><body><p>This page moved to <a href="{new}">{BASE}{new}</a>.</p></body></html>')
INDEXNOW_KEY = "9cee734b008a5ed647a1d3686a478337"
open(f"public/{INDEXNOW_KEY}.txt", "w").write(INDEXNOW_KEY)
open("public/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
# Honest sitemap lastmod rules (never invented, never future):
# - tool page: that tool's own checked date (per-tool `checked` or global CHECKED as stored)
# - category / best-free page: latest checked date among the tools listed on that page
# - compare page: latest checked date among the compared tools on that page
# - best-for (job) page: latest checked date among its ranked tools
# - free-alternative page: latest checked date among the tool + alternatives shown
# - /free.html: latest checked date among the free tools listed
# - /tools.html (new directory): 2026-10-19, its actual build/ship date (America/New_York)
# - every other static/feature page (home, builder, calculator, wizard, guides, price-changes,
#   sponsor, newsletter): OMIT lastmod rather than inventing a date.
_lm = {}
for _n in tool_pages: _lm[turl(_n)] = find(_n).get("checked", CHECKED)
for _c in CATEGORIES:
    _lm[f"/best-ai-{_c['id']}-tools.html"] = max(t.get("checked", CHECKED) for t in _c["tools"])
    _fl = [t for t in _c["tools"] if hasfree(t, _c)]
    if _fl: _lm[f"/best-free-ai-{_c['id']}-tools.html"] = max(t.get("checked", CHECKED) for t in _fl)
for _x in COMPARISONS: _lm[f"/compare/{_x[0]}.html"] = max(find(_n).get("checked", CHECKED) for _n in cnames(_x))
for _js, _job, _cid, _ranked in JOBS: _lm[f"/best-ai-tool-for-{_js}.html"] = max(find(_n).get("checked", CHECKED) for _n in _ranked)
for _n, _path in FREE_ALT_URLS:
    _cats = tool_pages[_n]; _alts = list(dict.fromkeys(x["name"] for cc in _cats for x in cc["tools"] if x["name"] != _n and hasfree(x, cc)))
    _lm[_path] = max(find(_a).get("checked", CHECKED) for _a in [_n] + _alts)
if FREE_LIST: _lm["/free.html"] = max(t.get("checked", CHECKED) for _c, t in FREE_LIST)
for _sp in SEO_URLS:
    if _sp == SEO_VIDEO_PATH:
        _lm[_sp] = max(t.get("checked", CHECKED) for t in _video_under_sorted) if _video_under_sorted else CHECKED
    elif _sp.startswith("/free-alternative-to-"):
        _tn = next((n for n in SEO_FREE_ALT if f"/free-alternative-to-{slug(n)}.html" == _sp), None)
        if _tn:
            _cs = tool_pages[_tn]; _as = list(dict.fromkeys(x["name"] for cc in _cs for x in cc["tools"] if x["name"] != _tn and hasfree(x, cc)))
            _lm[_sp] = max(find(_a).get("checked", CHECKED) for _a in [_tn] + _as)
_lm["/tools.html"] = "2026-10-19"
open("public/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc>" + (f"<lastmod>{_lm[u]}</lastmod>" if u in _lm else "") + "</url>" for u in URLS) + "</urlset>")
open("public/tools.json","w").write(json.dumps({"checked":CHECKED,"categories":CATEGORIES},indent=1))
print("pages:", len(URLS), "unique tools:", total_tools, {c["id"]:len(c["tools"]) for c in CATEGORIES})
