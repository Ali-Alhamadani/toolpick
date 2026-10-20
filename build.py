"""Builds public/ from tools.py.  Usage: BASE=https://your-site python3 build.py
Pages: index, /best-ai-<category>-tools.html, /tools/<slug>.html, /compare/<slug>.html, sitemap, robots, tools.json"""
import os, re, html, json, shutil
from tools import CATEGORIES, CHECKED, COMPARISONS, PRICE_TABLE, JOBS, SPONSOR_TIERS, FREE_ALT_FOR, REDIRECTS
FREE_V21 = True  # v21: set True to ship the 'Can I do it for free?' job picker at /free.html
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
#out{text-align:left}#out>h2{font-size:1.1rem;margin:var(--s5) 0 var(--s2)}.fempty{background:var(--sf);border:2px dashed var(--ac);border-radius:var(--r);padding:var(--s5);margin:var(--s4) 0;color:var(--tx);font-size:1rem;line-height:1.6}.fempty h2{font-size:1.25rem;margin:0 0 var(--s2);color:var(--tx)}.fempty p{color:var(--tx)}.fsugg{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s3)}.fsugg button{display:inline-flex;align-items:center;min-height:44px;padding:0 var(--s4);border-radius:999px;border:1px solid var(--bd);background:var(--sf2);color:var(--tx);font-size:.95rem;cursor:pointer;font-family:inherit}.fsugg button:hover{border-color:var(--ac)}
.needs{display:flex;flex-wrap:wrap;gap:var(--s2);margin:var(--s4) 0}.needs button.on{background:var(--ac);border-color:var(--ac);color:var(--sf)}.tabs section{display:none}.tabs section.on{display:block}
.finderbox,.free-filter{margin:var(--s4) 0}.free-filter select{min-height:44px;border-radius:10px;padding:0 var(--s3);background:var(--sf);color:var(--tx);border:1px solid var(--bd)}
.btn{display:inline-flex;align-items:center;min-height:44px;background:var(--ac);color:var(--sf);padding:0 var(--s5);border-radius:999px;text-decoration:none;font-weight:600}
footer.site{border-top:1px solid var(--bd);background:var(--sf);margin-top:var(--s7)}footer.site .wrap{padding-top:var(--s6);padding-bottom:var(--s6)}footer.site a{display:inline-flex;align-items:center;min-height:44px;margin-right:var(--s4)}
input,select,button{font:inherit}th{white-space:nowrap}td,th{vertical-align:middle}#out,#out>h2{scroll-margin-top:96px}.card h3 a,td a,th a,.pick a,.freealt a,.sponsor a{display:inline-flex;align-items:center;min-height:44px}
@media(max-width:640px){main{padding-top:var(--s4)}.hero{padding-top:var(--s4)}.hstick{position:sticky;top:0;z-index:15;background:var(--bg);padding:var(--s2) 0}.sbar{padding-left:var(--s4)}.sbar button{padding:0 var(--s4)}nav.top{margin-left:0;width:100%}.menu{left:0;right:auto}.card{padding:var(--s4)}}
@media(prefers-reduced-motion:no-preference){.card{transition:box-shadow .15s,transform .15s}.card:hover{transform:translateY(-1px)}}
.builder{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s5);margin:var(--s4) 0}#calc-out .tw table{min-width:640px}.cform{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--s4)}.cform label{font-weight:600;display:block}.cform select,.cform input[type=number]{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3)}.cform fieldset{border:0;padding:0;margin:0}.cform legend{font-weight:600;margin-bottom:var(--s2)}@media(max-width:760px){.cform{grid-template-columns:1fr}}.bform{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)}.bform label{font-weight:600;display:block}.bform select{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);max-width:100%}.bactions{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4);align-items:center}.bbtn{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--s5);border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-weight:600;cursor:pointer}.bbtn.primary{background:var(--ac);color:var(--sf);border-color:var(--ac)}.bstatus{min-height:1.5em}.bnote{background:var(--sf2);border-radius:10px;padding:var(--s3) var(--s4);margin:var(--s4) 0}@media(max-width:760px){.bform{grid-template-columns:1fr}.builder{padding:var(--s4)}}.dform{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)}.dform label{font-weight:600;display:block}.dform select{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);max-width:100%}@media(max-width:760px){.dform{grid-template-columns:1fr}}.tray{position:sticky;bottom:12px;z-index:10;background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s3) var(--s4);display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin:var(--s4) 0}.tray .bbtn{min-height:44px}.addbtn{margin-top:auto}.aform{display:grid;grid-template-columns:1fr auto;gap:var(--s3);align-items:end}.aform label{font-weight:600;display:block}.aform select,.aform input[type=search]{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);max-width:100%}@media(max-width:760px){.aform{grid-template-columns:1fr}}.arow{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s4);margin:var(--s3) 0}.arow .rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s3);margin-top:var(--s3)}.arow label{font-weight:600;display:block}.arow input,.arow select{width:100%;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3)}@media(max-width:760px){.arow .rgrid{grid-template-columns:1fr}}.ares{border-left:4px solid var(--ac)}.ares.save{border-left-color:var(--ok)}.atotal{background:var(--sf2);border-radius:10px;padding:var(--s3) var(--s4);margin:var(--s4) 0}.wizprog{height:10px;background:var(--sf2);border-radius:999px;overflow:hidden;margin:var(--s4) 0}.wizprog i{display:block;height:100%;background:var(--ac)}.opts{display:grid;gap:var(--s2);margin:var(--s4) 0}.opts label{display:flex;gap:var(--s3);align-items:flex-start;background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:var(--s4);cursor:pointer;min-height:44px}.opts label:hover{border-color:var(--ac)}.opts input{margin-top:4px;flex:none}.opts input:focus-visible+span{outline:3px solid var(--ac);outline-offset:2px}.wstep fieldset{border:0;padding:0;margin:0}.wstep legend{font-size:1.25rem;font-weight:700;line-height:1.3}.wnav{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4);align-items:center}
"""
CSS += ".verdict{margin:12px 0 20px}.vline{font-size:1.1rem;margin:0 0 8px}.vgrid{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:6px 14px;margin:0}.vgrid dt{color:var(--mu);font-weight:600}.vgrid dd{margin:0}@media(max-width:640px){.vgrid{grid-template-columns:1fr}.vgrid dd{margin-bottom:6px}}"

CSS += ".fpick{border-width:2px}.factions{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.factions .bbtn{text-decoration:none;display:inline-flex;align-items:center;min-height:44px}.fru{list-style:none;padding:0;margin:0;display:grid;gap:8px}.fru li{display:flex;gap:10px;align-items:flex-start;background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:10px 12px}.fmore{margin-top:10px}.fmore summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:500}"

CSS += ".mnav{display:none}nav.top{flex-wrap:nowrap}nav.top>a,nav.top summary{white-space:nowrap}.hstick{position:static!important}@media(max-width:760px){nav.top .dn{display:none}.mnav{display:block;margin-left:auto}nav.top{width:auto!important;margin-left:auto!important}.mnav .menu{right:0;left:auto!important;max-height:75vh;overflow:auto}}.pcba{display:grid;gap:8px;margin:8px 0}.pcba div{background:var(--sf2);border-radius:10px;padding:10px 12px;font-size:1rem;line-height:1.5;color:var(--tx)}.pcba b{display:block;font-size:.85rem;color:var(--mu);text-transform:uppercase;letter-spacing:.02em}"

FOOT = f"""<footer class="site small"><div class="wrap"><p><a href="/sponsor.html">Sponsor ToolPick</a> · <a href="/newsletter.html">Newsletter</a> · <a href="/llms.txt">llms.txt</a></p>Some links may become affiliate links in future; that never changes our picks. Prices copied from each tool's official pricing page; every tool shows its own checked date and pricing link (USD unless shown; yearly-billing prices in parentheses). "check site" = we could not verify the price, so we don't guess. Prices change — always confirm on the official page.</div></footer>"""
def page(path, title, desc, body, ld=None):
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    full = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>{lds}<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script><script defer src="/_vercel/insights/script.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site"><div class="wrap"><a class="brand" href="/"><i aria-hidden="true">T</i>ToolPick</a><nav class="top" aria-label="Main"><details class="dn"><summary>Find a tool</summary><div class="menu"><a href="/">Search by need</a><a href="/tools.html">Browse all tools</a><a href="/help-me-choose.html">Help me choose</a><a href="/stacks.html">Starter stacks</a><hr style="border:0;border-top:1px solid var(--bd);margin:4px 0">{''.join(f'<a href="/best-ai-{c["id"]}-tools.html">{e(c["name"])}</a>' for c in CATEGORIES)}</div></details><a class="dn" href="/compare-builder.html">Compare</a><a class="dn" href="/free.html">Free tools</a><details class="dn"><summary>Save money</summary><div class="menu"><a href="/save-money.html">Save money hub</a><a href="/pay-less.html">Pay less for a tool</a><a href="/monthly-or-yearly.html">Monthly or yearly?</a><a href="/free.html">Can I do it for free?</a><a href="/price-changes.html">Price changes</a><a href="/subscription-audit.html">Subscription Audit</a></div></details><a class="dn" href="/guides.html">Guides</a><details class="mnav"><summary>Menu</summary><div class="menu"><a href="/">Search by need</a><a href="/tools.html">Browse all tools</a><a href="/help-me-choose.html">Help me choose</a><a href="/stacks.html">Starter stacks</a><a href="/compare-builder.html">Compare</a><a href="/free.html">Free tools</a><a href="/save-money.html">Save money hub</a><a href="/pay-less.html">Pay less for a tool</a><a href="/monthly-or-yearly.html">Monthly or yearly?</a><a href="/free.html">Can I do it for free?</a><a href="/price-changes.html">Price changes</a><a href="/subscription-audit.html">Subscription Audit</a><a href="/guides.html">Guides</a></div></details></nav></div></header>
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
def _num(v): return v if isinstance(v, (int, float)) else None
import tools as _tm0
CAPS = _tm0.CAPS; CAP_LABEL = _tm0.CAP_LABEL
def cap1(n): return CAPS[n][0]
def cap_label(n): return CAP_LABEL.get(cap1(n), cap1(n))
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
<div class="freealt"><span class="badge b-free">FREE PLANS IN THIS CATEGORY</span>{', '.join(f'<a href="{turl(n)}">{e(n)}</a> <span class="small">({e(cap_label(n))})</span>' for n in c['free'])}{(lambda f: f' · <b>Free alternative to {e(b["name"])} that does the same main job ({e(cap_label(b["name"]))}):</b> <a href="{turl(f["name"])}">{e(f["name"])}</a>' if f else f' · No free alternative to {e(b["name"])} that does the same main job ({e(cap_label(b["name"]))}) in our list' + ('' if realfree(b) else '') )(free_alt(b["name"]))}</div>"""
def comps_for(names): return [x for x in COMPARISONS if set(x[2] if isinstance(x[2], list) else [x[2], x[3]]) & set(names)]
def complinks(lst): return ("<h2>Comparisons</h2><ul>" + "".join(f'<li><a href="/compare/{s}.html">{e(ti)}</a></li>' for s,ti,*_ in lst) + "</ul>") if lst else ""
total_tools = len(tool_pages)

# --- v16: AI starter stacks by role (hub /stacks.html + one page per role) ---
# Only verified tools.py data. Rules (stated on page):
#  rate = per-month price billed yearly when PRICE_TABLE has a numeric annual rate, else numeric monthly rate.
#  Tools whose price text is "check site" or whose rate is non-USD/non-numeric never enter a priced stack.
#  Free = realfree() only ($0). Under $30 = cheapest verified entry per job, total strictly < $30/mo.
#  Pro = the category's Best Value pick at its verified entry rate (PRICE_TABLE holds entry tiers only,
#  so no higher tier is ever invented); if that pick is unpriced, the highest verified entry rate in the category.
STACK_LIMIT = 30
STACK_BUILD_DATE = "2026-10-20"
ROLES = [
 ("students","student","Students",["writing","research","presentations","productivity"],"write essays, research sources, build class slides and stay organised"),
 ("marketers","marketer","Marketers",["writing","images","video","marketing"],"write copy, make images and short videos, and schedule or optimise content"),
 ("developers","developer","Developers",["coding","assistants","productivity","agents"],"write code, ask an assistant, run meetings and tasks, and automate workflows"),
 ("content-creators","content creator","Content creators & YouTubers",["video","audio","images","writing"],"edit videos, record and clean audio, design thumbnails and write scripts"),
 ("small-business","small business or online seller","Small businesses & online sellers",["marketing","images","agents","productivity"],"post on social, make product images, answer customers and keep work on track"),
 ("researchers","researcher","Researchers",["research","writing","productivity","assistants"],"find and read papers, write up results, take meeting notes and ask an assistant"),
]
BUDGETS = [("free","Free","$0 — only tools with a verified real free plan (no trials, no one-time credits)"),
           ("under30","Under $30/mo",f"cheapest monthly price per job (tools that do the same main job only), total strictly under ${STACK_LIMIT}/mo"),
           ("pro","Pro","each category's Best Value pick at its verified entry plan")]
_CATBY = {c["id"]: c for c in CATEGORIES}
def st_rate(t):
    # v26: one billing rule for every stack — the monthly price when checked, else the billed-yearly per-month price (labelled).
    if t["price"] == "check site": return None
    a, m = t.get("monthly"), t.get("annual")
    if isinstance(a, (int, float)): return (a, "monthly")
    if isinstance(m, (int, float)): return (m, "annual")
    return None
def st_money(v): return f"${v:,.2f}".replace(".00", "")
# v26: each stack slot is ONE main job (capability). Default = the main job of the category's Best Value pick;
# ROLE_SLOT_CAP overrides it where the role's stated need names a different job (e.g. creators "record and clean audio").
ROLE_SLOT_CAP = {("content-creators", "audio"): "edit-by-transcript", ("students", "productivity"): "meeting-notes", ("developers", "productivity"): "meeting-notes", ("researchers", "writing"): "writing-assistant"}
def slot_cap(rs, cid): return ROLE_SLOT_CAP.get((rs, cid)) or CAPS[_CATBY[cid]["best"]][0]
def st_pick(role_cats, budget, rs=None):
    used, out = set(), []
    total = 0.0
    for cid in role_cats:
        c = _CATBY[cid]; cap = slot_cap(rs, cid)
        pool = [t for t in c["tools"] if CAPS[t["name"]][0] == cap]
        if budget == "free":
            cands = [t for t in sorted(pool, key=lambda t: (t["name"] not in c["free"], c["tools"].index(t))) if realfree(t)]
            alts = cands
        else:
            # like-for-like: rank on monthly prices only (a tool with no monthly price is never called cheaper than a monthly one)
            cands = [t for t in pool if st_rate(t)]
            alts = sorted(cands, key=lambda t: (st_rate(t)[1] != "monthly", st_rate(t)[0], t["name"]))
            if budget == "under30": cands = [t for t in alts if st_rate(t)[1] == "monthly"]
            else:
                b = next((t for t in pool if t["name"] == c["best"] and st_rate(t)), None)
                cands = ([b] if b else []) + sorted(cands, key=lambda t: (st_rate(t)[1] != "monthly", -st_rate(t)[0]))
        ch = None
        for t in cands:
            if t["name"] in used: continue
            if budget == "under30" and total + st_rate(t)[0] >= STACK_LIMIT: continue
            ch = t; break
        if not ch: continue
        used.add(ch["name"]); total += st_rate(ch)[0] if budget != "free" else 0
        out.append((c, ch, alts))
    return out
def st_reason(t, c, budget):
    job = cap_label(t["name"])
    if budget == "free": return f"Main job: {job}. Verified free plan: {t['free']}."
    r, b = st_rate(t)
    s = f"Main job: {job}. Entry plan {st_money(r)}/mo {'billed yearly' if b == 'annual' else 'billed monthly'}"
    if budget == "under30":
        same = [x for x in c["tools"] if x is not t and CAPS[x["name"]][0] == CAPS[t["name"]][0] and _num(x.get("monthly")) is not None]
        if same and not [x for x in same if x["monthly"] < r]: s += f" — the cheapest monthly price we checked for {job} in {c['name']}"
    elif t["name"] == c["best"]: s += f" — ToolPick's Best Value pick in {c['name']}"
    else: s += f" — the {c['name']} Best Value pick doesn't do this job or has no verified price, so this is the highest verified entry plan for {job}"
    if t.get("per_output"): s += f" ({t['per_output']})"
    return s + "."
ROLE_DATA = {}
for _rs, _rn, _rt, _rc, _rj in ROLES:
    ROLE_DATA[_rs] = {b: st_pick(_rc, b, _rs) for b, *_ in BUDGETS}
def st_total(lst, budget): return 0.0 if budget == "free" else round(sum(st_rate(t)[0] for c, t, a in lst), 2)
def role_path(rs): return f"/best-ai-tools-for-{rs}.html"
STACK_URLS = ["/stacks.html"] + [role_path(r[0]) for r in ROLES]
_ST_CSS = "<style>.stabs{display:flex;flex-wrap:wrap;gap:var(--s2);margin:var(--s4) 0}.stabs button{min-height:44px;padding:0 var(--s4);border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-weight:600;cursor:pointer}.stabs button[aria-pressed=true]{background:var(--ac);color:var(--sf);border-color:var(--ac)}.spick{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s4);margin:var(--s3) 0}.spick h3{margin:.2em 0}.spick label{font-weight:600;display:block;margin-top:var(--s3)}.spick select{width:100%;max-width:420px;min-height:48px;margin-top:var(--s2);border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3)}.stot{background:var(--sf2);border-radius:10px;padding:var(--s3) var(--s4);margin:var(--s4) 0;font-size:1.1rem}.swarn{border-left:4px solid var(--warn);padding:var(--s3) var(--s4);background:var(--sf2);border-radius:10px;margin:var(--s3) 0}.sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:var(--s4)}</style>"
def st_tooljs(t, c, budget):
    r = st_rate(t) if budget != "free" else None
    return dict(n=t["name"], s=slug(t["name"]), u=turl(t["name"]), r=(r[0] if r else 0), b=(r[1] if r else "free"), k=t.get("checked", CHECKED), pr=t["pricing"], why=st_reason(t, c, budget))
def st_static(lst, budget):
    rows = "".join(f"<li><b>{e(c['name'])}:</b> <a href='{turl(t['name'])}'>{e(t['name'])}</a> — {e(st_reason(t, c, budget))} <span class='small'>checked {t.get('checked', CHECKED)}</span></li>" for c, t, a in lst)
    tot = st_total(lst, budget)
    return f"<ul>{rows}</ul><p><b>Total: {st_money(tot)}/mo · {st_money(round(tot*12,2))}/yr</b></p>"
for _rs, _rn, _rt, _rc, _rj in ROLES:
    path = role_path(_rs); D = ROLE_DATA[_rs]
    data = {}
    for b, bl, bd in BUDGETS:
        data[b] = [dict(job=c["id"], jn=c["name"], pick=slug(t["name"]), alts=[st_tooljs(x, c, b) for x in a]) for c, t, a in D[b]]
    missing = {b: [cid for cid in _rc if cid not in [c["id"] for c, t, a in D[b]]] for b, *_ in BUDGETS}
    tots = {b: st_total(D[b], b) for b, *_ in BUDGETS}
    names = lambda b: ", ".join(t["name"] for c, t, a in D[b])
    title = f"Best AI Tools for {_rt} ({CHECKED[:4]}): Free, Under $30 & Pro Starter Stacks"
    desc = f"AI starter stacks for {_rt.lower()}: a free stack ({names('free')}), an under-$30 stack at {st_money(tots['under30'])}/mo and a pro stack at {st_money(tots['pro'])}/mo, from verified prices."[:300]
    qas = [(f"What is the best free AI stack for {_rt.lower()}?", f"{names('free')} — every pick has a verified real free plan on its official pricing page, so the stack costs $0."),
           (f"How much does the under-$30 AI stack for {_rt.lower()} cost?", f"{st_money(tots['under30'])}/mo ({st_money(round(tots['under30']*12,2))}/yr) for {names('under30')}, using each tool's checked monthly price (monthly billing, so the tools are compared like for like)."),
           (f"Which tools are in the pro AI stack for {_rt.lower()}?", f"{names('pro')}, totalling {st_money(tots['pro'])}/mo ({st_money(round(tots['pro']*12,2))}/yr) at verified entry plans."),
           ("Where do these prices come from?", f"Each price was copied from the tool's official pricing page (checked dates shown per pick, latest {max(t.get('checked', CHECKED) for b in D for c,t,a in D[b])}). Tools marked 'check site' are never counted in a total.")]
    tabs = "".join(f'<button type="button" data-b="{b}" aria-pressed="{"true" if b=="free" else "false"}">{e(bl)}</button>' for b, bl, bd in BUDGETS)
    statics = "".join(f"<h3>{e(bl)} stack</h3><p class='small'>{e(bd)}.{(' Left out (no tool for that job fits on verified monthly prices): ' + ', '.join(_CATBY[m]['name'] for m in missing[b])) if missing[b] else ''}</p>{st_static(D[b], b)}" for b, bl, bd in BUDGETS)
    other = "".join(f'<li><a href="{role_path(r[0])}">AI tools for {e(r[2].lower())}</a></li>' for r in ROLES if r[0] != _rs)
    catlinks = " · ".join(f'<a href="/best-ai-{cid}-tools.html">AI {e(_CATBY[cid]["name"].lower())} tools</a>' for cid in _rc)
    body = f"""{_ST_CSS}<p class="small"><a href="/stacks.html">All starter stacks</a> › {e(_rt)}</p><h1>Best AI tools for {e(_rt.lower())}</h1><p class="tag">Starter stacks to {e(_rj)}. Pick a budget, swap any tool for another that does the same main job, and the total updates. Prices only from official pricing pages.</p>
<h2>Your stack</h2><div class="builder"><div class="stabs" role="group" aria-label="Budget">{tabs}</div><p class="small" id="sDesc"></p><div id="sPicks"></div><div class="stot" id="sTotal" aria-live="polite" aria-atomic="true"></div>
<div class="bactions"><button type="button" class="bbtn primary" id="sCopy">Copy share link</button><button type="button" class="bbtn" id="sReset">Reset swaps</button><span class="small bstatus" id="sStatus" role="status"></span></div></div>
<noscript>{statics}</noscript><h2>All three stacks at a glance</h2><div id="sStatic">{statics}</div>
<p class="small">How totals work: each slot is one main job (for example text to speech or meeting notes), and tools are only swapped or ranked against others that do that same job. We use the monthly price when it is checked, otherwise the billed-yearly per-month price (labelled on each tool); 1 person; prices in USD. "Under $30" means the total is strictly below ${STACK_LIMIT}/mo. Pro uses each category's Best Value pick at its verified entry plan — we only list tiers we've verified, so no higher tier is assumed. Prices change; confirm on the official pricing page.</p>
<h2>FAQ</h2>{''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in qas)}
<h2>Related</h2><p>{catlinks} · <a href="/tools.html">Browse all tools</a> · <a href="/subscription-audit.html">Audit what you already pay for</a></p><h2>Stacks for other roles</h2><ul>{other}</ul>
<script>const SD={json.dumps(data)},BUD={json.dumps({b:[bl,bd] for b,bl,bd in BUDGETS})},LIM={STACK_LIMIT},PATH={json.dumps(path)};
const X=v=>String(v).replace(/[&<>"]/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[ch]));const M=v=>'$'+(Math.round(v*100)/100).toFixed(2).replace(/\\.00$/,'');
let bud='free',sw={{}};function readURL(){{const p=new URLSearchParams(location.search);const b=p.get('budget');if(BUD[b])bud=b;sw={{}};(p.get('swap')||'').split(',').forEach(x=>{{const[j,s]=x.split(':');const row=(SD[bud]||[]).find(r=>r.job==j);if(row&&row.alts.some(a=>a.s==s))sw[j]=s}})}}
function cur(row){{const s=sw[row.job]||row.pick;return row.alts.find(a=>a.s==s)}}
function sharePath(){{const q=new URLSearchParams();q.set('role',{json.dumps(_rs)});q.set('budget',bud);const s=Object.entries(sw).filter(([j,v])=>{{const r=SD[bud].find(x=>x.job==j);return r&&r.pick!=v}}).map(([j,v])=>j+':'+v).join(',');if(s)q.set('swap',s);return PATH+'?'+q.toString().replace(/%3A/g,':').replace(/%2C/g,',')}}
function render(push){{document.querySelectorAll('.stabs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.b==bud?'true':'false'));document.getElementById('sDesc').textContent=BUD[bud][0]+': '+BUD[bud][1]+'.';
const rows=SD[bud];let tot=0;document.getElementById('sPicks').innerHTML=rows.map(r=>{{const t=cur(r);tot+=t.r;const others=r.alts.filter(a=>a.s!=t.s).slice(0,2).map(a=>a.s);const opts=r.alts.map(a=>`<option value="${{a.s}}"${{a.s==t.s?' selected':''}}>${{X(a.n)}} — ${{a.b=='free'?'$0 free plan':M(a.r)+'/mo '+(a.b=='annual'?'yearly':'monthly')}}</option>`).join('');
return `<article class="spick"><p class="small" style="margin:0">${{X(r.jn)}}</p><h3><a href="${{t.u}}">${{X(t.n)}}</a> <span class="badge ${{t.b=='free'?'b-free':'b-rank'}}">${{t.b=='free'?'$0':M(t.r)+'/mo'}}</span></h3><p class="small">${{X(t.why)}} Checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing</a></p><label for="sw-${{r.job}}">Swap ${{X(r.jn)}} tool</label><select id="sw-${{r.job}}" data-job="${{r.job}}">${{opts}}</select><p class="small"><a href="${{t.u}}">Tool page</a> · ${{others.length?`<a href="/compare-builder.html?tools=${{[t.s].concat(others).join(',')}}">Compare with alternatives</a> · `:''}}<a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=${{t.b=='monthly'?'monthly':'annual'}}">Cost calculator</a></p></article>`}}).join('')||'<p>No verified tools fit this budget.</p>';
tot=Math.round(tot*100)/100;const over=bud=='under30'&&tot>=LIM;const anyA=rows.some(r=>cur(r).b=='annual'),anyM=rows.some(r=>cur(r).b=='monthly');
document.getElementById('sTotal').innerHTML=`<b>Total: ${{M(tot)}}/mo · ${{M(tot*12)}}/yr</b> <span class="small">for ${{rows.length}} tool${{rows.length==1?'':'s'}}, 1 person${{bud=='free'?'':' · '+(anyA&&anyM?'mix of yearly and monthly billing (shown per tool)':anyA?'billed yearly':'billed monthly')}}</span>`+(over?`<div class="swarn" role="alert"><b>Over budget:</b> these swaps total ${{M(tot)}}/mo, which is not under $${{LIM}}. Swap a pick back or choose the Pro stack.</div>`:'');
document.querySelectorAll('#sPicks select').forEach(s=>s.addEventListener('change',ev=>{{sw[s.dataset.job]=s.value;render(true);document.getElementById('sw-'+s.dataset.job).focus()}}));
if(push)history.replaceState(null,'',sharePath())}}
document.querySelectorAll('.stabs button').forEach(b=>b.addEventListener('click',()=>{{bud=b.dataset.b;sw={{}};render(true)}}));
document.getElementById('sReset').addEventListener('click',()=>{{sw={{}};render(true);document.getElementById('sStatus').textContent='Swaps reset.'}});
document.getElementById('sCopy').addEventListener('click',async()=>{{const url=location.origin+sharePath();const st=document.getElementById('sStatus');try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url}}}});
readURL();render(false);</script>"""
    allt = [t for b in D for c, t, a in D[b]]
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(n),"name":n} for i, n in enumerate(dict.fromkeys(t["name"] for t in allt))]}
    fl = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in qas]}
    page(path, title, desc, body, [il, crumbs([("ToolPick","/"),("AI starter stacks","/stacks.html"),(f"AI tools for {_rt.lower()}",path)]), fl])
# hub
_cards = "".join(f'<article class="card"><h3><a href="{role_path(rs)}">AI tools for {e(rt.lower())}</a></h3><p>{e(rj[0].upper()+rj[1:])}.</p>' + "".join(f"<p class='small'><b>{e(bl)}:</b> {st_money(st_total(ROLE_DATA[rs][b], b))}/mo — {e(', '.join(t['name'] for c,t,a in ROLE_DATA[rs][b]))}</p>" for b, bl, bd in BUDGETS) + f'<p><a href="{role_path(rs)}">Open the {e(rt.lower())} stack →</a></p></article>' for rs, rn, rt, rc, rj in ROLES)
_hq = [("What is an AI starter stack?", "A small set of AI tools, one per job a role usually needs (for example writing, images, video and marketing for a marketer), with a total monthly and yearly cost from verified prices."),
       ("How are the three budgets built?", f"Free uses only tools with a verified real free plan. Under $30 picks the cheapest checked monthly price among tools that do that slot's main job while keeping the total strictly under ${STACK_LIMIT}/mo. Pro uses each category's Best Value pick at its verified entry plan.")]
_hub = f"""{_ST_CSS}<section class="hero"><h1>AI starter stacks by role</h1><p class="tag">Ready-made AI tool stacks for {len(ROLES)} roles, each at three budgets — Free, Under $30/mo and Pro — with totals from verified prices. Open a role to swap any pick and share your stack.</p></section><h2>Choose a role</h2><div class="sgrid">{_cards}</div>
<p class="small">Totals are per person per month (monthly prices where checked; any billed-yearly-only price is labelled). Tools without a verified price are never counted. Prices change — confirm on each official pricing page.</p><h2>FAQ</h2>{''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q,a in _hq)}<p><a href="/tools.html">Browse all tools</a> · <a href="/help-me-choose.html">Help me choose</a> · <a href="/cost-calculator.html">Cost calculator</a></p>
<script>(function(){{const r=new URLSearchParams(location.search).get('role');const ok={json.dumps([r[0] for r in ROLES])};if(ok.includes(r))location.replace('/best-ai-tools-for-'+r+'.html'+location.search)}})()</script>"""
page("/stacks.html", "AI Starter Stacks by Role: Free, Under $30 & Pro Tool Bundles | ToolPick", f"AI tool starter stacks for students, marketers, developers, creators, small businesses and researchers — Free, Under $30/mo and Pro, with verified monthly and yearly totals.", _hub,
     [{"@context":"https://schema.org","@type":"ItemList","name":"AI starter stacks by role","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+role_path(r[0]),"name":f"AI tools for {r[2].lower()}"} for i, r in enumerate(ROLES)]}, crumbs([("ToolPick","/"),("AI starter stacks","/stacks.html")]),
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in _hq]}])
# v13 SEO pages (preview): free alternatives that do not already exist + video under $20.
# 'free alternative to Cursor' already exists at /free-alternative-to-cursor.html, so it is not rebuilt.
SEO_FREE_ALT = ["Recraft", "Rytr"]
SEO_VIDEO_PATH = "/best-ai-video-tools-under-20.html"
def _num(v): return v if isinstance(v, (int, float)) else None
def _usd(v): r = round(v, 2); return "$" + (f"{int(r):,}" if r == int(r) else f"{r:,.2f}")
# --- v24-fix: ONE same-job rule + ONE free-alternative function, used by tool pages, pay-less, /free.html and search ---
# Same job = both tools have the same PRIMARY capability (first CAPS tag). Broad categories or secondary tags are not enough.
import tools as _tm
CAPS = _tm.CAPS; CAP_LABEL = _tm.CAP_LABEL; LOWER_TIER = _tm.LOWER_TIER; PLANS_SHORT = _tm.PLANS_SHORT
TOOL = {}
for _c in CATEGORIES:
    for _t in _c["tools"]: TOOL.setdefault(_t["name"], _t)
BEST_OF = {}
for _c in CATEGORIES: BEST_OF.setdefault(_c["best"], []).append(_c["id"])
def cap1(n): return CAPS[n][0]
def cap_label(n): return CAP_LABEL.get(cap1(n), cap1(n))
def samejob(n):
    t = TOOL[n]; c = cap1(n)
    return [x for k, x in TOOL.items() if k != n and dom(x["url"]) != dom(t["url"]) and CAPS[k][0] == c]
def cheaper_alt(n, key):
    L = sorted([x for x in samejob(n) if _num(x[key]) is not None], key=lambda x: (x[key], x["name"].lower()))
    return L[0] if L else None
def free_alt(n):
    """Shared free alternative: a real-free tool sharing n's primary capability.
    Order: a ToolPick Best Value pick first, then same PRIMARY capability, then lowest checked price, then name."""
    L = [x for x in samejob(n) if realfree(x)]
    if not L: return None
    def k(x):
        p = [v for v in (_num(x["monthly"]), _num(x["annual"])) if v is not None]
        return (0 if x["name"] in BEST_OF else 1, 0 if cap1(x["name"]) == cap1(n) else 1, min(p) if p else 1e9, x["name"].lower())
    return sorted(L, key=k)[0]
def tier_note(a, b):
    """'different tier' note when exactly one side's entry plan is a lower tier (LOWER_TIER in tools.py)."""
    return "Different tier: compare features before switching." if (a in LOWER_TIER) != (b in LOWER_TIER) else ""
NO_LIKE = "No like-for-like cheaper option checked"
def _likefields(m):
    for _v in m.values():
        _f = free_alt(_v["n"]); _v.update(cap=cap1(_v["n"]), cl=cap_label(_v["n"]), al=[slug(x["name"]) for x in samejob(_v["n"])], fa=slug(_f["name"]) if _f else None,
            mm=_num(TOOL[_v["n"]]["monthly"]), ma=_num(TOOL[_v["n"]]["annual"]), lt=LOWER_TIER.get(_v["n"]))
def _entry_num(t):
    vals = [v for v in (t.get("monthly"), t.get("annual")) if isinstance(v, (int, float))]
    return min(vals) if vals else None
# index
FDATA = json.dumps([dict(n=t["name"],c=c["id"],cn=c["name"],u=turl(t["name"]),p=t["price"],f=t["free"],k=t.get("checked",CHECKED),d=t["about"],dm=dom(t["url"]),a=t["about"]+" "+c["need"],
    m=min([v for v in (t["monthly"],t["annual"]) if isinstance(v,(int,float))],default=None),b=t["name"]==c["best"],fr=realfree(t),sl=slug(t["name"]),pr=t["pricing"],mm=t["monthly"] if isinstance(t["monthly"],(int,float)) else None,ma=t["annual"] if isinstance(t["annual"],(int,float)) else None,
    cap=cap1(t["name"]),caps=CAPS[t["name"]],fa=(lambda f: dict(n=f["name"],u=turl(f["name"]),f=f["free"]) if f else None)(free_alt(t["name"]))) for c in CATEGORIES for t in c["tools"]])
# Query -> capability mapping for the search (first matching rule wins; "all" = every stem must appear, "any" = at least one).
QCAP = [
 ("video-clipping", [], ["short clip", "into clips", "shorts", "viral clip", "clip"]),
 ("edit-by-transcript", ["edit"], ["transcri", "podcast", "by text", "text-based"]),
 ("meeting-notes", [], ["meeting", "note taker", "notetaker", "call notes"]),
 ("text-to-speech", [], ["text to speech", "text-to-speech", "voiceover", "voice over", "tts", "read aloud", "narrat", "voice generator"]),
 ("transcription", [], ["transcri"]),
 ("podcast-recording", ["record"], ["podcast", "interview"]),
 ("logo-design", [], ["logo"]),
 ("website-builder", [], ["website", "web site", "landing page"]),
 ("app-builder", ["build"], ["app"]),
 ("code-assistant", [], ["code", "coding", "programm", "debug", "developer"]),
 ("music-generation", [], ["music", "song"]),
 ("avatar-video", [], ["avatar", "presenter"]),
 ("presentations", [], ["slide", "deck", "presentation"]),
 ("photo-editing", [], ["product photo", "background remov", "photo edit", "edit photo"]),
 ("image-generation", [], ["image", "picture", "illustrat", "artwork", "poster"]),
 ("writing-assistant", [], ["grammar", "rewrite", "paraphras", "proofread"]),
 ("support-chatbot", [], ["support bot", "customer support", "support chatbot", "chatbot for my"]),
 ("paper-search", [], ["research paper", "papers", "literature", "peer-reviewed"]),
 ("social-scheduling", [], ["schedule post", "social media post", "social posts"]),
 ("seo-content", [], ["seo"]),
 ("video-editing", [], ["edit video", "edit a video", "video edit", "edit my video"]),
 ("video-generation", [], ["text to video", "generate video", "make a video", "ai video"]),
 ("workflow-automation", [], ["automate", "workflow", "automation"]),
]
FOPTS = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)
FINDER = ('''<div class="finder" role="search"><form class="hstick" id="ff" onsubmit="event.preventDefault();run();document.getElementById('out').scrollIntoView({behavior:'smooth'})"><label for="q" class="skip">Describe what you need</label><div class="sbar"><input type="search" id="q" autocomplete="off" placeholder="What do you need help with?"><button type="submit">Find</button></div></form>
<div class="chips" aria-label="Example searches"><button type="button" class="chip" data-q="turn my podcast into short clips">turn my podcast into short clips</button><button type="button" class="chip" data-q="cheap voiceover">cheap voiceover</button><button type="button" class="chip" data-q="pitch deck for investors">pitch deck for investors</button><button type="button" class="chip" data-q="AI coding assistant">AI coding assistant</button><button type="button" class="chip" data-q="meeting notes">meeting notes</button><button type="button" class="chip" data-q="logo with text">logo with text</button><button type="button" class="chip" data-q="research papers">research papers</button></div>
<div class="filters"><fieldset class="seg"><legend>Price</legend><input type="radio" name="pf" id="pf-all" value="all" checked><label for="pf-all">All</label><input type="radio" name="pf" id="pf-free" value="free"><label for="pf-free">Free plan</label><input type="radio" name="pf" id="pf-paid" value="paid"><label for="pf-paid">Paid</label></fieldset>
<label class="skip" for="cat">Category</label><select id="cat"><option value="">All categories</option>''' + FOPTS + '''</select>
<label class="skip" for="budget">Budget</label><select id="budget"><option value="any">Any budget</option><option value="0">Free only</option><option value="15">Up to $15/mo</option><option value="30">Up to $30/mo</option><option value="100">Up to $100/mo</option></select>
<label class="skip" for="skill">Experience</label><select id="skill"><option value="beginner">Beginner</option><option value="pro">Pro / power user</option></select></div><div id="out" aria-live="polite"></div></div>
<script>const D=''' + FDATA.replace("</", "<\\/") + r''';
const SW=new Set('the and for with into turn make want need some best good cheap free tool tools that this from your using use help a an my me i to'.split(' '));const hasFree=t=>t.fr;
const INT={writing:'write writing writer emails email mail essay essays blog text copy copywriting grammar rewrite letter letters draft editing editor'.split(' '),coding:'code coding programmer programming developer develop app apps debug software website build builder'.split(' '),images:'logo logos image images design designer illustration illustrations poster posters photo photos picture pictures art generate generation brand vector'.split(' '),audio:'podcast podcasts audio voiceover voice voices music song songs sound transcribe transcription transcript recording'.split(' '),video:'video videos clip clips film movie movies youtube shorts avatar explainer'.split(' '),presentations:'pitch deck slides slide presentation presentations startup decks'.split(' '),productivity:'meeting meetings notes note tasks task calendar schedule organise organize productivity transcribe transcription transcript emails email'.split(' '),research:'research papers paper study studies summarise summarize literature academic sources articles citations'.split(' '),marketing:'marketing seo social campaign advertising ads content posts post'.split(' '),assistants:'chat assistant ask question questions answer answers'.split(' '),agents:'chatbot chatbots agent agents bot bots automate automation workflow workflows'.split(' ')};
const SYN={logo:['logo','brand','vector','design','text','image'],logos:['logo','brand','vector','design','text','image'],podcast:['podcast','audio','transcript','editing','recording'],voiceover:['voice','speech'],transcribe:['transcription','transcript','notes'],meetings:['meeting','transcription','notes']};
const QC=''' + json.dumps(QCAP) + r''';const CL=''' + json.dumps(CAP_LABEL) + r''';function qcapOf(raw){const r=' '+raw.toLowerCase()+' ';for(const [cap,all,any] of QC){if(all.every(w=>r.includes(w))&&(!any.length||any.some(w=>r.includes(w))))return cap}return null}
const stem=w=>w.length>4?w.slice(0,5):w;const hit=(h,w)=>h.includes(w)||h.includes(stem(w));
function intentCats(q){const sc={};Object.keys(INT).forEach(c=>{let n=0;q.forEach(w=>{if(INT[c].some(k=>k==w||stem(k)==stem(w)))n++});if(n)sc[c]=n});const mx=Math.max(0,...Object.values(sc));return Object.keys(sc).filter(c=>sc[c]==mx&&mx>0)}
const CATS=[...new Map(D.map(t=>[t.c,t.cn])).entries()];
function suggHTML(){return `<div class="fsugg" role="group" aria-label="Suggested categories">${CATS.map(([id,n])=>`<button type="button" data-cat="${id}">${n}</button>`).join('')}</div>`}
function exHTML(){return `<div class="fsugg" role="group" aria-label="Example searches">${['write emails faster','design a logo','edit podcast audio','transcribe meetings','help me code'].map(x=>`<button type="button" data-ex="${x}">${x}</button>`).join('')}</div>`}
function emptyState(raw){const out=document.getElementById('out');if(!raw){out.innerHTML=`<div class="fempty" role="status"><h2>Describe what you need</h2><p>Tell us the job you want done - for example, writing emails, making a logo, or editing a podcast - and we will match tools from the right category. Use plain words; you do not need a tool name.</p>${exHTML()}<p style="margin-top:12px">Or browse by category:</p>${suggHTML()}</div>`}else{out.innerHTML=`<div class="fempty" role="status"><h2>No match for "${raw}"</h2><p>We could not match those words to a job our tools do. Try describing the job in plain words - what you want to make, write, record or organise - or pick a category below.</p>${exHTML()}<p style="margin-top:12px">Browse by category:</p>${suggHTML()}</div>`}}
function run(){{const bw=document.getElementById('browse');if(bw)bw.hidden=!!(document.getElementById('q').value.trim()||document.getElementById('cat').value)}const raw=document.getElementById('q').value.trim(),q=raw.toLowerCase().split(/\W+/).filter(w=>w.length>2&&!SW.has(w)),c=document.getElementById('cat').value,bu=document.getElementById('budget').value,sk=document.getElementById('skill').value,out=document.getElementById('out');
if(!raw&&!c){emptyState('');return}
const qcap=c?null:qcapOf(raw);const ic=c||qcap?[]:intentCats(q),primary=ic[0]||null;
let L=D.filter(t=>!c||t.c==c).map(t=>{const h=(t.n+' '+t.a+' '+t.cn).toLowerCase(),own=(t.n+' '+t.d).toLowerCase();let ms=0,ownHits=0;q.forEach(w=>{if(hit(h,w))ms++;if(hit(own,w))ownHits++;(SYN[w]||[]).forEach(sy=>{if(own.includes(sy))ms+=0.34})});let s=ms*3;const inIntent=primary&&t.c==primary;if(inIntent)s+=6;if(t.b)s+=2;if(hasFree(t)&&sk=='beginner')s+=1.5;if(t.m!=null&&sk=='pro')s+=0.5;return Object.assign({s,ms,ownHits,inIntent},t)});
if(qcap&&L.some(t=>t.caps.includes(qcap))){L=L.filter(t=>t.caps.includes(qcap));L.forEach(t=>{t.s+=t.cap==qcap?20:8})}else if(q.length&&!c){if(primary){L=L.filter(t=>t.inIntent||t.ownHits>=2)}else{const mx=Math.max(0,...L.map(t=>t.ms));if(mx>0)L=L.filter(t=>t.ms>0);else{emptyState(raw);return}}}
else if(q.length&&c){const mx=Math.max(0,...L.map(t=>t.ms));if(mx==0){emptyState(raw);return}L=L.filter(t=>t.ms>0)}
const pf=(document.querySelector('input[name=pf]:checked')||{}).value||'all';if(pf=='free')L=L.filter(hasFree);if(pf=='paid')L=L.filter(t=>!hasFree(t));if(bu=='0')L=L.filter(hasFree);else if(bu!='any')L=L.filter(t=>hasFree(t)||(t.m!=null&&t.m<=+bu));
L.sort((x,y)=>y.s-x.s||String(x.n).localeCompare(String(y.n)));const seen=new Set();L=L.filter(t=>!seen.has(t.n)&&seen.add(t.n));
if(!L.length){out.innerHTML=`<div class="fempty" role="status"><h2>No tools match those filters</h2><p>Try a broader budget, choose All for price, or describe the job in different words.</p>${exHTML()}${suggHTML()}</div>`;return}
const X=v=>String(v).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));const $m=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))};
const top=L.slice(0,5);const pick=top.find(t=>t.b&&top[0]&&t.c==top[0].c&&t.cap==top[0].cap)||top[0];const rest=top.filter(t=>t.n!=pick.n);const ru=rest.slice(0,2),more=rest.slice(2);
const cheap=t=>t.mm!=null?{v:t.mm,b:'monthly'}:(t.ma!=null?{v:t.ma,b:'yearly'}:null);
const ptxt=t=>{const c=cheap(t);return c?`from ${$m(c.v)}/mo ${c.b=='yearly'?'billed yearly only':'monthly'}`:'price not checked'};
const reason=t=>{const r=[];if(t.b)r.push(`ToolPick’s Best Value pick for ${X(t.cn.toLowerCase())}`);if(t.fr)r.push('has a real free plan');const c=cheap(t);if(c)r.push(`cheapest plan we checked is ${$m(c.v)}/mo ${c.b=='yearly'?'billed yearly only':'monthly'}`);else r.push('we could not check its price');return r.join(', ')};
const whyNot=t=>{const r=[];const B=pick.mm!=null&&t.mm!=null?'mm':(pick.ma!=null&&t.ma!=null?'ma':null);if(B){const d=Math.round((t[B]-pick[B])*100)/100;r.push(d>0?`${$m(d)}/mo more than ${X(pick.n)} (${B=='mm'?'monthly':'yearly'} prices)`:d<0?`${$m(-d)}/mo less than ${X(pick.n)} (${B=='mm'?'monthly':'yearly'} prices), but not our Best Value pick`:`same price as ${X(pick.n)}`)}else r.push(cheap(t)?`price not compared: ${X(t.n)} is ${ptxt(t)}, ${X(pick.n)} is ${ptxt(pick)}`:'price not checked — see official page');if(!t.fr&&pick.fr)r.push('no real free plan');return r.join('; ')};
const lg=t=>`<span class="logo"><img src="https://www.google.com/s2/favicons?domain=${t.dm}&amp;sz=64" alt="" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${X(t.n[0])}'))"></span>`;
const job=pick.c;let h=`<h2 class="skip" id="res-h">Results</h2><article class="card best fpick"><div class="th">${lg(pick)}<div><div class="badges"><span class="badge b-best">OUR PICK</span>${pick.fr?'<span class="badge b-free">FREE PLAN</span>':''}</div><h3 style="margin:0"><a href="${pick.u}">${X(pick.n)}</a></h3></div></div><p style="margin:8px 0">${X(pick.d)}</p><p><b>Why:</b> ${qcap?`it does the job you asked for (${X(CL[qcap]||qcap)})${pick.cap==qcap?' as its main job':''}, `:''}${reason(pick)}.</p>${!pick.fr&&pick.fa?`<p class="small"><b>Free alternative:</b> <a href="${pick.fa.u}">${X(pick.fa.n)}</a> — ${X(pick.fa.f)}</p>`:''}<p class="small meta">${X(pick.cn)} · checked ${pick.k} · <a href="${X(pick.pr)}" rel="noopener" target="_blank">official pricing</a></p>
<div class="factions">${pick.fr?`<a class="bbtn primary" href="/free.html?job=${job}">Start free with ${X(pick.n)}</a>`:`<a class="bbtn primary" href="${pick.u}">See ${X(pick.n)} prices</a>`}<a class="bbtn" href="/pay-less.html?tool=${pick.sl}">Paying for one already? See if you can pay less</a></div></article>`;
if(ru.length)h+=`<h3 style="margin:16px 0 8px;font-size:1rem">Runners-up</h3><ul class="fru">${ru.map(t=>`<li>${lg(t)}<div><a href="${t.u}"><b>${X(t.n)}</b></a> <span class="small">· ${ptxt(t)}${t.fr?' · free plan':''}</span><br><span class="small"><b>Why not this one:</b> ${whyNot(t)}.</span></div></li>`).join('')}</ul>`;
if(more.length)h+=`<details class="fmore"><summary>${more.length} more match${more.length>1?'es':''}</summary><ul class="fru">${more.map(t=>`<li>${lg(t)}<div><a href="${t.u}"><b>${X(t.n)}</b></a> <span class="small">· ${ptxt(t)}${t.fr?' · free plan':''}</span></div></li>`).join('')}</ul></details>`;
h+=`<p class="small" style="margin-top:12px"><a href="/compare-builder.html?tools=${[pick].concat(ru).map(t=>t.sl).join(',')}">Compare these side by side →</a> · <a href="/tools.html?category=${job}">All ${X(pick.cn.toLowerCase())} tools</a> · Our pick = the Best Value pick for this job if it matches, otherwise the top match. Prices from official pages.</p>`;
out.innerHTML=h}
['q','cat','budget','skill','pf-all','pf-free','pf-paid'].forEach(i=>{const el=document.getElementById(i);el.addEventListener('input',run);el.addEventListener('change',run)});document.querySelectorAll('.chip').forEach(b=>b.addEventListener('click',()=>{const q=document.getElementById('q');q.value=b.dataset.q;run();q.focus()}));document.getElementById('out').addEventListener('click',ev=>{const ex=ev.target.closest('[data-ex]'),ct=ev.target.closest('[data-cat]');if(ex){const q=document.getElementById('q');q.value=ex.dataset.ex;run();q.focus()}else if(ct){document.getElementById('q').value='';document.getElementById('cat').value=ct.dataset.cat;run();document.getElementById('out').scrollIntoView({behavior:'smooth'})}});run();</script>
''')
desc = f"Tell us what you need and compare {total_tools} AI tools across {len(CATEGORIES)} categories — prices checked on official pages, a best-value pick and a free option."
body = f"""<section class="hero"><h1>Find the right AI tool for your need</h1><p class="tag">{e(desc)}</p></section>{FINDER}<div class="pick"><b>Save money on tools you already pay for</b> — find a cheaper plan, see if yearly pays off, find real free plans, and track price changes. <a href="/save-money.html">Open Save money →</a></div><p class="small">More tools: <a href="/help-me-choose.html">Help me choose</a> · <a href="/compare-builder.html">Compare builder</a> · <a href="/cost-calculator.html">Cost calculator</a> · <a href="/tools.html">Browse all {total_tools} tools</a> · <a href="/stacks.html">Starter stacks</a> · <a href="/subscription-audit.html">Subscription Audit</a></p><div id="browse"><h2>Browse by category</h2>
<div class="needs">{''.join(f'<button data-id="{c["id"]}" class="{"on" if i==0 else ""}">{e(c["name"])}</button>' for i,c in enumerate(CATEGORIES))}</div><div class="tabs">
{''.join(f'<section id="{c["id"]}" class="{"on" if i==0 else ""}"><h2>{e(c["need"])}</h2>{picks(c)}<div class="grid">{"".join(card(t,c) for t in c["tools"])}</div><p><a href="/best-ai-{c["id"]}-tools.html">Full guide: best AI {e(c["name"].lower())} tools →</a></p></section>' for i,c in enumerate(CATEGORIES))}</div></div>
{complinks(COMPARISONS)}<p><a href="/guides.html">All guides →</a> · <a href="/price-changes.html">Price changes log</a></p><h2>Best AI tool for…</h2><ul>{"".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS)}</ul>
<script>const b=document.querySelectorAll('.needs button');function show(id){{b.forEach(x=>x.classList.toggle('on',x.dataset.id==id));document.querySelectorAll('.tabs section').forEach(s=>s.classList.toggle('on',s.id==id));}}
b.forEach(x=>x.onclick=()=>{{show(x.dataset.id);history.replaceState(null,'','#'+x.dataset.id)}});if(location.hash)show(location.hash.slice(1));</script>"""
page("/", "ToolPick — find the right AI tool for your need (verified prices)", desc, body,
     [{"@context":"https://schema.org","@type":"WebSite","name":"ToolPick","url":BASE+"/"}])
# category pages
for c in CATEGORIES:
    path = f"/best-ai-{c['id']}-tools.html"; n = c["name"]
    title = f"Best AI {n} Tools ({CHECKED[:4]}): Prices, Free Plans & Best Value"
    d = f"{len(c['tools'])} AI {n.lower()} tools compared with prices from official pricing pages (each tool shows its own checked date). Best value: {c['best']}. Free options: {', '.join(c['free'])}."
    rows = "".join(f"<tr><td><a href='{turl(t['name'])}'>{e(t['name'])}</a></td><td>{fmt(t['monthly'])}</td><td>{fmt(t['annual'])}</td><td>{e(t['per_output'] or '—')}</td><td>{e(t['price'])}</td><td>{e(t['free'])}</td><td>{CHECKED}</td></tr>" for t in c["tools"])
    body = f"""<h1>Best AI {e(n.lower())} tools</h1><p class="tag">{e(d)}</p>{picks(c)}
<div class="sponsor">Sponsored slot available for this category — <a href="/sponsor.html">sponsor ToolPick</a></div>
<h2>Price table</h2><p class="small">Entry paid plan. Monthly = billed monthly; Annual = per-month cost when billed yearly. "—" = not shown/verified on the official page.</p>
<div class="tw"><table><tr><th>Tool</th><th>Monthly</th><th>Annual (per mo)</th><th>Cost per output</th><th>All plans</th><th>Free tier</th><th>Checked</th></tr>{rows}</table></div><h2>All tools</h2><div class="grid">{''.join(card(t,c) for t in c['tools'])}</div>
{complinks(comps_for([t['name'] for t in c['tools']]))}<p><a href="/compare-builder.html">Build your own comparison →</a> Pick any 2–3 tools and share the result.</p>{"".join(f'<p><a href="{role_path(r[0])}">Starter stack for {e(r[2].lower())} →</a> Free, Under $30 and Pro stacks that include {e(n.lower())} tools.</p>' for r in ROLES if c["id"] in r[3])}{f'<p><a href="/free.html?job={c["id"]}">Can I do this for free? →</a> Every {e(n.lower())} tool with a real free plan, and the cheapest upgrade.</p>' if FREE_V21 else ''}<p><a href="/tools.html?category={c['id']}">Browse {e(n.lower())} tools in the full directory →</a> Filter by free plan, verified price, billing and seat pricing.</p><p><a href="/help-me-choose.html?category={c['id']}">Help me choose {e(n.lower())} tools →</a> Answer 5 quick questions and get a ranked shortlist for this category.</p>{'<p><a href="/best-ai-video-tools-under-20.html">Best AI video tools under $20 →</a> Every video tool with a verified entry price under $20/mo, ranked cheapest first.</p>' if c['id']=='video' else ''}{'<p><a href="/free-alternative-to-recraft.html">Free alternatives to Recraft →</a> Images tools with a verified real free plan.</p>' if c['id']=='images' else ''}{'<p><a href="/free-alternative-to-rytr.html">Free alternatives to Rytr →</a> Writing tools with a verified real free plan.</p>' if c['id']=='writing' else ''}"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(c["tools"])]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),(f"Best AI {n} tools",path)])])
# tool pages

# --- AI price changes tracker (v18): auto-generated from price_history.json snapshot diffs ---
# Add a new snapshot (snapshot.py) after a price edit; any tool whose price text differs from the
# previous snapshot appears automatically. Optional plain-English note/tag: PRICE_NOTES in tools.py.
import re as _pre
_ph = json.load(open("price_history.json")) if os.path.exists("price_history.json") else {}
_pd = sorted(_ph)
import tools as _tm; _PN = getattr(_tm, "PRICE_NOTES", {}); _PS = getattr(_tm, "PRICE_SKIP", {})
_TAGL = {"up":"Went up","down":"Went down","newplan":"New plan","correction":"Correction","currency":"Now in USD","changed":"Changed"}
def _dollars(x): return [float(v.replace(",","")) for v in _pre.findall(r"\$([\d,]+(?:\.\d+)?)", x or "")]
CHANGES = []
for _a, _b in zip(_pd, _pd[1:]):
    for _n in sorted(set(_ph[_a]) & set(_ph[_b])):
        _o, _w = _ph[_a][_n], _ph[_b][_n]
        if _o.get("price") == _w.get("price") or f"{_b}|{_n}" in _PS or _n not in tool_pages: continue
        if f"{_b}|{_n}" in _PN: _tag, _sum = _PN[f"{_b}|{_n}"]
        else:
            _od, _nd = _dollars(_o.get("price")), _dollars(_w.get("price"))
            _tag = ("up" if max(_nd) > max(_od) else "down" if max(_nd) < max(_od) else "changed") if _od and _nd else "changed"
            _sum = f"{_n}'s listed prices changed. See the before and after below."
        _t = next(x for x in tool_pages[_n][0]["tools"] if x["name"] == _n)
        CHANGES.append(dict(date=_b, prev=_a, name=_n, s=slug(_n), tag=_tag, label=_TAGL.get(_tag, "Changed"), summary=_sum, old=_o["price"], new=_w["price"],
                            oldf=_o.get("free"), newf=_w.get("free"), pricing=_t["pricing"], cats=[c["id"] for c in tool_pages[_n]]))
CHANGES.sort(key=lambda x: (x["date"], x["name"].lower()), reverse=True)
def _nicedate(d):
    import datetime as _dt; x = _dt.date.fromisoformat(d); return x.strftime("%b ") + str(x.day) + x.strftime(", %Y")
def change_card(c, h="h3"):
    fr = f'<p class="small">Free plan before: {e(c["oldf"])}<br>Free plan now: {e(c["newf"])}</p>' if c["oldf"] != c["newf"] and c["newf"] else ""
    cls = "b-best" if c["tag"] in ("down","newplan") else ("b-free" if c["tag"]=="currency" else "b-rank")
    return (f'<article class="card pcc" id="{c["date"]}-{c["s"]}" data-cats="{" ".join(c["cats"])}" style="margin:12px 0"><div class="badges"><span class="badge {cls}">{e(c["label"].upper())}</span></div>'
            f'<{h} style="margin:4px 0"><a href="{turl(c["name"])}">{e(c["name"])}</a></{h}><p>{e(c["summary"])}</p>'
            f'<div class="pcba"><div><b>Before ({c["prev"]})</b>{e(c["old"])}</div><div><b>Now (checked {c["date"]})</b>{e(c["new"])}</div></div>{fr}'
            f'<p class="small">Recorded {_nicedate(c["date"])} · <a href="{e(c["pricing"])}" rel="noopener" target="_blank">Official pricing page</a> · <a href="{turl(c["name"])}">{e(c["name"])} page</a> · <a href="/pay-less.html?tool={c["s"]}">Pay less than {e(c["name"])}? →</a></p></article>')
CHANGES_BY_TOOL = {}
for _c in CHANGES: CHANGES_BY_TOOL.setdefault(_c["name"], []).append(_c)
# --- v23 "Is X worth it?" verdict block for tool pages (verified facts only) ---
# Rule: 1) Best Value pick for one of its categories -> "Best value for <cat>".
# 2) else a same-category tool (different product) is cheaper on the same billing (monthly vs monthly; yearly vs yearly
#    if the tool has no monthly price) -> "Cheaper option: X at $Y/mo". 3) else no checked USD price -> "Price not checked".
# 4) else "No cheaper checked option". Free alternative: category Best Value if real-free, else first of c["free"], else first real-free.
def _num(v): return v if isinstance(v, (int, float)) else None
def _usd(v): r = round(v, 2); return "$" + (f"{int(r):,}" if r == int(r) else f"{r:,.2f}")
def tool_verdict(name, cats, t):
    m, a = _num(t["monthly"]), _num(t["annual"])
    cm, ca = cheaper_alt(name, "monthly"), cheaper_alt(name, "annual")
    fa = free_alt(name)
    bestc = [cc for cc in cats if cc["best"] == name]
    tn = ""
    if bestc: verdict = f"Best value for {bestc[0]['name'].lower()}" + (" — and it has a real free plan" if realfree(t) else "")
    elif m is not None and cm is not None and cm["monthly"] < m: verdict = f"Cheaper option: {cm['name']} at {_usd(cm['monthly'])}/mo (monthly prices, same job: {cap_label(name)})"; tn = tier_note(name, cm["name"])
    elif a is not None and ca is not None and ca["annual"] < a: verdict = f"Cheaper option: {ca['name']} at {_usd(ca['annual'])}/mo (billed-yearly prices, same job: {cap_label(name)})"; tn = tier_note(name, ca["name"])
    elif m is None and a is None: verdict = "Price not checked — see the official pricing page"
    elif not samejob(name) or (cm is None and ca is None): verdict = NO_LIKE
    else: verdict = f"No cheaper checked option — {name} has the lowest checked price for {cap_label(name)}"
    if tn: verdict += ". " + tn.rstrip(".")
    s = slug(name); rows = []
    rows.append(("Cheapest plan we checked", " · ".join(x for x in [f"{_usd(m)}/mo monthly" if m is not None else "", f"{_usd(a)}/mo paid yearly" if a is not None else ""] if x) or "Not checked in US dollars — see the official page"))
    rows.append(("All plans we listed", e(PLANS_SHORT.get(name, t["price"]))))
    rows.append(("Real free plan", ("Yes — " + e(t["free"])) if realfree(t) else "No (" + e(t["free"]) + ")"))
    rows.append(("ToolPick Best Value pick", f"Yes, for {e(bestc[0]['name'].lower())}" if bestc else "No"))
    def cmp(x, key, own):
        if x is None: return "none checked"
        d = (f" — {_usd(own - x[key])}/mo less" if x[key] < own else f" — {_usd(x[key] - own)}/mo more" if x[key] > own else " — same price") if own is not None else ""
        return f'<a href="{turl(x["name"])}">{e(x["name"])}</a> {_usd(x[key])}/mo{d}'
    alt_parts = []
    if m is not None or (a is None and cm is not None): alt_parts.append("Monthly: " + cmp(cm, "monthly", m))
    if a is not None: alt_parts.append("Billed yearly: " + cmp(ca, "annual", a))
    rows.append((f"Cheapest same-job alternative ({e(cap_label(name))})", " · ".join(alt_parts) if (cm or ca) else NO_LIKE))
    rows.append(("Best real-free alternative", f'<a href="{turl(fa["name"])}">{e(fa["name"])}</a> — {e(fa["free"])}' if fa else "None with the same main job in our list"))
    rows.append(("What it does (main job first)", e(", ".join(CAP_LABEL.get(k, k) for k in CAPS[name])))); rows.append(("Categories", ", ".join(f'<a href="/best-ai-{cc["id"]}-tools.html">{e(cc["name"])}</a>' for cc in cats)))
    ch = CHANGES_BY_TOOL.get(name, [])
    if ch: rows.append(("Recent price change", f'{e(ch[0]["label"])}, {ch[0]["date"]}: {e(ch[0]["summary"])} <a href="/price-changes.html#{ch[0]["date"]}-{ch[0]["s"]}">Details</a>'))
    btns = f'<a class="bbtn primary" href="/pay-less.html?tool={s}">Can I pay less?</a>'
    if realfree(t) or fa: btns += f'<a class="bbtn" href="/free.html?job={cats[0]["id"]}">Free options</a>'
    if m is not None and a is not None: btns += f'<a class="bbtn" href="/monthly-or-yearly.html?tool={s}">Monthly or yearly?</a>'
    html_ = (f'<section class="verdict card best" aria-labelledby="vh"><h2 id="vh" style="margin:0 0 6px;font-size:1.15rem">Is {e(name)} worth it?</h2><p class="vline"><b>{e(verdict)}.</b></p>'
             '<dl class="vgrid">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + '</dl>'
             f'<div class="factions">{btns}</div><p class="small" style="margin:8px 0 0">Prices checked {t.get("checked", CHECKED)} on the <a href="{e(t["pricing"])}" rel="noopener" target="_blank">official pricing page</a> · <a href="/cost-calculator.html?tool={s}&amp;seats=1&amp;billing=monthly">Full cost calculator</a>. Verdict rule: Best Value pick first; otherwise a cheaper tool that does the same main job ({e(cap_label(name))}) on the same billing; otherwise “{NO_LIKE}”. No ratings or reviews.</p></section>')
    return html_, verdict
for name, cats in tool_pages.items():
    c = cats[0]; t = next(x for x in c["tools"] if x["name"] == name); path = turl(name)
    pros, cons = proscons(t, c)
    title = f"{name} Pricing & Free Plan ({CHECKED[:7]}) — Pros, Cons, Alternatives"
    d = f"{name} pricing checked {t.get('checked', CHECKED)}: {t['price']}. Free tier: {t['free']}. Pros, cons and alternatives."[:300]
    alts = [x["name"] for cc in cats for x in cc["tools"] if x["name"] != name]
    vhtml, vtxt = tool_verdict(name, cats, t)
    u20 = ('<p><a href="/best-ai-video-tools-under-20.html">Best AI video tools under $20 →</a> This tool is in our under-$20 video list' + ('' if (_num(t['monthly']) is not None and t['monthly'] < 20) else ' (only when billed yearly)') + '.</p>') if (cats[0]['id']=='video' and _entry_num(t) is not None and _entry_num(t) < 20) else ''

    body = f"""<h1>{e(name)} pricing &amp; review</h1><p class="tag">{e(t['about'])}</p>{vhtml}
<p><a class="btn" href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Visit {e(name)} official site</a></p>{DISCLOSURE if t.get('affiliate') else ''}
{'<p><a href="/free-alternative-to-recraft.html">Free alternatives to Recraft →</a> Compare Images tools with a verified real free plan.</p>' if name=='Recraft' else ''}{'<p><a href="/free-alternative-to-rytr.html">Free alternatives to Rytr →</a> Compare Writing tools with a verified real free plan.</p>' if name=='Rytr' else ''}{u20}
<h2>Alternatives that do the same main job ({e(cap_label(name))})</h2><p>{(' · '.join(f'<a href="{turl(x["name"])}">{e(x["name"])}</a>' for x in samejob(name))) or 'None in our list yet. ' + ' · '.join(f'<a href="/best-ai-{cc["id"]}-tools.html">All {e(cc["name"].lower())} tools</a>' for cc in cats)}</p>{complinks(comps_for([name]))}"""
    sw = {"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"applicationCategory":"BusinessApplication","operatingSystem":"Web","url":t["url"],"description":t["about"]}
    fh, fl = faq(tool_qas(t) + [(f"Is there a cheaper alternative to {name}?", vtxt + " (ToolPick verdict from prices checked on official pricing pages).")]); body += fh
    page(path, title, d, body, [sw, fl, crumbs([("ToolPick","/"),(f"Best AI {c['name']} tools",f"/best-ai-{c['id']}-tools.html"),(name,path)])])
# comparison pages
def find(n): return next(x for c in CATEGORIES for x in c["tools"] if x["name"] == n)
def cnames(x): return x[2] if isinstance(x[2], list) else [x[2], x[3]]
def compare_verdict(N, TT, c):
    """v25: like-for-like compare verdict. Same main job (cap1) -> same-billing price comparison; else 'different jobs', no price pick."""
    def nm(t): return f'<a href="{turl(t["name"])}">{e(t["name"])}</a>'
    caps = {t["name"]: cap1(t["name"]) for t in TT}
    same = len(set(caps.values())) == 1
    free = [t for t in TT if realfree(t)]
    rows = []; tnote = ""; ranked = []; basis = None; win = None
    BL = {"monthly": "monthly", "annual": "billed-yearly"}
    if not same:
        verdict = "These do different jobs: " + ", ".join(f"{t['name']} is for {cap_label(t['name'])}" for t in TT) + " — so we make no price-based pick"
        rows.append(("Main job", " · ".join(f'{nm(t)}: {e(cap_label(t["name"]))}' for t in TT)))
    else:
        basis = "monthly" if all(_num(t["monthly"]) is not None for t in TT) else ("annual" if all(_num(t["annual"]) is not None for t in TT) else None)
        if basis:
            ranked = sorted(TT, key=lambda t: (t[basis], t["name"].lower()))
            win = ranked[0] if ranked[0][basis] < ranked[1][basis] else None
            lo = ranked[0][basis]
            rows.append((f"Price on {BL[basis]} billing", " · ".join(f'{nm(t)} {_usd(t[basis])}/mo' + (f' (+{_usd(t[basis]-lo)}/mo, +{_usd((t[basis]-lo)*12)}/yr)' if t[basis] > lo else '') for t in ranked)))
            ob = "annual" if basis == "monthly" else "monthly"
            if all(_num(t[ob]) is not None for t in TT):
                r2 = sorted(TT, key=lambda t: (t[ob], t["name"].lower())); lo2 = r2[0][ob]
                rows.append((f"On {BL[ob]} billing", " · ".join(f'{nm(t)} {_usd(t[ob])}/mo' + (f' (+{_usd(t[ob]-lo2)}/mo, +{_usd((t[ob]-lo2)*12)}/yr)' if t[ob] > lo2 else '') for t in r2)))
            if win: tnote = next((tier_note(win["name"], t["name"]) for t in ranked[1:] if tier_note(win["name"], t["name"])), "")
        else:
            nop = [t for t in TT if _num(t["monthly"]) is None and _num(t["annual"]) is None]
            S = {b: sorted([t for t in TT if _num(t[b]) is not None], key=lambda t: (t[b], t["name"].lower())) for b in ("monthly", "annual")}
            S = {b: L for b, L in S.items() if len(L) >= 2}
            for b, L in S.items():
                lo = L[0][b]
                rows.append((f"Price on {BL[b]} billing", " · ".join(f'{nm(t)} {_usd(t[b])}/mo' + (f' (+{_usd(t[b]-lo)}/mo, +{_usd((t[b]-lo)*12)}/yr)' if t[b] > lo else '') for t in L) + (" · not listed: " + ", ".join(e(t["name"]) for t in TT if t not in L) + " (no checked price on this billing)" if len(L) < len(TT) else "")))
            for t in nop: rows.append(("Price", f'{nm(t)}: {e(t["price"])} — not in a form we can compare, so it is not ranked'))
            mixed_win = None
            cov = set(t["name"] for L in S.values() for t in L)
            if S and not nop and cov == set(t["name"] for t in TT):
                cands = [t for t in TT if all(t in L and L[0] is t and L[1][b] > t[b] for b, L in S.items())]
                if cands: mixed_win = cands[0]
            if mixed_win:
                verdict_mixed = f"Pick {mixed_win['name']} if price matters: it is cheapest on each billing we can compare like for like — " + "; ".join(f"{_usd(L[1][b]-L[0][b])}/mo ({_usd((L[1][b]-L[0][b])*12)}/yr) less than {L[1]['name']} on {BL[b]} billing" for b, L in S.items())
            else:
                verdict_mixed = "No price pick: " + (", ".join(t["name"] for t in nop) + " has no comparable checked price" if nop else "their prices are not all checked on the same billing") + " — compare the plans on the official pages"
        if len(free) == 1:
            o = [t for t in TT if t is not free[0]]
            verdict = f"Start free with {free[0]['name']}: only it has a real free plan" + (f"; if you will pay, {win['name']} is {_usd(ranked[1][basis]-win[basis])}/mo ({_usd((ranked[1][basis]-win[basis])*12)}/yr) less on {BL[basis]} billing" if win and len(TT) == 2 else "")
        elif win:
            nxt = ranked[1]; d = nxt[basis] - win[basis]
            verdict = f"Pick {win['name']} if price matters: {_usd(d)}/mo ({_usd(d*12)}/yr) less than {nxt['name']} on {BL[basis]} billing"
        elif basis: verdict = f"Same {BL[basis]} price — pick on features"
        else: verdict = verdict_mixed
        if tnote: verdict += ". " + tnote.rstrip(".")
        if tnote: rows.append(("Plan tier", " · ".join(f'{nm(t)}: {e(LOWER_TIER[t["name"]])}' for t in TT if t["name"] in LOWER_TIER) + " — compare features before switching"))
    rows.append(("Real free plan", " · ".join(f'{nm(t)}: {"yes" if realfree(t) else "no"}' for t in TT)))
    fa_parts = []
    for t in TT:
        if realfree(t): continue
        onpage = next((x for x in TT if same and realfree(x)), None)
        f = onpage or free_alt(t["name"])
        fa_parts.append(f'For {e(t["name"])}: ' + (f'{nm(f)}' + (' (on this page)' if f is onpage else '') + f' — {e(f["free"])}' if f else "none that does the same main job"))
    if fa_parts: rows.append(("Free alternative (same main job)", " · ".join(fa_parts)))
    bv = [t for t in TT if t["name"] in BEST_OF]
    rows.append(("ToolPick Best Value pick", " · ".join(f'{nm(t)} (for {e(", ".join(cc["name"].lower() for cc in CATEGORIES if cc["best"]==t["name"]))})' for t in bv) or f'Neither — for {e(c["name"].lower())} it is <a href="{turl(c["best"])}">{e(c["best"])}</a>'))
    btns = ""
    for k, f0 in enumerate(free[:2]): btns += f'<a class="bbtn{" primary" if k == 0 else ""}" href="{turl(f0["name"])}">Start free with {e(f0["name"])}</a>'
    if same and basis and ranked and ranked[-1][basis] > ranked[0][basis]:
        ex = ranked[-1]; btns += f'<a class="bbtn" href="/pay-less.html?tool={slug(ex["name"])}&amp;pay={ex[basis]:g}' + ('&amp;bill=yearly' if basis == "annual" else '') + f'">Paying for {e(ex["name"])}? See your saving</a>'
    btns += f'<a class="bbtn" href="/compare-builder.html?tools={",".join(slug(n) for n in N)}">Open in compare builder</a>'
    html_ = (f'<section class="verdict card best" aria-labelledby="vh"><h2 id="vh" style="margin:0 0 6px;font-size:1.15rem">Which should you pick?</h2><p class="vline"><b>{e(verdict)}.</b></p><dl class="vgrid">'
             + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + f'</dl><div class="factions">{btns}</div><p class="small" style="margin:8px 0 0">Rule: we only compare prices when the tools do the same main job (from what each official site says it does), and only on the same billing (monthly with monthly, billed-yearly with billed-yearly). A real free plan on only one tool comes first. Prices from official pricing pages, each with its own checked date below. No ratings or reviews.</p></section>')
    return html_, verdict

for x in COMPARISONS:
    s_, title0, cid = x[0], x[1], x[4]; N = cnames(x); TT = [find(n) for n in N]
    path = f"/compare/{s_}.html"; c = next(y for y in CATEGORIES if y["id"] == cid)
    title = f"{title0} ({CHECKED[:4]}): Price, Free Plan & Which to Pick"
    d = f"{' vs '.join(N)} compared with prices from official pricing pages (per-tool checked dates): plans, free tiers and which is better value."
    vhtml, vtxt = compare_verdict(N, TT, c)
    row = lambda lab, f: f"<tr><th>{lab}</th>" + "".join(f"<td>{f(t)}</td>" for t in TT) + "</tr>"
    _rel = [y for y in comps_for(N) if y[0] != s_][:8]
    body = (f'<h1>{e(title0)}</h1><p class="tag">{e(d)}</p>{vhtml}<div class="tw"><table><tr><th></th>' + "".join(f'<th><a href="{turl(n)}">{e(n)}</a></th>' for n in N) + "</tr>"
      + row("What it is", lambda t: e(t["about"])) + row("All plans", lambda t: e(t["price"])) + row("Free tier", lambda t: e(t["free"]))
      + row("Checked", lambda t: f'{t.get("checked", CHECKED)} · <a href="{e(t["pricing"])}" rel="noopener">pricing page</a>') + "</table></div>"
      + f'<p class="small">More: <a href="/best-ai-{cid}-tools.html">best AI {e(c["name"].lower())} tools</a> · <a href="/tools.html?category={cid}">all {e(c["name"].lower())} tools</a> · <a href="/cost-calculator.html?category={cid}&amp;seats=1&amp;billing=monthly">cost calculator</a></p>{complinks(_rel)}')
    il = {"@context":"https://schema.org","@type":"ItemList","name":title0,"itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(n),"name":n} for k,n in enumerate(N)]}
    qas = [q for t in TT for q in tool_qas(t)] + [(f"What is ToolPick's best-value pick for {c['name'].lower()}?", f"{c['best']}: {find(c['best']).get('why','')}".strip())]
    qas.append((f"Which should I pick, {' or '.join(N)}?", vtxt + " (ToolPick rule using prices checked on official pricing pages)."))
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
_likefields(_bmap)
BDATA = json.dumps(sorted(_bmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
BOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])} — {e(", ".join(v["cats"]))}</option>' for v in sorted(_bmap.values(), key=lambda x: x["n"].lower()))
builder_body = f"""<h1>Compare any AI tools side by side</h1><p class="tag">Pick 2 or 3 tools from ToolPick's verified list and compare what they do, what they cost, and whether they have a free plan. Prices are copied from official pricing pages — checked dates are shown on every card. Nothing here is invented or re-priced.</p>
<div class="builder"><form id="bform"><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-bottom:12px">Choose 2–3 tools to compare</legend><div class="bform">
<div><label for="tool1">Tool 1 (required)</label><select id="tool1" name="tool1"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool2">Tool 2 (required)</label><select id="tool2" name="tool2"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool3">Tool 3 (optional)</label><select id="tool3" name="tool3"><option value="">Select a tool…</option>{BOPTS}</select></div>
</div></fieldset><div class="bactions"><button type="submit" class="bbtn primary">Compare tools</button><button type="button" class="bbtn" id="copyBtn">Copy share link</button><button type="button" class="bbtn" id="clearBtn">Clear</button><span class="small bstatus" id="bstatus" role="status"></span></div></form></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How the Best Value badge is chosen</h2><p class="small" style="margin:0">Only when your picks do the same main job (from what each official site says it does). Then: if exactly one is ToolPick's Best Value pick for its category, it gets the badge; otherwise the badge goes to the tool that is cheaper on the same billing (monthly with monthly, or billed-yearly with billed-yearly, when all picks have that price). If your picks do different jobs, or their prices aren't checked on the same billing, no badge is given. Prices we can't compare (“check site”, euros, usage-only) are never ranked.</p><p class="small" style="margin:12px 0 0">Want true monthly and yearly totals by seats and billing period? <a href="/cost-calculator.html">Open the “What will it really cost?” calculator →</a></p><p class="small" style="margin:12px 0 0">Or <a href="/tools.html">browse the full directory of all tools →</a> and add tools to compare from there.</p></div>
<div id="builder-out" aria-live="polite" aria-atomic="false"><p class="small">Pick at least 2 different tools above to see your comparison. You can also try <a href="/compare-builder.html?tools=elevenlabs,murf,speechify">ElevenLabs vs Murf vs Speechify</a>.</p></div>
<script>const BD={BDATA};
const bySlug={{}};BD.forEach(t=>bySlug[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
const sels=()=>['tool1','tool2','tool3'].map(id=>document.getElementById(id));
function selected(){{const seen=new Set(),out=[];sels().forEach(s=>{{if(s.value&&!seen.has(s.value)&&bySlug[s.value]){{seen.add(s.value);out.push(bySlug[s.value])}}}});return out}}
function sameJob(list){{return list.every(t=>t.cap==list[0].cap)}}
function basis(list){{return list.every(t=>t.mm!=null)?'mm':(list.every(t=>t.ma!=null)?'ma':null)}}
function bestValue(list){{if(list.length<2||!sameJob(list))return null;const catBest=list.filter(t=>t.b);if(catBest.length==1)return catBest[0];const B=basis(list);if(!B)return null;const r=list.slice().sort((a,b)=>a[B]-b[B]);return r[0][B]<r[1][B]?r[0]:null}}
function m$(v){{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))}}
function entry(t){{const p=[];if(t.mm!=null)p.push(m$(t.mm)+'/mo monthly');if(t.ma!=null)p.push(m$(t.ma)+'/mo billed yearly');return p.length?'Cheapest plan we checked: '+p.join(' · '):'Price not in a form we can compare (“check site”, euros or usage-based)'}}
function verdictLine(list,bv){{if(!sameJob(list))return '<div class="pick"><b>These do different jobs:</b> '+list.map(t=>X(t.n)+' is for '+X(t.cl)).join(', ')+' — so we don’t pick one on price.</div>';const B=basis(list);if(!B)return '<div class="pick"><b>Same main job ('+X(list[0].cl)+'), but not every price is checked on the same billing</b>, so we don’t name a cheaper one.</div>';const r=list.slice().sort((a,b)=>a[B]-b[B]);const BL=B=='mm'?'monthly':'billed-yearly';const d=r[1][B]-r[0][B];const tn=list.some(t=>t.lt)&&!list.every(t=>t.lt)?' <b>Different tier: compare features before switching.</b>':'';return '<div class="pick">'+(bv?'<span class="badge b-best">BEST VALUE</span> <b><a href="'+bv.u+'">'+X(bv.n)+'</a></b> — '+(bv.b&&list.filter(t=>t.b).length==1?'ToolPick’s Best Value pick for its category. ':'')+'':'')+'Same main job ('+X(list[0].cl)+'). On '+BL+' billing: '+r.map(t=>X(t.n)+' '+m$(t[B])+'/mo').join(' · ')+(d>0?' — '+X(r[0].n)+' is '+m$(d)+'/mo ('+m$(d*12)+'/yr) less than '+X(r[1].n)+'.':' — same price.')+tn+'</div>'}}
function render(push=true){{const list=selected();const out=document.getElementById('builder-out');const st=document.getElementById('bstatus');
if(list.length<2){{out.innerHTML='<div class="pick"><b>Pick at least 2 different tools to compare.</b><p class="small" style="margin-bottom:0">You have selected '+list.length+' tool'+(list.length==1?'':'s')+'. Choose '+(2-list.length)+' more above — comparisons work with 2 or 3 tools.</p></div>';if(push)history.replaceState(null,'',list.length?('?tools='+list.map(t=>t.s).join(',')):'/compare-builder.html');return}}
const bv=bestValue(list);
const cards=list.map(t=>`<article class="card${{bv&&t.s==bv.s?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{bv&&t.s==bv.s?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p><p class="small">${{X(t.f)}}</p><p class="small">${{entry(t)}}</p><p class="small meta">${{X(t.cats.join(', '))}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p></article>`).join('');
const row=(lab,fn)=>'<tr><th scope="row">'+lab+'</th>'+list.map(t=>`<td>${{fn(t)}}</td>`).join('')+'</tr>';
out.innerHTML=`<h2>Your comparison (${{list.length}} tools)</h2>${{verdictLine(list,bv)}}<div class="grid">${{cards}}</div><div class="tw"><table><caption class="small" style="text-align:left;padding:12px 16px">Side-by-side details. Prices checked on official pages; confirm before buying.</caption><tr><th scope="col">Tool</th>${{list.map(t=>`<th scope="col"><a href="${{t.u}}">${{X(t.n)}}</a>${{bv&&t.s==bv.s?' ★':''}}</th>`).join('')}}</tr>${{row('What it is',t=>X(t.d))}}${{row('Starting price (as listed)',t=>X(t.p))}}${{row('Cheapest plan we checked',t=>entry(t))}}${{row('Main job',t=>X(t.cl))}}${{row('Free plan / free option',t=>X(t.f))}}${{row('Categories',t=>X(t.cats.join(', ')))}}${{row('Price checked',t=>t.k+' · <a href="'+X(t.pr)+'" rel="noopener" target="_blank">pricing page</a>')}}</table></div><p class="small">Share this comparison: <a href="?tools=${{list.map(t=>t.s).join(',')}}">${{location.origin}}/compare-builder.html?tools=${{list.map(t=>t.s).join(',')}}</a></p>`;
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
_likefields(_cmap)
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
<p class="small">Paying for several tools? <a href="/subscription-audit.html">Run the 60-second Subscription Audit →</a> Check for overlapping subscriptions and free tiers you could try first.</p><p class="small">Browse first? <a href="/tools.html">Open the full tools directory →</a> · Compare tools instead? <a href="/compare-builder.html">Open the compare builder →</a> Prices change — always confirm on the official pricing page linked with every result.</p>
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
function catView(cat,seats,billing){{const rows=cat.tools.map(s=>byS[s]).filter(Boolean).map(t=>({{t:t,c:cost(t,billing,seats)}}));const priced=rows.filter(x=>x.c).sort((x,y)=>x.t.cl.localeCompare(y.t.cl)||(x.c.monthly-y.c.monthly));const unpriced=rows.filter(x=>!x.c);const bvT=priced.find(x=>x.t.s==cat.best);const bv=bvT||null;const rule='ToolPick’s existing Best Value pick for this category, with a verified price for your billing choice.';const low={{}};priced.forEach(x=>{{if(!low[x.t.cap])low[x.t.cap]={{s:x.t.s,n:0}};low[x.t.cap].n++}});
let h=`<h2>${{X(cat.name)}} — true costs (${{seats}} seat${{seats==1?'':'s'}}, ${{billing}} billing)</h2>`;
if(bv){{h+=`<div class="pick"><span class="badge b-best">BEST VALUE</span> <b><a href="${{bv.t.u}}">${{X(bv.t.n)}}</a></b> — ${{rule}} True cost: <b>${{money(bv.c.monthly,bv.c.cur)}}/mo · ${{money(bv.c.yearly,bv.c.cur)}}/yr</b>. <span class="small">${{basis(bv.t,seats)}} · checked ${{bv.t.k}} · <a href="${{X(bv.t.pr)}}" rel="noopener" target="_blank">official pricing page</a></span></div>`}}
else if(priced.length){{h+=`<div class="pick"><b>The ${{X(cat.name)}} Best Value pick has no verified price for ${{billing}} billing, so we don’t name one here.</b> <span class="small">These tools do different main jobs, so we only call one cheaper within the same job (marked below).</span></div>`}}
else{{h+=`<div class="pick"><b>No verified numeric entry prices in this category for ${{billing}} billing, so nothing is ranked.</b><p class="small" style="margin-bottom:0">Try the other billing period, or check the official pricing pages linked below. We don't guess prices.</p></div>`}}
h+=`<div class="tw"><table><caption class="small" style="text-align:left;padding:12px 16px">Grouped by main job, cheapest first within each job on your billing choice — we only call a tool cheaper than another that does the same job. Tools with no verified rate for this billing choice are listed last and not ranked.</caption><tr><th scope="col">Tool</th><th scope="col">Listed price (as verified)</th><th scope="col">True monthly</th><th scope="col">True yearly</th><th scope="col">Free option</th><th scope="col">Checked</th></tr>`;
priced.concat(unpriced).forEach(x=>{{const t=x.t;h+=`<tr><td><a href="${{t.u}}">${{X(t.n)}}</a>${{bv&&t.s==bv.t.s?' <span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?' <span class="badge b-free">FREE PLAN</span>':''}}${{x.c&&low[t.cap]&&low[t.cap].s==t.s&&low[t.cap].n>1?' <span class="badge b-rank">CHEAPEST FOR THIS JOB</span>':''}}<br><span class="small">Main job: ${{X(t.cl)}} · ${{basis(t,seats)}}</span></td><td class="small">${{X(t.p)}}</td><td>${{x.c?('<b>'+money(x.c.monthly,x.c.cur)+'/mo</b>'):'<span class="check">No verified rate — not ranked</span>'}}</td><td>${{x.c?('<b>'+money(x.c.yearly,x.c.cur)+'/yr</b>'):'—'}}</td><td class="small">${{X(t.f)}}</td><td class="small">${{t.k}}<br><a href="${{X(t.pr)}}" rel="noopener" target="_blank">Pricing page</a></td></tr>`}});
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
_likefields(_wmap)
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
<p class="small">Prefer to browse? <a href="/tools.html">See the full directory with filters →</a> · Already paying for tools? <a href="/subscription-audit.html">Audit your subscriptions in 60 seconds →</a></p><div id="wiz-out" aria-live="polite" aria-atomic="false"></div>
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
if(opts.lowest&&opts.lowest[t.cap]&&opts.lowest[t.cap].t.s==t.s&&opts.lowest[t.cap].n>1&&e)reasons.push('Cheapest '+v.billing+' price here for '+t.cl+' at '+money(e.amt,e.cur)+'/mo');
if(t.fr)reasons.push('Has a verified free plan');
const sv=annualSave(t);if(sv&&v.billing=='annual')reasons.push('Annual billing saves '+money(sv.m.amt-sv.a.amt,sv.a.cur)+'/mo vs monthly per verified rates ('+money(sv.a.amt,sv.a.cur)+' vs '+money(sv.m.amt,sv.m.cur)+')');
if(e&&t.ps&&v.seats>1)reasons.push('Per-seat entry price × '+v.seats+' seats');
if(opts.over&&e)reasons.push('Closest verified option at '+money(e.amt,e.cur)+'/mo — over your '+(v.budget=='free'?'free-only':('$'+v.budget+'/mo'))+' budget');
else if(e&&v.budget!='any'&&v.budget!='free')reasons.push('Verified entry '+money(e.amt,e.cur)+'/mo fits your $'+v.budget+' budget');
if(!opts.over&&v.budget=='free'&&t.fr)reasons.push('Fits free-only using its verified free plan');
if(!e)reasons.push('Price not verified in our table — shown unranked, never assumed to fit a budget');
const uniq=[...new Set(reasons)].slice(0,3);
return `<article class="card${{isBV?' best':''}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{opts.over?'<span class="badge" style="background:var(--warn);color:#fff">OVER BUDGET</span>':''}}${{isBV?'<span class="badge b-best">BEST VALUE</span>':''}}${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}${{!e&&!opts.over?'<span class="badge b-rank">PRICE NOT VERIFIED</span>':''}}</div><h3><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p>${{X(t.d)}}</p><p class="price">${{X(t.p)}}</p>${{e?`<p><b>${{money(e.amt,e.cur)}}/mo</b> <span class="small">true entry cost at ${{v.seats}} seat${{v.seats==1?'':'s'}}, ${{v.billing}} billing${{t.ps?' (per-seat price × seats)':' (seats don’t change the listed price)'}}</span></p>`:`<p class="small check">No verified numeric entry rate for ${{v.billing}} billing — not ranked by price.</p>`}}<p class="small">${{X(t.f)}}</p>${{uniq.length?`<p class="small"><b>Why this pick:</b> ${{uniq.map(X).join(' · ')}}</p>`:''}}<p class="small meta">Main job: ${{X(t.cl)}} · checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p><p class="small"><a href="${{t.u}}">Tool page →</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=${{v.seats}}&amp;billing=${{v.billing}}">Cost calculator for ${{X(t.n)}} →</a></p></article>`}}
function results(push=true){{const v=vals();const out=document.getElementById('wiz-out');const st=document.getElementById('wStatus');if(!v.category){{st.textContent='Pick what you are trying to do first.';showStep(1);return}}
const cat=catBy[v.category];let cand=cat.tools.map(s=>byS[s]).filter(Boolean).map(t=>({{t:t,e:eff(t,v.billing,v.seats)}}));
cand=cand.filter(x=>(v.free!='required'||x.t.fr)&&(v.annual!='required'||annualSave(x.t)));
const fitting=cand.filter(x=>fitsBudget(x.t,v,x.e));
const priced=fitting.filter(x=>x.e&&x.e.cur=='$').sort((a,b)=>a.e.amt-b.e.amt);
const lowest={{}};priced.forEach(x=>{{const k=x.t.cap;if(!lowest[k])lowest[k]={{t:x.t,n:0}};lowest[k].n++}});
let bv=null;const catBest=fitting.find(x=>x.t.s==cat.best);if(catBest)bv=catBest.t;
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



# --- AI Subscription Audit (v14 preview) ---
# Only verified tools.py data + the user's own amounts. One primary action per paid tool
# (overlap-cancel > try-free-tier > cheaper/free switch > keep) so potential savings never
# double-count a tool. Fully client-side: no form is sent, no amounts are stored by us.
_amap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _amap:
            _amap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"],
                             fr=realfree(_t), cats=[])
        _catref = dict(id=_c["id"], name=_c["name"], best=slug(_c["best"]), bestName=_c["best"])
        if _catref not in _amap[_k]["cats"]: _amap[_k]["cats"].append(_catref)
_likefields(_amap)
ADATA = json.dumps(sorted(_amap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
AOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])} — {e(", ".join(x["name"] for x in v["cats"]))}</option>' for v in sorted(_amap.values(), key=lambda x: x["n"].lower()))
audit_body = f"""<h1>AI Subscription Audit — what could you stop paying for?</h1><p class="tag">A 60-second check for subscription fatigue. Add the AI tools you pay for, confirm what you pay each month (our verified entry price is prefilled where we have one — edit it, your plan may differ), and get one clear action per tool: keep it, consider cancelling it, try its free tier first, or check a cheaper switch. Potential savings are counted once per tool, never twice.</p>
<div class="bnote"><p class="small" style="margin:0"><b>Your privacy:</b> this runs entirely in your browser. Your list and amounts are not sent to us and are not stored by us. They only appear in the share link if you copy one — so only share that link if you are happy for whoever opens it to see your list and amounts. Every price we show is copied from the tool's official pricing page with its checked date; free-tier limits are on that official page, not guessed here.</p></div>
<div class="builder"><h2 style="margin-top:0;font-size:1.05rem">1. Add tools you pay for</h2><div class="aform"><div><label for="a-search">Search tools</label><input type="search" id="a-search" autocomplete="off" placeholder="Start typing a tool name…"></div><div><label for="a-select">Tool</label><select id="a-select"><option value="">Select a tool…</option>{AOPTS}</select></div><button type="button" class="bbtn primary" id="a-add">Add tool</button></div><p class="small" id="a-status" role="status" style="margin:12px 0 0"></p><div id="a-rows"></div><div class="atotal" aria-live="polite" id="a-total">No tools added yet. Add your first paid tool above — it takes about a minute.</div><div class="bactions"><button type="button" class="bbtn primary" id="a-run">Run my audit</button><button type="button" class="bbtn" id="a-copy">Copy share link</button><button type="button" class="bbtn" id="a-clear">Clear all</button></div></div>
<h2>2. Your audit</h2><div id="a-out" aria-live="polite" aria-atomic="false"><div class="pick"><b>No tools added yet.</b><p class="small" style="margin-bottom:0">Add the tools you pay for above, check the amounts, and your keep / consider cancelling / try the free tier checklist will appear here. Try the example: <a href="/subscription-audit.html?tools=descript:24:monthly,chatgpt:8:monthly,midjourney:10:monthly">Descript $24 + ChatGPT $8 + Midjourney $10</a>.</p></div></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How each action is chosen — one per tool</h2><p class="small" style="margin:0">In this order, so a tool is never counted twice: <b>1. Consider cancelling</b> — you pay for 2 or more tools that do the same main job (based on what each official site says it does — a shared broad category is not enough); we suggest keeping a ToolPick Best Value pick if one is among them, otherwise the one that costs you least, and cancelling the others. <b>2. Try the free tier</b> — the tool itself has a verified real free plan (free trials and one-time credits do not count). <b>3. Switch to check</b> — another tool that does the same main job has a cheaper checked price on the same billing you pay (monthly with monthly, billed-yearly with billed-yearly); we add a tier note when the plans are different tiers, and count only the difference as potential saving, not your whole amount. <b>4. Keep</b> — none of the above applies on verified data. “Potential saving” always means <i>if you act on every suggestion</i>; tick or untick suggestions below to see your own plan total.</p><p class="small" style="margin:12px 0 0">Next steps: <a href="/compare-builder.html">compare tools side by side</a> · <a href="/cost-calculator.html">what will it really cost?</a> · <a href="/help-me-choose.html">help me choose a replacement</a> · <a href="/tools.html">browse all tools</a></p></div>
<script>const AD={ADATA};
const byS={{}};AD.forEach(t=>byS[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function pv(v){{if(v==null)return null;if(typeof v=='number')return{{amt:v,cur:'$'}};const m=String(v).match(/([€$£])\\s*([\\d.]+)/);if(m)return{{amt:parseFloat(m[2]),cur:m[1]}};const n=String(v).match(/([\\d.]+)/);return n?{{amt:parseFloat(n[1]),cur:'$'}}:null}}
function money(v){{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))}}
function entry(t){{const vals=[pv(t.m),pv(t.a)].filter(x=>x&&x.cur=='$');if(!vals.length)return null;vals.sort((a,b)=>a.amt-b.amt);return vals[0]}}
function prefill(t){{const m=pv(t.m);if(m&&m.cur=='$')return{{v:m.amt,src:'our verified monthly-billing entry rate'}};const a=pv(t.a);if(a&&a.cur=='$')return{{v:a.amt,src:'our verified per-month rate when billed yearly, shown as a monthly amount'}};return null}}
const MAXROWS=12;let rows=[];const ticks={{}};
function eff(r){{const amt=parseFloat(r.amt);if(isNaN(amt)||amt<0)return 0;return r.billing=='annual'?amt/12:amt}}
function sharePath(){{const q=rows.filter(r=>byS[r.s]).map(r=>r.s+':'+(r.amt===''?'':r.amt)+':'+r.billing).join(',');return '/subscription-audit.html'+(q?('?tools='+encodeURIComponent(q)):'')}}
function syncURL(){{history.replaceState(null,'',sharePath())}}
function renderTotals(){{const valid=rows.map(r=>({{r:r,t:byS[r.s],e:eff(r)}})).filter(x=>x.t&&x.e>0);const tot=valid.reduce((sum,x)=>sum+x.e,0);document.getElementById('a-total').innerHTML=rows.length?('<b>Current spend you told us: '+money(tot)+'/mo ('+money(tot*12)+'/yr)</b> across '+valid.length+' tool'+(valid.length==1?'':'s')+' with an amount. '+(rows.length-valid.length?((rows.length-valid.length)+' tool(s) still need an amount.'):'')):'No tools added yet. Add your first paid tool above — it takes about a minute.';return{{valid:valid,tot:tot}}}}
function renderRows(focusSlug){{const wrap=document.getElementById('a-rows');
if(!rows.length){{wrap.innerHTML='<p class="small">Nothing added yet — your tools will appear here as editable rows.</p>';renderTotals();return}}
wrap.innerHTML=rows.map((r,i)=>{{const t=byS[r.s];const pf=prefill(t);const e=eff(r);
return `<article class="arow" data-row="${{r.s}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3 style="margin:0"><a href="${{t.u}}">${{X(t.n)}}</a></h3><p class="small" style="margin:0">Main job: ${{X(t.cl)}}</p></div></div><p class="price">${{X(t.p)}}</p><p class="small">${{X(t.f)}}<br>Our listed price checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a> · <a href="${{t.u}}">Tool page</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=monthly">Cost calculator</a></p><div class="rgrid"><div><label for="amt-${{r.s}}">What you pay for ${{X(t.n)}}</label><input type="number" id="amt-${{r.s}}" data-amt="${{r.s}}" min="0" step="0.01" inputmode="decimal" value="${{X(r.amt)}}" placeholder="Tell us what you pay"><p class="small" style="margin:6px 0 0">${{pf?('Prefilled with '+pf.src+' ('+money(pf.v)+'/mo) — edit it, your plan may differ. This is <b>what you told us</b> once you change it.'):'No verified USD entry rate in our table, so nothing is prefilled — tell us what you pay.'}}</p></div><div><label for="bill-${{r.s}}">That amount is…</label><select id="bill-${{r.s}}" data-bill="${{r.s}}"><option value="monthly"${{r.billing=='monthly'?' selected':''}}>Per month</option><option value="annual"${{r.billing=='annual'?' selected':''}}>Per year (we show it ÷ 12)</option></select><p class="small" style="margin:6px 0 0" data-eff="${{r.s}}">${{e?('Counts as <b>'+money(e)+'/mo</b> in your total'+(r.billing=='annual'?' ('+money(parseFloat(r.amt)||0)+'/yr ÷ 12)':'')):'Add an amount to include this tool.'}}</p></div><div><label aria-hidden="true">&nbsp;</label><button type="button" class="bbtn" data-remove="${{r.s}}" aria-label="Remove ${{X(t.n)}} from your audit">Remove ${{X(t.n)}}</button></div></div></article>`}}).join('');
wrap.querySelectorAll('[data-amt]').forEach(inp=>inp.addEventListener('input',()=>{{const r=rows.find(x=>x.s==inp.dataset.amt);if(r){{r.amt=inp.value;const t=byS[r.s];const el=wrap.querySelector('[data-eff="'+r.s+'"]');const e=eff(r);if(el)el.innerHTML=e?('Counts as <b>'+money(e)+'/mo</b> in your total'+(r.billing=='annual'?' ('+money(parseFloat(r.amt)||0)+'/yr ÷ 12)':'')):'Add an amount to include this tool.';renderTotals();renderResults(false);syncURL()}}}}));
wrap.querySelectorAll('[data-bill]').forEach(sel=>sel.addEventListener('change',()=>{{const r=rows.find(x=>x.s==sel.dataset.bill);if(r){{r.billing=sel.value;renderRows(r.s);renderResults(false);syncURL();const f=document.getElementById('bill-'+r.s);if(f)f.focus()}}}}));
wrap.querySelectorAll('[data-remove]').forEach(b=>b.addEventListener('click',()=>{{rows=rows.filter(x=>x.s!=b.dataset.remove);delete ticks[b.dataset.remove];renderRows();renderResults(false);syncURL();document.getElementById('a-status').textContent=byS[b.dataset.remove].n+' removed.';document.getElementById('a-select').focus()}}));
renderTotals();
if(focusSlug){{const f=document.getElementById('amt-'+focusSlug);if(f){{f.focus();f.select()}}}}}}
function audit(){{const info=renderTotals();const valid=info.valid;
const act={{}}; /* slug -> {{kind,save,reason,alt,keeper,catName}} */
/* 1) overlap = 2+ tools with the same MAIN job (capability), not just the same broad category */
const byCap={{}};valid.forEach(x=>{{(byCap[x.t.cap]=byCap[x.t.cap]||[]).push(x)}});
Object.keys(byCap).forEach(cap=>{{const group=byCap[cap];if(group.length<2)return;const job=group[0].t.cl;
const bvk=group.find(x=>x.t.cats.some(c=>c.best==x.t.s));let keeper=bvk||group.slice().sort((a,b)=>(a.e-b.e)||a.t.n.localeCompare(b.t.n))[0];
const whyKeeper=bvk?('it is a ToolPick Best Value pick ('+keeper.t.cats.filter(c=>c.best==keeper.t.s).map(c=>c.name).join(', ')+')'):('it costs you the least of these ('+money(keeper.e)+'/mo, from what you told us)');
group.forEach(x=>{{if(x.t.s!=keeper.t.s&&!act[x.t.s])act[x.t.s]={{kind:'cancel',save:x.e,keeper:keeper.t,catName:job,reason:'You told us you pay for '+group.length+' tools that do the same main job ('+job+': '+group.map(y=>y.t.n).join(', ')+'). Keep '+keeper.t.n+' — '+whyKeeper+'. Consider cancelling '+x.t.n+' instead of paying for both.'}}}})}});
/* 2-4) per tool */
valid.forEach(x=>{{const t=x.t;if(act[t.s])return;
if(t.fr){{act[t.s]={{kind:'free',save:x.e,reason:t.n+' itself has a verified real free plan: '+t.f+'. Try the free tier first — if the free plan covers you, you could stop paying. Check its limits on the official pricing page (we do not state limits we have not verified).'}};return}}
const B=x.r.billing=='annual'?'ma':'mm',BL=x.r.billing=='annual'?'billed-yearly':'monthly';
let bestAlt=null;t.al.forEach(k=>{{const alt=byS[k];if(!alt)return;const v=alt[B];if(v==null||v>=x.e)return;if(!bestAlt||v<bestAlt.v||(v==bestAlt.v&&alt.n<bestAlt.alt.n))bestAlt={{alt:alt,v:v}}}});
if(bestAlt){{const tn=(!!bestAlt.alt.lt)!=(!!t.lt)?' Different tier: compare features before switching'+(bestAlt.alt.lt?' ('+bestAlt.alt.lt+').':(t.lt?' ('+t.lt+').':'.')):'';act[t.s]={{kind:'switch',save:Math.round((x.e-bestAlt.v)*100)/100,alt:bestAlt.alt,reason:bestAlt.alt.n+' does the same main job ('+t.cl+') and its cheapest '+BL+' plan we checked is '+money(bestAlt.v)+'/mo (checked '+bestAlt.alt.k+'), lower than the '+money(x.e)+'/mo you told us you pay for '+t.n+' on '+BL+' billing.'+tn+' We count only the difference as potential saving.'}};return}}
act[t.s]={{kind:'keep',save:0,reason:'No like-for-like cheaper option checked: no overlap with your other tools, no real free plan on '+t.n+' itself, and no tool that does the same main job ('+t.cl+') has a cheaper '+(x.r.billing=='annual'?'billed-yearly':'monthly')+' price than what you told us. On verified data, keep it.'+(t.fa&&byS[t.fa]?' Free option that does the same job: '+byS[t.fa].n+' ('+byS[t.fa].f+').':'')}}}});
return{{valid:valid,tot:info.tot,act:act}}}}
function renderResults(scroll=false){{const out=document.getElementById('a-out');const res=audit();const valid=res.valid;
if(!rows.length){{out.innerHTML='<div class="pick"><b>No tools added yet.</b><p class="small" style="margin-bottom:0">Add the tools you pay for above, check the amounts, and your checklist will appear here.</p></div>';return}}
if(!valid.length){{out.innerHTML='<div class="pick"><b>Add what you pay to finish the audit.</b><p class="small" style="margin-bottom:0">You added '+rows.length+' tool'+(rows.length==1?'':'s')+', but none has an amount yet, so we cannot work out spend or savings and we will not guess either.</p></div>';return}}
const items=valid.map(x=>({{x:x,a:res.act[x.t.s]||{{kind:'keep',save:0,reason:''}}}})).sort((a,b)=>(b.a.save-a.a.save)||a.x.t.n.localeCompare(b.x.t.n));
const potential=items.reduce((sum,i)=>sum+i.a.save,0);
const labels={{cancel:'CONSIDER CANCELLING',free:'TRY FREE TIER',switch:'SWITCH TO CHECK',keep:'KEEP'}};
let h='';
if(potential>0){{h+=`<div class="pick"><b>Potential saving: ${{money(potential)}}/mo (${{money(potential*12)}}/yr)</b> — if you act on every suggestion below. <span class="small">Current spend you told us: ${{money(res.tot)}}/mo (${{money(res.tot*12)}}/yr). Each tool is counted once only. Tick or untick suggestions to build your own plan.</span><p class="small" id="a-plan" aria-live="polite" style="margin:8px 0 0"></p></div>`}}
else{{h+=`<div class="pick"><b>No obvious waste found on verified data.</b><p class="small" style="margin-bottom:0">You told us you pay ${{money(res.tot)}}/mo (${{money(res.tot*12)}}/yr) across ${{valid.length}} tool${{valid.length==1?'':'s'}}, and no tool overlaps in its category, has a verified real free plan to fall back on, or has a cheaper verified free-plan alternative in our data. We are not inventing a saving — keep what you have, and re-check when prices change.</p></div>`}}
h+=items.map(i=>{{const t=i.x.t,a=i.a;const tickable=a.kind!='keep';
if(!(t.s in ticks))ticks[t.s]=true;
const extra=a.kind=='cancel'&&a.keeper?`<p class="small"><a href="/compare-builder.html?tools=${{t.s}},${{a.keeper.s}}">Compare ${{X(t.n)}} with ${{X(a.keeper.n)}} (the one to keep) →</a> · <a href="${{a.keeper.u}}">${{X(a.keeper.n)}} tool page</a></p>`:(a.kind=='switch'&&a.alt?`<p class="small"><a href="${{a.alt.u}}">See ${{X(a.alt.n)}} →</a> · <a href="/compare-builder.html?tools=${{t.s}},${{a.alt.s}}">Compare ${{X(t.n)}} with ${{X(a.alt.n)}} →</a> · <a href="${{X(a.alt.pr)}}" rel="noopener" target="_blank">${{X(a.alt.n)}} official pricing</a></p>`:'');
return `<article class="card ares${{a.save>0?' save':''}}" style="margin:12px 0"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges"><span class="badge ${{a.kind=='keep'?'b-rank':'b-best'}}">${{labels[a.kind]}}</span>${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3 style="margin:0"><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p class="small">You told us: <b>${{money(i.x.e)}}/mo</b>${{i.x.r.billing=='annual'?' (from '+money(parseFloat(i.x.r.amt)||0)+'/yr ÷ 12)':''}} · Our listed verified price: ${{X(t.p)}} (checked ${{t.k}}) · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p><p>${{X(a.reason)}}</p><p><b>Potential saving from this one tool: ${{money(a.save)}}/mo</b>${{a.kind=='free'?' if the free plan covers you — check its limits on the official page':a.kind=='switch'?' (difference to the alternative\\u2019s verified entry price only)':a.kind=='cancel'?' (the full amount you told us, counted once)':''}}</p>${{extra}}<p class="small"><a href="${{t.u}}">Tool page →</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=monthly">What will ${{X(t.n)}} really cost? →</a></p>${{tickable?`<label style="display:flex;gap:10px;align-items:flex-start;min-height:44px"><input type="checkbox" data-tick="${{t.s}}" data-save="${{a.save}}" ${{ticks[t.s]?'checked':''}} style="margin-top:4px"> <span>Count this in my plan — I will act on this suggestion (${{money(a.save)}}/mo)</span></label>`:'<p class="small">No saving counted for Keep.</p>'}}</article>`}}).join('');
const keepers=items.filter(i=>i.a.kind=='keep'||i.a.kind=='free').map(i=>i.x.t.s);const alts=items.filter(i=>i.a.kind=='switch'&&i.a.alt).map(i=>i.a.alt.s);const comp=[...new Set(keepers.concat(alts))].slice(0,3);
if(comp.length>=2)h+=`<p><a class="btn" href="/compare-builder.html?tools=${{comp.join(',')}}">Compare your keepers &amp; suggested switches →</a></p>`;
out.innerHTML=h;
function plan(){{let sum=0;out.querySelectorAll('[data-tick]').forEach(cb=>{{ticks[cb.dataset.tick]=cb.checked;if(cb.checked)sum+=parseFloat(cb.dataset.save)||0}});const el=document.getElementById('a-plan');if(el)el.innerHTML='<b>Your plan saves '+money(sum)+'/mo ('+money(sum*12)+'/yr)</b> from the suggestions you ticked.'}}
out.querySelectorAll('[data-tick]').forEach(cb=>cb.addEventListener('change',plan));plan();
if(scroll)out.scrollIntoView({{behavior:'smooth',block:'start'}})}}
document.getElementById('a-add').addEventListener('click',()=>{{const sel=document.getElementById('a-select');const st=document.getElementById('a-status');if(!sel.value){{st.textContent='Select a tool first, then Add tool.';sel.focus();return}}if(rows.some(r=>r.s==sel.value)){{st.textContent=byS[sel.value].n+' is already in your audit — edit its amount below.';const f=document.getElementById('amt-'+sel.value);if(f){{f.focus();f.select()}}return}}if(rows.length>=MAXROWS){{st.textContent='That is the maximum of '+MAXROWS+' tools for one audit. Remove one to add another.';return}}const t=byS[sel.value];const pf=prefill(t);rows.push({{s:t.s,amt:pf?String(pf.v):'',billing:'monthly'}});renderRows(t.s);renderResults(false);syncURL();st.textContent=t.n+' added'+(pf?(' at our verified entry price — edit it if your plan differs.'):' — tell us what you pay.')}});
document.getElementById('a-search').addEventListener('input',ev=>{{const q=ev.target.value.toLowerCase();const sel=document.getElementById('a-select');[...sel.options].forEach((o,i)=>{{if(i==0)return;o.hidden=q?!o.textContent.toLowerCase().includes(q):false}});const first=[...sel.options].find(o=>!o.hidden&&o.value);if(first&&q)sel.value=first.value}});
document.getElementById('a-run').addEventListener('click',()=>{{renderResults(true);document.getElementById('a-status').textContent=rows.length?'Audit updated below.':'Add a tool first.'}});
document.getElementById('a-clear').addEventListener('click',()=>{{rows=[];Object.keys(ticks).forEach(k=>delete ticks[k]);renderRows();renderResults(false);syncURL();document.getElementById('a-status').textContent='Cleared. Add tools to start again.';document.getElementById('a-select').focus()}});
document.getElementById('a-copy').addEventListener('click',async()=>{{const st=document.getElementById('a-status');if(!rows.length){{st.textContent='Add at least one tool before copying a share link.';return}}const url=location.origin+sharePath();try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
(function init(){{const q=new URLSearchParams(location.search).get('tools');if(q){{q.split(',').map(x=>x.trim()).filter(Boolean).slice(0,MAXROWS).forEach(part=>{{const bits=part.split(':');const t=byS[bits[0]];if(!t||rows.some(r=>r.s==t.s))return;rows.push({{s:t.s,amt:bits[1]&&!isNaN(parseFloat(bits[1]))?bits[1]:(prefill(t)?String(prefill(t).v):''),billing:bits[2]=='annual'?'annual':'monthly'}})}})}}renderRows();renderResults(false);}})();
</script>"""
page("/subscription-audit.html", "AI Subscription Audit — Keep, Cancel or Try the Free Tier in 60 Seconds | ToolPick", "List the AI tools you pay for and get a keep, consider cancelling, try the free tier or switch checklist with a potential saving counted once per tool, from verified ToolPick prices only. Runs in your browser.", audit_body,
     [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick AI Subscription Audit","url":BASE+"/subscription-audit.html","description":"60-second audit of paid AI subscriptions using verified prices, returning one action per tool with potential savings counted once."}, crumbs([("ToolPick","/"),("Subscription Audit","/subscription-audit.html")])])


# --- Pay less for the same job (v17) ---
# One tool in -> cheapest verified same-category plan, best real free option, saving vs what you pay.
# Only verified PRICE_TABLE USD numbers are ranked/summed; 'check site' and non-USD are never ranked.
PAYLESS_PATH = "/pay-less.html"
PAYLESS_DATE = "2026-10-20"
_pmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _pmap:
            _pmap[_k] = dict(s=_k, n=_t["name"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED), u=turl(_t["name"]),
                             dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"], fr=realfree(_t), cats=[], bc=[])
        if _c["id"] not in _pmap[_k]["cats"]: _pmap[_k]["cats"].append(_c["id"])
        if _c["best"] == _t["name"]: _pmap[_k]["bc"].append(_c["id"])
for _v in _pmap.values():
    _v["al"] = [slug(x["name"]) for x in samejob(_v["n"])]; _fa = free_alt(_v["n"]); _v["fa"] = slug(_fa["name"]) if _fa else None
    _v["cap"] = cap_label(_v["n"]); _v["lt"] = _v["n"] in LOWER_TIER
PCATS = json.dumps({c["id"]: c["name"] for c in CATEGORIES})
PDATA = json.dumps(sorted(_pmap.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
POPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])}</option>' for v in sorted(_pmap.values(), key=lambda x: x["n"].lower()))
_pl_js = r"""<script>const PD=__PD__,PC=__PC__;const byS={};PD.forEach(t=>byS[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const money=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))};
const usd=v=>typeof v=='number'?v:null;
const BL={m:'monthly',a:'yearly'};
function priceOn(t,B){return usd(t[B])}
function plan(v,B){return money(v)+'/mo'+(B=='a'?' (paid yearly)':' (paid monthly)')}
function cheapOn(alts,B){return alts.map(x=>({x,v:priceOn(x,B)})).filter(z=>z.v!=null).sort((p,q)=>p.v-q.v||p.x.n.localeCompare(q.x.n))[0]||null}
function src(t){return `<span class="small">Checked ${X(t.k)} · <a href="${X(t.pr)}" rel="noopener" target="_blank">official pricing page</a></span>`}
const out=()=>document.getElementById('pl-out');
const billEl=()=>document.getElementById('pl-bill');
function share(s,amt){const q=new URLSearchParams();if(s)q.set('tool',s);if(s&&amt!=='')q.set('pay',amt);if(s&&billEl().value=='a')q.set('bill','yearly');history.replaceState(null,'','/pay-less.html'+(q.toString()?'?'+q:''))}
function pickTool(s,keepAmt,billQ){const t=byS[s],a=document.getElementById('pl-pay'),bw=document.getElementById('pl-billwrap');if(!t){a.value='';bw.hidden=true;return}
const hasM=usd(t.m)!=null,hasA=usd(t.a)!=null;let B=billQ||(hasM?'m':(hasA?'a':'m'));if(B=='a'&&!hasA&&hasM&&!billQ)B='m';billEl().value=B;bw.hidden=!(hasM&&hasA)&&!billQ;
if(!keepAmt){const v=usd(t[B]);a.value=v==null?'':String(v)}note(t)}
function note(t){const B=billEl().value,v=usd(t[B]);document.getElementById('pl-paynote').textContent=v!=null?('We filled in '+t.n+'\u2019s cheapest plan we checked, '+(B=='a'?'paid yearly (shown per month)':'paid monthly')+'. Change it if you pay something else.'):'We could not check a '+BL[B]+' dollar price for '+t.n+', so type what you pay per month.'}
function run(){const s=document.getElementById('pl-tool').value,raw=document.getElementById('pl-pay').value.trim(),o=out();share(s,raw);
if(!s){o.innerHTML='<div class="pick" role="status"><b>Pick the tool you pay for to see your answer.</b><p class="small" style="margin-bottom:0">Try an example: <a href="/pay-less.html?tool=descript&amp;pay=24">Descript at $24 a month</a> · <a href="/pay-less.html?tool=descript&amp;pay=16&amp;bill=yearly">Descript at $16 a month, paid yearly</a> · <a href="/pay-less.html?tool=elevenlabs&amp;pay=6">ElevenLabs at $6</a></p></div>';return}
const t=byS[s];const B=billEl().value,O=B=='m'?'a':'m';const pay=raw===''?null:parseFloat(raw);const bad=raw!==''&&(isNaN(pay)||pay<0);
const alts=t.al.map(k=>byS[k]).filter(Boolean);const TN=x=>x&&x.lt!=t.lt?' <span class="small"><b>Different tier: compare features before switching.</b></span>':'';
const cheap=cheapOn(alts,B);const cheapO=cheapOn(alts,O);
const free=t.fa?byS[t.fa]:null;
const cats=t.cap;let h='';const per=B=='a'?'/mo paid yearly':'/mo';
if(bad){o.innerHTML='<div class="pick" role="status"><b>Please type what you pay as a number, like 24 or 19.99.</b></div>';return}
if(pay==null){h+=`<div class="pick" role="status"><b>Type what you pay for ${X(t.n)} per month to see your saving.</b> The options below still show what we checked.</div>`}
const cheaper=cheap&&pay!=null&&cheap.v<pay,ownFree=t.fr;
if(pay!=null){if(cheaper)h+=`<div class="pick pl-ans"><span class="badge b-best">YOU CAN PAY LESS</span> <b>${X(cheap.x.n)} costs ${plan(cheap.v,B)}</b> — ${money(pay-cheap.v)}/mo less than the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''} (${money((pay-cheap.v)*12)}/yr). Both prices are ${BL[B]} billing.${TN(cheap.x)}${ownFree?` Or try ${X(t.n)}\u2019s own free plan first.`:''}</div>`;
else if(ownFree)h+=`<div class="pick pl-ans"><span class="badge b-free">TRY YOUR FREE PLAN</span> <b>${alts.length?'No cheaper '+BL[B]+' plan we checked':'No like-for-like cheaper option checked'} — but ${X(t.n)} has its own free plan.</b> If it covers what you do, you could pay $0 and save ${money(pay)}/mo (${money(pay*12)}/yr).<p class="small" style="margin:6px 0 0">Free plan: ${X(t.f)} · ${src(t)}</p></div>`;
else h+=`<div class="pick pl-ans"><span class="badge b-rank">STAY PUT</span> <b>${alts.length?'Nothing cheaper that we checked.':'No like-for-like cheaper option checked.'}</b> No other tool that does the same main job (${X(cats)}) in our list has a checked ${BL[B]} price below the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''} for ${X(t.n)}, so keep it.${free?` The only way to pay less is a free plan with limits, like ${X(free.n)}\u2019s below.`:''}</div>`}
const card=(lab,cls,x,body)=>`<article class="card" style="margin:12px 0"><div class="badges"><span class="badge ${cls}">${lab}</span></div><h3 style="margin:4px 0"><a href="${x.u}">${X(x.n)}</a></h3>${body}<p class="small">${src(x)} · <a href="/compare-builder.html?tools=${t.s},${x.s}">Compare with ${X(t.n)} →</a></p></article>`;
h+=`<h2>Cheapest plan we checked (${BL[B]} billing)</h2>`;
h+=cheap?card(cheaper?'CHEAPER':'CHEAPEST OTHER','b-best',cheap.x,`<p class="price">${plan(cheap.v,B)}</p><p class="small">${X(cheap.x.p)}</p>${TN(cheap.x)}<p>${pay==null?'Type what you pay to see the difference.':cheaper?`You would save <b>${money(pay-cheap.v)}/mo</b> (<b>${money((pay-cheap.v)*12)}/yr</b>) compared with the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''}.`:`This is not cheaper than the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''}, so it would not save you money.`}</p>`):`<p>${alts.length?`We have no checked ${BL[B]} dollar price for another tool that does the same main job (${X(cats)}).`:'No like-for-like cheaper option checked: no other tool in our list does the same main job ('+X(cats)+').'}</p>`;
const tO=usd(t[O]);if(tO!=null&&cheapO){const d=Math.round((tO-cheapO.v)*100)/100;h+=`<div class="bnote"><p style="margin:0"><b>On ${BL[O]} billing instead:</b> ${X(t.n)} is ${plan(tO,O)} and the cheapest other is ${X(cheapO.x.n)} at ${plan(cheapO.v,O)} — ${d>0?`${money(d)}/mo less (${money(d*12)}/yr)`:'not cheaper'}. We only compare ${BL[O]} with ${BL[O]}.</p></div>`}
h+='<h2>Best free option</h2>';
h+=free?card('FREE PLAN','b-free',free,`<p>${X(free.f)}</p><p>${pay==null?'':`If the free plan covers you, you would save <b>${money(pay)}/mo</b> (<b>${money(pay*12)}/yr</b>). Free plans have limits — check them on the official page.`}</p>`):`<p>No other tool that does the same main job (${X(cats)}) has a real free plan (free trials and one-time credits do not count).</p>`;
h+=`<p class="small">What we compared against: <a href="${t.u}">${X(t.n)}</a> — ${X(t.p)} · ${src(t)}. Same job means the same main job (${X(cats)}), based on what each tool’s official site says it does; features differ, so check the tool fits before you switch. <a href="/cost-calculator.html?tool=${t.s}&amp;seats=1&amp;billing=monthly">See the full cost of ${X(t.n)} →</a>${usd(t.m)!=null&&usd(t.a)!=null?` · <a href="/monthly-or-yearly.html?tool=${t.s}">Monthly or yearly for ${X(t.n)}? →</a>`:''}</p>`;
o.innerHTML=h}
document.getElementById('pl-tool').addEventListener('change',e=>{pickTool(e.target.value,false);run()});
document.getElementById('pl-pay').addEventListener('input',run);document.getElementById('pl-bill').addEventListener('change',()=>{const t=byS[document.getElementById('pl-tool').value];if(t){const v=usd(t[billEl().value]);if(v!=null)document.getElementById('pl-pay').value=String(v);note(t)}run()});
document.getElementById('pl-form').addEventListener('submit',e=>{e.preventDefault();run();out().focus()});
document.getElementById('pl-copy').addEventListener('click',async()=>{const st=document.getElementById('pl-status');const u=location.href;try{await navigator.clipboard.writeText(u);st.textContent='Link copied.'}catch(err){st.textContent='Copy this link: '+u}});
(function(){const q=new URLSearchParams(location.search),s=q.get('tool'),p=q.get('pay');const sel=document.getElementById('pl-tool');if(s&&byS[s]){sel.value=s;pickTool(s,p!=null,q.get('bill')=='yearly'?'a':(q.get('bill')=='monthly'?'m':null));if(p!=null)document.getElementById('pl-pay').value=p}else if(s){document.getElementById('pl-status').textContent='We do not have a tool called "'+s+'". Pick one from the list.'}run()})();
</script>"""
payless_body = f"""<section class="hero"><h1>Pay less for the same job</h1><p class="tag">Pick the AI tool you pay for. We will show you the cheapest plan we checked for the same kind of tool, the best free option, and how much you could save.</p></section>
<form class="builder" id="pl-form"><div class="aform"><div><label for="pl-tool">The tool you pay for</label><select id="pl-tool"><option value="">Choose a tool…</option>{POPTS}</select></div><div><label for="pl-pay">What you pay per month ($)</label><input type="number" id="pl-pay" min="0" step="0.01" inputmode="decimal" placeholder="e.g. 20"><p class="small" id="pl-paynote" style="margin:6px 0 0"></p></div><div id="pl-billwrap" hidden><label for="pl-bill">How you pay</label><select id="pl-bill"><option value="m">Monthly</option><option value="a">Yearly (price per month)</option></select></div><button type="submit" class="bbtn primary">Show my answer</button></div><p class="small" style="margin:10px 0 0"><button type="button" class="bbtn" id="pl-copy">Copy link to this answer</button> <span id="pl-status" role="status"></span></p></form>
<div id="pl-out" tabindex="-1" aria-live="polite"></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How we work it out</h2><p class="small" style="margin:0">“Same job” means the same main job — the tool’s first capability tag, taken from what its official site says it does (for example text to speech, edit by transcript, meeting notes). A broad category is not enough. “Cheapest plan we checked” is the lowest dollar price we copied from each tool’s official pricing page, with the date we checked it. Tools whose price we could not check, or that only list non-dollar prices, are never ranked. A “free option” must be a real free plan — free trials and one-time credits do not count. Your saving is what you pay minus the other tool’s price on the same billing — monthly against monthly, yearly against yearly, never mixed. Everything runs in your browser; nothing is sent to us.</p><p class="small" style="margin:12px 0 0"><a href="/free.html">Can I do it for free? →</a> · <a href="/monthly-or-yearly.html">Monthly or yearly?</a> · <a href="/save-money.html">Save money hub</a> · Paying for several tools? <a href="/subscription-audit.html">Run the Subscription Audit →</a> · <a href="/tools.html">Browse all tools</a> · <a href="/compare-builder.html">Compare builder</a></p></div>
""" + _pl_js.replace("__PD__", PDATA).replace("__PC__", PCATS)
page(PAYLESS_PATH, "Pay Less for the Same AI Tool — Cheaper & Free Alternatives, Checked Prices | ToolPick",
     "Pick the AI tool you pay for and see the cheapest plan we checked for the same job, the best free option, and your monthly and yearly saving. Official prices with checked dates.", payless_body,
     [{"@context":"https://schema.org","@type":"WebApplication","name":"ToolPick Pay less for the same job","url":BASE+PAYLESS_PATH,"applicationCategory":"FinanceApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":"Find a cheaper or free AI tool for the same job using prices checked on official pricing pages."}, crumbs([("ToolPick","/"),("Pay less","/pay-less.html")])])


# --- Monthly or yearly? (v19) ---
# Only tools whose PRICE_TABLE has BOTH a numeric USD monthly price and a numeric USD per-month-billed-yearly price
# for the same (cheapest paid) plan. Yearly total = yearly-per-month x 12; break-even months = ceil(yearly total / monthly).
import math as _math
MY_PATH = "/monthly-or-yearly.html"; MY_DATE = "2026-10-20"
_mym = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k in _mym: continue
        _m, _a = _t["monthly"], _t["annual"]
        _both = isinstance(_m, (int, float)) and isinstance(_a, (int, float))
        _r = dict(s=_k, n=_t["name"], p=_t["price"], k=_t.get("checked", CHECKED), u=turl(_t["name"]), pr=_t["pricing"], dm=dom(_t["url"]), both=_both,
                  m=_m if isinstance(_m, (int, float)) else None, a=_a if isinstance(_a, (int, float)) else None)
        if _both:
            _yt = round(_a * 12, 2); _r.update(yt=_yt, sv=round(_m * 12 - _yt, 2), pct=round((_m - _a) / _m * 100), be=_math.ceil(round(_yt / _m, 6)))
        _mym[_k] = _r
MY_BOTH = {k for k, v in _mym.items() if v["both"]}
_mylist = sorted([v for v in _mym.values() if v["both"] and v["sv"] > 0], key=lambda v: (-v["pct"], -v["sv"], v["n"].lower()))
_seen_dm = set(); _mylist = [v for v in _mylist if not (v["dm"] in _seen_dm or _seen_dm.add(v["dm"]))]
def _mm(v): r = round(v, 2); return "$" + (str(int(r)) if r == int(r) else f"{r:.2f}")
MYDATA = json.dumps(sorted(_mym.values(), key=lambda x: x["n"].lower())).replace("</", "<\\/")
MYOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])}</option>' for v in sorted(_mym.values(), key=lambda x: x["n"].lower()))
_myrows = "".join(f'<tr><td><a href="{MY_PATH}?tool={v["s"]}">{e(v["n"])}</a></td><td>{_mm(v["m"])}/mo</td><td>{_mm(v["a"])}/mo ({_mm(v["yt"])} upfront)</td><td><b>{v["pct"]}%</b> · {_mm(v["sv"])}/yr</td><td>{v["be"]} months</td><td class="small">{v["k"]} · <a href="{e(v["pr"])}" rel="noopener" target="_blank">official</a></td></tr>' for v in _mylist)
_my_js = r"""<script>const MY=__D__;const byS={};MY.forEach(t=>byS[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const money=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))};
const src=t=>`Checked ${X(t.k)} · <a href="${X(t.pr)}" rel="noopener" target="_blank">official pricing page</a>`;
function run(){const s=document.getElementById('my-tool').value,o=document.getElementById('my-out');history.replaceState(null,'','/monthly-or-yearly.html'+(s?'?tool='+s:''));
if(!s){o.innerHTML='<div class="pick" role="status"><b>Pick the tool you pay for to see your answer.</b> Or look at the biggest yearly discounts below.</div>';return}
const t=byS[s];let h='';
if(!t.both){o.innerHTML=`<div class="pick" role="status"><span class="badge b-rank">ONE PRICE ONLY</span> <b>${t.m==null&&t.a==null?`We don’t have a checked US-dollar price for ${X(t.n)}`:`We only checked one price for ${X(t.n)}`}, so we can’t compare monthly and yearly.</b><p class="small" style="margin:6px 0 0">${t.m!=null?'Monthly: '+money(t.m)+'/mo. ':''}${t.a!=null?'Billed yearly: '+money(t.a)+'/mo. ':''}What we listed: ${X(t.p)}. See the official page for both prices. ${src(t)} · <a href="${t.u}">${X(t.n)} page</a></p></div>`;return}
if(t.sv<=0){o.innerHTML=`<div class="pick" role="status"><span class="badge b-rank">STAY MONTHLY</span> <b>${X(t.n)} costs the same or more when paid yearly</b> (${money(t.m)}/mo monthly vs ${money(t.a)}/mo yearly), so stay monthly. <p class="small" style="margin:6px 0 0">${src(t)}</p></div>`;return}
h+=`<div class="pick pl-ans"><span class="badge b-best">YEARLY SAVES ${t.pct}%</span> <b>Yearly saves ${money(t.sv)} if you’ll use ${X(t.n)} for 12 months. If you might stop before month ${t.be}, stay monthly.</b></div>
<article class="card" style="margin:12px 0"><h2 style="margin:0 0 6px;font-size:1.1rem"><a href="${t.u}">${X(t.n)}</a> — cheapest paid plan</h2><div class="tw"><table><tr><th>Pay monthly</th><td>${money(t.m)}/mo · ${money(t.m*12)} over 12 months</td></tr><tr><th>Pay yearly</th><td>${money(t.a)}/mo · <b>${money(t.yt)} upfront</b></td></tr><tr><th>Yearly saving</th><td><b>${money(t.sv)}</b> (${t.pct}%)</td></tr><tr><th>Break-even</th><td>${t.be} months — paying yearly only wins if you keep it at least ${t.be} months (${money(t.yt)} ÷ ${money(t.m)} = ${(t.yt/t.m).toFixed(2)}, rounded up)</td></tr></table></div>
<p class="small">All plans we listed: ${X(t.p)}</p><p class="small">${src(t)} · <a href="/pay-less.html?tool=${t.s}&amp;pay=${t.m}">Pay less than ${X(t.n)}? →</a> · <a href="/cost-calculator.html?tool=${t.s}&amp;seats=1&amp;billing=annual">Full cost →</a></p></article>`;
o.innerHTML=h}
document.getElementById('my-tool').addEventListener('change',run);document.getElementById('my-form').addEventListener('submit',e=>{e.preventDefault();run();document.getElementById('my-out').focus()});
(function(){const q=new URLSearchParams(location.search).get('tool'),sel=document.getElementById('my-tool');if(q&&byS[q])sel.value=q;else if(q)document.getElementById('my-status').textContent='We do not have a tool called "'+q+'". Pick one from the list.';run()})();</script>"""
my_body = f"""<section class="hero"><h1>Monthly or yearly?</h1><p class="tag">Pick the AI tool you pay for. We’ll show the monthly price, the yearly price, how much yearly saves, what you pay upfront, and how many months you need to keep it for yearly to be worth it.</p></section>
<form class="builder" id="my-form"><div class="aform"><div><label for="my-tool">The tool you pay for</label><select id="my-tool"><option value="">Choose a tool…</option>{MYOPTS}</select></div><button type="submit" class="bbtn primary">Show my answer</button></div><p class="small" id="my-status" role="status" style="margin:8px 0 0"></p></form>
<div id="my-out" tabindex="-1" aria-live="polite"></div>
<h2>Biggest yearly discounts we checked</h2><p class="small">{len(_mylist)} tools where we checked both the monthly and the billed-yearly price of the cheapest paid plan, biggest discount first.</p>
<div class="tw"><table><tr><th>Tool</th><th>Monthly</th><th>Billed yearly</th><th>Yearly saves</th><th>Break-even</th><th>Checked</th></tr>{_myrows}</table></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How we work it out</h2><p class="small" style="margin:0">We use the cheapest paid plan’s monthly price and its per-month price when billed yearly, both copied from the official pricing page with the date we checked. Upfront cost = yearly per-month price × 12. Yearly saving = monthly price × 12 − upfront cost. Break-even = upfront cost ÷ monthly price, rounded up: if you might cancel before that month, monthly is cheaper. Tools where we only checked one of the two prices are not ranked. Other plans can have different discounts — check the official page.</p><p class="small" style="margin:12px 0 0"><a href="/pay-less.html">Pay less for the same job →</a> · <a href="/price-changes.html">AI price changes</a> · <a href="/cost-calculator.html">Cost calculator</a></p></div>
""" + _my_js.replace("__D__", MYDATA)
page(MY_PATH, "Monthly or Yearly? AI Tool Annual Discounts & Break-Even, Checked Prices | ToolPick",
     f"Should you pay monthly or yearly for your AI tool? See the yearly saving in $ and %, the upfront cost and break-even month for {len(_mylist)} AI tools, from official pricing pages.", my_body,
     [{"@context":"https://schema.org","@type":"WebApplication","name":"ToolPick Monthly or yearly?","url":BASE+MY_PATH,"applicationCategory":"FinanceApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},
      {"@context":"https://schema.org","@type":"ItemList","name":"Biggest yearly discounts on AI tools","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+v["u"],"name":f"{v['n']}: {v['pct']}% off yearly"} for i, v in enumerate(_mylist)]},
      crumbs([("ToolPick","/"),("Monthly or yearly?",MY_PATH)])])


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
<p class="small">Want a ready-made set? <a href="/stacks.html">AI starter stacks by role →</a> <a href="/best-ai-tools-for-students.html">Students</a> · <a href="/best-ai-tools-for-marketers.html">Marketers</a> · <a href="/best-ai-tools-for-developers.html">Developers</a> · <a href="/best-ai-tools-for-content-creators.html">Content creators</a> · <a href="/best-ai-tools-for-small-business.html">Small business</a> · <a href="/best-ai-tools-for-researchers.html">Researchers</a></p><p class="small">Paying for one tool? <a href="/pay-less.html">See if you can pay less for the same job →</a></p><p class="small">Already paying for some of these? <a href="/subscription-audit.html">Run the Subscription Audit →</a> · Found a shortlist? <a href="/help-me-choose.html">Help me choose in 5 steps →</a> · <a href="/cost-calculator.html">What will it really cost? →</a> Prices change — always confirm on the official pricing page linked on every card.</p>
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
    d = f"The top 3 AI tools for {job}: {', '.join(ranked)}. Prices from official pricing pages, each with its own checked date."
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
    alts = [x["name"] for x in samejob(name) if realfree(x)]
    if not alts: REDIRECTS[f"/free-alternative-to-{slug(name)}.html"] = turl(name); continue
    path = f"/free-alternative-to-{slug(name)}.html"; FREE_ALT_URLS.append((name, path))
    title = f"Free Alternatives to {name} ({CHECKED[:4]}) — {len(alts)} Options with Free Plans"
    d = f"{name} costs {t['price']}. Free alternatives with a verified free tier: {', '.join(alts[:5])}. Checked {t.get('checked', CHECKED)}."[:300]
    items = "".join(f"<li><h3><a href='{turl(a)}'>{e(a)}</a></h3><p>{e(find(a)['about'])}</p><p>🆓 {e(find(a)['free'])}</p><p class='price'>💲 Paid: {e(find(a)['price'])}</p><p class='small'>checked {find(a).get('checked', CHECKED)}</p></li>" for a in alts)
    body = f"""<h1>Free alternatives to {e(name)}</h1><p class="tag">{e(d)}</p><p><a href="{turl(name)}">{e(name)}</a>: {e(t['price'])}. Free tier: {e(t['free'])}.</p><ol>{items}</ol>
<p class="small">Only tools whose official pricing page showed a free plan are listed; each shows its own checked date.</p><p>See all <a href="/best-ai-{cats[0]['id']}-tools.html">AI {e(cats[0]['name'].lower())} tools</a>.</p>"""
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
UNDER = None
def _seo_card(t, cat, rank, best_name, lowest_name):
    en = _entry_num(t)
    is_best = t["name"] == best_name
    badges = (f"<span class='badge b-rank'>#{rank}</span>" if True else "") + ("<span class='badge b-best'>BEST VALUE</span>" if is_best else "") + ("<span class='badge b-free'>FREE PLAN</span>" if realfree(t) else "")
    reasons = []
    if is_best: reasons.append(f"ToolPick's Best Value pick for {cat['name']}")
    if lowest_name and t["name"] == lowest_name and en is not None: reasons.append(f"Lowest checked entry on this page: ${en:g}/mo" + (" billed yearly" if en != _num(t.get("monthly")) else " monthly"))
    if realfree(t): reasons.append("Has a verified real free plan (trials and one-time credits do not count)")
    if en is not None: reasons.append(f"Entry ${en:g}/mo " + ("monthly" if en == _num(t.get("monthly")) else "billed yearly"))
    else: reasons.append("No verified numeric entry rate in our price table")
    reason_txt = " · ".join(dict.fromkeys(reasons))
    _m, _a = _num(t.get("monthly")), _num(t.get("annual"))
    _bill = " · ".join(x for x in [f"{_usd(_m)}/mo monthly" if _m is not None else "", f"{_usd(_a)}/mo billed yearly" if _a is not None else ""] if x)
    entry_line = (f"Cheapest plan we checked: {_bill}" if en is not None else "Entry price not verified in our price table")
    if UNDER and en is not None:
        if _m is not None and _m < UNDER: entry_line += f" — under ${UNDER} on monthly billing"
        elif _a is not None and _a < UNDER: entry_line += f" — under ${UNDER} only when billed yearly" + (f" ({_usd(_m)}/mo if you pay monthly)" if _m is not None else " (no monthly price checked)")
    return f"""<article class="card{' best' if is_best else ''}"><div class="th">{logo(t)}<div><div class="badges">{badges}</div><h3><a href="{turl(t['name'])}">{e(t['name'])}</a></h3></div></div><p>{e(t['about'])}</p>
<p class="price">{e(t['price'])}</p><p class="small">{e(entry_line)}</p><p class="small">{e(t['free'])}</p><p class="small"><b>Why this pick:</b> {e(reason_txt)}.</p>
<p class="small meta">{e(cat['name'])} · checked {t.get('checked', CHECKED)} · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Official pricing page</a></p></article>"""
def _seo_table(rows_tools, cat):
    rows = ""
    for i, t in enumerate(rows_tools, 1):
        en = _entry_num(t)
        rows += f"<tr><td>{i}</td><td><a href='{turl(t['name'])}'>{e(t['name'])}</a>{' <span class=\"badge b-best\">BEST VALUE</span>' if t['name']==cat['best'] else ''}</td><td>{('$'+format(en,'g')+'/mo ' + ('monthly' if en == _num(t.get('monthly')) else 'billed yearly')) if en is not None else '—'}</td><td>{e(t['price'])}</td><td>{e(t['free'])}</td><td>{t.get('checked', CHECKED)}<br><a href=\"{e(t['pricing'])}\" rel=\"noopener\" target=\"_blank\">Pricing page</a></td></tr>"
    return f"<div class='tw'><table><caption class='small' style='text-align:left;padding:12px 16px'>Verified prices from official pricing pages. Confirm before buying.</caption><tr><th>#</th><th>Tool</th><th>Verified entry</th><th>All plans (as listed)</th><th>Free plan</th><th>Checked</th></tr>{rows}</table></div>"

SEO_URLS = []
for _target in SEO_FREE_ALT:
    _cats = tool_pages[_target]; _cat = _cats[0]; _tgt = find(_target)
    _alts = [x["name"] for x in samejob(_target) if realfree(x)]
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
UNDER = 20
_vcards = "".join(_seo_card(t, _vcat, i+1, _vbest, _vlowest) for i, t in enumerate(_video_under_sorted))
_vtop3 = ",".join(slug(t["name"]) for t in _video_under_sorted[:3])
_vyonly = [t for t in _video_under_sorted if not (_num(t.get("monthly")) is not None and _num(t["monthly"]) < 20)]
_vyl = ", ".join(f"{t['name']} (" + (f"{_usd(_num(t['monthly']))}/mo monthly, " if _num(t.get('monthly')) is not None else "no monthly price checked, ") + f"{_usd(_num(t['annual']))}/mo billed yearly)" for t in _vyonly)
_vqas = [
    ("Which of these are under $20 only when billed yearly?", (f"{_vyl}. On monthly billing they cost $20/mo or more (or have no checked monthly price)." if _vyonly else "None: every tool here is under $20 on monthly billing.")),
    ("What does “under $20” mean on this page?", "It means the tool's lowest verified entry rate in ToolPick's price table — the lower of its monthly rate and its per-month rate when billed yearly — is under $20/mo (less than $20, not $20 or less). Tools at exactly $20/mo or with no verified numeric entry rate are not included."),
    (f"What is the cheapest AI video tool under $20 here?", f"{_video_under_sorted[0]['name']} at ${_entry_num(_video_under_sorted[0]):g}/mo verified entry (checked {_video_under_sorted[0].get('checked', CHECKED)}): {_video_under_sorted[0]['price']}."),
    ("What is the Best Value pick among these video tools?", f"{_vcat['best']} is ToolPick's Best Value pick for video and carries the badge on this page. " + find(_vcat['best']).get('why','')),
]
_vfh, _vfl = faq(_vqas)
_vbody = f"""<h1>Best AI video tools under $20</h1><p class="tag">Every AI video tool on ToolPick whose verified entry price is <b>under $20/mo</b> — that means less than $20, using the lowest verified monthly or annual-billing rate in our price table. Sorted cheapest first.{(" Under $20 only when billed yearly: " + e(_vyl) + ".") if _vyonly else ""} Prices were copied from official pricing pages; each tool shows its checked date and pricing link.</p>
<p>Threshold stated plainly: a tool is included only if its verified entry rate is &lt; $20/mo. A tool listed at exactly $20/mo, or with no verified numeric entry rate (“check site”), is excluded — never guessed in. The Best Value badge follows ToolPick's existing rule: the category Best Value pick for video ({e(_vcat['best'])}) when it is on this list.</p>
<h2>Ranked cheapest first</h2><div class="grid">{_vcards}</div>{_seo_table(_video_under_sorted, _vcat)}
<p><a class="btn" href="/compare-builder.html?tools={_vtop3}">Compare the 3 cheapest side by side →</a></p>
<p><a href="/cost-calculator.html?category=video&amp;seats=1&amp;billing=monthly">What will video tools really cost? →</a> See true monthly and yearly costs by seats and billing in the cost calculator.</p>
<p>More: <a href="/best-ai-video-tools.html">best AI video tools</a> · <a href="/best-free-ai-video-tools.html">best free AI video tools</a> · <a href="/tools.html?category=video">browse all video tools in the directory</a> · <a href="/help-me-choose.html?category=video">help me choose a video tool</a></p>{_vfh}"""
UNDER = None
_vil = {"@context":"https://schema.org","@type":"ItemList","name":_vtitle,"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+turl(t["name"]),"name":t["name"]} for i,t in enumerate(_video_under_sorted)]}
page(SEO_VIDEO_PATH, _vtitle, _vd[:300], _vbody, [_vil, _vfl, crumbs([("ToolPick","/"),("Best AI video tools","/best-ai-video-tools.html"),("Best AI video tools under $20",SEO_VIDEO_PATH)])])
SEO_URLS.append(SEO_VIDEO_PATH)

# /free and best-free pages
FREE_LIST = [(c, t) for c in CATEGORIES for t in c["tools"] if hasfree(t, c)]
if FREE_V21:
    # --- Can I do it for free? (v20) — /free.html rebuilt as a one-path job picker ---
    # Top-pick rule (stated on page): the category's ToolPick Best Value pick if it has a real free plan;
    # otherwise the first tool in the category's existing free-alternatives order (c["free"]); otherwise the
    # first real-free tool in the category's listed order. Real free = realfree(): trials, one-time credits excluded.
    def _fr_top(c):
        L = [t for t in c["tools"] if realfree(t)]
        if not L: return None
        b = next((t for t in L if t["name"] == c["best"]), None)
        if b: return b, "it is ToolPick's Best Value pick for this job and has a real free plan"
        for n in c["free"]:
            x = next((t for t in L if t["name"] == n), None)
            if x: return x, "it is first in our free-alternatives list for this job"
        return L[0], "it is the first tool with a real free plan in our list for this job"
    def _fr_up(t):
        o = [(v, y) for v, y in ((t["monthly"], False), (t["annual"], True)) if isinstance(v, (int, float))]
        if not o: return "No checked US-dollar price — see the official pricing page."
        v, y = min(o); return f"Cheapest paid plan we checked: ${v:g}/mo" + (" (when paid yearly)" if y else "")
    _FR_QTY = _re.compile(r"\d")
    def _fr_inc(t):
        f = t["free"]; txt = _re.sub(r"\$0", "", f)
        return e(f) + ("" if _FR_QTY.search(txt) else " <span class='small'>(Limits not listed here — see the official page.)</span>")
    _fr_secs = ""; _fr_summary = ""
    for c in CATEGORIES:
        L = [t for t in c["tools"] if realfree(t)]; X_ = [t for t in c["tools"] if not realfree(t)]
        tp = _fr_top(c)
        cards = "".join(f'<article class="card"><div class="th">{logo(t)}<div><div class="badges"><span class="badge b-free">REAL FREE PLAN</span>{"<span class=\'badge b-best\'>START HERE</span>" if tp and t is tp[0] else ""}</div><h3><a href="{turl(t["name"])}">{e(t["name"])}</a></h3></div></div><p>{e(t["about"])}</p><p><b>Free plan:</b> {_fr_inc(t)}</p><p class="small"><b>If you outgrow it:</b> {e(_fr_up(t))}</p><p class="small meta">Checked {t.get("checked", CHECKED)} · <a href="{e(t["pricing"])}" rel="noopener" target="_blank">Official pricing page</a></p></article>' for t in L)
        excl = ("<p class='small'><b>Not counted as free</b> (trial, credits only, or not verified): " + "; ".join(f'<a href="{turl(t["name"])}">{e(t["name"])}</a> — {e(t["free"])}' + ((lambda f: f' (free alternative that does the same main job: <a href="{turl(f["name"])}">{e(f["name"])}</a>)' if f else ' (no free alternative that does the same main job)')(free_alt(t["name"]))) for t in X_) + "</p>") if X_ else ""
        top = (f'<div class="pick pl-ans"><span class="badge b-free">START WITH</span> <b>Start with {e(tp[0]["name"])} free</b> — {e(tp[1])}. <span class="small">If you outgrow it: {e(_fr_up(tp[0]))}</span></div>' if tp else '<div class="pick"><b>We found no real free plan for this job.</b> Every tool here is paid, a trial or credits only.</div>')
        _fr_secs += f'<section class="frjob" id="job-{c["id"]}" data-job="{c["id"]}" hidden><h2>{e(c["need"])}: {len(L)} tool{"s" if len(L)!=1 else ""} with a real free plan</h2>{top}<div class="grid">{cards}</div>{excl}<p class="small"><a href="/best-free-ai-{c["id"]}-tools.html">Best free {e(c["name"].lower())} tools guide</a> · <a href="/best-ai-{c["id"]}-tools.html">All {e(c["name"].lower())} tools</a> · <a href="/save-money.html">More ways to save →</a></p></section>'
        if tp: _fr_summary += f'<li><a href="/free.html?job={c["id"]}">{e(c["need"])}</a> — start with <a href="{turl(tp[0]["name"])}">{e(tp[0]["name"])}</a> free ({len(L)} free option{"s" if len(L)!=1 else ""})</li>'
    _fr_opts = "".join(f'<option value="{c["id"]}">{e(c["need"])}</option>' for c in CATEGORIES)
    page("/free.html", f"Can I Do It for Free? Free AI Tools by Job ({CHECKED[:4]}) — Real Free Plans Only | ToolPick",
      f"Pick the job you need and see every AI tool with a real free plan (no trials), what the free plan includes, and the cheapest upgrade. {len({t['name'] for _,t in FREE_LIST})} tools, checked on official pricing pages.",
      f"""<section class="hero"><h1>Can I do it for free?</h1><p class="tag">Pick the job you need. We’ll show every tool with a real free plan for it, what the free plan includes, and the cheapest upgrade if you outgrow it. Free trials and one-time credits don’t count.</p></section>
    <form class="builder" id="fr-form"><label for="fr-job">What do you need to do?</label> <select id="fr-job"><option value="">Choose a job…</option>{_fr_opts}</select> <span id="fr-status" class="small" role="status" aria-live="polite"></span></form>
    <div id="fr-out" tabindex="-1">{_fr_secs}<div id="fr-all"><h2>Start here for each job</h2><ul>{_fr_summary}</ul></div></div>
    <div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How we pick “Start with”</h2><p class="small" style="margin:0">1. The job’s ToolPick Best Value pick, if it has a real free plan. 2. Otherwise the first tool in our free-alternatives list for that job. 3. Otherwise the first tool with a real free plan in our list. A “real free plan” means the official pricing page shows a free plan you can keep using — free trials, one-time credits and unverified plans are excluded. Free-plan details are copied from the official page; where they don’t state limits, we say so instead of guessing.</p><p class="small" style="margin:12px 0 0"><a href="/save-money.html">Save money hub →</a> · <a href="/pay-less.html">Pay less for a tool you use</a> · <a href="/monthly-or-yearly.html">Monthly or yearly?</a></p></div>
    <script>(function(){{const s=document.getElementById('fr-job'),secs=[...document.querySelectorAll('.frjob')],all=document.getElementById('fr-all'),st=document.getElementById('fr-status');
    function run(){{const v=s.value;secs.forEach(x=>x.hidden=x.dataset.job!==v);all.hidden=!!v;const cur=secs.find(x=>!x.hidden);st.textContent=cur?cur.querySelector('h2').textContent:'';history.replaceState(null,'','/free.html'+(v?'?job='+v:''))}}
    const q=new URLSearchParams(location.search).get('job');if(q&&[...s.options].some(o=>o.value==q))s.value=q;else if(q)st.textContent='We do not have that job. Pick one from the list.';
    s.addEventListener('change',()=>{{run();document.getElementById('fr-out').focus()}});run();if(q&&!s.value)st.textContent='We do not have that job. Pick one from the list.'}})();</script>""",
      [{"@context":"https://schema.org","@type":"ItemList","name":"Free AI tools by job","itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,(c,t) in enumerate(FREE_LIST)]},
       crumbs([("ToolPick","/"),("Save money","/save-money.html"),("Can I do it for free?","/free.html")])])
else:
    fcards = "".join(f'<article class="card" data-c="{c["id"]}"><div class="th">{logo(t)}<div><div class="badges"><span class="badge b-free">FREE PLAN</span></div><h3><a href="{turl(t["name"])}">{e(t["name"])}</a></h3></div></div><p>{e(t["about"])}</p><p class="small">{e(t["free"])}</p><p class="price">Paid: {e(t["price"])}</p><p class="small meta">{e(c["name"])} · checked {t.get("checked", CHECKED)}</p></article>' for c, t in FREE_LIST)
    page("/free.html", f"Free AI Tools ({CHECKED[:4]}): {len({t['name'] for _,t in FREE_LIST})} Tools with a Confirmed Free Plan", "Every AI tool on ToolPick with a free plan confirmed on its official pricing page, filterable by category.",
      f"""<h1>Free AI tools</h1><p class="tag">Tools whose official pricing page showed a free plan (each tool shows its own checked date). Free trials are not counted.</p>
    <select id="fc" class="finder" style="padding:10px"><option value="">All categories</option>{''.join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES)}</select>
    <p>{''.join(f'<a href="/best-free-ai-{c["id"]}-tools.html">Best free {e(c["name"].lower())}</a> · ' for c in CATEGORIES)}</p><div class="grid" id="fl">{fcards}</div>
    <script>document.getElementById('fc').onchange=function(){{var v=this.value;document.querySelectorAll('#fl .card').forEach(function(x){{x.style.display=!v||x.dataset.c==v?'':'none'}})}}</script>""",
      [{"@context":"https://schema.org","@type":"ItemList","name":"Free AI tools","itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,(c,t) in enumerate(FREE_LIST)]}])
# --- Save money hub (v20) ---
_SM = [("/pay-less.html","Pay less for a tool you use","Pick the one tool you pay for and see the cheapest plan we checked for the same job, plus your saving."),
       ("/monthly-or-yearly.html","Monthly or yearly?","See how much paying yearly saves, what you pay upfront, and how many months you need to keep it."),
       ("/price-changes.html","Recent price changes","Which AI tools raised or cut prices, newest first, with old and new prices.")]
if FREE_V21: _SM.insert(2, ("/free.html","Can I do it for free?","Pick a job and see every tool with a real free plan, and the cheapest upgrade if you outgrow it."))
_sm_tools = "".join(f'<option value="{slug(n)}">{e(n)}</option>' for n in sorted(tool_pages, key=str.lower))
page("/save-money.html", "Save Money on AI Tools — Pay Less, Go Yearly, Go Free | ToolPick",
  "Four simple ways to spend less on AI tools: find a cheaper plan for the same job, see if yearly billing pays off, find real free plans, and track price changes. Official prices with checked dates.",
  f"""<section class="hero"><h1>Save money on AI tools</h1><p class="tag">Simple ways to spend less, all from prices we checked on official pricing pages.</p></section>
<div class="sgrid">{''.join(f'<a class="card" href="{u}" style="display:block;text-decoration:none"><h2 style="margin:0 0 6px;font-size:1.15rem">{e(t)} →</h2><p style="margin:0">{e(d)}</p></a>' for u,t,d in _SM)}</div>
<form class="builder" id="sm-form" action="/pay-less.html" method="get" style="margin-top:20px"><label for="sm-tool">Quick check: the tool you pay for</label> <select id="sm-tool" name="tool"><option value="">Choose a tool…</option>{_sm_tools}</select> <button type="submit" class="bbtn primary">Can I pay less?</button> <button type="submit" class="bbtn" formaction="/monthly-or-yearly.html">Monthly or yearly?</button></form>
<p class="small">Paying for several tools? <a href="/subscription-audit.html">Run the 60-second Subscription Audit →</a>{"" if FREE_V21 else " · Coming next: <b>Can I do it for free?</b> — pick a job and see every real free plan. Until then, see <a href='/free.html'>free AI tools</a>."}</p>""",
  [{"@context":"https://schema.org","@type":"ItemList","name":"Ways to save money on AI tools","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+u,"name":t} for i,(u,t,d) in enumerate(_SM)]},
   crumbs([("ToolPick","/"),("Save money","/save-money.html")])])
for c in CATEGORIES:
    L = [t for cc, t in FREE_LIST if cc is c]
    if not L: continue
    path = f"/best-free-ai-{c['id']}-tools.html"; n = c["name"]
    title = f"Best Free AI {n} Tools ({CHECKED[:4]}) — {len(L)} with Free Plans"
    d = f"{len(L)} free AI {n.lower()} tools with a free plan confirmed on the official pricing page (each shows its own checked date): {', '.join(t['name'] for t in L[:5])}. They do different main jobs, so pick by the job you need."
    body = f"""<h1>Best free AI {e(n.lower())} tools</h1><p class="tag">{e(d)}</p><ol>{''.join(f"<li><h3><a href='{turl(t['name'])}'>{e(t['name'])}</a></h3><p>{e(t['about'])}</p><p class='small'><b>Main job:</b> {e(cap_label(t['name']))}</p><p>🆓 {e(t['free'])}</p><p class='price'>💲 Paid: {e(t['price'])}</p><p class='small'>checked {t.get('checked', CHECKED)}</p></li>" for t in L)}</ol>
<p>Compare paid options: <a href="/best-ai-{c['id']}-tools.html">all AI {e(n.lower())} tools</a> · <a href="/free.html">all free AI tools</a></p>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,t in enumerate(L)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),("Free AI tools","/free.html"),(f"Best free AI {n} tools",path)])])

# guides hub
page("/guides.html", "AI tool guides: best tool for every job & free alternatives", "Every ToolPick guide: best AI tool for a job, free alternatives and head-to-head comparisons.",
  "<h1>Guides</h1><h2>New guides</h2><ul><li><a href='/free-alternative-to-recraft.html'>Free alternative to Recraft</a></li><li><a href='/free-alternative-to-rytr.html'>Free alternative to Rytr</a></li><li><a href='/best-ai-video-tools-under-20.html'>Best AI video tools under $20</a></li></ul><h2>Best AI tool for…</h2><ul>" + "".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS) + "</ul><h2>Free tools</h2><ul>" + "".join(f'<li><a href="/best-free-ai-{c["id"]}-tools.html">Best free AI {e(c["name"].lower())} tools</a></li>' for c in CATEGORIES) + "</ul><h2>Free alternatives</h2><ul>" +
  "".join(f'<li><a href="{p}">Free alternative to {e(n)}</a></li>' for n,p in FREE_ALT_URLS) + "</ul>" + complinks(COMPARISONS))
# price changes tracker page (v18) — data from CHANGES above
_PCO = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATEGORIES if any(c["id"] in x["cats"] for x in CHANGES))
_pc_latest = CHANGES[0]["date"] if CHANGES else CHECKED
_pc_cards = "".join(change_card(c, "h2") for c in CHANGES) or "<p>No changes recorded yet.</p>"
_pc_body = f"""<section class="hero"><h1>AI price changes</h1><p class="tag">When an AI tool changes its prices, it shows up here — newest first, in plain words, with the old and new prices from the official pricing page. {len(CHANGES)} changes recorded across {len(_pd)} price checks ({', '.join(_pd)}).</p></section>
<div class="builder"><label for="pc-cat">Show changes for</label> <select id="pc-cat"><option value="">All categories</option>{_PCO}</select> <span id="pc-count" class="small" role="status" aria-live="polite"></span></div>
<div id="pc-list">{_pc_cards}</div>
<div class="pick" id="pc-none" hidden><b>No price changes in this category yet.</b> <button type="button" class="bbtn" id="pc-all">Show all changes</button></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How this list is made</h2><p class="small" style="margin:0">We compare each price check with the one before; a change shows only when both old and new prices were recorded.<br>“Correction” = we fixed our own listing. “Now in USD” = the tool switched currency.<br><a href="/price-changes.xml">Feed (Atom)</a> · <a href="/save-money.html">Save money hub</a> · <a href="/pay-less.html">Pay less</a></p></div>
<script>(function(){{const s=document.getElementById('pc-cat'),cards=[...document.querySelectorAll('.pcc')],none=document.getElementById('pc-none'),cnt=document.getElementById('pc-count');
function run(){{const v=s.value;let n=0;cards.forEach(c=>{{const ok=!v||c.dataset.cats.split(' ').includes(v);c.hidden=!ok;if(ok)n++}});none.hidden=n>0;cnt.textContent=n+' change'+(n==1?'':'s')+' shown';history.replaceState(null,'','/price-changes.html'+(v?'?category='+v:''))}}
const q=new URLSearchParams(location.search).get('category');if(q&&[...s.options].some(o=>o.value==q))s.value=q;s.addEventListener('change',run);document.getElementById('pc-all').addEventListener('click',()=>{{s.value='';run();s.focus()}});run()}})();</script>"""
page("/price-changes.html", "AI Price Changes Tracker — Which AI Tools Raised or Cut Prices | ToolPick",
     f"Newest-first tracker of AI tool price changes: old vs new price, date checked and official pricing link for each. {len(CHANGES)} changes recorded, latest {_pc_latest}.", _pc_body,
     [{"@context":"https://schema.org","@type":"ItemList","name":"AI tool price changes","itemListOrder":"https://schema.org/ItemListOrderDescending","numberOfItems":len(CHANGES),
       "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/price-changes.html#{c['date']}-{c['s']}","name":f"{c['name']}: {c['summary']}"} for i, c in enumerate(CHANGES)]},
      crumbs([("ToolPick","/"),("Price changes","/price-changes.html")])])
from xml.sax.saxutils import escape as _xe
open("public/price-changes.xml","w").write('<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>ToolPick — AI price changes</title>'
  + f'<link href="{BASE}/price-changes.html"/><link rel="self" href="{BASE}/price-changes.xml"/><id>{BASE}/price-changes.xml</id><updated>{_pc_latest}T00:00:00Z</updated>'
  + "".join(f'<entry><title>{_xe(c["name"] + " — " + c["label"])}</title><link href="{BASE}/price-changes.html#{c["date"]}-{c["s"]}"/><id>{BASE}/price-changes.html#{c["date"]}-{c["s"]}</id><updated>{c["date"]}T00:00:00Z</updated><summary>{_xe(c["summary"] + " Before: " + c["old"] + " Now: " + c["new"])}</summary><author><name>ToolPick</name></author></entry>' for c in CHANGES) + "</feed>")
# sponsor + newsletter
tiers = "".join(f"<div class='card'><h3>{e(a)}</h3><p>{e(b)}</p><p class='price'>{e(p)}</p></div>" for a,b,p in SPONSOR_TIERS)
page("/sponsor.html", "Sponsor ToolPick — reach people choosing AI tools", "Sponsorship options on ToolPick: category spotlight, sitewide banner and newsletter feature. Sponsored placements are always labelled.",
     f"<h1>Sponsor ToolPick</h1><p>Reach people at the moment they pick an AI tool. Sponsored placements are always labelled and never change our best-value picks or prices.</p><div class='grid'>{tiers}</div><h2>Contact</h2><p>Sponsorship contact: <b>coming soon</b> (contact details will be added here).</p>")
page("/newsletter.html", "ToolPick newsletter — AI tool price changes (coming soon)", "A weekly email with AI tool price changes and new free tiers. Coming soon.",
     "<h1>ToolPick newsletter</h1><p>Weekly: AI tool price changes, new free tiers and best-value picks. <b>Coming soon. Nothing is collected yet.</b></p><form onsubmit='return false'><input type='email' placeholder='you@example.com' disabled style='padding:10px;border-radius:8px'> <button disabled class='btn'>Coming soon</button></form>")
# llms.txt
ll = [f"# ToolPick", f"> Needs-based AI tool finder. {total_tools} tools, prices copied from official pricing pages; each tool has its own checked date (latest {CHECKED}). 'check site' means unverified.", "", "## Categories"]
ll += [f"- [{c['name']}]({BASE}/best-ai-{c['id']}-tools.html): best value {c['best']}; free options {', '.join(c['free'])}" for c in CATEGORIES]
ll += ["", "## Tools"] + [f"- [{n}]({BASE}{turl(n)}): {find(n)['price']} | free: {find(n)['free']}" for n in tool_pages]
ll += ["", "## Comparisons"] + [f"- [{t}]({BASE}/compare/{s}.html)" for s,t,*_ in COMPARISONS] + ["", "## Best tool for a job"] + [f"- [{j[1]}]({BASE}/best-ai-tool-for-{j[0]}.html)" for j in JOBS]
ll += ["", "## Subscription Audit", f"- [AI Subscription Audit]({BASE}/subscription-audit.html): list tools you pay for, get keep/cancel/try-free-tier checklist with potential saving from verified data only, e.g. ?tools=elevenlabs:6:monthly,descript:16:monthly", "", "## New SEO guides", "- [Free alternatives to Recraft]({BASE}/free-alternative-to-recraft.html)", "- [Free alternatives to Rytr]({BASE}/free-alternative-to-rytr.html)", "- [Best AI video tools under $20]({BASE}/best-ai-video-tools-under-20.html): verified entry under $20/mo, cheapest first", "", "## Help me choose", f"- [Help me choose wizard]({BASE}/help-me-choose.html): 5-step guided shortlist, e.g. ?category=audio&budget=10&billing=monthly&seats=1&free=any&annual=any", "", "## Compare builder", f"- [Compare builder]({BASE}/compare-builder.html): pick any 2-3 tools, e.g. ?tools=elevenlabs,descript,heygen", "", "## Cost calculator", f"- [Cost calculator]({BASE}/cost-calculator.html): true monthly/yearly cost by tool or category, seats and billing period, from verified entry prices, e.g. ?tool=elevenlabs&seats=1&billing=monthly", "", "## Browse all tools", f"- [Browse all tools directory]({BASE}/tools.html): filter all tools by category, free plan, verified price, billing and seat pricing, e.g. ?category=audio&free=yes&sort=price", "", f"Data: {BASE}/tools.json"]
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
if FREE_LIST: _lm["/free.html"] = max(max(t.get("checked", CHECKED) for _c, t in FREE_LIST), "2026-10-20") if FREE_V21 else max(t.get("checked", CHECKED) for _c, t in FREE_LIST)
for _sp in SEO_URLS:
    if _sp == SEO_VIDEO_PATH:
        _lm[_sp] = max(t.get("checked", CHECKED) for t in _video_under_sorted) if _video_under_sorted else CHECKED
    elif _sp.startswith("/free-alternative-to-"):
        _tn = next((n for n in SEO_FREE_ALT if f"/free-alternative-to-{slug(n)}.html" == _sp), None)
        if _tn:
            _cs = tool_pages[_tn]; _as = list(dict.fromkeys(x["name"] for cc in _cs for x in cc["tools"] if x["name"] != _tn and hasfree(x, cc)))
            _lm[_sp] = max(find(_a).get("checked", CHECKED) for _a in [_tn] + _as)
_lm["/tools.html"] = "2026-10-19"
_lm["/stacks.html"] = STACK_BUILD_DATE
_lm[PAYLESS_PATH] = PAYLESS_DATE
_lm[MY_PATH] = MY_DATE
_lm["/save-money.html"] = "2026-10-20"
PC_BUILD_DATE = "2026-10-20"  # tracker page + its tool-page boxes redesigned (v18)
_lm["/price-changes.html"] = max(_pc_latest, PC_BUILD_DATE)
for _n in CHANGES_BY_TOOL: _lm[turl(_n)] = max(_lm.get(turl(_n), CHECKED), PC_BUILD_DATE)
for _r in ROLES:
    _lm[role_path(_r[0])] = max(x.get("checked", CHECKED) for b in ROLE_DATA[_r[0]] for c, t, al in ROLE_DATA[_r[0]][b] for x in [t] + al)
open("public/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc>" + (f"<lastmod>{_lm[u]}</lastmod>" if u in _lm else "") + "</url>" for u in URLS) + "</urlset>")
open("public/tools.json","w").write(json.dumps({"checked":CHECKED,"categories":CATEGORIES},indent=1))
print("pages:", len(URLS), "unique tools:", total_tools, {c["id"]:len(c["tools"]) for c in CATEGORIES})
