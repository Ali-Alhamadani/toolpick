"""Builds public/ from tools.py.  Usage: BASE=https://your-site python3 build.py
Pages: index, /best-ai-<category>-tools.html, /tools/<slug>.html, /compare/<slug>.html, sitemap, robots, tools.json"""
import os, re, html, json, shutil
from tools import CATEGORIES, CHECKED, COMPARISONS, PRICE_TABLE, JOBS, SPONSOR_TIERS, FREE_ALT_FOR, REDIRECTS
# v27: price strings in tools.py may carry their own "(checked YYYY-MM-DD)"; pages append the date
# themselves, so strip it from the rendered text only (tools.py facts are untouched).
_CKRE = re.compile(r"\s*\(checked \d{4}-\d{2}-\d{2}\)")
def strip_checked(x): return _CKRE.sub("", x).strip() if isinstance(x, str) else x
for _c in CATEGORIES:
    for _t in _c.get("tools", []):
        if isinstance(_t, dict) and "price" in _t: _t["price"] = strip_checked(_t["price"])
for _k, _v in list(PRICE_TABLE.items()) if isinstance(PRICE_TABLE, dict) else []:
    if isinstance(_v, dict):
        for _f in list(_v):
            if isinstance(_v[_f], str): _v[_f] = strip_checked(_v[_f])
FREE_V21 = True  # v21: set True to ship the 'Can I do it for free?' job picker at /free.html
BASE = os.environ.get("BASE", "https://toolpick-ai.vercel.app").rstrip("/")
e = html.escape
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
CSS = """:root{--bg:#f7f8fa;--sf:#fff;--sf2:#f1f3f6;--tx:#111827;--mu:#4b5563;--bd:#e3e6eb;--ac:#2563eb;--acs:#e8efff;--ok:#15803d;--okt:#fff;--fr:#fef3c7;--frt:#78350f;--warn:#b45309;--sh:0 1px 2px rgba(16,24,40,.05),0 4px 12px rgba(16,24,40,.06);--r:14px;--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:48px}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--sf:#161b22;--sf2:#1c232c;--tx:#e6edf3;--mu:#a3adb8;--bd:#2d3540;--ac:#7cb7ff;--acs:#15253d;--ok:#1f7a3a;--okt:#fff;--fr:#4a3a0c;--frt:#fde68a;--warn:#fbbf24;--sh:0 1px 2px rgba(0,0,0,.4),0 6px 16px rgba(0,0,0,.35)}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;font-size:16px;overflow-wrap:break-word}
h2.h3{font-size:1.17em}a{color:var(--ac);text-underline-offset:2px}a:hover{text-decoration-thickness:2px}
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
CSS += ".fparse{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0}.fpc{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--ac);background:var(--acs);color:var(--tx);font:inherit;font-size:.92rem;cursor:pointer}.fpc:hover{border-width:2px}.fpj{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1px dashed var(--bd);background:var(--sf);color:var(--tx);font-size:.92rem}.fvs{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.fvs>div{border:1px solid var(--bd);border-radius:12px;padding:12px;background:var(--sf)}.fhid{margin-top:10px}"  # v45 smart search

CSS += ".mnav{display:none}nav.top{flex-wrap:nowrap}nav.top>a,nav.top summary{white-space:nowrap}.hstick{position:static!important}@media(max-width:760px){nav.top .dn{display:none}.mnav{display:block;margin-left:auto}nav.top{width:auto!important;margin-left:auto!important}.mnav .menu{right:0;left:auto!important;max-height:75vh;overflow:auto}}.pcba{display:grid;gap:8px;margin:8px 0}.pcba div{background:var(--sf2);border-radius:10px;padding:10px 12px;font-size:1rem;line-height:1.5;color:var(--tx)}.pcba b{display:block;font-size:.85rem;color:var(--mu);text-transform:uppercase;letter-spacing:.02em}"

FOOT = f"""<footer class="site small"><div class="wrap"><p><a href="/how-we-pick.html">How we pick</a> · <a href="/sponsor.html">Sponsor ToolPick</a> · <a href="/newsletter.html">Newsletter</a> · <a href="/embed.html">Embed price cards</a> · <a href="/llms.txt">llms.txt</a></p>Some links may become affiliate links in future; that never changes our picks. Prices copied from each tool's official pricing page; every tool shows its own checked date and pricing link (USD unless shown; yearly-billing prices in parentheses). "check site" = we could not verify the price, so we don't guess. Prices change — always confirm on the official page.</div></footer>"""
def page(path, title, desc, body, ld=None):
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    full = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>{lds}<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script><script defer src="/_vercel/insights/script.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site"><div class="wrap"><a class="brand" href="/"><i aria-hidden="true">T</i>ToolPick</a><nav class="top" aria-label="Main"><details class="dn"><summary>Find a tool</summary><div class="menu"><a href="/">Search by need</a><a href="/tools.html">Browse all tools</a><a href="/help-me-choose.html">Help me choose</a><a href="/stacks.html">Starter stacks</a><hr style="border:0;border-top:1px solid var(--bd);margin:4px 0">{''.join(f'<a href="/best-ai-{c["id"]}-tools.html">{e(c["name"])}</a>' for c in CATEGORIES)}</div></details><a class="dn" href="/compare-builder.html">Compare</a><a class="dn" href="/free.html">Free tools</a><details class="dn"><summary>Save money</summary><div class="menu"><a href="/save-money.html">Save money hub</a><a href="/pay-less.html">Pay less for a tool</a><a href="/monthly-or-yearly.html">Monthly or yearly?</a><a href="/free.html">Can I do it for free?</a><a href="/price-changes.html">Price changes</a><a href="/renewal-reminders.html">Renewal reminders</a><a href="/ai-video-cost.html">Real cost of AI video</a><a href="/ai-voice-cost.html">Real cost of AI voice</a><a href="/subscription-audit.html">Subscription Audit</a></div></details><a class="dn" href="/guides.html">Guides</a><details class="mnav"><summary>Menu</summary><div class="menu"><a href="/">Search by need</a><a href="/tools.html">Browse all tools</a><a href="/help-me-choose.html">Help me choose</a><a href="/stacks.html">Starter stacks</a><a href="/compare-builder.html">Compare</a><a href="/free.html">Free tools</a><a href="/save-money.html">Save money hub</a><a href="/pay-less.html">Pay less for a tool</a><a href="/monthly-or-yearly.html">Monthly or yearly?</a><a href="/free.html">Can I do it for free?</a><a href="/price-changes.html">Price changes</a><a href="/renewal-reminders.html">Renewal reminders</a><a href="/ai-video-cost.html">Real cost of AI video</a><a href="/ai-voice-cost.html">Real cost of AI voice</a><a href="/subscription-audit.html">Subscription Audit</a><a href="/guides.html">Guides</a></div></details></nav></div></header>
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
# --- v35: Trust badge per pick (MarketLens backlog #6). Every fact comes from saved verified data: official pricing-page
# text + checked date, our dated price snapshots (price_history.json), affiliate field. We say plainly that picks are
# not hands-on tested. One limitation per tool is derived only from verified pricing-page text, never written freehand.
_PH = json.load(open("price_history.json"))
_PH_DATES = sorted(_PH)
def price_hist(t):
    n = t["name"]; seen = [d for d in _PH_DATES if n in _PH[d]]
    if not seen: return f"First recorded in our checks on {t.get('checked', CHECKED)}."
    first = seen[0]; texts = [_PH[d][n].get("price") for d in seen]
    chg = [seen[i] for i in range(1, len(seen)) if texts[i] != texts[i-1]]
    cur_diff = t["price"] != texts[-1]
    if len(seen) == 1 and not cur_diff: return f"First recorded in our checks on {first}."
    if not chg and not cur_diff: return f"Same listed price in every check since {first} ({len(seen)} checks)."
    parts = []
    if chg: parts.append("listed price changed on " + ", ".join(chg))
    if cur_diff: parts.append(f"current price text confirmed on {t.get('checked', CHECKED)}")
    return f"Tracked since {first}; " + "; ".join(parts) + "."
_LIM_FREE = _re.compile(r"watermark|\blimit(ed|s)?\b|credit|no commercial|per (day|month|week)|minutes?|/mo\b|/day\b|exports?|resolution|720p|480p|queue|daily", _re.I)
_SEAT = _re.compile(r"per (seat|user|member|editor)|/seat|/user", _re.I)
def limitation(t):
    n, p, f, po = t["name"], t["price"], t["free"], t.get("per_output") or ""
    if p == "check site": return "We could not verify a price on the official pricing page, so we don't show one."
    if f == "check site": return "We could not verify the free-plan details on the official page, so we don't claim a free plan."
    if _re.search(r"AI trial", f, _re.I): return f"The free plan includes AI features only as a trial ({f.rstrip('.')})."
    if _re.search(r"self-hosted", f, _re.I): return f"Free only if you host it yourself; the cloud version is not free ({f.rstrip('.')})."
    if f.lower().startswith("no free"):
        _r = _re.sub(r"^no free plan( (shown|listed)( on (the )?pricing page)?)?[;,]?\s*", "", f.rstrip("."), flags=_re.I).strip("() ")
        return "No free plan on the pricing page we checked" + (f" ({_r})." if _r else ".")
    if _re.search(r"trial", f, _re.I) and not realfree(t): return f"No permanent free plan, only a trial ({f.rstrip('.')})."
    if _re.search(r"one-time|free (api )?credit|in free credits", f, _re.I): return f"The free option is one-time credits, not an ongoing free plan ({f.rstrip('.')})."
    if n in LOWER_TIER: return "The lowest price is a lighter tier: " + LOWER_TIER[n].rstrip(".") + "."
    if _re.search(r"€|£", p) and "$" not in p: return "Prices are listed in euros or pounds, not US dollars, so your cost depends on the exchange rate."
    if t.get("monthly") is None and t.get("annual") is not None: return "The price we checked is billed yearly; we could not confirm a monthly price, so expect to pay a year upfront."
    if po:
        if _re.search(r"per channel", po, _re.I): return "Priced per social channel, so the cost grows with every account you connect."
        if _re.search(r"free", po, _re.I): return f"The free plan has limits: {po.rstrip('.')}."
        return f"Usage costs can add up beyond the plan: {po.rstrip('.')}."
    if realfree(t) and _LIM_FREE.search(f) and len(f) > 14: return f"The free plan has limits: {f.rstrip('.')}."
    segs = [x.strip() for x in p.split(";")]
    if any(x.lower() == "per seat" for x in segs) or (segs and _SEAT.search(segs[0])): return "Priced per seat, so the cost multiplies with team size."
    if _SEAT.search(p): return "Team plans are priced per seat, so team costs multiply with headcount."
    if _re.search(r"credit", p, _re.I): return "Plans are credit-based: heavy use can push you to a higher tier."
    if not realfree(t): return f"No free plan listed ({f.rstrip('.')})."
    return "We haven't recorded a specific usage limit for this tool yet; check the limits on the official pricing page before paying."
def earn(t):
    return ("Affiliate link: ToolPick may earn a commission if you buy. It never changes our pick or the price shown." if t.get("affiliate")
            else "We earn nothing from this pick: no affiliate link, no sponsorship, no payment from the vendor.")
HOW_PICKED = "Picked from the tool's official pricing page and stated features, compared with other tools that do the same main job. Not hands-on tested by ToolPick."
def trust_rows(t):
    ck = t.get("checked", CHECKED)
    return [("How we picked", HOW_PICKED), (f"Price on {ck}", t["price"] + f" (from the official pricing page)"),
            ("Price history", price_hist(t)), ("Money", earn(t)), ("One real limitation", limitation(t))]
TB_CSS = ".tb{margin-top:8px;font-size:.88rem}.tb summary{cursor:pointer;color:var(--ac);font-weight:600;min-height:24px;list-style-position:inside}.tb dl{margin:6px 0 0;display:grid;gap:4px}.tb dt{font-weight:700;color:var(--tx)}.tb dd{margin:0 0 4px;color:var(--mu)}.tbl{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:.8rem;color:var(--mu);margin-top:6px}.tbl span::before{content:'\\2713 ';color:#15803d;font-weight:700}.tbp dl{display:grid;grid-template-columns:minmax(120px,190px) 1fr;gap:6px 14px;margin:0}.tbp dt{font-weight:700}.tbp dd{margin:0}@media(max-width:560px){.tbp dl{grid-template-columns:1fr}.tbp dd{margin-bottom:6px}}"
def trust_mini(t):
    ck = t.get("checked", CHECKED)
    return (f'<div class="tbl" aria-label="Trust summary"><span>Price checked {ck}</span><span>{"Affiliate link" if t.get("affiliate") else "We earn $0"}</span><span>Not paid placement</span></div>'
            f'<details class="tb"><summary>Why trust this pick?</summary><dl>' + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in trust_rows(t)) +
            '</dl><p class="small" style="margin:4px 0 0"><a href="/how-we-pick.html">How we pick</a></p></details>')
def trust_panel(t):
    return (f'<section class="card tbp" aria-labelledby="tbh"><h2 id="tbh" style="margin:0 0 8px;font-size:1.1rem">Why trust this pick</h2><dl>' +
            "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in trust_rows(t)) +
            f'</dl><p class="small" style="margin:8px 0 0"><a href="{e(t["pricing"])}" rel="noopener" target="_blank">Check the official pricing page</a> · <a href="/how-we-pick.html">How we pick</a> · <a href="/price-changes.html">Price changes log</a></p></section>')
CSS += TB_CSS
def card(t, c):
    best = t["name"] == c["best"]; free = t["name"] in c["free"]
    badges = ("<span class='badge b-best'>BEST VALUE</span>" if best else "") + ("<span class='badge b-free'>FREE OPTION</span>" if free else "")
    pc = "price check" if t["price"] == "check site" else "price"
    return f"""<article class="card{' best' if best else ''}"><div class="th">{logo(t)}<div><div class="badges">{badges}</div><h3><a href="{turl(t['name'])}">{e(t['name'])}</a></h3></div></div><p>{e(t['about'])}</p>
<p class="{pc}">{e(t['price'])}</p><p class="small">{e(t["free"])}</p>
<p class="small meta"><a href="{e(t.get('affiliate') or t['url'])}" rel="{'sponsored noopener' if t.get('affiliate') else 'noopener'}" target="_blank">Official site</a> · <a href="{e(t['pricing'])}" rel="noopener" target="_blank">Pricing page</a> · checked {t.get('checked', CHECKED)}</p>{DISCLOSURE if t.get('affiliate') else ''}{trust_mini(t)}</article>"""
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
            if budget == "under30": cands = alts = [t for t in alts if st_rate(t)[1] == "monthly"]  # v29: swaps too stay monthly-only
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
def st_leftout(picks, b, miss, rs):
    # v27: for each left-out job, the cheapest same-job tool with a checked USD monthly price (never yearly, never 'check site').
    if not miss: return ""
    tot = st_total(picks, b) if b != "free" else 0.0
    used = {t["name"] for c, t, a in picks}; rows = []
    for cid in miss:
        cap = slot_cap(rs, cid); job = CAP_LABEL.get(cap, cap)
        pool = sorted({t["name"]: t for c in CATEGORIES for t in c["tools"] if CAPS[t["name"]][0] == cap and t["name"] not in used and t["price"] != "check site" and isinstance(t.get("monthly"), (int, float))}.values(), key=lambda t: (t["monthly"], t["name"]))
        if pool:
            t = pool[0]; z = t["monthly"]
            rows.append(f'<li>Cheapest real option for {e(job)}: <a href="{turl(t["name"])}">{e(t["name"])}</a> at {st_money(z)}/mo (monthly) — adds {st_money(z)}, total {st_money(round(tot + z, 2))}/mo</li>')
        else:
            rows.append(f'<li>Cheapest real option for {e(job)}: no checked monthly price for any tool that does this job</li>')
    return f'<ul class="small">{"".join(rows)}</ul>'
def st_reason(t, c, budget):
    job = cap_label(t["name"])
    if budget == "free": return f"Main job: {job}. Verified free plan: {t['free']}."
    r, b = st_rate(t)
    s = f"Main job: {job}. Entry plan {st_money(r)}/mo {'billed yearly' if b == 'annual' else 'billed monthly'}"
    if budget == "under30":
        same = [x for x in c["tools"] if x is not t and CAPS[x["name"]][0] == CAPS[t["name"]][0] and _num(x.get("monthly")) is not None]
        if b == "monthly" and same and not [x for x in same if _num(x["monthly"]) < r]: s += f" — the cheapest monthly price we checked for {job} in {c['name']}"
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
    na = sum(1 for c, t, a in lst if budget != "free" and st_rate(t)[1] == "annual")
    note = (f" <span class='small'>({na} billed-yearly price{'s' if na != 1 else ''} converted to per month, yearly price ÷ 12; the rest billed monthly)</span>" if na else (" <span class='small'>(all billed monthly)</span>" if budget != "free" else ""))
    return f"<ul>{rows}</ul><p><b>Total: {st_money(tot)}/mo · {st_money(round(tot*12,2))}/yr</b>{note}</p>"
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
    statics = "".join(f"<h3>{e(bl)} stack</h3><p class='small'>{e(bd)}.{(' Left out (no tool for that job fits on verified monthly prices): ' + ', '.join(_CATBY[m]['name'] for m in missing[b])) if missing[b] else ''}</p>{st_leftout(D[b], b, missing[b], _rs)}{st_static(D[b], b)}" for b, bl, bd in BUDGETS)
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
let bud='free',sw={{}};function readURL(){{const p=new URLSearchParams(location.search);const b=p.get('budget');if(BUD[b])bud=b;sw={{}};(p.get('swap')||'').split(',').forEach(x=>{{const[j,s]=x.split(':');const row=(SD[bud]||[]).find(r=>r.job==j);if(row&&row.alts.some(a=>a.s==s))sw[j]=s}});if(bud=='under30'){{const t=(SD[bud]||[]).reduce((m,r)=>m+cur(r).r,0);if(Math.round(t*100)/100>=LIM)sw={{}}}}}}
function cur(row){{const s=sw[row.job]||row.pick;return row.alts.find(a=>a.s==s)}}
function sharePath(){{const q=new URLSearchParams();q.set('role',{json.dumps(_rs)});q.set('budget',bud);const s=Object.entries(sw).filter(([j,v])=>{{const r=SD[bud].find(x=>x.job==j);return r&&r.pick!=v}}).map(([j,v])=>j+':'+v).join(',');if(s)q.set('swap',s);return PATH+'?'+q.toString().replace(/%3A/g,':').replace(/%2C/g,',')}}
function render(push){{document.querySelectorAll('.stabs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.b==bud?'true':'false'));document.getElementById('sDesc').textContent=BUD[bud][0]+': '+BUD[bud][1]+'.';
const rows=SD[bud];let tot=0;document.getElementById('sPicks').innerHTML=rows.map(r=>{{const t=cur(r);tot+=t.r;const others=r.alts.filter(a=>a.s!=t.s).slice(0,2).map(a=>a.s);const rest=rows.reduce((m,x)=>m+(x===r?0:cur(x).r),0);const opts=r.alts.map(a=>{{const ov=bud=='under30'&&a.s!=t.s&&Math.round((rest+a.r)*100)/100>=LIM;return `<option value="${{a.s}}"${{a.s==t.s?' selected':''}}${{ov?' disabled':''}}>${{X(a.n)}} — ${{a.b=='free'?'$0 free plan':M(a.r)+'/mo '+(a.b=='annual'?'billed yearly (yearly price ÷ 12)':'billed monthly')}}${{ov?' — over the $'+LIM+' budget':''}}</option>`}}).join('');
return `<article class="spick"><p class="small" style="margin:0">${{X(r.jn)}}</p><h3><a href="${{t.u}}">${{X(t.n)}}</a> <span class="badge ${{t.b=='free'?'b-free':'b-rank'}}">${{t.b=='free'?'$0':M(t.r)+'/mo'+(t.b=='annual'?' billed yearly':'')}}</span></h3><p class="small">${{X(t.why)}} Checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing</a></p><label for="sw-${{r.job}}">Swap ${{X(r.jn)}} tool</label><select id="sw-${{r.job}}" data-job="${{r.job}}">${{opts}}</select><p class="small"><a href="${{t.u}}">Tool page</a> · ${{others.length?`<a href="/compare-builder.html?tools=${{[t.s].concat(others).join(',')}}">Compare with alternatives</a> · `:''}}<a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=${{t.b=='monthly'?'monthly':'annual'}}">Cost calculator</a></p></article>`}}).join('')||'<p>No verified tools fit this budget.</p>';
tot=Math.round(tot*100)/100;const over=bud=='under30'&&tot>=LIM;const anyA=rows.some(r=>cur(r).b=='annual'),anyM=rows.some(r=>cur(r).b=='monthly');
document.getElementById('sTotal').innerHTML=`<b>Total: ${{M(tot)}}/mo · ${{M(tot*12)}}/yr</b> <span class="small">for ${{rows.length}} tool${{rows.length==1?'':'s'}}, 1 person${{bud=='free'?'':' · '+(anyA?(rows.filter(r=>cur(r).b=='annual').length+' billed-yearly price'+(rows.filter(r=>cur(r).b=='annual').length==1?'':'s')+' converted to a per-month amount (yearly price ÷ 12) and labelled'+(anyM?'; the rest billed monthly':'')):'all billed monthly')}}</span>`+(over?`<div class="swarn" role="alert"><b>Over budget:</b> these swaps total ${{M(tot)}}/mo, which is not under $${{LIM}}. Swap a pick back or choose the Pro stack.</div>`:'');
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
_cards = "".join(f'<article class="card"><h3><a href="{role_path(rs)}">AI tools for {e(rt.lower())}</a></h3><p>{e(rj[0].upper()+rj[1:])}.</p>' + "".join(f"<p class='small'><b>{e(bl)}:</b> {st_money(st_total(ROLE_DATA[rs][b], b))}/mo — {e(', '.join(t['name'] + (' (billed yearly, per-month rate)' if b != 'free' and st_rate(t)[1] == 'annual' else '') for c,t,a in ROLE_DATA[rs][b]))}</p>" for b, bl, bd in BUDGETS) + f'<p><a href="{role_path(rs)}">Open the {e(rt.lower())} stack →</a></p></article>' for rs, rn, rt, rc, rj in ROLES)
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
TIER_MATCH = getattr(_tm, "TIER_MATCH", {})
def cmp_price(x, n, key):
    """v31 like-for-like tier rule: a lower-tier entry plan (LOWER_TIER) compared with a full-tier tool uses its comparable
    full tier (TIER_MATCH, monthly) instead; two lower-tier entry plans are compared entry to entry."""
    if key == "monthly" and x["name"] in TIER_MATCH and n not in LOWER_TIER: return TIER_MATCH[x["name"]][1]
    return _num(x[key])
def tname(x): return x["name"] + (f" ({x['_tier']})" if x.get("_tier") else "")
def cheaper_alt(n, key):
    L = sorted([x for x in samejob(n) if cmp_price(x, n, key) is not None], key=lambda x: (cmp_price(x, n, key), x["name"].lower()))
    if not L: return None
    x = L[0]; v = cmp_price(x, n, key)
    if v != _num(x[key]): x = dict(x, **{key: v, "_tier": TIER_MATCH[x["name"]][0]})
    return x
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
            mm=_num(TOOL[_v["n"]]["monthly"]), ma=_num(TOOL[_v["n"]]["annual"]), lt=LOWER_TIER.get(_v["n"]),
            mf=TIER_MATCH[_v["n"]][1] if _v["n"] in TIER_MATCH else None, mp=TIER_MATCH[_v["n"]][0] if _v["n"] in TIER_MATCH else None)
def _entry_num(t):
    vals = [v for v in (t.get("monthly"), t.get("annual")) if isinstance(v, (int, float))]
    return min(vals) if vals else None
# --- v45: Smart search - the finder reads the whole sentence: tool names ("cheaper than Canva", "like ElevenLabs but free",
# "ChatGPT vs Claude"), budget ("under $10", "$120/year"), team size ("team of 5" -> per-seat totals only where the verified
# entry price is per seat), billing ("no annual plan") and "cheap". Uses ONLY existing verified tools.py data and the one
# same-job rule (samejob/cmp_price/TIER_MATCH). Shareable via /?q=...
def _ps45(t):
    _f = t["price"].split(";")[0]
    if re.search(r"/seat|per seat|/user|per user|/member|per member|per person", _f, re.I): return True
    _p = t["price"].split(";")
    return bool(len(_p) > 1 and re.search(r"^\s*per seat\b", _p[-1], re.I))
def _al45(n):
    out = []
    for x in samejob(n):
        cm, ca = cmp_price(x, n, "monthly"), cmp_price(x, n, "annual")
        tr = TIER_MATCH[x["name"]][0] if (x["name"] in TIER_MATCH and cm is not None and cm != _num(x["monthly"])) else ""
        out.append([slug(x["name"]), cm, ca, tr])
    return out
_AMB45 = {"bolt", "buffer", "captions", "consensus", "motion", "gamma", "surfer", "otter", "runway", "warp", "pitch", "elicit", "lovable",
          "magnific", "reclaim", "perplexity", "notion", "superhuman", "riverside", "fireflies", "fathom", "windsurf", "cursor", "beautiful ai",
          "plus ai", "notion ai", "krea", "gpt", "openai", "bard", "luma", "kling", "jasper", "leonardo", "lindy", "suno", "udio", "pika", "v0"}
_EXTRA45 = {"ChatGPT": ["chat gpt", "chatgpt plus", "openai", "gpt"], "Claude": ["claude ai", "claude code", "anthropic"], "Google Gemini": ["gemini", "bard", "gemini advanced"],
            "Microsoft Copilot": ["copilot", "bing copilot", "copilot pro", "m365 copilot"], "GitHub Copilot": ["gh copilot", "github copilot pro"],
            "Le Chat (Mistral)": ["le chat", "mistral", "mistral ai"], "ElevenLabs": ["eleven labs", "11labs", "11 labs", "elevenlabs.io"],
            "HeyGen": ["hey gen"], "CapCut": ["cap cut"], "ClickUp": ["click up"], "InVideo": ["invideo ai"], "Kling AI": ["kling"],
            "Luma Dream Machine": ["luma", "dream machine", "luma ai"], "Opus Clip": ["opusclip", "opus.pro"], "Otter": ["otter.ai", "otter ai"],
            "Fireflies": ["fireflies.ai", "fireflies ai"], "Gamma": ["gamma.app", "gamma app", "gamma ai"], "Motion": ["motion app", "usemotion"],
            "Surfer": ["surfer seo", "surferseo"], "Bolt": ["bolt.new", "bolt new"], "Warp": ["warp terminal", "warp.dev"], "Pitch": ["pitch.com", "pitch app"],
            "Runway": ["runway ml", "runwayml", "runway ai"], "Perplexity": ["perplexity ai"], "Riverside": ["riverside.fm", "riverside fm"],
            "Magnific": ["magnific ai"], "Consensus": ["consensus ai", "consensus app"], "Lovable": ["lovable.dev", "lovable dev"], "Reclaim": ["reclaim.ai", "reclaim ai"],
            "Captions": ["captions app", "captions ai"], "Buffer": ["buffer app"], "Notion AI": ["notion"], "ResearchRabbit": ["research rabbit"],
            "SciSpace": ["sci space"], "Predis.ai": ["predis", "predis ai"], "Copy.ai": ["copy ai", "copyai"], "Beautiful.ai": ["beautiful ai"],
            "You.com API": ["you.com"], "v0": ["v0.dev", "v0 dev"], "Midjourney": ["mid journey"], "Photoroom": ["photo room"], "SlidesAI": ["slides ai", "slidesai.io"],
            "Krea": ["krea ai"], "Leonardo": ["leonardo ai", "leonardo.ai"], "Fathom": ["fathom ai", "fathom video"], "Grammarly": ["grammarly premium"]}
_ta = {}
for _n in TOOL:
    _al = {_n.lower(), re.sub(r"\s*\(.*?\)", "", _n).lower().strip()} | ({_n.lower().replace(".", " ")} if "." in _n else set()) | set(_EXTRA45.get(_n, []))
    for _a in _al:
        _ta.setdefault(_a, [_a, slug(_n), _a in _AMB45, slug("GitHub Copilot") if _a == "copilot" else None])
_TA45 = json.dumps(sorted(_ta.values(), key=lambda x: -len(x[0])))
_CMP45 = json.dumps([[c[0], (c[2] if isinstance(c[2], list) else [c[2], c[3]]), c[1]] for c in COMPARISONS]).replace("</", "<\\/")
# index
FDATA = json.dumps([dict(n=t["name"],c=c["id"],cn=c["name"],u=turl(t["name"]),p=t["price"],f=t["free"],k=t.get("checked",CHECKED),d=t["about"],dm=dom(t["url"]),a=t["about"]+" "+c["need"],
    m=min([v for v in (t["monthly"],t["annual"]) if isinstance(v,(int,float))],default=None),b=t["name"]==c["best"],fr=realfree(t),sl=slug(t["name"]),pr=t["pricing"],mm=t["monthly"] if isinstance(t["monthly"],(int,float)) else None,ma=t["annual"] if isinstance(t["annual"],(int,float)) else None,
    cap=cap1(t["name"]),caps=CAPS[t["name"]],ps=_ps45(t),al=_al45(t["name"]),lt=LOWER_TIER.get(t["name"]),fa=(lambda f: dict(n=f["name"],u=turl(f["name"]),f=f["free"]) if f else None)(free_alt(t["name"]))) for c in CATEGORIES for t in c["tools"]])
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
FINDER = ('''<div class="finder" role="search"><form class="hstick" id="ff" onsubmit="event.preventDefault();run();document.getElementById('out').scrollIntoView({behavior:'smooth'})"><label for="q" class="skip">Describe what you need</label><div class="sbar"><input type="search" id="q" autocomplete="off" placeholder="What do you need? e.g. voiceover under $10"><button type="submit">Find</button></div></form>
<div class="chips" aria-label="Example searches"><button type="button" class="chip" data-q="turn my podcast into short clips">turn my podcast into short clips</button><button type="button" class="chip" data-q="voiceover under $10">voiceover under $10</button><button type="button" class="chip" data-q="pitch deck for investors">pitch deck for investors</button><button type="button" class="chip" data-q="cheaper than ChatGPT">cheaper than ChatGPT</button><button type="button" class="chip" data-q="meeting notes for a team of 5">meeting notes for a team of 5</button><button type="button" class="chip" data-q="free alternative to Canva">free alternative to Canva</button><button type="button" class="chip" data-q="research papers">research papers</button></div>
<div class="filters"><fieldset class="seg"><legend>Price</legend><input type="radio" name="pf" id="pf-all" value="all" checked><label for="pf-all">All</label><input type="radio" name="pf" id="pf-free" value="free"><label for="pf-free">Free plan</label><input type="radio" name="pf" id="pf-paid" value="paid"><label for="pf-paid">Paid</label></fieldset>
<label class="skip" for="cat">Category</label><select id="cat"><option value="">All categories</option>''' + FOPTS + '''</select>
<label class="skip" for="budget">Budget</label><select id="budget"><option value="any">Any budget</option><option value="0">Free only</option><option value="15">Up to $15/mo</option><option value="30">Up to $30/mo</option><option value="100">Up to $100/mo</option></select>
<label class="skip" for="skill">Experience</label><select id="skill"><option value="beginner">Beginner</option><option value="pro">Pro / power user</option></select></div><div id="out" aria-live="polite"></div></div>
<script>const D=''' + FDATA.replace("</", "<\\/") + r''';
const SW=new Set('the and for with into turn make want need some best good cheap free tool tools that this from your using use help a an my me i to but something anything similar alternative alternatives instead than less like under per month team people plan plans app apps software budget dollars bucks only can which what get looking find'.split(' '));const hasFree=t=>t.fr;
const INT={writing:'write writing writer emails email mail essay essays blog text copy copywriting grammar rewrite letter letters draft editing editor'.split(' '),coding:'code coding programmer programming developer develop app apps debug software website build builder'.split(' '),images:'logo logos image images design designer illustration illustrations poster posters photo photos picture pictures art generate generation brand vector'.split(' '),audio:'podcast podcasts audio voiceover voice voices music song songs sound transcribe transcription transcript recording'.split(' '),video:'video videos clip clips film movie movies youtube shorts avatar explainer'.split(' '),presentations:'pitch deck slides slide presentation presentations startup decks'.split(' '),productivity:'meeting meetings notes note tasks task calendar schedule organise organize productivity transcribe transcription transcript emails email'.split(' '),research:'research papers paper study studies summarise summarize literature academic sources articles citations'.split(' '),marketing:'marketing seo social campaign advertising ads content posts post'.split(' '),assistants:'chat assistant ask question questions answer answers'.split(' '),agents:'chatbot chatbots agent agents bot bots automate automation workflow workflows'.split(' ')};
const SYN={logo:['logo','brand','vector','design','text','image'],logos:['logo','brand','vector','design','text','image'],podcast:['podcast','audio','transcript','editing','recording'],voiceover:['voice','speech'],transcribe:['transcription','transcript','notes'],meetings:['meeting','transcription','notes']};
const TA=''' + _TA45 + r''';const CMP=''' + _CMP45 + r''';const BY={};D.forEach(t=>{if(!BY[t.sl])BY[t.sl]=Object.assign({},t)});D.forEach(t=>{const o=BY[t.sl];o.cs=(o.cs||[]).concat([[t.c,t.cn]]);if(t.b){o.b=true;o.bcn=t.cn}});
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));const $m=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))};
const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const NW={one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,eleven:11,twelve:12,fifteen:15,twenty:20,thirty:30,fifty:50};const NWR='\\d+|'+Object.keys(NW).join('|');const num=v=>NW[v]!=null?NW[v]:parseFloat(v);
const RB_CHEAP=/(?:^|\s)((?:a |any |some )?(?:cheaper|less expensive|more affordable)(?: alternatives?| options?| tools?| apps?| version)?(?: (?:than|to|of|for))?|(?:cost|costs) less than|save (?:money )?on|pay less (?:than|for|on))\s+$/;
const RB_ALT=/(?:^|\s)((?:good |best |other |any |some |an |the )?(?:alternatives?|replacements?|competitors?|substitutes?) (?:to|for|of)|instead of|similar to|(?:tools?|apps?|something|anything|software|sites?|options?) (?:like|similar to)|like|replace|replacing|switch(?:ing)? (?:away )?from|moving (?:away )?from|other than|besides|ditch(?:ing)?|leaving|quit(?:ting)?)\s+$/;
const RB_VS=/(?:^|\s)(vs\.?|versus|or|compare|compared to|compared with|and|between)\s+$/;
const RA_CHEAP=/^\s+((?:but |that is |that's |thats |just |only |and )?(?:cheaper|less expensive|for less)|(?:is |are |seems |feels |got |gets )?(?:too |so |very |getting )?(?:expensive|pricey|costly))(?=\s)/;
const RA_ALT=/^\s+((?:alternatives?|replacements?|competitors?|substitutes?)|(?:but |that is |that's )?(?:similar|alike))(?=\s)/;
const RA_VS=/^\s+(vs\.?|versus|or|compared to|compared with|and)(?=\s)/;
const CODEW=/\b(code|coding|developer|developers|programming|ide|vs code|vscode|github|repo|debug)\b/;
let P={chips:[],tools:[]};
function parse(raw0){const raw=raw0.replace(/\s+/g,' ').trim().slice(0,200);const s=' '+raw.toLowerCase()+' ';const used=new Array(s.length).fill(false);
const R={raw,tools:[],mode:null,x:null,free:false,budget:null,bl:'',seats:null,bill:null,cheap:false,chips:[],txt:''};
const take=(a,b)=>{for(let i=a;i<b;i++)used[i]=true};const isFree=(a,b)=>{for(let i=a;i<b;i++)if(used[i])return false;return true};
const chip=(k,label,a,b)=>R.chips.push({k,label,st:Math.max(0,a-1),en:Math.max(0,b-1)});
const grab=(re,fn)=>{re.lastIndex=0;let m;while((m=re.exec(s))){const a=m.index,b=a+m[0].length;if(m[0].length&&isFree(a,b)){if(fn(m,a,b)!==false)take(a,b)}if(!m[0].length)re.lastIndex++}};
const found=[];for(const [a,sl,amb,alt] of TA){const re=new RegExp('(?<![a-z0-9])'+esc(a)+'(?![a-z0-9])','g');let m;while((m=re.exec(s))){const st=m.index,en=st+a.length;if(found.some(f=>st<f.en&&en>f.st))continue;found.push({sl:alt&&CODEW.test(s)?alt:sl,st,en,amb})}}
found.sort((p,q)=>p.st-q.st);
for(const f of found){const bf=s.slice(0,f.st),af=s.slice(f.en);let rel=null,st=f.st,en=f.en,mb=null,ma=null,kb=null,ka=null;
 for(const [k,re] of [['cheaper',RB_CHEAP],['alt',RB_ALT],['vs',RB_VS]]){const m=bf.match(re);if(m){mb=m;kb=k;break}}
 for(const [k,re] of [['cheaper',RA_CHEAP],['alt',RA_ALT],['vs',RA_VS]]){const m=af.match(re);if(m){ma=m;ka=k;break}}
 rel=(kb=='cheaper'||ka=='cheaper')?'cheaper':(kb=='alt'||ka=='alt')?'alt':(kb||ka)?'vs':null;
 const rest=(bf+' '+af).trim();const alone=/^(?:pricing|prices?|costs?|plans?|reviews?|free plan|free)?$/.test(rest);
 if(f.amb&&!rel&&!alone)continue;
 if(mb&&kb==rel)st=mb.index+mb[0].indexOf(mb[1]);if(ma&&ka==rel)en=f.en+ma[0].length;
 if(R.tools.some(t=>t.sl==f.sl))continue;R.tools.push({sl:f.sl,rel,st,en,amb:f.amb})}
if(R.tools.length<2)R.tools=R.tools.filter(t=>!(t.rel=='vs'&&t.amb)).map(t=>t.rel=='vs'?Object.assign(t,{rel:null,st:t.st,en:t.en}):t);
const T=R.tools;T.forEach(t=>take(t.st,t.en));
if(T.length>=2&&(T.some(t=>t.rel=='vs')||T.every(t=>!t.rel))){R.mode='vs';chip('vs',T.slice(0,3).map(t=>BY[t.sl].n).join(' vs '),Math.min(...T.map(t=>t.st)),Math.max(...T.map(t=>t.en)))}
else if(T.length){const c=T.find(t=>t.rel=='cheaper')||T.find(t=>t.rel=='alt')||T[0];R.x=c.sl;R.mode=c.rel=='cheaper'?'cheaper':c.rel=='alt'?'alt':'tool';chip('tool',(R.mode=='cheaper'?'Cheaper than ':R.mode=='alt'?'Alternatives to ':'Tool: ')+BY[c.sl].n,c.st,c.en)}
grab(/(?<![\w-])(?<!royalty |copyright |hands |distraction |error |stress |watermark |ad |ads |sugar |gluten )(?:for free|free of charge|free plan|free tier|free version|free forever|free|no cost|zero cost|costs nothing|without paying|\$0(?![\d.]))(?![\w-])/g,(m,a,b)=>{if(!R.free){R.free=true;chip('free','Free plan',a,b)}});
const setB=(v,lab,a,b)=>{if(R.budget!=null)return;if(!(v>0)){if(!R.free){R.free=true;chip('free','Free plan',a,b)}return}R.budget=v;R.bl=lab;chip('budget',lab,a,b)};
const KW='(?:under|below|less than|cheaper than|max(?:imum)?|up to|at most|within|no more than|not more than|not over|<=?|budget(?: of| is)?|for)';const MO='(?:\\s*(?:\\/\\s*mo(?:nth)?|a month|per month|monthly|each month|a mo|\\/m)\\b)?';
grab(new RegExp('(?:'+KW+'\\s*)?\\$\\s?(\\d+(?:\\.\\d+)?)\\s*(?:\\/\\s*|a |per |each )(?:year|yr)\\b(?:\\s*(?:or less|max|or under))?','g'),(m,a,b)=>setB(parseFloat(m[1])/12,'Up to $'+m[1]+'/year',a,b));
grab(new RegExp(KW+'\\s*(?:\\$\\s?(\\d+(?:\\.\\d+)?)|(\\d+(?:\\.\\d+)?)\\s*(?:\\$|dollars?|bucks|usd)|(\\d+(?:\\.\\d+)?)(?=\\s*(?:\\/\\s*mo|a month|per month|monthly)))'+MO,'g'),(m,a,b)=>{const v=parseFloat(m[1]||m[2]||m[3]);setB(v,'Up to '+$m(v)+'/mo',a,b)});
grab(/(?:under|below|less than|max(?:imum)?|up to|at most|no more than)\s+(\d+(?:\.\d+)?)(?![\d.])(?!\s*(?:%|people|persons?|users?|seats?|members?|employees|staff|min|mins|minutes?|sec|secs|seconds?|hours?|hrs?|pages?|mb|gb|k\b|words?|images?|videos?|credits?|clips?|slides?|files?|languages?|tracks?|songs?|projects?|days?|weeks?|months?|years?|of us))/g,(m,a,b)=>{const v=parseFloat(m[1]);setB(v,'Up to '+$m(v)+'/mo',a,b)});
grab(new RegExp('\\$\\s?(\\d+(?:\\.\\d+)?)'+MO+'(?:\\s*(?:or less|or under|or cheaper|max|tops|at most|or below|budget))?','g'),(m,a,b)=>{const v=parseFloat(m[1]);setB(v,'Up to '+$m(v)+'/mo',a,b)});
grab(new RegExp('(\\d+(?:\\.\\d+)?)\\s*(?:dollars?|bucks|usd)'+MO,'g'),(m,a,b)=>{const v=parseFloat(m[1]);setB(v,'Up to '+$m(v)+'/mo',a,b)});
const SU='(?:people|persons|person|users?|seats?|members|employees|staff|colleagues|teammates|devs|developers|writers|designers|marketers|editors|students|of us|agents|reps)';
const setS=(v,a,b)=>{v=Math.round(num(v));if(R.seats==null&&v>=1&&v<=500){R.seats=v;chip('seats',v==1?'1 seat':'Team of '+v,a,b)}};
grab(new RegExp('(?:(?:a |my |our )?(?:team|group|crew|staff|company|business|agency|class) of)\\s+('+NWR+')(?:\\s+'+SU+')?\\b','g'),(m,a,b)=>setS(m[1],a,b));
grab(new RegExp('(?:for\\s+)?(?<![\\d.$])('+NWR+')\\s+'+SU+'\\b','g'),(m,a,b)=>setS(m[1],a,b));
grab(/\b(?:month[- ]to[- ]month|monthly (?:billing|plan|subscription|payment)|(?:pay|paid|billed|billing) monthly|no (?:annual|yearly|long[- ]term) (?:plan|commitment|contract|subscription)|without (?:an? )?(?:annual|yearly) (?:plan|commitment|contract)|no commitment|no contract|cancel any ?time)\b/g,(m,a,b)=>{if(!R.bill){R.bill='monthly';chip('bill','Monthly billing',a,b)}});
grab(/\b(?:(?:annual|yearly) (?:billing|plan|subscription|payment)|(?:pay|paid|billed|billing) (?:yearly|annually)|annually|yearly)\b/g,(m,a,b)=>{if(!R.bill){R.bill='yearly';chip('bill','Billed yearly',a,b)}});
grab(/(?<![\w-])(?:cheapest|cheaper|cheap|affordable|inexpensive|low[- ]cost|budget|lowest price|least expensive|low price|not expensive|best price|best deal)(?![\w-])/g,(m,a,b)=>{if(!R.cheap){R.cheap=true;chip('cheap','Cheapest first',a,b)}});
if(R.mode=='alt'&&R.cheap){R.mode='cheaper';const tc=R.chips.find(c=>c.k=='tool');if(tc)tc.label=tc.label.replace('Alternatives to ','Cheaper than ');R.chips=R.chips.filter(c=>c.k!='cheap')}
R.txt=s.split('').map((ch,i)=>used[i]?' ':ch).join('').replace(/\s+/g,' ').trim();
R.chips.sort((p,q)=>p.st-q.st);return R}
const QC=''' + json.dumps(QCAP) + r''';const CL=''' + json.dumps(CAP_LABEL) + r''';function qcapOf(raw){const r=' '+raw.toLowerCase()+' ';for(const [cap,all,any] of QC){if(all.every(w=>r.includes(w))&&(!any.length||any.some(w=>r.includes(w))))return cap}return null}
const stem=w=>w.length>4?w.slice(0,5):w;const hit=(h,w)=>h.includes(w)||h.includes(stem(w));
function intentCats(q){const sc={};Object.keys(INT).forEach(c=>{let n=0;q.forEach(w=>{if(INT[c].some(k=>k==w||stem(k)==stem(w)))n++});if(n)sc[c]=n});const mx=Math.max(0,...Object.values(sc));return Object.keys(sc).filter(c=>sc[c]==mx&&mx>0)}
const CATS=[...new Map(D.map(t=>[t.c,t.cn])).entries()];
function suggHTML(){return `<div class="fsugg" role="group" aria-label="Suggested categories">${CATS.map(([id,n])=>`<button type="button" data-cat="${id}">${n}</button>`).join('')}</div>`}
function exHTML(){return `<div class="fsugg" role="group" aria-label="Example searches">${['write emails faster','design a logo','voiceover under $10','cheaper than Canva','transcribe meetings for a team of 5'].map(x=>`<button type="button" data-ex="${x}">${x}</button>`).join('')}</div>`}
function emptyState(raw,lead){const out=document.getElementById('out');if(!raw){out.innerHTML=`<div class="fempty" role="status"><h2>Describe what you need</h2><p>Tell us the job you want done - for example, writing emails, making a logo, or editing a podcast - and we will match tools from the right category. Use plain words; you do not need a tool name. You can also add a budget or team size ("under $20 for 3 people") or name a tool you use ("cheaper than Canva").</p>${exHTML()}<p style="margin-top:12px">Or browse by category:</p>${suggHTML()}</div>`}else if(lead){out.innerHTML=parsedHTML()+`<div class="fempty" role="status"><h2>Now tell us the job</h2><p>We got your filters above. Add what you want to do - for example "voiceover", "logo" or "meeting notes" - or name a tool you use now ("like Canva").</p>${exHTML()}<p style="margin-top:12px">Or browse by category:</p>${suggHTML()}</div>`}else{out.innerHTML=parsedHTML()+`<div class="fempty" role="status"><h2>No match for "${X(raw)}"</h2><p>We could not match those words to a job our tools do. Try describing the job in plain words - what you want to make, write, record or organise - or pick a category below.</p>${exHTML()}<p style="margin-top:12px">Browse by category:</p>${suggHTML()}</div>`}}
function parsedHTML(job){const cs=P.chips.map((ch,i)=>`<button type="button" class="fpc" data-cut="${i}" aria-label="Remove ${X(ch.label)} from your search">${X(ch.label)}<span aria-hidden="true">&nbsp;×</span></button>`).join('');const j=job?`<span class="fpj">Job: ${X(job)}</span>`:'';return (cs||j)?`<div class="fparse" role="group" aria-label="What we understood from your search"><span class="small">We understood:</span>${j}${cs}</div>`:''}
function bestP(t){const c=[];if(P.bill!='yearly'&&t.mm!=null)c.push({v:t.mm,b:'monthly'});if(P.bill!='monthly'&&t.ma!=null)c.push({v:t.ma,b:'yearly'});if(!c.length)return null;let r=c[0];if(P.budget!=null||P.cheap)r=c.reduce((a,b)=>b.v<a.v?b:a);const f=P.seats&&t.ps?P.seats:1;return {v:r.v*f,u:r.v,b:r.b,f}}
const within=t=>{const p=bestP(t);return !!p&&p.v<=P.budget+1e-9};
function ptxt(t){const p=bestP(t);if(!p)return P.bill?`no ${P.bill=='monthly'?'monthly':'billed-yearly'} price checked`:'price not checked';let s=`from ${$m(p.u)}/mo ${p.b=='yearly'?(t.mm==null?'billed yearly only':'billed yearly'):'monthly'}`;if(P.seats>1)s+=t.ps?` · ${$m(p.v)}/mo for ${P.seats} seats`:' · per plan (our data doesn’t say it’s per seat)';if(P.budget!=null&&p.v>P.budget+1e-9)s+=` · over your ${$m(P.budget)}/mo budget${t.fr?' (free plan available)':''}`;return s}
function dropSel(L){const pf=(document.querySelector('input[name=pf]:checked')||{}).value||'all',bu=document.getElementById('budget').value;if(pf=='free')L=L.filter(hasFree);if(pf=='paid')L=L.filter(t=>!hasFree(t));if(bu=='0')L=L.filter(hasFree);else if(bu!='any')L=L.filter(t=>hasFree(t)||(t.m!=null&&t.m<=+bu));return L}
function applyC(L){let h=0;const K=L.filter(t=>{let ok=true;if(P.free&&!t.fr)ok=false;if(ok&&P.bill&&!bestP(t)&&!t.fr)ok=false;if(ok&&P.budget!=null&&!within(t)&&!t.fr)ok=false;if(!ok)h++;return ok});return {L:K,h}}
const pv=t=>{const p=bestP(t);return p?p.v:1e9};
const lg=t=>`<span class="logo"><img src="https://www.google.com/s2/favicons?domain=${t.dm}&amp;sz=64" alt="" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${X(t.n[0])}'))"></span>`;
const liH=(t,extra)=>`<li>${lg(t)}<div><a href="${t.u}"><b>${X(t.n)}</b></a> <span class="small">· ${ptxt(t)}${t.fr?' · free plan':''}</span>${extra?`<br><span class="small">${extra}</span>`:''}</div></li>`;
function hidH(h){if(!h)return'';const w=[P.free?'free plan':'',P.budget!=null?'budget':'',P.bill?'billing':''].filter(Boolean).join(', ');return `<p class="small fhid">${h} more tool${h>1?'s':''} hidden by your ${w||'filters'} (paid only, over budget, or price not checked). Remove a filter above to see ${h>1?'them':'it'}.</p>`}
function cardH(t,badge,why,acts){return `<article class="card best fpick"><div class="th">${lg(t)}<div><div class="badges"><span class="badge b-best">${badge}</span>${t.fr?'<span class="badge b-free">FREE PLAN</span>':''}</div><h3 style="margin:0"><a href="${t.u}">${X(t.n)}</a></h3></div></div><p style="margin:8px 0">${X(t.d)}</p><p style="margin:8px 0">${X(ptxt(t)).replace(/^f/,'F')}</p>${why?`<p><b>Why:</b> ${why}.</p>`:''}${!t.fr&&t.fa?`<p class="small"><b>Free alternative:</b> <a href="${t.fa.u}">${X(t.fa.n)}</a> — ${X(t.fa.f)}</p>`:''}<p class="small meta">${X(t.cn)} · checked ${t.k} · <a href="${X(t.pr)}" rel="noopener" target="_blank">official pricing</a></p><div class="factions">${acts}</div></article>`}
const reason=t=>{const r=[];if(t.b)r.push(`ToolPick’s Best Value pick for ${X((t.bcn||t.cn).toLowerCase())}`);if(t.fr)r.push('has a real free plan');const p=bestP(t);if(p){if(P.budget!=null&&p.v<=P.budget+1e-9)r.push(`fits your ${$m(P.budget)}/mo budget (${$m(p.v)}/mo ${p.b=='yearly'?'billed yearly':'monthly'}${p.f>1?' for '+p.f+' seats':''})`);else if(!(P.budget!=null))r.push(`cheapest plan we checked is ${$m(p.u)}/mo ${p.b=='yearly'?(t.mm==null?'billed yearly only':'billed yearly'):'monthly'}`)}else r.push('we could not check its price');return r.join(', ')};
function dvs(a,x){let k=null;if(a.cm!=null&&x.mm!=null&&P.bill!='yearly')k='m';else if(a.ca!=null&&x.ma!=null&&P.bill!='monthly')k='a';if(!k)return 'price not compared with '+X(x.n)+' (no checked price on the same billing)';const av=k=='m'?a.cm:a.ca,xv=k=='m'?x.mm:x.ma,d=Math.round((av-xv)*100)/100;return (d<0?`${$m(-d)}/mo less than ${X(x.n)}`:d>0?`${$m(d)}/mo more than ${X(x.n)}`:`same price as ${X(x.n)}`)+` (${k=='m'?'monthly':'billed-yearly'} prices${a.tr&&k=='m'?`, its ${X(a.tr)} plan at ${$m(av)}/mo — the tier comparable to ${X(x.n)}`:''})`}
function altsOf(x){return x.al.map(([s,cm,ca,tr])=>BY[s]?Object.assign({},BY[s],{cm,ca,tr}):null).filter(Boolean)}
function relOf(x){const xc=x.cs.map(c=>c[0]);return Object.values(BY).filter(t=>t.sl!=x.sl&&t.dm!=x.dm).map(t=>{const sh=x.caps.filter(c=>t.caps.includes(c));const capOK=sh.length&&(x.caps.includes(t.cap)||t.caps.includes(x.cap));const cat=t.cs.find(c=>xc.includes(c[0]));return Object.assign({},t,{sh:capOK?sh:[],cat:cat?cat[1]:'',sc:(capOK?sh.reduce((a,c)=>a+(c==x.cap?2:1),0)+(x.caps.includes(t.cap)?0.5:0):0)+(cat?2:0)})}).filter(t=>t.sh.length||t.cat)}
const shW=t=>t.sh.length?t.sh.map(c=>X(CL[c]||c)).join(', '):'the '+X(t.cat.toLowerCase())+' category';const shH=t=>'Shares: '+shW(t)+' (not the same main job, so prices are not compared)';
function relRender(out,x,head,note){const r=applyC(dropSel(relOf(x)));const L=r.L.sort((p,q)=>(P.budget!=null?(within(q)?1:0)-(within(p)?1:0):0)||(P.cheap?pv(p)-pv(q):0)||q.sc-p.sc||(q.b?1:0)-(p.b?1:0)||pv(p)-pv(q)||p.n.localeCompare(q.n));const job=X(CL[x.cap]||x.cap);
const selfLine=`<p class="small" style="margin-top:12px"><b><a href="${x.u}">${X(x.n)}</a> itself:</b> ${ptxt(x)}${x.fr?' · real free plan':''} · checked ${x.k} · <a href="${X(x.pr)}" rel="noopener" target="_blank">official pricing</a></p>`;
let h=parsedHTML(CL[x.cap])+'<h2 class="skip" id="res-h">Results</h2>'+head;if(!L.length){out.innerHTML=h+`<p class="small">${r.h?'Nothing that shares part of the job fits your filters. Remove a filter above to see more.':'No other tool in our list shares part of this job.'}</p>`+selfLine;return}
const pk=L[0],ru=L.slice(1,4),more=L.slice(4);h+=cardH(pk,'CLOSEST MATCH',`no tool in our list does exactly the same main job as ${X(x.n)} (${job}); ${X(pk.n)} shares ${shW(pk)}, ${reason(pk)}`,`<a class="bbtn primary" href="${pk.u}">See ${X(pk.n)} prices</a><a class="bbtn" href="/compare-builder.html?tools=${[x.sl,pk.sl].concat(ru.map(t=>t.sl)).slice(0,3).join(',')}">Compare with ${X(x.n)}</a>`);
if(ru.length)h+=`<h3 style="margin:16px 0 8px;font-size:1rem">Also share part of the job</h3><ul class="fru">${ru.map(t=>liH(t,shH(t))).join('')}</ul>`;if(more.length)h+=`<details class="fmore"><summary>${more.length} more</summary><ul class="fru">${more.map(t=>liH(t,shH(t))).join('')}</ul></details>`;
out.innerHTML=h+hidH(r.h)+selfLine+`<p class="small">${note||'Closest match = shares the most jobs with '+X(x.n)+', then a ToolPick Best Value pick, then the lowest checked price. Prices from official pages.'}</p>`}
function renderTool(out){const T=P.tools;
if(P.mode=='vs'){const L=T.slice(0,3).map(t=>BY[t.sl]),A=L[0],B=L[1];const names=L.map(t=>t.n);const cs=CMP.filter(c=>c[1].length==L.length&&names.every(n=>c[1].includes(n)));const raw=P.raw.toLowerCase();const cp=cs.find(c=>c[2].toLowerCase().split(' for ').slice(1).some(w=>raw.includes(w)))||cs.sort((p,q)=>p[0].length-q[0].length)[0];const same=L.every(t=>t.cap==A.cap);
const col=t=>`<div><h3 style="margin:0 0 6px"><a href="${t.u}">${X(t.n)}</a></h3><p class="small" style="margin:0 0 6px">${X(t.d)}</p><p style="margin:0 0 6px">${X(ptxt(t)).replace(/^f/,'F')}</p><p class="small" style="margin:0 0 6px">${t.fr?'<b>Real free plan:</b> '+X(t.f):'<b>No real free plan</b> ('+X(t.f)+')'}</p><p class="small" style="margin:0 0 6px"><b>Main job:</b> ${X(CL[t.cap]||t.cap)}</p><p class="small meta" style="margin:0">checked ${t.k} · <a href="${X(t.pr)}" rel="noopener" target="_blank">official pricing</a></p></div>`;
out.innerHTML=parsedHTML()+`<h2 class="skip" id="res-h">Results</h2><article class="card best fpick"><h3 style="margin:0 0 10px">${L.map(t=>X(t.n)).join(' vs ')}</h3><div class="fvs">${L.map(col).join('')}</div><p style="margin:10px 0">${same?`They do the same main job (${X(CL[A.cap]||A.cap)}). The full comparison picks a winner on like-for-like plans.`:`They do different main jobs: ${L.map(t=>X(t.n)+' — '+X(CL[t.cap]||t.cap)).join('; ')}. Compare features before choosing.`}</p><div class="factions"><a class="bbtn primary" href="${cp?'/compare/'+cp[0]+'.html':'/compare-builder.html?tools='+L.map(t=>t.sl).join(',')}">${cp?'Read the full comparison':'Compare side by side'}</a>${L.map(t=>`<button type="button" class="bbtn" data-ex="cheaper than ${X(t.n)}">Cheaper than ${X(t.n)}?</button>`).slice(0,2).join('')}</div></article>`;return}
const x=BY[P.x];const alts=dropSel(altsOf(x));const job=X(CL[x.cap]||x.cap);const tierN=x.lt?`<p class="small"><b>Tier note:</b> ${X(x.lt)}.</p>`:'';
const selfLine=`<p class="small" style="margin-top:12px"><b><a href="${x.u}">${X(x.n)}</a> itself:</b> ${ptxt(x)}${x.fr?' · real free plan':''} · checked ${x.k} · <a href="${X(x.pr)}" rel="noopener" target="_blank">official pricing</a></p>`;
if(P.mode=='cheaper'){let key=(P.bill=='yearly'||x.mm==null)?'ca':'cm',own=key=='cm'?x.mm:x.ma;let ch=own==null?[]:alts.filter(a=>a[key]!=null&&a[key]<own);if(key=='cm'&&!ch.length&&P.bill!='monthly'&&x.ma!=null){const c2=alts.filter(a=>a.ca!=null&&a.ca<x.ma);if(c2.length){ch=c2;key='ca';own=x.ma}}
 ch.sort((p,q)=>p[key]-q[key]||p.n.localeCompare(q.n));const bl=key=='cm'?'monthly':'billed-yearly';
 if(!ch.length&&!alts.length&&!altsOf(x).length){relRender(out,x,`<div class="fempty" role="status"><h2>No same-job tool to compare with ${X(x.n)}</h2><p>No other tool in our list does the same main job as ${X(x.n)} (${job}), so we can’t name a cheaper like-for-like option.${x.fa?` Free alternative: <a href="${x.fa.u}">${X(x.fa.n)}</a> — ${X(x.fa.f)}.`:''} These tools share part of the job:</p></div>`);return}
 if(!ch.length){const others=alts.slice().sort((p,q)=>(q.b?1:0)-(p.b?1:0)||pv(p)-pv(q));out.innerHTML=parsedHTML(CL[x.cap])+`<div class="fempty" role="status"><h2>No cheaper checked option than ${X(x.n)}</h2><p>${own==null?`We have no checked ${P.bill=='yearly'?'billed-yearly':'monthly or yearly'} price for ${X(x.n)}, so we can’t say what is cheaper.`:`${X(x.n)} has the lowest checked ${bl} price (${$m(own)}/mo) among tools that do the same main job (${job}).`}${x.fa?` Free alternative: <a href="${x.fa.u}">${X(x.fa.n)}</a> — ${X(x.fa.f)}.`:''}</p></div>${tierN}${others.length?`<h3 style="margin:16px 0 8px;font-size:1rem">Other tools that do the same job</h3><ul class="fru">${others.slice(0,5).map(t=>liH(t,dvs(t,x))).join('')}</ul>`:''}${selfLine}`;return}
 const r=applyC(ch);if(!r.L.length){out.innerHTML=parsedHTML(CL[x.cap])+`<div class="fempty" role="status"><h2>No cheaper option fits your filters</h2><p>${ch.length} tool${ch.length>1?'s':''} that do${ch.length>1?'':'es'} the same job as ${X(x.n)} cost${ch.length>1?'':'s'} less, but none fit${ch.length>1?'':'s'} your filters. Remove a filter above to see ${ch.length>1?'them':'it'}.</p></div>${selfLine}`;return}
 const pk=r.L[0],ru=r.L.slice(1,3),more=r.L.slice(3);const sv=Math.round((own-pk[key])*100)/100;
 let h=parsedHTML(CL[x.cap])+'<h2 class="skip" id="res-h">Results</h2>'+cardH(pk,'CHEAPEST SAME-JOB OPTION',`it does the same main job as ${X(x.n)} (${job}) and costs ${$m(sv)}/mo less on ${bl} prices (${X(pk.n)}${pk.tr&&key=='cm'?' '+X(pk.tr)+' plan':''} ${$m(pk[key])}/mo vs ${X(x.n)} ${$m(own)}/mo)${pk.tr&&key=='cm'?` — compared at its ${X(pk.tr)} plan, the tier comparable to ${X(x.n)}`:''}${pk.fr?', and it has a real free plan':''}`,`<a class="bbtn primary" href="${pk.u}">See ${X(pk.n)} prices</a><a class="bbtn" href="/compare-builder.html?tools=${[x.sl,pk.sl].concat(ru.map(t=>t.sl)).slice(0,3).join(',')}">Compare with ${X(x.n)}</a>`);
 if(ru.length)h+=`<h3 style="margin:16px 0 8px;font-size:1rem">Also cheaper than ${X(x.n)}</h3><ul class="fru">${ru.map(t=>liH(t,dvs(t,x))).join('')}</ul>`;if(more.length)h+=`<details class="fmore"><summary>${more.length} more cheaper option${more.length>1?'s':''}</summary><ul class="fru">${more.map(t=>liH(t,dvs(t,x))).join('')}</ul></details>`;
 out.innerHTML=h+tierN+hidH(r.h)+selfLine+`<p class="small">Same rule as every ToolPick page: only tools with the same main job (${job}), compared on the same billing (monthly with monthly, yearly with yearly). Prices from official pages.</p>`;return}
const r=applyC(alts);const L=r.L.sort((p,q)=>(P.budget!=null?(within(q)?1:0)-(within(p)?1:0):0)||(P.cheap?pv(p)-pv(q):0)||(q.b?1:0)-(p.b?1:0)||pv(p)-pv(q)||p.n.localeCompare(q.n));
if(P.mode=='tool'&&!altsOf(x).length){relRender(out,x,cardH(x,'YOU SEARCHED FOR',reason(x),`<a class="bbtn primary" href="${x.u}">See ${X(x.n)} prices</a>`)+`<h3 style="margin:16px 0 8px;font-size:1rem">No tool does exactly the same main job (${job}). Closest matches:</h3>`);return}
if(P.mode=='tool'){let h=parsedHTML(CL[x.cap])+'<h2 class="skip" id="res-h">Results</h2>'+cardH(x,'YOU SEARCHED FOR',reason(x),`<a class="bbtn primary" href="${x.u}">See ${X(x.n)} prices</a><button type="button" class="bbtn" data-ex="cheaper than ${X(x.n)}">Find cheaper than ${X(x.n)}</button>`)+tierN;
 h+=L.length?`<h3 style="margin:16px 0 8px;font-size:1rem">Tools that do the same job (${job})</h3><ul class="fru">${L.slice(0,4).map(t=>liH(t,dvs(t,x))).join('')}</ul>${L.length>4?`<details class="fmore"><summary>${L.length-4} more</summary><ul class="fru">${L.slice(4).map(t=>liH(t,dvs(t,x))).join('')}</ul></details>`:''}`:`<p class="small">No other tool in our list does the same main job (${job}) with your filters.</p>`;out.innerHTML=h+hidH(r.h);return}
if(!altsOf(x).length){relRender(out,x,'');return}
if(!L.length){out.innerHTML=parsedHTML(CL[x.cap])+`<div class="fempty" role="status"><h2>${alts.length?'No alternative fits your filters':'No same-job alternative in our list'}</h2><p>${alts.length?`${alts.length} tool${alts.length>1?'s':''} do the same main job as ${X(x.n)} (${job}), but none fit your filters. Remove a filter above to see them.`:`No other tool we track does the same main job as ${X(x.n)} (${job}).`}</p></div>${selfLine}`;return}
const pk=L[0],ru=L.slice(1,3),more=L.slice(3);
let h=parsedHTML(CL[x.cap])+'<h2 class="skip" id="res-h">Results</h2>'+cardH(pk,'OUR PICK',`it does the same main job as ${X(x.n)} (${job}), ${reason(pk)}; ${dvs(pk,x)}`,`<a class="bbtn primary" href="${pk.u}">See ${X(pk.n)} prices</a><a class="bbtn" href="/compare-builder.html?tools=${[x.sl,pk.sl].concat(ru.map(t=>t.sl)).slice(0,3).join(',')}">Compare with ${X(x.n)}</a>`);
if(ru.length)h+=`<h3 style="margin:16px 0 8px;font-size:1rem">Runners-up</h3><ul class="fru">${ru.map(t=>liH(t,dvs(t,x))).join('')}</ul>`;if(more.length)h+=`<details class="fmore"><summary>${more.length} more alternative${more.length>1?'s':''}</summary><ul class="fru">${more.map(t=>liH(t,dvs(t,x))).join('')}</ul></details>`;
out.innerHTML=h+tierN+hidH(r.h)+selfLine+`<p class="small">Alternatives = tools with the same main job (${job}). Our pick = a ToolPick Best Value pick if one fits, otherwise the lowest checked price. Prices from official pages.</p>`}
function syncURL(raw){try{const u=new URL(location.href);if(raw)u.searchParams.set('q',raw);else u.searchParams.delete('q');const n=u.pathname+u.search+u.hash;if(n!=location.pathname+location.search+location.hash)history.replaceState(null,'',n)}catch(e){}}
function run(){const bw=document.getElementById('browse');if(bw)bw.hidden=!!(document.getElementById('q').value.trim()||document.getElementById('cat').value);P=parse(document.getElementById('q').value);const raw=P.raw;syncURL(raw);const qt=P.txt,q=qt.split(/\W+/).filter(w=>w.length>2&&!SW.has(w)&&!/^\d/.test(w)),c=document.getElementById('cat').value,sk=document.getElementById('skill').value,out=document.getElementById('out');
if(!raw&&!c){emptyState('');return}
if(P.mode){renderTool(out);return}
const qcap=c?null:qcapOf(qt);if(!q.length&&!qcap&&!c){emptyState(raw,P.chips.length>0);return}
const ic=c||qcap?[]:intentCats(q),primary=ic[0]||null;
let L=D.filter(t=>!c||t.c==c).map(t=>{const h=(t.n+' '+t.a+' '+t.cn).toLowerCase(),own=(t.n+' '+t.d).toLowerCase();let ms=0,ownHits=0;q.forEach(w=>{if(hit(h,w))ms++;if(hit(own,w))ownHits++;(SYN[w]||[]).forEach(sy=>{if(own.includes(sy))ms+=0.34})});let s=ms*3;const inIntent=primary&&t.c==primary;if(inIntent)s+=6;if(t.b)s+=2;if(hasFree(t)&&sk=='beginner')s+=1.5;if(t.m!=null&&sk=='pro')s+=0.5;return Object.assign({s,ms,ownHits,inIntent},t)});
if(qcap&&L.some(t=>t.caps.includes(qcap))){L=L.filter(t=>t.caps.includes(qcap));L.forEach(t=>{t.s+=t.cap==qcap?20:8})}else if(q.length&&!c){if(primary){L=L.filter(t=>t.inIntent||t.ownHits>=2)}else{const mx=Math.max(0,...L.map(t=>t.ms));if(mx>0)L=L.filter(t=>t.ms>0);else{emptyState(raw);return}}}
else if(q.length&&c){const mx=Math.max(0,...L.map(t=>t.ms));if(mx==0){emptyState(raw);return}L=L.filter(t=>t.ms>0)}
L=dropSel(L);L.sort((x,y)=>y.s-x.s||String(x.n).localeCompare(String(y.n)));const seen=new Set();L=L.filter(t=>!seen.has(t.n)&&seen.add(t.n));
const r=applyC(L);L=r.L;if(P.budget!=null)L.sort((x,y)=>(within(y)?1:0)-(within(x)?1:0)||y.s-x.s||x.n.localeCompare(y.n));if(P.cheap){const tp=L.slice(0,8).sort((x,y)=>pv(x)-pv(y)||y.s-x.s);L=tp.concat(L.slice(8))}
if(!L.length){out.innerHTML=parsedHTML(qcap?CL[qcap]||qcap:'')+`<div class="fempty" role="status"><h2>No tools match those filters</h2><p>${r.h?`${r.h} tool${r.h>1?'s':''} match the job but not your ${[P.free?'free plan':'',P.budget!=null?'budget':'',P.bill?'billing':''].filter(Boolean).join(', ')}. Remove a filter above, `:'Try a broader budget, choose All for price, '}or describe the job in different words.</p>${exHTML()}${suggHTML()}</div>`;return}
const top=L.slice(0,5);const pick=P.cheap?top[0]:(top.find(t=>t.b&&top[0]&&t.c==top[0].c&&t.cap==top[0].cap&&(P.budget==null||within(t)))||top[0]);const rest=top.filter(t=>t.n!=pick.n);const ru=rest.slice(0,2),more=rest.slice(2);
const whyNot=t=>{const r=[];const B=pick.mm!=null&&t.mm!=null&&P.bill!='yearly'?'mm':(pick.ma!=null&&t.ma!=null&&P.bill!='monthly'?'ma':null);if(B){const d=Math.round((t[B]-pick[B])*100)/100;r.push(d>0?`${$m(d)}/mo more than ${X(pick.n)} (${B=='mm'?'monthly':'yearly'} prices)`:d<0?`${$m(-d)}/mo less than ${X(pick.n)} (${B=='mm'?'monthly':'yearly'} prices), but ${P.cheap?'ranked lower for your job':'not our Best Value pick'}`:`same price as ${X(pick.n)}`)}else r.push(bestP(t)?`price not compared: ${X(t.n)} is ${ptxt(t)}, ${X(pick.n)} is ${ptxt(pick)}`:'price not checked — see official page');if(!t.fr&&pick.fr)r.push('no real free plan');return r.join('; ')};
const job=pick.c;let h=parsedHTML(qcap?CL[qcap]||qcap:'')+`<h2 class="skip" id="res-h">Results</h2>`+cardH(pick,P.cheap?'CHEAPEST MATCH':'OUR PICK',(qcap?`it does the job you asked for (${X(CL[qcap]||qcap)})${pick.cap==qcap?' as its main job':''}, `:'')+reason(pick),pick.fr?`<a class="bbtn primary" href="/free.html?job=${job}">Start free with ${X(pick.n)}</a><a class="bbtn" href="/pay-less.html?tool=${pick.sl}">Paying for one already? See if you can pay less</a>`:`<a class="bbtn primary" href="${pick.u}">See ${X(pick.n)} prices</a><a class="bbtn" href="/pay-less.html?tool=${pick.sl}">Paying for one already? See if you can pay less</a>`);
if(ru.length)h+=`<h3 style="margin:16px 0 8px;font-size:1rem">Runners-up</h3><ul class="fru">${ru.map(t=>liH(t,'<b>Why not this one:</b> '+whyNot(t)+'.')).join('')}</ul>`;
if(more.length)h+=`<details class="fmore"><summary>${more.length} more match${more.length>1?'es':''}</summary><ul class="fru">${more.map(t=>liH(t)).join('')}</ul></details>`;
h+=hidH(r.h)+`<p class="small" style="margin-top:12px"><a href="/compare-builder.html?tools=${[pick].concat(ru).map(t=>t.sl).join(',')}">Compare these side by side →</a> · <a href="/tools.html?category=${job}">All ${X(pick.cn.toLowerCase())} tools</a> · ${P.cheap?'Cheapest first = lowest checked price among the closest matches.':'Our pick = the Best Value pick for this job if it matches, otherwise the top match.'} Prices from official pages.</p>`;
out.innerHTML=h}
['q','cat','budget','skill','pf-all','pf-free','pf-paid'].forEach(i=>{const el=document.getElementById(i);el.addEventListener('input',run);el.addEventListener('change',run)});document.querySelectorAll('.chip').forEach(b=>b.addEventListener('click',()=>{const q=document.getElementById('q');q.value=b.dataset.q;run();q.focus()}));document.getElementById('out').addEventListener('click',ev=>{const ex=ev.target.closest('[data-ex]'),ct=ev.target.closest('[data-cat]'),cu=ev.target.closest('[data-cut]');if(cu){const ch=P.chips[+cu.dataset.cut],q=document.getElementById('q');if(ch){q.value=(P.raw.slice(0,ch.st)+' '+P.raw.slice(ch.en)).replace(/\s+/g,' ').replace(/\s*(?:,|\band\b|\bbut\b|\bthat'?s\b|\bfor\b|\bwith\b)\s*$/i,'').trim();run();q.focus()}}else if(ex){const q=document.getElementById('q');q.value=ex.dataset.ex;run();q.focus()}else if(ct){document.getElementById('q').value='';document.getElementById('cat').value=ct.dataset.cat;run();document.getElementById('out').scrollIntoView({behavior:'smooth'})}});{const iq=new URLSearchParams(location.search).get('q');if(iq)document.getElementById('q').value=iq.slice(0,200)}run();</script>
''')
desc = f"Tell us what you need and compare {total_tools} AI tools across {len(CATEGORIES)} categories — prices checked on official pages, a best-value pick and a free option."
body = f"""<section class="hero"><h1>Find the right AI tool for your need</h1><p class="tag">{e(desc)}</p></section>{FINDER}<div class="pick"><b>Save money on tools you already pay for</b> — find a cheaper plan, see if yearly pays off, find real free plans, and track price changes. <a href="/save-money.html">Open Save money →</a></div><p class="small">More tools: <a href="/help-me-choose.html">Help me choose</a> · <a href="/compare-builder.html">Compare builder</a> · <a href="/cost-calculator.html">Cost calculator</a> · <a href="/tools.html">Browse all {total_tools} tools</a> · <a href="/stacks.html">Starter stacks</a> · <a href="/subscription-audit.html">Subscription Audit</a></p><div id="browse"><h2>Browse by category</h2>
<div class="needs">{''.join(f'<button data-id="{c["id"]}" class="{"on" if i==0 else ""}">{e(c["name"])}</button>' for i,c in enumerate(CATEGORIES))}</div><div class="tabs">
{''.join(f'<section id="{c["id"]}" class="{"on" if i==0 else ""}"><h2>{e(c["need"])}</h2>{picks(c)}<div class="grid">{"".join(card(t,c) for t in c["tools"])}</div><p><a href="/best-ai-{c["id"]}-tools.html">Full guide: best AI {e(c["name"].lower())} tools →</a></p></section>' for i,c in enumerate(CATEGORIES))}</div></div>
{complinks(COMPARISONS)}<p><a href="/guides.html">All guides →</a> · <a href="/price-changes.html">Price changes log</a></p><h2>Best AI tool for…</h2><ul>{"".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS)}</ul>
<script>const b=document.querySelectorAll('.needs button');function show(id){{b.forEach(x=>x.classList.toggle('on',x.dataset.id==id));document.querySelectorAll('.tabs section').forEach(s=>s.classList.toggle('on',s.id==id));}}
b.forEach(x=>x.onclick=()=>{{show(x.dataset.id);history.replaceState(null,'','#'+x.dataset.id)}});if(location.hash)show(location.hash.slice(1));</script>"""
page("/", "ToolPick — find the right AI tool for your need (verified prices)", desc, body,
     [{"@context":"https://schema.org","@type":"WebSite","name":"ToolPick","url":BASE+"/","potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":BASE+"/?q={search_term_string}"},"query-input":"required name=search_term_string"}}])
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
{complinks(comps_for([t['name'] for t in c['tools']]))}<p><a href="/compare-builder.html">Build your own comparison →</a> Pick any 2–3 tools and share the result.</p>{"".join(f'<p><a href="{role_path(r[0])}">Starter stack for {e(r[2].lower())} →</a> Free, Under $30 and Pro stacks that include {e(n.lower())} tools.</p>' for r in ROLES if c["id"] in r[3])}{f'<p><a href="/free.html?job={c["id"]}">Can I do this for free? →</a> Every {e(n.lower())} tool with a real free plan, and the cheapest upgrade.</p>' if FREE_V21 else ''}<p><a href="/tools.html?category={c['id']}">Browse {e(n.lower())} tools in the full directory →</a> Search, and filter by what it does, free plan, verified price and billing.</p><p><a href="/help-me-choose.html?category={c['id']}">Help me choose {e(n.lower())} tools →</a> Answer 5 quick questions and get a ranked shortlist for this category.</p>{'<p><a href="/best-ai-video-tools-under-20.html">Best AI video tools under $20 →</a> Every video tool with a verified entry price under $20/mo, ranked cheapest first.</p>' if c['id']=='video' else ''}{'<p><a href="/free-alternative-to-recraft.html">Free alternatives to Recraft →</a> Images tools with a verified real free plan.</p>' if c['id']=='images' else ''}{'<p><a href="/free-alternative-to-rytr.html">Free alternatives to Rytr →</a> Writing tools with a verified real free plan.</p>' if c['id']=='writing' else ''}"""
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
TV_TEXT = {}; CMP_TXT = {}
def tool_verdict(name, cats, t):
    m, a = _num(t["monthly"]), _num(t["annual"])
    cm, ca = cheaper_alt(name, "monthly"), cheaper_alt(name, "annual")
    fa = free_alt(name)
    bestc = [cc for cc in cats if cc["best"] == name]
    tn = ""
    # v29: one rule everywhere (tool pages, compare pages, audit): the price answer comes first and is never
    # overridden by the Best Value label; Best Value is added as a separate note.
    bv = (f"{name} is ToolPick's Best Value pick for {bestc[0]['name'].lower()} (chosen for overall value, not only price)" + (" and has a real free plan" if realfree(t) else "")) if bestc else ""
    if m is None and a is None: verdict = "Price not checked — see the official pricing page"
    elif m is not None and cm is not None and cm["monthly"] < m: verdict = f"Cheaper option: {tname(cm)} at {_usd(cm['monthly'])}/mo (monthly prices, same job: {cap_label(name)})"; tn = tier_note(name, cm["name"])
    elif a is not None and ca is not None and ca["annual"] < a: verdict = f"Cheaper option: {tname(ca)} at {_usd(ca['annual'])}/mo (billed-yearly prices, same job: {cap_label(name)})"; tn = tier_note(name, ca["name"])
    elif not samejob(name) or (cm is None and ca is None): verdict = NO_LIKE
    else:
        _lt = [x["name"] for x in samejob(name) if x["name"] in TIER_MATCH] if name not in LOWER_TIER else []
        verdict = (f"No cheaper comparable plan checked — {name} has the lowest checked price for {cap_label(name)} among comparable plans (lighter entry tiers of " + ", ".join(_lt) + " are compared at their comparable tier)") if _lt else f"No cheaper checked option — {name} has the lowest checked price for {cap_label(name)}"
    if bv: verdict += ". " + bv
    if name in LOWER_TIER and m is not None: verdict += ". Tier note: " + LOWER_TIER[name].rstrip(".") + (f"; against full-tier plans like Claude Pro we compare its {TIER_MATCH[name][0]} plan ({_usd(TIER_MATCH[name][1])}/mo)" if name in TIER_MATCH else "")
    if tn: verdict += ". " + tn.rstrip(".")
    TV_TEXT[name] = dict(v=verdict, m=m, a=a)
    s = slug(name); rows = []
    rows.append(("Cheapest plan we checked", " · ".join(x for x in [f"{_usd(m)}/mo monthly" if m is not None else "", f"{_usd(a)}/mo paid yearly" if a is not None else ""] if x) or "Not checked in US dollars — see the official page"))
    rows.append(("All plans we listed", e(PLANS_SHORT.get(name, t["price"]))))
    rows.append(("Real free plan", ("Yes — " + e(t["free"])) if realfree(t) else "No (" + e(t["free"]) + ")"))
    rows.append(("ToolPick Best Value pick", f"Yes, for {e(bestc[0]['name'].lower())}" if bestc else "No"))
    def cmp(x, key, own):
        if x is None: return "none checked"
        d = (f" — {_usd(own - x[key])}/mo less" if x[key] < own else f" — {_usd(x[key] - own)}/mo more" if x[key] > own else " — same price") if own is not None else ""
        return f'<a href="{turl(x["name"])}">{e(tname(x))}</a> {_usd(x[key])}/mo{d}'
    alt_parts = []
    if m is not None or (a is None and cm is not None): alt_parts.append("Monthly: " + cmp(cm, "monthly", m))
    if a is not None: alt_parts.append("Billed yearly: " + cmp(ca, "annual", a))
    rows.append((f"Cheapest same-job alternative ({e(cap_label(name))})", " · ".join(alt_parts) if (cm or ca) else NO_LIKE))
    rows.append(("Best real-free alternative", f'<a href="{turl(fa["name"])}">{e(fa["name"])}</a> — {e(fa["free"])}' if fa else "None with the same main job in our list"))
    rows.append(("What it does (main job first)", ", ".join(f'<a href="/tools.html?job={k}">{e(CAP_LABEL.get(k, k))}</a>' for k in CAPS[name]) + ' <span class="small">(see every tool that does it)</span>')); rows.append(("Categories", ", ".join(f'<a href="/best-ai-{cc["id"]}-tools.html">{e(cc["name"])}</a>' for cc in cats)))
    ch = CHANGES_BY_TOOL.get(name, [])
    if ch: rows.append(("Recent price change", f'{e(ch[0]["label"])}, {ch[0]["date"]}: {e(ch[0]["summary"])} <a href="/price-changes.html#{ch[0]["date"]}-{ch[0]["s"]}">Details</a>'))
    btns = f'<a class="bbtn primary" href="/pay-less.html?tool={s}">Can I pay less?</a>'
    btns += f'<a class="bbtn" href="/watchlist.html?add={s}">Watch this price</a><a class="bbtn" href="/renewal-reminders.html?add={s}">Remind me before renewal</a>'
    if realfree(t) or fa: btns += f'<a class="bbtn" href="/free.html?job={cats[0]["id"]}">Free options</a>'
    if m is not None and a is not None: btns += f'<a class="bbtn" href="/monthly-or-yearly.html?tool={s}">Monthly or yearly?</a>'
    html_ = (f'<section class="verdict card best" aria-labelledby="vh"><h2 id="vh" style="margin:0 0 6px;font-size:1.15rem">Is {e(name)} worth it?</h2><p class="vline"><b>{e(verdict)}.</b></p>'
             '<dl class="vgrid">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + '</dl>'
             f'<div class="factions">{btns}</div><p class="small" style="margin:8px 0 0">Prices checked {t.get("checked", CHECKED)} on the <a href="{e(t["pricing"])}" rel="noopener" target="_blank">official pricing page</a> · <a href="/cost-calculator.html?tool={s}&amp;seats=1&amp;billing=monthly">Full cost calculator</a>. Verdict rule, the same on every page: 1) we look for a tool that does the same main job ({e(cap_label(name))}) with a lower checked price on the same billing (monthly with monthly, yearly with yearly) and name the cheapest; 2) if there is none, we say so; 3) the Best Value label is shown separately and never replaces the price answer. No ratings or reviews.</p></section>')
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
    if any(t["name"] not in LOWER_TIER for t in TT):
        TT = [dict(t, monthly=TIER_MATCH[t["name"]][1], _tier=TIER_MATCH[t["name"]][0]) if t["name"] in TIER_MATCH and _num(t["monthly"]) is not None else t for t in TT]
    def nm(t): return f'<a href="{turl(t["name"])}">{e(t["name"])}</a>'
    def nmp(t): return f'<a href="{turl(t["name"])}">{e(tname(t))}</a>'
    caps = {t["name"]: cap1(t["name"]) for t in TT}
    same = len(set(caps.values())) == 1
    free = [t for t in TT if realfree(t)]
    rows = []; tnote = ""; ranked = []; basis = None; win = None
    if same and any(t.get("_tier") for t in TT):
        rows.append(("Plan compared", " · ".join(f'{nm(t)}: {e(t["_tier"])} {_usd(t["monthly"])}/mo, the tier comparable to the others here (its lighter entry plan is not compared: {e(LOWER_TIER.get(t["name"], ""))})' for t in TT if t.get("_tier"))))
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
            rows.append((f"Price on {BL[basis]} billing", " · ".join(f'{nmp(t)} {_usd(t[basis])}/mo' + (f' (+{_usd(t[basis]-lo)}/mo, +{_usd((t[basis]-lo)*12)}/yr)' if t[basis] > lo else '') for t in ranked)))
            ob = "annual" if basis == "monthly" else "monthly"
            if all(_num(t[ob]) is not None for t in TT):
                r2 = sorted(TT, key=lambda t: (t[ob], t["name"].lower())); lo2 = r2[0][ob]
                rows.append((f"On {BL[ob]} billing", " · ".join(f'{nmp(t)} {_usd(t[ob])}/mo' + (f' (+{_usd(t[ob]-lo2)}/mo, +{_usd((t[ob]-lo2)*12)}/yr)' if t[ob] > lo2 else '') for t in r2)))
            if win and not any(t.get("_tier") for t in TT): tnote = next((tier_note(win["name"], t["name"]) for t in ranked[1:] if tier_note(win["name"], t["name"])), "")
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
            verdict = f"Start free with {free[0]['name']}: only it has a real free plan" + (f"; if you will pay, {tname(win)} is {_usd(ranked[1][basis]-win[basis])}/mo ({_usd((ranked[1][basis]-win[basis])*12)}/yr) less on {BL[basis]} billing" if win and len(TT) == 2 else "")
        elif win:
            nxt = ranked[1]; d = nxt[basis] - win[basis]
            verdict = f"Pick {tname(win)} if price matters: {_usd(d)}/mo ({_usd(d*12)}/yr) less than {tname(nxt)} on {BL[basis]} billing"
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
             + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + f'</dl><div class="factions">{btns}</div><p class="small" style="margin:8px 0 0">Rule: we only compare prices when the tools do the same main job (from what each official site says it does), and only on the same billing (monthly with monthly, billed-yearly with billed-yearly). A real free plan on only one tool comes first. Prices from official pricing pages, each with its own checked date below. No ratings or reviews. The cheaper pick comes from price alone; the Best Value label is shown separately and never replaces it — the same rule as on each tool page.</p></section>')
    return html_, verdict

for x in COMPARISONS:
    s_, title0, cid = x[0], x[1], x[4]; N = cnames(x); TT = [find(n) for n in N]
    path = f"/compare/{s_}.html"; c = next(y for y in CATEGORIES if y["id"] == cid)
    title = f"{title0} ({CHECKED[:4]}): Price, Free Plan & Which to Pick"
    d = f"{' vs '.join(N)} compared with prices from official pricing pages (per-tool checked dates): plans, free tiers and which is better value."
    vhtml, vtxt = compare_verdict(N, TT, c)
    CMP_TXT[s_] = vtxt
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
function adj(list){{return list.some(x=>!x.lt)?list.map(t=>t.mf!=null&&t.mm!=null?Object.assign({{}},t,{{mm:t.mf,n:t.n+' ('+t.mp+')',lt:null}}):t):list}}
function bestValue(list){{list=adj(list);if(list.length<2||!sameJob(list))return null;const catBest=list.filter(t=>t.b);if(catBest.length==1)return catBest[0];const B=basis(list);if(!B)return null;const r=list.slice().sort((a,b)=>a[B]-b[B]);return r[0][B]<r[1][B]?r[0]:null}}
function m$(v){{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))}}
function entry(t){{const p=[];if(t.mm!=null)p.push(m$(t.mm)+'/mo monthly');if(t.ma!=null)p.push(m$(t.ma)+'/mo billed yearly');return p.length?'Cheapest plan we checked: '+p.join(' · '):'Price not in a form we can compare (“check site”, euros or usage-based)'}}
function verdictLine(list,bv){{list=adj(list);if(!sameJob(list))return '<div class="pick"><b>These do different jobs:</b> '+list.map(t=>X(t.n)+' is for '+X(t.cl)).join(', ')+' — so we don’t pick one on price.</div>';const B=basis(list);if(!B)return '<div class="pick"><b>Same main job ('+X(list[0].cl)+'), but not every price is checked on the same billing</b>, so we don’t name a cheaper one.</div>';const r=list.slice().sort((a,b)=>a[B]-b[B]);const BL=B=='mm'?'monthly':'billed-yearly';const d=r[1][B]-r[0][B];const tn=list.some(t=>t.lt)&&!list.every(t=>t.lt)?' <b>Different tier: compare features before switching.</b>':'';return '<div class="pick">'+(bv?'<span class="badge b-best">BEST VALUE</span> <b><a href="'+bv.u+'">'+X(bv.n)+'</a></b> — '+(bv.b&&list.filter(t=>t.b).length==1?'ToolPick’s Best Value pick for its category. ':'')+'':'')+'Same main job ('+X(list[0].cl)+'). On '+BL+' billing: '+r.map(t=>X(t.n)+' '+m$(t[B])+'/mo').join(' · ')+(d>0?' — '+X(r[0].n)+' is '+m$(d)+'/mo ('+m$(d*12)+'/yr) less than '+X(r[1].n)+'.':' — same price.')+tn+'</div>'}}
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
<div class="builder"><form id="cform" novalidate><div class="cform">
<div><label for="cc-tool">Specific tool (optional)</label><select id="cc-tool" name="tool"><option value="">No specific tool — use category below</option>{CTOOLOPTS}</select></div>
<div><label for="cc-cat">Category (used when no tool is picked)</label><select id="cc-cat" name="category"><option value="">Select a category…</option>{CCATOPTS}</select></div>
<div><label for="cc-seats">Seats / users (1–50)</label><input type="number" id="cc-seats" name="seats" min="1" max="50" step="1" value="1" inputmode="numeric"><p class="small" style="margin:6px 0 0">Seats only change the total where the verified entry price itself is stated per seat / per user / per member. Otherwise we say so and seats don't change the listed price.</p><p class="small" id="cc-seatmsg" role="status" hidden style="margin:6px 0 0;color:var(--warn);font-weight:600"></p></div>
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
function vals(){{const rawS=document.getElementById('cc-seats').value.trim();let seats=parseInt(rawS,10);let clamp='';if(rawS===''||isNaN(seats)){{if(rawS!=='')clamp='“'+rawS+'” isn’t a number of seats, so we used 1 seat.';seats=1}}else if(seats<1){{clamp='Seats can’t be below 1, so we used 1 seat.';seats=1}}else if(seats>50){{clamp='This calculator goes up to 50 seats, so we used 50. For bigger teams, check the official pricing page.';seats=50}}else if(!/^\\d+$/.test(rawS)){{clamp='Seats are whole numbers, so we used '+seats+'.'}}
const sm=document.getElementById('cc-seatmsg');if(sm){{sm.textContent=clamp;sm.hidden=!clamp}}const billing=(document.querySelector('input[name=cc-billing]:checked')||{{}}).value||'monthly';return{{tool:document.getElementById('cc-tool').value,cat:document.getElementById('cc-cat').value,seats:seats,billing:billing}}}}
function shareURL(v){{const q=new URLSearchParams();if(v.tool)q.set('tool',v.tool);else if(v.cat)q.set('category',v.cat);q.set('seats',String(v.seats));q.set('billing',v.billing);return location.origin+'/cost-calculator.html?'+q.toString()}}
function render(push=true,submitted=false){{const v=vals();v.submitted=submitted;document.getElementById('cc-seats').value=v.seats;const out=document.getElementById('calc-out');const st=document.getElementById('ccStatus');
if(v.tool&&byS[v.tool]){{out.innerHTML=toolView(byS[v.tool],v.seats,v.billing);st.textContent=byS[v.tool].n+' cost calculated. Share link updated.'}}
else if(v.cat&&catBy[v.cat]){{out.innerHTML=catView(catBy[v.cat],v.seats,v.billing);st.textContent=catBy[v.cat].name+' costs calculated, cheapest verified first. Share link updated.'}}
else if(v.submitted){{out.innerHTML='<div class="pick" role="alert" style="border-color:var(--warn)"><b>Please pick a tool or a category first.</b><p class="small" style="margin-bottom:0">Nothing was calculated because no tool or category is selected. Choose one above, then press Calculate cost.</p></div>';st.textContent='Pick a tool or a category first.';document.getElementById('cc-tool').focus();return}}
else{{out.innerHTML='<div class="pick"><b>Pick a tool or a category to calculate.</b><p class="small" style="margin-bottom:0">Choose a specific tool above, or choose a category (it is used when no tool is picked), set seats and billing, then Calculate. If a tool has no verified numeric price we will say so plainly instead of guessing.</p></div>';st.textContent='Nothing selected yet.';if(push)history.replaceState(null,'','/cost-calculator.html');return}}
if(push)history.replaceState(null,'',shareURL(v).replace(location.origin,''));}}
document.getElementById('cform').addEventListener('submit',ev=>{{ev.preventDefault();const v0=vals();render(true,true);if(v0.tool||v0.cat)document.getElementById('calc-out').scrollIntoView({{behavior:'smooth',block:'start'}})}});
['cc-tool','cc-cat'].forEach(id=>document.getElementById(id).addEventListener('change',()=>render()));
document.querySelectorAll('input[name=cc-billing]').forEach(r=>r.addEventListener('change',()=>render()));document.getElementById('cc-seats').addEventListener('change',()=>{{render();const v=vals();if(v.tool||v.cat)document.getElementById('calc-out').scrollIntoView({{behavior:'smooth',block:'nearest'}})}});
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
V28_CARD_JS = r'''/* v28: My AI stack card — built from the same audit() result, so savings follow the like-for-like rules. */
function stackURL(){return location.origin+sharePath()+'#my-stack'}
function changedRows(){return rows.map(r=>{const t=byS[r.s];if(!t||r.ref==null)return null;const pf=prefill(t);const cur=pf?pf.v:null;if(cur!=null&&Math.abs(cur-r.ref)<0.005)return null;return {r:r,t:t,was:r.ref,wd:r.rd,now:cur,nd:t.k}}).filter(Boolean)}
function cardData(){const res=audit();const valid=res.valid;const sum=k=>Math.round(valid.reduce((m,x)=>{const a=res.act[x.t.s];return m+(a&&a.kind==k?a.save:0)},0)*100)/100;const firm=sum('cancel'),upFree=sum('free'),upSw=sum('switch');const potential=Math.round((firm+upFree+upSw)*100)/100;
const dates=[...new Set(rows.map(r=>byS[r.s]&&byS[r.s].k).filter(Boolean))].sort();
return {valid:valid,tot:Math.round(res.tot*100)/100,potential:potential,firm:firm,upFree:upFree,upSw:upSw,dates:dates,changes:changedRows(),missing:rows.filter(r=>byS[r.s]&&!(eff(r)>0)).map(r=>byS[r.s].n)}}
function saveLines(d){if(!(d.potential>0))return ['Already lean: no saving found on checked prices'];const L=[d.firm>0?'Firm saving if you cancel duplicates: '+money(d.firm)+'/mo ('+money(d.firm*12)+'/yr)':'Firm saving if you cancel duplicates: $0 — no duplicates found'];if(d.upFree>0)L.push('Up to '+money(d.upFree)+'/mo more ('+money(d.upFree*12)+'/yr) if free tiers cover you');if(d.upSw>0)L.push('Up to '+money(d.upSw)+'/mo more ('+money(d.upSw*12)+'/yr) if you switch to a cheaper tool for the same job');return L}
function cardText(d){let s='My AI stack (ToolPick)\n';d.valid.forEach(x=>{s+='- '+x.t.n+': '+money(x.e)+'/mo'+(x.r.billing=='annual'?' (paid yearly)':'')+'\n'});
s+='Total: '+money(d.tot)+'/mo ('+money(d.tot*12)+'/yr)\n';s+=saveLines(d).join('\n')+'\n';
s+='Prices checked '+d.dates.join(', ')+'\n';d.changes.forEach(c=>{s+='Price changed: '+c.t.n+' was '+money(c.was)+'/mo (checked '+c.wd+'), now '+(c.now==null?'no checked price':money(c.now)+'/mo')+' (checked '+c.nd+')\n'});return s+stackURL()}
function renderCard(){const box=document.getElementById('sc-card');if(!box)return;const d=cardData();const btns=document.querySelectorAll('[data-needs-stack]');
btns.forEach(b=>b.disabled=!d.valid.length);document.getElementById('sc-upd').hidden=!d.changes.length;
if(!d.valid.length){box.innerHTML='<p class="sc-h">My AI stack</p><p style="margin:0">Your card is empty. Add the tools you pay for in step 1 and your card appears here, with your monthly and yearly total.</p><p class="small sc-url">toolpick-ai.vercel.app/subscription-audit.html</p>'+(d.missing.length?'<p class="small">'+d.missing.length+' tool(s) still need an amount.</p>':'');return}
let h='<p class="sc-h">My AI stack</p><ul class="sc-list">'+d.valid.map(x=>'<li><span>'+X(x.t.n)+'<span class="small"> · '+X(x.t.cl)+'</span></span><b>'+money(x.e)+'/mo</b></li>').join('')+'</ul>';
h+='<p class="sc-tot"><span>Total</span><b>'+money(d.tot)+'/mo · '+money(d.tot*12)+'/yr</b></p>';
h+=saveLines(d).map((l,i)=>'<p class="sc-save'+(i?' sc-up':'')+'">'+X(l)+'</p>').join('');
if(d.missing.length)h+='<p class="small">Not counted (no amount yet): '+X(d.missing.join(', '))+'</p>';
if(d.changes.length)h+='<div class="sc-chg" role="note"><b>Price changed since this link was made</b><ul>'+d.changes.map(c=>'<li>'+X(c.t.n)+': was '+money(c.was)+'/mo (checked '+X(c.wd)+'), now '+(c.now==null?'no checked price':money(c.now)+'/mo')+' (checked '+X(c.nd)+')'+(c.r.auto?' — your total uses the new price.':' — you entered your own amount, so check whether your plan changed.')+'</li>').join('')+'</ul></div>';
h+='<p class="small" style="margin:8px 0 0">Prices checked '+X(d.dates.join(', '))+' on official pricing pages</p><p class="small sc-url">toolpick-ai.vercel.app</p>';box.innerHTML=h}
function drawCard(){const d=cardData();const SL=saveLines(d);const n=Math.max(d.valid.length,1),W=1200,H=380+n*56+(SL.length-1)*42+(d.changes.length?40+d.changes.length*34:0);const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');
const F='system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif';g.fillStyle='#ffffff';g.fillRect(0,0,W,H);g.fillStyle='#2563eb';g.fillRect(0,0,W,12);
g.fillStyle='#111827';g.font='700 46px '+F;g.fillText('My AI stack',60,90);g.font='400 24px '+F;g.fillStyle='#4b5563';g.fillText('ToolPick · prices from official pricing pages',60,128);
let y=190;g.font='500 30px '+F;if(!d.valid.length){g.fillStyle='#4b5563';g.fillText('No tools yet',60,y);y+=56}
d.valid.forEach(x=>{g.fillStyle='#111827';g.textAlign='left';let nm=x.t.n;g.fillText(nm,60,y);g.textAlign='right';g.fillText(money(x.e)+'/mo',W-60,y);g.textAlign='left';y+=56});
g.fillStyle='#e3e6eb';g.fillRect(60,y-30,W-120,2);y+=20;g.fillStyle='#111827';g.font='700 34px '+F;g.fillText('Total',60,y);g.textAlign='right';g.fillText(money(d.tot)+'/mo · '+money(d.tot*12)+'/yr',W-60,y);g.textAlign='left';y+=62;
SL.forEach((l,i)=>{g.fillStyle=i?'#374151':'#15803d';g.font=(i?'600 26px ':'700 30px ')+F;g.fillText(l,60,y);y+=i?42:46});
if(d.changes.length){g.fillStyle='#b45309';g.font='600 24px '+F;g.fillText('Price changed since this link was made:',60,y);y+=34;g.font='400 22px '+F;d.changes.forEach(ch=>{g.fillText(ch.t.n+': was '+money(ch.was)+'/mo ('+ch.wd+'), now '+(ch.now==null?'no checked price':money(ch.now)+'/mo')+' ('+ch.nd+')',60,y);y+=34});y+=6}
g.fillStyle='#4b5563';g.font='400 22px '+F;g.fillText('Prices checked '+d.dates.join(', '),60,y);g.fillStyle='#2563eb';g.font='600 24px '+F;g.fillText('toolpick-ai.vercel.app/subscription-audit.html',60,H-36);return c}
function scSay(m){document.getElementById('sc-status').textContent=m}
document.getElementById('sc-copylink').addEventListener('click',async()=>{const u=stackURL();try{await navigator.clipboard.writeText(u);scSay('Link copied. Save it to re-check your stack when prices change: '+u)}catch(e){scSay('Copy this link: '+u);window.prompt('Copy this link',u)}});
document.getElementById('sc-copytext').addEventListener('click',async()=>{const t=cardText(cardData());try{await navigator.clipboard.writeText(t);scSay('Summary copied.')}catch(e){scSay('Copy the summary from the box that opened.');window.prompt('Copy this summary',t)}});
document.getElementById('sc-png').addEventListener('click',()=>{drawCard().toBlob(b=>{const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='my-ai-stack.png';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);scSay('Image downloaded: my-ai-stack.png')},'image/png')});
document.getElementById('sc-upd').addEventListener('click',()=>{rows.forEach(r=>{const t=byS[r.s];const pf=prefill(t);r.ref=pf?pf.v:null;r.rd=t.k});syncURL();renderCard();scSay('Saved prices updated in the link. Copy the link again to keep the new version.')});
const _rr=renderResults;renderResults=function(s){_rr(s);renderCard()};renderCard();
'''
audit_body = f"""<style>details.bnote summary{{cursor:pointer;min-height:44px;display:flex;align-items:center}}@media(max-width:600px){{.alinks,.adet,.arow .price{{display:none}}.ares .small{{font-size:.85rem}}.arow{{padding:12px}}}}#sc-upd[hidden]{{display:none}}.scard{{background:var(--sf);border:1px solid var(--bd);border-top:6px solid var(--ac);border-radius:14px;padding:18px 20px;max-width:640px;box-shadow:var(--sh)}}.sc-h{{font-size:1.4rem;font-weight:700;margin:0 0 8px}}.sc-list{{list-style:none;padding:0;margin:0}}.sc-list li,.sc-tot{{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px solid var(--bd);margin:0}}.sc-tot{{border-bottom:0;font-size:1.1rem;padding-top:10px}}.sc-save{{font-weight:700;color:var(--ok);margin:6px 0}}.sc-up{{color:var(--tx);font-weight:600}}.sc-save .small{{font-weight:400;color:var(--mu)}}.sc-url{{color:var(--ac);margin:4px 0 0}}.sc-chg{{border:1px solid var(--warn);border-radius:10px;padding:8px 12px;margin:8px 0}}.sc-chg ul{{margin:4px 0 0;padding-left:18px}}@media(prefers-color-scheme:dark){{.sc-save{{color:#4ade80}}}}</style><h1>AI Subscription Audit — what could you stop paying for?</h1><p class="tag">A 60-second check for subscription fatigue. Add the AI tools you pay for, confirm what you pay each month (our verified entry price is prefilled where we have one — edit it, your plan may differ), and get one clear action per tool: keep it, consider cancelling it, try its free tier first, or check a cheaper switch. Potential savings are counted once per tool, never twice.</p>
<details class="bnote"><summary><b>Your privacy:</b> runs in your browser, nothing is sent to us</summary><p class="small" style="margin:8px 0 0">This runs entirely in your browser. Your list and amounts are not sent to us and are not stored by us. They only appear in the share link if you copy one — so only share that link if you are happy for whoever opens it to see your list and amounts. Every price we show is copied from the tool's official pricing page with its checked date; free-tier limits are on that official page, not guessed here.</p></details>
<div class="builder"><h2 style="margin-top:0;font-size:1.05rem">1. Add tools you pay for</h2><div class="aform"><div><label for="a-search">Search tools</label><input type="search" id="a-search" autocomplete="off" placeholder="Start typing a tool name…"></div><div><label for="a-select">Tool</label><select id="a-select"><option value="">Select a tool…</option>{AOPTS}</select></div><button type="button" class="bbtn primary" id="a-add">Add tool</button></div><p class="small" id="a-status" role="status" style="margin:12px 0 0"></p><div class="pick" id="a-linkmsg" role="alert" hidden style="margin-top:12px"></div><div id="a-rows"></div><div class="atotal" aria-live="polite" id="a-total">No tools added yet. Add your first paid tool above — it takes about a minute.</div><div class="bactions"><button type="button" class="bbtn primary" id="a-run">Run my audit</button><button type="button" class="bbtn" id="a-copy">Copy share link</button><button type="button" class="bbtn" id="a-clear">Clear all</button></div></div>
<h2>2. Your audit</h2><div id="a-out" aria-live="polite" aria-atomic="false"><div class="pick"><b>No tools added yet.</b><p class="small" style="margin-bottom:0">Add the tools you pay for above, check the amounts, and your keep / consider cancelling / try the free tier checklist will appear here. Try the example: <a href="/subscription-audit.html?tools=descript:24:monthly,chatgpt:8:monthly,midjourney:10:monthly">Descript $24 + ChatGPT $8 + Midjourney $10</a>.</p></div></div>
<section id="my-stack" aria-labelledby="sc-title"><h2 id="sc-title">3. Your AI stack card</h2><p class="small">A clean summary of your stack to keep or share. <b>Save this link to re-check when prices change:</b> opening it again re-prices your stack from our latest checked prices and flags any tool whose price changed since the link was made. No account, no email.</p>
<div class="scard" id="sc-card" aria-live="polite"></div>
<div class="bactions"><button type="button" class="bbtn primary" id="sc-copylink" data-needs-stack>Copy share link</button><button type="button" class="bbtn" id="sc-png" data-needs-stack>Download image</button><button type="button" class="bbtn" id="sc-copytext" data-needs-stack>Copy text</button><button type="button" class="bbtn" id="sc-upd" hidden>Update saved prices in my link</button><span class="small bstatus" id="sc-status" role="status"></span></div>
<p class="small">The image is drawn in your browser; nothing is uploaded. When you paste the link into a chat or social post, the preview shows ToolPick's standard picture, not your stack: this is a static site, so it can't make a preview image for each stack. Your stack appears when the link is opened. Amounts you didn't edit are left out of the link and re-priced from current data; amounts you typed yourself are kept.</p></section>
<details class="bnote"><summary><h2 style="display:inline;margin:0;font-size:1.05rem">How each action is chosen — one per tool</h2></summary><p class="small" style="margin:8px 0 0">In this order, so a tool is never counted twice: <b>1. Consider cancelling</b> — you pay for 2 or more tools that do the same main job (based on what each official site says it does — a shared broad category is not enough); we suggest keeping a ToolPick Best Value pick if one is among them, otherwise the one that costs you least, and cancelling the others. <b>2. Try the free tier</b> — the tool itself has a verified real free plan (free trials and one-time credits do not count). <b>3. Switch to check</b> — another tool that does the same main job has a cheaper checked price on the same billing you pay (monthly with monthly, billed-yearly with billed-yearly); we add a tier note when the plans are different tiers, and count only the difference as potential saving, not your whole amount. <b>4. Keep</b> — none of the above applies on verified data. “Potential saving” always means <i>if you act on every suggestion</i>; tick or untick suggestions below to see your own plan total.</p><p class="small" style="margin:12px 0 0">Next steps: <a href="/compare-builder.html">compare tools side by side</a> · <a href="/cost-calculator.html">what will it really cost?</a> · <a href="/help-me-choose.html">help me choose a replacement</a> · <a href="/tools.html">browse all tools</a></p></details>
<script>const AD={ADATA};
const byS={{}};AD.forEach(t=>byS[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function pv(v){{if(v==null)return null;if(typeof v=='number')return{{amt:v,cur:'$'}};const m=String(v).match(/([€$£])\\s*([\\d.]+)/);if(m)return{{amt:parseFloat(m[2]),cur:m[1]}};const n=String(v).match(/([\\d.]+)/);return n?{{amt:parseFloat(n[1]),cur:'$'}}:null}}
function money(v){{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))}}
function entry(t){{const vals=[pv(t.m),pv(t.a)].filter(x=>x&&x.cur=='$');if(!vals.length)return null;vals.sort((a,b)=>a.amt-b.amt);return vals[0]}}
function prefill(t){{const m=pv(t.m);if(m&&m.cur=='$')return{{v:m.amt,src:'our verified monthly-billing entry rate'}};const a=pv(t.a);if(a&&a.cur=='$')return{{v:a.amt,src:'our verified per-month rate when billed yearly, shown as a monthly amount'}};return null}}
const MAXROWS=12,AMAX=10000;let rows=[];const ticks={{}};
function eff(r){{const amt=parseFloat(r.amt);if(isNaN(amt)||amt<0||amt>AMAX||!/^\\s*\\d+(\\.\\d+)?\\s*$/.test(String(r.amt)))return 0;return r.billing=='annual'?amt/12:amt}}
function sharePath(){{const q=rows.filter(r=>byS[r.s]).map(r=>r.s+':'+(r.auto||r.amt===''?'':r.amt)+':'+r.billing+(r.ref!=null?':'+r.ref+':'+r.rd:'')).join(',');return '/subscription-audit.html'+(q?('?tools='+encodeURIComponent(q)):'')}}
function syncURL(){{history.replaceState(null,'',sharePath())}}
function renderTotals(){{const valid=rows.map(r=>({{r:r,t:byS[r.s],e:eff(r)}})).filter(x=>x.t&&x.e>0);const tot=valid.reduce((sum,x)=>sum+x.e,0);document.getElementById('a-total').innerHTML=rows.length?('<b>Current spend you told us: '+money(tot)+'/mo ('+money(tot*12)+'/yr)</b> across '+valid.length+' tool'+(valid.length==1?'':'s')+' with an amount. '+(rows.length-valid.length?((rows.length-valid.length)+' tool(s) still need an amount.'):'')):'No tools added yet. Add your first paid tool above — it takes about a minute.';return{{valid:valid,tot:tot}}}}
function renderRows(focusSlug){{const wrap=document.getElementById('a-rows');
if(!rows.length){{wrap.innerHTML='<p class="small">Nothing added yet — your tools will appear here as editable rows.</p>';renderTotals();return}}
wrap.innerHTML=rows.map((r,i)=>{{const t=byS[r.s];const pf=prefill(t);const e=eff(r);
return `<article class="arow" data-row="${{r.s}}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges">${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3 style="margin:0"><a href="${{t.u}}">${{X(t.n)}}</a></h3><p class="small" style="margin:0">Main job: ${{X(t.cl)}}</p></div></div><p class="price">${{X(t.p)}}</p><p class="small adet">${{X(t.f)}}<br>Our listed price checked ${{t.k}} · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a> · <a href="${{t.u}}">Tool page</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=monthly">Cost calculator</a></p><div class="rgrid"><div><label for="amt-${{r.s}}">What you pay for ${{X(t.n)}}</label><input type="number" id="amt-${{r.s}}" data-amt="${{r.s}}" min="0" step="0.01" inputmode="decimal" value="${{X(r.amt)}}" placeholder="Tell us what you pay"><p class="small" style="margin:6px 0 0">${{pf?('Prefilled with '+pf.src+' ('+money(pf.v)+'/mo) — edit it, your plan may differ. This is <b>what you told us</b> once you change it.'):'No verified USD entry rate in our table, so nothing is prefilled — tell us what you pay.'}}</p></div><div><label for="bill-${{r.s}}">That amount is…</label><select id="bill-${{r.s}}" data-bill="${{r.s}}"><option value="monthly"${{r.billing=='monthly'?' selected':''}}>Per month</option><option value="annual"${{r.billing=='annual'?' selected':''}}>Per year (we show it ÷ 12)</option></select><p class="small" style="margin:6px 0 0" data-eff="${{r.s}}">${{e?('Counts as <b>'+money(e)+'/mo</b> in your total'+(r.billing=='annual'?' ('+money(parseFloat(r.amt)||0)+'/yr ÷ 12)':'')):(String(r.amt).trim()===''?'Add an amount to include this tool.':'That amount can\u2019t be used (use a number from 0 to $10,000). Not counted.')}}</p></div><div><label aria-hidden="true">&nbsp;</label><button type="button" class="bbtn" data-remove="${{r.s}}" aria-label="Remove ${{X(t.n)}} from your audit">Remove ${{X(t.n)}}</button></div></div></article>`}}).join('');
wrap.querySelectorAll('[data-amt]').forEach(inp=>inp.addEventListener('input',()=>{{const r=rows.find(x=>x.s==inp.dataset.amt);if(r){{r.amt=inp.value;r.auto=false;const t=byS[r.s];const el=wrap.querySelector('[data-eff="'+r.s+'"]');const e=eff(r);if(el)el.innerHTML=e?('Counts as <b>'+money(e)+'/mo</b> in your total'+(r.billing=='annual'?' ('+money(parseFloat(r.amt)||0)+'/yr ÷ 12)':'')):(String(r.amt).trim()===''?'Add an amount to include this tool.':'That amount can\u2019t be used (use a number from 0 to $10,000). Not counted.');renderTotals();renderResults(false);syncURL()}}}}));
wrap.querySelectorAll('[data-bill]').forEach(sel=>sel.addEventListener('change',()=>{{const r=rows.find(x=>x.s==sel.dataset.bill);if(r){{r.billing=sel.value;r.auto=false;renderRows(r.s);renderResults(false);syncURL();const f=document.getElementById('bill-'+r.s);if(f)f.focus()}}}}));
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
if(!act[keeper.t.s])act[keeper.t.s]={{kind:'keep',save:0,keeperOf:job,reason:'Keep '+keeper.t.n+': '+whyKeeper+'. It is the one to keep from your '+job+' overlap, so we do not also suggest dropping it to a free tier — cancel the others and keep paying for this one.'}};
group.forEach(x=>{{if(x.t.s!=keeper.t.s&&!act[x.t.s])act[x.t.s]={{kind:'cancel',save:x.e,keeper:keeper.t,catName:job,reason:'You told us you pay for '+group.length+' tools that do the same main job ('+job+': '+group.map(y=>y.t.n).join(', ')+'). Keep '+keeper.t.n+' — '+whyKeeper+'. Consider cancelling '+x.t.n+' instead of paying for both.'}}}})}});
/* 2-4) per tool */
valid.forEach(x=>{{const t=x.t;if(act[t.s])return;
if(t.fr){{act[t.s]={{kind:'free',save:x.e,reason:t.n+' itself has a verified real free plan: '+t.f+'. Try the free tier first — if the free plan covers you, you could stop paying. Check its limits on the official pricing page (we do not state limits we have not verified).'}};return}}
const B=x.r.billing=='annual'?'ma':'mm',BL=x.r.billing=='annual'?'billed-yearly':'monthly';
let bestAlt=null;t.al.forEach(k=>{{const alt=byS[k];if(!alt)return;const v=(B=='mm'&&alt.mf!=null&&!t.lt)?alt.mf:alt[B];if(v==null||v>=x.e)return;if(!bestAlt||v<bestAlt.v||(v==bestAlt.v&&alt.n<bestAlt.alt.n))bestAlt={{alt:alt,v:v}}}});
if(bestAlt){{const sub=(B=='mm'&&bestAlt.alt.mf!=null&&!t.lt);const tn=!sub&&(!!bestAlt.alt.lt)!=(!!t.lt)?' Different tier: compare features before switching'+(bestAlt.alt.lt?' ('+bestAlt.alt.lt+').':(t.lt?' ('+t.lt+').':'.')):'';act[t.s]={{kind:'switch',save:Math.round((x.e-bestAlt.v)*100)/100,alt:bestAlt.alt,reason:bestAlt.alt.n+((B=='mm'&&bestAlt.alt.mf!=null&&!t.lt)?' ('+bestAlt.alt.mp+', the tier comparable to yours)':'')+' does the same main job ('+t.cl+') and its '+((B=='mm'&&bestAlt.alt.mf!=null&&!t.lt)?'comparable':'cheapest')+' '+BL+' plan we checked is '+money(bestAlt.v)+'/mo (checked '+bestAlt.alt.k+'), lower than the '+money(x.e)+'/mo you told us you pay for '+t.n+' on '+BL+' billing.'+tn+' We count only the difference as potential saving.'}};return}}
act[t.s]={{kind:'keep',save:0,reason:'No like-for-like cheaper option checked: no overlap with your other tools, no real free plan on '+t.n+' itself, and no tool that does the same main job ('+t.cl+') has a cheaper '+(x.r.billing=='annual'?'billed-yearly':'monthly')+' price than what you told us. On verified data, keep it.'+(t.fa&&byS[t.fa]?' Free option that does the same job: '+byS[t.fa].n+' ('+byS[t.fa].f+').':'')}}}});
return{{valid:valid,tot:info.tot,act:act}}}}
function renderResults(scroll=false){{const out=document.getElementById('a-out');const res=audit();const valid=res.valid;
if(!rows.length){{out.innerHTML='<div class="pick"><b>No tools added yet.</b><p class="small" style="margin-bottom:0">Add the tools you pay for above, check the amounts, and your checklist will appear here.</p></div>';return}}
if(!valid.length){{out.innerHTML='<div class="pick"><b>Add what you pay to finish the audit.</b><p class="small" style="margin-bottom:0">You added '+rows.length+' tool'+(rows.length==1?'':'s')+', but none has an amount yet, so we cannot work out spend or savings and we will not guess either.</p></div>';return}}
const items=valid.map(x=>({{x:x,a:res.act[x.t.s]||{{kind:'keep',save:0,reason:''}}}})).sort((a,b)=>(b.a.save-a.a.save)||a.x.t.n.localeCompare(b.x.t.n));
const potential=items.reduce((sum,i)=>sum+i.a.save,0);
const labels={{cancel:'CONSIDER CANCELLING',free:'TRY FREE TIER',switch:'SWITCH TO CHECK',keep:'KEEP'}};
let h='';
const firm=Math.round(items.filter(i=>i.a.kind=='cancel').reduce((m,i)=>m+i.a.save,0)*100)/100,upFree=Math.round(items.filter(i=>i.a.kind=='free').reduce((m,i)=>m+i.a.save,0)*100)/100,upSw=Math.round(items.filter(i=>i.a.kind=='switch').reduce((m,i)=>m+i.a.save,0)*100)/100;
if(potential>0){{h+=`<div class="pick"><p style="margin:0"><b>${{firm>0?'Firm saving if you cancel duplicates: '+money(firm)+'/mo ('+money(firm*12)+'/yr)':'Firm saving if you cancel duplicates: $0 — no duplicates found'}}</b></p>${{upFree>0?`<p style="margin:4px 0 0"><b>Up to ${{money(upFree)}}/mo more (${{money(upFree*12)}}/yr) if free tiers cover you</b> <span class="small">— not counted until you tick it, because only you know if the free limits are enough.</span></p>`:''}}${{upSw>0?`<p style="margin:4px 0 0"><b>Up to ${{money(upSw)}}/mo more (${{money(upSw*12)}}/yr) if you switch to a cheaper tool for the same job</b> <span class="small">— check the plans first.</span></p>`:''}}<p class="small" style="margin:6px 0 0">Current spend you told us: ${{money(res.tot)}}/mo (${{money(res.tot*12)}}/yr). Each tool gets one suggestion and is counted once. Tick the suggestions you will act on.</p><p class="small" id="a-plan" aria-live="polite" style="margin:8px 0 0"></p></div>`}}
else{{h+=`<div class="pick"><b>Already lean: no saving found on checked prices.</b><p class="small" style="margin-bottom:0">You told us you pay ${{money(res.tot)}}/mo (${{money(res.tot*12)}}/yr) across ${{valid.length}} tool${{valid.length==1?'':'s'}}. None of them do the same main job as another, none has a real free plan, and no tool that does the same job is cheaper on the same billing. We are not inventing a saving — re-check when prices change.</p></div>`}}
h+=items.map(i=>{{const t=i.x.t,a=i.a;const tickable=a.kind!='keep';
if(!(t.s in ticks))ticks[t.s]=a.kind!='free';
const extra=a.kind=='cancel'&&a.keeper?`<p class="small"><a href="/compare-builder.html?tools=${{t.s}},${{a.keeper.s}}">Compare ${{X(t.n)}} with ${{X(a.keeper.n)}} (the one to keep) →</a> · <a href="${{a.keeper.u}}">${{X(a.keeper.n)}} tool page</a></p>`:(a.kind=='switch'&&a.alt?`<p class="small"><a href="${{a.alt.u}}">See ${{X(a.alt.n)}} →</a> · <a href="/compare-builder.html?tools=${{t.s}},${{a.alt.s}}">Compare ${{X(t.n)}} with ${{X(a.alt.n)}} →</a> · <a href="${{X(a.alt.pr)}}" rel="noopener" target="_blank">${{X(a.alt.n)}} official pricing</a></p>`:'');
return `<article class="card ares${{a.save>0?' save':''}}" style="margin:12px 0"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${{t.dm}}&amp;sz=64" alt="${{X(t.n)}} logo" width="28" height="28" loading="lazy" onerror="this.replaceWith(document.createTextNode('${{X(t.n[0])}}'))"></span><div><div class="badges"><span class="badge ${{a.kind=='keep'?'b-rank':'b-best'}}">${{labels[a.kind]}}</span>${{t.fr?'<span class="badge b-free">FREE PLAN</span>':''}}</div><h3 style="margin:0"><a href="${{t.u}}">${{X(t.n)}}</a></h3></div></div><p class="small">You told us: <b>${{money(i.x.e)}}/mo</b>${{i.x.r.billing=='annual'?' (from '+money(parseFloat(i.x.r.amt)||0)+'/yr ÷ 12)':''}} · Our listed verified price: ${{X(t.p)}} (checked ${{t.k}}) · <a href="${{X(t.pr)}}" rel="noopener" target="_blank">Official pricing page</a></p><p>${{X(a.reason)}}</p><p><b>Potential saving from this one tool: ${{money(a.save)}}/mo</b>${{a.kind=='free'?' if the free plan covers you — check its limits on the official page':a.kind=='switch'?' (difference to the alternative\\u2019s verified entry price only)':a.kind=='cancel'?' (the full amount you told us, counted once)':''}}</p>${{extra}}<p class="small alinks"><a href="${{t.u}}">Tool page →</a> · <a href="/cost-calculator.html?tool=${{t.s}}&amp;seats=1&amp;billing=monthly">What will ${{X(t.n)}} really cost? →</a></p>${{tickable?`<label style="display:flex;gap:10px;align-items:flex-start;min-height:44px"><input type="checkbox" data-tick="${{t.s}}" data-save="${{a.save}}" ${{ticks[t.s]?'checked':''}} style="margin-top:4px"> <span>Count this in my plan — I will act on this suggestion (${{money(a.save)}}/mo)</span></label>`:'<p class="small">No saving counted for Keep.</p>'}}</article>`}}).join('');
const keepers=items.filter(i=>i.a.kind=='keep'||i.a.kind=='free').map(i=>i.x.t.s);const alts=items.filter(i=>i.a.kind=='switch'&&i.a.alt).map(i=>i.a.alt.s);const comp=[...new Set(keepers.concat(alts))].slice(0,3);
if(comp.length>=2)h+=`<p><a class="btn" href="/compare-builder.html?tools=${{comp.join(',')}}">Compare your keepers &amp; suggested switches →</a></p>`;
out.innerHTML=h;
function plan(){{let sum=0;out.querySelectorAll('[data-tick]').forEach(cb=>{{ticks[cb.dataset.tick]=cb.checked;if(cb.checked)sum+=parseFloat(cb.dataset.save)||0}});const el=document.getElementById('a-plan');if(el)el.innerHTML='<b>Your plan saves '+money(sum)+'/mo ('+money(sum*12)+'/yr)</b> from the suggestions you ticked.'}}
out.querySelectorAll('[data-tick]').forEach(cb=>cb.addEventListener('change',plan));plan();
if(scroll)out.scrollIntoView({{behavior:'smooth',block:'start'}})}}
document.getElementById('a-add').addEventListener('click',()=>{{const sel=document.getElementById('a-select');const st=document.getElementById('a-status');if(!sel.value){{st.textContent='Select a tool first, then Add tool.';sel.focus();return}}if(rows.some(r=>r.s==sel.value)){{st.textContent=byS[sel.value].n+' is already in your audit — edit its amount below.';const f=document.getElementById('amt-'+sel.value);if(f){{f.focus();f.select()}}return}}if(rows.length>=MAXROWS){{st.textContent='That is the maximum of '+MAXROWS+' tools for one audit. Remove one to add another.';return}}const t=byS[sel.value];const pf=prefill(t);rows.push({{s:t.s,amt:pf?String(pf.v):'',billing:'monthly',auto:!!pf,ref:pf?pf.v:null,rd:t.k}});renderRows(t.s);renderResults(false);syncURL();st.textContent=t.n+' added'+(pf?(' at our verified entry price — edit it if your plan differs.'):' — tell us what you pay.')}});
document.getElementById('a-search').addEventListener('input',ev=>{{const q=ev.target.value.toLowerCase();const sel=document.getElementById('a-select');[...sel.options].forEach((o,i)=>{{if(i==0)return;o.hidden=q?!o.textContent.toLowerCase().includes(q):false}});const first=[...sel.options].find(o=>!o.hidden&&o.value);if(first&&q)sel.value=first.value}});
document.getElementById('a-run').addEventListener('click',()=>{{renderResults(true);document.getElementById('a-status').textContent=rows.length?'Audit updated below.':'Add a tool first.'}});
document.getElementById('a-clear').addEventListener('click',()=>{{rows=[];Object.keys(ticks).forEach(k=>delete ticks[k]);renderRows();renderResults(false);syncURL();document.getElementById('a-status').textContent='Cleared. Add tools to start again.';document.getElementById('a-select').focus()}});
document.getElementById('a-copy').addEventListener('click',async()=>{{const st=document.getElementById('a-status');if(!rows.length){{st.textContent='Add at least one tool before copying a share link.';return}}const url=location.origin+sharePath();try{{await navigator.clipboard.writeText(url);st.textContent='Share link copied: '+url}}catch(err){{st.textContent='Copy this share link: '+url;window.prompt('Copy this share link',url)}}}});
(function init(){{const raw=new URLSearchParams(location.search).get('tools');if(raw==null){{renderRows();renderResults(false);return}}
const parts=raw.split(',').map(x=>x.trim()).filter(Boolean);let bad=0,junk=[],extra=0;const okNum=v=>v!=null&&/^\\d+(\\.\\d{{1,2}})?$/.test(v)&&parseFloat(v)<=AMAX;
parts.forEach((part,idx)=>{{const bits=part.split(':');const t=byS[bits[0]];if(!t){{bad++;return}}if(rows.some(r=>r.s==t.s))return;if(rows.length>=MAXROWS){{extra++;return}}
const pf=prefill(t);let own=false;if(bits[1]!=null&&bits[1]!==''){{if(okNum(bits[1]))own=true;else junk.push(t.n)}}
const rf=okNum(bits[3])?parseFloat(bits[3]):(pf?pf.v:null);rows.push({{s:t.s,amt:own?bits[1]:(pf?String(pf.v):''),billing:bits[2]=='annual'?'annual':'monthly',auto:!own&&!!pf,ref:rf,rd:bits[4]&&/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(bits[4])?bits[4]:t.k}})}});
const msg=[];if(!rows.length&&parts.length)msg.push('<b>This link is invalid.</b> None of its tools could be loaded, so there is nothing to restore. Start a new audit below.');
else{{if(bad+extra)msg.push('<b>This link was incomplete: '+(bad+extra)+' tool'+((bad+extra)==1?'':'s')+' couldn\u2019t load</b>'+(bad?' ('+bad+' not recognised'+(extra?', ':')'):(extra?' (':''))+(extra?extra+' over the '+MAXROWS+'-tool limit)':'')+'. The rest of your stack is shown below.');
if(junk.length)msg.push('<b>We ignored an amount we couldn\u2019t use</b> for '+X(junk.join(', '))+' (it was negative, not a number, or over $10,000). '+(junk.length==1?'It now shows':'They now show')+' our checked price instead — edit it if you pay something else.')}}
const m=document.getElementById('a-linkmsg');if(msg.length){{m.innerHTML=msg.map(x=>'<p style="margin:0">'+x+'</p>').join('');m.hidden=false}}
renderRows();renderResults(false);}})();
"""+V28_CARD_JS+"""</script>"""
page("/subscription-audit.html", "AI Subscription Audit — Keep, Cancel or Try the Free Tier in 60 Seconds | ToolPick", "List the AI tools you pay for and get a keep, consider cancelling, try the free tier or switch checklist with a potential saving counted once per tool, from verified ToolPick prices only. Runs in your browser.", audit_body,
     [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick AI Subscription Audit","url":BASE+"/subscription-audit.html","description":"60-second audit of paid AI subscriptions using verified prices, returning one action per tool with potential savings counted once."}, crumbs([("ToolPick","/"),("Subscription Audit","/subscription-audit.html")])])



# --- v30: Price watchlist (localStorage + share link; verified prices only) ---
WL_JS = r'''const WD=__WDATA__;const byS={};WD.forEach(t=>byS[t.s]=t);const K='tp_watch_v1',MAX=20;
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const M=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))};
const snap=t=>({m:t.m,a:t.a,k:t.k});
function load(){try{const w=JSON.parse(localStorage.getItem(K));if(w&&Array.isArray(w.t))return{t:w.t.filter(s=>byS[s]).slice(0,MAX),seen:w.seen||{},last:w.last||null}}catch(e){}return{t:[],seen:{},last:null}}
function save(w){try{localStorage.setItem(K,JSON.stringify(w));return true}catch(e){return false}}
let W=load(),shared=false,note='';
const okN=v=>v===''||v==null?null:(/^\d+(\.\d{1,2})?$/.test(v)&&parseFloat(v)<=10000?parseFloat(v):undefined);
(function fromURL(){const q=new URLSearchParams(location.search).get('w');if(q==null)return;const parts=q.split(',').map(x=>x.trim()).filter(Boolean);let bad=0;const t=[],seen={};
parts.forEach(p=>{const b=p.split(':');const tool=byS[b[0]];if(!tool||t.includes(tool.s)||t.length>=MAX){bad++;return}t.push(tool.s);const m=okN(b[1]),a=okN(b[2]);const k=/^\d{4}-\d{2}-\d{2}$/.test(b[3]||'')?b[3]:null;seen[tool.s]=(m===undefined||a===undefined||!k)?snap(tool):{m:m,a:a,k:k}});
if(!t.length){note='<b>This watchlist link is invalid.</b> None of its tools could be loaded. Add tools below to start your own.';return}
if(bad)note='<b>This link was incomplete: '+bad+' tool'+(bad==1?'':'s')+' couldn\u2019t load.</b> The rest are shown below.';shared=true;W={t:t,seen:seen,last:null}})();
const cv=(o,t,key)=>(key=='m'&&o.mf!=null&&!t.lt)?o.mf:o[key];
function cheaper(t,key){let best=null,bv=null;(t.al||[]).forEach(s=>{const o=byS[s];if(!o)return;const v=cv(o,t,key);if(v==null||t[key]==null||v>=t[key])return;if(!best||v<bv||(v==bv&&o.n<best.n)){best=o;bv=v}});return best?{o:best,v:bv,tier:(key=='m'&&best.mf!=null&&!t.lt)?best.mp:null}:null}
function priceTxt(m,a){return [m!=null?M(m)+'/mo monthly':'',a!=null?M(a)+'/mo billed yearly':''].filter(Boolean).join(' · ')||'no checked US-dollar price'}
function status(t){const s=W.seen[t.s];if(!s)return{kind:'new',html:'Just added.'};
const ch=(s.m!==t.m)||(s.a!==t.a);if(ch)return{kind:'changed',html:'<b>Price changed since you last looked.</b> Was '+X(priceTxt(s.m,s.a))+' (checked '+X(s.k)+'), now '+X(priceTxt(t.m,t.a))+' (checked '+X(t.k)+').'};
if(s.k!==t.k)return{kind:'rechecked',html:'Re-checked on '+X(t.k)+': same price as when you last looked ('+X(s.k)+').'};return{kind:'same',html:'No change since you last looked (checked '+X(t.k)+').'}}
function card(t){const st=status(t);const cm=cheaper(t,'m'),ca=cheaper(t,'a');const last=t.ch&&t.ch[0];
const alt=[cm?'Monthly: <a href="'+cm.o.u+'">'+X(cm.o.n)+(cm.tier?' ('+X(cm.tier)+')':'')+'</a> at '+M(cm.v)+'/mo, '+M(t.m-cm.v)+'/mo less':'',ca?'Billed yearly: <a href="'+ca.o.u+'">'+X(ca.o.n)+'</a> at '+M(ca.v)+'/mo, '+M(t.a-ca.v)+'/mo less':''].filter(Boolean);
return `<article class="card wl-card${st.kind=='changed'?' wl-chg':''}"><div class="badges">${st.kind=='changed'?'<span class="badge b-best">PRICE CHANGED</span>':''}${t.fr?'<span class="badge b-free">FREE PLAN</span>':''}</div><h3 style="margin:4px 0"><a href="${t.u}">${X(t.n)}</a></h3><p class="small" style="margin:0">Main job: ${X(t.cl)}</p>
<p class="wl-price"><b>${X(priceTxt(t.m,t.a))}</b></p><p class="small">${X(t.p)}<br>Checked ${X(t.k)} · <a href="${X(t.pr)}" rel="noopener" target="_blank">Official pricing page</a></p>
<p class="wl-st" role="status">${st.html}</p>${last?`<p class="small">Last change we recorded: ${X(last.label)} on ${X(last.d)} — <a href="/price-changes.html#${last.d}-${t.s}">before and after</a></p>`:'<p class="small">No price change recorded since we started tracking.</p>'}
<p class="small"><b>Cheaper for the same job, same billing:</b> ${alt.length?alt.join(' · '):'none checked'}</p>
<p class="small"><a href="/pay-less.html?tool=${t.s}">Can I pay less?</a> · <button type="button" class="linkbtn" data-rm="${t.s}">Stop watching ${X(t.n)}</button></p></article>`}
function shareURL(){return location.origin+'/watchlist.html?w='+W.t.map(s=>{const v=W.seen[s]||snap(byS[s]);return s+':'+(v.m==null?'':v.m)+':'+(v.a==null?'':v.a)+':'+v.k}).join(',')+(SORT!='added'?'&sort='+SORT:'')}
function render(){const out=document.getElementById('wl-out');const msg=document.getElementById('wl-msg');
let banner=note;if(shared)banner+=(banner?'<br>':'')+'You opened a watchlist link. Prices are re-checked against our latest data. <button type="button" class="bbtn" id="wl-keep">Keep this list in my browser</button>';
msg.innerHTML=banner;msg.hidden=!banner;const k=document.getElementById('wl-keep');if(k)k.onclick=()=>{shared=false;note='';save(W);history.replaceState(null,'','/watchlist.html');say('Saved in this browser.');render()};
document.querySelectorAll('[data-needs]').forEach(b=>b.disabled=!W.t.length);
if(!W.t.length){out.innerHTML='<div class="pick"><b>Your watchlist is empty.</b><p class="small" style="margin-bottom:0">Add the AI tools you pay for or are thinking about. Come back any time: we show which prices changed since you last looked, using the prices we check on official pricing pages.</p></div>';document.getElementById('wl-sum').textContent='';return}
const items=W.t.map(s=>byS[s]);const nC=items.filter(t=>status(t).kind=='changed').length;
document.getElementById('wl-sum').innerHTML='<b>'+items.length+' tool'+(items.length==1?'':'s')+' watched · '+(nC?nC+' price change'+(nC==1?'':'s')+' since you last looked':'no price changes since you last looked')+'</b>'+(W.last&&!shared?' <span class="small">(last marked as seen '+X(W.last)+')</span>':'');
out.innerHTML=sorted(items).map(card).join('');
out.querySelectorAll('[data-rm]').forEach(b=>b.onclick=()=>{W.t=W.t.filter(x=>x!=b.dataset.rm);delete W.seen[b.dataset.rm];persist();say(byS[b.dataset.rm].n+' removed.');render();document.getElementById('wl-sel').focus()})}
const SK='tp_watch_sort_v1',SORTS=['added','name','price','changed'];let SORT=(function(){const q=new URLSearchParams(location.search).get('sort');if(SORTS.includes(q))return q;try{const v=localStorage.getItem(SK);if(SORTS.includes(v))return v}catch(e){}return 'added'})();
const pv=t=>t.m!=null?t.m:(t.a!=null?1e6+t.a:Infinity);
function sorted(items){const idx=s=>W.t.indexOf(s);const a=items.slice();
if(SORT=='name')a.sort((x,y)=>x.n.localeCompare(y.n));else if(SORT=='price')a.sort((x,y)=>pv(x)-pv(y)||idx(x.s)-idx(y.s));else if(SORT=='changed')a.sort((x,y)=>(status(y).kind=='changed')-(status(x).kind=='changed')||idx(x.s)-idx(y.s));return a}
function persist(){if(!shared)save(W);else history.replaceState(null,'',shareURL().replace(location.origin,''))}
function say(m){document.getElementById('wl-status').textContent=m}
document.getElementById('wl-add').onclick=()=>{const s=document.getElementById('wl-sel').value;if(!s){say('Choose a tool first.');document.getElementById('wl-sel').focus();return}if(W.t.includes(s)){say(byS[s].n+' is already on your watchlist.');return}if(W.t.length>=MAX){say('That is the limit of '+MAX+' tools. Remove one first.');return}W.t.push(s);W.seen[s]=snap(byS[s]);persist();say(byS[s].n+' added at '+priceTxt(byS[s].m,byS[s].a)+'.');render()};
document.getElementById('wl-seen').onclick=()=>{W.t.forEach(s=>W.seen[s]=snap(byS[s]));W.last=new Date().toLocaleDateString('en-CA');persist();say('Marked as seen. Next time, we will flag anything that changes from today\u2019s prices.');render()};
document.getElementById('wl-copy').onclick=async()=>{const u=shareURL();try{await navigator.clipboard.writeText(u);say('Link copied. Bookmark it or share it: it re-checks these tools against our latest prices when opened.')}catch(e){say('Copy this link: '+u);window.prompt('Copy this link',u)}};
const DLG=document.getElementById('wl-dlg'),TOAST=document.getElementById('wl-toast');let undoT=null,undoS=null;
function doClear(){undoS={W:JSON.parse(JSON.stringify(W)),shared:shared,note:note,url:location.pathname+location.search};W={t:[],seen:{},last:null};shared=false;note='';save(W);history.replaceState(null,'','/watchlist.html');say('');render();
const n=undoS.W.t.length;TOAST.innerHTML='<span id="wl-tmsg">Watchlist cleared ('+n+' tool'+(n==1?'':'s')+').</span><button type="button" id="wl-undo">Undo</button><button type="button" id="wl-tx" class="tx" aria-label="Dismiss">&times;</button>';document.getElementById('wl-undo').onclick=undo;document.getElementById('wl-tx').onclick=dismiss;TOAST.hidden=false;TOAST.style.display='flex';document.getElementById('wl-undo').focus();clearTimeout(undoT);
// phones: stay until dismissed; desktop: 15 seconds
if(!matchMedia('(pointer:coarse), (max-width:760px)').matches)undoT=setTimeout(hideToast,15000)}
function hideToast(){TOAST.hidden=true;TOAST.style.display='none';TOAST.innerHTML='';undoS=null;clearTimeout(undoT)}
function dismiss(){hideToast();say('Watchlist cleared.');document.getElementById('wl-clear').focus()};
function undo(){if(!undoS)return;W=undoS.W;shared=undoS.shared;note=undoS.note;if(!shared)save(W);history.replaceState(null,'',undoS.url);const n=W.t.length;hideToast();render();say('Restored '+n+' tool'+(n==1?'':'s')+' with your saved baseline prices.');document.getElementById('wl-clear').focus()};
document.getElementById('wl-clear').onclick=()=>{const n=W.t.length;document.getElementById('wl-dmsg').textContent='This removes all '+n+' tool'+(n==1?'':'s')+' and the prices you were comparing against. You can undo it afterwards.';
if(DLG&&typeof DLG.showModal=='function'){DLG.returnValue='';DLG.showModal();document.getElementById('wl-dno').focus()}else if(window.confirm('Clear your whole watchlist?'))doClear()};
if(DLG){document.getElementById('wl-dno').onclick=()=>DLG.close('no');document.getElementById('wl-dyes').onclick=()=>DLG.close('yes');DLG.addEventListener('close',()=>{if(DLG.returnValue=='yes')doClear();else document.getElementById('wl-clear').focus()})}
const SEL=document.getElementById('wl-sort');SEL.value=SORT;SEL.onchange=()=>{SORT=SEL.value;try{localStorage.setItem(SK,SORT)}catch(e){}if(shared)persist();say('Sorted by '+SEL.options[SEL.selectedIndex].text.toLowerCase()+'.');render()};
const pre=new URLSearchParams(location.search).get('add');if(pre&&byS[pre]&&!shared&&!W.t.includes(pre)&&W.t.length<MAX){W.t.push(pre);W.seen[pre]=snap(byS[pre]);save(W);history.replaceState(null,'','/watchlist.html');say(byS[pre].n+' added to your watchlist.')}
render();
'''

_wl = []
for _v in sorted(_amap.values(), key=lambda x: x["n"].lower()):
    _wl.append(dict(s=_v["s"], n=_v["n"], u=_v["u"], pr=_v["pr"], p=_v["p"], k=_v["k"], m=_v["mm"], a=_v["ma"], cl=_v["cl"], al=_v["al"], fr=_v["fr"], lt=bool(_v.get("lt")), mf=_v.get("mf"), mp=_v.get("mp"),
                    ch=[dict(d=c["date"], label=c["label"]) for c in CHANGES_BY_TOOL.get(_v["n"], [])]))
_WLDATA = json.dumps(_wl).replace("</", "<\\/")
_WLOPTS = "".join(f'<option value="{e(v["s"])}">{e(v["n"])}</option>' for v in _wl)
_wl_body = f"""<style>.wl-grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}.wl-card.wl-chg{{border-color:var(--warn);border-width:2px}}.wl-price{{margin:8px 0 4px}}.wl-st{{background:var(--sf2);border-radius:8px;padding:8px 10px;margin:8px 0}}#wl-dlg{{border:1px solid var(--bd);border-radius:12px;padding:18px;max-width:min(92vw,420px);background:var(--sf,#fff);color:var(--tx)}}#wl-dlg::backdrop{{background:rgba(15,23,42,.55)}}#wl-toast{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;background:#0f172a;color:#fff;border-radius:10px;padding:10px 14px;display:flex;gap:12px;align-items:center;box-shadow:0 6px 24px rgba(0,0,0,.3);max-width:92vw}}#wl-toast[hidden]{{display:none}}#wl-toast .tx{{background:transparent!important;color:#fff!important;font-size:1.4rem;line-height:1;padding:4px 10px!important;min-width:44px;min-height:44px!important}}#wl-toast button{{background:#fff;color:#0f172a;border:0;border-radius:6px;padding:6px 12px;font-weight:700;cursor:pointer;min-height:36px}}.linkbtn{{background:none;border:0;padding:0;color:var(--ac);text-decoration:underline;cursor:pointer;font:inherit;min-height:24px}}</style>
<p class="small"><a href="/save-money.html">Save money</a> › Price watchlist</p><h1>My AI price watchlist</h1><p class="tag">Watch the AI tools you pay for. Come back any time and see which prices changed since you last looked, plus any cheaper tool for the same job on the same billing. Prices come only from official pricing pages, each with its checked date.</p>
<div class="bnote"><p class="small" style="margin:0"><b>No account, no email.</b> Your list is saved only in this browser (local storage) and in the link if you copy one. Want updates in a feed reader? Follow <a href="/price-changes.xml">our price-changes feed</a> (Atom) or the <a href="/price-changes.html">price changes log</a>.</p></div>
<div class="pick" id="wl-msg" role="alert" hidden></div>
<div class="builder"><div class="aform"><div><label for="wl-sel">Add a tool</label><select id="wl-sel"><option value="">Choose a tool…</option>{_WLOPTS}</select></div><button type="button" class="bbtn primary" id="wl-add">Watch this tool</button></div>
<div class="bactions"><button type="button" class="bbtn" id="wl-seen" data-needs>Mark all as seen</button><button type="button" class="bbtn" id="wl-copy" data-needs>Copy watchlist link</button><button type="button" class="bbtn" id="wl-clear" data-needs>Clear list</button><span class="small bstatus" id="wl-status" role="status"></span></div>
<p id="wl-sum" aria-live="polite"></p></div>
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px"><h2 style="margin:0">Your watched tools</h2><p style="margin:0"><label for="wl-sort">Sort</label> <select id="wl-sort"><option value="added">Order added</option><option value="name">Name (A–Z)</option><option value="price">Monthly price (lowest first)</option><option value="changed">Changed first</option></select></p></div><div id="wl-out" class="wl-grid" aria-live="polite"></div><dialog id="wl-dlg" aria-labelledby="wl-dh" aria-describedby="wl-dmsg"><h2 id="wl-dh" style="margin-top:0;font-size:1.15rem">Clear your watchlist?</h2><p id="wl-dmsg"></p><div style="display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap"><button type="button" class="bbtn" id="wl-dno">Cancel</button><button type="button" class="bbtn primary" id="wl-dyes">Yes, clear list</button></div></dialog><div id="wl-toast" role="status" aria-live="polite" hidden style="display:none"></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How the watchlist works</h2><p class="small" style="margin:0">When you add a tool we remember the price we had checked at that moment. Each visit compares that with our latest checked price and flags any change; “Mark all as seen” resets the comparison to today’s prices. “Cheaper for the same job” only compares tools that do the same main job, monthly with monthly and billed-yearly with billed-yearly. We never guess a price: tools without a checked US-dollar price say so.</p></div>
<script>""" + WL_JS.replace("__WDATA__", _WLDATA) + """</script>"""
page("/watchlist.html", "AI Price Watchlist — See Which AI Tool Prices Changed | ToolPick",
     "Watch the AI tools you pay for and see which prices changed since you last looked, plus cheaper tools for the same job on the same billing. Verified prices, no account, no email.",
     _wl_body, [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick AI price watchlist","url":BASE+"/watchlist.html"}, crumbs([("ToolPick","/"),("Save money","/save-money.html"),("Price watchlist","/watchlist.html")])])

# --- v34: Renewal reminders (calendar file / Google Calendar; localStorage + share link; verified prices only) ---
RR_DATE = "2026-10-20"
RR_JS = r'''const WD=__WDATA__;const byS={};WD.forEach(t=>byS[t.s]=t);const K='tp_renew_v1',MAX=20,B=__BASE__;
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const M=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?String(r):r.toFixed(2))};
const $=id=>document.getElementById(id);const pad=n=>String(n).padStart(2,'0');
const iso=d=>d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
function pd(s){if(!/^\d{4}-\d{2}-\d{2}$/.test(s||''))return null;const [y,m,d]=s.split('-').map(Number);const x=new Date(y,m-1,d);return(x.getFullYear()==y&&x.getMonth()==m-1&&x.getDate()==d)?x:null}
function addP(d,b,n){const x=new Date(d.getFullYear(),d.getMonth()+(b=='m'?n:12*n),1);const last=new Date(x.getFullYear(),x.getMonth()+1,0).getDate();x.setDate(Math.min(d.getDate(),last));return x}
const today=()=>{const t=new Date();return new Date(t.getFullYear(),t.getMonth(),t.getDate())};
function nextDate(r){const d0=pd(r.d);if(!d0)return null;let k=0,d=d0;while(d<today()&&k<400){k++;d=addP(d0,r.b,k)}return d}
const okN=v=>v===''||v==null?null:(/^\d+(\.\d{1,2})?$/.test(v)&&parseFloat(v)<=10000?parseFloat(v):undefined);
let R=[],LEAD=3,shared=false,note='';
function load(){try{const w=JSON.parse(localStorage.getItem(K));if(w&&Array.isArray(w.r)){LEAD=[1,3,7].includes(w.lead)?w.lead:3;R=w.r.filter(r=>byS[r.s]&&pd(r.d)&&(r.b=='m'||r.b=='y')).slice(0,MAX).map(r=>({...r,l:[1,3,7].includes(r.l)?r.l:LEAD}))}}catch(e){}}
function save(){if(shared)return;try{localStorage.setItem(K,JSON.stringify({r:R,lead:LEAD}))}catch(e){}}
load();
(function fromURL(){const q=new URLSearchParams(location.search);const v=q.get('r');if(v==null)return;let bad=0;const out=[];
const l=parseInt(q.get('lead'));if([1,3,7].includes(l))LEAD=l;
v.split(',').filter(Boolean).forEach(p=>{const b=p.split(':');const t=byS[b[0]];const pay=okN(b[3]);const li=parseInt(b[4]);if(!t||!(b[1]=='m'||b[1]=='y')||!pd(b[2])||pay===undefined||out.length>=MAX||out.some(r=>r.s==t.s)){bad++;return}out.push({s:t.s,b:b[1],d:b[2],p:pay,l:[1,3,7].includes(li)?li:LEAD})});
if(!out.length){note='<b>This reminders link is invalid.</b> None of its subscriptions could be loaded.';return}
if(bad)note='<b>This link was incomplete: '+bad+' entr'+(bad==1?'y':'ies')+' couldn\u2019t load.</b> The rest are shown below.';shared=true;R=out})();
const cv=(o,t,key)=>(key=='m'&&o.mf!=null&&!t.lt)?o.mf:o[key];
function cheaper(t,key){let best=null,bv=null;(t.al||[]).forEach(s=>{const o=byS[s];if(!o)return;const v=cv(o,t,key);if(v==null||t[key]==null||v>=t[key])return;if(!best||v<bv||(v==bv&&o.n<best.n)){best=o;bv=v}});return best?{o:best,v:bv,tier:(key=='m'&&best.mf!=null&&!t.lt)?best.mp:null}:null}
const bl=b=>b=='m'?'monthly':'yearly';
function info(r){const t=byS[r.s],key=r.b=='m'?'m':'a',ck=t[key];const c=cheaper(t,key);const nd=nextDate(r);
// prices are per month; a yearly renewal charges 12x. The user's own price (r.p) is used for totals and reminder text.
const per=r.b=='m'?'/mo':'/mo billed yearly';const amt=v=>r.b=='m'?M(v)+'/mo':M(v)+'/mo billed yearly ('+M(v*12)+' per year)';
const yours=r.p!=null?r.p:null,use=yours!=null?yours:ck;const charge=use!=null?(r.b=='m'?M(use):M(use*12)+' per year'):null;
let price;if(yours!=null){price='Your price: '+amt(yours)+(ck!=null?(Math.abs(yours-ck)>0.005?' (our checked price is '+M(ck)+per+', checked '+t.k+', so check which plan you are on)':' (matches our checked price, checked '+t.k+')'):'')}
else price=ck!=null?'Our checked price: '+amt(ck)+', checked '+t.k:'We have no checked '+bl(r.b)+' US-dollar price for '+t.n+'; enter what you pay to include it in your totals';
const alt=c?'Cheaper for the same job ('+t.cl+'), same '+bl(r.b)+' billing: '+c.o.n+(c.tier?' ('+c.tier+')':'')+' at '+M(c.v)+per+', '+M(ck-c.v)+per+' less than our checked '+t.n+' price':(ck!=null?'No cheaper tool checked for the same job on '+bl(r.b)+' billing':'');
return{t:t,nd:nd,price:price,alt:alt,c:c,ck:ck,charge:charge}}
function shareURL(){return B+'/renewal-reminders.html?r='+R.map(r=>r.s+':'+r.b+':'+r.d+':'+(r.p==null?'':r.p)+':'+r.l).join(',')}
function summary(r,i){return 'Renewal: '+i.t.n+' ('+bl(r.b)+(i.charge?', '+i.charge:'')+')'}
function details(r,i){return [i.t.n+' renews '+bl(r.b)+(i.nd?' on '+i.nd.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}):'')+'. Keep, downgrade or cancel?','Alert: '+r.l+' day'+(r.l==1?'':'s')+' before.',i.price+'.',i.alt?i.alt+'.':'','Official pricing page: '+i.t.pr,'Re-check prices on ToolPick: '+B+i.t.u,'Your reminders: '+shareURL()].filter(Boolean).join('\n')}
function gcal(r,i){const d=new Date(i.nd.getFullYear(),i.nd.getMonth(),i.nd.getDate()-r.l),e=new Date(d.getFullYear(),d.getMonth(),d.getDate()+1),f=x=>iso(x).replace(/-/g,'');
return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(i.t.n+' renews in '+r.l+' day'+(r.l==1?'':'s')+' ('+bl(r.b)+(i.charge?', '+i.charge:'')+')')+'&dates='+f(d)+'/'+f(e)+'&details='+encodeURIComponent(details(r,i))+'&recur='+encodeURIComponent('RRULE:FREQ='+(r.b=='m'?'MONTHLY':'YEARLY'))}
function esc(s){return String(s).replace(/\\/g,'\\\\').replace(/;/g,'\\;').replace(/,/g,'\\,').replace(/\r?\n/g,'\\n')}
function fold(l){const out=[];let cur='',n=0;for(const ch of l){const b=new TextEncoder().encode(ch).length;if(n+b>(out.length?74:75)){out.push(cur);cur='';n=0}cur+=ch;n+=b}out.push(cur);return out.join('\r\n ')}
function ics(){const st=new Date().toISOString().replace(/[-:]/g,'').replace(/\.\d+/,'');const L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolPick//Renewal reminders//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:AI subscription renewals (ToolPick)'];
R.forEach(r=>{const i=info(r);if(!i.nd)return;const d=iso(i.nd).replace(/-/g,''),e=iso(new Date(i.nd.getFullYear(),i.nd.getMonth(),i.nd.getDate()+1)).replace(/-/g,'');const dom=i.nd.getDate();
L.push('BEGIN:VEVENT','UID:'+r.s+'-'+r.b+'-'+d+'@toolpick-ai.vercel.app','DTSTAMP:'+st,'DTSTART;VALUE=DATE:'+d,'DTEND;VALUE=DATE:'+e,'RRULE:FREQ='+(r.b=='m'?(dom>28?'MONTHLY;BYMONTHDAY=-1':'MONTHLY'):'YEARLY'),'SUMMARY:'+esc(summary(r,i)),'DESCRIPTION:'+esc(details(r,i)),'URL:'+B+i.t.u,'TRANSP:TRANSPARENT',
'BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+esc(i.t.n+' renews in '+r.l+' day'+(r.l==1?'':'s')),'TRIGGER:-P'+r.l+'D','END:VALARM','END:VEVENT')});L.push('END:VCALENDAR');return L.map(fold).join('\r\n')+'\r\n'}
function say(m){$('rr-status').textContent=m}
function render(){$('rr-msg').innerHTML=note+(shared?(note?'<br>':'')+'You opened a reminders link. <button type="button" class="bbtn" id="rr-keep">Keep these in my browser</button>':'');$('rr-msg').hidden=!(note||shared);
const k=$('rr-keep');if(k)k.onclick=()=>{shared=false;note='';save();history.replaceState(null,'','/renewal-reminders.html');say('Saved in this browser.');render()};
document.querySelectorAll('[data-needs]').forEach(b=>b.disabled=!R.length);$('rr-lead').value=String(LEAD);
const out=$('rr-out');if(!R.length){out.innerHTML='<div class="pick"><b>No subscriptions yet.</b><p class="small" style="margin-bottom:0">Add the AI tools you pay for and when they next renew. You get a calendar reminder before each renewal, with our latest checked price and any cheaper tool for the same job.</p></div>';$('rr-sum').textContent='';return}
const rows=R.map(r=>({r:r,i:info(r)})).sort((a,b)=>a.i.nd-b.i.nd);
let mo=0,yr=0,unk=0,own=0;R.forEach(r=>{const t=byS[r.s],v=r.p!=null?r.p:(r.b=='m'?t.m:t.a);if(v==null){unk++;return}if(r.p!=null)own++;if(r.b=='m')mo+=v;else yr+=v*12});
$('rr-sum').innerHTML='<b>'+R.length+' subscription'+(R.length==1?'':'s')+' · next renewal '+X(rows[0].i.nd.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}))+' ('+X(rows[0].i.t.n)+')</b>'+(mo?'<br>Monthly renewals: '+M(mo)+'/mo':'')+(yr?'<br>Yearly renewals: '+M(yr)+' per year':'')+(own?'<br><span class="small">Includes your price for '+own+' subscription'+(own==1?'':'s')+'; others use our checked price.</span>':'')+(unk?'<br><span class="small">'+unk+' without a checked or entered price, not counted.</span>':'');
out.innerHTML=rows.map(({r,i})=>{const days=Math.round((i.nd-today())/864e5);return `<article class="card rr-card"><h3 style="margin:4px 0"><a href="${i.t.u}">${X(i.t.n)}</a></h3><p class="small" style="margin:0">Main job: ${X(i.t.cl)} · billed ${bl(r.b)}</p>
<p class="rr-when"><b>Renews ${X(i.nd.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}))}</b> <span class="small">(${days==0?'today':days==1?'tomorrow':'in '+days+' days'})</span></p>
<p class="small">${X(i.price)}. <a href="${X(i.t.pr)}" rel="noopener" target="_blank">Official pricing page</a></p>${i.alt?`<p class="small"><b>${i.c?'Before you renew:':'Checked:'}</b> ${i.c?X(i.alt).replace(X(i.c.o.n),'<a href="'+i.c.o.u+'">'+X(i.c.o.n)+'</a>'):X(i.alt)}.</p>`:''}
<p class="small"><label for="rl-${r.s}">Alert for ${X(i.t.n)}</label> <select id="rl-${r.s}" data-lead="${r.s}">${[1,3,7].map(n=>`<option value="${n}"${n==r.l?' selected':''}>${n} day${n==1?'':'s'} before</option>`).join('')}</select></p>
<p class="small"><a href="${X(gcal(r,i))}" target="_blank" rel="noopener">Add to Google Calendar</a> · <a href="/pay-less.html?tool=${r.s}">Can I pay less?</a> · <button type="button" class="linkbtn" data-rm="${r.s}">Remove</button></p></article>`}).join('');
out.querySelectorAll('[data-lead]').forEach(sel=>sel.onchange=()=>{const r=R.find(x=>x.s==sel.dataset.lead);r.l=parseInt(sel.value);persist();say(byS[r.s].n+': alert '+r.l+' day'+(r.l==1?'':'s')+' before. Download the calendar file again to update your calendar.');render();const n=document.getElementById('rl-'+r.s);if(n)n.focus()});
out.querySelectorAll('[data-rm]').forEach(b=>b.onclick=()=>{R=R.filter(r=>r.s!=b.dataset.rm);persist();say(byS[b.dataset.rm].n+' removed.');render();$('rr-sel').focus()})}
function persist(){if(shared)history.replaceState(null,'',shareURL().replace(B,''));else save()}
function fillPay(){const t=byS[$('rr-sel').value];const b=$('rr-bill').value;const v=t?(b=='m'?t.m:t.a):null;$('rr-pay').placeholder=v!=null?String(v):'e.g. 20';
$('rr-hint').textContent=t?(v!=null?'Our checked '+bl(b)+' price: '+M(v)+(b=='m'?'/mo':'/mo billed yearly ('+M(v*12)+' per year)')+', checked '+t.k+'.':'We have no checked '+bl(b)+' US-dollar price for '+t.n+'. Enter what you pay and we will use your price.'):''}
$('rr-sel').onchange=fillPay;$('rr-bill').onchange=fillPay;
$('rr-add').onclick=()=>{const s=$('rr-sel').value,b=$('rr-bill').value,d=$('rr-date').value,pv=$('rr-pay').value.trim();
if(!s){say('Choose a tool first.');$('rr-sel').focus();return}if(!pd(d)){say('Enter the next renewal date.');$('rr-date').focus();return}
const x=pd(d);if(x>addP(today(),'y',2)){say('Use a date within the next two years.');$('rr-date').focus();return}
const p=okN(pv);if(p===undefined){say('Enter what you pay as a number, like 20 or 9.99, or leave it blank.');$('rr-pay').focus();return}
if(R.length>=MAX&&!R.some(r=>r.s==s)){say('That is the limit of '+MAX+'. Remove one first.');return}
R=R.filter(r=>r.s!=s);R.push({s:s,b:b,d:d,p:p,l:LEAD});persist();const nd=nextDate({s:s,b:b,d:d});
say(byS[s].n+' added. Next renewal '+nd.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})+(x<today()?' (that date has passed, so we moved it to the next '+bl(b)+' renewal)':'')+'.');$('rr-pay').value='';render()};
$('rr-lead').onchange=()=>{LEAD=parseInt($('rr-lead').value);persist();say('New reminders will alert '+LEAD+' day'+(LEAD==1?'':'s')+' before. Change any existing one on its card.')};
$('rr-ics').onclick=()=>{const blob=new Blob([ics()],{type:'text/calendar;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ai-subscription-renewals.ics';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);
say('Calendar file downloaded. Open it to add '+R.length+' repeating reminder'+(R.length==1?'':'s')+', each with its own alert, to Apple Calendar, Outlook or Google Calendar.')};
$('rr-copy').onclick=async()=>{const u=shareURL();try{await navigator.clipboard.writeText(u);say('Link copied. Bookmark it to come back and re-check prices before you renew.')}catch(e){say('Copy this link: '+u)}};
const DLG=$('rr-dlg');let undoS=null,undoT=null;
function doClear(){undoS={R:R.slice(),shared:shared,url:location.pathname+location.search};R=[];shared=false;note='';save();history.replaceState(null,'','/renewal-reminders.html');render();showToast(true);$('rr-undo').focus();clearTimeout(undoT);undoT=setTimeout(()=>{showToast(false);undoS=null},8000)}
function showToast(on){const T=$('rr-toast');T.innerHTML=on?'<span id="rr-tmsg">Subscriptions cleared.</span><button type="button" id="rr-undo">Undo</button>':'';T.hidden=!on;T.style.display=on?'flex':'none';if(on)$('rr-undo').onclick=undo}
const undo=()=>{if(!undoS)return;R=undoS.R;shared=undoS.shared;if(!shared)save();history.replaceState(null,'',undoS.url);undoS=null;clearTimeout(undoT);showToast(false);render();say('Restored.');$('rr-clear').focus()};
$('rr-clear').onclick=()=>{if(DLG&&typeof DLG.showModal=='function'){DLG.returnValue='';DLG.showModal();$('rr-dno').focus()}else if(window.confirm('Remove all subscriptions?'))doClear()};
if(DLG){$('rr-dno').onclick=()=>DLG.close('no');$('rr-dyes').onclick=()=>DLG.close('yes');DLG.addEventListener('close',()=>{if(DLG.returnValue=='yes')doClear();else $('rr-clear').focus()})}
const pre=new URLSearchParams(location.search).get('add');if(pre&&byS[pre]){$('rr-sel').value=pre;fillPay()}
$('rr-date').min=iso(addP(today(),'y',-2));$('rr-date').max=iso(addP(today(),'y',2));
render();
'''
_rr_body = f"""<style>.rr-grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}.rr-when{{margin:8px 0 4px}}.linkbtn{{background:none;border:0;padding:0;color:var(--ac);text-decoration:underline;cursor:pointer;font:inherit;min-height:24px}}#rr-dlg{{border:1px solid var(--bd);border-radius:12px;padding:18px;max-width:min(92vw,420px);color:var(--tx)}}#rr-dlg::backdrop{{background:rgba(15,23,42,.55)}}#rr-toast{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;background:#0f172a;color:#fff;border-radius:10px;padding:10px 14px;display:flex;gap:12px;align-items:center;max-width:92vw}}#rr-toast[hidden]{{display:none}}#rr-toast button{{background:#fff;color:#0f172a;border:0;border-radius:6px;padding:6px 12px;font-weight:700;min-height:36px}}.rr-form{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));align-items:end}}.rr-form input,.rr-form select{{width:100%}}</style>
<p class="small"><a href="/save-money.html">Save money</a> › Renewal reminders</p><h1>AI subscription renewal reminders</h1><p class="tag">Get a calendar reminder a few days before each AI subscription renews, with our latest checked price and any cheaper tool for the same job, so you can keep, switch or cancel before you're charged.</p>
<div class="bnote"><p class="small" style="margin:0"><b>No account, no email.</b> Reminders go into your own calendar (a downloadable calendar file, or Google Calendar). Your list is saved only in this browser and in the link if you copy one.</p></div>
<div class="pick" id="rr-msg" role="alert" hidden></div>
<div class="builder"><div class="rr-form">
<div><label for="rr-sel">Tool you pay for</label><select id="rr-sel"><option value="">Choose a tool…</option>{_WLOPTS}</select></div>
<div><label for="rr-bill">Billing</label><select id="rr-bill"><option value="m">Monthly</option><option value="y">Yearly</option></select></div>
<div><label for="rr-date">Next renewal date</label><input type="date" id="rr-date"></div>
<div><label for="rr-pay">What you pay per month (optional)</label><input id="rr-pay" inputmode="decimal" autocomplete="off" aria-describedby="rr-hint"></div>
<button type="button" class="bbtn primary" id="rr-add">Add reminder</button></div><p class="small" id="rr-hint" style="margin:6px 0 0"></p>
<div class="bactions"><label for="rr-lead" class="small">Default alert for new reminders</label> <select id="rr-lead"><option value="1">1 day before</option><option value="3">3 days before</option><option value="7">7 days before</option></select>
<button type="button" class="bbtn primary" id="rr-ics" data-needs>Download calendar file (.ics)</button><button type="button" class="bbtn" id="rr-copy" data-needs>Copy reminders link</button><button type="button" class="bbtn" id="rr-clear" data-needs>Clear all</button><span class="small bstatus" id="rr-status" role="status"></span></div>
<p id="rr-sum" aria-live="polite"></p></div>
<h2>Upcoming renewals</h2><div id="rr-out" class="rr-grid" aria-live="polite"></div>
<dialog id="rr-dlg" aria-labelledby="rr-dh"><h2 id="rr-dh" style="margin-top:0;font-size:1.15rem">Remove all subscriptions?</h2><p>This clears the list in this browser. Reminders already added to your calendar stay there. You can undo for a few seconds.</p><div style="display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap"><button type="button" class="bbtn" id="rr-dno">Cancel</button><button type="button" class="bbtn primary" id="rr-dyes">Yes, clear all</button></div></dialog>
<div id="rr-toast" role="status" aria-live="polite" hidden style="display:none"></div>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How it works</h2><p class="small" style="margin:0">Each reminder repeats every month or every year on your renewal date, with an alert 1, 3 or 7 days before (set per reminder: the calendar file adds the alert, and Google Calendar links place the event on the alert day). Prices come only from each tool's official pricing page with its checked date. “Cheaper for the same job” compares only tools with the same main job on the same billing (monthly with monthly, yearly with yearly), and lighter entry tiers are compared at their comparable tier. Yearly prices are shown per month, plus the yearly charge. Reminders carry the price as of the day you download them; open your reminders link any time to re-check the latest prices.</p></div>
<p class="small">Also useful: <a href="/watchlist.html">Price watchlist</a> · <a href="/subscription-audit.html">Subscription Audit</a> · <a href="/monthly-or-yearly.html">Monthly or yearly?</a></p>
<script>""" + RR_JS.replace("__WDATA__", _WLDATA).replace("__BASE__", json.dumps(BASE)) + """</script>"""
page("/renewal-reminders.html", "AI Subscription Renewal Reminders — Calendar Alerts Before You're Charged | ToolPick",
     "Add the AI tools you pay for and get calendar reminders before each renewal, with the latest checked price and cheaper tools for the same job. No account, no email.",
     _rr_body, [{"@context":"https://schema.org","@type":"WebPage","name":"ToolPick AI subscription renewal reminders","url":BASE+"/renewal-reminders.html"}, crumbs([("ToolPick","/"),("Save money","/save-money.html"),("Renewal reminders","/renewal-reminders.html")])])

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
    _v["cap"] = cap_label(_v["n"]); _v["lt"] = _v["n"] in LOWER_TIER; _v["mf"] = TIER_MATCH[_v["n"]][1] if _v["n"] in TIER_MATCH else None; _v["mp"] = TIER_MATCH[_v["n"]][0] if _v["n"] in TIER_MATCH else None
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
function cheapOn(alts,B,t){return alts.map(x=>({x,v:(t&&B=='m'&&x.mf!=null&&!t.lt)?x.mf:priceOn(x,B),tier:(t&&B=='m'&&x.mf!=null&&!t.lt)?x.mp:null})).filter(z=>z.v!=null).sort((p,q)=>p.v-q.v||p.x.n.localeCompare(q.x.n))[0]||null}
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
const alts=t.al.map(k=>byS[k]).filter(Boolean);const TN=(x,z)=>x&&x.lt!=t.lt&&!(z&&z.tier)?' <span class="small"><b>Different tier: compare features before switching.</b></span>':'';
const cheap=cheapOn(alts,B,t);const cheapO=cheapOn(alts,O,t);
const free=t.fa?byS[t.fa]:null;
const cats=t.cap;let h='';const per=B=='a'?'/mo paid yearly':'/mo';
if(bad){o.innerHTML='<div class="pick" role="status"><b>Please type what you pay as a number, like 24 or 19.99.</b></div>';return}
if(pay==null){h+=`<div class="pick" role="status"><b>Type what you pay for ${X(t.n)} per month to see your saving.</b> The options below still show what we checked.</div>`}
const cheaper=cheap&&pay!=null&&cheap.v<pay,ownFree=t.fr;
if(pay!=null){if(cheaper)h+=`<div class="pick pl-ans"><span class="badge b-best">YOU CAN PAY LESS</span> <b>${X(cheap.x.n)+(cheap.tier?' ('+X(cheap.tier)+')':'')} costs ${plan(cheap.v,B)}</b> — ${money(pay-cheap.v)}/mo less than the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''} (${money((pay-cheap.v)*12)}/yr). Both prices are ${BL[B]} billing.${TN(cheap.x,cheap)}${ownFree?` Or try ${X(t.n)}\u2019s own free plan first.`:''}</div>`;
else if(ownFree)h+=`<div class="pick pl-ans"><span class="badge b-free">TRY YOUR FREE PLAN</span> <b>${alts.length?'No cheaper '+BL[B]+' plan we checked':'No like-for-like cheaper option checked'} — but ${X(t.n)} has its own free plan.</b> If it covers what you do, you could pay $0 and save ${money(pay)}/mo (${money(pay*12)}/yr).<p class="small" style="margin:6px 0 0">Free plan: ${X(t.f)} · ${src(t)}</p></div>`;
else h+=`<div class="pick pl-ans"><span class="badge b-rank">STAY PUT</span> <b>${alts.length?'Nothing cheaper that we checked.':'No like-for-like cheaper option checked.'}</b> No other tool that does the same main job (${X(cats)}) in our list has a checked ${BL[B]} price below the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''} for ${X(t.n)}, so keep it.${free?` The only way to pay less is a free plan with limits, like ${X(free.n)}\u2019s below.`:''}</div>`}
const card=(lab,cls,x,body)=>`<article class="card" style="margin:12px 0"><div class="badges"><span class="badge ${cls}">${lab}</span></div><h3 style="margin:4px 0"><a href="${x.u}">${X(x.n)}</a></h3>${body}<p class="small">${src(x)} · <a href="/compare-builder.html?tools=${t.s},${x.s}">Compare with ${X(t.n)} →</a></p></article>`;
h+=`<h2>Cheapest plan we checked (${BL[B]} billing)</h2>`;
h+=cheap?card(cheaper?'CHEAPER':'CHEAPEST OTHER','b-best',cheap.x,`<p class="price">${plan(cheap.v,B)}</p><p class="small">${X(cheap.x.p)}</p>${TN(cheap.x,cheap)}<p>${pay==null?'Type what you pay to see the difference.':cheaper?`You would save <b>${money(pay-cheap.v)}/mo</b> (<b>${money((pay-cheap.v)*12)}/yr</b>) compared with the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''}.`:`This is not cheaper than the ${money(pay)}/mo you pay${B=='a'?' (yearly billing)':''}, so it would not save you money.`}</p>`):`<p>${alts.length?`We have no checked ${BL[B]} dollar price for another tool that does the same main job (${X(cats)}).`:'No like-for-like cheaper option checked: no other tool in our list does the same main job ('+X(cats)+').'}</p>`;
const tO=usd(t[O]);if(tO!=null&&cheapO){const d=Math.round((tO-cheapO.v)*100)/100;h+=`<div class="bnote"><p style="margin:0"><b>On ${BL[O]} billing instead:</b> ${X(t.n)} is ${plan(tO,O)} and the cheapest other is ${X(cheapO.x.n)+(cheapO.tier?' ('+X(cheapO.tier)+')':'')} at ${plan(cheapO.v,O)} — ${d>0?`${money(d)}/mo less (${money(d*12)}/yr)`:'not cheaper'}. We only compare ${BL[O]} with ${BL[O]}.</p></div>`}
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


# --- Browse all tools directory (v53: search + "what it does" + one-tap filters) ---
# Filters use only verified fields already in tools.py/PRICE_TABLE: category membership,
# realfree(), PRICE_TABLE monthly/annual availability, lowest numeric entry rate,
# _perseat() wording in the verified entry price text, and CAPS (what each tool's own site
# says it does, checked 2026-10-20). Search only matches our own saved text (name, about,
# job labels, category); it never invents prices or features.
_dmap = {}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        _k = slug(_t["name"])
        if _k not in _dmap:
            _dmap[_k] = dict(s=_k, n=_t["name"], d=_t["about"], p=_t["price"], f=_t["free"], k=_t.get("checked", CHECKED),
                             u=turl(_t["name"]), dm=dom(_t["url"]), pr=_t["pricing"], m=_t["monthly"], a=_t["annual"],
                             ps=_perseat(_t), fr=realfree(_t), cats=[], bestFor=[], j=list(CAPS[_t["name"]]))
        if _c["id"] not in [x["id"] for x in _dmap[_k]["cats"]]: _dmap[_k]["cats"].append(dict(id=_c["id"], name=_c["name"]))
        if _t["name"] == _c["best"] and _c["id"] not in _dmap[_k]["bestFor"]: _dmap[_k]["bestFor"].append(_c["id"])
_DLIST = sorted(_dmap.values(), key=lambda x: x["n"].lower())
DDATA = json.dumps(_DLIST).replace("</", "<\\/")
_JOBC = {}
for _v in _DLIST:
    for _j in _v["j"]: _JOBC[_j] = _JOBC.get(_j, 0) + 1
JOBDATA = json.dumps({k: CAP_LABEL.get(k, k) for k in _JOBC})
CATDATA = json.dumps([dict(id=c["id"], n=c["name"], need=c["need"]) for c in CATEGORIES])
DIR_DATE = "2026-10-28"
def _d_pv(v):
    if v is None: return None
    if isinstance(v, (int, float)): return (float(v), "$")
    m = _re.search(r"([€$£])\s*([\d.]+)", str(v))
    if m: return (float(m.group(2)), m.group(1))
    m = _re.search(r"([\d.]+)", str(v)); return (float(m.group(1)), "$") if m else None
def _d_entry(t):
    vs = [x for x in (_d_pv(t["m"]), _d_pv(t["a"])) if x]
    return sorted(vs)[0] if vs else None
def _d_money(amt, cur):
    r = round(amt * 100) / 100
    return cur + (str(int(r)) if r == int(r) else f"{r:.2f}")
def _d_card(t):  # mirrors card() in the page script, used to pre-render the default list (no JS needed, no layout shift)
    en = _d_entry(t); bv = bool(t["bestFor"])
    jobs = [CAP_LABEL.get(k, k) for k in t["j"]]
    b = ('<span class="badge b-best">BEST VALUE</span>' if bv else '') + ('<span class="badge b-free">FREE PLAN</span>' if t["fr"] else '') + ('' if en else '<span class="badge b-rank">PRICE NOT VERIFIED</span>')
    ent = (f'<p class="dent"><b>From {_d_money(*en)}/mo</b> <span class="small">lowest verified entry{" · per seat" if t["ps"] else ""}</span></p>' if en
           else '<p class="small check">No verified numeric entry price — check the official page.</p>')
    return (f'<article class="card dcard{" best" if bv else ""}" data-s="{t["s"]}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain={t["dm"]}&amp;sz=64" alt="{e(t["n"])} logo" width="28" height="28" loading="lazy"></span><div><div class="badges">{b}</div><h3><a href="{t["u"]}">{e(t["n"])}</a></h3></div></div>'
            f'<p class="djob"><span class="small">Main job:</span> {e(jobs[0])}{(" <span class=small>· also " + e(", ".join(jobs[1:])) + "</span>") if len(jobs) > 1 else ""}</p><p>{e(t["d"])}</p>{ent}<p class="price small">{e(t["p"])}</p><p class="small">{e(t["f"])}</p>'
            f'<p class="small meta">{e(", ".join(c["name"] for c in t["cats"]))} · checked {t["k"]} · <a href="{e(t["pr"])}" rel="noopener" target="_blank">Official pricing</a></p>'
            f'<div class="dact"><a class="bbtn" href="{t["u"]}">Details</a><button type="button" class="bbtn addbtn" data-add="{t["s"]}" aria-pressed="false">+ Compare</button></div></article>')
def _d_sortkey(t):
    en = _d_entry(t)
    return (0 if t["bestFor"] else 1, (0 if t["fr"] else 1) if en else 2, en[0] if en else 1e9, t["n"].lower())
_D_SSR = "".join(_d_card(t) for t in sorted(_DLIST, key=_d_sortkey))
_D_CHIPS = '<button type="button" class="dchip" data-cat="" aria-pressed="true">All <span class="dn2">' + str(len(_DLIST)) + '</span></button>' + "".join(
    f'<button type="button" class="dchip" data-cat="{c["id"]}" aria-pressed="false">{e(c["name"])} <span class="dn2">{len({slug(t["name"]) for t in c["tools"]})}</span></button>' for c in CATEGORIES)
_D_QUICK = "".join(f'<button type="button" class="dchip dq" data-q="{k}" aria-pressed="false">{lab}</button>' for k, lab in
                   [("free", "Free plan"), ("u10", "Under $10/mo"), ("bv", "Best Value picks"), ("monthly", "Pay monthly")])
_D_JOBOPTS = '<option value="">Any job</option>' + "".join(f'<option value="{k}">{e(CAP_LABEL.get(k, k))} ({n})</option>' for k, n in sorted(_JOBC.items(), key=lambda x: CAP_LABEL.get(x[0], x[0]).lower()))
DIR_CSS = """<style>
.dhead{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:4px 16px}.dhead h1{margin-bottom:4px}
.dshort{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0 0 var(--s3)}
.dbar{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:var(--s4);margin:var(--s3) 0 var(--s4)}
.dsearch{position:relative;display:flex;gap:8px;align-items:center}
.dsearch input{flex:1;min-width:0;min-height:52px;font:inherit;font-size:1.05rem;border:2px solid var(--bd);border-radius:12px;padding:0 44px 0 14px;background:var(--sf);color:var(--tx)}
.dsearch input:focus{border-color:var(--ac);outline:none}
.dx{position:absolute;right:6px;top:50%;transform:translateY(-50%);width:44px;height:44px;border:0;background:none;font-size:1.3rem;color:var(--mu);cursor:pointer;border-radius:10px}
.dx[hidden]{display:none}.dsearch input::-webkit-search-cancel-button{-webkit-appearance:none;display:none}
.drow{display:flex;flex-wrap:wrap;gap:8px;margin-top:var(--s3);overflow-x:auto;scrollbar-width:thin;padding-bottom:2px;-webkit-overflow-scrolling:touch}
.drow.wrapr{flex-wrap:wrap;overflow:visible}
.dchip{flex:none;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;font-size:.92rem;font-weight:600;cursor:pointer;white-space:nowrap}
.dchip:hover{border-color:var(--ac)}
.dchip[aria-pressed=true]{background:var(--ac);border-color:var(--ac);color:#fff}
.dchip[disabled]{opacity:.45;cursor:default}
.dn2{font-weight:500;font-size:.8rem;color:var(--mu)}.dchip[aria-pressed=true] .dn2{color:#fff}
.dq[aria-pressed=true]::before{content:"\\2713"}
.dlab{font-size:.8rem;font-weight:700;color:var(--mu);text-transform:uppercase;letter-spacing:.04em;margin:var(--s3) 0 0}
.dsel{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:var(--s3);margin-top:var(--s3)}
.dsel label{font-weight:600;display:block;font-size:.92rem}
.dsel select{width:100%;min-height:48px;margin-top:6px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 var(--s3);font:inherit}
.dmore{margin-top:var(--s3)}.dmore>summary{cursor:pointer;min-height:44px;display:inline-flex;align-items:center;font-weight:600;color:var(--ac)}
.dres{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 16px;margin:var(--s4) 0 var(--s2)}
.dres h2{margin:0;font-size:1.2rem}
.dtools{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dtools select{min-height:44px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 10px;font:inherit}
.dview{display:inline-flex;border:1px solid var(--bd);border-radius:999px;overflow:hidden}
.dview button{min-height:44px;padding:0 14px;border:0;background:var(--sf);color:var(--tx);font:inherit;font-weight:600;cursor:pointer}
.dview button[aria-pressed=true]{background:var(--tx);color:var(--sf)}
.dact2{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 var(--s3)}
.dact2:empty{display:none}
.dact2 .dchip{background:var(--acs);border-color:var(--ac);color:var(--tx)}
.dact2 .dchip::after{content:"\\00d7";font-size:1.15rem;line-height:1;margin-left:2px}
.dclr{background:none;border:0;color:var(--ac);font:inherit;font-weight:600;text-decoration:underline;cursor:pointer;min-height:44px;padding:0 6px}
.djob{margin:0;font-weight:600}
.dent{margin:4px 0 0;font-size:1.05rem}
.dact{display:flex;gap:8px;margin-top:auto;padding-top:var(--s2)}
.dact .bbtn{min-height:44px}
.addbtn[aria-pressed=true]{background:var(--acs);border-color:var(--ac)}
.dempty{background:var(--sf);border:1px solid var(--bd);border-left:4px solid var(--warn);border-radius:var(--r);padding:var(--s4)}
.dempty .drow{flex-wrap:wrap;overflow:visible}
.dtab{overflow-x:auto;border:1px solid var(--bd);border-radius:var(--r);background:var(--sf);box-shadow:var(--sh)}
.dtab table{border:0;display:table;min-width:720px;width:100%;border-radius:0}
.dtab th,.dtab td{padding:10px 12px;border-bottom:1px solid var(--bd);text-align:left;vertical-align:top;font-size:.92rem}
.dtab th:first-child,.dtab td:first-child{position:sticky;left:0;background:var(--sf);z-index:1}
.dtab thead th:first-child{background:var(--sf2)}.dtab tbody th{font-weight:600}
.dtab td .bbtn{min-height:44px;padding:0 12px;font-size:.88rem;white-space:nowrap}
.yes{color:var(--ok);font-weight:700}
.dtray{position:sticky;bottom:10px;z-index:20;display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;background:var(--tx);color:#fff;border-radius:var(--r);box-shadow:0 8px 24px rgba(16,24,40,.25);padding:10px 12px 10px 16px;margin:var(--s4) 0}
.dtray[hidden]{display:none}
.dtray .tl{flex:1 1 220px;min-width:0;font-size:.92rem}
.dtray .tl b{display:block}
.dtray .bbtn{min-height:44px;flex:none}
.dtray .bbtn.primary{background:#fff;color:var(--tx);border-color:#fff}
.dtray .bbtn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
.dnote{margin-top:var(--s5)}
@media(max-width:640px){.dtag2,#d-qh,.dlab{display:none}.dhead+.tag{font-size:.98rem}.drow,.drow.wrapr{flex-wrap:nowrap;overflow-x:auto}.dempty .drow{flex-wrap:wrap}.dshort{font-size:.82rem;gap:2px 12px}.dbar{padding:var(--s3)}.dres h2{font-size:1.05rem}.dtray .tl{flex-basis:100%}.dtray .bbtn{flex:1 1 0}}
</style>"""
directory_body = DIR_CSS + f"""<div class="dhead"><h1>Browse all AI tools</h1></div>
<p class="tag" style="margin:0 0 var(--s2)">{total_tools} AI tools in {len(CATEGORIES)} categories. Search by name or job, tap a filter, and compare up to 3.<span class="dtag2"> Every price is copied from the official pricing page, with the date we checked it.</span></p>
<p class="small dshort v53">Shortcuts: <a href="/ai-team-plans.html">Team plans by team size</a> <a href="/alternatives.html">Same-job alternatives</a> <a href="/ai-student-discounts.html">Student discounts</a> <a href="/free-plan-limits.html">Free plan limits</a></p>
<form class="dbar" id="dform" role="search" onsubmit="return false"><label for="d-q" class="skip">Search AI tools</label>
<div class="dsearch"><input id="d-q" name="q" type="search" autocomplete="off" enterkeyhint="search" placeholder="Search: voiceover, slides, meeting notes, Cursor…" aria-describedby="d-qh"><button type="button" class="dx" id="d-qx" aria-label="Clear search" hidden>×</button></div>
<p class="small" id="d-qh" style="margin:6px 0 0">Matches tool names, what each tool does, and categories.</p>
<p class="dlab" id="d-catl">Category</p><div class="drow" id="d-cats" role="group" aria-labelledby="d-catl">{_D_CHIPS}</div>
<p class="dlab" id="d-ql">Quick filters</p><div class="drow wrapr" id="d-quick" role="group" aria-labelledby="d-ql">{_D_QUICK}</div>
<details class="dmore" id="d-more"><summary>More filters<span class="dtag2">: what it does, price range, billing, seats</span></summary><div class="dsel">
<div><label for="d-job">What it does</label><select id="d-job" name="job">{_D_JOBOPTS}</select></div>
<div><label for="d-price">Starting price (verified)</label><select id="d-price" name="price"><option value="any">Any price</option><option value="free">Free to start (real free plan)</option><option value="u10">Under $10/mo</option><option value="10-25">$10–$25/mo</option><option value="over25">Over $25/mo</option><option value="unverified">Price not verified</option></select></div>
<div><label for="d-free">Free plan</label><select id="d-free" name="free"><option value="any">Any</option><option value="yes">Has a real free plan</option><option value="no">No real free plan</option></select></div>
<div><label for="d-billing">Billing (verified)</label><select id="d-billing" name="billing"><option value="any">Any</option><option value="monthly">Can pay monthly</option><option value="annual">Has a yearly-billing price</option><option value="both">Both monthly and yearly</option></select></div>
<div><label for="d-seat">Seat pricing</label><select id="d-seat" name="seat"><option value="any">Any</option><option value="perseat">Entry price is per seat</option><option value="flat">Entry price not per seat</option></select></div>
</div></details></form>
<div class="dres"><h2><span id="dir-count" role="status" aria-live="polite">{len(_DLIST)} tools</span></h2><div class="dtools"><label for="d-sort" class="skip">Sort by</label><select id="d-sort" name="sort" aria-label="Sort by"><option value="value">Sort: Best Value first</option><option value="price">Sort: Lowest price</option><option value="name">Sort: Name A–Z</option></select><div class="dview" role="group" aria-label="View"><button type="button" data-v="cards" aria-pressed="true">Cards</button><button type="button" data-v="table" aria-pressed="false">Table</button></div></div></div>
<div class="dact2" id="d-active" aria-label="Active filters"></div>
<div id="dir-out"><div class="grid">{_D_SSR}</div></div>
<div class="dtray" id="dir-tray" hidden><div class="tl" id="tray-list" aria-live="polite"></div><a class="bbtn primary" id="dir-go" href="/compare-builder.html">Compare</a><button type="button" class="bbtn ghost" id="tray-clear">Clear</button></div>
<details class="bnote dnote"><summary><h2 style="display:inline;margin:0;font-size:1.05rem">How these filters work</h2></summary><p class="small" style="margin:8px 0 0"><b>What it does</b> comes from each tool's own website (checked 2026-10-20); the first job listed is the tool's main job, which is what “same job” means everywhere on ToolPick. <b>Price filters</b> use the lowest verified monthly or yearly-billing entry price in our price table. Tools without a numeric entry price (“check site”, custom or usage-only) only appear under “Price not verified” and sort last by price — we never guess them into a range. <b>Free plan</b> means a real free plan; free trials and one-time credits don't count. <b>Best Value</b> is ToolPick's pick for a category. Search only looks at our saved text, so it can't promise a feature a tool's site doesn't state.</p><p class="small" style="margin:12px 0 0">Want a ranked answer instead? <a href="/">Describe your need in the finder →</a> · <a href="/help-me-choose.html">Help me choose in 5 steps</a> · <a href="/stacks.html">Starter stacks by role</a> · <a href="/pay-less.html">Pay less for a tool you use</a></p></details>
<script>const DD=__DD__,JOBS=__JOBS__,CATS=__CATS__;</script>""" + r"""<script>
(function(){
const byS={};DD.forEach(t=>byS[t.s]=t);const $=id=>document.getElementById(id);
document.addEventListener('error',ev=>{const i=ev.target;if(i&&i.tagName=='IMG'&&i.closest('.logo')){i.replaceWith(document.createTextNode((i.alt||'?')[0]))}},true);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function pv(v){if(v==null)return null;if(typeof v=='number')return{amt:v,cur:'$'};const m=String(v).match(/([€$£])\s*([\d.]+)/);if(m)return{amt:parseFloat(m[2]),cur:m[1]};const n=String(v).match(/([\d.]+)/);return n?{amt:parseFloat(n[1]),cur:'$'}:null}
function entry(t){const v=[pv(t.m),pv(t.a)].filter(Boolean);if(!v.length)return null;v.sort((a,b)=>a.amt-b.amt);return v[0]}
function money(a,c){const r=Math.round(a*100)/100;return c+(Number.isInteger(r)?String(r):r.toFixed(2))}
const catName={};CATS.forEach(c=>catName[c.id]=c.n);
const SYN={voice:'speech',voiceover:'speech',voiceovers:'speech',tts:'speech',narration:'speech',slides:'presentation',slide:'presentation',deck:'presentation',decks:'presentation',powerpoint:'presentation',ppt:'presentation',pitch:'presentation',notes:'notes',notetaker:'notes',meeting:'meeting',meetings:'meeting',chat:'chat',chatbot:'chat',assistant:'assistant',code:'cod',coding:'cod',programming:'cod',developer:'cod',ide:'cod',logo:'logo',logos:'logo',music:'music',song:'music',songs:'music',transcribe:'transcri',transcript:'transcri',transcription:'transcri',subtitles:'transcri',picture:'image',pictures:'image',photo:'photo',photos:'photo',image:'image',images:'image',art:'image',website:'website',site:'website',app:'app',apps:'app',seo:'seo',social:'social',instagram:'social',tiktok:'social',ads:'ad',ad:'ad',calendar:'calendar',schedule:'schedul',scheduling:'schedul',automate:'automat',automation:'automat',papers:'paper',paper:'paper',academic:'paper',pdf:'doc',pdfs:'doc',documents:'doc',video:'video',videos:'video',clip:'clip',clips:'clip',avatar:'avatar',podcast:'podcast',agent:'agent',agents:'agent',support:'support',email:'mail',emails:'mail',writing:'writ',write:'writ',essay:'writ',grammar:'grammar',research:'research',search:'search',edit:'edit',editing:'edit',editor:'edit',design:'design',upscale:'upscal',music:'music',translate:'translat',dub:'dub',dubbing:'dub',tasks:'task',project:'project'};
const STOP=new Set(['a','an','the','for','to','and','or','ai','tool','tools','i','need','want','best','with','my','me','of','in','that','can','on','make','making','something','some','good','use','using','help','is','it','do','how','free','cheap']);
DD.forEach(t=>{t.jl=t.j.map(k=>JOBS[k]||k);t.hay=(t.n+' '+t.d+' '+t.jl.join(' ')+' '+t.j.join(' ')+' '+t.cats.map(c=>c.name).join(' ')).toLowerCase();t.nl=t.n.toLowerCase()});
function toks(q){return q.toLowerCase().replace(/[^a-z0-9.+#\s-]/g,' ').split(/\s+/).filter(w=>w&&!STOP.has(w))}
function tokHit(t,w){if(t.hay.includes(w))return true;const s=SYN[w];if(s&&t.hay.includes(s))return true;if(w.length>4&&w.endsWith('s')&&t.hay.includes(w.slice(0,-1)))return true;return false}
let sel=[];try{sel=JSON.parse(sessionStorage.getItem('tpCmp')||'[]').filter(s=>byS[s]).slice(0,3)}catch(e){}
const S={q:'',category:'',job:'',free:'any',price:'any',billing:'any',seat:'any',bv:false,sort:'value',view:'cards'};
function share(){const p=new URLSearchParams();if(S.q.trim())p.set('q',S.q.trim());if(S.category)p.set('category',S.category);if(S.job)p.set('job',S.job);['free','price','billing','seat'].forEach(k=>{if(S[k]!='any')p.set(k,S[k])});if(S.bv)p.set('bv','1');if(S.sort!='value')p.set('sort',S.sort);if(S.view!='cards')p.set('view',S.view);const s=p.toString();return '/tools.html'+(s?'?'+s:'')}
function match(t,v,skip){skip=skip||'';const en=entry(t);
if(skip!='category'&&v.category&&!t.cats.some(c=>c.id==v.category))return false;
if(skip!='job'&&v.job&&!t.j.includes(v.job))return false;
if(skip!='free'&&(v.free=='yes'&&!t.fr||v.free=='no'&&t.fr))return false;
if(skip!='price'){if(v.price=='free'&&!t.fr)return false;if(v.price=='u10'&&!(en&&en.amt<10))return false;if(v.price=='10-25'&&!(en&&en.amt>=10&&en.amt<=25))return false;if(v.price=='over25'&&!(en&&en.amt>25))return false;if(v.price=='unverified'&&en)return false}
if(skip!='billing'&&(v.billing=='monthly'&&t.m==null||v.billing=='annual'&&t.a==null||v.billing=='both'&&(t.m==null||t.a==null)))return false;
if(skip!='seat'&&(v.seat=='perseat'&&!t.ps||v.seat=='flat'&&t.ps))return false;
if(skip!='bv'&&v.bv&&!(v.category?t.bestFor.includes(v.category):t.bestFor.length))return false;
if(skip!='q'&&v.q.trim()){const w=toks(v.q);if(w.length&&!w.every(x=>tokHit(t,x)))return false}
return true}
function isBV(t){return S.category?t.bestFor.includes(S.category):t.bestFor.length>0}
function qscore(t){const w=toks(S.q);if(!w.length)return 0;let s=0;w.forEach(x=>{if(t.nl==x||t.nl.startsWith(x))s+=10;else if(t.nl.includes(x))s+=6;if(t.jl[0]&&(t.jl[0].toLowerCase().includes(x)||(SYN[x]&&t.jl[0].toLowerCase().includes(SYN[x]))))s+=4});return s}
function sorted(list){const en=entry;
if(S.sort=='name')return list.sort((a,b)=>a.n.localeCompare(b.n));
if(S.sort=='price')return list.sort((a,b)=>{const ea=en(a),eb=en(b);if(ea&&eb&&ea.amt!=eb.amt)return ea.amt-eb.amt;if(ea&&!eb)return -1;if(!ea&&eb)return 1;return a.n.localeCompare(b.n)});
return list.sort((a,b)=>{const qa=qscore(a),qb=qscore(b);if(qa!=qb)return qb-qa;const ba=isBV(a)?0:1,bb=isBV(b)?0:1;if(ba!=bb)return ba-bb;const ea=en(a),eb=en(b);const ga=ea?(a.fr?0:1):2,gb=eb?(b.fr?0:1):2;if(ga!=gb)return ga-gb;if(ea&&eb&&ea.amt!=eb.amt)return ea.amt-eb.amt;if(ea&&!eb)return -1;if(!ea&&eb)return 1;return a.n.localeCompare(b.n)})}
function cbtn(t,cls){const on=sel.includes(t.s);return `<button type="button" class="bbtn addbtn${cls||''}" data-add="${t.s}" aria-pressed="${on}" aria-label="${on?'Remove '+X(t.n)+' from compare':'Add '+X(t.n)+' to compare'}">${on?'✓ In compare':'+ Compare'}</button>`}
function card(t){const en=entry(t),bv=isBV(t);
return `<article class="card dcard${bv?' best':''}" data-s="${t.s}"><div class="th"><span class="logo"><img src="https://www.google.com/s2/favicons?domain=${t.dm}&amp;sz=64" alt="${X(t.n)} logo" width="28" height="28" loading="lazy"></span><div><div class="badges">${bv?'<span class="badge b-best">BEST VALUE</span>':''}${t.fr?'<span class="badge b-free">FREE PLAN</span>':''}${en?'':'<span class="badge b-rank">PRICE NOT VERIFIED</span>'}</div><h3><a href="${t.u}">${X(t.n)}</a></h3></div></div><p class="djob"><span class="small">Main job:</span> ${X(t.jl[0])}${t.jl.length>1?' <span class=small>· also '+X(t.jl.slice(1).join(', '))+'</span>':''}</p><p>${X(t.d)}</p>${en?`<p class="dent"><b>From ${money(en.amt,en.cur)}/mo</b> <span class="small">lowest verified entry${t.ps?' · per seat':''}</span></p>`:'<p class="small check">No verified numeric entry price — check the official page.</p>'}<p class="price small">${X(t.p)}</p><p class="small">${X(t.f)}</p><p class="small meta">${X(t.cats.map(c=>c.name).join(', '))} · checked ${t.k} · <a href="${X(t.pr)}" rel="noopener" target="_blank">Official pricing</a></p><div class="dact"><a class="bbtn" href="${t.u}">Details</a>${cbtn(t)}</div></article>`}
function table(list){return '<div class="dtab" tabindex="0" role="region" aria-label="Tools table, scroll sideways for more"><table><caption class="skip">AI tools matching your filters</caption><thead><tr><th scope="col">Tool</th><th scope="col">Main job</th><th scope="col">From (verified)</th><th scope="col">Free plan</th><th scope="col">Billing verified</th><th scope="col">Checked</th><th scope="col">Compare</th></tr></thead><tbody>'+list.map(t=>{const en=entry(t);const bill=[t.m!=null?'monthly':'',t.a!=null?'yearly':''].filter(Boolean).join(' + ')||'—';return `<tr><th scope="row"><a href="${t.u}">${X(t.n)}</a>${isBV(t)?' <span class="badge b-best">BEST VALUE</span>':''}</th><td>${X(t.jl[0])}</td><td>${en?'<b>'+money(en.amt,en.cur)+'/mo</b>'+(t.ps?' per seat':''):'<span class="small">not verified</span>'}</td><td>${t.fr?'<span class="yes">Yes</span>':'No'}</td><td>${bill}</td><td>${t.k}</td><td>${cbtn(t)}</td></tr>`}).join('')+'</tbody></table></div>'}
const LAB={free:{yes:'Free plan',no:'No free plan'},price:{free:'Free to start',u10:'Under $10/mo','10-25':'$10–$25/mo',over25:'Over $25/mo',unverified:'Price not verified'},billing:{monthly:'Pay monthly',annual:'Yearly price',both:'Monthly + yearly'},seat:{perseat:'Per-seat price',flat:'Not per seat'}};
function actives(){const a=[];if(S.q.trim())a.push(['q','“'+S.q.trim()+'”']);if(S.category)a.push(['category',catName[S.category]]);if(S.job)a.push(['job',JOBS[S.job]]);['free','price','billing','seat'].forEach(k=>{if(S[k]!='any')a.push([k,LAB[k][S[k]]])});if(S.bv)a.push(['bv','Best Value picks']);return a}
function reset(k){if(k=='q')S.q='';else if(k=='category'||k=='job')S[k]='';else if(k=='bv')S.bv=false;else S[k]='any'}
function syncUI(){$('d-q').value!==S.q&&($('d-q').value=S.q);$('d-qx').hidden=!S.q;$('d-job').value=S.job;['free','price','billing','seat'].forEach(k=>$('d-'+k).value=S[k]);$('d-sort').value=S.sort;
document.querySelectorAll('#d-cats .dchip').forEach(b=>{const on=b.dataset.cat==S.category;b.setAttribute('aria-pressed',on);const n=DD.filter(t=>(!b.dataset.cat||t.cats.some(c=>c.id==b.dataset.cat))&&match(t,S,'category')).length;b.querySelector('.dn2').textContent=n;b.disabled=!n&&!on});
const Q={free:S.free=='yes'||S.price=='free',u10:S.price=='u10',bv:S.bv,monthly:S.billing=='monthly'};document.querySelectorAll('#d-quick .dq').forEach(b=>b.setAttribute('aria-pressed',!!Q[b.dataset.q]));
document.querySelectorAll('.dview button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.v==S.view));
const jc={};DD.filter(t=>match(t,S,'job')).forEach(t=>t.j.forEach(k=>jc[k]=(jc[k]||0)+1));[...$('d-job').options].forEach(o=>{if(!o.value)return;const n=jc[o.value]||0;o.textContent=JOBS[o.value]+' ('+n+')';o.disabled=!n&&o.value!=S.job});
if(S.job||S.price!='any'&&S.price!='u10'&&S.price!='free'||S.billing!='any'&&S.billing!='monthly'||S.seat!='any'||S.free=='no')$('d-more').open=true}
function render(push){const list=sorted(DD.filter(t=>match(t,S)));const out=$('dir-out');
$('dir-count').textContent=list.length==DD.length?DD.length+' tools':list.length+' of '+DD.length+' tools';
const a=actives();$('d-active').innerHTML=a.length?a.map(([k,l])=>`<button type="button" class="dchip" data-rm="${k}" aria-label="Remove filter: ${X(l)}">${X(l)}</button>`).join('')+'<button type="button" class="dclr" id="d-clear">Clear all</button>':'';
if(!list.length){const tips=a.map(([k,l])=>{const n=DD.filter(t=>match(t,S,k)).length;return n?`<button type="button" class="dchip" data-rm="${k}">Remove ${k=='q'?X(l):'“'+X(l)+'”'} → ${n} tool${n>1?'s':''}</button>`:''}).filter(Boolean).join('');
const fq=S.q.trim()?`<p class="small" style="margin:12px 0 0">Or ask the finder, which reads whole sentences: <a href="/?q=${encodeURIComponent(S.q.trim())}">“${X(S.q.trim())}” in the finder →</a></p>`:'';
out.innerHTML=`<div class="dempty"><b>No tools match all of these.</b>${tips?'<p class="small" style="margin:8px 0 0">Try one change:</p><div class="drow">'+tips+'</div>':''}${fq}</div>`}
else out.innerHTML=S.view=='table'?table(list):'<div class="grid">'+list.map(card).join('')+'</div>';
syncUI();tray();if(push!==false)history.replaceState(null,'',share())}
function tray(){const tr=$('dir-tray');tr.hidden=!sel.length;try{sessionStorage.setItem('tpCmp',JSON.stringify(sel))}catch(e){}if(!sel.length)return;
$('tray-list').innerHTML='<b>Compare '+sel.length+' of 3</b>'+X(sel.map(s=>byS[s].n).join(' · '))+(sel.length<2?' — add one more':'');
const go=$('dir-go');go.href=sel.length>=2?'/compare-builder.html?tools='+sel.join(','):'#';go.setAttribute('aria-disabled',sel.length<2);go.textContent=sel.length>=2?'Compare '+sel.length+' →':'Pick 2+';}
function toggle(s,btn){const i=sel.indexOf(s);if(i>=0)sel.splice(i,1);else{if(sel.length>=3){$('tray-list').innerHTML='<b>Compare holds 3 tools.</b>Remove one first: '+X(sel.map(x=>byS[x].n).join(' · '));clearTimeout(window._tpT);window._tpT=setTimeout(tray,3500);return}sel.push(s)}
document.querySelectorAll('[data-add="'+s+'"]').forEach(b=>{const on=sel.includes(s);b.setAttribute('aria-pressed',on);b.textContent=on?'✓ In compare':'+ Compare';b.setAttribute('aria-label',(on?'Remove ':'Add ')+byS[s].n+(on?' from compare':' to compare'))});tray()}
document.addEventListener('click',ev=>{const b=ev.target.closest('button');if(!b)return;
if(b.dataset.add){toggle(b.dataset.add,b);return}
if(b.dataset.rm){reset(b.dataset.rm);render();return}
if(b.id=='d-clear'){Object.assign(S,{q:'',category:'',job:'',free:'any',price:'any',billing:'any',seat:'any',bv:false});render();$('d-q').focus();return}
if(b.dataset.cat!=null&&b.closest('#d-cats')){S.category=b.dataset.cat;render();return}
if(b.dataset.q){const k=b.dataset.q,on=b.getAttribute('aria-pressed')=='true';if(k=='free'){S.free=on?'any':'yes';if(on&&S.price=='free')S.price='any'}else if(k=='u10')S.price=on?'any':'u10';else if(k=='bv')S.bv=!on;else if(k=='monthly')S.billing=on?'any':'monthly';render();return}
if(b.dataset.v){S.view=b.dataset.v;render();return}
if(b.id=='d-qx'){S.q='';render();$('d-q').focus();return}
if(b.id=='tray-clear'){sel=[];document.querySelectorAll('[data-add]').forEach(x=>{x.setAttribute('aria-pressed',false);x.textContent='+ Compare'});tray();return}});
$('dir-go').addEventListener('click',ev=>{if(sel.length<2)ev.preventDefault()});
let tm;$('d-q').addEventListener('input',ev=>{S.q=ev.target.value;$('d-qx').hidden=!S.q;clearTimeout(tm);tm=setTimeout(()=>render(),120)});
$('d-q').addEventListener('keydown',ev=>{if(ev.key=='Escape'&&S.q){S.q='';render()}});
['job','free','price','billing','seat','sort'].forEach(k=>$('d-'+k).addEventListener('change',ev=>{S[k]=ev.target.value;render()}));
const p=new URLSearchParams(location.search);const ok=(id,v)=>v&&[...$(id).options].some(o=>o.value==v);
S.q=(p.get('q')||'').slice(0,80);if(p.get('category')&&catName[p.get('category')])S.category=p.get('category');if(p.get('job')&&JOBS[p.get('job')])S.job=p.get('job');
['free','price','billing','seat','sort'].forEach(k=>{if(ok('d-'+k,p.get(k)))S[k]=p.get(k)});S.bv=p.get('bv')=='1';if(p.get('view')=='table')S.view='table';
const any=[...p.keys()].length>0;if(any)render(false);else{syncUI();tray();document.querySelectorAll('#dir-out [data-add]').forEach(b=>{if(sel.includes(b.dataset.add)){b.setAttribute('aria-pressed',true);b.textContent='✓ In compare'}})}
})();
</script>"""
directory_body = directory_body.replace("__DD__", DDATA).replace("__JOBS__", JOBDATA).replace("__CATS__", CATDATA)
page("/tools.html", "Browse All AI Tools — Search & Filter by Job, Free Plan, Price | ToolPick", f"Search and filter all {total_tools} AI tools by what they do, category, real free plan, verified starting price and billing. Compare up to 3 side by side, with checked dates and official pricing links.", directory_body,
     [{"@context":"https://schema.org","@type":"ItemList","name":"All AI tools on ToolPick","itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+v["u"],"name":v["n"]} for i,v in enumerate(_DLIST)]}, crumbs([("ToolPick","/"),("Browse all tools","/tools.html")])])


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
    d = f"{name} costs {t['price']}. Free alternatives that do the same main job ({cap_label(name)}) with a verified free tier: {', '.join(alts[:5])}. Checked {t.get('checked', CHECKED)}."[:300]
    items = "".join(f"<li><h2 class='h3'><a href='{turl(a)}'>{e(a)}</a></h2><p>{e(find(a)['about'])}</p><p>🆓 {e(find(a)['free'])}</p><p class='price'>💲 Paid: {e(find(a)['price'])}</p><p class='small'>checked {find(a).get('checked', CHECKED)}</p></li>" for a in alts)
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
    reasons = [f"Main job: {cap_label(t['name'])}"]
    if is_best: reasons.append(f"ToolPick's Best Value pick for {cat['name']}")
    if lowest_name and t["name"] == lowest_name and en is not None: reasons.append(f"Lowest checked monthly price on this page: ${_num(t.get('monthly')):g}/mo billed monthly")
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
    _priced = [(_num(t.get("monthly")), t) for t in _alt_tools if t["price"] != "check site" and _num(t.get("monthly")) is not None]  # v27: same billing only
    _lowest_name = min(_priced, key=lambda x: x[0])[1]["name"] if _priced else None
    _title = f"Free Alternatives to {_target} ({CHECKED[:4]}) — {len(_alt_tools)} {_cat['name']} Tools with Real Free Plans"
    _d = f"Free alternatives to {_target} in {_cat['name'].lower()}: {', '.join(t['name'] for t in _alt_tools)} — each with a verified real free plan, entry price, checked date and official pricing link."
    _cards = "".join(_seo_card(t, _cat, i+1, _best_name, _lowest_name) for i, t in enumerate(_alt_tools))
    _top3 = ",".join(slug(t["name"]) for t in _alt_tools[:3])
    _qas = [
        (f"Does {_target} have a free plan?", f"Per its official pricing page (checked {_tgt.get('checked', CHECKED)}): {_tgt['free']}. Paid entry as listed: {_tgt['price']}."),
        (f"What is the Best Value free alternative to {_target}?", f"{_cat['best']} is ToolPick's Best Value pick for {_cat['name'].lower()} and is listed first here. " + (find(_cat['best']).get('why','') if any(t['name']==_cat['best'] for t in _alt_tools) else "")),
        (f"Which free alternative to {_target} has the lowest checked monthly price?", f"{_lowest_name} at ${_num(find(_lowest_name).get('monthly')):g}/mo billed monthly (lowest checked monthly price among these alternatives, which all do the same main job as {_target}: {cap_label(_target)}; checked {find(_lowest_name).get('checked', CHECKED)})." if _lowest_name else "None of these alternatives has a checked monthly price, so we don't rank them on price."),
    ]
    _fh, _fl = faq(_qas)
    _body = f"""<h1>Free alternatives to {e(_target)}</h1><p class="tag">Looking for a free alternative to {e(_target)}? These tools do the same main job as {e(_target)} ({e(cap_label(_target))}) and each have a verified real free plan — free trials and one-time credits do not count. Every price below was copied from the tool's official pricing page and shows its checked date.</p>
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
_vlowest = None  # v27: no single "lowest" across different video jobs; see the per-job FAQ answer
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
    ("Which is cheapest here?", "These tools do different main jobs, so we only compare within a job, on monthly prices: " + "; ".join(f"{cap_label(g[0]['name'])}: {g[0]['name']} at {_usd(_num(g[0]['monthly']))}/mo" for g in [sorted([t for t in _video_under_sorted if CAPS[t['name']][0] == cp and _num(t.get('monthly')) is not None], key=lambda t: (_num(t['monthly']), t['name'])) for cp in dict.fromkeys(CAPS[t['name']][0] for t in _video_under_sorted)] if g) + ". Tools with only a billed-yearly price are not ranked."),
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
       ("/price-changes.html","Recent price changes","Which AI tools raised or cut prices, newest first, with old and new prices."),
       ("/ai-video-cost.html","Real cost of AI video","See how many seconds of video each Runway, Pika and Luma plan really buys and the price per minute, same model only."),
       ("/ai-image-cost.html","Real cost of AI images","See how many images each Midjourney, Ideogram, Recraft and Krea plan really buys, the price per image, and which plans are unlimited."),
       ("/ai-voice-cost.html","Real cost of AI voice","See how many minutes of text to speech each ElevenLabs, Luma and Runway plan really buys and the price per minute."),
       ("/renewal-reminders.html","Renewal reminders","Get a calendar alert before each AI subscription renews, with the latest checked price and cheaper tools for the same job."),
       ("/watchlist.html","Price watchlist","Watch the tools you pay for and see which prices changed since you last looked. No account or email."),
       ("/subscription-audit.html#my-stack","My AI stack card","Add the tools you pay for and get a card with your monthly and yearly total, what you could save, and a link to re-check when prices change.")]
if FREE_V21: _SM.insert(2, ("/free.html","Can I do it for free?","Pick a job and see every tool with a real free plan, and the cheapest upgrade if you outgrow it."))
_sm_tools = "".join(f'<option value="{slug(n)}">{e(n)}</option>' for n in sorted(tool_pages, key=str.lower))
page("/save-money.html", "Save Money on AI Tools — Pay Less, Go Yearly, Go Free | ToolPick",
  "Simple ways to spend less on AI tools: find a cheaper plan for the same job, see if yearly billing pays off, find real free plans, track price changes and make a shareable card of your AI stack. Official prices with checked dates.",
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
    body = f"""<h1>Best free AI {e(n.lower())} tools</h1><p class="tag">{e(d)}</p><ol>{''.join(f"<li><h2 class='h3'><a href='{turl(t['name'])}'>{e(t['name'])}</a></h2><p>{e(t['about'])}</p><p class='small'><b>Main job:</b> {e(cap_label(t['name']))}</p><p>🆓 {e(t['free'])}</p><p class='price'>💲 Paid: {e(t['price'])}</p><p class='small'>checked {t.get('checked', CHECKED)}</p></li>" for t in L)}</ol>
<p>Compare paid options: <a href="/best-ai-{c['id']}-tools.html">all AI {e(n.lower())} tools</a> · <a href="/free.html">all free AI tools</a></p>"""
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":k+1,"url":BASE+turl(t["name"]),"name":t["name"]} for k,t in enumerate(L)]}
    page(path, title, d, body, [il, crumbs([("ToolPick","/"),("Free AI tools","/free.html"),(f"Best free AI {n} tools",path)])])

# guides hub
page("/guides.html", "AI tool guides: best tool for every job & free alternatives", "Every ToolPick guide: best AI tool for a job, free alternatives and head-to-head comparisons.",
  "<h1>Guides</h1><h2>New guides</h2><ul><li><a href='/embed.html'>Embed live AI price cards on your site</a></li><li><a href='/free-alternative-to-recraft.html'>Free alternative to Recraft</a></li><li><a href='/free-alternative-to-rytr.html'>Free alternative to Rytr</a></li><li><a href='/best-ai-video-tools-under-20.html'>Best AI video tools under $20</a></li></ul><h2>Best AI tool for…</h2><ul>" + "".join(f'<li><a href="/best-ai-tool-for-{j[0]}.html">{e(j[1])}</a></li>' for j in JOBS) + "</ul><h2>Free tools</h2><ul>" + "".join(f'<li><a href="/best-free-ai-{c["id"]}-tools.html">Best free AI {e(c["name"].lower())} tools</a></li>' for c in CATEGORIES) + "</ul><h2>Free alternatives</h2><ul>" +
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
ll += ["", "## Subscription Audit", f"- [AI Subscription Audit]({BASE}/subscription-audit.html): list tools you pay for, get keep/cancel/try-free-tier checklist with potential saving from verified data only, e.g. ?tools=elevenlabs:6:monthly,descript:16:monthly", "", "## New SEO guides", f"- [Free alternatives to Recraft]({BASE}/free-alternative-to-recraft.html)", f"- [Free alternatives to Rytr]({BASE}/free-alternative-to-rytr.html)", f"- [Best AI video tools under $20]({BASE}/best-ai-video-tools-under-20.html): verified entry under $20/mo, each tool's main job shown; cheapest only compared within a job", "", "## Help me choose", f"- [Help me choose wizard]({BASE}/help-me-choose.html): 5-step guided shortlist, e.g. ?category=audio&budget=10&billing=monthly&seats=1&free=any&annual=any", "", "## Compare builder", f"- [Compare builder]({BASE}/compare-builder.html): pick any 2-3 tools, e.g. ?tools=elevenlabs,descript,heygen", "", "## Cost calculator", f"- [Cost calculator]({BASE}/cost-calculator.html): true monthly/yearly cost by tool or category, seats and billing period, from verified entry prices, e.g. ?tool=elevenlabs&seats=1&billing=monthly", "", "## Browse all tools", f"- [Browse all tools directory]({BASE}/tools.html): filter all tools by category, free plan, verified price, billing and seat pricing, e.g. ?category=audio&free=yes&sort=price", "", "", "## How we pick", f"- [How we pick]({BASE}/how-we-pick.html): every pick shows how it was picked (official pricing data, not hands-on tested), price on its checked date, price history, earn disclosure (no affiliate links) and one real limitation", "", "## Real cost of AI video", f"- [Real cost of AI video]({BASE}/ai-video-cost.html): seconds of video per plan and $/minute for Runway, Pika, Luma from official credit rates; same model+resolution comparisons only, e.g. ?s=60&t=3", "", "## Real cost of AI voice", f"- [Real cost of AI voice]({BASE}/ai-voice-cost.html): minutes of text-to-speech per plan and $/minute for ElevenLabs, Luma, Runway from official pricing pages; monthly billing, same-model ranking, e.g. ?m=60&t=2", "", "## Renewal reminders", f"- [Renewal reminders]({BASE}/renewal-reminders.html): calendar (.ics) or Google Calendar reminders before each AI subscription renews, with checked price and same-job cheaper option, e.g. ?r=claude:m:2026-11-05:20", "", "## Embed price cards", f"- [Embed live price cards]({BASE}/embed.html): free iframe price cards per tool ({BASE}/embed/claude.html) and per comparison ({BASE}/embed/compare/chatgpt-vs-claude.html), same like-for-like verdicts, auto-updating", f"Data: {BASE}/tools.json"]
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
# --- v32: Embeddable live price cards (/embed.html generator + /embed/<tool>.html, /embed/compare/<slug>.html) ---
# Cards reuse the exact same verdict text as tool/compare pages (TV_TEXT / CMP_TXT), so like-for-like tier and billing
# rules are identical. Only checked prices are shown; each card shows its checked date and official pricing link.
EMBED_DATE = "2026-10-20"
EMBED_CSS = """*{box-sizing:border-box}html,body{margin:0;background:transparent}body{font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f172a}
.c{--bg:#fff;--tx:#0f172a;--mu:#475569;--bd:#e2e8f0;--sf:#f1f5f9;--ac:#1d4ed8;background:var(--bg);color:var(--tx);border:1px solid var(--bd);border-radius:12px;padding:14px 16px;max-width:100%}
.dark .c{--bg:#0f172a;--tx:#f1f5f9;--mu:#cbd5e1;--bd:#334155;--sf:#1e293b;--ac:#93c5fd}
@media(prefers-color-scheme:dark){.auto .c{--bg:#0f172a;--tx:#f1f5f9;--mu:#cbd5e1;--bd:#334155;--sf:#1e293b;--ac:#93c5fd}}
.h{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}.h b{font-size:1.05rem}.br{font-size:.78rem;color:var(--mu);text-decoration:none}.br i{font-style:normal;background:#1d4ed8;color:#fff;border-radius:4px;padding:0 5px;margin-right:4px;font-weight:700}
.j{color:var(--mu);font-size:.85rem;margin:2px 0 8px}.r{background:var(--sf);border-radius:8px;padding:7px 10px;margin:6px 0}.r span{display:block;font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;color:var(--mu)}
.v{margin:8px 0;font-weight:600}.f{font-size:.78rem;color:var(--mu);margin-top:8px}a{color:var(--ac)}.cta{display:inline-block;margin-top:6px;font-weight:600}
.g{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}"""
EMBED_JS = "<script>var t=new URLSearchParams(location.search).get('theme');document.documentElement.className=(t==='dark'||t==='light')?t:'auto';</script>"
def _embed_doc(title, canon, inner):
    return f'<!doctype html><html lang="en" class="auto"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{canon}"><base target="_blank">{EMBED_JS}<meta name="description" content="{e(title)}: checked prices and like-for-like verdict."><style>{EMBED_CSS}</style></head><body><main class="c">{inner}</main><script>(function(){{var c=document.querySelector(".c");function s(){{try{{parent.postMessage({{tp:"toolpick-embed",h:Math.ceil(c.getBoundingClientRect().height)+2}},"*")}}catch(e){{}}}}s();addEventListener("load",s);addEventListener("resize",s);if(window.ResizeObserver)new ResizeObserver(s).observe(c)}})();</script></body></html>'
_BR = f'<a class="br" href="{BASE}/?utm_source=embed" rel="noopener"><i>T</i>ToolPick</a>'
def _cheap_line(n):
    d = TV_TEXT.get(n, {}); m, a = d.get("m"), d.get("a")
    return " · ".join(x for x in [f"{_usd(m)}/mo monthly" if m is not None else "", f"{_usd(a)}/mo paid yearly" if a is not None else ""] if x) or "Not checked in US dollars — see the official page"
EMBED_TOOLS, _seen = [], set()
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _seen: continue
        _seen.add(_t["name"]); _n = _t["name"]; _s = slug(_n); _ck = _t.get("checked", CHECKED)
        _v = TV_TEXT.get(_n, {}).get("v", "")
        _inner = (f'<div class="h"><b>{e(_n)} pricing</b>{_BR}</div><div class="j">Main job: {e(cap_label(_n))}</div>'
            f'<div class="r"><span>Cheapest plan checked</span>{e(_cheap_line(_n))}</div>'
            f'<div class="r"><span>Plans</span>{e(PLANS_SHORT.get(_n, _t["price"]))}</div>'
            f'<div class="r"><span>Free plan</span>{("Yes — " + e(_t["free"])) if realfree(_t) else "No (" + e(_t["free"]) + ")"}</div>'
            + (f'<div class="v">{e(_v)}</div>' if _v else "") +
            f'<a class="cta" href="{BASE}{turl(_n)}?utm_source=embed" rel="noopener">Compare like-for-like alternatives on ToolPick →</a>'
            f'<div class="f">Checked {_ck} on the <a href="{e(_t["pricing"])}" rel="noopener">official pricing page</a>. USD; prices change, confirm before buying.</div>')
        os.makedirs("public/embed", exist_ok=True)
        open(f"public/embed/{_s}.html", "w").write(_embed_doc(f"{_n} price card · ToolPick", turl(_n), _inner))
        EMBED_TOOLS.append(dict(s=_s, n=_n, k="t", ck=_ck))
EMBED_CMP = []
for _x in COMPARISONS:
    _s, _ti, _N = _x[0], _x[1], cnames(_x)
    if _s not in CMP_TXT: continue
    _TT = [find(n) for n in _N]; _ck = max(t.get("checked", CHECKED) for t in _TT)
    _sw = any(n not in LOWER_TIER for n in _N)
    def _pc(n): return f'<br><b>Plan compared here: {e(TIER_MATCH[n][0])} {_usd(TIER_MATCH[n][1])}/mo</b> (the tier comparable to the other plan)' if _sw and n in TIER_MATCH and n in LOWER_TIER else ""
    _cols = "".join(f'<div class="r"><span>{e(t["name"])}</span>{e(_cheap_line(t["name"]))}{_pc(t["name"])}<br><small>{e(PLANS_SHORT.get(t["name"], t["price"]))}</small></div>' for t in _TT)
    _inner = (f'<div class="h"><b>{e(_ti)}: price check</b>{_BR}</div><div class="g">{_cols}</div><div class="v">{e(CMP_TXT[_s])}</div>'
        f'<a class="cta" href="{BASE}/compare/{_s}.html?utm_source=embed" rel="noopener">Full like-for-like comparison on ToolPick →</a>'
        f'<div class="f">Checked {", ".join(sorted(set(t.get("checked", CHECKED) for t in _TT)))} on each official pricing page (' + " · ".join(f'<a href="{e(t["pricing"])}" rel="noopener">{e(t["name"])}</a>' for t in _TT) + '). USD; prices change, confirm before buying.</div>')
    os.makedirs("public/embed/compare", exist_ok=True)
    open(f"public/embed/compare/{_s}.html", "w").write(_embed_doc(f"{_ti} price card · ToolPick", f"/compare/{_s}.html", _inner))
    EMBED_CMP.append(dict(s="compare/" + _s, n=_ti, k="c", ck=_ck))
_ED = json.dumps(EMBED_TOOLS + EMBED_CMP)
_opts = ('<optgroup label="Single tool">' + "".join(f'<option value="{x["s"]}">{e(x["n"])}</option>' for x in sorted(EMBED_TOOLS, key=lambda x: x["n"].lower())) + '</optgroup>'
         '<optgroup label="Comparison">' + "".join(f'<option value="{x["s"]}">{e(x["n"])}</option>' for x in EMBED_CMP) + '</optgroup>')
EMBED_BODY = f"""<h1>Embed live AI price cards</h1>
<p class="tag">Writing about AI tools? Put a price card in your post or newsletter page. It shows the checked price, the free plan and our like-for-like verdict, and it updates itself whenever we re-check the official pricing page — so your post never shows a stale price.</p>
<section class="card" aria-labelledby="eb-h"><h2 id="eb-h">1. Pick a card</h2>
<p><label for="eb-t">Tool or comparison</label><br><select id="eb-t" style="max-width:100%">{_opts}</select></p>
<p><label for="eb-th">Theme</label><br><select id="eb-th"><option value="auto">Match reader's light/dark setting</option><option value="light">Light</option><option value="dark">Dark</option></select>
 <label for="eb-w" style="margin-left:8px">Width</label> <select id="eb-w"><option value="480">480px (sidebar / post)</option><option value="360">360px (narrow)</option><option value="640">640px (wide)</option></select></p>
<h2>2. Preview</h2><div id="eb-pv" style="max-width:100%;overflow:auto"><iframe id="eb-f" title="Price card preview" style="border:0;width:480px;max-width:100%;height:320px" loading="lazy"></iframe></div>
<p class="small" id="eb-ck"></p>
<h2>3. Copy the code</h2><p><label for="eb-c">Paste this into your page's HTML</label> <span class="small">(the card resizes itself to fit; if your site blocks scripts, the height is sized for narrow phone screens so nothing gets cut off)</span></p><textarea id="eb-c" rows="5" readonly style="width:100%;font:13px ui-monospace,monospace"></textarea>
<p><button type="button" class="btn" id="eb-cp">Copy embed code</button> <span id="eb-ok" role="status" class="small"></span></p>
<p class="small">Can't paste HTML (e.g. some newsletter tools)? Use the plain link instead: <a id="eb-l" href="/">link</a></p></section>
<h2>How the cards stay honest</h2><ul><li>Only prices copied from each tool's official pricing page, with the checked date on the card. Unverified prices show "check site", never a guess.</li><li>The verdict uses the same like-for-like rule as every ToolPick page: same main job, same billing (monthly with monthly, yearly with yearly), lighter entry tiers compared at their comparable tier.</li><li>No tracking scripts inside the card, no ads, free to use. Each card links to the full page on ToolPick.</li></ul>
<p class="small">Other ways to keep up with prices: <a href="/watchlist.html">Price watchlist</a> · <a href="/price-changes.html">Price changes log</a> (<a href="/price-changes.xml">RSS</a>).</p>
<script>(function(){{var D={_ED},B={json.dumps(BASE)},q=new URLSearchParams(location.search),T=document.getElementById('eb-t'),H=document.getElementById('eb-th'),W=document.getElementById('eb-w'),F=document.getElementById('eb-f'),C=document.getElementById('eb-c');
if(q.get('card')&&D.some(function(x){{return x.s===q.get('card')}}))T.value=q.get('card');if(['light','dark'].indexOf(q.get('theme'))>=0)H.value=q.get('theme');
function cur(){{for(var i=0;i<D.length;i++)if(D[i].s===T.value)return D[i]}}
function code(h){{var x=cur(),u=B+'/embed/'+x.s+'.html'+(H.value==='auto'?'':'?theme='+H.value),pg=B+(x.k==='t'?'/tools/'+x.s+'.html':'/'+x.s+'.html');
C.value='<iframe data-toolpick src="'+u+'" title="'+x.n.replace(/"/g,'&quot;')+' price card by ToolPick" width="'+W.value+'" height="'+h+'" style="border:0;max-width:100%" loading="lazy"></iframe>\\n<script>window.addEventListener("message",function(e){{if(e.origin!=="'+B+'"||!e.data||e.data.tp!=="toolpick-embed")return;document.querySelectorAll("iframe[data-toolpick]").forEach(function(f){{if(f.contentWindow===e.source)f.style.height=e.data.h+"px"}})}});<\\/script>\\n<p style="font-size:12px"><a href="'+pg+'">'+x.n.replace(/</g,'&lt;')+' pricing on ToolPick</a></p>';
var L=document.getElementById('eb-l');L.href=pg;L.textContent=pg;document.getElementById('eb-ck').textContent='Prices on this card checked '+x.ck+'. The card updates automatically when we re-check.'}}
function fit(){{try{{var d=F.contentDocument,w=F.style.width;F.style.width='340px';F.style.height='10px';var hn=Math.ceil(d.documentElement.scrollHeight)+4;F.style.width=w;var h=Math.ceil(d.documentElement.scrollHeight)+4;F.style.height=h+'px';code(Math.max(h,hn))}}catch(err){{code(560)}}}}
function go(){{var x=cur();F.style.width=W.value+'px';F.src='/embed/'+x.s+'.html'+(H.value==='auto'?'':'?theme='+H.value);code(340);history.replaceState(null,'','?card='+encodeURIComponent(x.s)+(H.value==='auto'?'':'&theme='+H.value))}}
F.addEventListener('load',fit);window.addEventListener('message',function(ev){{if(ev.source===F.contentWindow&&ev.data&&ev.data.tp==='toolpick-embed')F.style.height=ev.data.h+'px'}});[T,H,W].forEach(function(el){{el.addEventListener('change',go)}});
document.getElementById('eb-cp').addEventListener('click',function(){{C.select();var ok=document.getElementById('eb-ok');(navigator.clipboard?navigator.clipboard.writeText(C.value):Promise.reject()).then(function(){{ok.textContent='Copied.'}},function(){{try{{document.execCommand('copy');ok.textContent='Copied.'}}catch(x){{ok.textContent='Select the code and copy it.'}}}})}});go()}})();</script>"""
page("/embed.html", "Embed live AI tool price cards on your site · ToolPick", "Free embeddable price cards for 82 AI tools and every ToolPick comparison: checked prices, free plans and like-for-like verdicts that update themselves.", EMBED_BODY,
     [crumbs([("Home", "/"), ("Embed price cards", "/embed.html")])])
# link the card from every tool and compare page
for _x in EMBED_TOOLS + EMBED_CMP:
    _fp = "public" + (turl(_x["n"]) if _x["k"] == "t" else "/" + _x["s"] + ".html")
    _h = open(_fp).read()
    if "/embed.html?card=" not in _h:
        open(_fp, "w").write(_h.replace("</main>", f'<p class="small">Writing about this? <a href="/embed.html?card={_x["s"]}">Embed this price card</a> — it updates when we re-check prices.</p></main>', 1))

# v35: trust panel on every tool page + How we pick page
for _n in tool_pages:
    _fp = "public" + turl(_n); _h = open(_fp).read(); _i = _h.find('<section class="verdict card best"')
    if _i < 0 or 'id="tbh"' in _h: continue
    _j = _h.index("</section>", _i) + len("</section>")
    open(_fp, "w").write(_h[:_j] + trust_panel(find(_n)) + _h[_j:])
_aff = sum(1 for c in CATEGORIES for t in c["tools"] if t.get("affiliate"))
HWP_DATE = "2026-10-20"
_ih = open("public/index.html").read()
_out, _pos = [], 0
for _m in _re.finditer(r'(?s)<article class="card[^"]*">.*?</article>', _ih):
    _a = _m.group(0); _sl = _re.search(r'href="/tools/([^"]+)\.html"', _a)
    if _sl: _a = _re.sub(r'(?s)<details class="tb">.*?</details>', '<p class="small" style="margin:6px 0 0"><a href="/tools/' + _sl.group(1) + '.html#tbh">Why trust this pick?</a></p>', _a)
    _out.append(_ih[_pos:_m.start()] + _a); _pos = _m.end()
open("public/index.html", "w").write("".join(_out) + _ih[_pos:])
_hw_body = f"""<p class="small"><a href="/">ToolPick</a> › How we pick</p><h1>How ToolPick picks AI tools</h1>
<p class="tag">Many "best AI tools" lists are written or paid for by the vendors they rank. Here is exactly how our picks are made, what we check, and what we don't do, so you can judge every pick for yourself.</p>
<section class="card"><h2 style="margin-top:0">What every pick shows</h2><p>Every tool card and tool page has a <b>“Why trust this pick”</b> box with five facts:</p><ol>
<li><b>How we picked.</b> {e(HOW_PICKED)}</li>
<li><b>The price on the date we checked it</b>, copied from the tool's official pricing page, with a link to that page.</li>
<li><b>Price history</b> from our dated checks ({", ".join(_PH_DATES)}), so you can see whether a price has moved.</li>
<li><b>Money.</b> Whether we earn anything if you buy. Right now {"no tool on ToolPick has an affiliate link" if not _aff else f"{_aff} tools have affiliate links, each labelled"}, and no vendor pays for placement.</li>
<li><b>One real limitation</b>, taken from the pricing page we checked: no free plan or trial only, one-time credits, a lighter entry tier, yearly-only billing, usage costs, per-seat pricing, or limits on the free plan. If we haven't recorded one, we say so instead of inventing one.</li></ol></section>
<h2>What we compare, and how</h2><ul><li><b>Same job only.</b> A tool is only called cheaper than another if both do the same main job.</li><li><b>Same billing.</b> Monthly prices are compared with monthly prices, and billed-yearly prices with billed-yearly prices.</li><li><b>Same tier.</b> Lighter entry tiers (like Google AI Plus or ChatGPT Go) are compared with each other; against full plans like Claude Pro we use the comparable tier (like Google AI Pro).</li><li><b>No guessing.</b> If we can't verify a price, the tool shows “check site” and is never counted in a total or a “cheapest” claim.</li><li><b>Best Value is separate from price.</b> It's our overall-value pick for a category and never replaces the price answer.</li></ul>
<h2>What we don't do</h2><ul><li>We don't hands-on test every tool, and we don't claim to. We don't publish star ratings or reviews.</li><li>We don't accept payment for placement or rankings.</li><li>We don't show prices we haven't checked on the official page.</li></ul>
<h2>Keep us honest</h2><p>Prices change. Each pick links to the official pricing page so you can confirm before you buy. See every recorded change on the <a href="/price-changes.html">price changes log</a>, or watch the tools you pay for with the <a href="/watchlist.html">price watchlist</a>.</p>"""
page("/how-we-pick.html", "How ToolPick Picks AI Tools — Checked Prices, No Paid Rankings | ToolPick",
     "How ToolPick picks AI tools: official pricing pages with checked dates, same-job and same-billing comparisons, price history, earn disclosure and one real limitation per tool. Not paid placement.",
     _hw_body, [crumbs([("ToolPick", "/"), ("How we pick", "/how-we-pick.html")])])

# --- v37: Real cost of AI video (credits -> seconds -> $ per minute), verified per official pricing page ---
VC = _tm0.VIDEO_CREDITS; VIDEO_CHECKED = _tm0.VIDEO_CHECKED
def _secs(cr, cps): return cr / cps
_vcd = [dict(n=n, s=slug(n), u=turl(n), pr=v["pricing"], fr=v["free"], tp=v["topup"], tn=v["topup_note"],
             pl=[dict(n=a, p=b, c=c) for a, b, c in v["plans"]], md=[dict(n=a, r=b, c=c) for a, b, c in v["models"]]) for n, v in VC.items()]
_VCJSON = json.dumps(_vcd).replace("</", "<\\/")
def _mlabel(m): return m[0] + (f", {m[1]}" if m[1] else " (resolution not stated)")
_vt_rows = ""
for n, v in VC.items():
    for m in v["models"]:
        _vt_rows += f"<tr><th scope='row'><a href='{turl(n)}'>{e(n)}</a></th><td>{e(_mlabel(m))}</td><td>{m[2]:g}</td>" + "".join(
            f"<td>{int(_secs(c, m[2]))}s <span class='small'>(${p}: ${p / (_secs(c, m[2]) / 60):.2f}/min)</span></td>" for a, p, c in v["plans"]) + "</tr>"
VC_JS = r'''const D=__VC__;const $=id=>document.getElementById(id);const M=v=>'$'+(Math.round(v*100)/100).toFixed(2).replace(/\.00$/,'');
const key=m=>m.n+'|'+m.r;const lab=m=>m.n+(m.r?', '+m.r:' (resolution not stated)');
const q=new URLSearchParams(location.search);let sel={};D.forEach(t=>{const i=t.md.findIndex(m=>m.n=='Seedance 2.5'&&m.r=='720p');sel[t.s]=i>=0?i:0});
(q.get('m')||'').split(',').forEach(p=>{const [s,i]=p.split(':');const t=D.find(x=>x.s==s);if(t&&t.md[+i])sel[s]=+i});
const qs=parseInt(q.get('s')),qt=parseInt(q.get('t'));if(qs>0&&qs<=36000)$('vc-sec').value=qs;if([1,2,3,5].includes(qt))$('vc-try').value=qt;
D.forEach(t=>{const s=$('vm-'+t.s);s.innerHTML=t.md.map((m,i)=>'<option value="'+i+'">'+lab(m)+' · '+m.c+' credits/sec</option>').join('');s.value=sel[t.s];s.onchange=()=>{sel[t.s]=+s.value;go()}});
function cost(t,need){let best=null;t.pl.forEach(p=>{const ex=Math.max(0,need-p.c);if(ex>0&&!t.tp)return;const usd=p.p+(ex>0?Math.ceil(ex/t.tp):0);if(!best||usd<best.usd)best={plan:p,usd:usd,extra:ex,top:ex>0}});
if(best)return best;const top=t.pl[t.pl.length-1];return{plan:top,usd:null,extra:need-top.c,top:true}}
function go(){const sec=Math.max(1,Math.min(36000,parseInt($('vc-sec').value)||0)),tries=parseInt($('vc-try').value);const R=[];
D.forEach(t=>{const m=t.md[sel[t.s]];const need=Math.ceil(sec*tries*m.c);const c=cost(t,need);R.push({t,m,need,c});
const per=c.usd!=null?c.usd/(sec/60):null;const cap=c.plan.c/m.c;
$('vo-'+t.s).innerHTML='<p class="vc-big">'+(c.usd!=null?M(c.usd)+'/mo':'More than the biggest plan')+'</p>'+
(c.usd!=null?'<p class="small" style="margin:0">'+(c.top?c.plan.n+' plan '+M(c.plan.p)+' + '+M(Math.ceil(c.extra/t.tp))+' of top-up credits ('+t.tn+')':c.plan.n+' plan ('+c.plan.c.toLocaleString()+' credits)')+' · <b>'+M(per)+' per minute you keep</b></p>':'<p class="small" style="margin:0">Needs '+need.toLocaleString()+' credits; '+c.plan.n+' has '+c.plan.c.toLocaleString()+'. Extra: '+t.tn+'.</p>')+
'<p class="small">Needs '+need.toLocaleString()+' credits ('+sec+'s × '+tries+' tr'+(tries==1?'y':'ies')+' × '+m.c+'/sec). The '+c.plan.n+' plan covers about '+Math.floor(cap)+'s of '+m.n+(m.r?' '+m.r:'')+'.</p>'});
const g={};R.forEach(r=>{(g[key(r.m)]=g[key(r.m)]||[]).push(r)});const same=Object.values(g).filter(a=>a.length>1);let v='';
if(same.length){v=same.map(a=>{const ok=a.filter(r=>r.c.usd!=null).sort((x,y)=>x.c.usd-y.c.usd);if(ok.length<2)return 'Same model ('+lab(a[0].m)+'): not enough plan data to rank.';const w=ok[0],n=ok[1];
return 'Same model ('+lab(w.m)+'), monthly billing: <b>'+w.t.n+' is cheaper</b> at '+M(w.c.usd)+'/mo vs '+n.t.n+' at '+M(n.c.usd)+'/mo for '+sec+'s of finished video'+(tries>1?' with '+tries+' tries each':'')+'.'}).join('<br>');
const solo=R.filter(r=>g[key(r.m)].length==1).map(r=>r.t.n);if(solo.length)v+='<br><span class="small">'+solo.join(' and ')+(solo.length==1?' uses':' use')+' a different model here, so '+(solo.length==1?'it is':'they are')+' not ranked. Pick the same model to compare.</span>'}
else v='Each tool uses a different model here, so we don\u2019t rank them: credits per second differ by model. Pick the same model (e.g. Seedance 2.5, 720p) to compare like for like.';
$('vc-verdict').innerHTML=v;history.replaceState(null,'','?s='+sec+'&t='+tries+'&m='+D.map(t=>t.s+':'+sel[t.s]).join(','))}
['vc-sec','vc-try'].forEach(i=>{$(i).addEventListener('input',go);$(i).addEventListener('change',go)});
$('vc-copy').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);$('vc-st').textContent='Link copied.'}catch(e){$('vc-st').textContent='Copy this link: '+location.href}};go();
'''
_vc_cards = "".join(f'<article class="card"><h3 style="margin:0"><a href="{turl(n)}">{e(n)}</a></h3><p class="small" style="margin:2px 0 8px">Free: {e(v["free"])} · <a href="{e(v["pricing"])}" rel="noopener" target="_blank">official pricing</a></p><label for="vm-{slug(n)}">Model</label><select id="vm-{slug(n)}" style="width:100%"></select><div id="vo-{slug(n)}" aria-live="polite"></div></article>' for n, v in VC.items())
_vc_body = f"""<style>.vc-big{{font-size:1.5rem;font-weight:800;margin:10px 0 2px}}.vc-in{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));align-items:end}}.vc-in input,.vc-in select{{width:100%}}</style>
<p class="small"><a href="/save-money.html">Save money</a> › Real cost of AI video</p><h1>What does a minute of AI video really cost?</h1>
<p class="tag">AI video plans are sold in credits, and each model burns credits at a different rate per second. Enter how much finished video you need a month and see which plan you'd actually need, and the real price per minute, from each tool's official pricing page.</p>
<div class="bnote"><p class="small" style="margin:0"><b>Why this exists:</b> people regularly report running out of credits after a few short clips, e.g. “About… FIVE SHORT (&lt;10s) videos later, i ran out of my credits for the month” (<a href="https://www.reddit.com/r/generativeAI/comments/1vxzwfk/really_bad_experience_with_runway_pro_plan_avoid/" rel="noopener" target="_blank">r/generativeAI</a>) and “a short 15sec vid. It uses 70% of my credits in one go” (<a href="https://www.reddit.com/r/runwayml/comments/1vv1v6j/does_signing_up_feel_like_getting_ripped_after/" rel="noopener" target="_blank">r/runwayml</a>).</p></div>
<div class="builder"><div class="vc-in"><div><label for="vc-sec">Seconds of finished video per month</label><input id="vc-sec" type="number" inputmode="numeric" min="1" max="36000" value="60"></div>
<div><label for="vc-try">Tries per clip you keep</label><select id="vc-try"><option value="1">1 (every generation is a keeper)</option><option value="2">2</option><option value="3">3</option><option value="5">5</option></select></div>
<div><button type="button" class="bbtn" id="vc-copy">Copy link to this result</button> <span id="vc-st" class="small" role="status"></span></div></div>
<p id="vc-verdict" class="pick" aria-live="polite" style="margin-top:12px"></p></div>
<h2>Your result by tool</h2><div class="grid">{_vc_cards}</div>
<h2>How many seconds each plan buys</h2><p class="small">Monthly billing, using all of a plan's monthly credits on one model. Credits per second and plan credits copied from each official pricing page on {VIDEO_CHECKED}. “$/min” is the plan price divided by the minutes it buys.</p>
<div class="tw"><table><caption class="small" style="text-align:left">Columns are each tool's three paid plans, cheapest first.</caption><tr><th scope="col">Tool</th><th scope="col">Model</th><th scope="col">Credits/sec</th><th scope="col">Plan 1</th><th scope="col">Plan 2</th><th scope="col">Plan 3</th></tr>{_vt_rows}</table></div>
<p class="small">Plans: """ + " · ".join(f"{e(n)}: " + ", ".join(f"{a} ${b}/mo ({c:,} credits)" for a, b, c in v["plans"]) for n, v in VC.items()) + f""".</p>
<h2>How we compare</h2><ul><li><b>Same model only.</b> We only call one tool cheaper when both use the same model at the same resolution (for example Seedance 2.5 at 720p on Pika and Luma). Credit rates differ by model, so other combinations are shown but not ranked.</li><li><b>Monthly billing.</b> All plan prices here are billed monthly.</li><li><b>Only what the pricing page shows.</b> Where a page shows no top-up price, we say so instead of estimating. Credits can be used on other features too; this assumes all go to video.</li><li><b>Not included yet:</b> Kling AI (we couldn't load its pricing page), and HeyGen (its pricing page doesn't show credits per minute). Avatar tools like Synthesia do a different job.</li></ul>
<p class="small">Related: <a href="/best-ai-video-tools.html">Best AI video tools</a> · <a href="/compare/runway-vs-pika.html">Runway vs Pika</a> · <a href="/renewal-reminders.html">Renewal reminders</a> · <a href="/how-we-pick.html">How we pick</a></p>
<script>""" + VC_JS.replace("__VC__", _VCJSON) + "</script>"
page("/ai-video-cost.html", "What a Minute of AI Video Really Costs — Runway, Pika, Luma Credits | ToolPick",
     f"How many seconds of video each Runway, Pika and Luma plan really buys, and the real price per minute, from official credit rates (checked {VIDEO_CHECKED}). Same-model comparisons only.",
     _vc_body, [crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Real cost of AI video", "/ai-video-cost.html")])])
for _n in VC:
    _fp = "public" + turl(_n); _h = open(_fp).read()
    if "/ai-video-cost.html" not in _h:
        open(_fp, "w").write(_h.replace('<section class="card tbp"', f'<p class="pick"><b>Credits run out fast?</b> See how many seconds of video each {e(_n)} plan really buys, and the price per minute: <a href="/ai-video-cost.html">Real cost of AI video →</a></p><section class="card tbp"', 1))
_fp = "public/best-ai-video-tools.html"; _h = open(_fp).read()
open(_fp, "w").write(_h.replace("</h1>", '</h1><p class="pick">Video plans are sold in credits. <a href="/ai-video-cost.html">See what a minute of AI video really costs →</a></p>', 1))

# --- v38: Real cost of AI voice (characters -> minutes -> $ per minute), verified per official pricing page ---
VO = _tm0.VOICE_COSTS; VOICE_CHECKED = _tm0.VOICE_CHECKED; CPM = _tm0.VOICE_CPM
_vod = [dict(n=n, s=slug(n), u=turl(n), md=v["model"], sm=v["same"], tn=v["topup_note"], nt=v["note"],
             pl=[dict(n=a, p=b, c=c, x=x) for a, b, c, x in v["plans"]]) for n, v in VO.items()]
_VOJSON = json.dumps(_vod).replace("</", "<\\/")
_vo_rows = "".join(f"<tr><th scope='row'><a href='{turl(n)}'>{e(n)}</a></th><td>{e(v['model'])}</td>" + "".join(
    f"<td>{a} ${b}: {c:,} chars ≈ {c // CPM:,} min <span class='small'>(${b / (c / CPM):.3f}/min)</span></td>" for a, b, c, x in v["plans"][:3]) + "</tr>" for n, v in VO.items())
VO_JS = r'''const D=__VO__,CPM=__CPM__;const $=id=>document.getElementById(id);const M=v=>'$'+(Math.round(v*100)/100).toFixed(2).replace(/\.00$/,'');
const q=new URLSearchParams(location.search);const qm=parseInt(q.get('m')),qt=parseInt(q.get('t'));if(qm>0&&qm<=100000)$('vo-min').value=qm;if([1,2,3].includes(qt))$('vo-try').value=qt;
function cost(t,need){let best=null;t.pl.forEach(p=>{const ex=Math.max(0,need-p.c);if(ex>0&&p.x==null)return;const add=ex>0?Math.ceil(ex/CPM)*p.x:0;const usd=p.p+add;if(!best||usd<best.usd)best={plan:p,usd:usd,extra:ex,add:add}});
if(best)return best;return{plan:t.pl[t.pl.length-1],usd:null}}
function go(){const min=Math.max(1,Math.min(100000,parseInt($('vo-min').value)||0)),tries=parseInt($('vo-try').value);const need=min*tries*CPM;const R=[];
D.forEach(t=>{const c=cost(t,need);R.push({t,c});const per=c.usd!=null?c.usd/min:null;
$('vr-'+t.s).innerHTML='<p class="vc-big">'+(c.usd!=null?M(c.usd)+'/mo':'More than the biggest plan')+'</p>'+
(c.usd!=null?'<p class="small" style="margin:0">'+c.plan.n+' plan '+M(c.plan.p)+(c.extra>0?' + '+Math.ceil(c.extra/CPM).toLocaleString()+' extra minutes at '+M(c.plan.x)+' = '+M(c.add):' ('+c.plan.c.toLocaleString()+' characters)')+' · <b>'+M(per)+' per minute you keep</b></p>':'<p class="small" style="margin:0">Needs '+need.toLocaleString()+' characters; '+c.plan.n+' covers '+c.plan.c.toLocaleString()+'. Extra: '+t.tn+'.</p>')+
'<p class="small">Model: '+t.md+'. '+t.nt+'</p>'});
const ok=R.filter(r=>r.t.sm&&r.c.usd!=null).sort((x,y)=>x.c.usd-y.c.usd);let v;
if(ok.length>=2){const w=ok[0],n=ok[1];v='Same model ('+w.t.sm+'), monthly billing: <b>'+w.t.n+' is cheaper</b> at '+M(w.c.usd)+'/mo vs '+n.t.n+' at '+M(n.c.usd)+'/mo for '+min.toLocaleString()+' min of finished audio'+(tries>1?' with '+tries+' takes each':'')+'.'}
else v='Not enough same-model plan data to rank at this amount.';
const solo=R.filter(r=>!r.t.sm).map(r=>r.t.n);if(solo.length)v+='<br><span class="small">'+solo.join(' and ')+' doesn\u2019t name its voice model, so it isn\u2019t ranked.</span>';
$('vo-verdict').innerHTML=v;history.replaceState(null,'','?m='+min+'&t='+tries)}
['vo-min','vo-try'].forEach(i=>{$(i).addEventListener('input',go);$(i).addEventListener('change',go)});
$('vo-copy').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);$('vo-st').textContent='Link copied.'}catch(e){$('vo-st').textContent='Copy this link: '+location.href}};go();
'''
_vo_cards = "".join(f'<article class="card"><h3 style="margin:0"><a href="{turl(n)}">{e(n)}</a></h3><p class="small" style="margin:2px 0 8px">Free: {e(v["free"])} · <a href="{e(v["pricing"])}" rel="noopener" target="_blank">official pricing</a></p><div id="vr-{slug(n)}" aria-live="polite"></div></article>' for n, v in VO.items())
_vo_left = "".join(f"<li><a href='{turl(n)}'>{e(n)}</a>: {e(r)}.</li>" for n, r in _tm0.VOICE_LEFT_OUT)
_vo_body = f"""<style>.vc-big{{font-size:1.5rem;font-weight:800;margin:10px 0 2px}}.vc-in{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));align-items:end}}.vc-in input,.vc-in select{{width:100%}}</style>
<p class="small"><a href="/save-money.html">Save money</a> › Real cost of AI voice</p><h1>What does a minute of AI voice really cost?</h1>
<p class="tag">Text-to-speech plans are sold in characters or credits, not minutes. Enter how many minutes of finished speech you need a month and see which plan you'd actually need, and the real price per minute, from each tool's official pricing page.</p>
<div class="builder"><div class="vc-in"><div><label for="vo-min">Minutes of finished speech per month</label><input id="vo-min" type="number" inputmode="numeric" min="1" max="100000" value="60"></div>
<div><label for="vo-try">Takes per line you keep</label><select id="vo-try"><option value="1">1 (every take is a keeper)</option><option value="2">2</option><option value="3">3</option></select></div>
<div><button type="button" class="bbtn" id="vo-copy">Copy link to this result</button> <span id="vo-st" class="small" role="status"></span></div></div>
<p id="vo-verdict" class="pick" aria-live="polite" style="margin-top:12px"></p></div>
<h2>Your result by tool</h2><div class="grid">{_vo_cards}</div>
<h2>How many minutes each plan buys</h2><p class="small">Monthly billing, using all of a plan's credits on speech. Characters per plan and credit rates copied from each official pricing page on {VOICE_CHECKED}. Minutes use ElevenLabs' own estimate of about {CPM:,} characters per minute (its Starter plan's 30,000 credits ≈ 30 minutes), applied to every tool so the unit is the same.</p>
<div class="tw"><table><caption class="small" style="text-align:left">First three paid plans, cheapest first.</caption><tr><th scope="col">Tool</th><th scope="col">Model</th><th scope="col">Plan 1</th><th scope="col">Plan 2</th><th scope="col">Plan 3</th></tr>{_vo_rows}</table></div>
<p class="small">Sources: ElevenLabs: “Text to Speech 1 credit per character”, and the extra-minute price per plan from its “Text to Speech (UI)” table (Starter ~$0.20, Creator ~$0.18, Pro/Scale/Business ~$0.17). Luma: “ElevenLabs v3 text-to-speech 21 credits/1000 characters”. Runway: “Text to Speech 1 credit/50 chars”. All plans: """ + " · ".join(f"{e(n)}: " + ", ".join(f"{a} ${b}/mo" for a, b, c, x in v["plans"]) for n, v in VO.items()) + f""".</p>
<h2>How we compare</h2><ul><li><b>Same unit.</b> Everything is converted to characters, then minutes at the same rate.</li><li><b>Same model only for the verdict.</b> ElevenLabs and Luma both sell ElevenLabs v3 speech, so we rank them. Runway doesn't name its voice model, so it's shown but not ranked.</li><li><b>Monthly billing only.</b> Prices are the regular monthly price; ElevenLabs' $11 first month for Creator isn't used.</li><li><b>Only what the pricing page shows.</b> Extra minutes are added only where a price is shown (ElevenLabs). Otherwise we say “More than the biggest plan” instead of guessing.</li><li><b>The ElevenLabs API</b> is billed separately per 1,000 characters (pay as you go) and isn't mixed in here.</li></ul>
<h2>Tools left out</h2><ul>{_vo_left}<li>Music tools (Suno, Udio) and transcription tools (Otter) do a different job.</li></ul>
<p class="small">Related: <a href="/best-ai-audio-tools.html">Best AI audio tools</a> · <a href="/ai-video-cost.html">Real cost of AI video</a><a href="/ai-voice-cost.html">Real cost of AI voice</a> · <a href="/renewal-reminders.html">Renewal reminders</a> · <a href="/how-we-pick.html">How we pick</a></p>
<script>""" + VO_JS.replace("__VO__", _VOJSON).replace("__CPM__", str(CPM)) + "</script>"
page("/ai-voice-cost.html", "What a Minute of AI Voice Really Costs — ElevenLabs, Luma, Runway | ToolPick",
     f"How many minutes of text-to-speech each ElevenLabs, Luma and Runway plan really buys, and the real price per minute, from official pricing pages (checked {VOICE_CHECKED}).",
     _vo_body, [crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Real cost of AI voice", "/ai-voice-cost.html")])])
for _n in list(VO) + ["Murf"]:
    _fp = "public" + turl(_n); _h = open(_fp).read()
    if "/ai-voice-cost.html" not in _h:
        open(_fp, "w").write(_h.replace('<section class="card tbp"', f'<p class="pick"><b>Paying for text to speech?</b> See how many minutes of speech each plan really buys, and the price per minute: <a href="/ai-voice-cost.html">Real cost of AI voice →</a></p><section class="card tbp"', 1))
_fp = "public/best-ai-audio-tools.html"; _h = open(_fp).read()
open(_fp, "w").write(_h.replace("</h1>", '</h1><p class="pick">Voice plans are sold in characters. <a href="/ai-voice-cost.html">See what a minute of AI voice really costs →</a></p>', 1))

# --- v41: high-intent coding pages (prices re-verified 2026-10-21 on official pages) ---
CD = _tm0.CODING_V41; CODING_CHECKED = _tm0.CODING_CHECKED
def _cl(t): return t.get("label", t["n"])
def _pl(x): return f'{e(x[0])} ${x[1]}/mo' + (f' <span class="small">({e(x[2])})</span>' if len(x) > 2 and x[2] else "")
def _src(t): return f'<a href="{e(t["pr"])}" rel="noopener" target="_blank">official pricing</a>'
_V41_PAGES = []
_cur = next(t for t in CD if t["n"] == "Cursor")
_rows = "".join(f"<tr><th scope='row'><a href='{turl(t['n'])}'>{e(_cl(t))}</a></th><td>{e(t['free'])}</td><td>{_pl(t['entry'])}</td><td>{_pl(t['main']) if t['main'] != t['entry'] else '—'}</td><td>{('$%d/mo (%s, billed yearly)' % (t['yearly'][1], e(t['yearly'][0]))) if t['yearly'] else 'not shown'}</td><td>{_src(t)}</td></tr>" for t in CD)
_tbl = f"""<div class="tw"><table><caption class="small" style="text-align:left">Individual plans, monthly billing, from each official pricing page on {CODING_CHECKED}. Yearly prices are shown separately and never mixed into the monthly ranking.</caption><tr><th scope="col">Tool</th><th scope="col">Free plan</th><th scope="col">Cheapest paid plan</th><th scope="col">Main plan (if different)</th><th scope="col">Yearly option</th><th scope="col">Source</th></tr>{_rows}</table></div>"""
_left = "".join(f"<li><a href='{turl(n)}'>{e(n)}</a>: {e(r)}.</li>" for n, r in _tm0.CODING_LEFT_OUT)
_how = f"""<h2>How we compare</h2><ul><li><b>Monthly billing</b>, individual plans only. Team plans (Cursor Teams $30+/user, Windsurf Teams $80 + $40/seat) aren't ranked against individual plans.</li><li><b>Usage limits differ</b> between tools and aren't published in the same unit, so we compare plan prices and say what each plan includes; we don't guess usage.</li><li><b>Prices re-checked {CODING_CHECKED}</b> on each official pricing page. If a price couldn't be checked, the tool is left out.</li></ul><h2>Left out</h2><ul>{_left}</ul>"""
def _ld_list(name, path, items): return [{"@context": "https://schema.org", "@type": "ItemList", "name": name, "url": BASE + path, "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": BASE + turl(n)} for i, n in enumerate(items)]}]
def _ld_faq(qas): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}
def _faq(qas): return "<h2>FAQ</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in qas)
# A) Cursor alternatives
_alts = [t for t in CD if t["n"] != "Cursor"]
_cmp = "".join(f"<li><a href='{turl(t['n'])}'>{e(_cl(t))}</a>: {_pl(t['entry'])} — ${_cur['main'][1] - t['entry'][1]}/mo less than Cursor Premium (${_cur['main'][1]}/mo).</li>" for t in sorted(_alts, key=lambda t: t["entry"][1]))
_qa_a = [("What is the cheapest alternative to Cursor?", f"GitHub Copilot Pro at $10/mo (monthly billing, checked {CODING_CHECKED}). Cursor's own Plus plan is $8/mo but only includes Grok models."),
         ("Is Claude Code included in Claude Pro?", f"Yes. Claude's pricing page lists Claude Code in Pro ($20/mo billed monthly, $17/mo billed yearly), but not in the Free plan (checked {CODING_CHECKED}).")]
_a_body = f"""<p class="small"><a href="/best-ai-coding-tools.html">AI coding tools</a> › Cursor alternatives</p><h1>Cursor alternatives, with prices checked today</h1>
<p class="tag">Cursor Premium is ${_cur['main'][1]}/mo. Here is what GitHub Copilot, Windsurf, Claude Code and Warp cost instead, from each official pricing page ({CODING_CHECKED}).</p>
<p class="pick"><b>Cheapest paid alternative:</b> <a href="{turl('GitHub Copilot')}">GitHub Copilot Pro</a> at $10/mo. Cursor's own Plus plan is $8/mo, but its pricing page says only Grok models are available on it.</p>
<h2>Alternatives vs Cursor Premium (${_cur['main'][1]}/mo)</h2><ul>{_cmp}</ul><h2>All plans side by side</h2>{_tbl}{_how}{_faq(_qa_a)}
<p class="small">Related: <a href="/compare/cursor-vs-claude-code.html">Cursor vs Claude Code</a> · <a href="/cheapest-ai-coding-assistant.html">Cheapest AI coding assistant</a> · <a href="/compare/github-copilot-vs-cursor.html">GitHub Copilot vs Cursor</a> · <a href="/compare/cursor-vs-windsurf.html">Cursor vs Windsurf</a></p>"""
page("/cursor-alternatives.html", f"Cursor Alternatives ({CODING_CHECKED[:4]}): Copilot, Windsurf, Claude Code, Warp Prices | ToolPick",
     f"Cheaper alternatives to Cursor with prices checked {CODING_CHECKED} on official pages: GitHub Copilot Pro $10/mo, Windsurf Pro $20, Claude Pro (Claude Code) $20, Warp Build $20, vs Cursor Premium $30.",
     _a_body, _ld_list("Cursor alternatives", "/cursor-alternatives.html", [t["n"] for t in _alts]) + [_ld_faq(_qa_a), crumbs([("ToolPick", "/"), ("AI coding tools", "/best-ai-coding-tools.html"), ("Cursor alternatives", "/cursor-alternatives.html")])])
_V41_PAGES.append("/cursor-alternatives.html")
# B) Cursor vs Claude Code
_cc = next(t for t in CD if t["n"] == "Claude")
_b_rows = "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in [
  ("Free plan", "Free $0 (limited AI usage)", "Free $0, but Claude Code isn't included"),
  ("Cheapest paid", "Plus $8/mo (only Grok models)", "Pro $20/mo (includes Claude Code)"),
  ("Main plan", "Premium $30/mo (most popular)", "Pro $20/mo"),
  ("Higher tier", "Super $100/mo · Ultra $200/mo", "Max from $100/mo"),
  ("Yearly billing", "not shown on the pricing page", "Pro $17/mo ($200 billed up front)"),
  ("What it is", "An AI code editor", "A coding agent included with a Claude subscription, alongside the Claude chat app")])
_qa_b = [("Is Claude Code cheaper than Cursor?", f"On monthly billing, Claude Pro (which includes Claude Code) is $20/mo and Cursor Premium is $30/mo. Cursor Plus is $8/mo but only includes Grok models (checked {CODING_CHECKED})."),
         ("Does the free Claude plan include Claude Code?", "No. Claude's pricing page lists Claude Code from the Pro plan up.")]
_b_body = f"""<p class="small"><a href="/best-ai-coding-tools.html">AI coding tools</a> › Cursor vs Claude Code</p><h1>Cursor vs Claude Code: price comparison</h1>
<p class="tag">Plans and prices from Cursor's and Claude's official pricing pages, checked {CODING_CHECKED}. Monthly billing unless marked.</p>
<p class="pick"><b>Verdict on price:</b> on monthly billing, the main plans are Claude Pro at $20/mo (with Claude Code) and Cursor Premium at $30/mo, so Claude Pro costs $10/mo less. Cursor Plus ($8/mo) is cheaper, but limited to Grok models.</p>
<div class="tw"><table><caption class="small" style="text-align:left">Cursor and Claude Code plans, checked {CODING_CHECKED}</caption><tr><th scope="col"></th><th scope="col"><a href="{turl('Cursor')}">Cursor</a></th><th scope="col"><a href="{turl('Claude')}">Claude Code</a></th></tr>{_b_rows}</table></div>
<p class="small">Sources: <a href="{e(_cur['pr'])}" rel="noopener" target="_blank">cursor.com/pricing</a> · <a href="{e(_cc['pr'])}" rel="noopener" target="_blank">claude.com/pricing</a>. Usage limits are set differently on each plan and aren't published in the same unit, so we don't compare usage.</p>{_faq(_qa_b)}
<p class="small">Related: <a href="/cursor-alternatives.html">Cursor alternatives</a> · <a href="/cheapest-ai-coding-assistant.html">Cheapest AI coding assistant</a> · <a href="/compare/github-copilot-vs-cursor.html">GitHub Copilot vs Cursor</a></p>"""
page("/compare/cursor-vs-claude-code.html", f"Cursor vs Claude Code ({CODING_CHECKED[:4]}): Pricing Compared | ToolPick",
     f"Cursor vs Claude Code prices checked {CODING_CHECKED}: Cursor Plus $8 (Grok models only), Premium $30; Claude Pro with Claude Code $20/mo or $17/mo yearly; Max from $100.",
     _b_body, _ld_list("Cursor vs Claude Code", "/compare/cursor-vs-claude-code.html", ["Cursor", "Claude"]) + [_ld_faq(_qa_b), crumbs([("ToolPick", "/"), ("Compare", "/compare-builder.html"), ("Cursor vs Claude Code", "/compare/cursor-vs-claude-code.html")])])
_V41_PAGES.append("/compare/cursor-vs-claude-code.html")
# C) Cheapest AI coding assistant
_rank = sorted(CD, key=lambda t: t["entry"][1])
_c_list = "".join(f"<li><a href='{turl(t['n'])}'>{e(_cl(t))}</a>: {_pl(t['entry'])} · {_src(t)}</li>" for t in _rank)
_qa_c = [("What is the cheapest AI coding assistant?", f"Free: GitHub Copilot, Cursor, Windsurf and Warp all have $0 plans. Cheapest paid on monthly billing: Cursor Plus at $8/mo (Grok models only), then GitHub Copilot Pro at $10/mo (checked {CODING_CHECKED})."),
         ("Is yearly billing cheaper?", "Where the official page shows it: Claude Pro is $17/mo billed yearly ($20 monthly), and Warp Build is $18/mo yearly ($20 monthly).")]
_c_body = f"""<p class="small"><a href="/best-ai-coding-tools.html">AI coding tools</a> › Cheapest AI coding assistant</p><h1>The cheapest way to get an AI coding assistant</h1>
<p class="tag">Free plans first, then the cheapest paid plans on monthly billing, from each official pricing page ({CODING_CHECKED}).</p>
<p class="pick"><b>Free:</b> GitHub Copilot, Cursor, Windsurf and Warp have $0 plans with limited usage (Claude's free plan doesn't include Claude Code). <b>Cheapest paid:</b> Cursor Plus $8/mo (Grok models only), or GitHub Copilot Pro $10/mo.</p>
<h2>Cheapest paid plan per tool (monthly billing)</h2><ol>{_c_list}</ol><h2>All plans side by side</h2>{_tbl}{_how}{_faq(_qa_c)}
<p class="small">Related: <a href="/cursor-alternatives.html">Cursor alternatives</a> · <a href="/compare/cursor-vs-claude-code.html">Cursor vs Claude Code</a> · <a href="/pay-less.html">Pay less for a tool</a></p>"""
page("/cheapest-ai-coding-assistant.html", f"Cheapest AI Coding Assistant ({CODING_CHECKED[:4]}): Free & Paid Plans Compared | ToolPick",
     f"The cheapest AI coding assistants, checked {CODING_CHECKED}: free plans from Copilot, Cursor, Windsurf, Warp; paid from Cursor Plus $8 (Grok only) and GitHub Copilot Pro $10/mo.",
     _c_body, _ld_list("Cheapest AI coding assistants", "/cheapest-ai-coding-assistant.html", [t["n"] for t in _rank]) + [_ld_faq(_qa_c), crumbs([("ToolPick", "/"), ("AI coding tools", "/best-ai-coding-tools.html"), ("Cheapest AI coding assistant", "/cheapest-ai-coding-assistant.html")])])
_V41_PAGES.append("/cheapest-ai-coding-assistant.html")
# one-line links from tool and compare pages
_V41_LINE = '<p class="pick small v41">Coding plans checked {d}: <a href="/cursor-alternatives.html">Cursor alternatives</a> · <a href="/compare/cursor-vs-claude-code.html">Cursor vs Claude Code</a> · <a href="/cheapest-ai-coding-assistant.html">Cheapest AI coding assistant</a></p>'.format(d=CODING_CHECKED)
V41_CHANGED = list(_V41_PAGES)
for _n in ["Cursor", "GitHub Copilot", "Windsurf", "Claude", "Warp"]:
    _fp = "public" + turl(_n); _h = open(_fp).read()
    if 'class="pick small v41"' not in _h: open(_fp, "w").write(_h.replace('<section class="card tbp"', _V41_LINE + '<section class="card tbp"', 1)); V41_CHANGED.append(turl(_n))
for _x in COMPARISONS:
    if any(n in ("Cursor", "Claude", "GitHub Copilot", "Windsurf", "Warp") for n in cnames(_x)) and any(n in ("Cursor", "GitHub Copilot", "Windsurf", "Warp") for n in cnames(_x)):
        _fp = f"public/compare/{_x[0]}.html"; _h = open(_fp).read()
        if 'v41"' not in _h: open(_fp, "w").write(_h.replace("</h1>", "</h1>" + _V41_LINE, 1)); V41_CHANGED.append(f"/compare/{_x[0]}.html")
open("public/llms.txt", "a").write(f"\n## AI coding prices\n- [Cursor alternatives]({BASE}/cursor-alternatives.html): GitHub Copilot, Windsurf, Claude Code, Warp vs Cursor, monthly prices checked {CODING_CHECKED}\n- [Cursor vs Claude Code]({BASE}/compare/cursor-vs-claude-code.html): plan-by-plan prices from both official pages\n- [Cheapest AI coding assistant]({BASE}/cheapest-ai-coding-assistant.html): free plans and cheapest paid monthly plans, yearly shown separately\n")

# --- v42: Free plan limits, side by side (verified 2026-10-22) ---
FL = _tm0.FREE_LIMITS; FREE_CHECKED = _tm0.FREE_CHECKED; _NS = _tm0.NS
_fcat = {}
for _c in CATEGORIES:
    for _t in _c["tools"]: _fcat.setdefault(_t["name"], _c)
def _cell(v): return '<span class="small" style="color:var(--mu,#555)">not stated</span>' if v == _NS else e(v)
_frows = ""
for n, inc, lim, wm, com, up in FL:
    _c = _fcat[n]; _s2 = _tm0.FREE_SRC2.get(n)
    _frows += (f"<tr data-cat='{_c['id']}'><th scope='row'><a href='{turl(n)}'>{e(n)}</a><br><span class='small'>{e(_c['name'])}</span></th><td>{_cell(inc)}</td><td>{_cell(lim)}</td><td>{_cell(wm)}</td><td>{_cell(com)}</td><td>{_cell(up)}</td>"
               f"<td><a href='{e(_tm0.FREE_SRC[n])}' rel='noopener' target='_blank'>Pricing</a>" + (f" · <a href='{e(_s2)}' rel='noopener' target='_blank'>Help/terms</a>" if _s2 else "") + "</td></tr>")
_fcats = [c for c in CATEGORIES if any(_fcat[r[0]]["id"] == c["id"] for r in FL)]
_fopts = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in _fcats)
_fbest = "".join(f"<li data-cat='{cid}'><b>{e(next(c['name'] for c in CATEGORIES if c['id'] == cid))}:</b> <a href='{turl(n)}'>{e(n)}</a>, {e(why)}.</li>" for cid, (n, why) in _tm0.FREE_BEST.items())
_fleft = "".join(f"<li><a href='{turl(n)}'>{e(n)}</a>: {e(r)}.</li>" for n, r in _tm0.FREE_LEFT_OUT)
_fl_body = f"""<p class="small"><a href="/free.html">Free tools</a> › Free plan limits</p><h1>Free plan limits, side by side</h1>
<p class="tag">What each free plan really includes, its main limit, watermarks, commercial use, and the cheapest monthly upgrade. Every value read on the tool's official pricing, help or terms page on {FREE_CHECKED}; “not stated” means the page doesn't say.</p>
<h2>Best free plan for…</h2><ul id="fl-best">{_fbest}</ul>
<style>{"".join(f'html[data-fc="{c["id"]}"] #fl-t tr[data-cat]:not([data-cat="{c["id"]}"]),html[data-fc="{c["id"]}"] #fl-best li:not([data-cat="{c["id"]}"]){{display:none}}' for c in _fcats)}</style><script>(function(){{var q=new URLSearchParams(location.search).get("cat");if(q&&/^[a-z]+$/.test(q))document.documentElement.setAttribute("data-fc",q)}})()</script><p><label for="fl-cat">Show category</label> <select id="fl-cat"><option value="">All categories</option>{_fopts}</select> <span id="fl-n" class="small" role="status"></span></p>
<div class="tw"><table id="fl-t"><caption class="small" style="text-align:left">Free plans of {len(FL)} tools, checked {FREE_CHECKED}. Upgrade prices are monthly billing.</caption><tr><th scope="col">Tool</th><th scope="col">Free plan includes</th><th scope="col">Main limit</th><th scope="col">Watermark</th><th scope="col">Commercial use</th><th scope="col">Cheapest paid step-up (monthly)</th><th scope="col">Source</th></tr>{_frows}</table></div>
<h2>Not in the table</h2><ul>{_fleft}</ul>
<p class="small">Related: <a href="/free.html">Can I do it for free?</a> · <a href="/how-we-pick.html">How we pick</a></p>
<script>const S=document.getElementById('fl-cat'),R=[...document.querySelectorAll('#fl-t tr[data-cat]')],B=[...document.querySelectorAll('#fl-best li')],N=document.getElementById('fl-n');
function f(){{const v=S.value;if(v)document.documentElement.setAttribute('data-fc',v);else document.documentElement.removeAttribute('data-fc');let k=0;R.forEach(r=>{{const on=!v||r.dataset.cat==v;r.hidden=!on;if(on)k++}});B.forEach(li=>li.hidden=!!v&&li.dataset.cat!=v);N.textContent=k+' tool'+(k==1?'':'s')+' shown';if(v)history.replaceState(null,'','?cat='+v);else history.replaceState(null,'',location.pathname)}}
const q=new URLSearchParams(location.search).get('cat');if(q&&[...S.options].some(o=>o.value==q))S.value=q;S.addEventListener('change',f);f();</script>"""
page("/free-plan-limits.html", f"Free Plan Limits Side by Side ({FREE_CHECKED[:4]}): Watermarks, Commercial Use, Upgrade Prices | ToolPick",
     f"Free plans of {len(FL)} AI tools compared: what's included, the main limit, watermark, commercial use and the cheapest monthly upgrade, from official pages checked {FREE_CHECKED}.",
     _fl_body, [{"@context": "https://schema.org", "@type": "ItemList", "name": "AI tool free plan limits", "url": BASE + "/free-plan-limits.html", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": r[0], "url": BASE + turl(r[0])} for i, r in enumerate(FL)]},
                {"@context": "https://schema.org", "@type": "Dataset", "name": "AI tool free plan limits", "description": f"Free plan inclusions, limits, watermark, commercial use and cheapest monthly upgrade for {len(FL)} AI tools, from official pricing pages.", "url": BASE + "/free-plan-limits.html", "dateModified": FREE_CHECKED, "creator": {"@type": "Organization", "name": "ToolPick"}, "license": BASE + "/how-we-pick.html"},
                crumbs([("ToolPick", "/"), ("Free tools", "/free.html"), ("Free plan limits", "/free-plan-limits.html")])])
V42_CHANGED = ["/free-plan-limits.html"]
for n, inc, lim, wm, com, up in FL:
    _fp = "public" + turl(n); _h = open(_fp).read()
    if 'class="small v42"' in _h: continue
    _bits = [x for x in [inc if inc != _NS else "", ("limit: " + lim) if lim != _NS else ""] if x]
    _line = f'<p class="small v42"><b>Free plan:</b> {e("; ".join(_bits) or "see the official pricing page")} (checked {FREE_CHECKED}) · <a href="/free-plan-limits.html?cat={_fcat[n]["id"]}">Compare free plans</a></p>'
    _i = _h.find('<section class="verdict')
    if _i > 0: open(_fp, "w").write(_h[:_i] + _line + _h[_i:]); V42_CHANGED.append(turl(n))
_FLINE = f'<p class="pick small v42">Free plans compared side by side (limits, watermarks, commercial use), checked {FREE_CHECKED}: <a href="/free-plan-limits.html">Free plan limits →</a></p>'
for _fp in ["public/free.html"] + sorted(_glob0 for _glob0 in __import__("glob").glob("public/best-free-ai-*-tools.html")):
    _h = open(_fp).read()
    if 'v42"' not in _h: open(_fp, "w").write(_h.replace("</h1>", "</h1>" + _FLINE, 1)); V42_CHANGED.append(_fp[6:])
open("public/llms.txt", "a").write(f"\n## Free plan limits\n- [Free plan limits, side by side]({BASE}/free-plan-limits.html): {len(FL)} AI tools' free plans: what's included, main limit, watermark, commercial use, cheapest monthly upgrade; official pages checked {FREE_CHECKED}; filter with ?cat=video etc.\n")

# --- v44: Cursor pricing explained + AI subscription costs per month ---
CURSOR_CHECKED = _tm0.CURSOR_CHECKED
_cp_rows = "".join(f"<tr><th scope='row'>{e(p)}</th><td>{('$' + str(pr) + '/mo') if isinstance(pr, int) else ('$' + e(pr) + '/mo')}</td><td>{e(u)}</td><td>{e(a)}</td></tr>" for p, pr, u, a in _tm0.CURSOR_PLANS)
_qa_cp = [("Is Cursor free?", f"Yes. Cursor's Free plan is $0/month with limited AI usage, agent and chat requests (checked {CURSOR_CHECKED})."),
          ("What's the difference between Cursor Plus and Premium?", "Plus is $8/month and only includes Grok models. Premium is $30/month with 4x the usage of Plus, cloud agents, AI code reviews and third-party models at API list price."),
          ("Are third-party models included in the Cursor price?", "No. Cursor's pricing page says third-party model usage isn't included in the monthly prices and is billed separately by usage."),
          ("Do Cursor prices include tax?", "No. The pricing page says prices don't include applicable taxes or fees such as VAT.")]
_cp_body = f"""<p class="small"><a href="{turl('Cursor')}">Cursor</a> › Pricing explained</p><h1>Cursor pricing explained: free vs paid</h1>
<p class="tag">Every Cursor plan in one table, from <a href="https://cursor.com/pricing" rel="noopener" target="_blank">cursor.com/pricing</a> (checked {CURSOR_CHECKED}). Monthly prices, before tax.</p>
<p class="pick"><b>In short:</b> Free costs $0 with limited usage. Plus ($8/mo) is the cheapest paid plan but only has Grok models. Premium ($30/mo) is the most popular: 4x Plus usage, cloud agents, code reviews, and other models billed at API list price.</p>
<div class="tw"><table><caption class="small" style="text-align:left">Cursor plans, checked {CURSOR_CHECKED}. Usage is shown the way Cursor shows it: relative to Plus.</caption><tr><th scope="col">Plan</th><th scope="col">Price</th><th scope="col">Usage</th><th scope="col">What the pricing page says it adds</th></tr>{_cp_rows}</table></div>
<h2>Free vs paid: what changes</h2><ul><li><b>Free → Plus ($8/mo):</b> a shared AI usage pool instead of limited requests, but only Grok models.</li><li><b>Plus → Premium ($30/mo):</b> 4x the usage, cloud agents and automations, code hosting, AI code reviews, and third-party models at API list price.</li><li><b>Premium → Super ($100/mo) or Ultra ($200/mo):</b> 15x or 50x Plus usage; Super adds priority model access at peak times.</li><li><b>Watch out:</b> third-party model usage is billed separately on top of the plan price.</li></ul>
{_faq(_qa_cp)}
<p class="small">Related: <a href="/cursor-alternatives.html">Cursor alternatives</a> · <a href="/compare/cursor-vs-claude-code.html">Cursor vs Claude Code</a> · <a href="/cheapest-ai-coding-assistant.html">Cheapest AI coding assistant</a> · <a href="/free-plan-limits.html?cat=coding">Free plan limits</a></p>"""
page("/cursor-pricing.html", f"Cursor Pricing Explained ({CURSOR_CHECKED[:4]}): Free vs Plus vs Premium vs Ultra | ToolPick",
     f"Cursor pricing checked {CURSOR_CHECKED}: Free $0, Plus $8/mo (Grok models only), Premium $30 (4x usage), Super $100, Ultra $200, Teams $30+/user. What each plan adds and what costs extra.",
     _cp_body, [{"@context": "https://schema.org", "@type": "Product", "name": "Cursor", "url": BASE + "/cursor-pricing.html", "brand": {"@type": "Brand", "name": "Cursor"},
                 "offers": [{"@type": "Offer", "name": p, "price": pr, "priceCurrency": "USD", "url": "https://cursor.com/pricing"} for p, pr, u, a in _tm0.CURSOR_PLANS if isinstance(pr, int)]},
                _ld_faq(_qa_cp), crumbs([("ToolPick", "/"), ("Cursor", turl("Cursor")), ("Cursor pricing explained", "/cursor-pricing.html")])])
# B) AI subscription costs per month
_sc = {}
for n, pl, pr, q in _tm0.SUB_COSTS:
    _t = find(n); assert q in _t["price"], (n, q, _t["price"]); _sc[n] = (pl, pr, _t.get("checked", CHECKED), _t["pricing"])
def _m(v): return ("$%.2f" % v).replace(".00", "")
_sc_rows = "".join(f"<tr><th scope='row'><a href='{turl(n)}'>{e(n)}</a></th><td>{e(pl)}</td><td>{_m(pr)}/mo</td><td>{dt}</td><td><a href='{e(src)}' rel='noopener' target='_blank'>official pricing</a></td></tr>" for n, (pl, pr, dt, src) in sorted(_sc.items(), key=lambda kv: kv[1][1]))
_sc_stacks = "".join(f"<li><b>{e(r)}:</b> " + " + ".join(f"<a href='{turl(n)}'>{e(n)}</a> {e(_sc[n][0])} {_m(_sc[n][1])}" for n in ns) + f" = <b>{_m(sum(_sc[n][1] for n in ns))}/mo</b> ({_m(12 * sum(_sc[n][1] for n in ns))} a year)</li>" for r, ns in _tm0.SUB_STACKS)
_scv = sorted(v[1] for v in _sc.values()); _scmed = _scv[len(_scv) // 2]
_qa_sc = [("How much does an AI subscription cost per month?", f"Most popular entry plans we checked cost {_m(_scv[0])} to {_m(_scv[-1])} a month on monthly billing; the middle of the range is {_m(_scmed)}. ChatGPT Plus and Claude Pro are $20/mo."),
          ("How much do two or three AI tools cost together?", "Our example stacks range from " + _m(min(sum(_sc[n][1] for n in ns) for r, ns in _tm0.SUB_STACKS)) + " to " + _m(max(sum(_sc[n][1] for n in ns) for r, ns in _tm0.SUB_STACKS)) + " a month on monthly billing.")]
_sc_body = f"""<p class="small"><a href="/my-ai-costs.html">My AI costs</a> › AI subscription costs</p><h1>How much do AI subscriptions cost per month?</h1>
<p class="tag">The monthly price of {len(_sc)} popular AI subscriptions, and what common combinations add up to. Prices are monthly billing from each official pricing page, with the date we last checked.</p>
<p class="pick"><b>In short:</b> entry plans run {_m(_scv[0])}–{_m(_scv[-1])}/mo; the middle of the range is {_m(_scmed)}/mo. Our example stacks of two or three tools cost {_m(min(sum(_sc[n][1] for n in ns) for r, ns in _tm0.SUB_STACKS))}–{_m(max(sum(_sc[n][1] for n in ns) for r, ns in _tm0.SUB_STACKS))}/mo. <a href="/my-ai-costs.html#audit">Add up your own subscriptions →</a></p>
<h2>Example stacks (monthly billing)</h2><ul>{_sc_stacks}</ul>
<h2>Entry plan prices, cheapest first</h2><div class="tw"><table><caption class="small" style="text-align:left">The main individual plan of each tool, billed monthly. Prices change; always confirm on the official page.</caption><tr><th scope="col">Tool</th><th scope="col">Plan</th><th scope="col">Price</th><th scope="col">Checked</th><th scope="col">Source</th></tr>{_sc_rows}</table></div>
<h2>Not included</h2><ul>{''.join(f"<li><a href='{turl(n)}'>{e(n)}</a>: {e(r)}.</li>" for n, r in _tm0.SUB_NOT_STATED)}</ul>
{_faq(_qa_sc)}
<p class="small">Related: <a href="/my-ai-costs.html">My AI costs</a> · <a href="/stacks.html">Starter stacks</a> · <a href="/free-plan-limits.html">Free plan limits</a> · <a href="/help-me-choose.html">Help me choose</a></p>"""
page("/ai-subscription-costs.html", f"How Much Do AI Subscriptions Cost per Month? ({CHECKED[:4]}) ChatGPT, Claude, Cursor & More | ToolPick",
     f"Monthly prices of {len(_sc)} popular AI subscriptions from official pricing pages, cheapest first, plus what common AI tool stacks cost per month and per year.",
     _sc_body, _ld_list("AI subscription costs per month", "/ai-subscription-costs.html", [n for n, *_ in sorted(_sc.items(), key=lambda kv: kv[1][1])]) + [_ld_faq(_qa_sc), crumbs([("ToolPick", "/"), ("My AI costs", "/my-ai-costs.html"), ("AI subscription costs", "/ai-subscription-costs.html")])])
# internal links (one line each)
V44_CHANGED = ["/cursor-pricing.html", "/ai-subscription-costs.html"]
def _v44ins(path, marker, html, after=False):
    _fp = "public" + path; _h = open(_fp).read()
    if 'v44"' in _h or marker not in _h: return
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V44_CHANGED.append(path)
_v44ins(turl("Cursor"), '<section class="card tbp"', f'<p class="pick small v44">Free vs Plus vs Premium, plan by plan (checked {CURSOR_CHECKED}): <a href="/cursor-pricing.html">Cursor pricing explained →</a></p>')
for _p in ["/cursor-alternatives.html", "/compare/cursor-vs-claude-code.html", "/cheapest-ai-coding-assistant.html"]:
    _v44ins(_p, "</h1>", '<p class="small v44"><a href="/cursor-pricing.html">Cursor pricing explained, plan by plan →</a></p>', after=True)
V44_CHANGED.append("/my-ai-costs.html")
_v44ins("/help-me-choose.html", "</h1>", '<p class="small v44">Budgeting? <a href="/ai-subscription-costs.html">See what popular AI subscriptions cost per month →</a></p>', after=True)
_v44ins("/stacks.html", "</h1>", '<p class="small v44"><a href="/ai-subscription-costs.html">Monthly cost of popular AI subscriptions →</a></p>', after=True)
open("public/llms.txt", "a").write(f"\n## Pricing explainers\n- [Cursor pricing explained]({BASE}/cursor-pricing.html): Free, Plus (Grok only), Premium, Super, Ultra, Teams; usage vs Plus and what costs extra; checked {CURSOR_CHECKED}\n- [AI subscription costs per month]({BASE}/ai-subscription-costs.html): monthly prices of {len(_sc)} popular AI subscriptions with checked dates, plus example stack totals\n")

# --- v47: ChatGPT pricing + Is Claude Pro worth it ---
CGC = _tm0.CHATGPT_CHECKED
_cg_rows = "".join(f"<tr><th scope='row'>{e(p)}</th><td>{e(pr) if pr != 'not stated' else '<span class=small>not stated</span>'}</td><td>{dt}</td><td>{e(bf)}</td><td>{e(k)}</td></tr>" for p, pr, dt, bf, k in _tm0.CHATGPT_PLANS)
_cg_feat = "".join(f"<tr><th scope='row'>{e(r)}</th>" + "".join(f"<td>{e(v)}</td>" for v in vals) + "</tr>" for r, *vals in _tm0.CHATGPT_FEATURES)
_qa_cg = [("How much is ChatGPT Plus?", f"$20/month on monthly billing (official pricing page, checked in a browser {CGC})."),
          ("Is ChatGPT Go available in the US?", f"Go is listed on the official pricing page at $8/month (checked in a browser {CGC}); the page shows prices by country."),
          ("How much is ChatGPT Pro?", f"From $100/month, with a choice of 3 usage tiers (official pricing page, {CGC})."),
          ("Is ChatGPT free?", "Yes. The Free plan includes unlimited text chats with GPT-6, with limits on uploads, image creation, voice, deep research and memory.")]
_cg_body = f"""<p class="small"><a href="{turl('ChatGPT')}">ChatGPT</a> › Pricing</p><h1>ChatGPT pricing: Free vs Go vs Plus vs Pro</h1>
<p class="tag">Every ChatGPT plan from the official pricing page (fetched {CGC}). Each price shows the date we confirmed it; where the page didn't show a price, we say so.</p>
<p class="pick"><b>In short:</b> Free is $0 with unlimited text chats. Go ($8/mo) adds more messages, uploads and images and may include ads. Plus ($20/mo) adds advanced reasoning, more deep research and Codex. Pro starts at $100/mo, and Business is $25 per seat monthly ($20 billed annually).</p>
<h2>Plans and prices</h2><div class="tw"><table><caption class="small" style="text-align:left">Monthly prices, per user. “Price confirmed” is the date we last read that price on the official page.</caption><tr><th scope="col">Plan</th><th scope="col">Price</th><th scope="col">Price confirmed</th><th scope="col">Best for</th><th scope="col">What it includes</th></tr>{_cg_rows}</table></div>
<p class="small">How we checked: the official <a href="https://chatgpt.com/pricing" rel="noopener" target="_blank">chatgpt.com/pricing</a> page fills in dollar prices by country in your browser, so we read it in a US browser on {CGC}. Business is per seat, from 2 users; Enterprise is custom pricing.</p>
<h2>Key differences</h2><div class="tw"><table><caption class="small" style="text-align:left">From the plan comparison on the official page, {CGC}. *Usage must be reasonable and follow OpenAI's policies.</caption><tr><th scope="col">Feature</th><th scope="col">Free</th><th scope="col">Go</th><th scope="col">Plus</th><th scope="col">Pro</th></tr>{_cg_feat}</table></div>
{_faq(_qa_cg)}
<p class="small">Related: <a href="/compare/chatgpt-vs-claude.html">ChatGPT vs Claude</a> · <a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it?</a> · <a href="/ai-subscription-costs.html">AI subscription costs</a> · <a href="/free-plan-limits.html?cat=writing">Free plan limits</a></p>"""
page("/chatgpt-pricing.html", f"ChatGPT Pricing ({CGC[:4]}): Free vs Go vs Plus vs Pro Explained | ToolPick",
     f"ChatGPT plans compared from the official pricing page ({CGC}): Free $0, Go $8/mo, Plus $20/mo, Pro from $100/mo, with each price's confirmation date and the key feature differences.",
     _cg_body, [{"@context": "https://schema.org", "@type": "Product", "name": "ChatGPT", "url": BASE + "/chatgpt-pricing.html", "brand": {"@type": "Brand", "name": "OpenAI"},
                 "offers": [{"@type": "Offer", "name": "Free", "price": 0, "priceCurrency": "USD"}, {"@type": "Offer", "name": "Go", "price": 8, "priceCurrency": "USD"}, {"@type": "Offer", "name": "Plus", "price": 20, "priceCurrency": "USD"}, {"@type": "AggregateOffer", "name": "Pro", "lowPrice": 100, "priceCurrency": "USD"}]},
                _ld_faq(_qa_cg), crumbs([("ToolPick", "/"), ("ChatGPT", turl("ChatGPT")), ("ChatGPT pricing", "/chatgpt-pricing.html")])])
# Is Claude Pro worth it
CLC = _tm0.CLAUDE_CHECKED
_alt = [(n, pl, pr, find(n).get("checked", CHECKED)) for n, pl, pr in [("ChatGPT", "Plus", "$20/mo"), ("Google Gemini", "Google AI Pro", "$19.99/mo"), ("Le Chat (Mistral)", "Pro", "$14.99/mo")]]
for n, pl, pr, dt in _alt: assert pr.split("/")[0] in find(n)["price"], n
_alt_li = "".join(f"<li><a href='{turl(n)}'>{e(n)}</a> {e(pl)}: {e(pr)} (checked {dt})</li>" for n, pl, pr, dt in _alt)
_qa_cl = [("How much is Claude Pro?", f"$20/month billed monthly, or $17/month billed yearly ($200 up front), before tax (claude.com/pricing, {CLC})."),
          ("Does Claude Pro include Claude Code?", "Yes. Claude Code is included in all paid plans and shares the same usage limits as your chats."),
          ("How much more usage does Pro give than Free?", "Claude says Pro gives at least 5x more usage per 5-hour session than Free. There's no fixed message count."),
          ("When is Claude Max better?", "Max starts at $100/month and gives 5x or 20x the usage of Pro, plus priority access at busy times.")]
_cl_body = f"""<p class="small"><a href="{turl('Claude')}">Claude</a> › Is Claude Pro worth it?</p><h1>Is Claude Pro worth it?</h1>
<p class="tag">What $20 a month gets you over the free plan, from <a href="https://claude.com/pricing" rel="noopener" target="_blank">claude.com/pricing</a> (checked {CLC}), and when to choose something else.</p>
<p class="pick"><b>Short answer:</b> worth it if you hit Free's limits often, want Claude Code, Research or Opus, or need more than 5 projects. Skip it if Free covers your everyday questions. Pay yearly and it's $17/mo instead of $20.</p>
<h2>What Pro adds over Free</h2><div class="tw"><table><caption class="small" style="text-align:left">From the plan comparison on claude.com/pricing, {CLC}.</caption><tr><th scope="col">Feature</th><th scope="col">Free ($0)</th><th scope="col">Pro ($20/mo, or $17/mo yearly)</th></tr>
<tr><th scope="row">Usage</th><td>Everyday questions</td><td>At least 5x Free per 5-hour session</td></tr><tr><th scope="row">Claude Code</th><td>No</td><td>Yes</td></tr><tr><th scope="row">Research</th><td>No</td><td>Yes</td></tr><tr><th scope="row">Opus model</th><td>No</td><td>Yes</td></tr><tr><th scope="row">Projects</th><td>Up to 5</td><td>Yes</td></tr><tr><th scope="row">Claude in Chrome, Microsoft 365, Outlook</th><td>No</td><td>Yes</td></tr><tr><th scope="row">Claude Dashboards (beta)</th><td>No</td><td>Yes</td></tr></table></div>
<h2>Worth it if…</h2><ul><li>You run into Free's usage limits most weeks.</li><li>You code: Claude Code is included and shares your plan's usage.</li><li>You want Research, the Opus model, or more than 5 projects.</li></ul>
<h2>Skip it if…</h2><ul><li>Free covers what you do: chat, web search, files and code, memory, Artifacts and connectors are all in Free.</li><li>You'd use it all day: Max (from $100/mo) gives 5x or 20x Pro's usage.</li></ul>
<h2>Similar plans elsewhere (monthly billing)</h2><ul>{_alt_li}</ul>
{_faq(_qa_cl)}
<p class="small">Related: <a href="/chatgpt-pricing.html">ChatGPT pricing</a> · <a href="/compare/chatgpt-vs-claude.html">ChatGPT vs Claude</a> · <a href="/compare/cursor-vs-claude-code.html">Cursor vs Claude Code</a> · <a href="/ai-subscription-costs.html">AI subscription costs</a></p>"""
page("/is-claude-pro-worth-it.html", f"Is Claude Pro Worth It? ({CLC[:4]}) What $20/mo Adds Over Free | ToolPick",
     f"Claude Pro is $20/mo ($17 yearly). What it adds over Free (Claude Code, Research, Opus, 5x usage), when to skip it, and similar plans, from claude.com/pricing checked {CLC}.",
     _cl_body, [{"@context": "https://schema.org", "@type": "Product", "name": "Claude Pro", "url": BASE + "/is-claude-pro-worth-it.html", "brand": {"@type": "Brand", "name": "Anthropic"}, "offers": [{"@type": "Offer", "name": "Pro (monthly)", "price": 20, "priceCurrency": "USD"}, {"@type": "Offer", "name": "Pro (yearly, per month)", "price": 17, "priceCurrency": "USD"}]},
                _ld_faq(_qa_cl), crumbs([("ToolPick", "/"), ("Claude", turl("Claude")), ("Is Claude Pro worth it?", "/is-claude-pro-worth-it.html")])])
V47_CHANGED = ["/chatgpt-pricing.html", "/is-claude-pro-worth-it.html"]
def _v47ins(path, marker, html, after=False):
    _fp = "public" + path
    if not __import__("os").path.exists(_fp): return
    _h = open(_fp).read()
    if 'v47"' in _h or marker not in _h: return
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V47_CHANGED.append(path)
_v47ins(turl("ChatGPT"), '<section class="card tbp"', f'<p class="pick small v47">Free vs Go vs Plus vs Pro, side by side ({CGC}): <a href="/chatgpt-pricing.html">ChatGPT pricing →</a></p>')
_v47ins(turl("Claude"), '<section class="card tbp"', f'<p class="pick small v47">What $20/mo adds over Free ({CLC}): <a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it? →</a></p>')
_v47ins(turl("Claude Pro") if "Claude Pro" in tool_pages else "/tools/claude-pro.html", '<section class="card tbp"', f'<p class="pick small v47"><a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it? →</a></p>')
for _x in COMPARISONS:
    _ns = cnames(_x); _l = []
    if "ChatGPT" in _ns: _l.append('<a href="/chatgpt-pricing.html">ChatGPT pricing</a>')
    if "Claude" in _ns: _l.append('<a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it?</a>')
    if _l: _v47ins(f"/compare/{_x[0]}.html", "</h1>", '<p class="small v47">' + " · ".join(_l) + "</p>", after=True)
_v47ins("/ai-subscription-costs.html", "</h1>", '<p class="small v47"><a href="/chatgpt-pricing.html">ChatGPT pricing</a> · <a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it?</a></p>', after=True)
open("public/llms.txt", "a").write(f"\n## ChatGPT and Claude plans\n- [ChatGPT pricing]({BASE}/chatgpt-pricing.html): Free vs Go vs Plus vs Pro (and Business), each price with its confirmation date; feature differences from the official page ({CGC})\n- [Is Claude Pro worth it?]({BASE}/is-claude-pro-worth-it.html): what Pro adds over Free, when to skip it, similar plans; claude.com/pricing checked {CLC}\n")

# --- v48: Student & teacher discounts (verified 2026-10-24 on official pages) ---
SOC = _tm0.STUDENT_CHECKED; SO = _tm0.STUDENT_OFFERS
_socat = {}
for _c in CATEGORIES:
    for _t in _c["tools"]: _socat.setdefault(_t["name"], _c)
for _o in SO:
    assert _o["reg"] in find(_o["tool"])["price"], ("student reg price not in tools.py", _o["tool"], _o["reg"])
    assert _o["kind"] in ("free", "off", "ask") and set(_o["who"]) <= {"s", "t"}
_SO_ORDER = {"free": 0, "off": 1, "ask": 2}
SO_SORTED = sorted(SO, key=lambda o: (_SO_ORDER[o["kind"]], -(o["save"][1] if o.get("save") else 0), o["tool"]))
def _sousd(v): return "$" + (f"{v:,.2f}" if round(v, 2) != int(v) else f"{int(v):,}")
_WHO_L = {"s": "Students", "t": "Teachers", "st": "Students & teachers"}
_KIND_L = {"free": "b-sofree", "off": "b-sooff", "ask": "b-soask"}
def _so_card(o):
    c = _socat[o["tool"]]; d = dom(o["src"]); tt = find(o["tool"]); ck = tt.get("checked", CHECKED)
    sv = o.get("save")
    save_html = f'<dt>Year-one saving</dt><dd><b>{_sousd(sv[1])}</b> <span class="small">= {e(sv[0])}</span></dd>' if sv else ""
    note = f'<p class="small sonote">{e(o["note"])}</p>' if o.get("note") else ""
    src2 = f' · <a href="{e(o["src2"])}" rel="noopener" target="_blank">{e(dom(o["src2"]))}</a>' if o.get("src2") else ""
    remind = f'<a class="bbtn" href="/my-ai-costs.html?add={slug(o["tool"])}#reminders">Remind me before it ends</a>' if o.get("end") else ""
    return (f'<article class="card so" id="o-{o["k"]}" data-k="{o["k"]}" data-who="{o["who"]}" data-cat="{c["id"]}" data-kind="{o["kind"]}" data-save="{sv[1] if sv else 0}" data-end="{1 if o.get("end") else 0}">'
            f'<div class="badges"><span class="badge {_KIND_L[o["kind"]]}">{e(o["badge"])}</span><span class="badge b-rank">{_WHO_L[o["who"]]}</span></div>'
            f'<h3><a href="{turl(o["tool"])}">{e(o["tool"])}</a> <span class="small">· {e(c["name"])}</span></h3><p class="sooffer">{e(o["offer"])}</p>'
            f'<dl class="sodl"><dt>What you get</dt><dd>{e(o["gets"])}</dd><dt>Who qualifies</dt><dd>{e(o["elig"])}</dd><dt>How to claim</dt><dd class="soclaim">{e(o["claim"])}</dd>'
            f'<dt>Regular price</dt><dd>{e(o["reg"])} <span class="small">(checked {ck})</span></dd>{save_html}</dl>{note}'
            f'<details class="soq"><summary>What the official page says</summary><blockquote>“{e(o["quote"])}”</blockquote><p class="small">Read on <a href="{e(o["src"])}" rel="noopener" target="_blank">{e(d)}</a>{src2} on {SOC}</p></details>'
            f'<div class="factions"><a class="bbtn primary" href="{e(o["src"])}" rel="noopener" target="_blank">Get it on {e(d)}<span class="skip"> (opens in a new tab)</span></a>'
            f'<button type="button" class="bbtn sopick" aria-pressed="false" data-k="{o["k"]}">＋ I\'d use this</button>{remind}</div></article>')
_so_cats = [c for c in CATEGORIES if any(_socat[o["tool"]]["id"] == c["id"] for o in SO)]
_so_chips = '<button type="button" class="on" aria-pressed="true" data-cat="">All</button>' + "".join(f'<button type="button" aria-pressed="false" data-cat="{c["id"]}">{e(c["name"])}</button>' for c in _so_cats)
_so_n_s = sum(1 for o in SO if "s" in o["who"]); _so_n_t = sum(1 for o in SO if "t" in o["who"]); _so_free_s = sum(1 for o in SO if "s" in o["who"] and o["kind"] == "free")
_so_save_s = round(sum(o["save"][1] for o in SO if "s" in o["who"] and o.get("save")), 2)
_so_school = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)} <span class="small">(<a href="{e(s)}" rel="noopener" target="_blank">{e(dom(s))}</a>, {SOC})</span></li>' for n, w, s, q in _tm0.STUDENT_SCHOOL_ONLY)
_so_none = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)} <span class="small">(<a href="{e(s)}" rel="noopener" target="_blank">{e(dom(s))}</a>, {SOC})</span></li>' for n, w, s in _tm0.STUDENT_NONE)
_qa_so = [("Which AI tools are free for students?", "Free offers we verified on " + SOC + ": " + "; ".join(f'{o["tool"]} ({o["offer"]})' for o in SO_SORTED if o["kind"] == "free" and "s" in o["who"]) + ". Each has eligibility rules, listed on the page."),
          ("Is ChatGPT free for students?", "Not with a special plan: on " + SOC + " ChatGPT's pricing page listed no student plan or discount. Its regular Free plan is open to everyone."),
          ("Do teachers get AI tool discounts?", "Yes. Verified on " + SOC + ": " + "; ".join(f'{o["tool"]} ({o["offer"]})' for o in SO_SORTED if "t" in o["who"] and o["kind"] != "ask") + "."),
          ("What happens when a free student year ends?", "Most time-limited offers (for example Google AI Pro, Beautiful.ai Pro, v0, Lovable) end after the stated period. Use “Remind me before it ends” on any card to get a reminder before you'd start paying.")]
_so_cards = "".join(_so_card(o) for o in SO_SORTED)
_so_css = (".sohead{display:flex;flex-wrap:wrap;gap:var(--s3) var(--s5);align-items:center}.sohead>span{font-weight:600}.b-sofree{background:var(--ok);color:var(--okt)}.b-sooff{background:var(--ac);color:var(--sf)}.b-soask{background:var(--sf2);color:var(--tx);border:1px solid var(--bd)}"
           ".so .sooffer{font-size:1.08rem;font-weight:700;margin:2px 0 6px}.sodl{display:grid;grid-template-columns:1fr;gap:2px;margin:0 0 6px}.sodl dt{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--mu);margin-top:6px}.sodl dd{margin:0}"
           ".soq summary{cursor:pointer;min-height:44px;display:flex;align-items:center;color:var(--ac);font-weight:600;font-size:.92rem}.soq blockquote{margin:0 0 6px;padding:8px 12px;border-left:3px solid var(--bd);background:var(--sf2);border-radius:8px;font-size:.92rem}"
           ".so .factions{margin-top:auto;padding-top:8px}.sopick[aria-pressed=true]{background:var(--ok);border-color:var(--ok);color:var(--okt)}.so.picked{border:2px solid var(--ok)}.so.hl{outline:3px solid var(--ac);outline-offset:3px}.sonote{border-left:3px solid var(--warn);padding-left:8px}"
           "#so-sum{font-size:1.05rem;margin:var(--s3) 0 0}#so-tray b{font-size:1.05rem}#so-tray .grow{flex:1 1 220px}#so-list li{margin:var(--s3) 0}.sofree{display:inline-flex;align-items:center;gap:8px;min-height:44px;font-weight:500;cursor:pointer}.sofree input{width:20px;height:20px}"
           "#so-tray[hidden],#so-plan[hidden],#so-hint[hidden]{display:none!important}@media(max-width:640px){#so-tray{bottom:8px;gap:8px;padding:10px 12px}#so-tray #so-tot2{display:none}#so-tray .grow{flex:1 1 100%}#so-tray .bbtn{flex:1 1 0;justify-content:center;padding-left:8px;padding-right:8px;min-width:0}}")
_so_body = f"""<style>{_so_css}</style><p class="small"><a href="/guides.html">Guides</a> › Student &amp; teacher discounts</p><h1>AI student discounts &amp; free plans</h1>
<p class="tag">{_so_n_s} offers for students and {_so_n_t} for teachers, each read on the tool's own official page on {SOC}. Pick who you are, tap <b>I'd use this</b> on the ones you want, and get your year-one saving plus a claim checklist.</p>
<div class="builder"><div class="sohead"><span id="so-wl">I am a</span><fieldset class="seg" aria-labelledby="so-wl"><legend>I am a</legend><input type="radio" name="sowho" id="so-ws" value="s" checked><label for="so-ws">Student</label><input type="radio" name="sowho" id="so-wt" value="t"><label for="so-wt">Teacher / educator</label></fieldset>
<label class="sofree"><input type="checkbox" id="so-free"> Free offers only</label></div>
<div class="needs" role="group" aria-label="Filter by what you need" id="so-cats">{_so_chips}</div>
<p id="so-sum" role="status" aria-live="polite">{_so_n_s} offers for students · {_so_free_s} free · up to {_sousd(_so_save_s)} saved in year one where both prices are stated</p></div>
<h2 class="skip">Offers</h2><div class="grid" id="so-grid">{_so_cards}</div>
<p id="so-empty" class="fempty" hidden>No offers match. <button type="button" class="bbtn" id="so-reset">Show all offers</button></p>
<div class="tray" id="so-tray" hidden><span class="grow"><b id="so-tot"></b><br><span class="small" id="so-tot2"></span></span><a class="bbtn primary" href="#so-plan">Checklist ↓</a><button type="button" class="bbtn" id="so-share">Copy link</button><button type="button" class="bbtn" id="so-clear">Clear</button></div>
<section id="so-plan" hidden aria-labelledby="so-ph"><h2 id="so-ph">Your claim checklist</h2><p class="small">Do these in order: most offers need your school email first. Time-limited offers renew at the regular price, so set a reminder.</p><ol id="so-list"></ol><p><button type="button" class="bbtn" id="so-copy">Copy checklist</button> <span class="small" id="so-msg" role="status"></span></p></section>
<h2>Only through your school</h2><p class="small">These tools offer education pricing to institutions, not to individuals. Ask your school's IT or library.</p><ul>{_so_school}</ul>
<h2>No student discount (checked {SOC})</h2><ul>{_so_none}</ul>
<p class="small">How we check: every offer is copied from the tool's own pricing, education or help page on {SOC}; the exact sentence is under “What the official page says” on each card. Year-one savings are only shown when the page names the plan and both prices are known (regular prices from our tool pages, with their checked date). Offers change often — always confirm on the official page. We earn nothing from these links.</p>
<p class="small">Related: <a href="/best-ai-tools-for-students.html">AI starter stack for students</a> · <a href="/free-plan-limits.html">Free plan limits</a> · <a href="/free.html">Free AI tools</a> · <a href="/my-ai-costs.html#reminders">Renewal reminders</a></p>
<h2>FAQ</h2>{"".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in _qa_so)}
<script>(function(){{const G=[...document.querySelectorAll('#so-grid .so')],CH=[...document.querySelectorAll('#so-cats button')],FR=document.getElementById('so-free'),SUM=document.getElementById('so-sum'),EM=document.getElementById('so-empty'),TR=document.getElementById('so-tray'),PL=document.getElementById('so-plan'),LI=document.getElementById('so-list'),MSG=document.getElementById('so-msg');
let who='s',cat='',picks=new Set();const usd=v=>'$'+(Math.round(v*100)%100?v.toFixed(2):String(Math.round(v))).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,',');
const p=new URLSearchParams(location.search);if(p.get('who')=='t')who='t';if(p.get('cat')&&CH.some(b=>b.dataset.cat==p.get('cat')))cat=p.get('cat');if(p.get('free')=='1')FR.checked=true;(p.get('pick')||'').split(',').forEach(k=>{{if(G.some(c=>c.dataset.k==k))picks.add(k)}});
document.getElementById(who=='t'?'so-wt':'so-ws').checked=true;
function url(){{const q=new URLSearchParams();if(who=='t')q.set('who','t');if(cat)q.set('cat',cat);if(FR.checked)q.set('free','1');if(picks.size)q.set('pick',[...picks].join(','));const s=q.toString();return location.pathname+(s?'?'+s:'')}}
function render(){{let n=0,f=0,sv=0;G.forEach(c=>{{const ok=c.dataset.who.includes(who)&&(!cat||c.dataset.cat==cat)&&(!FR.checked||c.dataset.kind=='free');c.hidden=!ok;if(ok){{n++;if(c.dataset.kind=='free')f++;sv+=+c.dataset.save}}const on=picks.has(c.dataset.k);c.classList.toggle('picked',on);const b=c.querySelector('.sopick');b.setAttribute('aria-pressed',on);b.textContent=on?'✓ Added':'＋ I\\'d use this'}});
CH.forEach(b=>{{const on=b.dataset.cat==cat;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)}});
SUM.textContent=n+' offer'+(n==1?'':'s')+' for '+(who=='t'?'teachers':'students')+' · '+f+' free'+(sv>0?' · up to '+usd(sv)+' saved in year one where both prices are stated':'');EM.hidden=n>0;
const P=G.filter(c=>picks.has(c.dataset.k));TR.hidden=PL.hidden=!P.length;
if(P.length){{const t=P.reduce((a,c)=>a+ +c.dataset.save,0),ns=P.filter(c=>!+c.dataset.save).length;document.getElementById('so-tot').textContent=P.length+' offer'+(P.length==1?'':'s')+' picked · '+(t>0?usd(t)+' saved in year one':'saving not stated');document.getElementById('so-tot2').textContent=ns?(ns+' pick'+(ns==1?' has':'s have')+' no stated $ saving (percent off or plan not named).'):'Savings use the regular prices on our tool pages.';
LI.innerHTML=P.map(c=>{{const a=c.querySelector('.factions a.primary'),r=c.querySelector('.factions a[href*="reminders"]');return '<li><b>'+c.querySelector('h3 a').textContent+'</b>: '+c.querySelector('.sooffer').textContent+'<br>'+c.querySelector('.soclaim').textContent+' <a href="'+a.href+'" rel="noopener" target="_blank">Official page</a>'+(r?' · <a href="'+r.getAttribute('href')+'">Remind me before it ends</a>':'')+'</li>'}}).join('')}}
history.replaceState(null,'',url())}}
document.querySelectorAll('input[name=sowho]').forEach(r=>r.addEventListener('change',()=>{{who=r.value;render()}}));FR.addEventListener('change',render);
CH.forEach(b=>b.addEventListener('click',()=>{{cat=b.dataset.cat;render()}}));document.getElementById('so-reset').addEventListener('click',()=>{{cat='';FR.checked=false;render()}});
G.forEach(c=>c.querySelector('.sopick').addEventListener('click',()=>{{const k=c.dataset.k;picks.has(k)?picks.delete(k):picks.add(k);render()}}));
document.getElementById('so-clear').addEventListener('click',()=>{{picks.clear();render()}});
function cp(t,okmsg){{const done=()=>{{MSG.textContent=okmsg;document.getElementById('so-tot2').textContent=okmsg}};if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,()=>prompt('Copy this:',t));else prompt('Copy this:',t)}}
document.getElementById('so-share').addEventListener('click',()=>cp(location.origin+url(),'Link copied: it opens with your picks.'));
document.getElementById('so-copy').addEventListener('click',()=>cp([...LI.querySelectorAll('li')].map((l,i)=>(i+1)+'. '+l.innerText.replace(/\\s*Official page.*$/s,'')+' — '+l.querySelector('a').href).join('\\n'),'Checklist copied.'));
render();const tk=p.get('tool');if(tk){{const c=G.find(x=>x.dataset.k==tk)||G.find(x=>x.dataset.k.startsWith(tk));if(c){{if(!c.dataset.who.includes(who)){{who=c.dataset.who.includes('s')?'s':'t';document.getElementById(who=='t'?'so-wt':'so-ws').checked=true;cat='';render()}}c.classList.add('hl');c.scrollIntoView({{block:'center'}})}}}}}})();</script>"""
page("/ai-student-discounts.html", f"AI Student Discounts ({SOC[:4]}): Free & Discounted AI Tools for Students and Teachers | ToolPick",
     f"{_so_n_s} verified AI student offers ({_so_free_s} free) and {_so_n_t} for teachers: Gemini, GitHub Copilot, Notion, Perplexity, Microsoft 365 and more. Eligibility, how to claim and year-one savings, checked {SOC} on official pages.",
     _so_body, [{"@context": "https://schema.org", "@type": "ItemList", "name": "AI student discounts", "url": BASE + "/ai-student-discounts.html", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{o["tool"]}: {o["offer"]}', "url": BASE + "/ai-student-discounts.html#o-" + o["k"]} for i, o in enumerate(SO_SORTED)]},
                _ld_faq(_qa_so), crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("AI student discounts", "/ai-student-discounts.html")])])
V48_CHANGED = ["/ai-student-discounts.html"]
def _v48ins(path, marker, html, after=False):
    _fp = "public" + path
    if not __import__("os").path.exists(_fp): return False
    _h = open(_fp).read()
    if 'v48"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V48_CHANGED.append(path); return True
_so_by = {}
for _o in SO_SORTED: _so_by.setdefault(_o["tool"], []).append(_o)
for _n, _os_ in _so_by.items():
    _txt = " · ".join(f'{e(o["offer"])} ({_WHO_L[o["who"]].lower()})' for o in _os_)
    _line = f'<p class="pick small v48"><b>Student &amp; teacher offer:</b> {_txt} — checked {SOC} · <a href="/ai-student-discounts.html?tool={_os_[0]["k"]}">All AI student discounts →</a></p>'
    if not _v48ins(turl(_n), '<section class="card tbp"', _line): _v48ins(turl(_n), '<section class="verdict', _line)
_SO_LINE = f'<p class="pick v48"><b>Student or teacher?</b> {_so_n_s} AI tools have verified student offers ({_so_free_s} free), checked {SOC}: <a href="/ai-student-discounts.html">AI student discounts →</a></p>'
_v48ins("/best-ai-tools-for-students.html", "</h1>", _SO_LINE, after=True)
_v48ins("/free.html", "</h1>", _SO_LINE, after=True)
_v48ins("/tools.html", "</h1>", f'<p class="small v48">Student or teacher? <a href="/ai-student-discounts.html">See verified AI student discounts →</a></p>', after=True)
_v48ins("/guides.html", "<h2>New guides</h2><ul>", "<li class=\"v48\"><a href='/ai-student-discounts.html'>AI student &amp; teacher discounts</a></li>", after=True)
_v48ins("/stacks.html", "</h1>", f'<p class="small v48">Student or teacher? <a href="/ai-student-discounts.html">Verified AI student discounts →</a></p>', after=True)
# Finder: when the search mentions students/teachers, show a one-tap link (doesn't change results)
_SOH = f'<p class="pick v48 sohint" hidden><b>Student or teacher?</b> {_so_n_s} AI tools have verified student offers ({_so_free_s} free): <a href="/ai-student-discounts.html">AI student discounts →</a></p>'
_v48ins("/index.html", '<div class="chips" aria-label="Example searches">', _SOH + '<style>.sohint[hidden]{display:none!important}.sohint{margin:var(--s3) auto;max-width:720px;text-align:left}</style>')
_h = open("public/index.html").read(); open("public/index.html", "w").write(_h.replace('<div id="out" aria-live="polite">', _SOH + '<div id="out" aria-live="polite">' + '<script>(function(){const q=document.getElementById("q"),H=[...document.querySelectorAll(".sohint")];if(!q||!H.length)return;const re=/\\b(student|students|college|university|teacher|teachers|educator|school|edu|study|studying|homework|class)\\b/i;const f=()=>{const m=re.test(q.value);H.forEach(h=>h.hidden=!m)};q.addEventListener("input",f);addEventListener("load",f);document.addEventListener("click",()=>setTimeout(f,50));f()})()</script>', 1))
open("public/llms.txt", "a").write(f"\n## AI student discounts (v48)\n- [AI student & teacher discounts]({BASE}/ai-student-discounts.html): {_so_n_s} student offers ({_so_free_s} free) and {_so_n_t} teacher offers, each with eligibility, how to claim, regular price and year-one saving where both prices are stated; read on official pages {SOC}. Also lists school-only plans (Claude, Grammarly, Canva Campus, Scite) and tools with no student discount (ChatGPT, Cursor, Warp). Filters: ?who=t, ?cat=coding, ?free=1, ?tool=lovable.\n")

# --- v49: "Alternatives to X" pages (/alternatives/<tool>.html + hub /alternatives.html) ---
# Built ONLY from verified tools.py data and the site's one same-job rule (samejob / cmp_price / cheaper_alt / free_alt,
# TIER_MATCH for lighter entry tiers). No new prices. Unverified values show "check site". Cursor keeps its own
# hand-checked page (/cursor-alternatives.html) and free-only pages (/free-alternative-to-*.html) are linked, not duplicated.
ALT49_DATE = "2026-10-25"
ALT49 = ["ChatGPT", "Claude", "Google Gemini", "Microsoft Copilot", "Midjourney", "ElevenLabs", "Runway", "Grammarly",
         "Otter", "GitHub Copilot", "Lovable", "Bolt", "Gamma", "Surfer", "Lindy"]
for _n in ALT49: assert _n in TOOL and len(samejob(_n)) >= 2, _n
def alt49_path(n): return "/cursor-alternatives.html" if n == "Cursor" else f"/alternatives/{slug(n)}.html"
ALT49_PATHS = {n: alt49_path(n) for n in ALT49 + ["Cursor"]}
_FA_PATH = dict(FREE_ALT_URLS)
_CAT49 = {}
for _c in CATEGORIES:
    for _t in _c["tools"]: _CAT49.setdefault(_t["name"], _c)
def _p49(v, unit="/mo"):
    if isinstance(v, (int, float)): return _usd(v) + unit
    if isinstance(v, str) and v.strip() and v != "check site": return e(v) + unit
    return '<span class="check">check site</span>'
def _cmpkey49(x, n):
    m, a = cmp_price(x, n, "monthly"), cmp_price(x, n, "annual")
    return (0 if m is not None else 1, m if m is not None else (a if a is not None else 1e9), x["name"].lower())
def _cheaper49(n):
    """Same rule as tool pages (tool_verdict): monthly with monthly first, then billed-yearly with billed-yearly."""
    t = TOOL[n]; m, a = _num(t["monthly"]), _num(t["annual"])
    cm, ca = cheaper_alt(n, "monthly"), cheaper_alt(n, "annual")
    if m is not None and cm is not None and cm["monthly"] < m: return cm, "monthly", cm["monthly"], m
    if a is not None and ca is not None and ca["annual"] < a: return ca, "annual", ca["annual"], a
    return None
def _bv49(n):
    return [x for x in [TOOL[n]] + samejob(n) if x["name"] in BEST_OF]
def _alt49_lines(n):
    t = TOOL[n]; job = cap_label(n); L = []
    ch = _cheaper49(n)
    if ch:
        x, key, v, own = ch; bl = "monthly billing" if key == "monthly" else "billed yearly"
        tn = tier_note(n, x["name"])
        L.append(("Cheaper", f'<a href="{turl(x["name"])}">{e(tname(x))}</a> at {_usd(v)}/mo vs {e(n)} at {_usd(own)}/mo ({bl}, same job).' + (f' <span class="small">{e(tn)}</span>' if tn else "")))
    else:
        m, a = _num(t["monthly"]), _num(t["annual"])
        if m is None and a is None: L.append(("Cheaper", f"We have no checked price for {e(n)}, so we can't say what is cheaper."))
        else: L.append(("Cheaper", f"None checked: {e(n)} already has the lowest checked entry price for {e(job)} among comparable plans."))
    fa = free_alt(n)
    if fa: L.append(("Free", f'<a href="{turl(fa["name"])}">{e(fa["name"])}</a> has a real free plan: {e(fa["free"])}.' + (f' {e(n)} has one too: {e(t["free"])}.' if realfree(t) else "")))
    elif realfree(t): L.append(("Free", f"No other same-job tool has a real free plan, but {e(n)} itself does: {e(t['free'])}."))
    else: L.append(("Free", f"No same-job tool in our list has a real free plan (trials and one-time credits don't count)."))
    bv = sorted([x for x in _bv49(n) if x["name"] != n], key=lambda x: 0 if _CAT49[n]["id"] in BEST_OF[x["name"]] else 1)
    if bv:
        x = bv[0]; c = next(cc for cc in CATEGORIES if cc["id"] == BEST_OF[x["name"]][0])
        L.append(("Best value", f'<a href="{turl(x["name"])}">{e(x["name"])}</a> is our Best Value pick for {e(c["name"])}' + (f": {e(x['why'].rstrip('.'))}." if x.get("why") else " (chosen for overall value, not only price).")))
    elif n in BEST_OF:
        c = next(cc for cc in CATEGORIES if cc["id"] == BEST_OF[n][0])
        L.append(("Best value", f"{e(n)} itself is our Best Value pick for {e(c['name'])}, so switch only for price or a specific feature."))
    return L
def _row49(x, n, is_target):
    m, a = _num(x["monthly"]), _num(x["annual"]); ck = x.get("checked", CHECKED)
    mon = _p49(x["monthly"]) if x["monthly"] is not None else '<span class="check">check site</span>'
    tier = ""
    _cmv = cmp_price(x, n, "monthly")
    if not is_target and _cmv is not None and _cmv != m: tier = f'<br><span class="small">Compared at {e(TIER_MATCH[x["name"]][0])}: {_usd(_cmv)}/mo</span>'
    yr = _p49(x["annual"]) if x["annual"] is not None else '<span class="check">check site</span>'
    fr = f'<b>Yes</b><br><span class="small">{e(x["free"])}</span>' if realfree(x) else f'No<br><span class="small">{e(x["free"])}</span>'
    bd = ('<span class="badge b-rank">THIS TOOL</span>' if is_target else "") + ('<span class="badge b-best">BEST VALUE</span>' if x["name"] in BEST_OF else "") + ('<span class="badge b-free">FREE PLAN</span>' if realfree(x) else "")
    return (f'<tr{" class=a49t" if is_target else ""}><th scope="row" data-l="Tool"><a href="{turl(x["name"])}">{e(x["name"])}</a><span class="a49b">{bd}</span><span class="small a49d">{e(x["about"])}</span></th>'
            f'<td data-l="Monthly">{mon}{tier}</td><td data-l="Billed yearly">{yr}</td><td data-l="Real free plan">{fr}</td><td data-l="Main limit">{e(limitation(x))}</td>'
            f'<td data-l="Checked">{ck}<br><a href="{e(x["pricing"])}" rel="noopener" target="_blank">Official pricing<span class="skip"> for {e(x["name"])} (opens in a new tab)</span></a></td></tr>')
ALT49_CSS = ("<style>.a49v{display:grid;gap:8px;margin:var(--s4) 0}.a49v div{background:var(--sf);border:1px solid var(--bd);border-left:4px solid var(--ok);border-radius:12px;padding:10px 14px}.a49v b{display:inline-block;min-width:92px}"
             ".a49 table{min-width:860px}.a49 th[scope=row]{font-weight:600;min-width:180px;white-space:normal}.a49 th[scope=row]>a{min-height:32px}.a49b{display:flex;flex-wrap:wrap;gap:4px;margin:2px 0}.a49b:empty{display:none}.a49d{display:block;font-weight:400}.a49 td{font-size:.92rem}.a49 tr.a49t{background:var(--sf2)}.a49 tr.a49t th[scope=row]{box-shadow:inset 4px 0 0 var(--ac)}.a49 td[data-l=Checked]{white-space:nowrap}.a49c{display:flex;flex-wrap:wrap;gap:0 16px;list-style:none;padding:0}.a49c li{margin:0}"
             ".a49h{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:var(--s4);margin:var(--s4) 0}.a49h .card h3 a{min-height:32px}.a49h .card p{font-size:.92rem}"
             "@media(max-width:640px){.a49 table{min-width:0}.a49 tr:first-child{display:none}.a49 table,.a49 tbody,.a49 tr,.a49 td,.a49 th[scope=row]{display:block;width:100%}.a49 tr{border-bottom:1px solid var(--bd);padding:10px 4px}.a49 td,.a49 th[scope=row]{border:0;padding:4px 12px}"
             ".a49 caption{display:block;width:100%}.a49 tr{margin:0 0 4px}.a49 td::before{content:attr(data-l);display:block;font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--mu)}.a49v b{display:block}}</style>")
ALT49_CHANGED = []
_alt49_summ = {}
for _n in ALT49:
    _t = TOOL[_n]; _p = ALT49_PATHS[_n]; _job = cap_label(_n); _cat = _CAT49[_n]
    _alts = sorted(samejob(_n), key=lambda x: _cmpkey49(x, _n))
    _rows = _row49(_t, _n, True) + "".join(_row49(x, _n, False) for x in _alts)
    _lines = _alt49_lines(_n)
    _ver = "".join(f"<div><b>{k}:</b> {v}</div>" for k, v in _lines)
    _cmps = [x for x in COMPARISONS if _n in cnames(x)]
    _cl = "".join(f'<li><a href="/compare/{x[0]}.html">{e(x[1])}</a></li>' for x in _cmps)
    _cb = "/compare-builder.html?tools=" + ",".join(slug(x) for x in [_n] + [a["name"] for a in _alts[:2]])
    _ch = _cheaper49(_n); _fa = free_alt(_n)
    _rel = [f'<a href="{turl(_n)}">{e(_n)} prices &amp; review</a>']
    if _n in _FA_PATH: _rel.append(f'<a href="{_FA_PATH[_n]}">Free alternatives to {e(_n)} only</a>')
    if _n == "ChatGPT": _rel.append('<a href="/chatgpt-pricing.html">ChatGPT pricing</a>')
    if _n == "Claude": _rel.append('<a href="/is-claude-pro-worth-it.html">Is Claude Pro worth it?</a>')
    if cap1(_n) == "code-assistant": _rel.append('<a href="/cursor-alternatives.html">Cursor alternatives</a>')
    _rel.append(f'<a href="/best-ai-{_cat["id"]}-tools.html">Best AI {e(_cat["name"].lower())} tools</a>')
    _rel.append('<a href="/alternatives.html">All alternatives pages</a>')
    _qa = [(f"What is the cheapest alternative to {_n}?",
            (f"{tname(_ch[0])} at {_usd(_ch[2])}/mo vs {_n} at {_usd(_ch[3])}/mo ({'monthly billing' if _ch[1]=='monthly' else 'billed yearly'}), among tools that do the same main job ({_job}). Prices checked on official pricing pages.") if _ch
            else f"None of the tools we track that do the same main job ({_job}) has a lower checked entry price than {_n}."),
           (f"Is there a free alternative to {_n}?",
            (f"Yes: {_fa['name']} has a real free plan ({_fa['free']}), checked {_fa.get('checked', CHECKED)}.") if _fa else f"No tool in our list that does the same main job as {_n} has a real free plan."),
           (f"How much does {_n} cost?", f"{_t['price']} (official pricing page, checked {_t.get('checked', CHECKED)})."),
           (f"Which tools do the same job as {_n}?", f"{', '.join(a['name'] for a in _alts)} all have the same main job ({_job}) in ToolPick's list.")]
    _body = f"""{ALT49_CSS}<p class="small"><a href="/alternatives.html">Alternatives</a> › {e(_n)}</p><h1>{e(_n)} alternatives</h1>
<p class="tag">{len(_alts)} tools that do the same main job as {e(_n)} ({e(_job)}), with prices copied from each official pricing page and the date we checked.</p>
<h2 class="h3" style="margin:var(--s5) 0 var(--s2)">Which one fits you</h2><div class="a49v">{_ver}</div>
<h2>Side by side</h2><div class="tw a49"><table><caption class="small" style="text-align:left;padding:12px 16px">Entry plan per month. “Billed yearly” is the monthly rate when you pay for a year. Real free plan = a free plan you can keep using (trials and one-time credits don't count). “check site” = not verified, so we don't guess.</caption>
<tr><th scope="col">Tool</th><th scope="col">Monthly</th><th scope="col">Billed yearly</th><th scope="col">Real free plan</th><th scope="col">Main limit</th><th scope="col">Checked</th></tr>{_rows}</table></div>
<p><a class="btn" href="{_cb}">Compare {e(_n)} with the top 2 side by side →</a></p>
{f'<h2>Head-to-head comparisons</h2><ul class="a49c">{_cl}</ul>' if _cl else ''}
<p class="small">How we pick alternatives: only tools whose main job is the same as {e(_n)}{'’' if _n.endswith('s') else '’s'} ({e(_job)}), sorted by checked monthly price. Cheaper is compared like for like: monthly with monthly, yearly with yearly, and lighter entry tiers at their comparable tier. Not hands-on tested. <a href="/how-we-pick.html">How we pick</a></p>
{_faq(_qa)}
<p class="small">Related: {' · '.join(_rel)}</p>"""
    _yr = ALT49_DATE[:4]
    _names = ", ".join(a["name"] for a in _alts[:4])
    _desc = (f"{len(_alts)} {_n} alternatives that do the same job ({_job}): {_names}. "
             + (f"Cheaper: {tname(_ch[0])} {_usd(_ch[2])}/mo. " if _ch else "") + (f"Free: {_fa['name']}. " if _fa else "")
             + "Monthly and yearly prices, free plans and limits from official pages.")[:300]
    page(_p, f"{_n} Alternatives ({_yr}): {len(_alts)} Same-Job Tools Compared on Price | ToolPick", _desc, _body,
         _ld_list(f"{_n} alternatives", _p, [a["name"] for a in _alts]) + [_ld_faq(_qa), crumbs([("ToolPick", "/"), ("Alternatives", "/alternatives.html"), (f"{_n} alternatives", _p)])])
    ALT49_CHANGED.append(_p)
    _lm_v = max(x.get("checked", CHECKED) for x in [_t] + _alts)
    _alt49_summ[_n] = dict(p=_p, n=len(_alts), ch=_ch, fa=_fa, job=_job, cat=_cat, lm=_lm_v, alts=[a["name"] for a in _alts])
# Hub
_hub_groups = {}
for _n in ALT49 + ["Cursor"]: _hub_groups.setdefault(_CAT49[_n]["id"], []).append(_n)
def _hub_card(n):
    if n == "Cursor":
        _al = samejob("Cursor")
        return (f'<article class="card"><h3><a href="/cursor-alternatives.html">Cursor alternatives</a></h3><p class="small">{len(_al)} same-job tools · {e(cap_label("Cursor"))}</p>'
                f'<p>Plan-by-plan coding prices, checked {CODING_CHECKED}.</p></article>')
    s = _alt49_summ[n]; ch, fa = s["ch"], s["fa"]
    return (f'<article class="card"><h3><a href="{s["p"]}">{e(n)} alternatives</a></h3><p class="small">{s["n"]} same-job tools · {e(s["job"])}</p>'
            f'<p><b>Cheaper:</b> {(e(tname(ch[0])) + " " + _usd(ch[2]) + "/mo" + (" yearly" if ch[1] == "annual" else "")) if ch else "none checked"}</p>'
            f'<p><b>Free:</b> {e(fa["name"]) if fa else ("only " + e(n) + " itself" if realfree(TOOL[n]) else "none")}</p></article>')
_hub_order = ALT49[:ALT49.index("GitHub Copilot") + 1] + ["Cursor"] + ALT49[ALT49.index("GitHub Copilot") + 1:]
_hub_html = f'<h2 class="skip">Alternatives pages</h2><div class="a49h">{"".join(_hub_card(n) for n in _hub_order)}</div>'
_qa_hub = [("How does ToolPick choose alternatives?", "Only tools with the same main job count as alternatives, so a chatbot is never compared with an image tool. Prices are copied from each tool's official pricing page with the date we checked."),
           ("What does 'cheaper' mean here?", "A lower checked entry price on the same billing: monthly with monthly, yearly with yearly. Lighter entry tiers (like ChatGPT Go or Google AI Plus) are compared at their comparable tier against full plans."),
           ("Only want free tools?", "Each page shows which alternatives have a real free plan. For free-only lists, see the free alternatives pages in Guides.")]
_hub_body = f"""{ALT49_CSS}<p class="small"><a href="/guides.html">Guides</a> › Alternatives</p><h1>Alternatives to popular AI tools</h1>
<p class="tag">Pick the tool you use now. Each page lists tools that do the same job, with checked monthly and yearly prices, free plans and the main limit, and tells you which is cheaper, which is free and which is our best-value pick.</p>
{_hub_html}
<p class="small">Free only? <a href="/free.html">Can I do it for free?</a> · Free-only lists: {" · ".join(f'<a href="{p}">{e(n)}</a>' for n, p in FREE_ALT_URLS if n in ALT49)} · <a href="/guides.html">all guides</a></p>
{_faq(_qa_hub)}"""
page("/alternatives.html", f"Alternatives to ChatGPT, Midjourney, ElevenLabs & More ({ALT49_DATE[:4]}) | ToolPick",
     f"Same-job alternatives to {len(ALT49) + 1} popular AI tools (ChatGPT, Claude, Midjourney, ElevenLabs, Runway, Grammarly, Cursor...) with checked prices, free plans and the cheaper and free option for each.",
     _hub_body, [{"@context": "https://schema.org", "@type": "ItemList", "name": "Alternatives to popular AI tools", "url": BASE + "/alternatives.html",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{n} alternatives", "url": BASE + ALT49_PATHS[n]} for i, n in enumerate(_hub_order)]},
                 _ld_faq(_qa_hub), crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("Alternatives", "/alternatives.html")])])
ALT49_CHANGED.append("/alternatives.html")
V49_CHANGED = []
def _v49ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if 'v49"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V49_CHANGED.append(path); return True
for _n in ALT49 + ["Cursor"]:
    _k = len(samejob(_n))
    _line = f'<p class="pick small v49">Looking for something else? <a href="{ALT49_PATHS[_n]}">See {_k} {e(_n)} alternatives that do the same job →</a></p>'
    if not _v49ins(turl(_n), '<section class="card tbp"', _line): _v49ins(turl(_n), '<section class="verdict', _line)
for _x in COMPARISONS:
    _ls = [f'<a href="{ALT49_PATHS[_nn]}">{e(_nn)} alternatives</a>' for _nn in cnames(_x) if _nn in ALT49_PATHS]
    if _ls: _v49ins(f"/compare/{_x[0]}.html", "</h1>", '<p class="small v49">See alternatives: ' + " · ".join(_ls) + "</p>", after=True)
for _n, _fp2 in FREE_ALT_URLS:
    if _n in ALT49_PATHS: _v49ins(_fp2, "</h1>", f'<p class="small v49">Paid options too? <a href="{ALT49_PATHS[_n]}">All {e(_n)} alternatives with prices →</a></p>', after=True)
_v49ins("/cursor-alternatives.html", "</h1>", '<p class="small v49">Other tools: <a href="/alternatives.html">alternatives to ChatGPT, Claude, Midjourney and more →</a></p>', after=True)
_v49ins("/guides.html", "<h2>New guides</h2><ul>", "<li class=\"v49\"><a href='/alternatives.html'>Alternatives to popular AI tools</a></li>", after=True)
_v49ins("/tools.html", "</h1>", '<p class="small v49">Replacing a tool you use? <a href="/alternatives.html">See same-job alternatives →</a></p>', after=True)
# Finder: the "itself" line under any tool result links that tool's alternatives page (when we have one).
_ih = open("public/index.html").read()
_sl_old = 'const selfLine=`<p class="small" style="margin-top:12px"><b><a href="${x.u}">${X(x.n)}</a> itself:</b> ${ptxt(x)}${x.fr?\' · real free plan\':\'\'} · checked ${x.k} · <a href="${X(x.pr)}" rel="noopener" target="_blank">official pricing</a></p>`;'
assert _ih.count(_sl_old) == 2, ("selfLine pattern", _ih.count(_sl_old))
_sl_new = _sl_old.replace('official pricing</a></p>`;', 'official pricing</a>${AP49[x.sl]?` · <a href="${AP49[x.sl]}">All ${X(x.n)} alternatives →</a>`:\'\'}</p>`;')
_ih = _ih.replace(_sl_old, _sl_new).replace("<script>", "<script>const AP49=" + json.dumps({slug(n): p for n, p in ALT49_PATHS.items()}) + ";", 1)
open("public/index.html", "w").write(_ih); V49_CHANGED.append("/")
open("public/llms.txt", "a").write(f"\n## Alternatives pages (v49)\n- [Alternatives to popular AI tools]({BASE}/alternatives.html): hub\n" + "".join(f"- [{n} alternatives]({BASE}{ALT49_PATHS[n]}): {_alt49_summ[n]['n']} same-job tools ({_alt49_summ[n]['job']}): {', '.join(_alt49_summ[n]['alts'])}; which is cheaper (like-for-like billing and tier), which has a real free plan, Best Value pick; monthly/yearly prices, main limit, checked dates\n" for n in ALT49))

# --- v50: AI team plan costs (/ai-team-plans.html) ---
# Team/business tiers read on official pricing pages on TEAM_CHECKED (tools.py TEAM_PLANS, exact page text in q).
# One input (team size) + billing switch: per-seat price x seats, seat minimums/maximums, flat workspace prices and
# platform fees applied exactly as the page states. Lowest team price is only marked inside one job group, on the same
# billing, among plans that allow that team size; add-ons that need another paid plan are never ranked.
TEAM_CHECKED = _tm0.TEAM_CHECKED; TEAM_GROUPS = _tm0.TEAM_GROUPS; TEAM_PLANS = _tm0.TEAM_PLANS; TEAM_LEFT_OUT = _tm0.TEAM_LEFT_OUT
TEAM_PATH = "/ai-team-plans.html"
_TG = dict(TEAM_GROUPS)
def _tnum(v): return ("%g" % v) if float(v).is_integer() else ("%.2f" % v)
for _p in TEAM_PLANS:
    assert _p["t"] in TOOL and _p["g"] in _TG, _p["t"]
    assert _p.get("m") is not None or _p.get("y") is not None, _p["t"]
    _qq = " ".join(_p["q"])
    for _k in ("m", "base", "mn", "mx"):
        if _p.get(_k) is not None: assert _tnum(_p[_k]).replace(".", " .") in _qq or _tnum(_p[_k]) in _qq, (_p["t"], _k, _p[_k])
    if _p.get("y") is not None and not _p.get("yr"): assert _tnum(_p["y"]) in _qq.replace(" .", "."), (_p["t"], "y")
    if _p.get("yr"): assert _tnum(_p["yr"]) in _qq, (_p["t"], "yr")
def _tcost(p, seats, bill):
    """Monthly team cost for `seats` on `bill` ('m' or 'y'); returns (monthly, billed_seats, why_not)."""
    per = p.get("y") if bill == "y" else p.get("m")
    if per is None: return None, None, ("Yearly price not stated. Switch to Monthly to see it." if bill == "y" else "Monthly price not stated. Switch to Billed yearly to see it.")
    if p.get("mx") and seats > p["mx"]: return None, None, f"This plan allows up to {p['mx']} seats."
    billed = max(seats, p.get("mn") or 1)
    tot = per if p.get("flat") else (p.get("base") or 0) + per * billed
    return tot, billed, None
def _tlowest(rows, seats, bill):
    c = [(r, _tcost(r, seats, bill)[0]) for r in rows if not r.get("addon")]
    c = [(r, v) for r, v in c if v is not None]
    if len(c) < 2: return set()
    lo = min(v for r, v in c); return {r["t"] for r, v in c if abs(v - lo) < 0.005}
def _tm(v): return _usd(v)
def _tper(p):
    a = []
    if p.get("flat"): a.append(f'{"from " if p.get("frm") else ""}{_tm(p["m"])}/mo for the whole workspace')
    else:
        if p.get("m") is not None: a.append(f'{"from " if p.get("frm") else ""}{_tm(p["m"])}/seat monthly')
        if p.get("yr"): a.append(f'{_tm(p["yr"])}/seat per year')
        elif p.get("y") is not None: a.append(f'{_tm(p["y"])}/seat billed yearly')
    s = " · ".join(a)
    return (f'{_tm(p["base"])}/mo plan fee + ' + s) if p.get("base") else s
def _trules(p):
    r = []
    if p.get("mn"): r.append(f'Min {p["mn"]} seats')
    if p.get("mx"): r.append(f'Max {p["mx"]} seats')
    if p.get("flat"): r.append("Unlimited users")
    if p.get("addon"): r.append("Add-on")
    return r
def _trow(p, seats, bill, low):
    s = slug(p["t"]); v, billed, why = _tcost(p, seats, bill)
    if v is None: tot, yr = f'<span class="check">{e(why)}</span>', "–"
    else:
        tot = f'<b>{_tm(v)}</b>/mo' + (f'<br><span class="small">billed for {billed} seats (minimum)</span>' if billed != seats and not p.get("flat") else "")
        yr = _tm(v * 12) + ("/yr" if bill == "y" else "/yr if you stay 12 months")
    bd = ('<span class="badge b-best">LOWEST FOR YOUR TEAM</span>' if p["t"] in low else "") + "".join(f'<span class="badge b-rank">{e(x)}</span>' for x in _trules(p))
    nt = e(p.get("note") or "")
    return (f'<tr id="t-{s}" data-k="{s}"{' class="lo"' if p["t"] in low else ""}><th scope="row" data-l="Plan"><a href="{turl(p["t"])}">{e(p["t"])}</a> <span class="t50p">{e(p["plan"])}</span><span class="t50b">{bd}</span></th>'
            f'<td data-l="Price">{_tper(p)}</td><td data-l="Your team" class="t50tot">{tot}</td><td data-l="Per year" class="t50yr">{yr}</td>'
            f'<td data-l="Good to know" class="small">{nt}</td><td data-l="Checked" class="small">{TEAM_CHECKED}<br><a href="{e(p["src"])}" rel="noopener" target="_blank">Official pricing<span class="skip"> for {e(p["t"])} (opens in a new tab)</span></a></td></tr>')
_T_DEF_SEATS, _T_DEF_BILL = 5, "m"
def _tgroup(g, seats, bill):
    rows = [p for p in TEAM_PLANS if p["g"] == g]
    low = _tlowest(rows, seats, bill)
    rows = sorted(rows, key=lambda p: (1 if p.get("addon") else 0, _tcost(p, seats, bill)[0] is None, _tcost(p, seats, bill)[0] or 0, p["t"].lower()))
    return (f'<section class="t50g" data-g="{g}" aria-labelledby="h-{g}"><h2 id="h-{g}">{e(_TG[g])}</h2><div class="tw a49 t50"><table>'
            f'<tr><th scope="col">Plan</th><th scope="col">Price on the official page</th><th scope="col">Your team</th><th scope="col">Per year</th><th scope="col">Good to know</th><th scope="col">Checked</th></tr>'
            + "".join(_trow(p, seats, bill, low) for p in rows) + "</table></div></section>")
def _tquick(seats, bill):
    li = []
    for g, gn in TEAM_GROUPS:
        rows = [p for p in TEAM_PLANS if p["g"] == g]; low = _tlowest(rows, seats, bill)
        if low:
            w = [p for p in rows if p["t"] in low]
            li.append(f'<li><b>{e(gn)}:</b> ' + " = ".join(f'<a href="#t-{slug(p["t"])}">{e(p["t"])} {e(p["plan"].split(" (")[0])}</a>' for p in w) + f' at {_tm(_tcost(w[0], seats, bill)[0])}/mo</li>')
    return "".join(li)
_tjs = [{"k": slug(p["t"]), "t": p["t"], "pl": p["plan"].split(" (")[0], "g": p["g"], "m": p.get("m"), "y": p.get("y"), "b": p.get("base") or 0,
         "f": 1 if p.get("flat") else 0, "mn": p.get("mn") or 1, "mx": p.get("mx") or 0, "ad": 1 if p.get("addon") else 0} for p in TEAM_PLANS]
_t_chips = '<button type="button" class="on" aria-pressed="true" data-g="">All</button>' + "".join(f'<button type="button" aria-pressed="false" data-g="{g}">{e(n)}</button>' for g, n in TEAM_GROUPS)
_t_left = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)}.</li>' if n in TOOL else f'<li>{e(n)}: {e(w)}.</li>' for n, w in TEAM_LEFT_OUT)
_t_n = len(TEAM_PLANS)
def _t_q5(g):
    rows = [p for p in TEAM_PLANS if p["g"] == g]; low = _tlowest(rows, 5, "m")
    return ", ".join(f'{p["t"]} {p["plan"].split(" (")[0]}' for p in rows if p["t"] in low), _tcost(next(p for p in rows if p["t"] in low), 5, "m")[0] if low else None
_qa_t = [("How much does ChatGPT Business cost for a team?", f"$25 per seat per month billed monthly, or $20 billed yearly (standard seat), for teams of 2 to 200; a team of 5 pays $125/mo monthly or $1,200 a year billed yearly. Read on chatgpt.com/pricing on {TEAM_CHECKED}."),
         ("Is Claude Team cheaper than ChatGPT Business?", f"On {TEAM_CHECKED} both standard seats cost the same: $25 per seat per month billed monthly or $20 billed yearly. Claude Team is for 2 to 150 seats, ChatGPT Business for 2 to 200."),
         ("Which AI coding assistant is cheapest for a team?", f"GitHub Copilot Business at $19 per user per month. For 5 developers that is $95/mo, vs Cursor Teams from $150/mo and Windsurf Teams $280/mo ($80 plan fee + $40 per seat), monthly prices read on {TEAM_CHECKED}."),
         ("Do AI team plans have seat minimums?", "Some do: ChatGPT Business, Claude Team, Fathom Team and Beautiful.ai Team start at 2 seats, so a solo buyer pays for 2. Others cap the team size, like Beautiful.ai (20), Otter Business (25 billed users) and Claude Team (150). The calculator applies these automatically."),
         ("Which team plans charge one price for everyone?", "Lovable Business is one price for the whole workspace with unlimited users (from $50/mo, credits shared), so it gets cheaper per person as the team grows. Windsurf charges a fixed $80/mo plan fee on top of $40 per seat.")]
_t_body = f"""<style>{ALT49_CSS[7:-8]}.t50 table{{min-width:0;width:100%}}.t50p{{display:block;font-weight:400;font-size:.92rem}}.t50b{{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 0}}.t50b:empty{{display:none}}.t50 tr.lo{{background:var(--sf2)}}.t50 tr.lo th[scope=row]{{box-shadow:inset 4px 0 0 var(--ok)}}.t50 td.t50tot{{min-width:8em;max-width:15em}}.t50tot b{{white-space:nowrap}}@media(min-width:641px){{.t50 td:nth-child(5){{min-width:13em}}}}
.t50c{{display:flex;flex-wrap:wrap;gap:var(--s3) var(--s5);align-items:flex-end}}.t50s label{{display:block;font-weight:600;margin-bottom:6px}}.t50s .row{{display:flex;gap:6px;align-items:center}}.t50s input{{width:5.5em;text-align:center;font-size:1.1rem;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx)}}.t50s button{{min-width:44px;font-size:1.2rem}}
#t50q{{margin:var(--s4) 0}}#t50q ul{{margin:6px 0 0;padding-left:20px}}#t50q li{{margin:4px 0}}.t50g[hidden],#t50msg:empty{{display:none!important}}.t50g h2{{margin-top:var(--s6)}}</style>
<p class="small"><a href="/my-ai-costs.html">My AI costs</a> › Team plans</p><h1>What will AI tools cost for your team?</h1>
<p class="tag">Enter your team size. We show what {_t_n} team and business plans really cost per month and per year, with seat minimums, seat limits and flat workspace prices applied. Every price was read on the official pricing page on {TEAM_CHECKED}.</p>
<div class="builder"><div class="t50c"><div class="t50s"><label for="t50n">Team size</label><div class="row"><button type="button" class="bbtn" id="t50dec" aria-label="One seat fewer">−</button><input type="number" id="t50n" min="1" max="500" step="1" value="{_T_DEF_SEATS}" inputmode="numeric"><button type="button" class="bbtn" id="t50inc" aria-label="One seat more">+</button></div></div>
<fieldset class="seg"><legend>Billing</legend><input type="radio" name="t50b" id="t50bm" value="m" checked><label for="t50bm">Monthly</label><input type="radio" name="t50b" id="t50by" value="y"><label for="t50by">Billed yearly</label></fieldset></div>
<div class="needs" role="group" aria-label="Show plans for" id="t50cats">{_t_chips}</div>
<p class="small" id="t50msg" role="status"></p></div>
<div class="pick" id="t50q" aria-live="polite"><b id="t50qh">Lowest price for a team of {_T_DEF_SEATS}, billed monthly</b><ul id="t50ql">{_tquick(_T_DEF_SEATS, _T_DEF_BILL)}</ul><p class="small" style="margin:6px 0 0">Compared only within the same job and the same billing. Plans differ in features and usage limits, so open the official page before you buy. <button type="button" class="bbtn" id="t50share">Copy link to these results</button></p></div>
<div id="t50groups">{"".join(_tgroup(g, _T_DEF_SEATS, _T_DEF_BILL) for g, n in TEAM_GROUPS)}</div>
<h2>How we work it out</h2><p class="small">Your team / month = price per seat × seats, using the seat minimum when your team is smaller (you pay for the minimum). Flat plans (one price for the whole workspace) don't multiply. A plan fee, like Windsurf's, is added once. “Billed yearly” uses the monthly rate the page shows when you pay for a year; per year = that × 12. If a page doesn't state a price for the billing you picked, or your team is above the plan's seat limit, we say so instead of guessing. Taxes are extra. Individual plans (Plus, Pro) aren't listed here: see <a href="/ai-subscription-costs.html">AI subscription costs</a>.</p>
<h2>Not included yet</h2><p class="small">We leave a tool out when its official page doesn't let us state the team price clearly (read {TEAM_CHECKED}):</p><ul class="small">{_t_left}</ul>
<p class="small">Related: <a href="/compare-builder.html">Compare tools side by side</a> · <a href="/alternatives.html">Alternatives to popular AI tools</a> · <a href="/best-ai-tools-for-small-business.html">AI tools for small business</a> · <a href="/my-ai-costs.html#calculator">Cost calculator</a></p>
{_faq(_qa_t)}
<script>(function(){{const P={json.dumps(_tjs, separators=(',', ':'))},GN={json.dumps(dict(TEAM_GROUPS), separators=(',', ':'))},N=document.getElementById('t50n'),MSG=document.getElementById('t50msg'),CH=[...document.querySelectorAll('#t50cats button')],SEC=[...document.querySelectorAll('.t50g')];
let seats={_T_DEF_SEATS},bill='m',cat='';const usd=v=>'$'+(Math.abs(v-Math.round(v))<.005?String(Math.round(v)):v.toFixed(2)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,',');
function cost(p){{const per=bill=='y'?p.y:p.m;if(per==null)return {{v:null,why:bill=='y'?'Yearly price not stated. Switch to Monthly to see it.':'Monthly price not stated. Switch to Billed yearly to see it.'}};if(p.mx&&seats>p.mx)return {{v:null,why:'This plan allows up to '+p.mx+' seats.'}};const b=Math.max(seats,p.mn);return {{v:p.f?per:p.b+per*b,b}}}}
function low(g){{const c=P.filter(p=>p.g==g&&!p.ad).map(p=>[p,cost(p).v]).filter(x=>x[1]!=null);if(c.length<2)return [];const lo=Math.min(...c.map(x=>x[1]));return c.filter(x=>Math.abs(x[1]-lo)<.005).map(x=>x[0])}}
function render(push){{const q=document.getElementById('t50ql');let qh='';
SEC.forEach(s=>{{const g=s.dataset.g,L=low(g),LK=L.map(p=>p.k),tb=s.querySelector('tbody')||s.querySelector('table');s.hidden=!!cat&&cat!=g;
const rows=P.filter(p=>p.g==g).sort((a,b)=>{{const A=cost(a).v,B=cost(b).v;return (a.ad-b.ad)||((A==null)-(B==null))||((A||0)-(B||0))||a.t.toLowerCase().localeCompare(b.t.toLowerCase())}});
rows.forEach(p=>{{const tr=document.getElementById('t-'+p.k),c=cost(p),tot=tr.querySelector('.t50tot'),yr=tr.querySelector('.t50yr'),bd=tr.querySelector('.t50b');
if(c.v==null){{tot.innerHTML='<span class="check">'+c.why+'</span>';yr.textContent='–'}}else{{tot.innerHTML='<b>'+usd(c.v)+'</b>/mo'+(c.b!=seats&&!p.f?'<br><span class="small">billed for '+c.b+' seats (minimum)</span>':'');yr.textContent=usd(c.v*12)+(bill=='y'?'/yr':'/yr if you stay 12 months')}}
const isl=LK.includes(p.k);tr.classList.toggle('lo',isl);let lb=bd.querySelector('.b-best');if(isl&&!lb){{lb=document.createElement('span');lb.className='badge b-best';lb.textContent='LOWEST FOR YOUR TEAM';bd.prepend(lb)}}else if(!isl&&lb)lb.remove();tr.parentNode.appendChild(tr)}});
if(L.length&&(!cat||cat==g))qh+='<li><b>'+GN[g]+':</b> '+L.map(p=>'<a href="#t-'+p.k+'">'+p.t+' '+p.pl+'</a>').join(' = ')+' at '+usd(cost(L[0]).v)+'/mo</li>'}});
q.innerHTML=qh||'<li>'+(bill=='y'?'Not enough yearly prices to compare here. Try Monthly.':'Not enough plans fit this team size to compare. See the table below.')+'</li>';document.getElementById('t50qh').textContent='Lowest price for '+(seats==1?'1 person':'a team of '+seats)+', '+(bill=='y'?'billed yearly':'billed monthly');
CH.forEach(b=>{{const on=b.dataset.g==cat;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)}});
const u=new URLSearchParams();if(seats!={_T_DEF_SEATS})u.set('seats',seats);if(bill=='y')u.set('bill','y');if(cat)u.set('cat',cat);const s=u.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash)}}
function setSeats(v,typed){{let n=parseInt(v,10);MSG.textContent='';if(isNaN(n)){{if(!typed||String(v).trim()!==''){{MSG.textContent='Team size must be a number, so we used 1.'}}n=1}}if(n<1){{n=1;MSG.textContent='Team size starts at 1.'}}if(n>500){{n=500;MSG.textContent='This calculator goes up to 500 seats. Bigger teams usually get custom pricing.'}}seats=n;if(!typed||String(N.value)!==String(n))N.value=n;render()}}
const p=new URLSearchParams(location.search);if(p.get('bill')=='y')bill='y';if(p.get('cat')&&GN[p.get('cat')])cat=p.get('cat');document.getElementById(bill=='y'?'t50by':'t50bm').checked=true;
N.addEventListener('input',()=>{{if(N.value.trim()!=='')setSeats(N.value,true)}});N.addEventListener('change',()=>setSeats(N.value,false));
document.getElementById('t50dec').addEventListener('click',()=>setSeats(seats-1));document.getElementById('t50inc').addEventListener('click',()=>setSeats(seats+1));
document.querySelectorAll('input[name=t50b]').forEach(r=>r.addEventListener('change',()=>{{bill=r.value;render()}}));CH.forEach(b=>b.addEventListener('click',()=>{{cat=b.dataset.g;render()}}));
document.getElementById('t50share').addEventListener('click',e=>{{const t=location.href,b=e.currentTarget,ok=()=>{{MSG.textContent='Link copied. It opens with this team size and billing.'}};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,()=>prompt('Copy this link:',t));else prompt('Copy this link:',t)}});
if(p.get('seats'))setSeats(p.get('seats'));else render();if(location.hash){{const el=document.getElementById(location.hash.slice(1));if(el){{el.classList.add('lo');el.scrollIntoView({{block:'center'}})}}}}}})();</script>"""
page(TEAM_PATH, f"AI Team Plan Costs ({TEAM_CHECKED[:4]}): ChatGPT Business, Claude Team, Copilot & More by Seat | ToolPick",
     f"Enter your team size and see what {_t_n} AI team plans cost per month and per year: ChatGPT Business, Claude Team, GitHub Copilot, Cursor, Notion, Otter, Gamma and more, with seat minimums applied. Official prices read {TEAM_CHECKED}.",
     _t_body, [{"@context": "https://schema.org", "@type": "WebApplication", "name": "AI team plan cost calculator", "url": BASE + TEAM_PATH, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": f"Monthly and yearly cost of {_t_n} AI team plans for any team size, from official pricing pages read {TEAM_CHECKED}."},
               {"@context": "https://schema.org", "@type": "ItemList", "name": "AI team and business plans", "url": BASE + TEAM_PATH,
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{p["t"]} {p["plan"]}', "url": BASE + TEAM_PATH + "#t-" + slug(p["t"])} for i, p in enumerate(TEAM_PLANS)]},
               _ld_faq(_qa_t), crumbs([("ToolPick", "/"), ("My AI costs", "/my-ai-costs.html"), ("Team plans", TEAM_PATH)])])
V50_CHANGED = [TEAM_PATH]
def _v50ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if 'v50"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V50_CHANGED.append(path); return True
for _p in TEAM_PLANS:
    _v, _b, _w = _tcost(_p, 5, "m") if _p.get("m") is not None else _tcost(_p, 5, "y")
    _bl = "monthly" if _p.get("m") is not None else "billed yearly"
    _line = (f'<p class="pick small v50"><b>Buying for a team?</b> {e(_p["t"])} {e(_p["plan"])}: {_tper(_p)} (checked {TEAM_CHECKED})'
             + ((f', so a team of 5 pays {_tm(_v)}/mo monthly' if _bl == "monthly" else f', so a team of 5 pays {_tm(_v * 12)} a year billed yearly') if _v is not None else "") + f'. <a href="{TEAM_PATH}?cat={_p["g"]}#t-{slug(_p["t"])}">Team costs for your team size →</a></p>')
    if not _v50ins(turl(_p["t"]), '<section class="card tbp"', _line): _v50ins(turl(_p["t"]), '<section class="verdict', _line)
_T_LINE = f'<p class="small v50">Buying for a team? <a href="{TEAM_PATH}">See what {_t_n} AI team plans cost for your team size →</a></p>'
for _pp in ["/best-ai-tools-for-small-business.html", "/compare-builder.html", "/chatgpt-pricing.html", "/is-claude-pro-worth-it.html", "/ai-subscription-costs.html", "/cheapest-ai-coding-assistant.html", "/tools.html"]:
    _v50ins(_pp, "</h1>", _T_LINE, after=True)
_v50ins("/guides.html", "<h2>New guides</h2><ul>", f"<li class=\"v50\"><a href='{TEAM_PATH}'>What AI tools cost for your team (team plans by seat)</a></li>", after=True)
for _x in COMPARISONS:
    _gs = [_p["g"] for _p in TEAM_PLANS if _p["t"] in cnames(_x)]
    _ls = sorted({g for g in _gs if _gs.count(g) >= 2})  # only when at least 2 of the compared tools have a team plan for the same job
    if _ls:
        _v50ins(f"/compare/{_x[0]}.html", "</h1>", f'<p class="small v50">Buying seats for a team? <a href="{TEAM_PATH}?cat={_ls[0]}">Compare their team plans by team size →</a></p>', after=True)
# Finder: when the search mentions a team size, show a one-tap link to team plan costs with that size (doesn't change results)
_TH = f'<p class="pick v50 tmhint" hidden><b>Buying for a team?</b> <a id="tmlink" href="{TEAM_PATH}">See team plan costs for your team size →</a></p>'
_h = open("public/index.html").read()
assert '<div id="out" aria-live="polite">' in _h
open("public/index.html", "w").write(_h.replace('<div id="out" aria-live="polite">', _TH + '<style>.tmhint[hidden]{display:none!important}.tmhint{margin:var(--s3) auto;max-width:720px;text-align:left}</style><div id="out" aria-live="polite">' + '<script>(function(){const q=document.getElementById("q"),H=document.querySelector(".tmhint"),A=document.getElementById("tmlink");if(!q||!H)return;const re=/\\b(?:team|group|company|agency|staff) of (\\d{1,3})\\b|\\b(\\d{1,3}) (?:people|users|seats|members|employees|devs|developers|teammates)\\b|\\bfor (?:my|our|a) (?:team|company|business|startup|agency)\\b/i;const rn=/\\b(?:team|group|company|agency|staff) of (\\d{1,3})\\b|\\b(\\d{1,3}) (?:people|users|seats|members|employees|devs|developers|teammates)\\b/i;const f=()=>{const m=q.value.match(re);H.hidden=!m;if(m){const k=q.value.match(rn),n=k?(k[1]||k[2]):null;A.href="' + TEAM_PATH + '"+(n?"?seats="+n:"");A.textContent=n?"See team plan costs for "+n+" seats →":"See team plan costs for your team size →"}};q.addEventListener("input",f);addEventListener("load",f);document.addEventListener("click",()=>setTimeout(f,50));f()})()</script>', 1)); V50_CHANGED.append("/")
open("public/llms.txt", "a").write(f"\n## AI team plan costs (v50)\n- [What AI tools cost for your team]({BASE}{TEAM_PATH}): {_t_n} team/business plans (ChatGPT Business, Claude Team, Le Chat Team, Perplexity Enterprise Pro, Microsoft 365 Copilot Business, GitHub Copilot Business, Cursor Teams, Windsurf Teams, Bolt Teams, Lovable Business, Otter, Fireflies, Fathom, Notion Business, Gamma, Beautiful.ai, Plus AI, Canva Business, Ideogram, Recraft, Descript, CapCut) with per-seat price, seat minimum/maximum, flat workspace prices and plan fees; monthly and yearly totals for any team size; lowest price per job; official pages read {TEAM_CHECKED}. Params: ?seats=10&bill=y&cat=coding\n")

# --- v51: ElevenLabs pricing + Is ElevenLabs worth it ---
ELC = _tm0.EL_CHECKED
def _m(v): return "Custom" if v is None else ("$0" if v == 0 else f"${v:,.2f}".replace(".00", ""))
def _ppm(p, mins):
    try: return f"~${p / int(mins.strip('~').replace(',', '')):.2f}" if p else "—"
    except Exception: return "—"
_el_rows = "".join(f"<tr><th scope='row'>{e(n)}</th><td>{_m(mo)}</td><td>{_m(yr) if yr is not None else ('—' if mo == 0 else 'Custom')}</td><td>{cr}</td><td>{mi}</td><td>{_ppm(mo, mi)}</td><td>{e(pr) or '—'}</td><td>{e(k)}</td></tr>" for n, mo, yr, cr, mi, pr, k in _tm0.EL_PLANS)
_el_cr = "".join(f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in _tm0.EL_CREDITS)
_qa_el = [("How much is ElevenLabs per month?", f"Free $0, Starter $6, Creator $22, Pro $99, Scale $299, Business $990 on monthly billing; Enterprise is custom (elevenlabs.io/pricing, {ELC}). Prices exclude taxes."),
          ("Is there an ElevenLabs discount right now?", f"On {ELC} the pricing page showed Starter at $1 for the first month (until Nov 1) and Creator at $11 for the first month (50% off). A separate banner on the same page said \"Ends September 30\", so check the page before you subscribe."),
          ("How many characters do ElevenLabs credits buy?", "For text to speech, 1 credit is 1 character on V2 Multilingual models (Flash/Turbo models cost 0.5–1 credit per character via the API). ElevenLabs estimates 10,000 credits at about 10 minutes of speech."),
          ("Is yearly billing cheaper?", "Yes. Yearly costs 10× the monthly price (two months free): Starter $5/mo, Creator $18.33/mo, Pro $82.50/mo."),
          ("Do unused credits roll over?", "On active paid plans, unused credits roll over for up to two months (a balance of up to 3× your monthly quota). They don't roll over on Free, and are forfeited if you downgrade or cancel.")]
_el_body = f"""<p class="small"><a href="{turl('ElevenLabs')}">ElevenLabs</a> › Pricing</p><h1>ElevenLabs pricing: plans, credits and minutes</h1>
<p class="tag">Every ElevenLabs plan from <a href="https://elevenlabs.io/pricing" rel="noopener" target="_blank">elevenlabs.io/pricing</a>, checked {ELC}. Monthly billing unless marked yearly.</p>
<p class="pick"><b>In short:</b> Free gives 10,000 credits (~10 min of speech) with no commercial license. Starter is $6/mo for 30,000 credits and a commercial license, and is $1 for the first month until Nov 1. Creator is $22/mo for 121,000 credits and Professional Voice Cloning.</p>
<h2>Plans and prices</h2><div class="tw"><table><caption class="small" style="text-align:left">Checked {ELC}. Minutes are ElevenLabs' own text-to-speech estimate. “Per minute” is our calculation: monthly price ÷ included minutes.</caption><tr><th scope="col">Plan</th><th scope="col">Monthly</th><th scope="col">Yearly (per month)</th><th scope="col">Credits / month</th><th scope="col">~Minutes of speech</th><th scope="col">Per minute</th><th scope="col">First-month offer</th><th scope="col">Adds</th></tr>{_el_rows}</table></div>
<h2>What credits buy</h2><p>All products share one monthly credit pool.</p><div class="tw"><table><caption class="small" style="text-align:left">Approximate credit costs, from the official FAQ ({ELC}).</caption><tr><th scope="col">Product</th><th scope="col">Credits</th></tr>{_el_cr}</table></div>
{_faq(_qa_el)}
<p class="small">Related: <a href="/is-elevenlabs-worth-it.html">Is ElevenLabs worth it?</a> · <a href="/free-alternative-to-elevenlabs.html">Free alternatives to ElevenLabs</a> · <a href="/my-ai-costs.html#voice">AI voice cost</a> · <a href="/compare/elevenlabs-vs-murf.html">ElevenLabs vs Murf</a></p>"""
page("/elevenlabs-pricing.html", f"ElevenLabs Pricing ({ELC[:4]}): Plans, Credits & Minutes Explained | ToolPick",
     f"ElevenLabs plans checked {ELC}: Free $0 (10k credits), Starter $6 (30k, $1 first month), Creator $22 (121k), Pro $99, Scale $299, Business $990. Yearly prices, minutes and credit costs.",
     _el_body, [{"@context": "https://schema.org", "@type": "Product", "name": "ElevenLabs", "url": BASE + "/elevenlabs-pricing.html", "brand": {"@type": "Brand", "name": "ElevenLabs"},
                 "offers": [{"@type": "Offer", "name": n, "price": mo, "priceCurrency": "USD"} for n, mo, *_ in _tm0.EL_PLANS if mo is not None]},
                _ld_faq(_qa_el), crumbs([("ToolPick", "/"), ("ElevenLabs", turl("ElevenLabs")), ("ElevenLabs pricing", "/elevenlabs-pricing.html")])])
_qa_ew = [("Is ElevenLabs Starter worth $6?", f"If you need a commercial license or voice cloning, yes: those start at Starter. You get 30,000 credits (~30 min of speech). On {ELC} the first month was $1 (until Nov 1)."),
          ("Can I use the free plan for YouTube or client work?", "Free has no commercial license, which starts at Starter. Free does include 10,000 credits a month for text to speech, speech to text, sound effects and music."),
          ("Starter or Creator?", "Creator ($22) adds Professional Voice Cloning and about 4× Starter's credits (121,000 vs 30,000). Pick it if you need a close clone of your own voice, or more than ~30 minutes a month."),
          ("Is there a cheaper way to pay?", "Yearly billing costs 10 months' price for 12, so Starter is $5/mo and Creator $18.33/mo. Unused credits also roll over for up to two months on active paid plans.")]
_ew_body = f"""<p class="small"><a href="{turl('ElevenLabs')}">ElevenLabs</a> › Is it worth it?</p><h1>Is ElevenLabs worth it?</h1>
<p class="tag">Free vs Starter vs Creator: what each step up gets you, from <a href="https://elevenlabs.io/pricing" rel="noopener" target="_blank">elevenlabs.io/pricing</a> (checked {ELC}).</p>
<p class="pick"><b>Short answer:</b> stay on Free for personal tests under ~10 minutes a month. Pay for Starter ($6) when you publish or sell the audio, because the commercial license starts there. Pay for Creator ($22) when you need Professional Voice Cloning or more than ~30 minutes a month.</p>
<div class="tw"><table><caption class="small" style="text-align:left">Monthly billing, checked {ELC}.</caption><tr><th scope="col"></th><th scope="col">Free</th><th scope="col">Starter</th><th scope="col">Creator</th></tr>
<tr><th scope="row">Price</th><td>$0</td><td>$6/mo ($1 first month, until Nov 1)</td><td>$22/mo ($11 first month)</td></tr>
<tr><th scope="row">Credits</th><td>10,000 (~10 min)</td><td>30,000 (~30 min)</td><td>121,000 (~121 min)</td></tr>
<tr><th scope="row">Commercial license</th><td>No</td><td>Yes</td><td>Yes</td></tr>
<tr><th scope="row">Voice cloning</th><td>No</td><td>Instant</td><td>Instant + Professional</td></tr>
<tr><th scope="row">Dubbing Studio</th><td>No</td><td>Yes</td><td>Yes</td></tr>
<tr><th scope="row">Credit rollover</th><td>No</td><td>Up to 2 months</td><td>Up to 2 months</td></tr></table></div>
<h2>Worth it if…</h2><ul><li>You publish voiceovers, podcasts or videos and need the commercial license.</li><li>You want to clone a voice: Instant on Starter, Professional on Creator.</li><li>You also use speech to text, sound effects or music, which all draw on the same credits.</li></ul>
<h2>Skip it if…</h2><ul><li>You only need a few minutes for personal use: Free covers ~10 minutes a month.</li><li>You just need text read aloud: see <a href="/free-alternative-to-elevenlabs.html">free alternatives to ElevenLabs</a>.</li></ul>
{_faq(_qa_ew)}
<p class="small">Related: <a href="/elevenlabs-pricing.html">ElevenLabs pricing (all plans)</a> · <a href="/my-ai-costs.html#voice">AI voice cost</a> · <a href="/compare/elevenlabs-vs-speechify.html">ElevenLabs vs Speechify</a> · <a href="/pay-less.html">Pay less for the same job</a></p>"""
page("/is-elevenlabs-worth-it.html", f"Is ElevenLabs Worth It? ({ELC[:4]}) Free vs Starter vs Creator | ToolPick",
     f"Is ElevenLabs worth paying for? Free (10k credits, no commercial use) vs Starter $6 (commercial license, cloning) vs Creator $22, from elevenlabs.io/pricing checked {ELC}.",
     _ew_body, [_ld_faq(_qa_ew), crumbs([("ToolPick", "/"), ("ElevenLabs", turl("ElevenLabs")), ("Is ElevenLabs worth it?", "/is-elevenlabs-worth-it.html")])])
V51_CHANGED = ["/elevenlabs-pricing.html", "/is-elevenlabs-worth-it.html"]
def _v51ins(path, marker, html, after=False):
    _fp = "public" + path
    if not __import__("os").path.exists(_fp): return
    _h = open(_fp).read()
    if ' v51"' in _h or marker not in _h: return
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V51_CHANGED.append(path)
_EL2 = '<a href="/elevenlabs-pricing.html">ElevenLabs pricing</a> · <a href="/is-elevenlabs-worth-it.html">Is ElevenLabs worth it?</a>'
_v51ins(turl("ElevenLabs"), '<section class="card tbp"', f'<p class="pick small v51">All plans, credits and minutes ({ELC}): {_EL2}</p>')
for _p in ["/free-alternative-to-elevenlabs.html", "/pay-less.html"] + [f"/compare/{_x[0]}.html" for _x in COMPARISONS if "ElevenLabs" in cnames(_x)]:
    _v51ins(_p, "</h1>", f'<p class="small v51">{_EL2}</p>', after=True)
open("public/llms.txt", "a").write(f"\n## ElevenLabs plans\n- [ElevenLabs pricing]({BASE}/elevenlabs-pricing.html): every plan with monthly and yearly price, credits, minutes, first-month offers and credit costs per product (elevenlabs.io/pricing, {ELC})\n- [Is ElevenLabs worth it?]({BASE}/is-elevenlabs-worth-it.html): Free vs Starter vs Creator, when to pay and when to skip ({ELC})\n")

# --- v52: Can I get a refund? Refund windows + how to cancel (/ai-refund-policies.html) ---
# Rules read on each tool's official help page on REFUND_CHECKED (tools.py REFUNDS, exact words in q).
# Checker: tool + when you were charged (+ billing) -> inside / at the edge / past the refund window, how to ask, how to cancel.
REFUND_CHECKED = _tm0.REFUND_CHECKED; REFUNDS = sorted(_tm0.REFUNDS, key=lambda r: r["t"].lower()); REFUND_LEFT_OUT = _tm0.REFUND_LEFT_OUT
R_PATH = "/ai-refund-policies.html"
for _r in REFUNDS:
    assert _r["t"] in TOOL and _r["k"] in "wcn" and _r["q"] and _r["sr"].startswith("https://") and _r["sc"].startswith("https://") and _r["cancel"], _r["t"]
    if _r["k"] == "n": assert _r["wm"] is None and _r["wy"] is None, _r["t"]
_RK = {"w": "Refund window", "c": "Case by case", "n": "No refunds"}
def _rwin(h): return None if h is None else (f"{h}-hour" if h < 72 else f"{h // 24}-day")
def _rshort(r):
    """One plain line: the refund rule."""
    if r["k"] == "n": return f"{r['t']} doesn't give refunds. Cancelling only stops the next charge."
    wm, wy = r["wm"], r["wy"]
    if wm is None and wy is None:
        return (f"Only if {r['cond'][4:] if r['cond'].startswith('you ') else r['cond']}." if r["k"] == "w" else f"Case by case: {r['cond']}.")
    w = (f"within {_rwin(wm).replace('-', ' ')}s" if wm == wy else f"within {_rwin(wm).replace('-', ' ')}s (monthly) or {_rwin(wy).replace('-', ' ')}s (yearly)")
    return ("Case by case, " if r["k"] == "c" else "Possible ") + w + " of the charge" + _RSUF.get(r["t"], "") + "."
_RSUF = {"ChatGPT": ", if the subscription is unused (their call)", "Cursor": ", if you haven't used it that billing period", "ElevenLabs": ", if you haven't used any credits",
         "Gamma": " when you first subscribe, only through support and under a credit limit", "HeyGen": ", less likely if you used a lot of credits", "Notion AI": ", asked from the owner or billing email",
         "Runway": ", if unused or close to unused (their call)", "Fireflies": ", depending on how many meetings you logged", "Jasper": ", after you cancel", "Perplexity": ", one refund per account"}
def _rdet(r):
    a = []
    if r["cond"]: a.append(f'<li><b>{"Who qualifies" if r["k"] != "n" else "Rule"}:</b> {e(r["cond"][0].upper() + r["cond"][1:])}.</li>')
    if r["how"]: a.append(f'<li><b>{"How to ask" if r["k"] != "n" else "Billing problem"}:</b> {e(r["how"])}</li>')
    if r["eu"]: a.append(f'<li><b>Where you live matters:</b> {e(r["eu"])}</li>')
    a.append(f'<li><b>How to cancel:</b> {e(r["cancel"])}{(" — do it " + e(r["notice"])) if r["notice"] else ""}.</li>')
    if r["after"]: a.append(f'<li><b>After you cancel:</b> {e(r["after"])}</li>')
    if r["app"]: a.append(f'<li><b>Paid in the iPhone or Android app?</b> Apple or Google handles that refund and cancel, not {e(r["t"])}.</li>')
    return ("<ul class=\"r52l\">" + "".join(a) + f'</ul><p class="small r52q">In their words: “{e(r["q"])}”</p>'
            f'<p class="small">Read {REFUND_CHECKED}: <a href="{e(r["sr"])}" rel="noopener" target="_blank">refund page<span class="skip"> for {e(r["t"])} (opens in a new tab)</span></a>'
            + (f' · <a href="{e(r["sc"])}" rel="noopener" target="_blank">cancel page<span class="skip"> for {e(r["t"])} (opens in a new tab)</span></a>' if r["sc"] != r["sr"] else "") + "</p>")
def _rcard(r):
    s = slug(r["t"])
    return (f'<article class="r52c r52{r["k"]}" id="r-{s}" data-k="{r["k"]}"><h3><a href="{turl(r["t"])}">{e(r["t"])}</a> <span class="r52b">{_RK[r["k"]]}</span></h3>'
            f'<p>{e(_rshort(r))}</p>' + (f'<p class="small check">Cancel {e(r["notice"])} or you may be charged again.</p>' if r["notice"] else "")
            + f'<details><summary>How to ask and how to cancel</summary>{_rdet(r)}</details><p class="small"><a href="{R_PATH}?tool={s}#check">Check my dates for {e(r["t"])}</a></p></article>')
_rn = len(REFUNDS); _rc = {k: sum(1 for r in REFUNDS if r["k"] == k) for k in "wcn"}
_r_opts = '<option value="">Choose a tool…</option>' + "".join(f'<option value="{slug(r["t"])}">{e(r["t"])}</option>' for r in REFUNDS)
_WHEN = [("pre", "I haven't paid yet", None, None), ("h24", "Less than 24 hours ago", 0, 24), ("d2", "1–2 days ago", 24, 48), ("d3", "2–3 days ago", 48, 72),
         ("d7", "4–7 days ago", 72, 168), ("d14", "8–14 days ago", 168, 336), ("d30", "15–30 days ago", 336, 720), ("old", "More than 30 days ago", 720, None)]
_w_opts = "".join(f'<option value="{k}">{e(l)}</option>' for k, l, a, b in _WHEN)
_r_chips = (f'<button type="button" class="on" aria-pressed="true" data-k="">All {_rn}</button>' + "".join(f'<button type="button" aria-pressed="false" data-k="{k}">{_RK[k]} ({_rc[k]})</button>' for k in "wcn"))
def _rjs(r): return {"s": slug(r["t"]), "t": r["t"], "k": r["k"], "wm": r["wm"], "wy": r["wy"], "c": r["cond"], "sh": _rshort(r), "d": _rdet(r), "n": r["notice"]}
_r_short = sorted([r for r in REFUNDS if r["wm"]], key=lambda r: r["wm"])
_r_tips = [
    "Shortest refund windows: " + ", ".join(f'<a href="#r-{slug(r["t"])}">{e(r["t"])}</a> ({_rwin(r["wm"])}' + (f" monthly, {_rwin(r['wy'])} yearly" if r["wy"] != r["wm"] else "") + ")" for r in _r_short if r["wm"] <= 72) + ". Try the free plan first, then test hard on day one.",
    "Cancel early: " + ", ".join(f'<a href="#r-{slug(r["t"])}">{e(r["t"])}</a> ({e(r["notice"])})' for r in REFUNDS if r["notice"]) + ".",
    "No refunds at all: " + ", ".join(f'<a href="#r-{slug(r["t"])}">{e(r["t"])}</a>' for r in REFUNDS if r["k"] == "n") + ". Start monthly, not yearly, until you're sure.",
    "Pause instead of cancelling: Canva (up to 3 months), Jasper (30, 60 or 90 days), Otter (once) and HeyGen offer a pause.",
    "You can lose things when you cancel: Synthesia removes access to your videos after the period ends, ElevenLabs and HeyGen unused credits go, Lovable freezes unused credits. Export first."]
_r_left = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)}.</li>' if n in TOOL else f'<li>{e(n)}: {e(w)}.</li>' for n, w in REFUND_LEFT_OUT)
_qa_r = [("Can I get a refund on ChatGPT Plus?", f"Payments are generally non-refundable, but OpenAI says a discretionary refund may be available for an unused individual subscription if you ask within seven days of the charge, through the Help Center chat. In the EU, UK and Turkey you get a prorated refund if you cancel within 14 days. Read {REFUND_CHECKED}."),
         ("Can I get a refund on Claude Pro?", f"Anthropic says all payments are non-refundable except where its Consumer Terms or the law say otherwise. You can check eligibility under Get help → Send us a message → Claude Refund Request. EEA and UK users can get a refund within 14 days, reduced for use. Read {REFUND_CHECKED}."),
         ("Which AI tools give refunds?", f"Of the {_rn} tools we checked on {REFUND_CHECKED}, {_rc['w']} state a refund window or rule (for example Cursor and ElevenLabs: 14 days if unused; Runway: 30 days if unused or close to unused), {_rc['c']} decide case by case, and {_rc['n']} don't refund: " + ", ".join(r["t"] for r in REFUNDS if r["k"] == "n") + "."),
         ("Does cancelling give me my money back?", "No. On every tool here, cancelling only stops the next renewal. You keep access until the end of the period you paid for. A refund is a separate request, usually to support, and most have a short window."),
         ("I paid in the iPhone app. Who refunds me?", "Apple. App Store subscriptions are refunded and cancelled through Apple (Google Play for Android), not by the tool itself. Several help pages say this, including ChatGPT, Notion, Canva and Perplexity.")]
_R_CSS = ("<style>.r52g{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:var(--s4);margin:var(--s4) 0}"
          ".r52c{background:var(--sf);border:1px solid var(--bd);border-left:4px solid var(--mu);border-radius:var(--r);padding:var(--s4);box-shadow:var(--sh)}.r52c.r52w{border-left-color:var(--ok)}.r52c.r52c{border-left-color:var(--warn)}.r52c[hidden]{display:none}"
          ".r52c h3{margin:0 0 6px;font-size:1.05rem}.r52c h3 a{min-height:32px}.r52c p{margin:6px 0}.r52b{display:inline-block;font-size:.72rem;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--sf2);color:var(--tx);vertical-align:middle}"
          ".r52c details summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:600;color:var(--ac)}.r52l{padding-left:18px;margin:6px 0}.r52l li{margin:4px 0}.r52q{font-style:italic}"
          ".r52f{display:flex;flex-wrap:wrap;gap:var(--s3) var(--s5);align-items:flex-end}.r52f label{display:block;font-weight:600;margin-bottom:6px}.r52f select{font-size:1rem;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 10px;min-width:min(100%,240px)}.r52f>div{max-width:100%}"
          "#r52out{margin:var(--s4) 0}#r52out h2{margin:0 0 6px;font-size:1.25rem}#r52out.r52in{border-left:4px solid var(--ok)}#r52out.r52edge,#r52out.r52case{border-left:4px solid var(--warn)}#r52out.r52out,#r52out.r52no{border-left:4px solid var(--mu)}"
          ".r52tips li{margin:6px 0}#r52msg:empty{display:none}</style>")
_r_body = f"""{_R_CSS}<p class="small"><a href="/save-money.html">Save money</a> › Refunds and cancelling</p><h1>Can I get a refund? AI subscription refund and cancel rules</h1>
<p class="tag">Pick your tool and when you paid. We tell you if you're still inside its refund window, how to ask, and how to cancel. Rules for {_rn} AI tools, read on each official help page on {REFUND_CHECKED}.</p>
<div class="builder" id="check"><div class="r52f"><div><label for="r52t">Tool</label><select id="r52t">{_r_opts}</select></div><div><label for="r52w">When were you charged?</label><select id="r52w">{_w_opts}</select></div>
<fieldset class="seg"><legend>Billing</legend><input type="radio" name="r52b" id="r52bm" value="m" checked><label for="r52bm">Monthly</label><input type="radio" name="r52b" id="r52by" value="y"><label for="r52by">Yearly</label></fieldset></div>
<div class="pick" id="r52out" aria-live="polite"><h2 id="r52h">Choose a tool to see its refund rule</h2><div id="r52d"><p class="small">Or scroll down: every tool's rule is listed below.</p></div><p class="small" style="margin:6px 0 0"><button type="button" class="bbtn" id="r52share">Copy link to this answer</button> <span id="r52msg" role="status"></span></p></div></div>
<p class="small">Refund rules change, and most say a refund “may” be given. We show what the official page says; the company decides. Not legal advice.</p>
<h2>Before you subscribe</h2><ul class="r52tips">{"".join(f"<li>{t}</li>" for t in _r_tips)}</ul>
<h2>All {_rn} tools at a glance</h2><div class="needs" role="group" aria-label="Show tools with" id="r52k">{_r_chips}</div>
<div class="r52g" id="r52all">{"".join(_rcard(r) for r in REFUNDS)}</div>
<h2>Not included yet</h2><p class="small">We leave a tool out when its official page doesn't state the rule clearly (read {REFUND_CHECKED}):</p><ul class="small">{_r_left}</ul>
<p class="small">Related: <a href="/my-ai-costs.html#audit">Subscription audit</a> · <a href="/my-ai-costs.html#reminders">Renewal reminders</a> · <a href="/monthly-or-yearly.html">Monthly or yearly?</a> · <a href="/pay-less.html">Pay less for the same job</a> · <a href="/alternatives.html">Alternatives to popular AI tools</a></p>
{_faq(_qa_r)}
<script>__R52JS__</script>"""
_R_JS = r"""(function(){const R=__DATA__,W=__WHEN__,S=document.getElementById('r52t'),WS=document.getElementById('r52w'),H=document.getElementById('r52h'),D=document.getElementById('r52d'),O=document.getElementById('r52out'),M=document.getElementById('r52msg'),CH=[...document.querySelectorAll('#r52k button')],CA=[...document.querySelectorAll('.r52c')];
const by={};R.forEach(r=>by[r.s]=r);const wf=h=>h<72?h+'-hour':(h/24)+'-day';let bill='m',kind='';
function render(){const r=by[S.value],w=W[WS.value]||W.pre;O.className='pick';M.textContent='';
if(!r){H.textContent='Choose a tool to see its refund rule';D.innerHTML='<p class="small">Or scroll down: every tool\'s rule is listed below.</p>';}
else{const h=bill=='y'?r.wy:r.wm;let t,c;
if(r.k=='n'){t=r.t+" doesn't give refunds";c='r52no'}
else if(h==null){t=r.k=='w'?r.t+': depends on how much you used, not on the date':r.t+': refunds are case by case';c='r52case'}
else if(w.a==null){t=r.t+' has a '+wf(h)+' refund window'+(r.k=='c'?' (case by case)':'')+' after you pay';c='r52case'}
else if(w.b!=null&&w.b<=h){t="You're inside "+r.t+"'s "+wf(h)+' refund window'+(r.k=='c'?' (they decide case by case)':'');c='r52in'}
else if(w.a>=h){t=r.t+"'s "+wf(h)+' refund window has passed';c='r52out'}
else{t="You're at the edge of "+r.t+"'s "+wf(h)+' refund window. Ask today';c='r52edge'}
O.classList.add(c);H.textContent=t;let lead=(c=='r52out'||c=='r52no')?'<p><b>Cancel now to stop the next charge.</b>'+(r.n?' Do it '+r.n+'.':'')+'</p>':(c=='r52in'||c=='r52edge')?'<p><b>Ask soon, and check the conditions below.</b></p>':'';
D.innerHTML=lead+'<p>'+r.sh+'</p>'+r.d}
CA.forEach(a=>{a.hidden=!!kind&&a.dataset.k!=kind});CH.forEach(b=>{const on=b.dataset.k==kind;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});
const u=new URLSearchParams();if(S.value)u.set('tool',S.value);if(WS.value!='pre')u.set('when',WS.value);if(bill=='y')u.set('bill','y');if(kind)u.set('k',kind);const s=u.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash)}
const p=new URLSearchParams(location.search);if(by[p.get('tool')])S.value=p.get('tool');if(W[p.get('when')])WS.value=p.get('when');if(p.get('bill')=='y'){bill='y';document.getElementById('r52by').checked=true}if('wcn'.includes(p.get('k')||'x'))kind=p.get('k');
S.addEventListener('change',render);WS.addEventListener('change',render);document.querySelectorAll('input[name=r52b]').forEach(x=>x.addEventListener('change',()=>{bill=x.value;render()}));CH.forEach(b=>b.addEventListener('click',()=>{kind=b.dataset.k;render()}));
document.querySelectorAll('.r52c a[href*="?tool="]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();S.value=new URL(a.href).searchParams.get('tool');render();document.getElementById('check').scrollIntoView({block:'start'});S.focus()}));
document.getElementById('r52share').addEventListener('click',()=>{const t=location.href,ok=()=>{M.textContent='Link copied.'};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,()=>prompt('Copy this link:',t));else prompt('Copy this link:',t)});
render();if(location.hash&&location.hash!='#check'){const el=document.getElementById(location.hash.slice(1));if(el){const d=el.querySelector('details');if(d)d.open=true;el.scrollIntoView({block:'center'})}}})();"""
_R_JS = _R_JS.replace("__DATA__", json.dumps([_rjs(r) for r in REFUNDS], separators=(",", ":")).replace("</", "<\\/")).replace("__WHEN__", json.dumps({k: {"a": a, "b": b} for k, l, a, b in _WHEN}, separators=(",", ":")))
page(R_PATH, f"Can I Get a Refund? AI Subscription Refund & Cancel Rules ({REFUND_CHECKED[:4]}): ChatGPT, Claude, Cursor & More | ToolPick",
     f"Refund windows and cancel steps for {_rn} AI tools: ChatGPT, Claude, Perplexity, Midjourney, Cursor, Copilot, ElevenLabs, Canva, Notion, Runway and more. Check if you're still inside the window. Official help pages read {REFUND_CHECKED}.",
     _r_body.replace("__R52JS__", _R_JS),
     [{"@context": "https://schema.org", "@type": "WebApplication", "name": "AI subscription refund checker", "url": BASE + R_PATH, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": f"Refund windows, conditions and cancel steps for {_rn} AI subscriptions, from official help pages read {REFUND_CHECKED}."},
      {"@context": "https://schema.org", "@type": "ItemList", "name": "AI subscription refund policies", "url": BASE + R_PATH,
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{r["t"]} refund policy', "url": BASE + R_PATH + "#r-" + slug(r["t"])} for i, r in enumerate(REFUNDS)]},
      _ld_faq(_qa_r), crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Refunds and cancelling", R_PATH)])])
V52_CHANGED = [R_PATH]
def _v52ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if ' v52"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V52_CHANGED.append(path); return True
_RB = {r["t"]: r for r in REFUNDS}
for _r in REFUNDS:
    _line = f'<p class="pick small v52"><b>Refunds:</b> {e(_rshort(_r))} (checked {REFUND_CHECKED}) <a href="{R_PATH}?tool={slug(_r["t"])}#check">Refund and cancel steps →</a></p>'
    if not _v52ins(turl(_r["t"]), '<section class="card tbp"', _line): _v52ins(turl(_r["t"]), '<section class="verdict', _line)
for _x in COMPARISONS:
    _ns = [n for n in cnames(_x) if n in _RB]
    if len(_ns) >= 2:
        _v52ins(f"/compare/{_x[0]}.html", "</h1>", '<p class="small v52"><b>Refund rules:</b> ' + " · ".join((f'{e(n)}: {_rwin(_RB[n]["wm"])} refund window' if _RB[n]["k"] == "w" and _RB[n]["wm"] and _RB[n]["wm"] == _RB[n]["wy"] else f'{e(n)}: {_RK[_RB[n]["k"]].lower()}') for n in _ns) + f'. <a href="{R_PATH}?tool={slug(_ns[0])}#check">Check before you pay →</a></p>', after=True)
_R_LINE = f'<p class="small v52">Paid and changed your mind? <a href="{R_PATH}">Refund windows and cancel steps for {_rn} AI tools →</a></p>'
for _pp in ["/save-money.html", "/monthly-or-yearly.html", "/pay-less.html", "/renewal-reminders.html", "/subscription-audit.html", "/alternatives.html", "/ai-subscription-costs.html"]:
    _v52ins(_pp, "</h1>", _R_LINE, after=True)
_v52ins("/guides.html", "<h2>New guides</h2><ul>", f"<li class=\"v52\"><a href='{R_PATH}'>Can I get a refund? AI subscription refund and cancel rules</a></li>", after=True)
# Finder: a search that mentions refunds or cancelling shows a one-tap link (doesn't change results)
_RH = f'<p class="pick v52 rfhint" hidden><b>Want your money back?</b> <a id="rflink" href="{R_PATH}">Refund and cancel rules for {_rn} AI tools →</a></p>'
_h = open("public/index.html").read()
assert '<div id="out" aria-live="polite">' in _h
_RSL = json.dumps({r["t"].lower(): [slug(r["t"]), r["t"]] for r in REFUNDS})
open("public/index.html", "w").write(_h.replace('<div id="out" aria-live="polite">', _RH + '<style>.rfhint[hidden]{display:none!important}.rfhint{margin:var(--s3) auto;max-width:720px;text-align:left}</style><div id="out" aria-live="polite">' + '<script>(function(){const q=document.getElementById("q"),H=document.querySelector(".rfhint"),A=document.getElementById("rflink"),T=' + _RSL + ';if(!q||!H)return;const f=()=>{const v=q.value.toLowerCase(),m=/\\b(refunds?|refundable|money back|cancel(l?ing|l?ed|lation)?|unsubscribe)\\b/.test(v);H.hidden=!m;if(m){const k=Object.keys(T).find(n=>v.includes(n));A.href="' + R_PATH + '"+(k?"?tool="+T[k][0]+"#check":"");A.textContent=k?"Refund and cancel rules for "+T[k][1]+" →":"Refund and cancel rules for ' + str(_rn) + ' AI tools →"}};q.addEventListener("input",f);addEventListener("load",f);f()})()</script>', 1)); V52_CHANGED.append("/")
open("public/llms.txt", "a").write(f"\n## Refunds and cancelling (v52)\n- [Can I get a refund? AI subscription refund and cancel rules]({BASE}{R_PATH}): {_rn} AI tools ({', '.join(r['t'] for r in REFUNDS)}): refund window and conditions (monthly/yearly), how to ask, exact cancel steps, cancel-notice deadlines, what you lose after cancelling, app-store note, official refund and cancel page links, read {REFUND_CHECKED}. Checker params: ?tool=chatgpt&when=d7&bill=y (when = pre, h24, d2, d3, d7, d14, d30, old)\n" + "".join(f"  - {r['t']}: {_RK[r['k']]}. {_rshort(r)}\n" for r in REFUNDS))

# --- v54: Does this AI train on my data? Privacy checker (/ai-data-privacy.html) ---
# Facts read on each tool's official privacy / help / trust page on PRIVACY_CHECKED (tools.py PRIVACY, exact words in q).
PRIVACY_CHECKED = _tm0.PRIVACY_CHECKED; PRIVACY = sorted(_tm0.PRIVACY, key=lambda r: r["t"].lower()); PRIVACY_LEFT_OUT = _tm0.PRIVACY_LEFT_OUT
P_PATH = "/ai-data-privacy.html"
for _p in PRIVACY:
    assert _p["t"] in TOOL and _p["k"] in "yxcnu" and _p["bk"] in "nau" and _p["q"] and _p["src"].startswith("https://") and _p["ind"] and _p["biz"], _p["t"]
    if _p["k"] in "yc": assert _p["steps"], _p["t"]
_PK = {"y": "Trains by default", "x": "Trains, no opt-out found", "c": "Only if you allow it", "n": "Doesn't train by default", "u": "Unclear — see policy"}
_PB = {"n": "Protected by default", "a": "Admin decides", "u": "Unclear — see policy"}
_PORD = {"x": 0, "y": 1, "u": 2, "c": 3, "n": 4}; _BORD = {"u": 0, "a": 1, "n": 2}
def _pans(p):
    t = p["t"]
    return {"y": f"Yes, by default. {t} can train on your content, but you can turn it off.",
            "x": f"Yes. {t} may train on your content, and we found no way to opt out.",
            "c": f"Only if you allow it. {t} asks for your permission.",
            "n": f"No. {t} doesn't train on your content by default.",
            "u": f"Unclear — see policy. {t}'s official pages don't say what the default is."}[p["k"]]
def _pbans(p):
    t = p["t"]
    return {"n": f"No. {t}'s team and business plans are protected by default.",
            "a": f"It depends on your admin. {t} lets a team admin control it.",
            "u": f"Unclear — see policy. {t} doesn't state the business-plan default on the pages we read."}[p["bk"]]
def _psrc(p):
    a = [f'<a href="{e(p["src"])}" rel="noopener" target="_blank">official page<span class="skip"> for {e(p["t"])} (opens in a new tab)</span></a>']
    if p["sb"] and p["sb"] != p["src"]: a.append(f'<a href="{e(p["sb"])}" rel="noopener" target="_blank">business page<span class="skip"> for {e(p["t"])} (opens in a new tab)</span></a>')
    a += [f'<a href="{e(u)}" rel="noopener" target="_blank">{e(l)}<span class="skip"> for {e(p["t"])} (opens in a new tab)</span></a>' for l, u in p["more"]]
    return f'Checked {PRIVACY_CHECKED}: ' + " · ".join(a)
def _pdet(p, plan):
    a = [f'<li><b>{"Free and personal paid plans" if plan == "i" else "Team and business plans"}:</b> {e(p["ind"] if plan == "i" else p["biz"])}</li>']
    if plan == "i":
        a.append(f'<li><b>How to opt out:</b> {e(p["steps"]) if p["steps"] else ("Nothing to switch off." if p["k"] == "n" else "No opt-out setting found on the official pages we read.")}</li>')
    else:
        a.append(f'<li><b>On a personal plan instead:</b> {e(_PK[p["k"]])}.</li>')
    if p["keep"]: a.append(f'<li><b>How long it&#39;s kept:</b> {e(p["keep"])}</li>')
    if p["note"]: a.append(f'<li><b>Watch out:</b> {e(p["note"])}</li>')
    return '<ul class="p54l">' + "".join(a) + f'</ul><p class="small p54q">In their words: “{e(p["q"])}”</p><p class="small">{_psrc(p)}</p>'
_pn = len(PRIVACY); _pc = {k: sum(1 for p in PRIVACY if p["k"] == k) for k in "yxcnu"}
_pf = {"n": sum(1 for p in PRIVACY if p["k"] == "n"), "o": sum(1 for p in PRIVACY if p["steps"]), "b": sum(1 for p in PRIVACY if p["bk"] == "n")}
_PF = [("n", "Doesn't train by default"), ("o", "Opt-out available"), ("b", "Business plans protected")]
def _prow(p):
    s = slug(p["t"])
    return (f'<tr id="p-{s}" data-t="{e(p["t"].lower())}" data-k="{_PORD[p["k"]]}" data-b="{_BORD[p["bk"]]}" data-fn="{int(p["k"] == "n")}" data-fo="{int(bool(p["steps"]))}" data-fb="{int(p["bk"] == "n")}">'
            f'<th scope="row" data-l="Tool"><a href="{turl(p["t"])}">{e(p["t"])}</a></th>'
            f'<td data-l="Free & personal plans"><span class="p54b p54k{p["k"]}">{_PK[p["k"]]}</span><br>{e(p["ind"])}</td>'
            f'<td data-l="How to opt out">{e(p["steps"]) if p["steps"] else ("Nothing to switch off." if p["k"] == "n" else "No opt-out found.")}</td>'
            f'<td data-l="Team & business plans"><span class="p54b p54b{p["bk"]}">{_PB[p["bk"]]}</span><br>{e(p["biz"])}</td>'
            f'<td data-l="Source" class="small">{_psrc(p)} · <a href="{P_PATH}?tool={s}#check">Check {e(p["t"])}</a></td></tr>')
_p_opts = '<option value="">Choose a tool…</option>' + "".join(f'<option value="{slug(p["t"])}">{e(p["t"])}</option>' for p in PRIVACY)
_p_chips = (f'<button type="button" class="on" aria-pressed="true" data-f="">All {_pn}</button>' + "".join(f'<button type="button" aria-pressed="false" data-f="{k}">{l} ({_pf[k]})</button>' for k, l in _PF))
def _pjs(p): return {"s": slug(p["t"]), "t": p["t"], "k": p["k"], "bk": p["bk"], "a": _pans(p), "ab": _pbans(p), "di": _pdet(p, "i"), "db": _pdet(p, "b"), "u": turl(p["t"])}
_p_left = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)}.</li>' if n in TOOL else f'<li>{e(n)}: {e(w)}.</li>' for n, w in PRIVACY_LEFT_OUT)
_p_no = [p["t"] for p in PRIVACY if p["k"] == "n"]; _p_yes = [p["t"] for p in PRIVACY if p["k"] in "yx"]
_qa_p = [("Does ChatGPT train on my data?", f"On Free, Plus and Pro, OpenAI may use your chats to train its models unless you turn off “Improve the model for everyone” in Settings → Data controls. Temporary chats aren't used for training. ChatGPT Business, Enterprise and Edu aren't used for training by default. Checked {PRIVACY_CHECKED} on OpenAI's help center."),
         ("Does Claude train on my chats?", f"On Free, Pro and Max, Anthropic uses your chats for training only if you allow it in Settings → Privacy (or if you send feedback, or a chat is flagged for safety review). Claude Team, Enterprise and the API aren't used for training by default. Checked {PRIVACY_CHECKED} on Anthropic's privacy center."),
         ("Which AI tools don't train on my data by default?", f"Of the {_pn} tools we checked on {PRIVACY_CHECKED}: " + ", ".join(_p_no) + ". Claude and Descript only train if you allow it."),
         ("Which AI tools train on my data unless I opt out?", ", ".join(_p_yes) + f" (on free and personal paid plans). All except Runway show a setting to switch it off. Checked {PRIVACY_CHECKED}."),
         ("Are team and business plans safer?", "Usually. On most tools here, team, business and enterprise plans aren't used for training by default. A few leave it to your admin (Grammarly team accounts bought on the website start with training on), and a few don't say."),
         ("Does opting out delete what they already used?", "Not necessarily. Opting out stops future use. Perplexity says data collected before you switch it off can't be removed, and OpenAI says turning off training doesn't delete your saved chats. Delete chats separately if you want them gone.")]
_P_CSS = ("<style>.p54f{display:flex;flex-wrap:wrap;gap:var(--s3) var(--s5);align-items:flex-end}.p54f label{display:block;font-weight:600;margin-bottom:6px}.p54f select{font-size:1rem;min-height:48px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 10px;min-width:min(100%,240px)}.p54f>div{max-width:100%}"
          "#p54out{margin:var(--s4) 0;border-left:4px solid var(--mu)}#p54out h2{margin:0 0 6px;font-size:1.25rem}#p54out.p54ok{border-left-color:var(--ok)}#p54out.p54warn{border-left-color:var(--warn)}#p54msg:empty{display:none}"
          ".p54l{padding-left:18px;margin:6px 0}.p54l li{margin:4px 0}.p54q{font-style:italic}"
          ".p54b{display:inline-block;font-size:.75rem;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--sf2);color:var(--tx);margin-bottom:4px;border-left:4px solid var(--mu)}.p54kn,.p54bn{border-left-color:var(--ok)}.p54ky,.p54kx,.p54ku,.p54bu,.p54ba,.p54kc{border-left-color:var(--warn)}"
          ".p54tw table{min-width:900px}.p54tw th button{font:inherit;font-weight:600;background:none;border:0;color:var(--ac);cursor:pointer;min-height:44px;padding:0;text-align:left}.p54tw tr[hidden]{display:none}.p54tw td,.p54tw th{font-size:.9rem}"
          ".p54s{display:flex;flex-wrap:wrap;gap:var(--s3);align-items:center;margin:var(--s3) 0}.p54s input{min-height:48px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px;font-size:1rem;width:min(100%,320px)}"
          "@media(max-width:760px){.p54tw{overflow:visible;border:0;box-shadow:none;background:none}.p54tw table{min-width:0;display:block}.p54tw thead{display:none}.p54tw tbody,.p54tw tr{display:block}.p54tw tr{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);margin:0 0 var(--s3);padding:var(--s3)}.p54tw td,.p54tw th{display:block;border:0;padding:6px 4px}.p54tw td::before{content:attr(data-l);display:block;font-weight:700;font-size:.78rem;color:var(--mu);text-transform:uppercase;letter-spacing:.02em}.p54tw th[scope=row]{font-size:1.05rem}.p54tw th[scope=row] a{display:inline-flex;align-items:center;min-height:44px}}"
          ".p54tw td a{display:inline-block;min-height:24px;padding:10px 0}</style>")
_p_body = f"""{_P_CSS}<p class="small"><a href="/guides.html">Guides</a> › AI data privacy</p><h1>Does this AI train on my data?</h1>
<p class="tag">Pick a tool and your plan. We tell you in plain words whether it uses your chats, files or recordings to train its AI, and exactly how to switch it off. {_pn} AI tools, read on each official privacy or help page on {PRIVACY_CHECKED}.</p>
<div class="builder" id="check"><div class="p54f"><div><label for="p54t">Tool</label><select id="p54t">{_p_opts}</select></div>
<fieldset class="seg"><legend>Your plan</legend><input type="radio" name="p54p" id="p54pi" value="i" checked><label for="p54pi">Free or personal</label><input type="radio" name="p54p" id="p54pb" value="b"><label for="p54pb">Team or business</label></fieldset></div>
<div class="pick" id="p54out" aria-live="polite"><h2 id="p54h">Choose a tool to see if it trains on your data</h2><div id="p54d"><p class="small">Or scroll down: every tool is in the table below.</p></div><p class="small" style="margin:6px 0 0"><button type="button" class="bbtn" id="p54share">Copy link to this answer</button> <span id="p54msg" role="status"></span></p></div></div>
<p class="small">Policies change. We show what the official page said on {PRIVACY_CHECKED} and link to it. Not legal advice.</p>
<h2>What “training on your data” means</h2><ul>
<li><b>Training</b> means the company uses what you type, upload or record to improve its next AI models. Some also let staff read samples.</li>
<li><b>Opting out</b> usually only stops future use. It often doesn't delete what was already collected, and it doesn't delete your chat history.</li>
<li><b>Feedback buttons count.</b> On ChatGPT, Claude and Le Chat, a thumbs up or down can let them use that conversation even after you opt out.</li>
<li><b>Business plans</b> are usually protected by contract, but check: on some tools your admin decides.</li></ul>
<h2>All {_pn} tools at a glance</h2><div class="needs" role="group" aria-label="Show tools that" id="p54k">{_p_chips}</div>
<div class="p54s"><label for="p54q" class="skip">Search tools</label><input type="search" id="p54q" placeholder="Search a tool, e.g. Gemini" autocomplete="off"><span class="small" id="p54c" role="status">{_pn} tools</span></div>
<div class="tw p54tw" role="region" aria-label="AI data training table" tabindex="0"><table><caption class="skip">Does each AI tool train on your data, by plan. Checked {PRIVACY_CHECKED}.</caption><thead><tr><th scope="col" aria-sort="ascending"><button type="button" data-s="t">Tool</button></th><th scope="col"><button type="button" data-s="k">Free &amp; personal plans</button></th><th scope="col">How to opt out</th><th scope="col"><button type="button" data-s="b">Team &amp; business plans</button></th><th scope="col">Source</th></tr></thead>
<tbody id="p54rows">{"".join(_prow(p) for p in PRIVACY)}</tbody></table></div>
<h2>Not included yet</h2><p class="small">We leave a tool out when its official pages don't say it clearly (read {PRIVACY_CHECKED}):</p><ul class="small">{_p_left}</ul>
<p class="small">Related: <a href="/ai-refund-policies.html">Refund and cancel rules</a> · <a href="/ai-team-plans.html">Team plans by team size</a> · <a href="/alternatives.html">Alternatives to popular AI tools</a> · <a href="/tools.html">Browse all tools</a></p>
{_faq(_qa_p)}
<script>__P54JS__</script>"""
_P_JS = r"""(function(){const R=__DATA__,S=document.getElementById('p54t'),H=document.getElementById('p54h'),D=document.getElementById('p54d'),O=document.getElementById('p54out'),M=document.getElementById('p54msg'),Q=document.getElementById('p54q'),C=document.getElementById('p54c'),TB=document.getElementById('p54rows'),CH=[...document.querySelectorAll('#p54k button')],SB=[...document.querySelectorAll('.p54tw th button')];
const by={};R.forEach(r=>by[r.s]=r);let plan='i',f='',sk='t',dir=1;
function rows(){const q=(Q.value||'').trim().toLowerCase();const tr=[...TB.rows];let n=0;
tr.sort((a,b)=>{const x=sk=='t'?a.dataset.t.localeCompare(b.dataset.t):(+a.dataset[sk]-+b.dataset[sk])||a.dataset.t.localeCompare(b.dataset.t);return x*dir}).forEach(r=>TB.appendChild(r));
tr.forEach(r=>{const h=(f&&r.dataset['f'+f]!='1')||(q&&!r.dataset.t.includes(q));r.hidden=h;if(!h)n++});C.textContent=n+(n==1?' tool':' tools');
SB.forEach(b=>b.parentNode.setAttribute('aria-sort',b.dataset.s==sk?(dir>0?'ascending':'descending'):'none'));CH.forEach(b=>{const on=b.dataset.f==f;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)})}
function render(){const r=by[S.value];O.className='pick';M.textContent='';
if(!r){H.textContent='Choose a tool to see if it trains on your data';D.innerHTML='<p class="small">Or scroll down: every tool is in the table below.</p>'}
else{const k=plan=='b'?r.bk:r.k;O.classList.add(k=='n'?'p54ok':'p54warn');H.textContent=plan=='b'?r.ab:r.a;D.innerHTML=(plan=='b'?r.db:r.di)+'<p class="small"><a href="'+r.u+'">'+r.t+' tool page</a> · <a href="#p-'+r.s+'">See it in the table</a></p>'}
const u=new URLSearchParams();if(S.value)u.set('tool',S.value);if(plan=='b')u.set('plan','business');if(f)u.set('f',f);const s=u.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash);rows()}
const p=new URLSearchParams(location.search);if(by[p.get('tool')])S.value=p.get('tool');if(p.get('plan')=='business'){plan='b';document.getElementById('p54pb').checked=true}if('nob'.includes(p.get('f')||'x'))f=p.get('f');
S.addEventListener('change',render);document.querySelectorAll('input[name=p54p]').forEach(x=>x.addEventListener('change',()=>{plan=x.value;render()}));CH.forEach(b=>b.addEventListener('click',()=>{f=b.dataset.f;render()}));Q.addEventListener('input',rows);
SB.forEach(b=>b.addEventListener('click',()=>{if(sk==b.dataset.s)dir=-dir;else{sk=b.dataset.s;dir=1}rows()}));
document.querySelectorAll('#p54rows a[href*="?tool="]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();S.value=new URL(a.href).searchParams.get('tool');render();document.getElementById('check').scrollIntoView({block:'start'});S.focus()}));
document.getElementById('p54share').addEventListener('click',()=>{const t=location.href,ok=()=>{M.textContent='Link copied.'};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,()=>prompt('Copy this link:',t));else prompt('Copy this link:',t)});
render()})();"""
_P_JS = _P_JS.replace("__DATA__", json.dumps([_pjs(p) for p in PRIVACY], separators=(",", ":")).replace("</", "<\\/"))
page(P_PATH, f"Does This AI Train on My Data? Opt-Out Checker for {_pn} AI Tools ({PRIVACY_CHECKED[:4]}) | ToolPick",
     f"Does ChatGPT, Claude, Gemini, Copilot, Perplexity, Grammarly or Canva train on your chats and files? Plain answers by plan, exact opt-out steps and official sources for {_pn} AI tools, checked {PRIVACY_CHECKED}.",
     _p_body.replace("__P54JS__", _P_JS),
     [{"@context": "https://schema.org", "@type": "WebApplication", "name": "AI data training checker", "url": BASE + P_PATH, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": f"Whether {_pn} AI tools train on your content by default, how to opt out, and the team/business plan default, from official pages read {PRIVACY_CHECKED}."},
      {"@context": "https://schema.org", "@type": "ItemList", "name": "AI tools data training policies", "url": BASE + P_PATH,
       "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'Does {p["t"]} train on your data?', "url": BASE + P_PATH + "#p-" + slug(p["t"])} for i, p in enumerate(PRIVACY)]},
      _ld_faq(_qa_p), crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("AI data privacy", P_PATH)])])
V54_CHANGED = [P_PATH]
def _v54ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if ' v54"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V54_CHANGED.append(path); return True
for _p in PRIVACY:
    _line = (f'<p class="pick small v54"><b>Trains on your data?</b> Free &amp; personal plans: {e(_PK[_p["k"]].lower() if _p["k"] != "u" else "unclear, see policy")}. '
             f'Team &amp; business: {e(_PB[_p["bk"]].lower() if _p["bk"] != "u" else "unclear, see policy")}. (checked {PRIVACY_CHECKED}) <a href="{P_PATH}?tool={slug(_p["t"])}#check">{"Privacy details" if _p["k"] == "n" else "How to opt out"} →</a></p>')
    if not _v54ins(turl(_p["t"]), '<section class="card tbp"', _line): _v54ins(turl(_p["t"]), '<section class="verdict', _line)
_v54ins("/guides.html", "<h2>New guides</h2><ul>", f"<li class=\"v54\"><a href='{P_PATH}'>Does this AI train on my data? Opt-out checker for {_pn} AI tools</a></li>", after=True)
open("public/llms.txt", "a").write(f"\n## AI data privacy (v54)\n- [Does this AI train on my data?]({BASE}{P_PATH}): {_pn} AI tools: whether free/personal plans train on your content by default (yes / only if you allow / no / unclear), exact opt-out steps, team/business plan default, retention notes, official source links, read {PRIVACY_CHECKED}. Checker params: ?tool=chatgpt&plan=business; filters ?f=n (doesn't train by default), ?f=o (opt-out available), ?f=b (business plans protected)\n" + "".join(f"  - {p['t']}: personal plans: {_PK[p['k']]}; team/business: {_PB[p['bk']]}. {p['ind']}{(' Opt out: ' + p['steps']) if p['steps'] else ''} Source: {p['src']}\n" for p in PRIVACY) + "".join(f"  - Left out: {n} ({w})\n" for n, w in PRIVACY_LEFT_OUT))

# --- v55: AI budget planner — build my AI stack under $X/mo (/ai-budget-planner.html) ---
# Entry-plan prices re-read on each official pricing page on PLANNER_CHECKED (tools.py PLANNER_PRICES, words seen in the quote).
PLANNER_CHECKED = _tm0.PLANNER_CHECKED; PLANNER_PRICES = _tm0.PLANNER_PRICES; PLANNER_FREE = set(_tm0.PLANNER_FREE); PLANNER_LEFT_OUT = _tm0.PLANNER_LEFT_OUT
B_PATH = "/ai-budget-planner.html"
_BJOBS = [(s, l, c, list(r)) for s, l, c, r in list(JOBS) + list(_tm0.PLANNER_EXTRA_JOBS)]
_BJOBS = [_BJOBS[-1]] + _BJOBS[:-1]  # everyday assistant first
_BJ = {j[0]: j for j in _BJOBS}
_BCAT = {c["id"]: c["name"] for c in CATEGORIES}
for _n, _v in PLANNER_PRICES.items():
    assert _n in TOOL and len(_v) == 4 and (_v[1] or _v[2]) and _v[3], _n
for _n in PLANNER_FREE: assert _n in TOOL and realfree(TOOL[_n]), _n
_bnames = list(dict.fromkeys(n for j in _BJOBS for n in j[3]))
def _bc(x): return None if x is None else int(round(x * 100))
def _bcost(n, bill):
    p = PLANNER_PRICES.get(n)
    if not p: return None
    m, y = _bc(p[1]), _bc(p[2])
    if bill == "m": return m
    return min([v for v in (m, y) if v is not None])
def _bbill(n, bill):  # which billing the chosen price is
    p = PLANNER_PRICES[n]; m, y = _bc(p[1]), _bc(p[2])
    if bill == "m" or y is None or (m is not None and m <= y): return "m"
    return "y"
def _bopts(j, bill):
    o = []
    for i, n in enumerate(j[3]):
        c = _bcost(n, bill)
        if c is not None: o.append((n, i, "p", 2 * i, c))
    for i, n in enumerate(j[3]):
        if n in PLANNER_FREE: o.append((n, i, "f", 2 * i + 3, 0)); break
    o.append((None, -1, "x", 20, 0))
    return o
def _bsolve(js, bill):
    opts = [_bopts(_BJ[s], bill) for s in js]; best = {}; allc = [None]; cur = []
    def rec(k):
        if k == len(opts):
            paid = {}
            for o in cur:
                if o[2] == "p": paid[o[0]] = o[4]
            tot = sum(paid.values()); sc = sum(o[3] for o in cur)
            if tot not in best or sc < best[tot][0]: best[tot] = (sc, list(cur))
            if all(o[2] != "x" for o in cur) and (allc[0] is None or tot < allc[0][0] or (tot == allc[0][0] and sc < allc[0][1])): allc[0] = (tot, sc, list(cur))
            return
        for o in opts[k]:
            cur.append(o); rec(k + 1); cur.pop()
    rec(0)
    fr = []; mn = None
    for tot in sorted(best):
        sc, combo = best[tot]
        if mn is None or sc < mn: fr.append((tot, sc, combo)); mn = sc
    return fr, allc[0]
def _bmoney(c):
    return f"${c // 100:,}" if c % 100 == 0 else f"${c / 100:,.2f}"
def _bwhy(o):
    if o[2] == "x": return "Nothing fits this budget"
    if o[2] == "f": return f"Free plan of our #{o[1] + 1} pick"
    return f"Our #{o[1] + 1} pick, paid plan"
def _bjs_data():
    T = {}
    for n in _bnames:
        t = TOOL[n]; p = PLANNER_PRICES.get(n)
        T[n] = {"u": turl(n), "r": t["pricing"], "f": int(n in PLANNER_FREE), "fd": t["free"] if n in PLANNER_FREE else "",
                "p": p[0] if p else "", "m": _bc(p[1]) if p else None, "y": _bc(p[2]) if p else None, "q": p[3] if p else "",
                "per": _tm0.PLANNER_PER.get(n, ""), "no": _tm0.PLANNER_NOTES.get(n, "")}
    return {"J": [{"s": s, "l": l, "c": _BCAT[c], "t": r} for s, l, c, r in _BJOBS], "T": T, "d": PLANNER_CHECKED}
_BPRESETS = [("Student", ["everyday-assistant", "literature-review", "class-presentations", "grammar-checking", "chat-with-pdfs"]),
             ("Creator", ["youtube-shorts", "voiceovers", "social-media-graphics", "video-editing-beginners", "ai-music"]),
             ("Small business", ["everyday-assistant", "social-scheduling", "meeting-notes", "customer-support-bot", "product-photos", "email-assistant"]),
             ("Developer", ["everyday-assistant", "code-autocomplete", "code-review", "building-web-apps-no-code"])]
for _pn5, _pj in _BPRESETS: assert all(x in _BJ for x in _pj) and len(_pj) <= 6
_BDEF = (["everyday-assistant", "youtube-shorts", "meeting-notes", "social-media-graphics"], 2000, "m")
def _bprice_line(n, bill):
    p = PLANNER_PRICES[n]; t = TOOL[n]; b = _bbill(n, bill); per = _tm0.PLANNER_PER.get(n, "")
    if b == "m": s = f"{_bmoney(_bc(p[1]))}/mo billed monthly"
    else: s = f"{_bmoney(_bc(p[2]))}/mo billed yearly (about {_bmoney(int(round(_bc(p[2]) * 12 / 100.0)) * 100)} a year)"
    return s + (f", {per}" if per else "")
def _bcard_py(s, o, shared, bill):
    j = _BJ[s]; n = o[0]
    if o[2] == "x":
        alts = [(c, x) for x, c in ((x, _bcost(x, bill)) for x in j[3]) if c is not None]
        hint = f" Cheapest paid pick: {e(min(alts)[1])} at {_bmoney(min(alts)[0])}/mo." if alts else " None of our picks has a verified price for this billing."
        return (f'<li class="p55c p55x"><span class="p55j">{e(j[1])}</span><b class="p55t">No pick within budget</b>'
                f'<span class="small">None of our 3 picks has a free plan we could confirm.{hint} <a href="/best-ai-tool-for-{s}.html">See the picks</a></span></li>')
    t = TOOL[n]
    if o[2] == "f":
        badge = '<span class="badge b-free">Free plan</span>'; line = e(t["free"])
        src = f'Free plan confirmed {PLANNER_CHECKED} on the <a href="{e(t["pricing"])}" rel="noopener" target="_blank">official pricing page<span class="skip"> for {e(n)} (opens in a new tab)</span></a>'
    else:
        p = PLANNER_PRICES[n]
        badge = f'<span class="badge b-rank">{e(p[0])} plan</span>'; line = e(_bprice_line(n, bill)) + (f'. Note: {e(_tm0.PLANNER_NOTES[n])}' if n in _tm0.PLANNER_NOTES else "")
        src = f'Price checked {PLANNER_CHECKED} on the <a href="{e(t["pricing"])}" rel="noopener" target="_blank">official pricing page<span class="skip"> for {e(n)} (opens in a new tab)</span></a>: “{e(p[3])}”'
    sh = f'<span class="p55sh">Also covers: {e(", ".join(shared))}</span>' if shared else ""
    return (f'<li class="p55c{" p55f" if o[2] == "f" else ""}"><span class="p55j">{e(j[1])}</span><b class="p55t"><a href="{turl(n)}">{e(n)}</a> {badge}</b>'
            f'<span class="p55w">{_bwhy(o)} · {line}</span>{sh}<span class="small">{src}</span></li>')
def _bdefault_html():
    js, bud, bill = _BDEF; fr, _ = _bsolve(js, bill)
    pick = [f for f in fr if f[0] <= bud][-1]; tot, sc, combo = pick
    cards = []; seen = set()
    for s, o in zip(js, combo):
        sh = [_BJ[s2][1] for s2, o2 in zip(js, combo) if s2 != s and o2[2] == "p" and o[2] == "p" and o2[0] == o[0]]
        if o[2] == "p" and o[0] in seen: cards.append(_bcard_py(s, o, [], bill).replace('class="p55c"', 'class="p55c p55dup"', 1))
        else: cards.append(_bcard_py(s, o, sh, bill))
        if o[2] == "p": seen.add(o[0])
    return (f'<h2 id="p55h">Your AI stack: {_bmoney(tot)}/mo</h2><p class="p55sum">{_bsum(combo, len(js))} · {_bmoney(bud - tot)} left of your {_bmoney(bud)} budget · about {_bmoney(int(round(tot * 12 / 100.0)) * 100)} a year</p>'
            f'<ol class="p55list">{"".join(cards)}</ol>')
def _bsum(combo, n):
    cv = sum(1 for o in combo if o[2] != "x"); pd = sum(1 for o in combo if o[2] == "p"); fr = sum(1 for o in combo if o[2] == "f")
    return f"{cv} of {n} jobs covered ({pd} paid, {fr} free)"
# Static table: every job, the free option and cheapest verified paid plan of each pick (works without JavaScript)
def _bcell(n):
    a = [f'<a href="{turl(n)}">{e(n)}</a>']
    if n in PLANNER_FREE: a.append('<span class="badge b-free">Free plan</span>')
    p = PLANNER_PRICES.get(n)
    if p:
        bits = []
        if p[1] is not None: bits.append(f"{_bmoney(_bc(p[1]))}/mo monthly")
        if p[2] is not None: bits.append(f"{_bmoney(_bc(p[2]))}/mo yearly")
        a.append(f'<span class="small">{e(p[0])}: {" or ".join(bits)}</span>')
    else: a.append('<span class="small">Paid price not verified tonight</span>')
    return "<br>".join(a)
_b_rows = "".join(f'<tr id="j-{s}"><th scope="row" data-l="Job"><a href="/best-ai-tool-for-{s}.html">{e(l[:1].upper() + l[1:])}</a>' if s in {j[0] for j in JOBS} else f'<tr id="j-{s}"><th scope="row" data-l="Job">{e(l[:1].upper() + l[1:])}'
                  for s, l, c, r in [_BJOBS[0]]) + "</th>" + "".join(f'<td data-l="#{i + 1} pick">{_bcell(n)}</td>' for i, n in enumerate(_BJOBS[0][3][:3])) + "</tr>"
_b_rows += "".join(f'<tr id="j-{s}"><th scope="row" data-l="Job"><a href="/best-ai-tool-for-{s}.html">{e(l[:1].upper() + l[1:])}</a></th>' + "".join(f'<td data-l="#{i + 1} pick">{_bcell(n)}</td>' for i, n in enumerate(r[:3])) + "</tr>" for s, l, c, r in _BJOBS[1:])
_bcats = list(dict.fromkeys(c for s, l, c, r in _BJOBS))
_b_chips = "".join(f'<div class="p55g"><h3>{e(_BCAT[c])}</h3><div class="needs">' + "".join(f'<button type="button" aria-pressed="{"true" if s in _BDEF[0] else "false"}"{" class=\"on\"" if s in _BDEF[0] else ""} data-j="{s}">{e(l[:1].upper() + l[1:])}</button>' for s, l, c2, r in _BJOBS if c2 == c) + "</div></div>" for c in _bcats)
_b_presets = "".join(f'<button type="button" class="bbtn" data-p="{",".join(js)}">{e(n)}</button>' for n, js in _BPRESETS)
_b_quick = "".join(f'<button type="button" data-b="{v}">${v}</button>' for v in (0, 10, 20, 30, 50, 100))
_b_left = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: {e(w)}.</li>' if n in TOOL else f'<li>{e(n)}: {e(w)}.</li>' for n, w in PLANNER_LEFT_OUT)
_bnp = len(PLANNER_PRICES); _bnf = len(PLANNER_FREE); _bnj = len(_BJOBS)
_qa_b = [("What's the cheapest way to get good AI tools?", f"Start with free plans: {_bnf} of the tools we rank have a free plan we confirmed on {PLANNER_CHECKED}. Pick your jobs in the planner with a $0 budget to see a free-only stack, then raise the budget to see which single upgrade helps most."),
         ("How does the planner choose?", "For each job you pick, it looks at ToolPick's top 3 tools for that job. A paid plan of our #1 pick scores best, then #2 and #3, then free plans, then nothing. It tries every combination and returns the best one whose monthly total fits your budget. If one paid tool covers two of your jobs, you only pay for it once."),
         ("Are these prices current?", f"Every paid price was read on the tool's official pricing page on {PLANNER_CHECKED}, and each card quotes the words we saw. We use the cheapest paid (entry) plan. Taxes, add-on credits, promos for the first month and seat minimums aren't included. Prices change, so check the linked page before you buy."),
         ("What does “Yearly billing OK” change?", "Many tools are cheaper per month when you pay for a year up front. With yearly billing on, the planner uses the lower per-month price and shows what you'd pay for the year. Some plans are only sold yearly, so they only appear with this option on."),
         ("Why is a tool missing?", f"We leave a paid plan out when its official page didn't show a clear US-dollar price on {PLANNER_CHECKED}. The list is on this page under “Left out tonight”. The tool's free plan can still be used if we confirmed it."),
         ("Is ChatGPT in the planner?", f"Yes, its free plan is (unlimited text chats on GPT-6, with limits on other features, per OpenAI's pricing page on {PLANNER_CHECKED}). Its paid plans aren't, because the pricing page didn't show amounts to our check tonight. For a paid everyday assistant the planner can pick Le Chat Pro ($14.99/mo) or Claude Pro ($20/mo, or $17/mo yearly).")]
_B_CSS = ("<style>.p55step{font-size:1.15rem;margin:0 0 var(--s2)}.p55pre{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin:0 0 var(--s3)}.p55pre .bbtn{min-height:44px}.p55gs{columns:3 210px;column-gap:var(--s4)}.p55g{break-inside:avoid;padding-bottom:var(--s2)}@media(pointer:fine) and (min-width:761px){.p55g .needs button{min-height:36px}}"
          ".p55g h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mu);margin:var(--s2) 0 6px}.p55g .needs{display:flex;flex-wrap:wrap;gap:6px}.p55g .needs button{font-size:.88rem;padding:0 12px;min-height:44px;text-align:left}"
          ".needs button.on{background:var(--ac);color:var(--sf);border-color:var(--ac)}.needs button[aria-disabled=true]{opacity:.5}"
          ".p55row{display:flex;flex-wrap:wrap;gap:var(--s3) var(--s5);align-items:flex-end;margin-top:var(--s4)}.p55row label{display:block;font-weight:600;margin-bottom:6px}.p55bud{display:flex;align-items:center;gap:6px}.p55bud input{width:110px;min-height:48px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px;font-size:1.1rem}"
          ".p55q{display:flex;flex-wrap:wrap;gap:6px}.p55q button{min-height:44px;min-width:52px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;cursor:pointer}.p55q button.on{background:var(--ac);color:var(--sf);border-color:var(--ac)}"
          "#p55out{border-left:4px solid var(--ok)}#p55out h2{margin:0 0 4px;font-size:1.4rem}.p55sum{margin:0 0 var(--s3);color:var(--mu)}.p55list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--s3)}"
          ".p55c{display:flex;flex-direction:column;gap:4px;background:var(--sf2);border-radius:12px;padding:var(--s3) var(--s4);border-left:4px solid var(--ok)}.p55c.p55f{border-left-color:var(--ac)}.p55c.p55x{border-left-color:var(--warn)}.p55c.p55dup{border-left-color:var(--mu)}"
          ".p55j{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--mu)}.p55t{font-size:1.1rem}.p55t a{color:var(--tx)}.p55w{font-size:.95rem}.p55sh{font-size:.85rem;font-weight:600;color:var(--ok)}.p55c .small a{display:inline-block;min-height:24px}"
          ".p55up{margin:var(--s4) 0 0;padding:var(--s3) var(--s4);background:var(--sf2);border-radius:12px}.p55up p{margin:0 0 6px}.p55lad{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 0}@media(max-width:760px){.p55lad{flex-wrap:nowrap;overflow-x:auto;padding-bottom:6px}.p55lad button{flex:none;max-width:200px}}.p55lad button{min-height:44px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;font-size:.88rem;padding:4px 12px;cursor:pointer;text-align:left}.p55lad button.on{border-color:var(--ok);box-shadow:inset 0 0 0 1px var(--ok)}.p55lad b{display:block}"
          "#p55msg:empty{display:none}.p55act{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin-top:var(--s4)}.p55act .bbtn{min-height:44px}"
          ".p55tw table{min-width:760px}.p55tw td,.p55tw th{font-size:.9rem;vertical-align:top}"
          "@media(max-width:760px){.p55list{grid-template-columns:1fr}.p55tw{overflow:visible;border:0;box-shadow:none;background:none}.p55tw table{min-width:0;display:block}.p55tw thead{display:none}.p55tw tbody,.p55tw tr{display:block}.p55tw tr{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);margin:0 0 var(--s3);padding:var(--s3)}.p55tw td,.p55tw th{display:block;border:0;padding:6px 4px}.p55tw td::before{content:attr(data-l);display:block;font-weight:700;font-size:.78rem;color:var(--mu);text-transform:uppercase}.p55tw th[scope=row] a{display:inline-flex;align-items:center;min-height:44px}}"
          ".p55tw td a{display:inline-block;min-height:24px;padding:10px 0}</style>")
_b_body = f"""{_B_CSS}<p class="small"><a href="/guides.html">Guides</a> › AI budget planner</p><h1>Build my AI stack under $X a month</h1>
<p class="tag">Pick what you need AI for and how much you want to spend. We pick the best mix of ToolPick's top-ranked tools that fits your budget, count a tool once if it covers two jobs, and show the next upgrade worth paying for. {_bnp} paid plans and {_bnf} free plans, read on official pricing pages on {PLANNER_CHECKED}.</p>
<div class="builder" id="plan"><h2 class="p55step">1. What do you need AI for? <span class="small" id="p55n">(4 of 6 picked)</span></h2>
<div class="p55pre"><span class="small">Quick start:</span>{_b_presets}<button type="button" class="bbtn" id="p55clr">Clear</button></div>
<div class="p55gs" id="p55jobs">{_b_chips}</div>
<div class="p55row"><div><h2 class="p55step">2. Your monthly budget</h2><div class="p55bud"><label for="p55b" class="skip">Budget in US dollars per month</label><span aria-hidden="true">$</span><input type="number" id="p55b" min="0" max="1000" step="1" value="20" inputmode="numeric"><span class="small">/ month</span></div></div>
<div class="p55q" role="group" aria-label="Quick budgets">{_b_quick}</div>
<fieldset class="seg"><legend>Billing</legend><input type="radio" name="p55bill" id="p55bm" value="m" checked><label for="p55bm">Pay monthly</label><input type="radio" name="p55bill" id="p55by" value="y"><label for="p55by">Yearly billing OK</label></fieldset></div>
<div class="pick" id="p55out" aria-live="polite">{_bdefault_html()}<div id="p55more"></div></div>
<div class="p55act"><button type="button" class="bbtn" id="p55share">Copy link to this stack</button><button type="button" class="bbtn" id="p55copy">Copy as a list</button><span id="p55msg" class="small" role="status"></span></div></div>
<p class="small">Prices are each tool's entry paid plan in US dollars before tax, read on the official pricing page on {PLANNER_CHECKED}. First-month promos, add-on credits and team minimums aren't counted. Check the linked page before you buy. Rankings are ToolPick's job picks, <a href="/how-we-pick.html">how we pick</a>.</p>
<h2>How the planner picks</h2><ol><li>For each job, it looks at our top 3 tools for that job.</li><li>Best is a paid plan of our #1 pick, then #2, then #3. A confirmed free plan comes next, and “no pick” is last.</li><li>It tries every combination and keeps the best one that fits your budget. A tool that covers two of your jobs is only paid once.</li><li>It also shows the next upgrade, so you can see what an extra few dollars buys.</li></ol>
<h2>Every job: free plans and entry prices</h2><p class="small">All {_bnj} jobs with our top 3 picks. Checked {PLANNER_CHECKED}.</p>
<div class="tw p55tw" role="region" aria-label="Free plans and entry prices by job" tabindex="0"><table><caption class="skip">Free plan and cheapest verified paid plan for each of our top 3 picks per job, checked {PLANNER_CHECKED}.</caption><thead><tr><th scope="col">Job</th><th scope="col">#1 pick</th><th scope="col">#2 pick</th><th scope="col">#3 pick</th></tr></thead><tbody>{_b_rows}</tbody></table></div>
<h2>Left out tonight</h2><p class="small">Paid plans we didn't use because the official page wasn't clear on {PLANNER_CHECKED}. Their free plans can still appear if we confirmed them.</p><ul class="small">{_b_left}</ul>
<p class="small">Related: <a href="/stacks.html">AI stacks by role</a> · <a href="/help-me-choose.html">Help me choose</a> · <a href="/cost-calculator.html">AI cost calculator</a> · <a href="/free.html">Free AI tools</a> · <a href="/ai-team-plans.html">Team plans</a></p>
{_faq(_qa_b)}
<script>__P55JS__</script>"""
_B_SOLVER = r"""function p55opts(j,bill,T){const o=[];j.t.forEach((n,i)=>{const c=p55cost(T[n],bill);if(c!=null)o.push([n,i,'p',2*i,c])});for(let i=0;i<j.t.length;i++){if(T[j.t[i]].f){o.push([j.t[i],i,'f',2*i+3,0]);break}}o.push([null,-1,'x',20,0]);return o}
function p55cost(t,bill){if(bill=='m')return t.m;const v=[t.m,t.y].filter(x=>x!=null);return v.length?Math.min(...v):null}
function p55solve(js,bill,T){const opts=js.map(j=>p55opts(j,bill,T)),best=new Map(),cur=[];let all=null;
(function rec(k){if(k==opts.length){const paid={};cur.forEach(o=>{if(o[2]=='p')paid[o[0]]=o[4]});let tot=0;for(const n in paid)tot+=paid[n];let sc=0;cur.forEach(o=>sc+=o[3]);
const b=best.get(tot);if(!b||sc<b[0])best.set(tot,[sc,cur.slice()]);if(cur.every(o=>o[2]!='x')&&(!all||tot<all[0]||(tot==all[0]&&sc<all[1])))all=[tot,sc,cur.slice()];return}
for(const o of opts[k]){cur.push(o);rec(k+1);cur.pop()}})(0);
const fr=[];let mn=null;[...best.keys()].sort((a,b)=>a-b).forEach(t=>{const[sc,c]=best.get(t);if(mn==null||sc<mn){fr.push([t,sc,c]);mn=sc}});return[fr,all]}"""
_B_JS = r"""(function(){const D=__DATA__,J=D.J,T=D.T,by={};J.forEach(j=>by[j.s]=j);
__SOLVER__
const MAX=6,CH=[...document.querySelectorAll('#p55jobs button')],B=document.getElementById('p55b'),Q=[...document.querySelectorAll('.p55q button')],O=document.getElementById('p55out'),N=document.getElementById('p55n'),M=document.getElementById('p55msg');
let sel=__DEF__,bill='m',last='';
const X=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const $m=c=>'$'+(c%100==0?(c/100).toLocaleString('en-US'):(c/100).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
const yr=c=>$m(Math.round(c*12/100)*100);
const cap=s=>s.charAt(0).toUpperCase()+s.slice(1);
function why(o){return o[2]=='x'?'Nothing fits this budget':o[2]=='f'?'Free plan of our #'+(o[1]+1)+' pick':'Our #'+(o[1]+1)+' pick, paid plan'}
function bb(n){const t=T[n];return(bill=='m'||t.y==null||(t.m!=null&&t.m<=t.y))?'m':'y'}
function pl(n){const t=T[n],b=bb(n);return(b=='m'?$m(t.m)+'/mo billed monthly':$m(t.y)+'/mo billed yearly (about '+yr(t.y)+' a year)')+(t.per?', '+t.per:'')}
const ext=n=>' rel="noopener" target="_blank">official pricing page<span class="skip"> for '+X(n)+' (opens in a new tab)</span></a>';
function card(j,o,sh,dup){const n=o[0];
if(o[2]=='x'){const a=j.t.map(x=>[p55cost(T[x],bill),x]).filter(a=>a[0]!=null).sort((a,b)=>a[0]-b[0]);
return '<li class="p55c p55x"><span class="p55j">'+X(j.l)+'</span><b class="p55t">No pick within budget</b><span class="small">None of our 3 picks has a free plan we could confirm.'+(a.length?' Cheapest paid pick: '+X(a[0][1])+' at '+$m(a[0][0])+'/mo.':' None of our picks has a verified price for this billing.')+' <a href="/best-ai-tool-for-'+j.s+'.html">See the picks</a></span></li>'}
const t=T[n];let badge,line,src;
if(o[2]=='f'){badge='<span class="badge b-free">Free plan</span>';line=X(t.fd);src='Free plan confirmed '+D.d+' on the <a href="'+X(t.r)+'"'+ext(n)}
else{badge='<span class="badge b-rank">'+X(t.p)+' plan</span>';line=X(pl(n))+(t.no?'. Note: '+X(t.no):'');src='Price checked '+D.d+' on the <a href="'+X(t.r)+'"'+ext(n)+': “'+X(t.q)+'”'}
return '<li class="p55c'+(o[2]=='f'?' p55f':'')+(dup?' p55dup':'')+'"><span class="p55j">'+X(j.l)+'</span><b class="p55t"><a href="'+t.u+'">'+X(n)+'</a> '+badge+'</b><span class="p55w">'+why(o)+' · '+(dup?'Already paid for above, no extra cost':line)+'</span>'+(sh.length?'<span class="p55sh">Also covers: '+X(sh.join(', '))+'</span>':'')+'<span class="small">'+src+'</span></li>'}
function cards(js,combo){const seen=new Set();return js.map((j,i)=>{const o=combo[i],dup=o[2]=='p'&&seen.has(o[0]);const sh=dup||o[2]!='p'?[]:js.filter((j2,k)=>k!=i&&combo[k][2]=='p'&&combo[k][0]==o[0]).map(j2=>j2.l);if(o[2]=='p')seen.add(o[0]);return card(j,o,sh,dup)}).join('')}
function lab(o,j){return o[2]=='x'?'no pick':o[0]+(o[2]=='f'?' free':' '+T[o[0]].p)}
function render(){const js=sel.map(s=>by[s]),bud=Math.max(0,Math.round((+B.value||0)*100));
N.textContent='('+sel.length+' of '+MAX+' picked)';CH.forEach(b=>{const on=sel.includes(b.dataset.j);b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);b.setAttribute('aria-disabled',!on&&sel.length>=MAX)});
Q.forEach(b=>b.classList.toggle('on',+b.dataset.b*100==bud));
const u=new URLSearchParams();if(sel.length)u.set('jobs',sel.join(','));u.set('b',bud/100);if(bill=='y')u.set('bill','y');history.replaceState(null,'',location.pathname+'?'+u.toString()+location.hash);
if(!js.length){O.innerHTML='<h2 id="p55h">Pick at least one job above</h2><p class="p55sum">Or tap a quick start: Student, Creator, Small business or Developer.</p>';last='';return}
const[fr,all]=p55solve(js,bill,T);let pi=0;fr.forEach((f,i)=>{if(f[0]<=bud)pi=i});const[tot,sc,combo]=fr[pi],nx=fr[pi+1];
const cnt=(c,k)=>c.filter(o=>o[2]==k).length;
let h='<h2 id="p55h">Your AI stack: '+$m(tot)+'/mo</h2><p class="p55sum">'+(js.length-cnt(combo,'x'))+' of '+js.length+' jobs covered ('+cnt(combo,'p')+' paid, '+cnt(combo,'f')+' free) · '+$m(bud-tot)+' left of your '+$m(bud)+' budget · about '+yr(tot)+' a year</p><ol class="p55list">'+cards(js,combo)+'</ol>';
let up='';
if(nx){const d=js.map((j,i)=>[j,combo[i],nx[2][i]]).filter(a=>a[1][0]!=a[2][0]||a[1][2]!=a[2][2]),g=d.filter(a=>a[2][3]<a[1][3]).map(a=>X(a[0].l)+': '+X(lab(a[2]))+' instead of '+X(lab(a[1]))),w=d.filter(a=>a[2][3]>=a[1][3]).map(a=>X(a[0].l)+' moves to '+X(lab(a[2])));
up+='<p><b>Next upgrade: +'+$m(nx[0]-tot)+'/mo</b> (total '+$m(nx[0])+'/mo) upgrades '+g.join('; ')+(w.length?' (to fit, '+w.join('; ')+')':'')+'. <button type="button" class="bbtn" data-go="'+nx[0]+'" style="min-height:44px;margin-left:4px">Use '+$m(nx[0])+' budget</button></p>'}
else up+='<p><b>This is the best stack we can build for these jobs.</b> Spending more won\'t get a better-ranked pick.</p>';
if(all&&combo.some(o=>o[2]=='x'))up+='<p>Cheapest way to cover all '+js.length+' jobs: <b>'+$m(all[0])+'/mo</b>. <button type="button" class="bbtn" data-go="'+all[0]+'" style="min-height:44px;margin-left:4px">Use '+$m(all[0])+' budget</button></p>';
if(fr.length>1)up+='<p class="small" style="margin-top:8px">Price ladder for these jobs (tap to try):</p><div class="p55lad">'+fr.slice(0,10).map((f,i)=>'<button type="button" data-go="'+f[0]+'"'+(i==pi?' class="on" aria-current="true"':'')+'><b>'+(f[0]?$m(f[0])+'/mo':'Free')+'</b>'+X(i?'Paid: '+[...new Set(f[2].filter(o=>o[2]=='p').map(o=>o[0]))].join(', '):'Free plans only'+(cnt(f[2],'x')?' ('+cnt(f[2],'x')+' not covered)':''))+'</button>').join('')+'</div>';
O.innerHTML=h+'<div class="p55up">'+up+'</div>';
last='My AI stack ('+$m(tot)+'/mo, prices checked '+D.d+'):\n'+js.map((j,i)=>{const o=combo[i];return '- '+cap(j.l)+': '+(o[2]=='x'?'no pick':o[0]+(o[2]=='f'?' (free plan)':' '+T[o[0]].p+' ('+pl(o[0])+')'))}).join('\n')+'\nBuilt with ToolPick: '+location.href}
O.addEventListener('click',ev=>{const b=ev.target.closest('[data-go]');if(!b)return;B.value=+b.dataset.go/100;render();O.focus&&O.scrollIntoView({block:'nearest'})});
CH.forEach(b=>b.addEventListener('click',()=>{const s=b.dataset.j,i=sel.indexOf(s);if(i>=0)sel.splice(i,1);else if(sel.length<MAX)sel.push(s);else{M.textContent='You can pick up to '+MAX+' jobs. Remove one first.';return}M.textContent='';render()}));
document.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{sel=b.dataset.p.split(',');M.textContent='';render()}));
document.getElementById('p55clr').addEventListener('click',()=>{sel=[];render()});
B.addEventListener('input',render);Q.forEach(b=>b.addEventListener('click',()=>{B.value=b.dataset.b;render()}));
document.querySelectorAll('input[name=p55bill]').forEach(x=>x.addEventListener('change',()=>{bill=x.value;render()}));
const cp=(t,msg)=>{const ok=()=>{M.textContent=msg};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,()=>prompt('Copy this:',t));else prompt('Copy this:',t)};
document.getElementById('p55share').addEventListener('click',()=>cp(location.href,'Link copied.'));document.getElementById('p55copy').addEventListener('click',()=>{if(last)cp(last,'List copied.')});
const p=new URLSearchParams(location.search);if(p.get('jobs')!=null){sel=[...new Set(p.get('jobs').split(',').filter(s=>by[s]))].slice(0,MAX)}if(p.get('b')!=null&&!isNaN(+p.get('b')))B.value=Math.max(0,Math.min(1000,+p.get('b')));if(p.get('bill')=='y'){bill='y';document.getElementById('p55by').checked=true}
render()})();"""
_B_JS = (_B_JS.replace("__SOLVER__", _B_SOLVER).replace("__DEF__", json.dumps(_BDEF[0]))
         .replace("__DATA__", json.dumps(_bjs_data(), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")))
_bt = "/tmp/p55"; os.makedirs(_bt, exist_ok=True)
open(_bt + "/p55-solver.js", "w").write(_B_SOLVER + "\nmodule.exports={p55solve};\n")
open(_bt + "/p55-data.json", "w").write(json.dumps(_bjs_data()))
open(_bt + "/p55-py.json", "w").write(json.dumps({f"{','.join(js)}|{bill}": [[f[0], f[1], [o[0] for o in f[2]], [o[2] for o in f[2]]] for f in _bsolve(js, bill)[0]] for js in [p[1] for p in _BPRESETS] + [_BDEF[0], ["text-to-video", "ai-art", "product-photos", "code-review", "pitch-decks", "blog-seo"]] for bill in "my"}))
page(B_PATH, f"AI Budget Planner: Build Your AI Tool Stack Under $X a Month ({PLANNER_CHECKED[:4]}) | ToolPick",
     f"Pick what you need AI for and your monthly budget. Get the best mix of top-ranked AI tools that fits, with free plans, verified entry prices for {_bnp} paid plans (checked {PLANNER_CHECKED}) and the next upgrade worth paying for.",
     _b_body.replace("__P55JS__", _B_JS),
     [{"@context": "https://schema.org", "@type": "WebApplication", "name": "AI budget planner", "url": BASE + B_PATH, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": f"Builds the best AI tool stack for your jobs under a monthly budget from ToolPick's top-3 picks per job, using entry prices read on official pricing pages on {PLANNER_CHECKED}."},
      _ld_faq(_qa_b), crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("AI budget planner", B_PATH)])])
V55_CHANGED = [B_PATH]
def _v55ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if ' v55"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V55_CHANGED.append(path); return True
for _s, _l, _c, _r in JOBS:
    _v55ins(f"/best-ai-tool-for-{_s}.html", "<h2>Comparisons</h2>", f'<p class="pick small v55"><b>On a budget?</b> See the cheapest way to cover {e(_l)} plus your other AI jobs, with free plans and prices checked {PLANNER_CHECKED}. <a href="{B_PATH}?jobs={_s}&amp;b=20">Plan my AI budget →</a></p>')
_v55ins("/guides.html", "<h2>New guides</h2><ul>", f"<li class=\"v55\"><a href='{B_PATH}'>AI budget planner: build your AI stack under $X a month</a></li>", after=True)
_v55ins("/stacks.html", "<h2>FAQ</h2>", f'<p class="pick v55"><b>Got a budget?</b> Pick your jobs and a monthly limit, and we build the best stack that fits, with the next upgrade worth paying for. <a href="{B_PATH}">Open the AI budget planner →</a></p>')
_v55ins("/help-me-choose.html", "</main>", f'<p class="small v55">Need tools for several jobs on a budget? <a href="{B_PATH}">Try the AI budget planner</a>.</p>')
open("public/llms.txt", "a").write(f"\n## AI budget planner (v55)\n- [Build my AI stack under $X/mo]({BASE}{B_PATH}): pick up to 6 of {_bnj} jobs and a monthly budget; returns the best mix of ToolPick's top-3 picks per job that fits (paid #1 > #2 > #3 > confirmed free plan > none; a tool shared across jobs is paid once), the next upgrade and a price ladder. Params: ?jobs=youtube-shorts,meeting-notes&b=20&bill=y (yearly billing OK). Entry prices read on official pricing pages {PLANNER_CHECKED}:\n"
                                    + "".join(f"  - {n}: {p[0]}" + (f" ${p[1]}/mo monthly" if p[1] is not None else "") + (f" ${p[2]}/mo billed yearly" if p[2] is not None else "") + f" ({TOOL[n]['pricing']})\n" for n, p in sorted(PLANNER_PRICES.items()))
                                    + "  - Free plans confirmed: " + ", ".join(sorted(PLANNER_FREE)) + "\n" + "".join(f"  - Paid plan left out: {n} ({w})\n" for n, w in PLANNER_LEFT_OUT))

# --- v56: Real cost of AI images (/ai-image-cost.html): images per plan and $ per image, from official pricing pages (tools.py IMAGE_COSTS) ---
import math as _math
IMG = _tm0.IMAGE_COSTS; IMAGE_CHECKED = _tm0.IMAGE_CHECKED; I_PATH = "/ai-image-cost.html"
def _icap(c, r): return int(c / r + 1e-9)
def _icost(t, r, need, slow):
    best = None
    for pn, p, c, sl, tp in t["plans"]:
        cap = _icap(c, r)
        if need <= cap: cand = (p, "fits", 0)
        elif slow and sl: cand = (p, "slow", 0)
        elif tp: k = _math.ceil((need * r - c) / tp[0] - 1e-9); cand = (round(p + k * tp[1], 2), "top", k)
        else: continue
        if best is None or cand[0] < best["usd"] - 1e-9: best = dict(plan=pn, price=p, cr=c, usd=cand[0], how=cand[1], k=cand[2], cap=cap, tp=tp)
    return best
def _m(v): return "$" + (f"{v:,.0f}" if abs(v - round(v)) < 1e-9 else f"{v:,.2f}")
def _m3(v): return "$" + (f"{v:.3f}" if v < 0.1 else f"{v:.2f}")
_idata = [dict(n=n, s=slug(n), u=turl(n), un=v["unit"], tn=v["top_note"], sn=v["slow_note"],
               pl=[dict(n=a, p=b, c=c, sl=d, tp=list(x) if x else None) for a, b, c, d, x in v["plans"]],
               md=[dict(n=a, r=round(b, 5), k=k) for a, b, k in v["models"]]) for n, v in IMG.items()]
_IJSON = json.dumps(_idata, separators=(",", ":")).replace("</", "<\\/")
I_DEF = dict(keep=100, tries=4, slow=False)
def _idesc(t, md, c, keep, need):
    if c is None: return f'<p class="vc-big">More than the biggest plan</p><p class="small" style="margin:0">Needs {need:,} images of {e(md[0])}; the biggest plan covers about {_icap(t["plans"][-1][2], md[1]):,}. Extra: {e(t["top_note"])}.</p>'
    if c["how"] == "fits": how = f'{e(c["plan"])} plan ({c["cr"]:,} {e(t["unit"])})' if c["price"] else f'{e(c["plan"])}'
    elif c["how"] == "slow": how = f'{e(c["plan"])} plan: about {c["cap"]:,} fast images, the rest in unlimited slow mode'
    else: how = (f'{e(c["plan"])} plan {_m(c["price"])} + ' if c["price"] else "Pay as you go: ") + (f'{c["k"]:,} × {c["tp"][0]:,} extra {e(t["unit"])} at {_m(c["tp"][1])}' if c["tp"][0] > 1 else f'{round(need * md[1]):,} credits at {_m(c["tp"][1])}')
    return f'<p class="vc-big">{_m(c["usd"])}/mo</p><p class="small" style="margin:0">{how} · <b>{_m3(c["usd"] / keep)} per image you keep</b></p>'
_icards = ""
for n, v in IMG.items():
    md = v["models"][0]; c = _icost(v, md[1], I_DEF["keep"] * I_DEF["tries"], I_DEF["slow"])
    _icards += (f'<article class="card i56c" id="ic-{slug(n)}"><h3 style="margin:0"><a href="{turl(n)}">{e(n)}</a></h3><p class="small" style="margin:2px 0 8px">Free: {e(v["free"])} · '
                f'<a href="{e(v["src"])}" rel="noopener" target="_blank">official pricing<span class="skip"> for {e(n)} (opens in a new tab)</span></a></p>'
                f'<label for="im-{slug(n)}">Model</label><select id="im-{slug(n)}" style="width:100%">' + "".join(f'<option value="{i}">{e(a)}</option>' for i, (a, b, k) in enumerate(v["models"])) + '</select>'
                f'<div id="io-{slug(n)}" aria-live="polite">{_idesc(v, md, c, I_DEF["keep"], I_DEF["keep"] * I_DEF["tries"])}</div><p class="small" style="margin:6px 0 0">{e(v["per_note"])}</p></article>')
_irows = ""
def _icell(pn, p, c, r, tp):
    if not c: return f"{e(pn)}: {_m3(r * tp[1])}/image" if tp else ""
    k = _icap(c, r); return f"{e(pn)} {_m(p)}/mo: <b>{k:,}</b> <span class=small>({_m3(p / k)} each)</span>" if k else f"{e(pn)} {_m(p)}/mo: 0"
for n, v in IMG.items():
    for a, r, k in v["models"]:
        _irows += f"<tr><th scope='row'><a href='{turl(n)}'>{e(n)}</a></th><td>{e(a)}</td><td>{r:.3g} {e(v['unit'])}</td><td>" + "<br>".join(_icell(pn, p, c, r, tp) for pn, p, c, sl, tp in v["plans"]) + "</td></tr>"
_iplans = " · ".join(f"<b>{e(n)}</b>: " + ", ".join(f"{e(a)} {_m(b)}/mo ({c:,} {e(v['unit'])})" if b else f"{e(a)} (1¢ per credit)" for a, b, c, d, x in v["plans"]) for n, v in IMG.items())
_iflat = "".join(f'<li><a href="{turl(n)}">{e(n)}</a> {e(p)}, {_m(pr)}/mo: {e(q)} (<a href="{e(u)}" rel="noopener" target="_blank">source<span class="skip"> for {e(n)} (opens in a new tab)</span></a>).</li>' for n, p, pr, q, u in _tm0.IMAGE_FLAT)
_ileft = "".join(f"<li><a href='{turl(n)}'>{e(n)}</a>: {e(r)}.</li>" for n, r in _tm0.IMAGE_LEFT_OUT)
_isrc = "".join(f'<li><a href="{turl(n)}">{e(n)}</a>: <a href="{e(v["src"])}" rel="noopener" target="_blank">pricing page<span class="skip"> for {e(n)} (opens in a new tab)</span></a>' + (f' and <a href="{e(v["src2"])}" rel="noopener" target="_blank">credit costs<span class="skip"> for {e(n)} (opens in a new tab)</span></a>' if v.get("src2") else "") + f". {e(v['per_note'])}</li>" for n, v in IMG.items())
I_JS = r'''(function(){const D=__ID__;const $=id=>document.getElementById(id);
const M=v=>'$'+(Math.abs(v-Math.round(v))<1e-9?Math.round(v).toLocaleString('en-US'):v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
const M3=v=>'$'+(v<0.1?v.toFixed(3):v.toFixed(2));const X=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cap=(c,r)=>Math.floor(c/r+1e-9);
function cost(t,r,need,slow){let b=null;t.pl.forEach(p=>{const k0=cap(p.c,r);let c;if(need<=k0)c=[p.p,'fits',0];else if(slow&&p.sl)c=[p.p,'slow',0];else if(p.tp){const k=Math.ceil((need*r-p.c)/p.tp[0]-1e-9);c=[Math.round((p.p+k*p.tp[1])*100)/100,'top',k]}else return;
if(!b||c[0]<b.usd-1e-9)b={p:p,usd:c[0],how:c[1],k:c[2],cap:k0}});return b}
const q=new URLSearchParams(location.search);const sel={};D.forEach(t=>sel[t.s]=0);
(q.get('m')||'').split(',').forEach(x=>{const [s,i]=x.split(':');const t=D.find(y=>y.s==s);if(t&&t.md[+i])sel[s]=+i});
const qk=parseInt(q.get('n')),qt=parseInt(q.get('t'));if(qk>0&&qk<=100000)$('ic-keep').value=qk;if([1,2,4].includes(qt))$('ic-try').value=qt;if(q.get('slow')=='1')$('ic-slow1').checked=true;
D.forEach(t=>{const s=$('im-'+t.s);s.value=sel[t.s];s.addEventListener('change',()=>{sel[t.s]=+s.value;go()})});
function go(){const keep=Math.max(1,Math.min(100000,parseInt($('ic-keep').value)||0)),tries=parseInt($('ic-try').value),slow=$('ic-slow1').checked,need=keep*tries;const R=[];
D.forEach(t=>{const m=t.md[sel[t.s]],c=cost(t,m.r,need,slow);R.push({t,m,c});let h;
if(!c){const big=t.pl[t.pl.length-1];h='<p class="vc-big">More than the biggest plan</p><p class="small" style="margin:0">Needs '+need.toLocaleString()+' images of '+X(m.n)+'; the biggest plan covers about '+cap(big.c,m.r).toLocaleString()+'. Extra: '+X(t.tn)+'.</p>'}
else{let how;if(c.how=='fits')how=c.p.p?X(c.p.n)+' plan ('+c.p.c.toLocaleString()+' '+t.un+')':X(c.p.n);else if(c.how=='slow')how=X(c.p.n)+' plan: about '+c.cap.toLocaleString()+' fast images, the rest in unlimited slow mode';
else how=(c.p.p?X(c.p.n)+' plan '+M(c.p.p)+' + ':'Pay as you go: ')+(c.p.tp[0]>1?c.k.toLocaleString()+' × '+c.p.tp[0].toLocaleString()+' extra '+t.un+' at '+M(c.p.tp[1]):Math.round(need*m.r).toLocaleString()+' credits at '+M(c.p.tp[1]));
h='<p class="vc-big">'+M(c.usd)+'/mo</p><p class="small" style="margin:0">'+how+' · <b>'+M3(c.usd/keep)+' per image you keep</b></p>'}
$('io-'+t.s).innerHTML=h});
const g={};R.forEach(r=>{if(r.m.k)(g[r.m.k]=g[r.m.k]||[]).push(r)});let v=[];
Object.values(g).filter(a=>a.length>1).forEach(a=>{const ok=a.filter(r=>r.c).sort((x,y)=>x.c.usd-y.c.usd);if(ok.length<2)return;const w=ok[0],n=ok[1];
const nm={'ideogram-4-turbo':'Ideogram 4.0 Turbo','recraft-v41-flash':'Recraft V4.1 Flash'}[w.m.k];v.push(w.c.usd==n.c.usd?'Same model ('+nm+'): '+X(w.t.n)+' and '+X(n.t.n)+' cost the same, '+M(w.c.usd)+'/mo.':'Same model ('+nm+'): <b>'+X(w.t.n)+' is cheaper</b> at '+M(w.c.usd)+'/mo vs '+X(n.t.n)+' at '+M(n.c.usd)+'/mo.')});
const ok=R.filter(r=>r.c).sort((x,y)=>x.c.usd-y.c.usd);
if(ok.length){const w=ok[0];v.unshift('For '+need.toLocaleString()+' images a month ('+keep.toLocaleString()+' kept × '+tries+' tr'+(tries==1?'y':'ies')+'), the lowest bill with the models picked is <b>'+X(w.t.n)+' ('+X(w.m.n)+') at '+M(w.c.usd)+'/mo</b>. Different models differ in quality and style, so that part isn\u2019t like for like.')}
if(!v.length)v.push('Pick the same model in two cards to compare like for like.');
else if(!Object.values(g).some(a=>a.length>1))v.push('<span class="small">Pick the same model in two cards (Ideogram 4.0 Turbo in Ideogram and Krea, or Recraft V4.1 Flash in Recraft and Krea) to compare like for like.</span>');
$('ic-verdict').innerHTML=v.join('<br>');history.replaceState(null,'','?n='+keep+'&t='+tries+(slow?'&slow=1':'')+'&m='+D.map(t=>t.s+':'+sel[t.s]).join(','))}
['ic-keep','ic-try'].forEach(i=>{$(i).addEventListener('input',go);$(i).addEventListener('change',go)});document.querySelectorAll('input[name=ic-slow]').forEach(x=>x.addEventListener('change',go));
$('ic-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);$('ic-st').textContent='Link copied.'}catch(e){$('ic-st').textContent='Copy this link: '+location.href}});
document.querySelectorAll('[data-ip]').forEach(b=>b.addEventListener('click',()=>{const [n,t,s]=b.dataset.ip.split('|');$('ic-keep').value=n;$('ic-try').value=t;$(s=='1'?'ic-slow1':'ic-slow0').checked=true;go()}));
go()})();'''
_ipre = [("50 images, every one a keeper", "50|1|0"), ("100 keepers from 4 tries each", "100|4|0"), ("500 a month, can wait", "500|4|1"), ("2,000 a month, fast", "2000|1|0")]
_i_qa = [("How much does one AI image cost?", f"On the entry plans we checked on {IMAGE_CHECKED}, from well under 1 cent (Krea 2 Turbo on Krea Basic: about 2,500 images for $9) to about 14 cents (Recraft V4.1 Pro Vector on Recraft Basic: 83 images for $12). The calculator works out your own cost from how many images you keep and how many tries each one takes."),
         ("How many images do I get with Midjourney Basic?", "Midjourney Basic ($10/mo) gives 200 minutes of Fast GPU time. One standard (SD) prompt makes 4 images and uses about 0.8 minutes, so that's about 250 prompts or 1,000 images a month, or about 615 HD images. Midjourney says these are approximate."),
         ("Which AI image plans are unlimited?", "Some plans let you keep generating in a slower queue after your fast credits run out: Ideogram Plus ($20/mo, unlimited slow credits), Midjourney Standard ($30/mo, unlimited Relax images), Leonardo Premium ($30/mo, unlimited relaxed images on selected models) and Krea Max ($105/mo, unlimited relaxed with supported in-house models). Choose “I can wait” in the calculator to count them."),
         ("Is pay as you go cheaper than a subscription?", "For small amounts it can be. Ideogram's pay-as-you-go rate is 1¢ per credit, so 300 Ideogram 4.0 Turbo images (3 credits each) cost about $9, less than Plus at $20/mo. Above about 2,000 credits a month, Plus is cheaper, and it adds unlimited slow generation."),
         ("Why do two tools charge differently for the same model?", f"Krea, Recraft and others resell models like Ideogram 4.0 and Recraft V4.1 Flash. Each sets its own credit price, so we compare them only when the same model is picked in both cards. Prices checked {IMAGE_CHECKED} on each official page.")]
_i_body = f"""<style>.vc-big{{font-size:1.5rem;font-weight:800;margin:10px 0 2px}}.vc-in{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));align-items:end}}.vc-in input[type=number],.vc-in select{{width:100%}}.i56pre{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}}.i56pre button{{min-height:44px}}.i56tw table{{min-width:600px}}.i56tw td,.i56tw th{{font-size:.9rem;vertical-align:top}}.seg.i56s{{margin:0}}</style>
<p class="small"><a href="/save-money.html">Save money</a> › Real cost of AI images</p><h1>What does an AI image really cost?</h1>
<p class="tag">AI image plans are sold in credits, GPU minutes or units, and every model uses a different amount per image. Tell us how many images you need a month and see which plan of Midjourney, Ideogram, Recraft and Krea you'd actually need, and the real price per image, from each tool's official pricing page (checked {IMAGE_CHECKED}).</p>
<div class="builder"><div class="i56pre" role="group" aria-label="Quick examples"><span class="small" style="align-self:center">Try:</span>{''.join(f'<button type="button" class="bbtn" data-ip="{v}">{e(l)}</button>' for l, v in _ipre)}</div>
<div class="vc-in"><div><label for="ic-keep">Images you keep per month</label><input id="ic-keep" type="number" inputmode="numeric" min="1" max="100000" value="{I_DEF['keep']}"></div>
<div><label for="ic-try">Images generated per keeper</label><select id="ic-try"><option value="1">1 (every image is a keeper)</option><option value="2">2</option><option value="4" selected>4 (one Midjourney grid)</option></select></div>
<fieldset class="seg i56s"><legend>Speed</legend><input type="radio" name="ic-slow" id="ic-slow0" value="0" checked><label for="ic-slow0">I need them fast</label><input type="radio" name="ic-slow" id="ic-slow1" value="1"><label for="ic-slow1">I can wait (slow mode)</label></fieldset>
<div><button type="button" class="bbtn" id="ic-copy">Copy link to this result</button> <span id="ic-st" class="small" role="status"></span></div></div>
<p id="ic-verdict" class="pick" aria-live="polite" style="margin-top:12px">Pick the same model in two cards to compare like for like.</p></div>
<h2>Your result by tool</h2><div class="grid">{_icards}</div>
<p class="small">Monthly billing, before tax. The plan shown is the cheapest way to get your images: a plan, a plan plus top-ups (only where the top-up price is on the official page), or unlimited slow mode if you picked “I can wait”.</p>
<h2>How many images each plan buys</h2><p class="small">Fast (priority) images per month, using all of a plan's monthly credits on one model. Credit costs and plan sizes copied from each official page on {IMAGE_CHECKED}. “$/image” is the plan price divided by the images it buys.</p>
<div class="tw i56tw" role="region" aria-label="Images per plan" tabindex="0"><table><thead><tr><th scope="col">Tool</th><th scope="col">Model</th><th scope="col">Uses per image</th><th scope="col">Fast images per month, by plan (monthly billing)</th></tr></thead><tbody>{_irows}</tbody></table></div>
<p class="small">Plans (monthly billing): {_iplans}.</p>
<h2>If you can wait: plans with unlimited slow images</h2><p>After the fast credits run out, these plans keep generating images in a slower queue at no extra cost, so a heavy month costs the same as a light one:</p><ul>{_iflat}</ul>
<h2>How we compare</h2><ul><li><b>Same unit.</b> Every plan is turned into images per month for the model you pick.</li><li><b>Same model for “cheaper”.</b> We only say one tool is cheaper when both run the same model (Ideogram 4.0 Turbo is on Ideogram and Krea; Recraft V4.1 Flash is on Recraft and Krea). Krea doesn't state the resolution for Ideogram 4.0; Ideogram's own rate is for 2K.</li><li><b>Monthly billing only.</b> Yearly plans are cheaper per month but paid up front; see <a href="/monthly-or-yearly.html">Monthly or yearly?</a></li><li><b>Only what the pages show.</b> Top-ups are added only where the price is on the official page (Midjourney $4 per GPU hour, Recraft $2 per 200 credits, Ideogram pay as you go at 1¢ per credit). Otherwise we say “More than the biggest plan” instead of guessing.</li><li><b>Approximate.</b> Midjourney's GPU minutes per prompt are its own averages; Krea's counts are rounded on its page. Editing, upscaling and reference images cost extra on most tools.</li></ul>
<h2>Sources (checked {IMAGE_CHECKED})</h2><ul class="small">{_isrc}</ul>
<h2>Tools left out</h2><ul>{_ileft}</ul>
{_faq(_i_qa)}
<p class="small">Related: <a href="/best-ai-images-tools.html">Best AI image tools</a> · <a href="/best-free-ai-images-tools.html">Free AI image tools</a> · <a href="/my-ai-costs.html#video">Real cost of AI video</a> · <a href="/my-ai-costs.html#voice">Real cost of AI voice</a> · <a href="/ai-budget-planner.html">AI budget planner</a> · <a href="/how-we-pick.html">How we pick</a></p>
<script>{I_JS.replace("__ID__", _IJSON)}</script>"""
page(I_PATH, f"AI Image Cost Calculator: Price per Image for Midjourney, Ideogram, Recraft, Krea ({IMAGE_CHECKED[:4]}) | ToolPick",
     f"How many images each Midjourney, Ideogram, Recraft and Krea plan really buys, the real price per image, and which plans are unlimited in slow mode. From official pricing pages, checked {IMAGE_CHECKED}.",
     _i_body, [{"@context": "https://schema.org", "@type": "WebApplication", "name": "AI image cost calculator", "url": BASE + I_PATH, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": f"Works out which Midjourney, Ideogram, Recraft or Krea plan you need for a number of images a month and the real price per image, from official credit costs checked {IMAGE_CHECKED}."},
      _ld_faq(_i_qa), crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Real cost of AI images", I_PATH)])])
V56_CHANGED = [I_PATH]
def _v56ins(path, marker, html, after=False):
    _fp = "public" + path
    if not os.path.exists(_fp): return False
    _h = open(_fp).read()
    if ' v56"' in _h or marker not in _h: return False
    open(_fp, "w").write(_h.replace(marker, (marker + html) if after else (html + marker), 1)); V56_CHANGED.append(path); return True
for _n in list(IMG) + ["Leonardo", "Magnific"]:
    _v56ins(turl(_n), '<section class="card tbp"', f'<p class="pick v56"><b>How many images will you get?</b> See what each {e(_n)} plan really buys and the price per image, next to other image tools: <a href="{I_PATH}">Real cost of AI images →</a></p>')
_v56ins("/best-ai-images-tools.html", "</h1>", f'<p class="pick v56">Image plans are sold in credits. <a href="{I_PATH}">See what an AI image really costs per plan →</a></p>', after=True)
_v56ins("/best-free-ai-images-tools.html", "</h1>", f'<p class="pick v56">Outgrowing a free plan? <a href="{I_PATH}">See the real price per image on paid plans →</a></p>', after=True)
for _js in ["ai-art", "logos-text-in-images", "social-media-graphics", "product-photos"]:
    _v56ins(f"/best-ai-tool-for-{_js}.html", "<h2>Comparisons</h2>", f'<p class="pick small v56"><b>Need lots of images?</b> Compare the real price per image and plans with unlimited slow mode: <a href="{I_PATH}">Real cost of AI images →</a></p>')
for _cs in ["midjourney-vs-leonardo", "midjourney-vs-ideogram", "midjourney-vs-krea", "leonardo-vs-ideogram", "ideogram-vs-recraft", "canva-vs-recraft"]:
    _v56ins(f"/compare/{_cs}.html", "</h1>", f'<p class="small v56">How many images does each plan buy? <a href="{I_PATH}">Real cost of AI images →</a></p>', after=True)
_v56ins("/guides.html", "<h2>New guides</h2><ul>", f"<li class=\"v56\"><a href='{I_PATH}'>Real cost of AI images: price per image for Midjourney, Ideogram, Recraft and Krea</a></li>", after=True)
V56_CHANGED.append("/save-money.html")
open("public/llms.txt", "a").write(f"\n## Real cost of AI images (v56)\n- [AI image cost calculator]({BASE}{I_PATH}): images per month you keep x tries per keeper -> cheapest plan (plan, plan + top-ups where priced, or unlimited slow mode if ?slow=1) and $ per kept image for Midjourney, Ideogram, Recraft, Krea; same-model 'cheaper' verdicts only (Ideogram 4.0 Turbo, Recraft V4.1 Flash). Params: ?n=100&t=4&slow=1&m=midjourney:0,ideogram:0,recraft:1,krea:5. Official pages checked {IMAGE_CHECKED}:\n"
    + "".join(f"  - {n} ({v['src']}): " + "; ".join(f"{a} ${b}/mo {c:,} {v['unit']}" + (" + unlimited slow" if d else "") for a, b, c, d, x in v["plans"]) + ". Per image: " + "; ".join(f"{a} {r:.3g} {v['unit']}" for a, r, k in v["models"]) + f". Extra: {v['top_note']}.\n" for n, v in IMG.items())
    + "".join(f"  - Left out: {n} ({w})\n" for n, w in _tm0.IMAGE_LEFT_OUT))

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
_lm["/tools.html"] = DIR_DATE
_lm["/stacks.html"] = STACK_BUILD_DATE
_lm[PAYLESS_PATH] = PAYLESS_DATE
_lm[MY_PATH] = MY_DATE
_lm["/save-money.html"] = "2026-10-20"
_lm["/ai-video-cost.html"] = VIDEO_CHECKED
_lm["/ai-voice-cost.html"] = VOICE_CHECKED
_lm["/how-we-pick.html"] = HWP_DATE
_lm["/renewal-reminders.html"] = RR_DATE
_lm["/embed.html"] = EMBED_DATE
_lm[TEAM_PATH] = TEAM_CHECKED
PC_BUILD_DATE = "2026-10-20"  # tracker page + its tool-page boxes redesigned (v18)
_lm["/price-changes.html"] = max(_pc_latest, PC_BUILD_DATE)
for _n in CHANGES_BY_TOOL: _lm[turl(_n)] = max(_lm.get(turl(_n), CHECKED), PC_BUILD_DATE)
for _r in ROLES:
    _lm[role_path(_r[0])] = max(x.get("checked", CHECKED) for b in ROLE_DATA[_r[0]] for c, t, al in ROLE_DATA[_r[0]][b] for x in [t] + al)
# --- v39: simplification pass (one nav, one costs page, collapsed details, fewer boxes) ---
import re as _re, os as _os, glob as _glob
V39_DATE = "2026-10-20"
MERGED = [("audit", "/subscription-audit.html", "Subscription audit"), ("watchlist", "/watchlist.html", "Watchlist"),
          ("reminders", "/renewal-reminders.html", "Renewal reminders"), ("calculator", "/cost-calculator.html", "Cost calculator"),
          ("video", "/ai-video-cost.html", "AI video cost"), ("voice", "/ai-voice-cost.html", "AI voice cost")]
_MAP = {p: t for t, p, n in MERGED}
_NAV = ('<nav class="top" aria-label="Main"><a class="nl" href="/tools.html">Find a tool</a><a class="nl" href="/compare-builder.html">Compare</a>'
        '<a class="nl" href="/free.html">Free tools</a><a class="nl" href="/my-ai-costs.html">My AI costs</a><a class="nl" href="/guides.html">Guides</a></nav>')
_CSS40 = '<style>:focus-visible{outline:3px solid #1d4ed8!important;outline-offset:2px;border-radius:6px}.top>a.nl{min-height:44px!important}main li>a{display:inline-flex;align-items:center;min-height:44px}main input:not([type=radio]):not([type=checkbox]):not([type=range]),main select,main button,main summary{min-height:44px;box-sizing:border-box}.mt{display:inline-flex!important;align-items:center;min-height:46px!important;box-sizing:border-box}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}}</style>'
_NCSS = _CSS40 + '<style>.top>a.nl{padding:0 10px}@media(max-width:760px){nav.top{width:100%!important;margin-left:0!important;flex-wrap:wrap!important;gap:0}.top>a.nl{min-height:40px;padding:0 8px;font-size:.92rem}}details.fold>summary{cursor:pointer;min-height:44px;display:flex;align-items:center}details.fold>summary h2{display:inline;margin:0}details.fold>summary::before{content:\"▸\";margin-right:8px}details.fold[open]>summary::before{content:\"▾\"}</style>'
def _relink(h):
    def f(m):
        path, q = m.group(2), m.group(3) or ""
        return f'{m.group(1)}"/my-ai-costs.html{q}#{_MAP[path]}"'
    return _re.sub(r'(href=)"(' + "|".join(_re.escape(p) for p in _MAP) + r')(\?[^"#]*)?(?:#[^"]*)?"', f, h)
def _fold(h):
    h = _re.sub(r'<h2>FAQ</h2>(.*?)(?=<h2|</main>)', r'<details class="fold"><summary><h2>FAQ</h2></summary>\1</details>', h, flags=_re.S)
    h = _re.sub(r'<section class="card tbp"([^>]*)>(<h2[^>]*>.*?</h2>)(.*?)</section>', r'<details class="card tbp fold"\1><summary>\2</summary>\3</details>', h, flags=_re.S)
    h = _re.sub(r'<div class="sponsor">.*?</div>', '', h, flags=_re.S)
    return h
_os.makedirs("public/app", exist_ok=True)
_APPJS = _CSS40 + '<base target="_top"><meta name="robots" content="noindex"><script>addEventListener("load",()=>{const s=()=>parent.postMessage({tpH:document.documentElement.scrollHeight,tpP:location.pathname},"*");s();new ResizeObserver(s).observe(document.body)})</script>'
for t, p, n in MERGED:
    h = open("public" + p).read()
    h = _re.sub(r'<header class="site">.*?</header>', '', h, flags=_re.S); h = _re.sub(r'<footer class="site.*?</footer>', '', h, flags=_re.S)
    h = _re.sub(r'<link rel="canonical"[^>]*>', '', h).replace("</head>", f'<link rel="canonical" href="{BASE}/my-ai-costs.html#{t}"><script>if(top===self&&!navigator.webdriver)location.replace("/my-ai-costs.html"+location.search+"#{t}")</script>' + _APPJS + "</head>", 1)
    h = _fold(_relink(h))
    for _p2 in _MAP: h = h.replace("'" + _p2, "'/app" + _p2).replace('"' + _p2 + '"', '"/app' + _p2 + '"')
    open("public/app" + p, "w").write(h)
    open("public" + p, "w").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved: {n} — ToolPick</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}/my-ai-costs.html#{t}">'
        f'<script>location.replace("/my-ai-costs.html"+location.search+"#{t}")</script><meta http-equiv="refresh" content="0; url=/my-ai-costs.html#{t}"></head><body><p>{n} has moved to <a href="/my-ai-costs.html#{t}">My AI costs</a>.</p></body></html>')
_tabs = "".join(f'<a role="tab" href="#{t}" id="tab-{t}" aria-controls="pane" class="mt">{e(n)}</a>' for t, p, n in MERGED)
_mbody = f"""<style>.mtabs{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px}}.mt{{padding:8px 12px;border:1px solid var(--bd);border-radius:999px;text-decoration:none;color:var(--tx);min-height:24px}}.mt[aria-selected=true]{{background:var(--tx);color:var(--bg)}}#pane{{width:100%;border:0;min-height:600px;display:block}}</style>
<h1>My AI costs</h1><p class="small v44">What do popular AI subscriptions cost? <a href="/ai-subscription-costs.html">Monthly prices and example stacks →</a></p><p class="tag">Audit what you pay, watch prices, set renewal reminders, and see what credits really buy. Prices from official pricing pages only.</p>
<div class="mtabs" role="tablist" aria-label="My AI costs">{_tabs}</div><iframe id="pane" role="tabpanel" tabindex="0" title="My AI costs tool" src="/app/subscription-audit.html"></iframe>
<script>const T={json.dumps({t: p for t, p, n in MERGED})};const fr=document.getElementById('pane');let first=true;
function show(){{let t=location.hash.slice(1);if(!T[t])t='audit';document.querySelectorAll('.mt').forEach(a=>{{const on=a.id=='tab-'+t;a.setAttribute('aria-selected',on);a.tabIndex=on?0:-1}});fr.setAttribute('aria-labelledby','tab-'+t);const src='/app'+T[t]+(first?location.search:'');first=false;if(fr.getAttribute('src')!=src)fr.setAttribute('src',src)}}
addEventListener('hashchange',show);show();const TL=[...document.querySelectorAll('.mt')];document.querySelector('.mtabs').addEventListener('keydown',ev=>{{const i=TL.indexOf(document.activeElement);if(i<0)return;let j=null;if(ev.key=='ArrowRight')j=(i+1)%TL.length;else if(ev.key=='ArrowLeft')j=(i-1+TL.length)%TL.length;else if(ev.key=='Home')j=0;else if(ev.key=='End')j=TL.length-1;else if(ev.key==' '){{ev.preventDefault();TL[i].click();return}}if(j!=null){{ev.preventDefault();TL[j].focus();TL[j].click()}}}});addEventListener('message',m=>{{if(m.origin==location.origin&&m.data&&m.data.tpH)fr.style.height=(m.data.tpH+20)+'px'}});</script>"""
page("/my-ai-costs.html", "My AI Costs — Audit, Watchlist, Reminders, Calculator, Video & Voice Cost | ToolPick",
     "One page for your AI subscriptions: audit what you pay, watch prices, renewal reminders, cost calculator, and the real cost of AI video and voice from official pricing pages.", _mbody,
     [crumbs([("ToolPick", "/"), ("My AI costs", "/my-ai-costs.html")])])
for p in _MAP:
    if p in URLS: URLS.remove(p)
_lm["/my-ai-costs.html"] = V39_DATE
_fpm = "public/my-ai-costs.html"; _hm = open(_fpm).read()
if ' v51"' not in _hm and "</h1>" in _hm: open(_fpm, "w").write(_hm.replace("</h1>", '</h1><p class="small v51">Paying for voice? <a href="/elevenlabs-pricing.html">ElevenLabs pricing</a> · <a href="/is-elevenlabs-worth-it.html">Is ElevenLabs worth it?</a></p>', 1)); _lm["/my-ai-costs.html"] = ELC
_lm["/"] = "2026-10-23"  # v45 smart search
for _u in V41_CHANGED: _lm[_u] = CODING_CHECKED
for _u in V42_CHANGED: _lm[_u] = FREE_CHECKED
for _u in V44_CHANGED: _lm[_u] = "2026-10-22"
for _u in V47_CHANGED: _lm[_u] = "2026-10-23"
for _u in V48_CHANGED: _lm[_u] = "2026-10-24"
for _u in V49_CHANGED: _lm[_u] = ALT49_DATE
for _n, _s in _alt49_summ.items(): _lm[_s["p"]] = _s["lm"]
_lm["/alternatives.html"] = ALT49_DATE
for _u in V51_CHANGED + ["/my-ai-costs.html"]: _lm[_u] = ELC
_fpm = "public/my-ai-costs.html"; _hm = open(_fpm).read()
if ' v52"' not in _hm and "</h1>" in _hm: open(_fpm, "w").write(_hm.replace("</h1>", f'</h1><p class="small v52">Want to stop paying for one? <a href="{R_PATH}">Refund and cancel rules for {_rn} AI tools →</a></p>', 1)); V52_CHANGED.append("/my-ai-costs.html")
for _u in V52_CHANGED: _lm[_u] = REFUND_CHECKED
for _u in V54_CHANGED: _lm[_u] = PRIVACY_CHECKED
for _u in V55_CHANGED: _lm[_u] = PLANNER_CHECKED
_v56ins("/my-ai-costs.html", "</h1>", f'<p class="small v56">Making images? <a href="{I_PATH}">Real cost of AI images: price per image and unlimited plans →</a></p>', after=True)
for _u in V56_CHANGED: _lm[_u] = IMAGE_CHECKED
open("/tmp/v47-changed.txt","w").write("\n".join(V47_CHANGED))
open("/tmp/v44-changed.txt","w").write("\n".join(V44_CHANGED))
open("/tmp/v42-changed.txt","w").write("\n".join(V42_CHANGED))
open("/tmp/v41-changed.txt","w").write("\n".join(V41_CHANGED))
for _n in dict.fromkeys(list(VC) + list(VO) + ["Murf"]):
    _fp = "public" + turl(_n); _h = open(_fp).read()
    _ls = ([f'<a href="/my-ai-costs.html#video">AI video</a>'] if _n in VC else []) + ([f'<a href="/my-ai-costs.html#voice">AI voice</a>'] if _n in VO or _n == "Murf" else [])
    if 'class="pick v39c"' not in _h:
        open(_fp, "w").write(_h.replace('<section class="card tbp"', f'<p class="pick v39c">What do {e(_n)} credits really buy? Real cost per minute: {" · ".join(_ls)}</p><section class="card tbp"', 1))
for _fp in _glob.glob("public/**/*.html", recursive=True):
    if _fp.startswith("public/app/") or _fp[6:] in _MAP: continue
    h = open(_fp).read(); o = h
    h = _re.sub(r'<nav class="top" aria-label="Main">.*?</nav>', _NAV, h, count=1, flags=_re.S).replace("</head>", _NCSS + '<link rel="icon" href="/favicon.svg" type="image/svg+xml"></head>', 1)
    h = _fold(_relink(h))
    _hm = _re.search(r'</h1>(.*?)<h([23])', h, _re.S)
    if _hm and _hm.group(2) == "3": h = h[:_hm.start(2)-2] + '<h2 class="skip">Our picks</h2>' + h[_hm.start(2)-2:]  # v49 fix: insert before '<h3', not between '<' and 'h3'
    if _fp == "public/index.html":
        h = _re.sub(r'<div class="pick"><b>Save money on tools you already pay for</b>.*?(</main>)', r'\1', h, count=1, flags=_re.S)
    if _fp == "public/how-we-pick.html":
        h = _re.sub(r'(<h2[^>]*>.*?</h2>)(.*?)(?=<h2|</main>)', lambda m: f'<details class="fold"><summary>{m.group(1)}</summary>{m.group(2)}</details>', h, flags=_re.S)
    if h != o: open(_fp, "w").write(h)
open("public/favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2563eb"/><text x="16" y="23" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">T</text></svg>')
import struct as _st, zlib as _zl
def _png(w, hgt):
    raw = b"".join(b"\x00" + bytes([37, 99, 235, 255]) * w for _ in range(hgt))
    ch = lambda t, d: _st.pack(">I", len(d)) + t + d + _st.pack(">I", _zl.crc32(t + d) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", _st.pack(">IIBBBBB", w, hgt, 8, 6, 0, 0, 0)) + ch(b"IDAT", _zl.compress(raw)) + ch(b"IEND", b"")
_pd = _png(32, 32); open("public/favicon.ico", "wb").write(_st.pack("<HHH", 0, 1, 1) + _st.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(_pd), 22) + _pd)
INDEXNOW_KEY = "be5a9f80b714743b3b0d00a7ddf35cbe"; open(f"public/{INDEXNOW_KEY}.txt", "w").write(INDEXNOW_KEY)
_ll = open("public/llms.txt").read()
for t, p, n in MERGED: _ll = _ll.replace(BASE + p, f"{BASE}/my-ai-costs.html#{t}")
open("public/llms.txt", "w").write(_ll + f"\n\n## My AI costs\n- [My AI costs]({BASE}/my-ai-costs.html): one page with tabs for the subscription audit, watchlist, renewal reminders, cost calculator, and real cost of AI video and voice. Old URLs redirect to the matching #tab.\n")

open("public/llms.txt", "a").write(f"\n## Smart search (v45)\n- [Finder]({BASE}/?q=voiceover%20under%20%2410): type a whole sentence. It reads the job, a budget (\"under $10\", \"$120/year\"), team size (\"team of 5\": per-seat totals only where the verified entry price is per seat), billing (\"no annual plan\"), \"free\", \"cheap\", and tool names: \"cheaper than ChatGPT\" (same main job, same billing, like-for-like tiers), \"like ElevenLabs but free\", \"ChatGPT vs Claude\" (links the full comparison). Shareable: {BASE}/?q=cheaper%20than%20ChatGPT\n")
# --- v53: directory page clean-up + llms.txt ---
_lm["/tools.html"] = DIR_DATE
_fpd = "public/tools.html"; _hd = open(_fpd).read()
_hd = _re.sub(r'<p class="small v(48|49|50)">.*?</p>', '', _hd)
open(_fpd, "w").write(_hd)
open("public/llms.txt", "a").write(f"\n## Tools directory (v53)\n- [Browse all AI tools]({BASE}/tools.html): search all {total_tools} tools by name or job (e.g. /tools.html?q=voiceover), filter by what each tool does (?job=text-to-speech, from each tool's own site), category (?category=video), real free plan (?free=yes), verified starting price (?price=u10), billing (?billing=monthly), Best Value picks (?bv=1); card or table view (?view=table); compare up to 3. Prices from official pricing pages with checked dates.\n")
open("public/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc>" + (f"<lastmod>{_lm[u]}</lastmod>" if u in _lm else "") + "</url>" for u in URLS) + "</urlset>")
open("public/tools.json","w").write(json.dumps({"checked":CHECKED,"categories":CATEGORIES},indent=1))
print("pages:", len(URLS), "unique tools:", total_tools, {c["id"]:len(c["tools"]) for c in CATEGORIES})
