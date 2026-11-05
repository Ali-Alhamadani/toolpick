"""v62 pages: Kling vs CapCut, free AI video limits, AI presentation cost. Called from build.py."""
import json, os
from tools import (
    PRESCOST, PRESCOST_CHECKED, PRESCOST_LEFT_OUT, V62_CHECKED, V62_LABEL,
    VIDEO4, FREE_LIMITS, FREE_CHECKED, FREE_SRC, FREE_SRC2, FREE_BEST, FREE_LEFT_OUT, NS,
)


def build_v62(ctx):
    page = ctx["page"]; e = ctx["e"]; turl = ctx["turl"]; find = ctx["find"]; slug = ctx["slug"]
    BASE = ctx["BASE"]; _faq = ctx["_faq"]; _ld_faq = ctx["_ld_faq"]; _ld_list = ctx["_ld_list"]
    crumbs = ctx["crumbs"]; faq = ctx["faq"]; _lm = ctx["_lm"]
    V4 = ctx["V4"]; KD = ctx["KD"]; _CRED = ctx["_CRED"]; FL = ctx["FL"]; _NS = ctx["_NS"]
    FREE_CHECKED_ = ctx["FREE_CHECKED"]
    V62_CHANGED = []

    def _v62ins(path, marker, html_s, after=False):
        fp = "public" + path
        if not os.path.exists(fp):
            return False
        h = open(fp).read()
        if ' v62"' in h or marker not in h:
            return False
        open(fp, "w").write(h.replace(marker, (marker + html_s) if after else (html_s + marker), 1))
        V62_CHANGED.append(path)
        return True

    def _d(v):
        if v is None:
            return "—"
        if v == 0:
            return "$0"
        if isinstance(v, float) and abs(v - int(v)) > 1e-9:
            return ("$%.2f" % v).rstrip("0").rstrip(".")
        return "$%s" % int(v)

    # ---------- 1) Kling vs CapCut ----------
    KC_PATH = "/kling-vs-capcut.html"
    names = ["Kling AI", "CapCut"]
    kv = {n: V4[n] for n in names}
    kd = kv["Kling AI"].get("checked", KD)
    cd = kv["CapCut"].get("checked", V62_CHECKED)

    def ysave(n):
        x = kv[n]
        if x.get("entry_y") is not None:
            return x["entry"] * 12 - x["entry_y"] * 12, x["entry_y"] * 12
        return x["entry"] * 12 - x["entry_yr"], x["entry_yr"]

    hd = "".join('<th scope="col"><a href="%s">%s</a></th>' % (turl(n), e(n)) for n in names)
    rows = [
        ("What it is", [
            "Text / image-to-video generator",
            "Video editor with AI features (not a generative-video subscription first)",
        ]),
        ("Free option", [e(kv[n]["free"]) for n in names]),
        ("Entry plan (monthly)", ["%s %s/mo" % (e(kv[n]["entry_name"]), _d(kv[n]["entry"])) for n in names]),
        ("Entry plan, paid yearly", [e(kv[n]["yearly"]) for n in names]),
        ("Yearly saving on entry plan", [
            "%s/yr (entry yearly total %s)" % (_d(ysave(n)[0]), _d(ysave(n)[1])) for n in names
        ]),
        ("Top plan (monthly)", ["%s %s/mo" % (e(kv[n]["top_name"]), _d(kv[n]["top"])) for n in names]),
        ("Current offer", [e(kv[n]["promo"]) for n in names]),
        ("Checked", [e(kv[n].get("checked", KD)) for n in names]),
        ("Source", [
            '<a href="%s" rel="noopener" target="_blank">%s</a>' % (
                kv[n]["url"], e(kv[n]["url"].split("//")[1])
            ) for n in names
        ]),
    ]
    tbl = (
        '<div class="tw"><table><caption class="small" style="text-align:left">'
        "Price and free plan only — no quality claims. Kling %s; CapCut %s.</caption>"
        '<tr><th scope="col"></th>%s</tr>'
    ) % (kd, cd, hd)
    tbl += "".join(
        '<tr><th scope="row">%s</th>' % a + "".join("<td>%s</td>" % v for v in vs) + "</tr>"
        for a, vs in rows
    ) + "</table></div>"

    qa_kc = [
        (
            "Is Kling cheaper than CapCut?",
            "On entry paid plans, yes: Kling Standard is $8.8/mo (or $6.99 for the first month, "
            "30%% off once) and CapCut Pro is $19.99/mo. Kling Standard yearly is $79.20/yr; "
            "CapCut Pro yearly is $179.99/yr. (Kling checked %s; CapCut checked %s.)" % (kd, cd),
        ),
        (
            "Which has a free plan?",
            "Both. Kling Basic is $0 (free credits not stated). CapCut has a free plan with basic "
            "editing and templates. CapCut's free plan is for editing; Kling's is for generative video.",
        ),
        (
            "Are Kling and CapCut the same kind of tool?",
            "No. Kling is a text/image-to-video generator. CapCut is primarily a video editor with "
            "AI features. We only compare price and free options here — not quality or features.",
        ),
        (
            "Does CapCut list credit counts?",
            "No. CapCut's pricing page shows Pro, Ultra and Teams dollar prices; it does not state "
            "a credit count we can compare with Kling's credits.",
        ),
        (
            "Which should I pick on price?",
            "Pick Kling if you want the lowest generative-video subscription. Pick CapCut if you "
            "want an editor and a free plan for basic editing.",
        ),
    ]
    body_kc = (
        '<p class="small"><a href="/compare-builder.html">Compare</a> › Kling vs CapCut</p>'
        "<h1>Kling vs CapCut: price &amp; free plan compared</h1>"
        '<p class="tag">Official prices only. Kling from its membership plan page (%s); '
        "CapCut from capcut.com/pricing (%s). We compare price and free options — not quality.</p>"
        % (kd, cd)
        + '<p class="pick"><b>Our pick:</b> <b>Kling</b> for the lowest generative-video subscription '
        "(Standard $8.8/mo, or $6.99 the first month). <b>CapCut</b> if you want a video editor plus "
        "a free plan for basic editing and templates. They do different jobs: Kling generates video; "
        "CapCut edits it.</p>"
        + tbl
        + _CRED
        + "<h2>Which to choose</h2><ul>"
        "<li><b>Cheapest generative-video bill:</b> Kling Standard at $8.8/mo ($79.20/yr), or $6.99 for the first month.</li>"
        "<li><b>Free editing to start:</b> CapCut's free plan with basic editing and templates.</li>"
        "<li><b>Heavier CapCut use:</b> CapCut Pro $19.99/mo ($179.99/yr) or Ultra $79/mo ($900/yr); Teams $12.49/seat/mo.</li>"
        "</ul>"
        + _faq(qa_kc)
        + '<p class="small">Related: <a href="/kling-pricing.html">Kling pricing</a> · '
        '<a href="/kling-vs-runway.html">Kling vs Runway</a> · <a href="%s">Kling AI</a> · '
        '<a href="%s">CapCut</a> · <a href="/best-ai-video-tools.html">Best AI video tools</a> · '
        '<a href="/free-ai-video-limits.html">Free AI video limits</a></p>'
        % (turl("Kling AI"), turl("CapCut"))
    )
    page(
        KC_PATH,
        "Kling vs CapCut (Nov 2026): Price & Free Plan Compared | ToolPick",
        "Kling vs CapCut on price and free plans: Kling Standard $8.8/mo vs CapCut Pro $19.99/mo; "
        "free options and yearly prices. Kling checked %s; CapCut checked %s." % (kd, cd),
        body_kc,
        _ld_list("Kling vs CapCut", KC_PATH, names)
        + [_ld_faq(qa_kc), crumbs([("ToolPick", "/"), ("Compare", "/compare-builder.html"), ("Kling vs CapCut", KC_PATH)])],
    )
    V62_CHANGED.append(KC_PATH)
    _lm[KC_PATH] = V62_CHECKED

    # ---------- 2) Free AI video limits ----------
    FV_PATH = "/free-ai-video-limits.html"
    fv_names = ["Runway", "Pika", "Kling AI", "HeyGen", "Descript", "CapCut"]
    fv_rows = [r for r in FL if r[0] in fv_names]
    assert set(r[0] for r in fv_rows) == set(fv_names), fv_rows

    def fv_cell(v):
        if v == _NS:
            return '<span class="small" style="color:var(--mu)">not stated</span>'
        return e(v)

    cards = []
    for n, inc, lim, wm, com, up in fv_rows:
        src = FREE_SRC.get(n, find(n).get("pricing", "#"))
        s2 = FREE_SRC2.get(n)
        extra = ""
        if s2:
            extra = ' · <a href="%s" rel="noopener" target="_blank">Help/terms</a>' % e(s2)
        cards.append(
            '<article class="card fv-card" data-free="yes">'
            '<h3><a href="%s">%s</a></h3>'
            '<p class="small" style="margin:0 0 6px">Checked %s · '
            '<a href="%s" rel="noopener" target="_blank">Official pricing'
            '<span class="skip"> for %s (opens in a new tab)</span></a>%s</p>'
            "<p><b>Free includes:</b> %s</p>"
            "<p><b>Main limit:</b> %s</p>"
            "<p><b>Watermark:</b> %s</p>"
            "<p><b>Commercial use:</b> %s</p>"
            "<p><b>Cheapest upgrade:</b> %s</p>"
            '<p class="small" style="margin:0"><a href="%s">%s on ToolPick →</a></p>'
            "</article>"
            % (
                turl(n), e(n), FREE_CHECKED_, e(src), e(n), extra,
                fv_cell(inc), fv_cell(lim), fv_cell(wm), fv_cell(com), fv_cell(up),
                turl(n), e(n),
            )
        )
    fv_best = FREE_BEST.get("video", ("Descript", "60 media minutes a month with 720p export"))
    left = [(n, r) for n, r in FREE_LEFT_OUT if n == "Luma Dream Machine"]
    not_checked = [
        ("Synthesia", "we have not verified their free limits on the free-plan-limits check date"),
        ("InVideo", "we have not verified their free limits on the free-plan-limits check date"),
        ("Opus Clip", "we have not verified their free limits on the free-plan-limits check date"),
        ("Captions", "we have not verified their free limits on the free-plan-limits check date"),
    ]
    qa_fv = [
        (
            "Which AI video tools have a free plan?",
            "On our free-plan-limits check (%s): Runway, Pika, Kling AI, HeyGen, Descript and CapCut. "
            "Luma Dream Machine lists no free plan." % FREE_CHECKED_,
        ),
        (
            "What's the best free AI video plan on this page?",
            "%s — %s (from our free-plan-limits best pick for video)." % (fv_best[0], fv_best[1]),
        ),
        (
            "Why aren't Synthesia, InVideo, Opus Clip or Captions here?",
            "We have not verified their free limits on the free-plan-limits check date, so we don't invent numbers for them.",
        ),
        (
            "Where do Kling's paid plan prices come from?",
            "This page uses free-plan limits checked %s. For Kling's paid plans and first-month offer, "
            "see the Kling pricing page (checked %s)." % (FREE_CHECKED_, KD),
        ),
    ]
    body_fv = (
        '<style>.fv-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}'
        ".fv-card p{margin:4px 0}.fv-chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}"
        ".fv-chips button{min-height:44px;min-width:44px;padding:0 16px;border-radius:999px;"
        "border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;cursor:pointer}"
        ".fv-chips button[aria-pressed=true]{background:var(--ac);color:var(--sf);border-color:var(--ac)}</style>"
        '<p class="small"><a href="/free.html">Free tools</a> › Free AI video limits</p>'
        "<h1>Free AI video plan limits</h1>"
        '<p class="tag">Side-by-side free plans for video tools only. Every number comes from FREE_LIMITS, '
        "checked %s on each official pricing page. “not stated” means the page didn't say.</p>" % FREE_CHECKED_
        + '<p class="pick"><b>Quick pick:</b> %s — %s. CapCut is free for basic editing; Kling Basic is $0 '
        "(credits not stated); Runway Free gives 125 one-time credits with a watermark. Also see "
        '<a href="/kling-pricing.html">Kling pricing (%s)</a> for paid Kling plans.</p>'
        % (fv_best[0], fv_best[1], KD)
        + '<div class="fv-chips" role="group" aria-label="Filter free plans">'
        '<button type="button" data-f="all" aria-pressed="true">All</button>'
        '<button type="button" data-f="free" aria-pressed="false">Has free plan</button></div>'
        '<p id="fv-n" class="small" role="status"></p>'
        '<div class="fv-grid" id="fv-grid">%s</div>' % "".join(cards)
        + "<h2>Not in this table</h2><ul>"
        + "".join("<li><b>%s</b>: %s.</li>" % (e(n), e(r)) for n, r in left + not_checked)
        + "</ul>"
        + '<p class="small">Source date for every card above: %s. Full cross-category table: '
        '<a href="/free-plan-limits.html?cat=video">Free plan limits (video filter)</a>.</p>' % FREE_CHECKED_
        + _faq(qa_fv)
        + '<p class="small">Related: <a href="/free-plan-limits.html">Free plan limits</a> · '
        '<a href="/best-free-ai-video-tools.html">Best free AI video tools</a> · '
        '<a href="/free.html">Can I do it for free?</a> · '
        '<a href="/kling-vs-capcut.html">Kling vs CapCut</a> · <a href="/guides.html">Guides</a></p>'
        + "<script>(()=>{const G=document.getElementById('fv-grid'),N=document.getElementById('fv-n'),"
        "C=[...G.children],B=[...document.querySelectorAll('.fv-chips button')];"
        "function run(f){let k=0;C.forEach(c=>{const on=f==='all'||c.dataset.free==='yes';c.hidden=!on;if(on)k++});"
        "N.textContent=k+' tool'+(k===1?'':'s')+' shown';"
        "B.forEach(b=>b.setAttribute('aria-pressed',b.dataset.f===f?'true':'false'))}"
        "B.forEach(b=>b.addEventListener('click',()=>run(b.dataset.f)));run('all')})()</script>"
    )
    page(
        FV_PATH,
        "Free AI Video Plan Limits (%s): Runway, Pika, Kling, CapCut & More | ToolPick" % FREE_CHECKED_[:4],
        "Free plan limits for AI video tools side by side: Runway, Pika, Kling AI, HeyGen, Descript and CapCut "
        "— inclusions, watermarks, commercial use and cheapest upgrades, checked %s." % FREE_CHECKED_,
        body_fv,
        [
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "Free AI video plan limits",
                "url": BASE + FV_PATH,
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": r[0], "url": BASE + turl(r[0])}
                    for i, r in enumerate(fv_rows)
                ],
            },
            _ld_faq(qa_fv),
            crumbs([("ToolPick", "/"), ("Free tools", "/free.html"), ("Free AI video limits", FV_PATH)]),
        ],
    )
    V62_CHANGED.append(FV_PATH)
    _lm[FV_PATH] = FREE_CHECKED_

    # ---------- 3) AI presentation cost ----------
    # Continued in build_v62_prescost called below
    from v62_prescost import build_prescost
    PC_PATH, PCD = build_prescost(ctx, V62_CHANGED)

    # Cross-links
    KCL = '<a href="%s">Kling vs CapCut</a>' % KC_PATH
    FVL = '<a href="%s">Free AI video limits</a>' % FV_PATH
    PCL = '<a href="%s">AI presentation cost calculator</a>' % PC_PATH
    _v62ins(turl("Kling AI"), '<section class="verdict',
            '<p class="pick small v62">Price vs CapCut (editor + free plan): %s · %s</p>' % (KCL, FVL))
    _v62ins(turl("CapCut"), '<section class="verdict',
            '<p class="pick small v62">Price vs Kling (generative video): %s · %s</p>' % (KCL, FVL))
    for p in ["/kling-pricing.html", "/kling-vs-runway.html", "/kling-vs-pika-vs-luma.html", "/best-ai-video-tools.html"]:
        _v62ins(p, "</h1>", '<p class="small v62">%s · %s</p>' % (KCL, FVL), after=True)
    for p in ["/free-plan-limits.html", "/best-free-ai-video-tools.html", "/free.html"]:
        _v62ins(p, "</h1>",
                '<p class="pick small v62">Video free plans only, friendlier cards: %s →</p>' % FVL, after=True)
    for d in PCD:
        others = ", ".join(e(x["n"]) for x in PCD if x is not d)
        _v62ins(
            d["u"],
            '<section class="card tbp"',
            '<p class="pick v62"><b>What will %s cost for your seats?</b> Compare with %s: '
            '<a href="%s">AI presentation cost calculator →</a></p>' % (e(d["n"]), others, PC_PATH),
        )
    for p in [
        "/best-ai-presentations-tools.html",
        "/best-free-ai-presentations-tools.html",
        "/best-ai-tool-for-pitch-decks.html",
        "/save-money.html",
    ]:
        _v62ins(
            p, "</h1>",
            '<p class="pick small v62">Paying for slides? See Gamma, Canva, Pitch and more by seats: %s →</p>' % PCL,
            after=True,
        )
    _v62ins(
        "/guides.html",
        "<h2>New guides</h2><ul>",
        '<li class="v62"><a href="%s">Kling vs CapCut: price and free plan</a></li>'
        '<li class="v62"><a href="%s">Free AI video plan limits (friendly cards)</a></li>'
        '<li class="v62"><a href="%s">AI presentation cost calculator: Gamma, Canva, Pitch and more by seats</a></li>'
        % (KC_PATH, FV_PATH, PC_PATH),
        after=True,
    )
    print("v62 pages:", KC_PATH, FV_PATH, PC_PATH, ";", len(V62_CHANGED), "pages touched;", len(PCD), "presentation tools")
    open("public/llms.txt", "a").write(
        "\n## Kling vs CapCut, free video limits, presentation cost (v62)\n"
        "- [Kling vs CapCut](%s%s): generative-video vs editor prices; Kling Standard $8.8/mo vs CapCut Pro $19.99/mo; "
        "free plans; Kling checked %s, CapCut checked %s\n"
        "- [Free AI video plan limits](%s%s): Runway, Pika, Kling AI, HeyGen, Descript, CapCut free "
        "inclusions/limits/watermarks/commercial use/upgrades from FREE_LIMITS checked %s\n"
        "- [AI presentation cost calculator](%s%s): Gamma, Canva, Pitch (EUR), Beautiful.ai, Plus AI, SlidesAI "
        "by seats and monthly/yearly; Pitch excluded from USD cheapest; deep link %s?seats=5&bill=y\n"
        % (BASE, KC_PATH, kd, cd, BASE, FV_PATH, FREE_CHECKED_, BASE, PC_PATH, PC_PATH)
    )
    return V62_CHANGED
