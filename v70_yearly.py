"""v70: Monthly vs yearly - how much does annual billing really save? (/monthly-or-yearly.html, rebuilt).
For every tool we track: the cheapest paid plan's monthly price and billed-yearly price, read on the official pricing page on
2026-11-13 with the exact words (tools.py V70_YEARLY), the % and $ saved per year, and the break-even month (from which month
on paying a year upfront costs no more than paying monthly). A "How long will you use it?" calculator (?tool=&months=),
filters with URL state (?cat=&show=&sort=&q=), summary boxes, short answers, a card per tool, and a savings box on every
tool page. Tools whose page shows only one price, no fixed price, or that we couldn't read are labelled - never guessed."""
import json, math, re

V70_DATE = "2026-11-13"
PATH = "/monthly-or-yearly.html"
SHOW = [("save", "Saves with yearly billing"), ("same", "No saving for yearly"), ("mo", "Monthly only (no yearly price)"),
        ("yr", "Only a yearly price shown"), ("none", "No fixed plan price"), ("nc", "Couldn't check tonight")]
SORT = [("pct", "Biggest % saving"), ("usd", "Biggest $ saving per year"), ("be", "Fastest break-even"), ("cheap", "Cheapest per month"), ("az", "A to Z")]


def money(v):
    r = round(v + 1e-9, 2)
    return "$" + (f"{int(r):,}" if r == int(r) else f"{r:,.2f}")


def calc(rows):
    """name -> dict(pl, m, y (per month billed yearly), yt (yearly total), st, save, pct, be, qm, qy, src, note)."""
    V = {}
    for n, pl, m, y, yt, st, qm, qy, src, note in rows:
        yt2 = yt if yt is not None else (round(y * 12, 2) if y is not None else None)
        ypm = y if y is not None else (round(yt / 12, 2) if yt is not None else None)
        d = dict(n=n, pl=pl, m=m, y=ypm, yt=yt2, st=st, qm=qm, qy=qy, src=src, note=note, save=None, pct=None, be=None)
        if st == "both":
            save = round(m * 12 - yt2, 2)
            d.update(save=save, pct=round(save / (m * 12) * 100), be=max(1, math.ceil(round(yt2 / m, 6))))
            d["code"] = "save" if save > 0 else "same"
        else:
            d["code"] = st
        V[n] = d
    return V


def build_v70(ctx):
    page = ctx["page"]; e = ctx["e"]; slug = ctx["slug"]; turl = ctx["turl"]; BASE = ctx["BASE"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]
    _lm = ctx["_lm"]; URLS = ctx["URLS"]; CATS = ctx["CATEGORIES"]; T = ctx["tools"]; RF = ctx["refunds"]; OLD = ctx["old"]
    V = calc(T.V70_YEARLY); ck = T.V70_CK
    cat1 = {}
    for c in CATS:
        for t in c["tools"]: cat1.setdefault(t["name"], c)
    names = sorted(cat1, key=str.lower)
    assert set(names) == set(V), ("v70: tool list mismatch", set(names) ^ set(V))
    cnt = {}
    for n in names: cnt[V[n]["code"]] = cnt.get(V[n]["code"], 0) + 1
    sv = [V[n] for n in names if V[n]["code"] == "save"]
    def alt(n): return "/cursor-alternatives.html" if n == "Cursor" else f"/alternatives/{slug(n)}.html"
    def src(n):
        r = V[n]
        return f'<p class="s70"><a href="{e(r["src"])}" rel="noopener" target="_blank">Official pricing page<span class="skip"> for {e(n)} (opens in a new tab)</span></a> · checked {ck}</p>'
    def quotes(r):
        q = [x for x in (r["qm"], r["qy"]) if x]
        if not q: return ""
        return '<details><summary>What the page says</summary>' + "".join(f'<blockquote>“{e(x)}”</blockquote>' for x in q) + '</details>'
    # ---------- cards ----------
    cards = []; data = []
    for n in names:
        r = V[n]; c = cat1[n]; code = r["code"]
        if code in ("save", "same"):
            fig = (f'<dl class="g70"><div><dt>Monthly</dt><dd>{money(r["m"])}<small>/mo</small></dd></div>'
                   f'<div><dt>Billed yearly</dt><dd>{money(r["y"])}<small>/mo</small></dd><dd class="u70">{money(r["yt"])} upfront</dd></div>'
                   f'<div class="{"k70" if code == "save" else ""}"><dt>Yearly saves</dt><dd>{(str(r["pct"]) + "%") if code == "save" else "0%"}</dd><dd class="u70">{money(max(r["save"], 0))}/yr</dd></div>'
                   f'<div><dt>Break-even</dt><dd>{"month " + str(r["be"]) if code == "save" else "—"}</dd></div></dl>')
            if code == "save":
                verdict = (f'<p class="v70 y"><b>Pay yearly if you’ll keep it {r["be"]}+ months.</b> Monthly for {r["be"] - 1} months costs {money(r["m"] * (r["be"] - 1))}; '
                           f'a year upfront is {money(r["yt"])}.</p>' if r["be"] > 1 else f'<p class="v70 y"><b>A year costs no more than one month.</b></p>')
            else:
                verdict = '<p class="v70 n"><b>Stay monthly:</b> paying yearly doesn’t save anything on this plan.</p>'
        elif code == "mo":
            fig = f'<dl class="g70 one"><div><dt>Monthly</dt><dd>{money(r["m"])}<small>/mo</small></dd></div><div><dt>Billed yearly</dt><dd class="na70">No yearly price</dd></div></dl>'
            verdict = '<p class="v70 p"><b>Monthly only</b> on its pricing page, so there’s nothing to save by paying upfront.</p>'
        elif code == "yr":
            fig = (f'<dl class="g70 one"><div><dt>Monthly</dt><dd class="na70">Not shown</dd></div><div><dt>Billed yearly</dt><dd>{money(r["y"])}<small>/mo</small></dd>'
                   + (f'<dd class="u70">{money(r["yt"])} upfront</dd>' if r["yt"] else "") + '</div></dl>')
            verdict = '<p class="v70 p"><b>Only a yearly price is shown</b>, so we can’t work out the saving. Check the page for a monthly option before you commit.</p>'
        elif code == "none":
            fig = ""; verdict = '<p class="v70 p"><b>No fixed plan price:</b> it’s usage-based or custom, so monthly vs yearly doesn’t apply.</p>'
        else:
            fig = ""; o = OLD.get(n)
            verdict = ('<p class="v70 u"><b>Couldn’t check tonight.</b></p>'
                       + (f'<p class="small">Our last check ({e(o[2])}): {money(o[0])}/mo monthly, {money(o[1])}/mo billed yearly.</p>' if o else ""))
        note = f'<p class="small">{e(r["note"])}</p>' if r["note"] else ""
        refund = RF.get(n)
        rl = f'<p class="small r70"><b>Refunds:</b> {e(refund[1])}' + (f' (checked {refund[2]})' if refund[2] else "") + '</p>' if refund and refund[0] != "nc" else ""
        key = " ".join([n, c["name"], r["pl"]]).lower()
        cards.append(f'<article class="card c70" id="t-{slug(n)}" data-n="{e(n.lower())}" data-k="{e(key)}" data-c="{c["id"]}" data-st="{code}"'
                     f' data-pct="{r["pct"] if code == "save" else -1}" data-usd="{r["save"] if code == "save" else -1}" data-be="{r["be"] if code == "save" else 99}"'
                     f' data-cheap="{min([x for x in (r["m"], r["y"]) if x is not None], default=9999)}">'
                     f'<h3><a href="{turl(n)}">{e(n)}</a> <span class="small">{e(c["name"])} · {e(r["pl"])}</span></h3>{fig}{verdict}{rl}{note}{quotes(r)}{src(n)}'
                     f'<p class="a70"><a href="{turl(n)}">{e(n)} prices &amp; review</a><a href="{alt(n)}?want=yearly">Alternatives that save yearly</a></p></article>')
        data.append(dict(s=slug(n), n=n, pl=r["pl"], m=r["m"], y=r["y"], yt=r["yt"], c=code, be=r["be"], sv=r["save"], p=r["pct"],
                         rf=(refund[1] if refund and refund[0] != "nc" else ""), rk=(refund[0] if refund else "nc")))
    # ---------- summary ----------
    pcts = sorted(x["pct"] for x in sv)
    med = pcts[len(pcts) // 2] if pcts else 0
    top_usd = max(sv, key=lambda x: x["save"]) if sv else None
    def box(code, lab, extra=""):
        return f'<a class="sb70 {"y" if code == "save" else ("n" if code == "same" else "p")}" href="{PATH}?show={code}#all70"><b>{cnt.get(code, 0)}</b><span>{e(lab)}{extra}</span></a>'
    summ = (f'<div class="sm70" aria-label="Summary">'
            + box("save", "save money with yearly billing") + box("mo", "are monthly only") + box("yr", "show only a yearly price")
            + f'<a class="sb70 p" href="{PATH}?show=none#all70"><b>{cnt.get("none", 0) + cnt.get("nc", 0)}</b><span>usage-based, custom or not checkable tonight</span></a>'
            + f'<div class="sb70 k"><b>{med}%</b><span>typical (median) yearly discount</span></div>'
            + (f'<a class="sb70 k" href="#t-{slug(top_usd["n"])}"><b>{money(top_usd["save"])}</b><span>biggest saving per year ({e(top_usd["n"])})</span></a>' if top_usd else "")
            + '</div>')
    def nl(xs, f=None): return ", ".join(f'<a href="#t-{slug(x["n"])}">{e(x["n"])}</a>' + (f" ({f(x)})" if f else "") for x in xs) or "none"
    by_pct = sorted(sv, key=lambda x: (-x["pct"], -x["save"], x["n"].lower()))
    by_usd = sorted(sv, key=lambda x: (-x["save"], x["n"].lower()))
    small = sorted([x for x in sv if x["pct"] <= 12], key=lambda x: (x["pct"], x["n"].lower()))
    mo_only = [V[n] for n in names if V[n]["code"] == "mo"]
    quick = (f'<section class="card q70" aria-labelledby="q70h"><h2 id="q70h" style="margin:0;font-size:1.1rem">Short answer</h2><dl>'
             f'<dt>Biggest % off for yearly</dt><dd>{nl(by_pct[:8], lambda x: str(x["pct"]) + "%")}</dd>'
             f'<dt>Most dollars saved a year</dt><dd>{nl(by_usd[:6], lambda x: money(x["save"]))}</dd>'
             f'<dt>Small yearly discounts (≤12%)</dt><dd>{nl(small)}</dd>'
             f'<dt>Monthly only</dt><dd>{nl(mo_only)}</dd></dl>'
             f'<p class="small" style="margin:8px 0 0">Rule of thumb: a 17% discount (“2 months free”) pays off from month 10; 50% off pays off from month 6. If you might stop sooner, stay monthly.</p></section>')
    # ---------- calculator ----------
    opts = '<option value="">Choose a tool…</option>' + "".join(f'<option value="{slug(n)}">{e(n)}</option>' for n in names)
    calc_html = (f'<section class="card k70c" id="calc" aria-labelledby="calch"><h2 id="calch" style="margin:0 0 4px;font-size:1.15rem">Should you pay yearly? Work it out for your plan</h2>'
                 f'<form class="cf70" id="cf70" action="{PATH}" method="get"><label class="l70"><span>The tool</span><select id="x70t" name="tool">{opts}</select></label>'
                 f'<label class="l70"><span>How many months will you use it?</span><input id="x70m" name="months" type="number" min="1" max="36" step="1" value="12" inputmode="numeric"></label>'
                 f'<noscript><button type="submit" class="bt">Show</button></noscript></form>'
                 f'<div id="o70" role="status" aria-live="polite"><p class="small">Pick a tool to see what monthly and yearly would cost you, and from which month yearly pays off.</p></div></section>')
    # ---------- filters ----------
    catopt = '<option value="">All categories</option>' + "".join(f'<option value="{c["id"]}">{e(c["name"])}</option>' for c in CATS)
    showopt = '<option value="">All tools</option>' + "".join(f'<option value="{v}">{e(t)} ({cnt.get(v, 0)})</option>' for v, t in SHOW if cnt.get(v))
    sortopt = "".join(f'<option value="{v}">{e(t)}</option>' for v, t in SORT)
    filt = (f'<form class="fl70" id="f70" action="{PATH}" method="get" role="search" aria-label="Filter AI tools by yearly saving">'
            f'<label class="l70"><span>Show</span><select id="x70s" name="show">{showopt}</select></label>'
            f'<label class="l70"><span>Category</span><select id="x70c" name="cat">{catopt}</select></label>'
            f'<label class="l70"><span>Sort</span><select id="x70o" name="sort">{sortopt}</select></label>'
            f'<label class="l70 q"><span>Find a tool</span><input id="x70q" name="q" type="search" placeholder="e.g. Canva, Claude, video" autocomplete="off"></label>'
            f'<p class="bt70"><button type="button" id="x70x">Clear all</button></p></form>'
            f'<p id="st70" class="small" role="status" aria-live="polite">Showing all {len(names)} tools, biggest % saving first.</p>')
    pre = "".join(f'<a class="p70" href="{PATH}?{q}#all70">{e(l)}</a>' for q, l in [
        ("show=save&sort=pct", f"Biggest yearly discounts ({cnt.get('save', 0)})"), ("show=save&sort=usd", "Most $ saved a year"),
        ("show=save&sort=be", "Pays off soonest"), ("show=mo", f"Monthly only ({cnt.get('mo', 0)})")])
    # ---------- order: biggest % saving first (no-JS default) ----------
    order = {"save": 0, "same": 1, "mo": 2, "yr": 3, "none": 4, "nc": 5}
    idx = sorted(range(len(names)), key=lambda i: (order[V[names[i]]["code"]], -(V[names[i]]["pct"] or 0), -(V[names[i]]["save"] or 0), names[i].lower()))
    cards = [cards[i] for i in idx]
    # ---------- page ----------
    qa = [("Is it cheaper to pay for AI tools yearly?",
           f"Usually, yes - {cnt.get('save', 0)} of the {len(names)} tools we track charge less per month on a yearly plan. The typical (median) discount is {med}%, from {pcts[0] if pcts else 0}% to {pcts[-1] if pcts else 0}%. But you pay the whole year upfront, and {sum(1 for d in data if d['c'] == 'save' and d['rk'] == 'none')} of those tools say payments are non-refundable, so only pay yearly if you'll keep it past the break-even month."),
          ("What is the break-even month?",
           "It's the month from which paying a year upfront costs no more than paying monthly. We work it out as the yearly price divided by the monthly price, rounded up. If you might cancel before that month, monthly is cheaper."),
          ("Which AI tools have the biggest yearly discount?", "Biggest % off: " + ", ".join(f"{x['n']} ({x['pct']}%)" for x in by_pct[:6]) + ". Most dollars saved a year: " + ", ".join(f"{x['n']} ({money(x['save'])})" for x in by_usd[:4]) + "."),
          ("Which AI tools are monthly only?", "On their pricing pages these show no yearly price for the cheapest paid plan: " + ", ".join(x["n"] for x in mo_only) + "."),
          ("Where do the prices come from?", f"From each tool's official pricing page, read on {ck} with the page's exact words shown on every card. We compare the cheapest paid plan on the same plan, monthly vs billed yearly, in US dollars before tax. Intro offers (like a cheaper first month) are not counted. If a page shows only one price, no fixed price, or we couldn't read it, the card says so instead of guessing.")]
    fh, fld = faq(qa)
    nojs = '<noscript><style>.fl70,#st70,.k70c{display:none!important}</style><p class="small">Filters and the calculator need JavaScript. All tools are listed below, biggest yearly saving first.</p></noscript>'
    body = (f'{CSS}{nojs}<p class="small"><a href="/save-money.html">Save money</a> › Monthly or yearly?</p>'
            f'<h1>Monthly vs yearly: how much does annual billing really save?</h1>'
            f'<p class="tag">All {len(names)} AI tools we track: the monthly price, the yearly price, how much a year upfront saves (in % and dollars) and the month it starts paying off. Every price was read on the tool’s official pricing page on Nov 13, 2026, with the exact words and a link.</p>'
            f'<p class="small">Cheapest paid plan, US dollars before tax, list prices (not first-month offers). Prices change, so open the source before you buy.</p>'
            + calc_html + summ + quick + f'<h2 id="all70">Every tool: monthly vs yearly</h2><div class="pr70">{pre}</div>' + filt
            + f'<p class="e70" id="e70" hidden>No tool matches all of those. <button type="button" id="x70y">Clear the filters</button></p>'
            + f'<div class="l70g" id="l70">{"".join(cards)}</div>'
            + f'<p class="small">How we check: we open each tool’s official pricing page, read the cheapest paid plan with the monthly and the yearly toggle, and copy the words. Saving per year = monthly price × 12 − the yearly total (the stated yearly total when the page gives one, otherwise the per-month yearly price × 12). % saved = that saving ÷ (monthly × 12). Break-even month = yearly total ÷ monthly price, rounded up. Per-seat prices are for one seat. <a href="/how-we-pick.html">How we pick</a></p>'
            + f'{fh}<p class="small">Related: <a href="/ai-privacy-refund-checker.html?refund=window">AI tools with a refund window</a> · <a href="/pay-less.html">Pay less for the same job</a> · <a href="/ai-price-history.html">AI price history</a> · <a href="/compare-builder.html">Compare any 2-3 tools</a> · <a href="/help-me-choose.html?billing=y&amp;m_yearly=must">Find a tool that’s cheaper yearly</a> · <a href="/save-money.html">Save money hub</a></p>'
            + f'<script>const D70={json.dumps(data, separators=(",", ":")).replace("</", "<\\/")};{JS}</script>')
    title = f"Monthly vs Yearly: How Much Does Annual Billing Save? {len(names)} AI Tools, Break-Even Month | ToolPick"
    desc = (f"Monthly vs yearly prices for {len(names)} AI tools, read on official pricing pages Nov 13, 2026: {cnt.get('save', 0)} save with yearly billing "
            f"(median {med}%), {cnt.get('mo', 0)} are monthly only. See % and $ saved per year and the break-even month.")
    ld = [{"@context": "https://schema.org", "@type": "Dataset", "name": "AI tool monthly vs yearly prices", "url": BASE + PATH,
           "description": f"Monthly and billed-yearly price of the cheapest paid plan for {len(names)} AI tools, with yearly saving, break-even month, exact pricing-page quotes and checked date.",
           "dateModified": V70_DATE, "creator": {"@type": "Organization", "name": "ToolPick", "url": BASE + "/"}, "isAccessibleForFree": True,
           "license": "https://creativecommons.org/licenses/by/4.0/", "variableMeasured": ["Monthly price", "Yearly price", "Yearly saving (%)", "Yearly saving (USD)", "Break-even month"]},
          fld, crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("Monthly or yearly?", PATH)])]
    had = PATH in URLS
    page(PATH, title, desc, body, ld)
    if had: URLS.pop()  # the URL is already in the sitemap list (older v19 page at the same address)
    _lm[PATH] = V70_DATE
    S = dict(cnt=cnt, total=len(names), med=med, top=(top_usd["n"], top_usd["save"]) if top_usd else None, both=sum(1 for n in names if V[n]["st"] == "both"))
    return V, S


def link_v70(ctx, V, S):
    """Tool pages: a 'Monthly or yearly?' box (#yearly-saving) before the privacy box. Save-money hub + guides: a pointer."""
    e = ctx["e"]; slug = ctx["slug"]; changed = []
    for n, r in V.items():
        fp = f"public/tools/{slug(n)}.html"
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' tp70"' in h: continue
        code = r["code"]
        if code == "save":
            li = (f'<li><b>Monthly</b> {money(r["m"])}/mo</li><li><b>Billed yearly</b> {money(r["y"])}/mo ({money(r["yt"])} upfront)</li>'
                  f'<li class="y"><b>Yearly saves</b> {r["pct"]}% · {money(r["save"])} a year</li><li><b>Break-even</b> month {r["be"]}: pay yearly only if you’ll keep it that long</li>')
        elif code == "same":
            li = f'<li><b>Monthly</b> {money(r["m"])}/mo</li><li><b>Billed yearly</b> {money(r["y"])}/mo</li><li class="n"><b>Yearly saves</b> nothing on this plan, so stay monthly</li>'
        elif code == "mo":
            li = f'<li><b>Monthly</b> {money(r["m"])}/mo</li><li><b>Billed yearly</b> no yearly price on its pricing page</li>'
        elif code == "yr":
            li = f'<li><b>Monthly</b> not shown on its pricing page</li><li><b>Billed yearly</b> {money(r["y"])}/mo' + (f' ({money(r["yt"])} upfront)' if r["yt"] else "") + '</li>'
        elif code == "none":
            li = '<li>No fixed plan price (usage-based or custom), so monthly vs yearly doesn’t apply.</li>'
        else:
            li = '<li>We couldn’t read its monthly and yearly prices on Nov 13, 2026.</li>'
        box = ('<style>.tp70 ul{list-style:none;margin:6px 0 0;padding:0}.tp70 li{margin:4px 0;font-size:.95rem}.tp70 li b{display:inline-block;min-width:8.5em}.tp70 li.y b,.tp70 li.y{color:var(--ok)}.tp70 li.y b{color:inherit}.tp70 li.y{font-weight:600}.tp70 .small{color:var(--mu)}.tp70 p>a{display:inline;padding:0}@media(max-width:640px){.tp70 li b{display:block;min-width:0}}</style>'
               f'<section class="card tp70 pick" style="margin-bottom:16px" id="yearly-saving" aria-labelledby="ys70"><h2 id="ys70" style="margin:0;font-size:1.1rem">{e(n)}: monthly or yearly? <span class="small" style="font-weight:400">{e(r["pl"])} plan</span></h2><ul>{li}</ul>'
               f'<p style="margin:8px 0 0"><a href="{PATH}?tool={slug(n)}#calc"><b>Work it out for how long you’ll use it&nbsp;→</b></a></p>'
               f'<p class="small" style="margin:2px 0 0"><a href="{e(r["src"])}" rel="noopener" target="_blank">Official pricing page<span class="skip"> for {e(n)} (opens in a new tab)</span></a> · checked {V70_DATE} · <a href="{PATH}">all {S["total"]} tools</a></p></section>')
        a = '<section class="card tp69' if '<section class="card tp69' in h else None
        if not a: continue
        h = h.replace(a, box + a, 1)
        open(fp, "w").write(h); changed.append(f"/tools/{slug(n)}.html")
    c = S["cnt"]
    note = (f'<p class="pick small v70" style="margin:12px 0">New: <a href="{PATH}"><b>Monthly vs yearly: how much does annual billing really save?</b></a> All {S["total"]} tools re-checked on Nov 13, 2026: '
            f'{c.get("save", 0)} save with yearly billing (median {S["med"]}%), {c.get("mo", 0)} are monthly only, with the break-even month for each.</p>')
    for p_ in ("/save-money.html", "/pay-less.html", "/tools.html"):
        fp = "public" + p_
        try: h = open(fp).read()
        except FileNotFoundError: continue
        if ' v70"' in h or "</h1>" not in h: continue
        i = h.index("</h1>") + 5
        m = re.compile(r'<p class="tag">.*?</p>', re.S).match(h, i)
        if m: i = m.end()
        h = h[:i] + note + h[i:]
        open(fp, "w").write(h); changed.append(p_)
    fp = "public/guides.html"; h = open(fp).read()
    if ' v70"' not in h and "<h2>New guides</h2><ul>" in h:
        open(fp, "w").write(h.replace("<h2>New guides</h2><ul>", f"<h2>New guides</h2><ul><li class=\"v70\"><a href='{PATH}'>Monthly vs yearly: how much annual billing saves on all {S['total']} AI tools, with the break-even month</a></li>", 1)); changed.append("/guides.html")
    return changed


CSS = ("<style>.k70c{margin:var(--s4) 0;border-left:4px solid var(--ac)}.cf70{display:grid;gap:8px 12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));align-items:end;margin:8px 0}"
       ".l70{display:flex;flex-direction:column;gap:4px;font-size:.85rem;font-weight:600}.l70 select,.l70 input{min-height:44px;border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);padding:0 10px;font:inherit;font-weight:400;font-size:.95rem;width:100%;box-sizing:border-box}"
       "#o70{margin-top:8px}#o70 .ans{font-size:1.05rem;margin:4px 0}#o70 table{border-collapse:collapse;width:100%;max-width:560px;margin:8px 0;font-size:.95rem}#o70 th,#o70 td{border-bottom:1px solid var(--bd);padding:6px 8px;text-align:left}#o70 td.r{text-align:right;font-variant-numeric:tabular-nums}#o70 tr.w td{font-weight:700;color:var(--ok)}"
       ".bdg70{display:inline-block;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:700;letter-spacing:.03em;margin-right:6px;background:var(--sf2);color:var(--tx);border:1px solid var(--bd)}.bdg70.y{background:var(--ok);color:var(--okt);border-color:var(--ok)}"
       ".sm70{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));margin:var(--s4) 0}.sb70{display:flex;flex-direction:column;justify-content:center;min-height:72px;padding:8px 12px;border-radius:var(--r);border:1px solid var(--bd);background:var(--sf);color:var(--tx);text-decoration:none}"
       ".sb70 b{font-size:1.4rem;line-height:1.15}.sb70 span{font-size:.85rem;color:var(--mu)}.sb70.y{border-left:4px solid var(--ok)}.sb70.n{border-left:4px solid var(--warn)}.sb70.p{border-left:4px solid var(--bd)}.sb70.k{border-left:4px solid var(--ac)}a.sb70:hover b{text-decoration:underline}"
       ".q70 dl{display:grid;grid-template-columns:max-content 1fr;gap:8px 14px;margin:8px 0 0;font-size:.93rem}.q70 dt{font-weight:600}.q70 dd{margin:0}.q70 dd a,.q70 p a{display:inline;padding:0}"
       ".pr70{margin:4px 0 8px}.p70{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font-size:.92rem;text-decoration:none;margin:0 6px 8px 0}"
       ".fl70{position:sticky;top:0;z-index:2;background:var(--bg);display:grid;gap:8px 12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));padding:10px 0;border-bottom:1px solid var(--bd);align-items:end}"
       ".bt70{margin:0;display:flex;gap:8px}.bt70 button,.e70 button{min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--bd);background:var(--sf);color:var(--tx);font:inherit;cursor:pointer}"
       ".l70 select:focus-visible,.l70 input:focus-visible,.bt70 button:focus-visible,.p70:focus-visible,.sb70:focus-visible{outline:3px solid var(--ac);outline-offset:2px}"
       "#st70{margin:8px 0;min-height:1.4em}.l70g{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));margin:var(--s3) 0}"
       ".c70{scroll-margin-top:12px;display:flex;flex-direction:column}.c70[hidden]{display:none}.c70 h3{margin:0 0 6px;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}.c70 h3 a{min-height:32px;display:inline-flex;align-items:center}.c70 h3 .small{color:var(--mu);font-weight:400}"
       ".g70{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:0 0 6px}.g70.one{grid-template-columns:1fr 1fr}.g70>div{background:var(--sf2);border-radius:10px;padding:6px 8px;min-width:0}.g70>div.k70{background:var(--acs)}"
       ".g70 dt{font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mu)}.g70 dd{margin:0;font-weight:700;font-size:1.02rem;font-variant-numeric:tabular-nums}.g70 dd small{font-weight:400;color:var(--mu);font-size:.8rem}.g70 dd.u70{font-weight:400;font-size:.8rem;color:var(--mu)}.g70 dd.na70{font-weight:500;font-size:.88rem;color:var(--mu)}"
       ".v70{margin:4px 0;font-size:.93rem}.v70.y b{color:var(--ok)}.v70.n b{color:var(--warn)}.v70.u b{color:var(--mu)}.r70{margin:2px 0!important}"
       ".c70 details{margin:2px 0}.c70 summary{cursor:pointer;min-height:44px;display:flex;align-items:center;gap:6px;font-size:.9rem;font-weight:600;color:var(--ac);list-style:none}.c70 summary::-webkit-details-marker{display:none}.c70 summary::before{content:'▸';font-size:.8rem}.c70 details[open] summary::before{content:'▾'}.c70 blockquote{margin:0 0 6px;padding:6px 10px;border-left:3px solid var(--bd);font-size:.88rem;color:var(--mu)}"
       ".s70{font-size:.85rem!important;color:var(--mu);margin:4px 0}.a70{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:auto!important;padding-top:8px;border-top:1px solid var(--bd);font-size:.92rem}.a70 a{min-height:44px;display:inline-flex;align-items:center}"
       ".e70{padding:var(--s4);border:1px dashed var(--bd);border-radius:var(--r)}"
       "@media(max-width:640px){.fl70{position:static;grid-template-columns:1fr 1fr}.l70.q{grid-column:1/-1}.q70 dl{grid-template-columns:1fr;gap:2px}.q70 dd{margin-bottom:8px}}</style>")

JS = r"""(()=>{const $=i=>document.getElementById(i),X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])),
M=v=>{const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r.toLocaleString('en-US'):r.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}))};
const BY={};D70.forEach(t=>BY[t.s]=t);const T=$('x70t'),MO=$('x70m'),O=$('o70');
function calc(push){const s=T.value,t=BY[s];let mo=parseInt(MO.value,10);if(!(mo>=1))mo=12;if(mo>36)mo=36;
if(push){const u=new URL(location.href);if(s)u.searchParams.set('tool',s);else u.searchParams.delete('tool');if(s&&mo!=12)u.searchParams.set('months',mo);else u.searchParams.delete('months');history.replaceState(null,'',u.pathname+u.search+u.hash)}
if(!t){O.innerHTML='<p class="small">Pick a tool to see what monthly and yearly would cost you, and from which month yearly pays off.</p>';return}
const card='<a href="#t-'+t.s+'">See the '+X(t.n)+' card with the exact words and source</a>';
if(t.c=='save'||t.c=='same'){const yrs=Math.ceil(mo/12),cm=t.m*mo,cy=t.yt*yrs,d=Math.round((cm-cy)*100)/100;
const win=d>0?'yearly':(d<0?'monthly':'same');
let h='<p class="ans">'+(win=='yearly'?'<span class="bdg70 y">PAY YEARLY</span>':(win=='monthly'?'<span class="bdg70">STAY MONTHLY</span>':'<span class="bdg70">SAME COST</span>'))+'<b>'+X(t.n)+' '+X(t.pl)+' for '+mo+' month'+(mo==1?'':'s')+': ';
h+=win=='yearly'?'yearly saves you '+M(d)+'.':(win=='monthly'?'monthly saves you '+M(-d)+'.':'both cost the same.')+'</b></p>';
h+='<table><caption class="skip">Cost of '+X(t.n)+' over '+mo+' months</caption><tbody><tr class="'+(win=='monthly'?'w':'')+'"><th scope="row">Pay monthly</th><td class="r">'+M(t.m)+' × '+mo+' = '+M(cm)+'</td></tr><tr class="'+(win=='yearly'?'w':'')+'"><th scope="row">Pay yearly</th><td class="r">'+(yrs>1?yrs+' × ':'')+M(t.yt)+' upfront = '+M(cy)+'</td></tr></tbody></table>';
h+=t.c=='save'?'<p class="small">Yearly saves '+t.p+'% ('+M(t.sv)+') over a full year and pays off from <b>month '+t.be+'</b>'+(mo<t.be?': you said '+mo+', so monthly is cheaper unless you keep it longer.':'.')+(yrs>1&&mo%12?' Past a year, yearly means paying for another full year upfront.':'')+'</p>':'<p class="small">This plan costs the same or more per month when billed yearly.</p>';
if(t.rf)h+='<p class="small"><b>If you change your mind:</b> '+X(t.rf)+'. A yearly plan is paid upfront, so check the refund rule first.</p>';
O.innerHTML=h+'<p class="small">'+card+'</p>';return}
const msg={mo:X(t.n)+' '+X(t.pl)+' is <b>monthly only</b> ('+M(t.m)+'/mo), so there’s no yearly saving. '+mo+' months cost '+M(t.m*mo)+'.',
yr:X(t.n)+' shows <b>only a yearly price</b> ('+M(t.y)+'/mo billed yearly), so we can’t compare it with monthly.',
none:X(t.n)+' has <b>no fixed plan price</b> (usage-based or custom).',nc:'We couldn’t read '+X(t.n)+'’s monthly and yearly prices tonight.'}[t.c];
O.innerHTML='<p class="ans">'+msg+'</p><p class="small">'+card+'</p>'}
T.addEventListener('change',()=>calc(true));MO.addEventListener('input',()=>calc(true));$('cf70').addEventListener('submit',ev=>{ev.preventDefault();calc(true)});
const F={show:$('x70s'),cat:$('x70c'),sort:$('x70o'),q:$('x70q')},C=[...document.querySelectorAll('.c70')],L=$('l70'),st=$('st70'),E=$('e70');let LS='pct';
const SL={pct:'biggest % saving first',usd:'biggest $ saving first',be:'fastest break-even first',cheap:'cheapest first',az:'A to Z'};
function go(push){const v={};for(const k in F)v[k]=(F[k].value||'').trim();const q=v.q.toLowerCase();let n=0;
C.forEach(c=>{const ok=(!v.show||c.dataset.st==v.show||(v.show=='none'&&c.dataset.st=='nc'))&&(!v.cat||c.dataset.c==v.cat)&&(!q||c.dataset.k.includes(q));c.hidden=!ok;if(ok)n++});
if(v.sort!=LS){LS=v.sort;const N=(c,k)=>parseFloat(c.dataset[k]),s=[...C],nm=(a,b)=>a.dataset.n.localeCompare(b.dataset.n),
O2={save:0,same:1,mo:2,yr:3,none:4,nc:5};
if(v.sort=='usd')s.sort((a,b)=>N(b,'usd')-N(a,'usd')||O2[a.dataset.st]-O2[b.dataset.st]||nm(a,b));else if(v.sort=='be')s.sort((a,b)=>N(a,'be')-N(b,'be')||N(b,'pct')-N(a,'pct')||nm(a,b));
else if(v.sort=='cheap')s.sort((a,b)=>N(a,'cheap')-N(b,'cheap')||nm(a,b));else if(v.sort=='az')s.sort(nm);else s.sort((a,b)=>O2[a.dataset.st]-O2[b.dataset.st]||N(b,'pct')-N(a,'pct')||N(b,'usd')-N(a,'usd')||nm(a,b));s.forEach(c=>L.appendChild(c))}
E.hidden=n>0;const on=[];if(v.show)on.push(F.show.options[F.show.selectedIndex].text.replace(/ \(\d+\)$/,''));if(v.cat)on.push(F.cat.options[F.cat.selectedIndex].text);if(q)on.push('“'+v.q+'”');
st.textContent=(on.length?n+' of '+C.length+' tools '+(n==1?'matches':'match')+': '+on.join(' + '):'Showing all '+C.length+' tools')+', '+SL[v.sort||'pct']+'.';
if(push){const u=new URL(location.href);for(const k in F){if(v[k]&&!(k=='sort'&&v[k]=='pct'))u.searchParams.set(k,v[k]);else u.searchParams.delete(k)}history.replaceState(null,'',u.pathname+u.search+u.hash)}}
for(const k in F)F[k].addEventListener(k=='q'?'input':'change',()=>go(true));$('f70').addEventListener('submit',ev=>{ev.preventDefault();go(true)});
const clr=()=>{for(const k in F)F[k].value=k=='sort'?'pct':'';go(true)};$('x70x').addEventListener('click',clr);$('x70y').addEventListener('click',clr);
const P=new URLSearchParams(location.search);for(const k in F){const x=P.get(k);if(x!==null){if(F[k].tagName=='SELECT'){if([...F[k].options].some(o=>o.value==x))F[k].value=x}else F[k].value=x}}
const pt=P.get('tool');if(pt&&BY[pt])T.value=pt;const pm=parseInt(P.get('months'),10);if(pm>=1&&pm<=36)MO.value=pm;
go(false);calc(false)})();"""
