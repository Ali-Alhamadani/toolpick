"""v68: '<Tool> alternatives' for every tool - pick your reason to switch.
One page per tool (/alternatives/<slug>.html; Cursor keeps its hand-checked /cursor-alternatives.html, which gets the same
reason finder) + a searchable hub (/alternatives.html) + an "Alternatives" box on every tool page.
Each page answers "what should I use instead, and why?" by the reason people switch: cheaper (same main job, same billing,
like-for-like tier rule), a real free plan, doesn't train AI on your content by default, a refund window, a student deal,
cheaper yearly billing, and no price rise recorded. Every claim reuses facts already verified in tools.py (via the v66 fact
table: official source link + checked date per fact) and the v67 price history; nothing new is invented. Alternatives are:
1) same main job (first CAPS tag) - the only group where prices are compared; 2) close alternatives that also do the job
(the tool's main job is one of their jobs, or ToolPick ranks both for the same job); 3) if fewer than 3 so far, other tools
in the same category, labelled as a different main job."""
import json, re, datetime

V68_DATE = "2026-11-11"
HUB = "/alternatives.html"
KEYS = [("cheaper", "Cheaper", "Costs less for the same job"), ("free", "Real free plan", "A free plan you can keep using"),
        ("privacy", "No AI training by default", "Doesn't train on your content unless you opt in"), ("refund", "Refund window", "States a refund window"),
        ("student", "Student deal", "Free or discounted for students"), ("yearly", "Cheaper yearly", "Saves if you pay for a year"),
        ("stable", "No price rise", "No price rise recorded in our checks")]
FACTS = [("free", "Free plan", "/free-plan-limits.html"), ("privacy", "No AI training by default", "/ai-data-privacy.html"),
         ("refund", "Refund window", "/ai-refund-policies.html"), ("student", "Student deal", "/ai-student-discounts.html"),
         ("yearly", "Yearly saving", "/monthly-or-yearly.html")]
ICON = {"y": ("✓", "Yes"), "p": ("~", "Partly"), "n": ("✕", "No"), "u": ("?", "Not checked")}


def nice(d):
    x = datetime.date.fromisoformat(d); return x.strftime("%b ") + str(x.day) + x.strftime(", %Y")


CSS = ("<style>.a68top{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));margin:var(--s4) 0}"
       ".a68now dl{display:grid;grid-template-columns:max-content 1fr;gap:6px 12px;margin:8px 0 0;font-size:.92rem}.a68now dt{font-weight:600}.a68now dd{margin:0}"
       ".a68q{list-style:none;padding:0;margin:8px 0 0}.a68q li{margin:0;padding:8px 0;border-top:1px solid var(--bd);font-size:.95rem}.a68q li:first-child{border-top:0}.a68q li{display:grid;grid-template-columns:120px 1fr;gap:10px}"
       ".a68f{position:sticky;top:0;z-index:2;background:var(--bg);padding:10px 0 8px;margin:var(--s5) 0 0;border-bottom:1px solid var(--bd)}"
       ".a68f h2{font-size:1.05rem;margin:0 0 8px}.a68c{display:flex;flex-wrap:wrap;gap:8px}"
       ".a68c button{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;font-size:.92rem;cursor:pointer}"
       ".a68c button[aria-pressed=true]{background:var(--ac);border-color:var(--ac);color:var(--sf);font-weight:700}.a68c button[aria-pressed=true]::before{content:'✓'}"
       ".a68c button:disabled{opacity:.55;cursor:not-allowed}.a68c button .n{font-size:.8rem}.a68c button:focus-visible{outline:3px solid var(--ac);outline-offset:2px}"
       "#a68st{margin:8px 0 0;min-height:1.4em}.a68g h2{margin:var(--s6) 0 4px}.a68g>.small{margin:0 0 8px}"
       ".a68l{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));margin:var(--s3) 0}"
       ".a68k{scroll-margin-top:150px}.a68k h3{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px}.a68k h3 a{min-height:32px;display:inline-flex;align-items:center}"
       ".a68k .pr{font-weight:700;font-size:1.05rem}.a68k ul{margin:4px 0 0;padding-left:1.1em}.a68k li{margin:3px 0;font-size:.93rem}.a68k li>a{padding:0;display:inline}"
       ".a68k .why li::marker{content:'+ ';color:var(--ok);font-weight:700}.a68k .wo li::marker{content:'– ';color:var(--warn);font-weight:700}"
       ".a68k h4{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mu);margin:10px 0 0}"
       ".a68i{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0;padding:0;list-style:none}.a68i li{margin:0!important;font-size:.8rem!important;padding:3px 9px;border-radius:999px;background:var(--sf2);border:1px solid var(--bd)}"
       ".a68i .y{border-color:var(--ok)}.a68i .n{border-color:var(--warn)}.a68i b{margin-right:3px}"
       ".a68k details{margin-top:8px}.a68k summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-size:.92rem;font-weight:600}"
       ".a68k dl{margin:0;font-size:.88rem}.a68k dt{font-weight:600;margin-top:6px}.a68k dd{margin:0}.a68k dd a{display:inline;padding:0}"
       ".a68a{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:auto!important;padding-top:10px;border-top:1px solid var(--bd);font-size:.92rem}.a68a a{min-height:44px;display:inline-flex;align-items:center}"
       ".a68k[hidden],.a68g[hidden]{display:none}.a68j{margin:4px 0 0}.a68j a{display:inline-flex;align-items:center;min-height:44px}#a68fh{scroll-margin-top:12px}.a68e{padding:var(--s4);border:1px dashed var(--bd);border-radius:var(--r)}"
       ".a68t table{min-width:760px}.a68t td,.a68t th{font-size:.9rem;vertical-align:top}.a68t tr.me{background:var(--sf2)}"
       ".a68h{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:var(--s4);margin:var(--s3) 0}.a68h .card p{font-size:.9rem}.a68h .card h3 a{min-height:32px;display:inline-flex;align-items:center}"
       ".a68s{width:100%;max-width:520px;min-height:48px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px;font:inherit}"
       ".tp68 ul{margin:6px 0 0;padding-left:1.1em}.tp68 li{margin:2px 0}.tp68 li::marker{color:var(--ok)}.tp68 li>a{display:inline;padding:0}"
       "@media(max-width:640px){.a68f{position:static}.a68q li{grid-template-columns:1fr;gap:2px}.a68now dl{grid-template-columns:1fr}.a68now dd{margin-bottom:6px}"
       ".a68t table{min-width:0}.a68t tr:first-child{display:none}.a68t table,.a68t tbody,.a68t tr,.a68t td,.a68t th{display:block;width:100%}.a68t tr{border-bottom:1px solid var(--bd);padding:8px 4px}"
       ".a68t td,.a68t th{border:0;padding:3px 12px}.a68t td::before{content:attr(data-l);display:block;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--mu)}}</style>")

JS = r"""(()=>{const B=[...document.querySelectorAll('.a68c button')],K=[...document.querySelectorAll('.a68k')],G=[...document.querySelectorAll('.a68g')],st=document.getElementById('a68st'),L=JSON.parse(document.getElementById('a68L').textContent);
function on(){return B.filter(b=>b.getAttribute('aria-pressed')=='true').map(b=>b.dataset.w)}
function go(push){const w=on();let n=0;K.forEach(k=>{const has=(k.dataset.w||'').split(' ');const ok=w.every(x=>has.includes(x));k.hidden=!ok;if(ok)n++});
G.forEach(g=>{const v=g.querySelectorAll('.a68k:not([hidden])').length;g.hidden=v==0;const c=g.querySelector('.gc');if(c)c.textContent=w.length?v+' of '+c.dataset.t:c.dataset.t});
const e=document.getElementById('a68e');if(e)e.hidden=n>0;
st.textContent=w.length?n+' of '+K.length+' alternatives '+(n==1?'matches':'match')+': '+w.map(x=>L[x]).join(' + ')+'.':'Showing all '+K.length+' alternatives. Pick one or more reasons to narrow them down.';
if(push){const u=new URL(location.href);if(w.length)u.searchParams.set('want',w.join(','));else u.searchParams.delete('want');history.replaceState(null,'',u.pathname+u.search+u.hash)}}
B.forEach(b=>b.addEventListener('click',()=>{if(b.disabled)return;b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')=='true'?'false':'true');go(true)}));
const r=document.getElementById('a68r');if(r)r.addEventListener('click',()=>{B.forEach(b=>b.setAttribute('aria-pressed','false'));go(true)});
const q=new URLSearchParams(location.search).get('want');if(q)q.split(',').forEach(x=>{const b=B.find(b=>b.dataset.w==x&&!b.disabled);if(b)b.setAttribute('aria-pressed','true')});go(false);
if(on().length&&!location.hash){const f=document.querySelector('.a68f');if(f)f.scrollIntoView()}})();"""

HUBJS = r"""(()=>{const i=document.getElementById('a68q'),C=[...document.querySelectorAll('.a68h .card')],S=[...document.querySelectorAll('.a68hs')],st=document.getElementById('a68hst');
function go(){const v=i.value.trim().toLowerCase();let n=0;C.forEach(c=>{const ok=!v||c.dataset.k.includes(v);c.hidden=!ok;if(ok)n++});S.forEach(s=>s.hidden=!s.querySelector('.card:not([hidden])'));st.textContent=v?n+' tool'+(n==1?'':'s')+' match “'+i.value.trim()+'”.':''}
i.addEventListener('input',go);const q=new URLSearchParams(location.search).get('q');if(q){i.value=q;go()}})();"""


def build_v68(ctx):
    page = ctx["page"]; e = ctx["e"]; slug = ctx["slug"]; turl = ctx["turl"]; BASE = ctx["BASE"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]
    _lm = ctx["_lm"]; URLS = ctx["URLS"]; TOOL = ctx["TOOL"]; samejob = ctx["samejob"]; cmp_price = ctx["cmp_price"]; num = ctx["_num"]; usd = ctx["_usd"]
    realfree = ctx["realfree"]; limitation = ctx["limitation"]; tier_note = ctx["tier_note"]; CAPS = ctx["CAPS"]; CAP_LABEL = ctx["CAP_LABEL"]
    JOBS = ctx["JOBS"]; CATS = ctx["CATEGORIES"]; BEST_OF = ctx["BEST_OF"]; COMPARISONS = ctx["COMPARISONS"]; cnames = ctx["cnames"]
    FREE_ALT = dict(ctx["FREE_ALT_URLS"]); TD = {t["n"]: t for t in ctx["TD"]}; REC = ctx["REC"]; TIER_MATCH = ctx["TIER_MATCH"]; LOWER_TIER = ctx["LOWER_TIER"]
    CHECKED = ctx["CHECKED"]; dom = ctx["dom"]
    names = sorted(TD, key=str.lower)
    assert set(names) == set(TOOL), set(names) ^ set(TOOL)
    CAT1 = {}
    for c in CATS:
        for t in c["tools"]: CAT1.setdefault(t["name"], c)
    cmpmap = {}
    for x in COMPARISONS:
        a, b = cnames(x)[:2]
        if len(cnames(x)) == 2: cmpmap[frozenset((a, b))] = f"/compare/{x[0]}.html"
    def path(n): return "/cursor-alternatives.html" if n == "Cursor" else f"/alternatives/{slug(n)}.html"
    def cl(n): return CAP_LABEL.get(CAPS[n][0], CAPS[n][0])
    def joblab(c): return CAP_LABEL.get(c, c)
    def raised(n):
        r = REC[slug(n)]; return [c for c in r["real"] if c["kind"] == "raise"]
    def f(n, k): return TD[n]["F"][k]
    def src(fx):
        st, lab, u, k = fx
        if not u: return ""
        return f' <span class="small">(<a href="{e(u)}" rel="noopener" target="_blank">source<span class="skip"> (opens in a new tab)</span></a>, checked {k})</span>'
    def pricetxt(n):
        t = TD[n]; m, a = t["mm"], t["ma"]
        if m is not None: return usd(m) + "/mo" + (f" ({usd(a)}/mo yearly)" if a is not None and a != m else "")
        if a is not None: return usd(a) + "/mo billed yearly"
        return "Price: check site"
    def vs_price(x, n):
        """Same main job only. (state, alt value, own value, billing, tier) using the site's like-for-like tier rule."""
        T = TOOL[n]; X = TOOL[x]
        for key, lab in (("monthly", "monthly billing"), ("annual", "billed yearly")):
            own = num(T[key]); v = cmp_price(X, n, key)
            if own is not None and v is not None:
                tier = TIER_MATCH[x][0] if (v != num(X[key])) else ""
                return ("cheaper" if v < own - 1e-9 else ("same" if abs(v - own) < 1e-9 else "more"), v, own, lab, tier)
        return None

    # ---------- alternatives per tool ----------
    jobs_of = {}
    for js, lab, cid, ranked in JOBS:
        for x in ranked: jobs_of.setdefault(x, []).append((js, lab, ranked))
    def related(n):
        same = samejob(n)
        sn = {x["name"] for x in same}
        prim = CAPS[n][0]; d0 = dom(TOOL[n]["url"])
        near = []
        for x in names:
            if x == n or x in sn or dom(TOOL[x]["url"]) == d0: continue
            why = []
            if prim in CAPS[x]: why.append(f"also does {joblab(prim)}")
            shared = [lab for js, lab, rk in jobs_of.get(n, []) if x in rk]
            if shared: why.append("ranked by ToolPick for " + shared[0])
            if not why and CAPS[x][0] in CAPS[n][1:]: why.append(f"its main job ({cl(x)}) is something {n} also does")
            if why: near.append((0 if shared else (1 if prim in CAPS[x] else 2), x, "; ".join(why)))
        near.sort(key=lambda r: (r[0], (num(TOOL[r[1]]["monthly"]) or num(TOOL[r[1]]["annual"]) or 1e9), r[1].lower()))
        near = near[:6]
        other = []
        if len(same) + len(near) < 3:
            used = sn | {x for _, x, _ in near} | {n}
            for t in CAT1[n]["tools"]:
                if t["name"] not in used and dom(t["url"]) != d0 and len(same) + len(near) + len(other) < 4:
                    other.append(t["name"])
        return [x["name"] for x in same], [(x, w) for _, x, w in near], other

    def satisfies(x, n, same):
        w = []
        if same:
            vp = vs_price(x, n)
            if vp and vp[0] == "cheaper": w.append("cheaper")
        for k in ("free", "privacy", "refund", "student", "yearly"):
            if f(x, k)[0] == "y": w.append(k)
        if not raised(x): w.append("stable")
        return w

    def reasons(x, n, same):
        why, wo = [], []
        if same:
            vp = vs_price(x, n)
            if vp:
                stt, v, own, lab, tier = vp
                tn = f" (compared at its {e(tier)} tier)" if tier else ""
                if stt == "cheaper": why.append(f"<b>Costs less:</b> {usd(v)}/mo vs {usd(own)}/mo for {e(n)} ({lab}, same job){tn}, {round((own - v) / own * 100)}% less.")
                elif stt == "more": wo.append(f"Costs more: {usd(v)}/mo vs {usd(own)}/mo for {e(n)} ({lab}){tn}.")
                else: why.append(f"Same entry price as {e(n)}: {usd(v)}/mo ({lab}){tn}.")
                note = tier_note(n, x)
                if note: wo.append(e(note))
            else: wo.append(f"Prices can't be compared like for like with {e(n)} (different billing checked).")
        X = {k: f(x, k) for k, *_ in FACTS}; T = {k: f(n, k) for k, *_ in FACTS}
        def lc(s_): s_ = s_.split("; team plans")[0]; return s_[0].lower() + s_[1:]
        if X["free"][0] == "y" and T["free"][0] != "y": why.append(f"<b>Real free plan</b> ({e(n)} has none): {e(X['free'][1])}." + src(X["free"]))
        elif X["free"][0] != "y" and T["free"][0] == "y": wo.append(f"No real free plan ({e(n)} has one).")
        tk = {"y": 3, "p": 2, "n": 1}
        if X["privacy"][0] == "y" and T["privacy"][0] != "y":
            why.append(f"<b>{e(X['privacy'][1])}</b>" + (f" ({e(n)}: {e(lc(T['privacy'][1]))})" if T["privacy"][0] != "u" else f" (not checked for {e(n)})") + "." + src(X["privacy"]))
        elif X["privacy"][0] in "pn" and T["privacy"][0] in "yp" and tk[X["privacy"][0]] < tk[T["privacy"][0]]: wo.append(f"Privacy: {e(X['privacy'][1])}.")
        if X["refund"][0] == "y" and T["refund"][0] != "y":
            why.append(f"<b>{e(X['refund'][1])}</b>" + (f" ({e(n)}: {e(lc(T['refund'][1]))})" if T["refund"][0] != "u" else f" (not checked for {e(n)})") + "." + src(X["refund"]))
        elif X["refund"][0] in "pn" and T["refund"][0] == "y": wo.append(f"Refunds: {e(X['refund'][1])}.")
        if X["student"][0] == "y" and T["student"][0] != "y": why.append(f"<b>{e(X['student'][1])}</b>." + src(X["student"]))
        if X["yearly"][0] == "y" and T["yearly"][0] == "n": why.append(f"<b>{e(X['yearly'][1])}</b> ({e(n)}: {e(T['yearly'][1][0].lower() + T['yearly'][1][1:])}).")
        rx, rn = raised(x), raised(n)
        if rn and not rx: why.append(f"<b>No price rise recorded</b> since we started tracking it on {nice(REC[slug(x)]['first'])} ({e(n)} raised a price on {nice(rn[0]['date'])}).")
        elif rx: wo.append(f"Raised a price on {nice(rx[0]['date'])} (<a href=\"/ai-price-history.html#t-{slug(x)}\">price history</a>).")
        if x in BEST_OF: why.append(f"ToolPick Best Value pick for {e(', '.join(next(c['name'] for c in CATS if c['id'] == i) for i in BEST_OF[x]))}.")
        lim = limitation(TOOL[x])
        if lim and not lim.startswith("We haven't recorded") and not any(lim[:30] in w for w in wo): wo.append(e(lim))
        return why, wo

    def facts_html(x):
        chips = "".join(f'<li class="{f(x, k)[0]}"><b aria-hidden="true">{ICON[f(x, k)[0]][0]}</b>{e(lab)}<span class="skip">: {ICON[f(x, k)[0]][1]}</span></li>' for k, lab, _ in FACTS)
        dl = "".join(f'<dt>{e(lab)}</dt><dd>{e(f(x, k)[1])}' + src(f(x, k)) + (f' · <a href="{g}">guide</a>' if g else "") + '</dd>' for k, lab, g in FACTS)
        r = REC[slug(x)]
        dl += f'<dt>Price history</dt><dd>' + (f'{len(r["real"])} price move{"s" if len(r["real"]) != 1 else ""} since {nice(r["first"])}' if r["real"] else f'No price change found since {nice(r["first"])}') + f' · <a href="/ai-price-history.html#t-{slug(x)}">details</a></dd>'
        t = TD[x]
        dl += f'<dt>Prices</dt><dd>{e(t["p"])} <span class="small">(<a href="{e(t["pr"])}" rel="noopener" target="_blank">official pricing<span class="skip"> for {e(x)} (opens in a new tab)</span></a>, checked {t["k"]})</span></dd>'
        return f'<ul class="a68i" aria-label="Facts for {e(x)}">{chips}</ul>', dl

    def card(x, n, grp, note=""):
        same = grp == "same"
        why, wo = reasons(x, n, same)
        w = satisfies(x, n, same)
        chips, dl = facts_html(x)
        bd = ('<span class="badge b-best">BEST VALUE</span>' if x in BEST_OF else "") + ('<span class="badge b-free">FREE PLAN</span>' if f(x, "free")[0] == "y" else "")
        cmpu = cmpmap.get(frozenset((x, n))) or f"/compare-builder.html?tools={slug(n)},{slug(x)}"
        cmpl = f"{e(n)} vs {e(x)}" if frozenset((x, n)) in cmpmap else f"Compare with {e(n)}"
        return (f'<article class="card a68k" id="a-{slug(x)}" data-w="{" ".join(w)}"><h3><a href="{turl(x)}">{e(x)}</a> <span class="pr">{pricetxt(x)}</span></h3>'
                f'<p class="small">{e(TD[x]["d"])} Main job: {e(cl(x))}.' + (f" <i>{e(note[0].upper() + note[1:])}.</i>" if note else "") + f'</p>{("<p>" + bd + "</p>") if bd else ""}'
                + (f'<h4>Why switch</h4><ul class="why">{"".join(f"<li>{r}</li>" for r in why)}</ul>' if why else f'<h4>Why switch</h4><p class="small">No clear edge over {e(n)} on the facts we check (price, free plan, AI training, refunds, student deal, yearly saving, price rises). It may still fit a different need.</p>')
                + (f'<h4>Keep in mind</h4><ul class="wo">{"".join(f"<li>{r}</li>" for r in wo[:3])}</ul>' if wo else "")
                + chips + f'<details><summary>All facts with sources</summary><dl>{dl}</dl></details>'
                + f'<p class="a68a"><a href="{turl(x)}">{e(x)} prices &amp; review</a><a href="{cmpu}">{cmpl}</a></p></article>'), w

    def quick(n, same, near, other):
        """Short answers per reason: (key, label, html, pick or None, tool itself has it)."""
        cand = [(x, True) for x in same] + [(x, False) for x, _ in near]
        out = []
        cs = [(vs_price(x, n), x) for x in same]
        cs = sorted([(v, x) for v, x in cs if v and v[0] == "cheaper"], key=lambda r: (r[0][1], r[1].lower()))
        if cs:
            (stt, v, own, lab, tier), x = cs[0]
            out.append(("cheaper", "Cheaper", f'<a href="#a-{slug(x)}">{e(x)}</a>: {usd(v)}/mo vs {usd(own)}/mo ({lab}, same job{", " + e(tier) + " tier" if tier else ""}).', x, False))
        elif same and (num(TOOL[n]["monthly"]) is not None or num(TOOL[n]["annual"]) is not None):
            out.append(("cheaper", "Cheaper", f"None: {e(n)} already has the lowest checked entry price among tools with the same main job ({e(cl(n))}) on comparable billing.", None, True))
        elif not same:
            out.append(("cheaper", "Cheaper", f"Not compared: no tool in our list has the same main job ({e(cl(n))}), and we don't compare prices across different jobs.", None, False))
        else:
            out.append(("cheaper", "Cheaper", f"Not compared: we have no checked price for {e(n)}.", None, False))
        NONE = {"free": "has a real free plan", "privacy": "is confirmed not to train on your content by default", "refund": "states a refund window", "student": "has a student deal we've confirmed"}
        SELF = {"free": "{n} has one: {l}.", "privacy": "{n} already doesn't train on your content by default.", "refund": "{n} has one: {l}.", "student": "{n} has one: {l}."}
        def best(k, sentence):
            ys = [(x, s_) for x, s_ in cand if f(x, k)[0] == "y"]
            if f(n, k)[0] == "y":
                h = e(SELF[k].format(n=n, l=f(n, k)[1][0].lower() + f(n, k)[1][1:])) + src(f(n, k))
                if ys: h += " Alternatives with one too: " + ", ".join(f'<a href="#a-{slug(x)}">{e(x)}</a>' for x, _ in ys[:3]) + "."
                out.append((k, sentence, h, ys[0][0] if ys else None, True)); return
            if ys:
                x, s_ = ys[0]
                out.append((k, sentence, f'<a href="#a-{slug(x)}">{e(x)}</a>' + ("" if s_ else " (close alternative)") + f": {e(f(x, k)[1])}." + src(f(x, k)), x, False)); return
            out.append((k, sentence, "None of these alternatives " + NONE[k] + f" in our checks ({e(n)}: {e(f(n, k)[1][0].lower() + f(n, k)[1][1:])}).", None, False))
        best("free", "Free plan"); best("privacy", "More private"); best("refund", "Refund window"); best("student", "Student deal")
        rn = raised(n)
        if rn:
            st_ = [x for x, s_ in cand if not raised(x)]
            if st_: out.append(("stable", "No price rise", f'<a href="#a-{slug(st_[0])}">{e(st_[0])}</a>: no price rise recorded since {nice(REC[slug(st_[0])]["first"])} ({e(n)} raised a price on {nice(rn[0]["date"])}).', st_[0], False))
        return out

    def now_panel(n):
        t = TD[n]
        rows = f'<dt>Price</dt><dd>{e(t["p"])} <span class="small">(<a href="{e(t["pr"])}" rel="noopener" target="_blank">official pricing<span class="skip"> for {e(n)} (opens in a new tab)</span></a>, checked {t["k"]})</span></dd>'
        rows += "".join(f'<dt>{e(lab)}</dt><dd><span aria-hidden="true">{ICON[f(n, k)[0]][0]}</span> {e(f(n, k)[1])}{src(f(n, k))}</dd>' for k, lab, _ in FACTS)
        r = REC[slug(n)]; rn = raised(n)
        rows += f'<dt>Price history</dt><dd>' + (f'Raised a price on {nice(rn[0]["date"])}' if rn else (f'{len(r["real"])} price move{"s" if len(r["real"]) != 1 else ""}' if r["real"] else "No price change found")) + f' since {nice(r["first"])} · <a href="/ai-price-history.html#t-{slug(n)}">details</a></dd>'
        return f'<section class="card a68now" aria-labelledby="a68n"><h2 id="a68n" class="h3" style="margin:0;font-size:1.1rem">What you get with {e(n)} now</h2><dl>{rows}</dl></section>'

    SUMM = {}
    def body_for(n, standalone=True):
        same, near, other = related(n)
        cards, counts, allw = [], {k: 0 for k, *_ in KEYS}, []
        groups = []
        if same:
            cs = sorted(same, key=lambda x: (0 if (vs_price(x, n) or ("",))[0] == "cheaper" else 1, (vs_price(x, n) or (0, 1e9))[1], x.lower()))
            h = []
            for x in cs:
                c, w = card(x, n, "same"); h.append(c); allw.append(w)
            groups.append(f'<section class="a68g" aria-labelledby="g68s"><h2 id="g68s">Same main job: {e(cl(n))} (<span class="gc" data-t="{len(cs)}">{len(cs)}</span>)</h2><p class="small">These do what {e(n)} mainly does, so prices are compared like for like: monthly with monthly, yearly with yearly, lighter entry tiers at a comparable tier.</p><div class="a68l">{"".join(h)}</div></section>')
            same = cs
        if near:
            h = []
            for x, why in near:
                c, w = card(x, n, "near", why); h.append(c); allw.append(w)
            groups.append(f'<section class="a68g" aria-labelledby="g68n"><h2 id="g68n">Close alternatives (<span class="gc" data-t="{len(near)}">{len(near)}</span>)</h2><p class="small">Their main job is different, but they also cover what you might use {e(n)} for. Prices aren\'t compared across different main jobs, so check the features you need.</p><div class="a68l">{"".join(h)}</div></section>')
        if other:
            h = []
            for x in other:
                c, w = card(x, n, "other", f"other {CAT1[n]['name']} tool, different main job"); h.append(c); allw.append(w)
            groups.append(f'<section class="a68g" aria-labelledby="g68o"><h2 id="g68o">Other {e(CAT1[n]["name"].lower())} tools (<span class="gc" data-t="{len(other)}">{len(other)}</span>)</h2><p class="small">No closer match in our list. These are in the same category but do a different main job, listed so you can see your options.</p><div class="a68l">{"".join(h)}</div></section>')
        for w in allw:
            for k in w: counts[k] += 1
        total = len(allw)
        chips = "".join(f'<button type="button" data-w="{k}" aria-pressed="false"{" disabled" if not counts[k] else ""} title="{e(sub)}">{e(lab)} <span class="n">({counts[k]})</span></button>' for k, lab, sub in KEYS if k != "cheaper" or same)
        L = json.dumps({k: lab for k, lab, _ in KEYS})
        qs = quick(n, same, near, other)
        qhtml = "".join(f'<li><b class="k">{e(lab)}</b><span>{txt}</span></li>' for k, lab, txt, _, _ in qs)
        nsame = len(same)
        lead = (f'{nsame} tool{"s that do" if nsame != 1 else " that does"} the same main job as {e(n)} ({e(cl(n))})' if nsame else f'No tool in our list does the same main job as {e(n)} ({e(cl(n))}), so here {"are" if len(near) + len(other) != 1 else "is"}')
        lead += ((" and " if nsame else " ") + f'{len(near)} close alternative{"s" if len(near) != 1 else ""}' if near else "") + ((" and " if nsame or near else " ") + f'{len(other)} other {e(CAT1[n]["name"].lower())} tool{"s" if len(other) != 1 else ""}' if other else "")
        lead += ". Pick why you want to switch (cheaper, free, more private, refunds, student deal) and see which alternatives fit, with every fact linked to the official page and the date we checked."
        # side-by-side table
        rows = []
        for x, me in [(n, True)] + [(x, False) for x in same] + [(x, False) for x, _ in near] + [(x, False) for x in other]:
            cells = "".join(f'<td data-l="{e(lab)}"><span aria-hidden="true">{ICON[f(x, k)[0]][0]}</span> {e(f(x, k)[1])}</td>' for k, lab, _ in FACTS)
            rx = raised(x)
            rows.append(f'<tr{" class=me" if me else ""}><th scope="row"><a href="{turl(x) if me else "#a-" + slug(x)}">{e(x)}</a>{" <span class=small>(this tool)</span>" if me else ""}<br><span class="small">{e(cl(x))}</span></th><td data-l="Entry price">{pricetxt(x)}<br><span class="small">checked {TD[x]["k"]}</span></td>{cells}<td data-l="Price rise">{"Raised " + nice(rx[0]["date"]) if rx else "None recorded"}</td></tr>')
        table = (f'<h2 id="a68tbl">All facts side by side</h2><div class="tw a68t"><table><caption class="small" style="text-align:left;padding:12px 16px">✓ yes · ~ partly · ✕ no · ? not checked yet. From official pricing, privacy, refund and student pages; each tool\'s card above links the exact source and checked date.</caption>'
                 f'<tr><th scope="col">Tool</th><th scope="col">Entry price</th>' + "".join(f'<th scope="col">{e(lab)}</th>' for _, lab, _ in FACTS) + f'<th scope="col">Price rise</th></tr>{"".join(rows)}</table></div>')
        finder = (f'<div class="a68f" role="region" aria-labelledby="a68fh"><h2 id="a68fh">Why do you want to switch from {e(n)}?</h2><div class="a68c" role="group" aria-label="Reasons to switch">{chips}'
                  f'<button type="button" id="a68r">Clear</button></div><p id="a68st" class="small" role="status" aria-live="polite">Showing all {total} alternatives. Pick one or more reasons to narrow them down.</p></div>'
                  f'<script type="application/json" id="a68L">{L}</script>')
        empty = f'<p class="a68e" id="a68e" hidden>No alternative matches all of those reasons. Clear one reason, or <a href="/help-me-choose.html">find a tool by job and budget</a>.</p>'
        top = f'<div class="a68top">{now_panel(n)}<section class="card" aria-labelledby="a68qh"><h2 id="a68qh" style="margin:0;font-size:1.1rem">Short answer</h2><ul class="a68q">{qhtml}</ul></section></div>'
        SUMM[n] = dict(p=path(n), same=same, near=[x for x, _ in near], other=other, q={k: (t, pk, sf) for k, _, t, pk, sf in qs}, total=total)
        jump = f'<p class="small a68j"><a href="#a68fh">Filter by your reason to switch ↓</a> · <a href="#a68tbl">All facts side by side ↓</a></p>'
        return lead, jump + top + finder + empty + "".join(groups) + table + f"<script>{JS}</script>", qs, same, near, other

    PAGES = []
    for n in names:
        if n == "Cursor": continue
        p = path(n)
        lead, main, qs, same, near, other = body_for(n)
        cat = CAT1[n]
        rel = [f'<a href="{turl(n)}">{e(n)} prices &amp; review</a>']
        if n in FREE_ALT: rel.append(f'<a href="{FREE_ALT[n]}">Free alternatives to {e(n)} only</a>')
        if CAPS[n][0] == "code-assistant": rel.append('<a href="/cursor-alternatives.html">Cursor alternatives</a>')
        js = next((j for j in JOBS if n in j[3]), None)
        if js: rel.append(f'<a href="/help-me-choose.html?job={js[0]}">Find my tool for {e(js[1])}</a>')
        rel.append(f'<a href="/best-ai-{cat["id"]}-tools.html">Best AI {e(cat["name"].lower())} tools</a>')
        rel.append(f'<a href="{HUB}">Alternatives to all {len(names)} tools</a>')
        qd = {k: t for k, _, t, _, _ in qs}; qp = {k: (pk, sf) for k, _, _, pk, sf in qs}
        strip = lambda h: re.sub(r"<[^>]+>", "", h).replace("&amp;", "&").replace("&#x27;", "'").replace("&quot;", '"').strip()
        qa = [(f"What is the cheapest alternative to {n}?", strip(qd["cheaper"]))]
        qa.append((f"Is there a free alternative to {n}?", strip(qd["free"]) + " A real free plan is one you can keep using; trials and one-time credits don't count."))
        if f(n, "privacy")[0] == "u": qa.append((f"Which {n} alternative doesn't train AI on my data?", strip(qd["privacy"]) + f" We haven't checked {n}'s own data-training policy yet."))
        else: qa.append((f"Does {n} train AI on my data, and which alternative doesn't?", f"{n}: {f(n, 'privacy')[1]} (official page checked {f(n, 'privacy')[3]}). " + strip(qd["privacy"])))
        qa.append((f"Which tools do the same job as {n}?", (", ".join(same) + f" have the same main job ({cl(n)})." if same else f"None in our list has the same main job ({cl(n)}).") + (f" Close alternatives: {', '.join(x for x, _ in near)}." if near else "")))
        fh, fld = faq(qa)
        alts = same + [x for x, _ in near] + other
        body = (f'{CSS}<p class="small"><a href="{HUB}">Alternatives</a> › {e(n)}</p><h1>{e(n)} alternatives</h1><p class="tag">{lead}</p>{main}'
                f'<p class="small">How we pick: same main job first (the only group where we call one tool cheaper), then tools ToolPick ranks for the same job or that also do it. Facts are copied from official pages with the date we checked; "not checked" means we don\'t guess. Not hands-on tested. <a href="/how-we-pick.html">How we pick</a></p>'
                f'{fh}<p class="small">Related: {" · ".join(rel)}</p>')
        bits = []
        for k_, lb_ in (("cheaper", "cheaper"), ("free", "free"), ("privacy", "more private")):
            if qp[k_][0] and not qp[k_][1]: bits.append(f"{lb_}: {qp[k_][0]}")
        desc = (f"{len(alts)} {n} alternatives" + (f" ({'; '.join(bits)})" if bits else "") + f": {', '.join(alts[:5])}. Compare by price, free plan, AI training on your data, refunds and student deals, from official pages.")[:300]
        title = f"{n} Alternatives (2026): Cheaper, Free & More Private Options | ToolPick"
        ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": f"{n} alternatives", "url": BASE + p,
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x, "url": BASE + turl(x)} for i, x in enumerate(alts)]},
              fld, crumbs([("ToolPick", "/"), ("Alternatives", HUB), (f"{n} alternatives", p)])]
        existed = p in URLS
        page(p, title, desc, body, ld)
        if existed: URLS.pop()
        _lm[p] = V68_DATE; PAGES.append(p)

    # ---------- Cursor: keep the hand-checked page, add the same reason finder ----------
    lead, main, qs, same, near, other = body_for("Cursor")
    fp = "public/cursor-alternatives.html"; h = open(fp).read()
    if ' a68f"' not in h and "<h2>FAQ</h2>" in h:
        sec = (f'{CSS}<section aria-labelledby="a68cur" style="margin:var(--s6) 0"><h2 id="a68cur">Pick your reason to switch from Cursor</h2><p class="small">{lead}</p>{main}</section>')
        h = h.replace("<h2>FAQ</h2>", sec + "<h2>FAQ</h2>", 1)
        open(fp, "w").write(h); _lm["/cursor-alternatives.html"] = V68_DATE; PAGES.append("/cursor-alternatives.html")

    # ---------- hub ----------
    secs = []
    for c in CATS:
        cards = []
        for t in c["tools"]:
            n = t["name"]
            if CAT1[n] is not c: continue
            s = SUMM[n]; q = s["q"]
            strip = lambda h_: re.sub(r"<[^>]+>", "", h_).strip()
            def one(k, lab):
                t_, pk, sf = q[k]
                if k == "cheaper":
                    return f'<p><b>{lab}:</b> ' + (e(pk) if pk else f'<span class="small">{"none cheaper" if s["same"] else "not compared (no same-job tool)"}</span>') + '</p>'
                if sf: return f'<p><b>{lab}:</b> {e(n)} itself' + (f' (also {e(pk)})' if pk else '') + '</p>'
                return f'<p><b>{lab}:</b> ' + (e(pk) if pk else '<span class="small">none in our checks</span>') + '</p>'
            k_ = " ".join([n, cl(n), c["name"]] + s["same"] + s["near"]).lower()
            cards.append(f'<article class="card" data-k="{e(k_)}"><h3><a href="{s["p"]}">{e(n)} alternatives</a></h3><p class="small">{len(s["same"])} same job · {len(s["near"])} close{(" · " + str(len(s["other"])) + " other") if s["other"] else ""} · {e(cl(n))}</p>'
                         + one("cheaper", "Cheaper") + one("free", "Free") + one("privacy", "More private") + '</article>')
        secs.append(f'<section class="a68hs" aria-labelledby="h68-{c["id"]}"><h2 id="h68-{c["id"]}">{e(c["name"])}</h2><div class="a68h">{"".join(cards)}</div></section>')
    qa = [("How does ToolPick choose alternatives?", "Tools with the same main job come first, and only they get a 'cheaper' verdict (monthly with monthly, yearly with yearly). Then close alternatives: tools that also do that job or that ToolPick ranks for the same job. If there are fewer than 3, other tools in the same category are listed and labelled as a different main job."),
          ("Where do the facts come from?", "Prices from each official pricing page; free plans, AI training on your data, refunds and student deals from official pricing, privacy, help and student pages. Every fact shows its source link and the date we checked it. Facts we haven't checked show 'not checked' and are never counted as a match."),
          ("What does 'More private' mean?", "The tool's official privacy pages say it doesn't train AI models on your content by default, or only if you opt in.")]
    fh, fld = faq(qa)
    hub = (f'{CSS}<p class="small"><a href="/guides.html">Guides</a> › Alternatives</p><h1>Alternatives to every AI tool we track</h1>'
           f'<p class="tag">Pick the tool you use now ({len(names)} tools). Each page shows what does the same job, which is cheaper, which is free, which doesn\'t train on your data and which has a refund window or student deal, with official sources and checked dates.</p>'
           f'<p><label for="a68q"><b>Find your tool</b></label><br><input id="a68q" class="a68s" type="search" placeholder="e.g. ChatGPT, Midjourney, transcription" autocomplete="off"></p><p id="a68hst" class="small" role="status" aria-live="polite"></p>'
           + "".join(secs) +
           f'<p class="small">Free only? <a href="/free.html">Can I do it for free?</a> · <a href="/free-plan-limits.html">Free plan limits</a> · Not sure what you need? <a href="/help-me-choose.html">Find my AI tool</a></p>{fh}<script>{HUBJS}</script>')
    existed = HUB in URLS
    page(HUB, f"AI Tool Alternatives ({len(names)} Tools): Cheaper, Free & More Private Options | ToolPick",
         f"Alternatives to all {len(names)} AI tools we track (ChatGPT, Claude, Midjourney, ElevenLabs, Cursor, Canva...): same-job tools, cheaper and free options, tools that don't train on your data, refunds and student deals, from official pages.",
         hub, [{"@context": "https://schema.org", "@type": "ItemList", "name": "AI tool alternatives", "url": BASE + HUB,
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{n} alternatives", "url": BASE + path(n)} for i, n in enumerate(names)]},
               fld, crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("Alternatives", HUB)])])
    if existed: URLS.pop()
    _lm[HUB] = V68_DATE; PAGES.append(HUB)
    nsame0 = sum(1 for n in names if not SUMM[n]["same"])
    return PAGES, SUMM, nsame0


def link_v68(ctx, SUMM):
    """Every tool page: an 'Alternatives' box (replaces the v49 one-liner); every /compare/ page links both tools' pages."""
    e = ctx["e"]; slug = ctx["slug"]; COMPARISONS = ctx["COMPARISONS"]; cnames = ctx["cnames"]; changed = []
    strip = lambda h_: re.sub(r"<[^>]+>", "", h_).strip()
    for n, s in SUMM.items():
        fp = f"public/tools/{slug(n)}.html"
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' tp68"' in h: continue
        h = re.sub(r'<p class="pick small v49">.*?</p>', "", h, count=1)
        li = []
        lab = {"cheaper": "Cheaper", "free": "Free plan", "privacy": "More private", "refund": "Refund window", "student": "Student deal", "stable": "No price rise"}
        for k in ("cheaper", "free", "privacy", "stable"):
            if k not in s["q"]: continue
            v, pk, sf = s["q"][k]
            if pk and not sf:
                v2 = re.sub(r'href="#a-', f'href="{s["p"]}#a-', v)
                li.append(f"<li><b>{lab[k]}:</b> {v2}</li>")
        tot = len(s["same"]) + len(s["near"]) + len(s["other"])
        sj = ", ".join(f'<a href="{s["p"]}#a-{slug(x)}">{e(x)}</a>' for x in s["same"][:5])
        box = ('<style>.tp68 ul{margin:6px 0 0;padding-left:1.1em}.tp68 li{margin:2px 0}.tp68 li::marker{color:var(--ok)}.tp68 li>a,.tp68 p>a{display:inline;padding:0}</style>' + f'<section class="card tp68 pick" style="margin-bottom:16px" id="alternatives" aria-labelledby="al68"><h2 id="al68" style="margin:0;font-size:1.1rem">{e(n)} alternatives</h2>'
               + (f'<p class="small" style="margin:4px 0 0">Same main job: {sj}</p>' if sj else "")
               + (f'<ul>{"".join(li)}</ul>' if li else f'<p class="small" style="margin:6px 0 0">None of the {tot} alternatives beats {e(n)} on price, free plan or privacy in our checks, but they may fit a different need.</p>')
               + f'<p style="margin:8px 0 0"><a href="{s["p"]}"><b>See all {tot} {e(n)} alternatives by reason to switch →</b></a> <span class="small">cheaper, free, more private, refunds, student deals</span></p></section>')
        a = None
        for cand in ('<section class="card tbp"', '<section class="verdict'):
            if cand in h: a = cand; break
        if not a: continue
        h = h.replace(a, box + a, 1)
        open(fp, "w").write(h); changed.append(f"/tools/{slug(n)}.html")
    for x in COMPARISONS:
        fp = f"public/compare/{x[0]}.html"
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' v68"' in h: continue
        ls = [f'<a href="{SUMM[nn]["p"]}">{e(nn)} alternatives</a>' for nn in cnames(x) if nn in SUMM]
        if not ls: continue
        new = '<p class="small v68">Neither quite right? ' + " · ".join(ls) + " (cheaper, free, more private)</p>"
        h2 = re.sub(r'<p class="small v49">See alternatives: .*?</p>', new, h, count=1)
        if h2 == h: h2 = h.replace("</h1>", "</h1>" + new, 1)
        open(fp, "w").write(h2); changed.append(f"/compare/{x[0]}.html")
    return changed
