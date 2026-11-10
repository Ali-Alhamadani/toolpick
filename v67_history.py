"""v67: AI tool price history (/ai-price-history.html) + a 'Price history' box on every tool page.
Built only from price_history.json snapshot diffs (CHANGES in build.py) and the plain-English PRICE_NOTES, with each change
classified in tools.py V67_KIND: real price moves (went up / went down / cheaper plan added / higher plan added / new plan /
plans reorganized / plan renamed / intro offer changed) are kept apart from our own listing updates (added detail, corrections,
currency). Moves (before -> after $) only restate the documented old/new price text of that change. Current prices are each
tool's cheapest checked plan with its own checked date and official pricing link. Re-checks where only the checked date changed
are dropped from the change log (they were never price changes)."""
import json, re, datetime

V67_DATE = "2026-11-10"
PATH = "/ai-price-history.html"
# kind -> (label, badge class, real move?, filter group)
KINDS = {
    "raise": ("Price went up", "k67u", True, "up"),
    "cut": ("Price went down", "k67d", True, "down"),
    "cheaper": ("Cheaper plan added", "k67d", True, "plans"),
    "top": ("Higher plan added", "k67n", True, "plans"),
    "newplan": ("New plan added", "k67n", True, "plans"),
    "restructure": ("Plans reorganized", "k67n", True, "plans"),
    "rename": ("Plan renamed, same price", "k67n", True, "names"),
    "promo": ("Intro offer changed", "k67n", True, "offers"),
    "detail": ("We added detail (no price change)", "k67l", False, "listing"),
    "correction": ("We corrected our listing", "k67l", False, "listing"),
    "currency": ("Now listed in US dollars", "k67l", False, "listing"),
    "changed": ("Listing changed", "k67l", False, "listing"),
}
TAG2KIND = {"up": "raise", "down": "cut", "newplan": "newplan", "correction": "correction", "currency": "currency", "changed": "changed"}
KIND2TAG = {"raise": "up", "cut": "down", "cheaper": "newplan", "newplan": "newplan", "top": "changed", "restructure": "changed", "rename": "changed",
            "promo": "changed", "detail": "changed", "correction": "correction", "currency": "currency", "changed": "changed"}
GROUPS = [("up", "Raised a price"), ("down", "Cut a price"), ("plans", "Added or reorganized plans"), ("names", "Renamed a plan"),
          ("offers", "Changed an intro offer"), ("none", "No price change found")]
CK = re.compile(r"\s*\(checked \d{4}-\d{2}-\d{2}\)")


def nice(d):
    x = datetime.date.fromisoformat(d); return x.strftime("%b ") + str(x.day) + x.strftime(", %Y")


def usd(v):
    r = round(v, 2); return "$" + (f"{int(r):,}" if r == int(r) else f"{r:,.2f}")


def classify(CHANGES, PRICE_NOTES, V67_KIND):
    """Drop date-only re-checks; give every change a kind, a clear label, a badge tag and its documented moves."""
    keep = []
    dropped = []
    for c in CHANGES:
        key = f'{c["date"]}|{c["name"]}'
        if key not in PRICE_NOTES and key not in V67_KIND and CK.sub("", c["old"] or "") == CK.sub("", c["new"] or "") and (c.get("oldf") == c.get("newf")):
            dropped.append(key); continue
        kind, moves = V67_KIND.get(key, (TAG2KIND.get(c["tag"], "changed"), []))
        c["kind"] = kind; c["moves"] = moves; c["label"] = KINDS[kind][0]; c["tag"] = KIND2TAG[kind]; c["real"] = KINDS[kind][2]
        keep.append(c)
    CHANGES[:] = keep
    return dropped


def move_txt(mv, e):
    plan, bill, a, b = mv
    pct = (b - a) / a * 100 if a else 0
    arrow = "up" if b > a else "down"
    return f'<span class="mv67">{e(plan)}: <s>{usd(a)}</s> → <b>{usd(b)}</b> {e(bill)} <span class="pc67 {arrow}">({"+" if pct > 0 else "−"}{abs(round(pct))}%)</span></span>'


CSS = """<style>.k67{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.02em;padding:3px 9px;border-radius:999px;margin:0 4px 2px 0;white-space:nowrap}
.k67u{background:#fde8e8;color:#8f1d1d}.k67d{background:#dcf5e3;color:#14532d}.k67n{background:var(--acs);color:var(--tx)}.k67l{background:var(--sf2);color:var(--mu);font-weight:600}
.st67{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:var(--s4) 0}.st67 button{font:inherit;text-align:left;cursor:pointer;background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:12px 14px;box-shadow:var(--sh);color:var(--tx);min-height:44px}
.st67 button b{display:block;font-size:1.6rem;line-height:1.1}.st67 button[aria-pressed=true]{outline:3px solid var(--ac);outline-offset:1px}
.tl67{list-style:none;padding:0;margin:6px 0 0;display:grid;gap:8px}.tl67 li{border-left:3px solid var(--bd);padding:2px 0 2px 12px}.tl67 li.r{border-left-color:var(--ac)}
.tl67 a{display:inline-block;padding:3px 0;min-height:24px}.tl67 time{font-weight:700;margin-right:6px;white-space:nowrap}.mv67{display:block;margin-top:2px}.pc67.up{color:#8f1d1d;font-weight:700}.pc67.down{color:#14532d;font-weight:700}
.h67{margin:12px 0;scroll-margin-top:80px}.h67 h3{margin:0;font-size:1.1rem;display:inline;margin-right:8px}.h67 p{margin:4px 0}.h67 details{margin-top:6px}.h67 summary{cursor:pointer;color:var(--mu);font-size:.9rem;min-height:32px}
.fb67{display:grid;grid-template-columns:minmax(0,2fr) repeat(3,minmax(0,1fr));gap:10px;align-items:end}.fb67>div{min-width:0}.fb67 select{width:100%}.fb67 label{display:block;font-weight:600;font-size:.9rem}@media(max-width:760px){.fb67{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.fb67 .q{grid-column:1/-1}}
.t67{width:100%;border-collapse:collapse;font-size:.92rem}.t67 th{white-space:normal;vertical-align:bottom}.sec67{min-width:0;max-width:100%}.sec67 .tw{max-width:100%}.t67 th,.t67 td{padding:8px 10px;border-bottom:1px solid var(--bd);text-align:left}.t67 td.n{text-align:right;font-variant-numeric:tabular-nums}
@media(max-width:640px){.t67.mv thead{display:none}.t67.mv tr{display:block;padding:8px 0;border-bottom:1px solid var(--bd)}.t67.mv td{display:block;border:0;padding:2px 10px;text-align:left}.t67.mv td[data-l]{display:inline-block;padding:2px 12px 2px 10px}.t67.mv td[data-l]::before{content:attr(data-l) ": ";font-weight:600;color:var(--mu)}}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.tp67 h2{margin:0 0 6px;font-size:1.15rem}.tp67 .tl67{margin-bottom:6px}</style>"""


def _timeline(chs, e, turl_=None, show_tool=False):
    out = []
    for c in chs:
        k = KINDS[c["kind"]]
        mv = "".join(move_txt(m, e) for m in c["moves"])
        out.append(f'<li class="{"r" if c["real"] else ""}"><time datetime="{c["date"]}">{nice(c["date"])}</time><span class="k67 {k[1]}">{e(k[0])}</span> {e(c["summary"])}{mv} '
                   f'<a href="/price-changes.html#{c["date"]}-{c["s"]}">Before and after<span class="sr"> for {e(c["name"])} on {nice(c["date"])}</span></a></li>')
    return "".join(out)


def tool_record(name, CHANGES_BY_TOOL, first, k, pricing, e):
    """(status sentence, real-moves html, listing-updates html, groups) for one tool."""
    chs = CHANGES_BY_TOOL.get(name, [])
    real = [c for c in chs if c["real"]]; lst = [c for c in chs if not c["real"]]
    groups = sorted({KINDS[c["kind"]][3] for c in real}) or ["none"]
    if real:
        last = real[0]
        sent = f'Latest price move: <b>{e(KINDS[last["kind"]][0].lower())}</b> on {nice(last["date"])}. {len(real)} price move{"s" if len(real) != 1 else ""} recorded since we started tracking on {nice(first)}.'
    else:
        sent = f'<b>No price change found</b> in our checks since we started tracking {e(name)} on {nice(first)}.'
    sent += f' Last checked on the <a href="{e(pricing)}" rel="noopener" target="_blank">official pricing page</a> on {nice(k)}.'
    return sent, _timeline(real, e), _timeline(lst, e), groups, real, lst


def build_v67(ctx):
    page = ctx["page"]; e = ctx["e"]; BASE = ctx["BASE"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]; _lm = ctx["_lm"]; URLS = ctx["URLS"]
    DLIST = ctx["_DLIST"]; CHANGES = ctx["CHANGES"]; CBT = ctx["CHANGES_BY_TOOL"]; PH = ctx["_ph"]; CATS = ctx["CATEGORIES"]
    dates = sorted(PH)
    REC = {}
    for v in DLIST:
        n = v["n"]
        seen = [d for d in dates if n in PH[d]]
        first = seen[0] if seen else v["k"]
        sent, rh, lh, groups, real, lst = tool_record(n, CBT, first, v["k"], v["pr"], e)
        REC[v["s"]] = dict(v=v, first=first, sent=sent, rh=rh, lh=lh, groups=groups, real=real, lst=lst)
    cnt = {g: sum(1 for r in REC.values() if g in r["groups"]) for g, _ in GROUPS}
    nreal = sum(1 for c in CHANGES if c["real"]); nlist = len(CHANGES) - nreal
    first_all = dates[0]; last_all = dates[-1]
    # stat buttons
    stats = "".join(f'<button type="button" data-g="{g}" aria-pressed="false"><b>{cnt[g]}</b>{e(lab)}</button>' for g, lab in GROUPS)
    # biggest documented moves
    mvrows = []
    for c in CHANGES:
        for m in c["moves"]:
            plan, bill, a, b = m; pct = (b - a) / a * 100 if a else 0
            mvrows.append((c, m, pct))
    mvrows.sort(key=lambda x: (x[0]["date"], abs(x[2])), reverse=True)
    mvt = "".join(f'<tr><td><a href="#t-{c["s"]}">{e(c["name"])}</a></td><td>{e(m[0])}<br><span class="small">{e(m[1])}</span></td><td class="n" data-l="Before → now"><s>{usd(m[2])}</s> → <b>{usd(m[3])}</b></td>'
                  f'<td class="n" data-l="Change"><span class="pc67 {"up" if p > 0 else "down"}">{"+" if p > 0 else "−"}{abs(round(p))}%</span></td><td data-l="Recorded">{nice(c["date"])}</td><td><a href="{e(c["pricing"])}" rel="noopener" target="_blank">Official page<span class="sr"> for {e(c["name"])}</span></a></td></tr>'
                  for c, m, p in mvrows)
    # by category
    crow = []
    for cat in CATS:
        rs = [r for r in REC.values() if any(x["id"] == cat["id"] for x in r["v"]["cats"])]
        if not rs: continue
        cc = {g: sum(1 for r in rs if g in r["groups"]) for g, _ in GROUPS}
        crow.append(f'<tr><td><a href="?category={cat["id"]}" data-cat="{cat["id"]}">{e(cat["name"])}</a></td><td class="n" data-l="Tools">{len(rs)}</td><td class="n" data-l="Raised">{cc["up"]}</td><td class="n" data-l="Cut">{cc["down"]}</td>'
                    f'<td class="n" data-l="Plans or offers changed">{len([r for r in rs if set(r["groups"]) & {"plans", "names", "offers"}])}</td><td class="n" data-l="No change found">{cc["none"]}</td></tr>')
    # board
    cards = []
    order = sorted(REC.values(), key=lambda r: ((r["real"][0]["date"] if r["real"] else "0"), r["v"]["n"].lower()), reverse=False)
    order = sorted(REC.values(), key=lambda r: r["v"]["n"].lower())
    order.sort(key=lambda r: (r["real"][0]["date"] if r["real"] else ""), reverse=True)
    for r in order:
        v = r["v"]; m, a = v["m"], v["a"]
        mm = m if isinstance(m, (int, float)) else None; aa = a if isinstance(a, (int, float)) else None
        price = " · ".join(x for x in [f"<b>{usd(mm)}/mo</b> billed monthly" if mm is not None else "", f"{usd(aa)}/mo billed yearly" if aa is not None else ""] if x)
        if not price: price = "not checked in US dollars, see the official page"
        per = ", per seat" if v.get("ps") else ""
        bad = "".join(f'<span class="k67 {KINDS[k][1]}">{e(KINDS[k][0])}</span>' for k in dict.fromkeys(c["kind"] for c in r["real"])) or '<span class="k67 k67l">No price change found</span>'
        body = (f'<ol class="tl67">{r["rh"]}</ol>' if r["rh"] else "")
        if r["lh"]: body += f'<details><summary>{len(r["lst"])} listing update{"s" if len(r["lst"]) != 1 else ""} by us (no price change)</summary><ol class="tl67">{r["lh"]}</ol></details>'
        cards.append(f'<article class="card h67" id="t-{v["s"]}" data-n="{e(v["n"].lower())}" data-c="{" ".join(x["id"] for x in v["cats"])}" data-g="{" ".join(r["groups"])}" '
                     f'data-d="{r["real"][0]["date"] if r["real"] else ""}" data-m="{mm if mm is not None else (aa if aa is not None else "")}" data-k="{v["k"]}">'
                     f'<div><h3><a href="{v["u"]}">{e(v["n"])}</a></h3>{bad}</div><p class="small">Cheapest plan now: {price}{per}. {r["sent"]}</p>{body}</article>')
    copts = "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATS)
    gopts = "".join(f'<option value="{g}">{e(lab)}</option>' for g, lab in GROUPS)
    up_names = [r["v"]["n"] for r in REC.values() if "up" in r["groups"]]
    down_names = [r["v"]["n"] for r in REC.values() if "down" in r["groups"]]
    body = f"""{CSS}<section class="hero"><p class="small"><a href="/save-money.html">Save money</a> › Price history</p><h1>AI tool price history</h1><p class="tag">Before you subscribe, see whether a tool has been raising its prices. We re-check {len(DLIST)} AI tools on their official pricing pages and record every change since {nice(first_all)}: who raised prices, who cut them, who added plans, and who held steady. Our own listing fixes are kept apart, so you only see real price moves.</p></section>
<section aria-labelledby="sum67"><h2 id="sum67">Since {nice(first_all)}, across {len(DLIST)} tools</h2><p class="small" style="margin:0">{nreal} real price move{"s" if nreal != 1 else ""} and {nlist} listing update{"s" if nlist != 1 else ""} by us across {len(dates)} price snapshots (latest {nice(last_all)}). Tap a box to filter the list below.</p><div class="st67" id="st67">{stats}</div>
<p>Raised a price: {", ".join(f'<a href="#t-{v["s"]}">{e(v["n"])}</a>' for v in DLIST if v["n"] in up_names) or "none"}. Cut a price: {", ".join(f'<a href="#t-{v["s"]}">{e(v["n"])}</a>' for v in DLIST if v["n"] in down_names) or "none"}.</p></section>
<section class="sec67" aria-labelledby="mv67h"><h2 id="mv67h">Every documented price move</h2><p class="small">Old and new prices exactly as listed on the official page at each check, on the same billing. Rows marked “cheapest plan” compare the cheapest plan before and after a new plan was added.</p><div class="tw"><table class="t67 mv"><thead><tr><th scope="col">Tool</th><th scope="col">Plan and billing</th><th scope="col">Before → now</th><th scope="col">Change</th><th scope="col">Recorded</th><th scope="col">Source</th></tr></thead><tbody>{mvt}</tbody></table></div></section>
<section class="sec67" aria-labelledby="cat67h"><h2 id="cat67h">By category</h2><div class="tw"><table class="t67 mv"><thead><tr><th scope="col">Category</th><th scope="col">Tools</th><th scope="col">Raised</th><th scope="col">Cut</th><th scope="col">Plans or offers changed</th><th scope="col">No change found</th></tr></thead><tbody>{"".join(crow)}</tbody></table></div></section>
<section aria-labelledby="all67h"><h2 id="all67h">Price history for every tool</h2>
<form class="builder fb67" id="f67" role="search" onsubmit="return false"><div class="q"><label for="q67">Find a tool</label><input type="search" id="q67" placeholder="e.g. ChatGPT or Runway" autocomplete="off"></div>
<div><label for="c67">Category</label><select id="c67"><option value="">All categories</option>{copts}</select></div>
<div><label for="g67">Show</label><select id="g67"><option value="">Every tool</option>{gopts}</select></div>
<div><label for="o67">Sort</label><select id="o67"><option value="recent">Latest price move first</option><option value="az">A to Z</option><option value="cheap">Cheapest plan first</option><option value="checked">Most recently checked</option></select></div></form>
<p class="small" id="n67" role="status" aria-live="polite"></p><div id="l67">{"".join(cards)}</div><div class="pick" id="z67" hidden><b>No tools match.</b> <button type="button" class="bbtn" id="r67">Show every tool</button></div></section>
<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">How we record a price change</h2><p class="small" style="margin:0">Each time we re-check a tool on its official pricing page we save the listed prices. When the text changes, we compare it with the check before and sort the change into a kind. <b>Real price moves</b>: price went up, price went down, cheaper plan added, higher plan added, new plan added, plans reorganized, plan renamed at the same price, intro offer changed. <b>Our listing updates</b> (no price change): we added detail such as yearly prices, corrected our own listing, or switched currency. Before and after amounts are only the ones written on the official page; when old and new plans aren't like for like, we don't call it a rise or a cut. “No price change found” means none in our checks, so always confirm on the official page before you pay. Tools are re-checked at different times; each shows its own last-checked date.</p>
<p class="small" style="margin:12px 0 0"><a href="/price-changes.html">Every change, newest first</a> · <a href="/price-changes.xml">Atom feed</a> · <a href="/my-ai-costs.html#watchlist">Watch the prices you pay</a> · <a href="/monthly-or-yearly.html">Lock a price in with yearly billing?</a> · <a href="/pay-less.html">Pay less for a tool</a> · <a href="/save-money.html">Save money hub</a></p></div>
<script>{JS}</script>"""
    qas = [("Which AI tools raised their prices recently?", f"Since {nice(first_all)} our checks recorded price rises at " + (", ".join(up_names) or "no tools") + f" and price cuts at " + (", ".join(down_names) or "no tools") + f". The other changes were new or renamed plans, intro offers, or our own listing updates. {cnt['none']} of {len(DLIST)} tools had no price change in our checks."),
           ("How do you know a price changed?", "We copy the listed prices from each tool's official pricing page every time we re-check it and compare them with the previous check. The before and after amounts are the ones written on the page, with the date we read it and a link to the page."),
           ("Does “no price change found” mean the price is guaranteed?", "No. It means none of our checks since we started tracking found a change. Each tool shows when we last checked it; always confirm on the official pricing page before you pay."),
           ("Should I pay yearly to avoid a price rise?", "Yearly billing usually locks the price for the year and is often cheaper per month, but you pay up front and refunds vary. Our Monthly or yearly page shows the saving for each tool, and the refund guide shows which tools refund a yearly plan.")]
    fh, fl = faq(qas)
    body += fh
    while PATH in URLS: URLS.remove(PATH)
    page(PATH, "AI Tool Price History: Who Raised, Cut or Held Prices (2026) | ToolPick",
         f"Price history for {len(DLIST)} AI tools, checked on official pricing pages since {nice(first_all)}: which tools raised or cut prices, added plans or held steady, with before and after prices, dates and sources.",
         body,
         [{"@context": "https://schema.org", "@type": "Dataset", "name": "AI tool price history", "url": BASE + PATH, "dateModified": last_all,
           "description": f"Recorded price changes for {len(DLIST)} AI tools from their official pricing pages since {first_all}, classified as real price moves or listing updates.",
           "creator": {"@type": "Organization", "name": "ToolPick", "url": BASE}, "temporalCoverage": f"{first_all}/{last_all}", "isAccessibleForFree": True, "license": BASE + "/how-we-pick.html"},
          fl, crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Price history", PATH)])])
    _lm[PATH] = V67_DATE
    return REC, cnt, nreal, nlist


JS = r"""(function(){const L=document.getElementById('l67'),C=[...L.querySelectorAll('.h67')],q=document.getElementById('q67'),c=document.getElementById('c67'),g=document.getElementById('g67'),o=document.getElementById('o67'),n=document.getElementById('n67'),z=document.getElementById('z67'),S=[...document.querySelectorAll('#st67 button')];
const has=(s,v)=>s.split(' ').includes(v);
function sortC(){const k=o.value;const a=C.slice();a.sort((x,y)=>{if(k=='az')return x.dataset.n.localeCompare(y.dataset.n);if(k=='cheap'){const p=x.dataset.m===''?1e9:+x.dataset.m,r=y.dataset.m===''?1e9:+y.dataset.m;return p-r||x.dataset.n.localeCompare(y.dataset.n)}if(k=='checked')return y.dataset.k.localeCompare(x.dataset.k)||x.dataset.n.localeCompare(y.dataset.n);return y.dataset.d.localeCompare(x.dataset.d)||x.dataset.n.localeCompare(y.dataset.n)});a.forEach(x=>L.appendChild(x))}
function run(push){const t=q.value.trim().toLowerCase(),cv=c.value,gv=g.value;let m=0;C.forEach(x=>{const ok=(!t||x.dataset.n.includes(t))&&(!cv||has(x.dataset.c,cv))&&(!gv||has(x.dataset.g,gv));x.hidden=!ok;if(ok)m++});
S.forEach(b=>b.setAttribute('aria-pressed',b.dataset.g==gv?'true':'false'));z.hidden=m>0;n.textContent=m+' of '+C.length+' tools shown'+(gv?' · '+g.options[g.selectedIndex].text.toLowerCase():'')+(cv?' · '+c.options[c.selectedIndex].text:'');
if(push){const p=new URLSearchParams();if(t)p.set('q',t);if(cv)p.set('category',cv);if(gv)p.set('show',gv);if(o.value!='recent')p.set('sort',o.value);const s=p.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash)}}
const P=new URLSearchParams(location.search);const setv=(el,v)=>{if(v&&[...el.options].some(x=>x.value==v))el.value=v};q.value=P.get('q')||'';setv(c,P.get('category'));setv(g,P.get('show'));setv(o,P.get('sort'));
[q].forEach(el=>el.addEventListener('input',()=>run(1)));[c,g].forEach(el=>el.addEventListener('change',()=>run(1)));o.addEventListener('change',()=>{sortC();run(1)});
S.forEach(b=>b.addEventListener('click',()=>{g.value=g.value==b.dataset.g?'':b.dataset.g;run(1);document.getElementById('all67h').scrollIntoView({behavior:'smooth',block:'start'})}));
document.querySelectorAll('a[data-cat]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();c.value=a.dataset.cat;run(1);document.getElementById('all67h').scrollIntoView({block:'start'});c.focus()}));
document.getElementById('r67').addEventListener('click',()=>{q.value='';c.value='';g.value='';run(1);q.focus()});
if(location.hash.startsWith('#t-')){const el=document.getElementById(location.hash.slice(1));if(el){q.value='';c.value='';g.value=''}}
if(o.value!='recent')sortC();run(0)})();"""


def link_v67(ctx, REC):
    """Tool pages get a 'Price history' box (and an accurate trust-panel line); hubs link to the page."""
    e = ctx["e"]; changed = []
    for s, r in REC.items():
        v = r["v"]; fp = f"public/tools/{s}.html"
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' tp67"' in h: continue
        body = (f'<ol class="tl67">{r["rh"]}</ol>' if r["rh"] else "")
        if r["lh"]: body += f'<details><summary>{len(r["lst"])} listing update{"s" if len(r["lst"]) != 1 else ""} by us (no price change)</summary><ol class="tl67">{r["lh"]}</ol></details>'
        box = (f'{CSS}<section class="card tp67" style="margin-bottom:16px" id="price-history" aria-labelledby="ph67"><h2 id="ph67">{e(v["n"])} price history</h2><p>{r["sent"]}</p>{body}'
               f'<p class="small" style="margin:6px 0 0"><a href="/ai-price-history.html#t-{s}">Compare with the price history of all {len(REC)} tools →</a> · <a href="/my-ai-costs.html?add={s}#watchlist">Watch this price</a></p></section>')
        a = '<p><a class="btn" href="'
        if a not in h: continue
        h = h.replace(a, box + a, 1)
        tr = re.sub(r'<dt>Price history</dt><dd>.*?</dd>', lambda m_: '<dt>Price history</dt><dd>' + (f'{len(r["real"])} price move{"s" if len(r["real"]) != 1 else ""} since {r["first"]}' if r["real"] else f'No price change found since {r["first"]}') + f'; last checked {v["k"]}. <a href="#price-history">See the history</a></dd>', h, count=1)
        open(fp, "w").write(tr); changed.append(f"/tools/{s}.html")
    fp = "public/price-changes.html"; h = open(fp).read()
    if ' v67"' not in h:
        h = h.replace("</p></section>", '</p><p class="pick v67" style="text-align:left">Choosing a tool? <a href="/ai-price-history.html"><b>See each tool\'s full price history</b></a>: who raised, cut or held prices since we started tracking, with real price moves kept apart from our own listing updates.</p></section>', 1)
        h = h.replace("“Correction” = we fixed our own listing.", "“We corrected our listing” and “We added detail” are our own listing updates, not price changes.", 1)
        open(fp, "w").write(h); changed.append("/price-changes.html")
    fp = "public/save-money.html"; h = open(fp).read()
    a = '<a class="card" href="/price-changes.html" style="display:block;text-decoration:none">'
    if ' v67"' not in h and a in h:
        h = h.replace(a, '<a class="card v67" href="/ai-price-history.html" style="display:block;text-decoration:none"><h2 style="margin:0 0 6px;font-size:1.15rem">AI tool price history →</h2><p style="margin:0">Before you subscribe: which tools raised, cut or held prices since we started tracking, tool by tool.</p></a>' + a, 1)
        open(fp, "w").write(h); changed.append("/save-money.html")
    fp = "public/guides.html"; h = open(fp).read()
    if ' v67"' not in h and "<h2>New guides</h2><ul>" in h:
        h = h.replace("<h2>New guides</h2><ul>", "<h2>New guides</h2><ul><li class=\"v67\"><a href='/ai-price-history.html'>AI tool price history: who raised, cut or held prices, tool by tool</a></li>", 1)
        open(fp, "w").write(h); changed.append("/guides.html")
    return changed
