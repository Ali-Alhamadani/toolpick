"""v66: Find my AI tool - 'Help me choose' 2.0 (/help-me-choose.html).
Four questions (the job, budget + billing + seats, must-haves / nice-to-haves, what matters most) -> a ranked
shortlist with a plain reason for every rank, a checklist of each thing you asked for (met / partly / no / not checked,
each with its official source link and checked date), a 'Left out and why' list, and one-tap 'relax a rule' suggestions
when nothing fits. Reuses only facts already verified in tools.py: JOBS picks, CAPS main jobs, entry prices (numeric USD
monthly / per-month-billed-yearly, each tool's checked date), the per-seat rule, realfree(), Best Value picks, and the
v57/v64 cells (_row57) for free plan, data training, student deal and refunds. A tool we haven't checked is never guessed in."""
import json, os, re

V66_DATE = "2026-11-09"
PATH = "/help-me-choose.html"
SRC_RE = re.compile(r'<span class="s57"><a href="([^"]+)"[^>]*>.*?checked (\d{4}-\d{2}-\d{2})', re.S)


def _src(h):
    m = SRC_RE.search(h or "")
    return (m.group(1).replace("&amp;", "&"), m.group(2)) if m else ("", "")


def build_v66(ctx):
    page = ctx["page"]; e = ctx["e"]; slug = ctx["slug"]; BASE = ctx["BASE"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]
    _lm = ctx["_lm"]; URLS = ctx["URLS"]; _row57 = ctx["_row57"]; bmap = ctx["_bmap"]; DLIST = ctx["_DLIST"]
    CATEGORIES = ctx["CATEGORIES"]; JOBS = ctx["JOBS"]; CAPS = ctx["CAPS"]; T = ctx["tools"]; USAGE = ctx["USAGE"]
    PV = ctx["_PV57"]; RF = ctx["_RF57"]; ST = ctx["_ST57"]; STN = ctx["_STN57"]; PLO = ctx["_PLO57"]; RLO = ctx["_RLO57"]
    SCHOOL = {a: (b, c) for a, b, c, *_ in T.STUDENT_SCHOOL_ONLY}
    names = {v["s"]: v["n"] for v in bmap.values()}
    dl = {v["s"]: v for v in DLIST}
    usage = {u["t"] for u in USAGE}
    PVLAB = {"n": "Doesn't train on your content by default", "c": "Trains only if you opt in", "y": "Trains by default; you can switch it off",
             "p": "Trains by default; only paid plans can switch it off", "x": "Trains on your content; no opt-out found", "u": "Unclear: the default isn't stated"}

    def hrs(h): return f"{h // 24}-day" if h >= 48 and h % 24 == 0 else f"{h}-hour"

    TD = []
    cover = dict(free=0, privacy=0, student=0, refund=0, yearly=0)
    for s in sorted(names, key=lambda k: names[k].lower()):
        b = bmap[s]; d = dl[s]; n = b["n"]
        F = {}
        # free plan (always known: realfree on the tool's checked free text, or FREE_LIMITS)
        c = _row57("free", n); u, k = _src(c["h"])
        F["free"] = ["y", d["f"], u, k] if b["fr"] else ["n", "No real free plan (" + d["f"] + ")", u, k]
        cover["free"] += 1
        # data training
        if n in PV:
            p = PV[n]; c = _row57("privacy", n); u, k = _src(c["h"])
            st = "y" if p["k"] in "nc" else ("p" if p["k"] in "yp" else ("u" if p["k"] == "u" else "n"))
            lab = PVLAB[p["k"]] + ("; team plans aren't used for training by default" if p.get("bk") == "n" and p["k"] not in "n" else "")
            F["privacy"] = [st, lab, u, k]; cover["privacy"] += 1
        else:
            F["privacy"] = ["u", ("Not stated plainly on its pages" if n in PLO else "Not checked yet"), "", ""]
        # student deal (students; teacher-only offers don't count)
        if n in ST:
            o = ST[n]; c = _row57("student", n); u, k = _src(c["h"])
            if o["kind"] in ("free", "off"): F["student"] = ["y", f"Student deal: {o['badge']} ({o['offer']})", u, k]
            else: F["student"] = ["p", f"Ask support: {o['offer']}", u, k]
            cover["student"] += 1
        elif n in SCHOOL:
            F["student"] = ["p", "Only through your school: " + SCHOOL[n][0], SCHOOL[n][1], T.STUDENT_CHECKED]; cover["student"] += 1
        elif n in STN:
            F["student"] = ["n", "No student deal on its official page", STN[n][1], T.STUDENT_CHECKED]; cover["student"] += 1
        else:
            F["student"] = ["u", "Not checked yet", "", ""]
        # refunds
        if n in RF:
            r = RF[n]; c = _row57("refund", n); u, k = _src(c["h"])
            if r["k"] == "w" and r["wm"]:
                w = hrs(r["wm"]) + (f" ({hrs(r['wy'])} on yearly)" if r.get("wy") and r["wy"] != r["wm"] else "")
                F["refund"] = ["y", f"Refund window: {w}, conditions apply", u, k]
            elif r["k"] == "w": F["refund"] = ["p", "Refunds only in narrow cases", u, k]
            elif r["k"] == "c": F["refund"] = ["p", "Refunds case by case", u, k]
            else: F["refund"] = ["n", "No refunds", u, k]
            cover["refund"] += 1
        else:
            F["refund"] = ["u", ("Refund rule unclear on its page" if n in RLO else "Not checked yet"), "", ""]
        # yearly saving (same cheapest paid plan, numeric USD monthly + per-month billed yearly)
        mm, ma = b.get("mm"), b.get("ma")
        if n in T.V57_YEARLY:
            pl, m_, y_, q_, u_ = T.V57_YEARLY[n]
            F["yearly"] = ["n", f"Monthly billing only on {pl}", u_, T.V57_CHECKED]; cover["yearly"] += 1
        elif d.get("ys", 0) > 0:
            F["yearly"] = ["y", f"Yearly billing saves {d['ys']}%" + (f" (${ma:g} vs ${mm:g}/mo)" if mm and ma else ""), b["pr"], b["k"]]; cover["yearly"] += 1
        elif mm is not None and ma is not None:
            F["yearly"] = ["n", "No saving for paying yearly", b["pr"], b["k"]]; cover["yearly"] += 1
        else:
            F["yearly"] = ["u", "Not checked in a form we can compare", "", ""]
        tm = ""
        if n in ctx["_TM57"]:
            tm = _row57("team", n)["h"]
        TD.append(dict(s=s, n=n, d=b["d"], u=b["u"], dm=b["dm"], pr=b["pr"], k=b["k"], p=b["p"], fr=b["fr"], ps=d["ps"],
                       mm=mm, ma=ma, lt=b.get("lt") or "", cl=b["cl"], cap=b["cap"], bv=d["bestFor"], cats=[c_["id"] for c_ in d["cats"]],
                       F=F, tm=tm, us=1 if n in usage else 0))
    # jobs: ToolPick's ranked picks for the job, plus tools with the same main job as the #1 pick or as 2+ of the picks
    J = []
    for js, lab, cid, ranked in JOBS:
        rs = [slug(x) for x in ranked if slug(x) in names]
        prim = [CAPS[x][0] for x in ranked]
        keep = {prim[0]} | {c for c in prim if prim.count(c) >= 2}
        same = [[v["s"], next(slug(x) for x in ranked if CAPS[x][0] == v["cap"])] for v in sorted(bmap.values(), key=lambda v: v["n"].lower()) if v["s"] not in rs and v["cap"] in keep]
        J.append(dict(id=js, l=lab, c=cid, t=rs, same=same, jp=f"/best-ai-tool-for-{js}.html"))
    C = [dict(id=c["id"], n=c["name"], need=c["need"], best=slug(c["best"]), t=[slug(t["name"]) for t in c["tools"]]) for c in CATEGORIES]
    for j in J:
        assert all(s in names for s in j["t"] + [a for a, b in j["same"]]), j
        assert os.path.exists("public" + j["jp"]), j["jp"]
    global TD_LAST; TD_LAST = TD  # v68 reuses these per-tool facts
    DATA = json.dumps(dict(t=TD, j=J, c=C), separators=(",", ":")).replace("</", "<\\/")

    # ---------- step 1 options: jobs grouped by category + "anything in X" ----------
    g = []
    for c in CATEGORIES:
        jobs = [j for j in J if j["c"] == c["id"]]
        opts = "".join(f'<label class="o66" data-k="{e((j["l"] + " " + c["name"] + " " + " ".join(names[s] for s in j["t"])).lower())}"><input type="radio" name="w1" value="job:{j["id"]}"><span>{e(j["l"][0].upper() + j["l"][1:])}</span></label>' for j in jobs)
        opts += f'<label class="o66 any" data-k="{e((c["name"] + " " + c["need"]).lower())}"><input type="radio" name="w1" value="cat:{c["id"]}"><span>Anything in {e(c["name"])}</span></label>'
        g.append(f'<div class="g66" data-g="{c["id"]}"><h3>{e(c["name"])} <span class="small">{e(c["need"])}</span></h3><div class="ol66">{opts}</div></div>')
    STEP1 = "".join(g)
    MUST = [("free", "A real free plan", "Free trials and one-time credits don't count.", "/free-plan-limits.html", "Free plan limits"),
            ("privacy", "Doesn't train AI on my data without my OK", f"Read on official privacy pages (checked {T.PRIVACY_CHECKED}); {cover['privacy']} of {len(TD)} tools checked so far.", "/ai-data-privacy.html", "Data privacy"),
            ("student", "A student deal", f"Free or discounted plans for students on official pages (checked {T.STUDENT_CHECKED}); {cover['student']} tools checked.", "/ai-student-discounts.html", "Student discounts"),
            ("refund", "A refund window if it's not for me", f"From official help pages (checked {T.REFUND_CHECKED}); {cover['refund']} tools checked.", "/ai-refund-policies.html", "Refund rules"),
            ("yearly", "Cheaper if I pay yearly", f"Same plan, monthly vs billed yearly; {cover['yearly']} tools checked.", "/monthly-or-yearly.html", "Monthly or yearly?")]
    mrows = "".join(f'<fieldset class="m66"><legend><b>{e(lab)}</b><span class="small">{e(sub)} <a href="{href}">{e(hl)}</a></span></legend><div class="sg66">'
                    + "".join(f'<label><input type="radio" name="m_{k}" value="{v}"{" checked" if v == "any" else ""}><span>{t}</span></label>' for v, t in (("any", "Don't mind"), ("nice", "Nice to have"), ("must", "Must have")))
                    + '</div></fieldset>' for k, lab, sub, href, hl in MUST)
    PRI = [("fit", "Best fit for the job", "Our ranked picks for that job come first."),
           ("cheap", "Lowest price", "The cheapest verified price for your billing and seats comes first."),
           ("privacy", "Privacy", "Tools that don't train on your data by default come first."),
           ("free", "Starting free", "Tools with a real free plan come first.")]
    prows = "".join(f'<label><input type="radio" name="w4" value="{v}"{" checked" if v == "fit" else ""}><span><b>{e(t)}</b> — {e(s)}</span></label>' for v, t, s in PRI)
    presets = [("job=voiceovers&budget=10&m_free=must", "A voiceover tool under $10 with a free plan"),
               ("job=meeting-notes&m_privacy=must&pri=privacy", "Meeting notes that don't train on my data"),
               ("job=code-autocomplete&m_student=nice&pri=cheap", "Cheapest code autocomplete (student deal a plus)"),
               ("job=long-form-writing&m_privacy=nice&m_refund=nice", "A writing assistant: privacy and refunds matter"),
               ("job=pitch-decks&seats=5&billing=y&m_yearly=must", "Pitch decks for a team of 5, billed yearly"),
               ("job=youtube-shorts&budget=free", "Free tool for YouTube Shorts")]
    pre = " ".join(f'<a class="chip" href="{PATH}?{e(q)}">{e(l)}</a>' for q, l in presets)
    jl = "".join(f'<li><a href="{j["jp"]}">{e(j["l"][0].upper() + j["l"][1:])}</a></li>' for j in J)
    css = ('<style>.o66{display:inline-flex}.o66 input,.sg66 input,.p66 input{position:absolute;opacity:0;width:1px;height:1px}'
           '.o66 span,.sg66 span{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);cursor:pointer;font-size:.95rem}'
           '.o66.any span{border-style:dashed}.o66 input:checked+span,.sg66 input:checked+span{background:var(--ac);border-color:var(--ac);color:var(--sf);font-weight:700}'
           '.o66 input:focus-visible+span,.sg66 input:focus-visible+span,.p66 input:focus-visible+span{outline:3px solid var(--ac);outline-offset:2px}'
           '.ol66{display:flex;flex-wrap:wrap;gap:8px}.g66{margin:0 0 14px}.g66 h3{font-size:1rem;margin:0 0 8px}.g66 h3 .small{font-weight:400;color:var(--mu)}'
           '.f66{width:100%;min-height:48px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px;margin:0 0 14px;font:inherit}'
           '.m66{border:0;border-top:1px solid var(--bd);padding:12px 0;margin:0;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}.m66:first-of-type{border-top:0}'
           '.m66 legend{float:left;max-width:440px;padding:0;font-size:1rem;font-weight:400;margin:0}.m66 legend b{font-size:1rem}.m66 legend .small{display:block;font-weight:400;color:var(--mu);margin-top:2px}.sg66{display:flex;gap:6px;flex-wrap:wrap}'
           '.p66{display:grid;gap:8px}.p66 label{display:block;border:1px solid var(--bd);border-radius:12px;padding:12px 14px;cursor:pointer;background:var(--sf)}.p66 input:checked+span{font-weight:400}.p66 label:has(input:checked){border:2px solid var(--ac);background:var(--acs)}'
           '.q66{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 0}.sum66{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 12px}.sum66 .chip{min-height:36px;font-size:.88rem}'
           '.top66{border:2px solid var(--ok);border-radius:var(--r);padding:var(--s4);background:var(--sf);margin:0 0 var(--s4)}.top66 h2{margin:0 0 4px;font-size:1.3rem}'
           '.ck66{list-style:none;padding:0;margin:8px 0;display:grid;gap:4px}.ck66 li{font-size:.92rem;padding-left:26px;position:relative;margin:0;line-height:1.45}.ck66 li::before{position:absolute;left:0;top:0;font-weight:800;width:20px;text-align:center}'
           '.ck66 .y::before{content:"✓";color:var(--ok)}.ck66 .p::before{content:"~";color:var(--warn)}.ck66 .n::before{content:"✗";color:#b91c1c}.ck66 .u::before{content:"?";color:var(--mu)}'
           '.ck66 .src{color:var(--mu);font-size:.82rem}.why66{margin:6px 0 0;padding-left:20px}.why66 li{font-size:.92rem;margin:2px 0}.rk66{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;border-radius:999px;background:var(--acs);color:var(--tx);font-weight:800;margin-right:6px}'
           '.lo66 li{margin:0 0 6px}.rx66{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 0}.v66nj{columns:2;column-gap:24px}@media(max-width:640px){.v66nj{columns:1}.m66 legend{float:none}.m66 .sg66{width:100%;flex-wrap:nowrap}.m66 .sg66 label{flex:1 1 0}.m66 .sg66 span{width:100%;justify-content:center;padding:0 6px;font-size:.88rem;text-align:center}.wnav .bbtn{flex:1 1 auto}}'
           '.tm66 .s57{display:block;font-size:.82rem;color:var(--mu)}.tm66 .na57{color:var(--mu)}#res66 h2:focus{outline:none}.pr66{font-size:1.05rem;margin:6px 0}</style>')
    body = f"""{css}<h1>Find my AI tool</h1><p class="tag">Answer 4 quick questions — the job, your budget, the must-haves you care about (free plan, privacy, student deal, refunds, yearly saving) and what matters most — and get a ranked shortlist from our {len(TD)} tools. Every pick says why it’s ranked there, and every fact links the official page we read it on, with the date.</p>
<div class="builder"><p class="small" id="wprog-label" role="status">Step 1 of 4</p><div class="wizprog" aria-hidden="true"><i id="wbar" style="width:25%"></i></div>
<form id="wform" action="{PATH}" method="get" onsubmit="return false">
<section class="wstep" data-step="1"><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;font-size:1.1rem;margin-bottom:10px">1. What do you want to do?</legend>
<label for="w1f" class="skip">Filter jobs</label><input id="w1f" class="f66" type="search" autocomplete="off" placeholder="Type to filter, e.g. podcast, slides, Cursor…">{STEP1}<p class="small" id="w1none" hidden>No job matches that. Try a broader word, or pick “Anything in …” for a whole category.</p></fieldset></section>
<section class="wstep" data-step="2" hidden><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;font-size:1.1rem;margin-bottom:10px">2. Budget, billing and seats</legend>
<p style="margin:0 0 6px;font-weight:600" id="w2bl">Monthly budget (all seats)</p><div class="sg66" role="radiogroup" aria-labelledby="w2bl">{"".join(f'<label><input type="radio" name="w2b" value="{v}"{" checked" if v == "any" else ""}><span>{t}</span></label>' for v, t in (("free", "Free only"), ("10", "Up to $10"), ("25", "Up to $25"), ("50", "Up to $50"), ("any", "Any budget")))}</div>
<p style="margin:16px 0 6px;font-weight:600" id="w2pl">How will you pay?</p><div class="sg66" role="radiogroup" aria-labelledby="w2pl"><label><input type="radio" name="w2p" value="m" checked><span>Monthly</span></label><label><input type="radio" name="w2p" value="y"><span>Yearly (pay up front)</span></label></div>
<label for="wseats" style="font-weight:600;display:block;margin-top:16px">How many people will use it? (1–50)</label><input type="number" id="wseats" min="1" max="50" step="1" value="1" inputmode="numeric" style="width:100%;max-width:220px;min-height:48px;margin-top:8px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 12px"><p class="small" style="margin:6px 0 0">Seats only multiply the price where the official price is per seat or per user (same rule as our cost calculator).</p></fieldset></section>
<section class="wstep" data-step="3" hidden><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;font-size:1.1rem;margin-bottom:4px">3. Must-haves and nice-to-haves</legend><p class="small" style="margin:0 0 8px">“Must have” removes tools that don’t have it <b>or that we haven’t checked</b> (we never guess). “Nice to have” moves tools that have it up the list.</p>{mrows}</fieldset></section>
<section class="wstep" data-step="4" hidden><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;font-size:1.1rem;margin-bottom:10px">4. What matters most?</legend><div class="p66">{prows}</div></fieldset></section>
<div class="wnav"><button type="button" class="bbtn" id="wBack">Back</button><button type="button" class="bbtn primary" id="wNext">Next</button><button type="button" class="bbtn" id="wGo">Show my picks</button><span class="small bstatus" id="wStatus" role="status" aria-live="polite"></span></div>
</form></div>
<noscript><div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">The picker needs JavaScript</h2><p class="small">Every job page below has our top 3 picks with checked prices, and the <a href="/tools.html">directory</a> has filters for free plans, privacy, refunds and student deals.</p><ul class="v66nj">{jl}</ul></div></noscript>
<div id="res66" aria-live="polite" aria-atomic="false"></div>
<section class="bnote" aria-labelledby="pre66"><h2 id="pre66" style="margin:0 0 6px;font-size:1.05rem">Or start from a common need</h2><div class="q66">{pre}</div></section>
<details class="bnote"><summary><h2 style="display:inline;margin:0;font-size:1.05rem">How we rank your picks</h2></summary><p class="small" style="margin:8px 0 0"><b>Which tools:</b> for a job, our 3 picks for that job (from its “best AI tool for …” page) plus every tool with the same main job as the top pick (what it does comes from each tool’s own site). For a whole category, every tool in it. <b>Budget:</b> the cheapest verified paid plan for your billing, times your seats only when the official price is per seat; yearly uses the per-month price billed yearly (or the monthly price if no yearly price is checked). If a tool’s paid plan is over budget but it has a real free plan, it stays in, marked “free plan only”. Prices that are “check site”, in euros or usage-only never count as fitting a budget. <b>Must-haves</b> remove tools that don’t have it or that we haven’t checked. <b>Ranking</b> adds simple points you can see on each card: job fit (our #1 pick for the job 40, #2 36, #3 32, same main job 28; for a category, its Best Value pick 32, others 24), +12 for each nice-to-have it has, +4 if it partly has it, −6 if it doesn’t, −10 for “free plan only”, and for what matters most to you: +10 for our picks when you choose best fit, up to +20 for the lowest price (scaled between the cheapest and dearest option), +20 for not training on your data by default (+8 if you can switch it off), or +20 for a real free plan. Ties go to the lower price, then the name. <b>Not ranked on:</b> features, quality or ease of use — we haven’t tested tools hands-on, so read the tool page before you buy. Facts and prices come from official pages and can change; each shows the date we read it.</p></details>
<p class="small">Prefer to browse? <a href="/tools.html">See every tool with filters →</a> · Already know 2–3 tools? <a href="/compare-builder.html">Compare them side by side →</a> · Several jobs on one budget? <a href="/ai-budget-planner.html">Plan my AI budget →</a></p>
<script>const D={DATA};
{JS}
</script>"""
    qas = [("How does Find my AI tool pick tools for me?", "You choose a job (or a whole category), a budget with billing and seats, which facts are must-haves or nice-to-haves, and what matters most. It starts from ToolPick's 3 picks for that job plus tools with the same main job, removes tools that miss your budget or a must-have, then ranks the rest with visible points for job fit, each nice-to-have and your top priority. Every card explains its rank."),
           ("What if a tool hasn't been checked for privacy, refunds or student deals?", f"It shows as “not checked” and is never counted as having it. A must-have removes it (it appears under “Left out and why”); a nice-to-have gives it no points. So far we've read data-training rules for {cover['privacy']} tools, refund rules for {cover['refund']} and student deals for {cover['student']}."),
           ("Can I share my picks?", f"Yes. The address updates with your answers, for example {BASE}{PATH}?job=voiceovers&budget=10&m_free=must, and the Copy link button copies it.")]
    fh, fl = faq(qas)
    body += fh
    while PATH in URLS: URLS.remove(PATH)
    page(PATH, "Find My AI Tool: 4 Questions, Ranked Picks with Reasons | ToolPick",
         "Answer 4 quick questions — the job, budget and seats, must-haves like a free plan, no AI training on your data, a student deal or refunds, and what matters most — and get ranked AI tool picks with a reason for each, from facts on official pages.",
         body,
         [{"@context": "https://schema.org", "@type": "WebApplication", "name": "ToolPick: Find my AI tool", "url": BASE + PATH, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "description": "Guided picker: choose a job, budget, must-haves (free plan, data training, student deal, refunds, yearly saving) and a priority to get ranked AI tool picks with reasons and sources."},
          fl, crumbs([("ToolPick", "/"), ("Find my AI tool", PATH)])])
    _lm[PATH] = V66_DATE
    return cover, len(DATA), len(J)


def link_v66(ctx):
    """Entry points: every job page and category page, the home finder and the directory link into the picker."""
    e = ctx["e"]; JOBS = ctx["JOBS"]; CATEGORIES = ctx["CATEGORIES"]; changed = []
    for js, lab, cid, ranked in JOBS:
        fp = f"public/best-ai-tool-for-{js}.html"; h = open(fp).read()
        if ' v66"' in h: continue
        snip = (f'<p class="pick small v66"><b>Want these ranked for you?</b> Add your budget, seats and must-haves (free plan, no AI training on your data, student deal, refunds) and get picks for {e(lab)} with a reason for each. '
                f'<a href="/help-me-choose.html?job={js}">Find my tool for {e(lab)} →</a></p>')
        for anchor in ("<h2>Comparisons</h2>", "<h2>Other jobs</h2>"):
            if anchor in h:
                open(fp, "w").write(h.replace(anchor, snip + anchor, 1)); changed.append(fp[6:]); break
    for c in CATEGORIES:
        fp = f"public/best-ai-{c['id']}-tools.html"; h = open(fp).read()
        old = "Answer 5 quick questions and get a ranked shortlist for this category."
        if old in h:
            h = h.replace(f'<a href="/help-me-choose.html?category={c["id"]}">', f'<a class="v66" href="/help-me-choose.html?category={c["id"]}">', 1)
            open(fp, "w").write(h.replace(old, "Answer 4 quick questions (budget, seats, must-haves like a free plan, privacy or a student deal) and get ranked picks with a reason for each.", 1)); changed.append(fp[6:])
    fp = "public/index.html"; h = open(fp).read()
    a = '</div>\n<div class="filters">'
    if ' v66"' not in h and a in h:
        h = h.replace(a, '</div>\n<p class="small v66" style="margin:10px 0 0">Not sure what to type? <a href="/help-me-choose.html"><b>Find my AI tool in 4 questions →</b></a> Pick the job, budget and must-haves; get ranked picks with reasons.</p>\n<div class="filters">', 1)
        open(fp, "w").write(h); changed.append("/")
    fp = "public/tools.html"; h = open(fp).read()
    a = '<p class="small dshort v53">Shortcuts: '
    if ' v66"' not in h and a in h:
        h = h.replace(a, a + '<a class="v66" href="/help-me-choose.html">Find my tool in 4 questions</a> ', 1)
        open(fp, "w").write(h); changed.append("/tools.html")
    return changed


JS = r"""const $=id=>document.getElementById(id);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const BY={};D.t.forEach(t=>BY[t.s]=t);const JB={};D.j.forEach(j=>JB[j.id]=j);const CB={};D.c.forEach(c=>CB[c.id]=c);
const MK=['free','privacy','student','refund','yearly'];
const ML={free:'Free plan',privacy:'No AI training without my OK',student:'Student deal',refund:'Refund window',yearly:'Cheaper yearly'};
const GU={free:s=>'/free-plan-limits.html',privacy:s=>'/ai-data-privacy.html?tool='+s,student:s=>'/ai-student-discounts.html',refund:s=>'/ai-refund-policies.html?tool='+s+'#check',yearly:s=>'/monthly-or-yearly.html?tool='+s};
const WANT={free:'free',privacy:'privacy',student:'student',refund:'refund',yearly:'yearly'};
const PRL={fit:'Best fit for the job',cheap:'Lowest price',privacy:'Privacy',free:'Starting free'};
const BL={free:'Free only','10':'Up to $10/mo','25':'Up to $25/mo','50':'Up to $50/mo',any:'Any budget'};
const m$=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))};
const cap=s=>s?s[0].toUpperCase()+s.slice(1):s;
let step=1,shown=false;
const g=n=>{const el=document.querySelector('input[name="'+n+'"]:checked');return el?el.value:''};
function vals(){let seats=parseInt($('wseats').value,10);if(isNaN(seats))seats=1;seats=Math.min(50,Math.max(1,seats));const m={};MK.forEach(k=>m[k]=g('m_'+k)||'any');return{w:g('w1'),budget:g('w2b')||'any',bill:g('w2p')||'m',seats:seats,m:m,pri:g('w4')||'fit'}}
function setR(n,v){const el=document.querySelector('input[name="'+n+'"][value="'+v+'"]');if(el){el.checked=true;return true}return false}
function share(v){const q=new URLSearchParams();if(v.w){const[a,b]=v.w.split(':');q.set(a=='job'?'job':'category',b)}if(v.budget!='any')q.set('budget',v.budget);if(v.bill!='m')q.set('billing','y');if(v.seats!=1)q.set('seats',v.seats);MK.forEach(k=>{if(v.m[k]!='any')q.set('m_'+k,v.m[k])});if(v.pri!='fit')q.set('pri',v.pri);const s=q.toString();return location.pathname+(s?'?'+s:'')}
function price(t,v){let b=null,note='';if(v.bill=='m'){b=t.mm;if(b==null&&t.ma!=null)note='only a yearly-billing price is checked ('+m$(t.ma)+'/mo billed yearly)'}else{b=t.ma;if(b==null&&t.mm!=null){b=t.mm;note='no yearly price checked, monthly price used'}}
if(b==null)return{c:null,note:note||'no verified price we can compare (“check site”, euros or usage-based)'};const f=t.ps?v.seats:1;return{c:b*f,base:b,f:f,note:note}}
function bstat(t,P,v){if(v.budget=='any')return'fit';if(v.budget=='free')return t.fr?'fit':'over';const B=+v.budget;if(P.c!=null&&P.c<=B)return'fit';if(t.fr)return'freeonly';return P.c==null?'unk':'over'}
function cands(v){if(!v.w)return[];const[a,b]=v.w.split(':');if(a=='job'){const j=JB[b];if(!j)return[];return j.t.map((s,i)=>({t:BY[s],fit:40-4*i,fw:i==0?'our #1 pick for '+j.l:'our #'+(i+1)+' pick for '+j.l})).concat(j.same.map(([s,m])=>({t:BY[s],fit:28,fw:'same main job ('+BY[s].cl+') as '+BY[m].n+', one of our picks'})))}
const c=CB[b];if(!c)return[];return c.t.map(s=>({t:BY[s],fit:s==c.best?32:24,fw:s==c.best?'ToolPick’s Best Value pick for '+c.n:'in '+c.n+' (main job: '+BY[s].cl+')'}))}
const PVR={y:1,p:.5,n:0,u:0};
function evaluate(v0,ov){ov=ov||{};const v=Object.assign({},v0,ov);v.m=Object.assign({},v0.m,ov.m||{});const L=cands(v).filter(x=>x.t);const keep=[],out=[];
L.forEach(x=>{const t=x.t,P=price(t,v),bs=bstat(t,P,v);x.P=P;x.bs=bs;const why=[];
if(bs=='over'||bs=='unk'){x.out=bs=='over'?(v.budget=='free'?'No real free plan'+(P.c!=null?' (paid from '+m$(P.c)+'/mo)':''):'Over your '+BL[v.budget].toLowerCase()+' budget: '+m$(P.c)+'/mo'+(t.ps&&v.seats>1?' for '+v.seats+' seats':'')+', and no real free plan'):'Price can’t be checked against your budget: '+P.note;out.push(x);return}
const miss=MK.filter(k=>v.m[k]=='must'&&t.F[k][0]!='y');if(miss.length){const k=miss[0];x.out='Must-have “'+ML[k]+'”: '+t.F[k][1];x.miss=miss;out.push(x);return}
let s=x.fit;why.push(['+'+x.fit,cap(x.fw)]);
MK.forEach(k=>{if(v.m[k]!='nice')return;const st=t.F[k][0];if(st=='y'){s+=12;why.push(['+12','has '+ML[k].toLowerCase()])}else if(st=='p'){s+=4;why.push(['+4','partly: '+t.F[k][1]])}else if(st=='n'){s-=6;why.push(['−6','no '+ML[k].toLowerCase()])}});
if(bs=='freeonly'){s-=10;why.push(['−10','paid plan is over your budget; you’d stay on the free plan'])}
x.s=s;x.why=why;keep.push(x)});
// priority bonus
if(v.pri=='cheap'){const cc=x=>v.budget=='free'?0:(x.bs=='freeonly'?null:x.P.c);const pr=keep.map(cc).filter(c=>c!=null);const lo=Math.min(...pr),hi=Math.max(...pr);keep.forEach(x=>{const c=cc(x);if(c==null){x.why.push(['+0',x.bs=='freeonly'?'paid plan is over your budget, so no lowest-price points':'no comparable price, so no lowest-price points']);return}const b=hi>lo?Math.round(20*(hi-c)/(hi-lo)):20;x.s+=b;x.why.push(['+'+b,c==lo?'lowest price here ('+(c?m$(c)+'/mo':'$0 on the free plan')+')':m$(c)+'/mo vs lowest '+m$(lo)+'/mo'])})}
if(v.pri=='privacy')keep.forEach(x=>{const st=x.t.F.privacy[0];const b=st=='y'?20:st=='p'?8:0;x.s+=b;x.why.push(['+'+b,st=='u'?'privacy not checked yet':x.t.F.privacy[1]])});
if(v.pri=='free')keep.forEach(x=>{const b=x.t.fr?20:0;x.s+=b;x.why.push(['+'+b,x.t.fr?'real free plan to start on':'no real free plan'])});
if(v.pri=='fit')keep.forEach(x=>{if(x.fit>=32){x.s+=10;x.why.push(['+10',v.w.startsWith('job')?'one of our 3 picks for this job':'our Best Value pick for this category'])}});
keep.sort((a,b)=>b.s-a.s||((a.P.c==null?1e9:a.P.c)-(b.P.c==null?1e9:b.P.c))||a.t.n.localeCompare(b.t.n));
return{keep:keep,out:out,v:v}}
function ckl(t,v,P,bs){const asked=MK.filter(k=>v.m[k]!='any');const ks=asked.length?asked:MK.filter(k=>t.F[k][0]=='y').slice(0,3);
return '<ul class="ck66" aria-label="What you asked for, for '+X(t.n)+'">'+ks.map(k=>{const f=t.F[k];const lab={y:'Yes',p:'Partly',n:'No',u:'Unclear or not checked'}[f[0]];return '<li class="'+f[0]+'"><span><span class="skip">'+lab+': </span><a href="'+GU[k](t.s)+'">'+X(ML[k])+'</a>: '+X(f[1])+(f[2]?' <span class="src">· <a href="'+X(f[2])+'" rel="noopener" target="_blank">source<span class="skip"> for '+X(t.n)+' (opens in a new tab)</span></a> · checked '+X(f[3])+'</span>':'')+(v.m[k]=='must'?' <span class="small">(must-have)</span>':'')+'</span></li>'}).join('')+'</ul>'}
function priceLine(t,v,P,bs){const who=v.seats+' seat'+(v.seats==1?'':'s')+', '+(v.bill=='m'?'monthly':'billed yearly');
if(v.budget=='free'||bs=='freeonly')return '<p class="pr66"><b>$0 on the free plan</b> <span class="small">'+X(t.F.free[1])+(P.c!=null?' · paid from '+m$(P.c)+'/mo ('+who+')':'')+'</span></p>';
return P.c!=null?'<p class="pr66"><b>'+m$(P.c)+'/mo</b> <span class="small">cheapest checked plan, '+who+(t.ps&&v.seats>1?' ('+m$(P.base)+' per seat × '+v.seats+')':(v.seats>1?' (price isn’t per seat)':''))+(P.note?' · '+X(P.note):'')+'</span></p>':'<p class="pr66 small check">'+X(cap(P.note))+'</p>'}
function card(x,i,v,top){const t=x.t;const b=(t.bv.length?'<span class="badge b-best">BEST VALUE</span>':'')+(x.bs=='freeonly'?'<span class="badge b-free">FREE PLAN ONLY</span>':(t.fr?'<span class="badge b-free">FREE PLAN</span>':''));
const why='<details'+(top?' open':'')+'><summary class="small"><b>Why #'+(i+1)+'</b> ('+x.s+' points)</summary><ul class="why66">'+x.why.map(w=>'<li><b>'+X(w[0])+'</b> '+X(w[1])+'</li>').join('')+'</ul></details>';
const team=v.seats>1&&t.tm?'<p class="small tm66"><b>Team plan:</b> '+t.tm+'</p>':'';
const lt=t.lt?'<p class="small">Note: '+X(t.lt)+'.</p>':'';
const us=t.us?' · <a href="/ai-usage-limits.html?tool='+t.s+'&amp;use=daily#picker">Usage limits</a>':'';
return '<article class="card'+(top?' best':'')+'"><div class="th"><span class="rk66" aria-hidden="true">'+(i+1)+'</span><span class="logo"><img src="https://www.google.com/s2/favicons?domain='+t.dm+'&amp;sz=64" alt="" width="28" height="28" loading="lazy"></span><div><div class="badges">'+b+'</div><h3><a href="'+t.u+'">'+(top?'':'<span class="skip">#'+(i+1)+' </span>')+X(t.n)+'</a></h3></div></div><p class="small"><b>Main job:</b> '+X(t.cl)+' · '+X(t.d)+'</p>'+priceLine(t,v,x.P,x.bs)+lt+ckl(t,v,x.P,x.bs)+team+why+'<p class="small meta">Price checked '+X(t.k)+' · <a href="'+X(t.pr)+'" rel="noopener" target="_blank">Official pricing<span class="skip"> for '+X(t.n)+' (opens in a new tab)</span></a> · <a href="'+t.u+'">Tool page</a>'+us+'</p></article>'}
function relax(R){const v=R.v,opts=[];MK.forEach(k=>{if(v.m[k]=='must'){const r=evaluate(v,{m:{[k]:'nice'}});if(r.keep.length>R.keep.length)opts.push(['m_'+k,'nice','Make “'+ML[k]+'” a nice-to-have',r.keep.length])}});
const up={free:'10','10':'25','25':'50','50':'any'}[v.budget];if(up){const r=evaluate(v,{budget:up});if(r.keep.length>R.keep.length)opts.push(['w2b',up,'Raise budget to '+BL[up].toLowerCase(),r.keep.length])}
if(v.w.startsWith('job:')){const c=JB[v.w.slice(4)].c;const r=evaluate(v,{w:'cat:'+c});if(r.keep.length>R.keep.length)opts.push(['w1','cat:'+c,'Look at all of '+CB[c].n,r.keep.length])}
const mu=MK.filter(k=>v.m[k]=='must');if(!opts.length&&mu.length>1){const mm={};mu.forEach(k=>mm[k]='nice');let r=evaluate(v,{m:mm});if(r.keep.length>R.keep.length)opts.push(['all','nice','Make all must-haves nice-to-haves',r.keep.length]);else if(v.budget!='any'){r=evaluate(v,{m:mm,budget:'any'});if(r.keep.length>R.keep.length)opts.push(['all','any','Make all must-haves nice-to-haves and allow any budget',r.keep.length])}}
if(!opts.length&&mu.length==1&&v.budget!='any'){const r=evaluate(v,{m:{[mu[0]]:'nice'},budget:'any'});if(r.keep.length>R.keep.length)opts.push(['one',mu[0],'Make “'+ML[mu[0]]+'” a nice-to-have and allow any budget',r.keep.length])}
return opts.slice(0,4)}
function render(focus){const v=vals();const out=$('res66'),st=$('wStatus');if(!v.w){st.textContent='Pick what you want to do first.';show(1);return}
const R=evaluate(v);const[a,b]=v.w.split(':');const job=a=='job'?JB[b]:null;const title=job?cap(job.l):'Anything in '+CB[b].n;
const asked=MK.filter(k=>v.m[k]!='any').map(k=>(v.m[k]=='must'?'Must: ':'Nice: ')+ML[k]);
const sum='<div class="sum66"><span class="small"><b>Your answers:</b></span>'+[[1,title],[2,BL[v.budget]+' · '+(v.bill=='m'?'monthly':'yearly')+' · '+v.seats+' seat'+(v.seats==1?'':'s')],[3,asked.length?asked.join(', '):'No must-haves'],[4,'Most important: '+PRL[v.pri]]].map(([s,l])=>'<button type="button" class="chip" data-edit="'+s+'">'+X(l)+' <span class="skip">(change)</span></button>').join('')+'</div>';
let h='<h2 id="res66h" tabindex="-1">'+(R.keep.length?'Your picks for '+X(title.toLowerCase()):'Nothing fits all your answers yet')+'</h2>'+sum;
const K=R.keep.slice(0,5);
if(K.length){h+='<section class="top66" aria-label="Our pick for you"><p class="small" style="margin:0 0 4px"><b>Our pick for you</b></p>'+card(K[0],0,v,true).replace('<article class="card best">','<div>').replace(/<\/article>$/,'</div>')+'</section>';
if(K.length>1)h+='<h3>Also worth a look</h3><div class="grid">'+K.slice(1).map((x,i)=>card(x,i+1,v,false)).join('')+'</div>';
const w=MK.filter(k=>v.m[k]!='any').map(k=>WANT[k]);if(v.pri=='cheap')w.unshift('price');if(v.pri=='privacy'&&!w.includes('privacy'))w.push('privacy');if(v.pri=='free'&&!w.includes('free'))w.push('free');
if(K.length>1)h+='<p><a class="btn" href="/compare-builder.html?tools='+K.slice(0,3).map(x=>x.t.s).join(',')+(w.length?'&amp;want='+w.join(','):'')+'">Compare your top '+Math.min(3,K.length)+' side by side →</a></p>';
if(R.keep.length>5)h+='<p class="small">'+(R.keep.length-5)+' more tool'+(R.keep.length-5==1?'':'s')+' also fit: '+R.keep.slice(5).map(x=>'<a href="'+x.t.u+'">'+X(x.t.n)+'</a>').join(', ')+'.</p>'}
else h+='<div class="pick"><b>No tool passes every rule</b> — we don’t bend your budget or must-haves, and we don’t count tools we haven’t checked.</div>';
const rx=K.length<3?relax(R):[];if(rx.length)h+='<p style="margin:12px 0 0;font-weight:600">'+(K.length?'Want more options?':'Loosen a rule')+'</p><div class="rx66">'+rx.map(o=>'<button type="button" class="chip" data-rx="'+o[0]+'='+o[1]+'">'+X(o[2])+' → '+o[3]+' pick'+(o[3]==1?'':'s')+'</button>').join('')+'</div>';
if(R.out.length)h+='<details class="bnote lo66"'+(K.length?'':' open')+'><summary><h3 style="display:inline;margin:0;font-size:1rem">Left out and why ('+R.out.length+')</h3></summary><ul class="small" style="margin:8px 0 0">'+R.out.map(x=>'<li><a href="'+x.t.u+'">'+X(x.t.n)+'</a> — '+X(x.out)+'</li>').join('')+'</ul></details>';
const sh=share(v);h+='<p class="small">'+(job?'<a href="'+job.jp+'">Our top 3 for '+X(job.l)+' →</a> · ':'')+'<a href="/cost-calculator.html?'+(job?'tool='+K.concat(R.out)[0].t.s:'category='+b)+'&amp;seats='+v.seats+'&amp;billing='+(v.bill=='m'?'monthly':'annual')+'">True cost by seats →</a> · Share these picks: <a href="'+X(sh)+'">'+X(location.origin+sh)+'</a></p><p class="wnav" style="margin-top:8px"><button type="button" class="bbtn" id="wCopy">Copy link</button><button type="button" class="bbtn" id="wAgain">Start again</button></p>';
out.innerHTML=h;shown=true;history.replaceState(null,'',sh);
st.textContent=K.length?(R.keep.length+' tool'+(R.keep.length==1?'':'s')+' fit. Our pick for you: '+K[0].t.n+'.'):'No tool fits all your answers. See below for what was left out and why'+(document.querySelector('.rx66')?', and rules you could loosen.':'.');
if(focus){$('res66h').focus();$('res66h').scrollIntoView({behavior:'smooth',block:'start'})}}
function show(n){step=Math.min(4,Math.max(1,n));document.querySelectorAll('.wstep').forEach(s=>s.hidden=+s.dataset.step!=step);$('wbar').style.width=(step*25)+'%';$('wprog-label').textContent='Step '+step+' of 4';$('wBack').disabled=step==1;$('wNext').hidden=step==4;$('wGo').classList.toggle('primary',step==4)}
function next(){const v=vals();if(step==1&&!v.w){$('wStatus').textContent='Pick what you want to do to continue.';return}if(step<4){show(step+1);const f=document.querySelector('.wstep[data-step="'+step+'"] input:checked')||document.querySelector('.wstep[data-step="'+step+'"] input');if(f)f.focus()}else render(true)}
$('wNext').addEventListener('click',next);
$('wGo').addEventListener('click',()=>render(true));
$('wBack').addEventListener('click',()=>{if(step>1){show(step-1);const f=document.querySelector('.wstep[data-step="'+step+'"] input:checked')||document.querySelector('.wstep[data-step="'+step+'"] input');if(f)f.focus()}});
// pointer clicks on step 1-2 options move on (keyboard arrows never auto-advance)
document.getElementById('wform').addEventListener('click',ev=>{if(ev.target.tagName=='INPUT')return;const l=ev.target.closest('label');if(!l||ev.detail===0)return;const inp=l.querySelector('input[type=radio]');if(!inp)return;if(inp.name=='w1'&&step==1)setTimeout(()=>{if(shown)render(false);next()},120)});
document.getElementById('wform').addEventListener('change',()=>{if(shown)render(false)});
$('wseats').addEventListener('input',()=>{if(shown)render(false)});
$('w1f').addEventListener('input',()=>{const q=$('w1f').value.trim().toLowerCase();let any=0;document.querySelectorAll('.g66').forEach(gr=>{let n=0;gr.querySelectorAll('.o66').forEach(o=>{const hit=!q||q.split(/\s+/).every(w=>o.dataset.k.includes(w));o.hidden=!hit;if(hit)n++});gr.hidden=!n;any+=n});$('w1none').hidden=!!any});
$('res66').addEventListener('click',async ev=>{const ed=ev.target.closest('[data-edit]');if(ed){show(+ed.dataset.edit);document.querySelector('.builder').scrollIntoView({behavior:'smooth',block:'start'});const f=document.querySelector('.wstep[data-step="'+step+'"] input:checked')||document.querySelector('.wstep[data-step="'+step+'"] input');if(f)f.focus({preventScroll:true});return}
const rx=ev.target.closest('[data-rx]');if(rx){const[n,val]=rx.dataset.rx.split('=');if(n=='all'){MK.forEach(k=>{if(g('m_'+k)=='must')setR('m_'+k,'nice')});if(val=='any')setR('w2b','any')}else if(n=='one'){setR('m_'+val,'nice');setR('w2b','any')}else setR(n,val);render(true);return}
if(ev.target.id=='wCopy'){const u=location.href;try{await navigator.clipboard.writeText(u);$('wStatus').textContent='Link copied: '+u}catch(e){$('wStatus').textContent='Copy this link: '+u;window.prompt('Copy this link',u)}return}
if(ev.target.id=='wAgain'){$('wform').reset();$('res66').innerHTML='';shown=false;history.replaceState(null,'',location.pathname);show(1);$('wStatus').textContent='Cleared.';const f=document.querySelector('input[name=w1]');if(f)f.focus()}});
(function init(){const q=new URLSearchParams(location.search);let w=null;if(q.get('job')&&JB[q.get('job')])w='job:'+q.get('job');else if(q.get('category')&&CB[q.get('category')])w='cat:'+q.get('category');if(w)setR('w1',w);
const bu=q.get('budget');if(bu)setR('w2b',bu);const bi=q.get('billing');if(bi)setR('w2p',bi=='y'||bi=='annual'||bi=='yearly'?'y':'m');if(q.get('seats'))$('wseats').value=Math.min(50,Math.max(1,parseInt(q.get('seats'),10)||1));
MK.forEach(k=>{const x=q.get('m_'+k);if(x)setR('m_'+k,x)});if(q.get('free')=='required')setR('m_free','must');if(q.get('annual')=='required')setR('m_yearly','must');if(q.get('pri'))setR('w4',q.get('pri'));
show(1);if(w)render(false)})();"""
