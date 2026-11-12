"""v69: Which AI tools train on your data? Privacy, refund & student-deal checker (/ai-privacy-refund-checker.html).
One page for all tools: does it train AI on your content (no / only if you opt in / yes, with an opt-out / yes, no opt-out
found / unclear), the refund rule (window / narrow cases / case by case / no refunds), and the student deal (deal / ask /
through your school / none listed). Filters with URL state (?train=&refund=&student=&cat=&q=&sort=), clickable summary
boxes, a card per tool with the official source link, exact quote and checked date for every fact, and a box on every
tool page. Facts come only from the merged v52/v54/v48/v57 lists plus the v69 rows read on official pages on 2026-11-12;
anything we haven't read says "not checked" and never matches a filter."""
import json, re

V69_DATE = "2026-11-12"
PATH = "/ai-privacy-refund-checker.html"
TRAIN = [("no", "Doesn't train on your content", "n"), ("optin", "Only if you opt in", "c"), ("optout", "Trains by default, you can opt out", "yp"),
         ("noopt", "Trains, no opt-out found", "x"), ("unclear", "Unclear on its pages", "u")]
REFUND = [("window", "Refund window"), ("narrow", "Refunds in narrow cases"), ("case", "Case by case"), ("none", "No refunds"), ("unclear", "Unclear on its pages")]
STUDENT = [("deal", "Student deal"), ("ask", "Ask for a student price"), ("school", "Only through your school"), ("none", "No student deal listed")]
TONE = {"no": "y", "optin": "y", "optout": "p", "noopt": "n", "unclear": "u", "window": "y", "narrow": "p", "case": "p", "none": "n", "deal": "y", "ask": "p", "school": "p", "nc": "u"}


def hrs(h): return f"{h // 24}-day" if h >= 48 and h % 24 == 0 else f"{h}-hour"


def build_v69(ctx):
    page = ctx["page"]; e = ctx["e"]; slug = ctx["slug"]; turl = ctx["turl"]; BASE = ctx["BASE"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]
    _lm = ctx["_lm"]; URLS = ctx["URLS"]; CATS = ctx["CATEGORIES"]; T = ctx["tools"]; rshort = ctx["_rshort"]
    PV = ctx["_PV57"]; RF = ctx["_RF57"]; ST = ctx["_ST57"]; STN = ctx["_STN57"]; PLO = ctx["_PLO57"]; RLO = ctx["_RLO57"]
    SCHOOL = {a: (b, c, d) for a, b, c, d in T.STUDENT_SCHOOL_ONLY}
    V57R = [r["t"] for r in T.V57_REFUNDS]; V57P = [r["t"] for r in T.V57_PRIVACY]
    cat1 = {}
    for c in CATS:
        for t in c["tools"]: cat1.setdefault(t["name"], c)
    names = sorted(cat1, key=str.lower)
    def alt(n): return "/cursor-alternatives.html" if n == "Cursor" else f"/alternatives/{slug(n)}.html"
    def src(u, d, n, what):
        return f'<p class="s69"><a href="{e(u)}" rel="noopener" target="_blank">Official {what}<span class="skip"> for {e(n)} (opens in a new tab)</span></a> · checked {d}</p>'
    ROWS = {}
    for n in names:
        R = {}
        # ---- AI training ----
        if n in PV:
            p = PV[n]; k = p["k"]
            code = {"n": "no", "c": "optin", "y": "optout", "p": "optout", "x": "noopt", "u": "unclear"}[k]
            d = p.get("ck") or (T.V57_CHECKED if n in V57P else T.PRIVACY_CHECKED)
            lab = {"n": "Doesn't train on your content", "c": "Only if you opt in", "y": "Trains by default, you can opt out",
                   "p": "Trains by default, only paid plans can opt out", "x": "Trains, no opt-out found", "u": "Unclear: the default isn't stated"}[k]
            det = f'<p>{e(p["ind"])}</p>'
            if p.get("steps") and k in "yupx": det += f'<p><b>How to opt out:</b> {e(p["steps"])}</p>'
            elif p.get("steps"): det += f'<p class="small">{e(p["steps"])}</p>'
            if p.get("biz"): det += f'<p class="small"><b>Team / business:</b> {e(p["biz"])}</p>'
            elif p.get("bk") == "n": det += '<p class="small"><b>Team / business:</b> not used for training by default.</p>'
            if p.get("note"): det += f'<p class="small">{e(p["note"])}</p>'
            det += f'<details><summary>What the page says</summary><blockquote>“{e(p["q"])}”</blockquote></details>' + src(p["src"], d, n, "page")
            R["train"] = (code, lab, det, d)
        elif n in PLO:
            R["train"] = ("unclear", "Unclear on its pages", f'<p class="small">We read its pages but they don\'t say it plainly: {e(PLO[n])}.</p>', T.PRIVACY_CHECKED)
        else:
            R["train"] = ("nc", "Not checked yet", '<p class="small">We haven\'t found a plain statement on its official pages yet, so we don\'t guess.</p>', "")
        # ---- refunds ----
        if n in RF:
            r = RF[n]; d = r.get("ck") or (T.V57_CHECKED if n in V57R else T.REFUND_CHECKED)
            if r["k"] == "w" and r["wm"]:
                code = "window"; w = hrs(r["wm"]) + (f" ({hrs(r['wy'])} on yearly)" if r.get("wy") and r["wy"] != r["wm"] else "")
                lab = f"{w[0].upper() + w[1:]} refund window"
            elif r["k"] == "w": code, lab = "narrow", "Refunds in narrow cases"
            elif r["k"] == "c": code, lab = "case", "Case by case"
            else: code, lab = "none", "No refunds"
            det = f'<p>{e(rshort(r))}</p>'
            if r["k"] != "n" and r.get("cond") and r["wm"]: det += f'<p class="small"><b>Conditions:</b> {e(r["cond"])}.</p>'
            if r.get("eu"): det += f'<p class="small">{e(r["eu"])}</p>'
            if r.get("cancel"): det += f'<p class="small"><b>Cancel:</b> {e(r["cancel"])}' + (f' ({e(r["notice"])})' if r.get("notice") else "") + '</p>'
            det += f'<details><summary>What the page says</summary><blockquote>“{e(r["q"])}”</blockquote></details>' + src(r["sr"], d, n, "page")
            R["refund"] = (code, lab, det, d)
        elif n in RLO:
            R["refund"] = ("unclear", "Unclear on its pages", f'<p class="small">{e(RLO[n][0].upper() + RLO[n][1:])}.</p>', T.REFUND_CHECKED)
        else:
            R["refund"] = ("nc", "Not checked yet", '<p class="small">We haven\'t read a clear refund rule on its official pages yet.</p>', "")
        # ---- student ----
        if n in ST:
            o = ST[n]; d = o.get("ck") or T.STUDENT_CHECKED
            code = "deal" if o["kind"] in ("free", "off") else "ask"
            det = f'<p>{e(o["offer"])}.</p>' + (f'<p class="small"><b>Who:</b> {e(o["elig"])}</p>' if o.get("elig") else "") + (f'<p class="small"><b>How:</b> {e(o["claim"])}</p>' if o.get("claim") else "")
            det += f'<details><summary>What the page says</summary><blockquote>“{e(o["quote"])}”</blockquote></details>' + src(o["src"], d, n, "page")
            R["student"] = (code, ("Student deal: " if code == "deal" else "") + o["badge"], det, d)
        elif n in SCHOOL:
            w_, u_, q_ = SCHOOL[n][0], SCHOOL[n][1], SCHOOL[n][2]
            R["student"] = ("school", "Only through your school", f'<p>{e(w_)}</p><details><summary>What the page says</summary><blockquote>“{e(q_)}”</blockquote></details>' + src(u_, T.STUDENT_CHECKED, n, "page"), T.STUDENT_CHECKED)
        elif n in STN:
            v = STN[n]; d = v[2] if len(v) > 2 else T.STUDENT_CHECKED
            R["student"] = ("none", "No student deal listed", f'<p>{e(v[0])}</p>' + src(v[1], d, n, "page"), d)
        else:
            R["student"] = ("nc", "Not checked yet", '<p class="small">We haven\'t checked its official pages for a student offer yet.</p>', "")
        ROWS[n] = R
    # ---------- counts ----------
    cnt = {k: {} for k in ("train", "refund", "student")}
    for n in names:
        for k in cnt: c_ = ROWS[n][k][0]; cnt[k][c_] = cnt[k].get(c_, 0) + 1
    checked = {k: sum(v for c_, v in cnt[k].items() if c_ != "nc") for k in cnt}
    new69 = {k: sum(1 for n in names if ROWS[n][k][3] == V69_DATE) for k in cnt}
    def lst(k, code): return [n for n in names if ROWS[n][k][0] == code]
    # ---------- cards ----------
    ICON = {"y": "✓", "p": "~", "n": "✕", "u": "?"}
    cards = []
    for n in names:
        R = ROWS[n]; c = cat1[n]
        parts = []
        for k, h in (("train", "Trains AI on your data?"), ("refund", "Refunds"), ("student", "Student deal")):
            code, lab, det, d = R[k]; tone = TONE[code]
            parts.append(f'<div class="f69 {tone}"><h4>{h}</h4><p class="b69"><b aria-hidden="true">{ICON[tone]}</b> {e(lab)}</p>{det}</div>')
        key = " ".join([n, c["name"]]).lower()
        cards.append(f'<article class="card c69" id="t-{slug(n)}" data-n="{e(n.lower())}" data-k="{e(key)}" data-c="{c["id"]}" data-train="{R["train"][0]}" data-refund="{R["refund"][0]}" data-student="{R["student"][0]}"'
                     f' data-ck="{max(R[k][3] for k in R)}" data-rw="{(RF[n]["wm"] or 0) if n in RF and RF[n]["k"] == "w" else 0}">'
                     f'<h3><a href="{turl(n)}">{e(n)}</a> <span class="small">{e(c["name"])}</span></h3>{"".join(parts)}'
                     f'<p class="a69"><a href="{turl(n)}">{e(n)} prices &amp; review</a><a href="{alt(n)}?want=privacy">More private alternatives</a></p></article>')
    # ---------- filters ----------
    def sel(id_, lab, opts, cn):
        o = f'<option value="">Any</option>' + "".join(f'<option value="{v}">{e(t)} ({cn.get(v, 0)})</option>' for v, t, *_ in opts) + (f'<option value="nc">Not checked yet ({cn.get("nc", 0)})</option>' if cn.get("nc") else "")
        return f'<label class="l69"><span>{lab}</span><select id="{id_}" name="{id_[1:]}">{o}</select></label>'
    catopt = '<option value="">All categories</option>' + "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATS)
    presets = [("train=no", f"Doesn't train on my data ({cnt['train'].get('no', 0)})"), ("train=optin", f"Only if I opt in ({cnt['train'].get('optin', 0)})"),
               ("refund=window", f"Has a refund window ({cnt['refund'].get('window', 0)})"), ("student=deal", f"Student deal ({cnt['student'].get('deal', 0)})"),
               ("train=noopt", f"Trains, no opt-out ({cnt['train'].get('noopt', 0)})")]
    pre = "".join(f'<a class="p69" href="{PATH}?{q}">{e(l)}</a>' for q, l in presets)
    filt = (f'<form class="fl69" id="f69" action="{PATH}" method="get" role="search" aria-label="Filter AI tools by privacy, refunds and student deals">'
            + sel("x69t", "Trains on your data?", TRAIN, cnt["train"]) + sel("x69r", "Refunds", REFUND, cnt["refund"]) + sel("x69s", "Student deal", STUDENT, cnt["student"])
            + f'<label class="l69"><span>Category</span><select id="x69c" name="cat">{catopt}</select></label>'
            + '<label class="l69"><span>Sort</span><select id="x69o" name="sort"><option value="az">A to Z</option><option value="private">Most private first</option><option value="refund">Longest refund window</option><option value="checked">Most recently checked</option></select></label>'
            + '<label class="l69 q"><span>Find a tool</span><input id="x69q" name="q" type="search" placeholder="e.g. ChatGPT, Canva, video" autocomplete="off"></label>'
            + '<p class="bt69"><button type="button" id="x69x">Clear all</button></p></form>'
            + f'<p id="st69" class="small" role="status" aria-live="polite">Showing all {len(names)} tools.</p>')
    # ---------- summary ----------
    def box(k, code, lab):
        n_ = cnt[k].get(code, 0); q = f"{ {'train': 'train', 'refund': 'refund', 'student': 'student'}[k]}={code}"
        return f'<a class="sb69 {TONE[code]}" href="{PATH}?{q}"><b>{n_}</b><span>{e(lab)}</span></a>'
    summ = ('<div class="sm69">'
            f'<section aria-labelledby="sm69t"><h2 id="sm69t" class="h3">Training on your data <span class="small">{checked["train"]} of {len(names)} checked</span></h2><div class="sg69">'
            + box("train", "no", "don't train on your content") + box("train", "optin", "only if you opt in") + box("train", "optout", "train by default, opt-out exists") + box("train", "noopt", "train, no opt-out found") + '</div></section>'
            f'<section aria-labelledby="sm69r"><h2 id="sm69r" class="h3">Refunds <span class="small">{checked["refund"]} of {len(names)} checked</span></h2><div class="sg69">'
            + box("refund", "window", "state a refund window") + box("refund", "narrow", "only in narrow cases") + box("refund", "case", "case by case") + box("refund", "none", "no refunds") + '</div></section>'
            f'<section aria-labelledby="sm69s"><h2 id="sm69s" class="h3">Student deals <span class="small">{checked["student"]} of {len(names)} checked</span></h2><div class="sg69">'
            + box("student", "deal", "free or discounted") + box("student", "ask", "ask for a student price") + box("student", "school", "only through your school") + box("student", "none", "none listed") + '</div></section></div>')
    def names_html(xs): return ", ".join(f'<a href="#t-{slug(x)}">{e(x)}</a>' for x in xs) or "none"
    quick = (f'<section class="card q69" aria-labelledby="q69h"><h2 id="q69h" style="margin:0;font-size:1.1rem">Short answer</h2><dl>'
             f'<dt>Don\'t train on your content</dt><dd>{names_html(lst("train", "no"))}</dd>'
             f'<dt>Only if you opt in</dt><dd>{names_html(lst("train", "optin"))}</dd>'
             f'<dt>Train by default, with an opt-out</dt><dd>{names_html(lst("train", "optout"))}</dd>'
             f'<dt>Train, no opt-out found</dt><dd>{names_html(lst("train", "noopt"))}</dd>'
             f'<dt>Longest refund windows</dt><dd>{names_html(sorted([n for n in names if ROWS[n]["refund"][0] == "window"], key=lambda x: (-RF[x]["wm"], x.lower()))[:8])}</dd>'
             f'<dt>Student deals</dt><dd>{names_html(lst("student", "deal"))}</dd></dl></section>')
    # ---------- page ----------
    qa = [("Which AI tools don't train on your data?", f"Of the {checked['train']} tools whose official pages we read, these say they don't train AI models on your content: " + ", ".join(lst("train", "no")) + ". These only do it if you opt in: " + ", ".join(lst("train", "optin")) + "."),
          ("Which AI tools train on my data with no way to opt out?", "On the pages we read, these use your content for AI training and we found no opt-out: " + ", ".join(lst("train", "noopt")) + ". Policies change; each card links the exact page and the date we read it."),
          ("Which AI subscriptions give refunds?", f"{cnt['refund'].get('window', 0)} tools state a refund window, for example " + ", ".join(sorted([n for n in names if ROWS[n]['refund'][0] == 'window'], key=lambda x: (-RF[x]['wm'], x.lower()))[:6]) + f". {cnt['refund'].get('none', 0)} say payments are non-refundable (except where the law requires)."),
          ("Where do these facts come from?", f"Only from each tool's own privacy policy, terms, trust page, help article or pricing page. Every fact shows the source link, the exact words and the date we read it ({T.PRIVACY_CHECKED} to {V69_DATE}). If we couldn't find a plain statement, it says 'not checked' and never counts as a match. Not legal advice.")]
    fh, fld = faq(qa)
    nojs = ('<noscript><style>.fl69,#st69{display:none!important}</style><p class="small">Filters need JavaScript. All tools are listed below, A to Z.</p></noscript>')
    body = (f'{CSS}{nojs}<p class="small"><a href="/guides.html">Guides</a> › Privacy, refunds &amp; student deals</p>'
            f'<h1>Which AI tools train on your data? Privacy, refund &amp; student-deal checker</h1>'
            f'<p class="tag">All {len(names)} AI tools we track: does it use your chats, files or recordings to train its AI, can you get your money back, and is there a student deal. Read on each tool\'s official pages, with the exact words, the source link and the date we checked.</p>'
            f'<p class="small">New on Nov 12, 2026: {new69["train"]} more tools checked for AI training, {new69["refund"]} for refunds and {new69["student"]} for student deals. Not legal advice; policies change, so open the source before you decide.</p>'
            + summ + quick + f'<h2 id="all69">Check any tool</h2>' + filt
            + f'<p class="e69" id="e69" hidden>No tool matches all of those. <button type="button" id="x69y">Clear the filters</button></p>'
            + f'<div class="l69g" id="l69">{"".join(cards)}</div>'
            + f'<p class="small">How we check: we read each tool\'s privacy policy, terms, trust or security page, refund help article and pricing page. "Trains on your content" means the page says it may use what you put in (prompts, files, recordings, outputs) to train or improve its AI models; we don\'t count analytics or anonymized usage stats. "No opt-out found" means the pages we read didn\'t offer one. <a href="/how-we-pick.html">How we pick</a></p>'
            + f'{fh}<p class="small">Related: <a href="/alternatives.html">Alternatives to every AI tool</a> · <a href="/help-me-choose.html?m_privacy=must">Find a tool that doesn\'t train on my data</a> · <a href="/compare-builder.html">Compare any 2-3 tools</a> · <a href="/tools.html">All AI tools</a> · <a href="/ai-data-privacy.html">Opt-out steps for the big assistants</a> · <a href="/ai-refund-policies.html">Refund window checker</a> · <a href="/ai-student-discounts.html">Student discounts</a></p>'
            + f'<script>{JS}</script>')
    title = f"Which AI Tools Train on Your Data? Privacy, Refund & Student Deal Checker ({len(names)} Tools) | ToolPick"
    desc = (f"Does ChatGPT, Canva, CapCut, HeyGen or Suno train on your data? Can you get a refund? Plain answers for {len(names)} AI tools: "
            f"{cnt['train'].get('no', 0)} don't train on your content, {cnt['train'].get('noopt', 0)} train with no opt-out found, {cnt['refund'].get('window', 0)} have a refund window. Official sources and dates.")
    ld = [{"@context": "https://schema.org", "@type": "Dataset", "name": "AI tool data training, refund and student-deal facts", "url": BASE + PATH,
           "description": f"For {len(names)} AI tools: whether the tool trains AI on your content (and how to opt out), its refund rule and any student deal, each from the official page with the exact words and checked date.",
           "dateModified": V69_DATE, "creator": {"@type": "Organization", "name": "ToolPick", "url": BASE + "/"}, "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
           "variableMeasured": ["Trains AI on user content", "Opt-out", "Refund window", "Student deal"]},
          fld, crumbs([("ToolPick", "/"), ("Guides", "/guides.html"), ("Privacy, refunds & student deals", PATH)])]
    page(PATH, title, desc, body, ld)
    _lm[PATH] = V69_DATE
    return ROWS, dict(cnt=cnt, checked=checked, new=new69, total=len(names))


def link_v69(ctx, ROWS, S):
    """Tool pages: a 'Privacy & refunds' box before the alternatives box. Guides: a pointer on the privacy/refund/student
    guides, guides.html and tools.html."""
    e = ctx["e"]; slug = ctx["slug"]; changed = []
    ICON = {"y": "✓", "p": "~", "n": "✕", "u": "?"}
    strip = lambda h: re.sub(r"<[^>]+>", "", h)
    for n, R in ROWS.items():
        fp = f"public/tools/{slug(n)}.html"
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' tp69"' in h: continue
        li = []
        for k, lab in (("train", "Trains AI on your data?"), ("refund", "Refunds"), ("student", "Student deal")):
            code, l_, det, d = R[k]; t = TONE[code]
            li.append(f'<li class="{t}"><b>{lab}</b> <i class="i69" aria-hidden="true">{ICON[t]}</i> {e(l_)}' + (f' <span class="small">(checked {d})</span>' if d else "") + '</li>')
        box = ('<style>.tp69 ul{list-style:none;margin:6px 0 0;padding:0}.tp69 li{margin:4px 0;font-size:.95rem}.tp69 li b{display:inline-block;min-width:11.5em}.tp69 .i69{font-style:normal;font-weight:700}.tp69 li.y .i69{color:var(--ok)}.tp69 li.n .i69{color:var(--warn)}.tp69 .small{color:var(--mu)}.tp69 p>a{display:inline;padding:0}@media(max-width:640px){.tp69 li b{display:block;min-width:0}}</style>'
               f'<section class="card tp69 pick" style="margin-bottom:16px" id="privacy-refunds" aria-labelledby="pr69"><h2 id="pr69" style="margin:0;font-size:1.1rem">{e(n)}: privacy, refunds &amp; student deal</h2><ul>{"".join(li)}</ul>'
               f'<p style="margin:8px 0 0"><a href="{PATH}#t-{slug(n)}"><b>Exact words, opt-out steps and sources&nbsp;→</b></a></p><p class="small" style="margin:2px 0 0">Or <a href="{PATH}">check all {S["total"]} tools</a> for AI training, refunds and student deals.</p></section>')
        a = '<section class="card tp68' if '<section class="card tp68' in h else ('<section class="card tbp"' if '<section class="card tbp"' in h else None)
        if not a: continue
        h = h.replace(a, box + a, 1)
        open(fp, "w").write(h); changed.append(f"/tools/{slug(n)}.html")
    note = (f'<p class="pick small v69" style="margin:12px 0">New: <a href="{PATH}"><b>Which AI tools train on your data? Privacy, refund &amp; student-deal checker</b></a> now covers all {S["total"]} tools '
            f'({S["checked"]["train"]} checked for AI training, {S["checked"]["refund"]} for refunds, {S["checked"]["student"]} for student deals).</p>')
    for p_ in ("/ai-data-privacy.html", "/ai-refund-policies.html", "/ai-student-discounts.html", "/tools.html", "/save-money.html", "/free.html"):
        fp = "public" + p_
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' v69"' in h or "</h1>" not in h: continue
        i = h.index("</h1>") + 5
        m = re.compile(r'<p class="tag">.*?</p>', re.S).match(h, i)
        if m: i = m.end()
        h = h[:i] + note + h[i:]
        open(fp, "w").write(h); changed.append(p_)
    fp = "public/guides.html"; h = open(fp).read()
    if ' v69"' not in h and "<h2>New guides</h2><ul>" in h:
        open(fp, "w").write(h.replace("<h2>New guides</h2><ul>", f"<h2>New guides</h2><ul><li class=\"v69\"><a href='{PATH}'>Which AI tools train on your data? Privacy, refund &amp; student-deal checker for all {S['total']} tools</a></li>", 1)); changed.append("/guides.html")
    return changed


CSS = ("<style>.sm69{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));margin:var(--s4) 0}.sm69 h2{font-size:1rem;margin:0 0 8px}.sm69 h2 .small{font-weight:400;color:var(--mu)}"
       ".sg69{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sb69{display:flex;flex-direction:column;justify-content:center;min-height:64px;padding:8px 12px;border-radius:var(--r);border:1px solid var(--bd);background:var(--sf);color:var(--tx);text-decoration:none}"
       ".sb69 b{font-size:1.4rem;line-height:1.1}.sb69 span{font-size:.85rem;color:var(--mu)}.sb69.y{border-left:4px solid var(--ok)}.sb69.n{border-left:4px solid var(--warn)}.sb69.p{border-left:4px solid var(--ac)}.sb69:hover b{text-decoration:underline}"
       ".q69 dl{display:grid;grid-template-columns:max-content 1fr;gap:8px 14px;margin:8px 0 0;font-size:.93rem}.q69 dt{font-weight:600}.q69 dd{margin:0}.q69 dd a{display:inline;padding:0}"
       ".p69{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-size:.92rem;text-decoration:none;margin:0 6px 8px 0}"
       ".fl69{position:sticky;top:0;z-index:2;background:var(--bg);display:grid;gap:8px 12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));padding:10px 0;border-bottom:1px solid var(--bd);align-items:end}"
       ".l69{display:flex;flex-direction:column;gap:4px;font-size:.85rem;font-weight:600}.l69 select,.l69 input{min-height:44px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 10px;font:inherit;font-weight:400;font-size:.95rem;width:100%;box-sizing:border-box}"
       ".bt69{margin:0;display:flex;gap:8px}.bt69 button,.e69 button{min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;cursor:pointer}.nojs69{display:none!important}"
       ".l69 select:focus-visible,.l69 input:focus-visible,.bt69 button:focus-visible,.p69:focus-visible,.sb69:focus-visible{outline:3px solid var(--ac);outline-offset:2px}"
       "#st69{margin:8px 0;min-height:1.4em}.l69g{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));margin:var(--s3) 0}"
       ".c69{scroll-margin-top:12px;display:flex;flex-direction:column}.c69[hidden]{display:none}.c69 h3{margin:0 0 4px;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}.c69 h3 a{min-height:32px;display:inline-flex;align-items:center}.c69 h3 .small{color:var(--mu);font-weight:400}"
       ".f69{border-top:1px solid var(--bd);padding:8px 0 4px}.f69 h4{font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mu);margin:0}.f69 p{margin:4px 0;font-size:.92rem}.f69 p a{display:inline;padding:0}"
       ".f69 .b69{font-weight:700;font-size:.98rem}.f69.y .b69 b{color:var(--ok)}.f69.n .b69 b{color:var(--warn)}.f69.p .b69 b,.f69.u .b69 b{color:var(--mu)}.f69.u .b69{font-weight:600;color:var(--mu)}"
       ".f69 details{margin:2px 0}.f69 summary{cursor:pointer;min-height:44px;display:flex;align-items:center;gap:6px;font-size:.9rem;font-weight:600;color:var(--ac);list-style:none}.f69 summary::-webkit-details-marker{display:none}.f69 summary::before{content:'▸';font-size:.8rem}.f69 details[open] summary::before{content:'▾'}.f69 blockquote{margin:0 0 6px;padding:6px 10px;border-left:3px solid var(--bd);font-size:.88rem;color:var(--mu)}"
       ".s69{font-size:.85rem!important;color:var(--mu)}.a69{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:auto!important;padding-top:8px;border-top:1px solid var(--bd);font-size:.92rem}.a69 a{min-height:44px;display:inline-flex;align-items:center}"
       ".e69{padding:var(--s4);border:1px dashed var(--bd);border-radius:var(--r)}"
       "@media(max-width:640px){.fl69{position:static;grid-template-columns:1fr 1fr}.l69.q{grid-column:1/-1}.q69 dl{grid-template-columns:1fr;gap:2px}.q69 dd{margin-bottom:8px}}</style>")

JS = r"""(()=>{const $=i=>document.getElementById(i),F={train:$('x69t'),refund:$('x69r'),student:$('x69s'),cat:$('x69c'),sort:$('x69o'),q:$('x69q')},C=[...document.querySelectorAll('.c69')],L=$('l69'),st=$('st69'),E=$('e69');
const LAB={train:'AI training',refund:'refunds',student:'student deal'};
const RK={no:0,optin:1,optout:2,unclear:3,nc:4,noopt:5};let LS='az';
function go(push){const v={};for(const k in F)v[k]=(F[k].value||'').trim();const q=v.q.toLowerCase();let n=0;
C.forEach(c=>{const ok=(!v.train||c.dataset.train==v.train)&&(!v.refund||c.dataset.refund==v.refund)&&(!v.student||c.dataset.student==v.student)&&(!v.cat||c.dataset.c==v.cat)&&(!q||c.dataset.k.includes(q));c.hidden=!ok;if(ok)n++});
if(v.sort!=LS){LS=v.sort;const s=[...C];if(v.sort=='private')s.sort((a,b)=>(RK[a.dataset.train]-RK[b.dataset.train])||a.dataset.n.localeCompare(b.dataset.n));else if(v.sort=='refund')s.sort((a,b)=>(b.dataset.rw-a.dataset.rw)||a.dataset.n.localeCompare(b.dataset.n));else if(v.sort=='checked')s.sort((a,b)=>b.dataset.ck.localeCompare(a.dataset.ck)||a.dataset.n.localeCompare(b.dataset.n));else s.sort((a,b)=>a.dataset.n.localeCompare(b.dataset.n));s.forEach(c=>L.appendChild(c))}
E.hidden=n>0;const on=['train','refund','student','cat'].filter(k=>v[k]).map(k=>k=='cat'?F.cat.options[F.cat.selectedIndex].text:F[k].options[F[k].selectedIndex].text.replace(/ \(\d+\)$/,''));if(q)on.push('“'+v.q+'”');
st.textContent=on.length?n+' of '+C.length+' tools '+(n==1?'matches':'match')+': '+on.join(' + ')+'.':'Showing all '+C.length+' tools.';
if(push){const u=new URL(location.href);for(const k in F){if(v[k]&&!(k=='sort'&&v[k]=='az'))u.searchParams.set(k,v[k]);else u.searchParams.delete(k)}history.replaceState(null,'',u.pathname+u.search+u.hash)}}
for(const k in F){F[k].addEventListener(k=='q'?'input':'change',()=>go(true))}
$('f69').addEventListener('submit',ev=>{ev.preventDefault();go(true)});
const clr=()=>{for(const k in F)F[k].value=k=='sort'?'az':'';go(true)};$('x69x').addEventListener('click',clr);$('x69y').addEventListener('click',clr);
const P=new URLSearchParams(location.search);let any=0;for(const k in F){const x=P.get(k);if(x!==null){if(F[k].tagName=='SELECT'){if([...F[k].options].some(o=>o.value==x)){F[k].value=x;any=1}}else{F[k].value=x;any=1}}}
go(false);if(any&&!location.hash&&(P.get('train')||P.get('refund')||P.get('student')||P.get('cat')||P.get('q'))){const a=$('all69');if(a)a.scrollIntoView()}})();"""
