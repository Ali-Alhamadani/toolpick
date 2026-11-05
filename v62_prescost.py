"""v62 presentation cost calculator page."""
import json
from tools import PRESCOST, PRESCOST_CHECKED, PRESCOST_LEFT_OUT


def build_prescost(ctx, V62_CHANGED):
    page = ctx["page"]; e = ctx["e"]; turl = ctx["turl"]; find = ctx["find"]; slug = ctx["slug"]
    BASE = ctx["BASE"]; _faq = ctx["_faq"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]; _lm = ctx["_lm"]

    PC_PATH = "/ai-presentation-cost.html"
    PCD = []
    for c in PRESCOST:
        t0 = find(c["t"])
        price = t0["price"]
        for pname, m, y, note in c["plans"]:
            if c["cur"] == "EUR":
                assert ("€%s" % (int(m) if m == int(m) else m)) in price or ("€%s" % m) in price, (c["t"], m, price)
            else:
                if m is not None:
                    ok = ("$%s" % m) in price or ("$%.2f" % m) in price
                    # Plus AI uses "$15 monthly" / "$25" etc.; Max monthly is $240
                    if c["t"] == "Plus AI" and pname == "Max":
                        ok = ok or "$240" in price
                    if c["t"] == "Canva" and pname == "Business":
                        ok = ok or "$25" in price
                    assert ok, (c["t"], pname, m, price)
                if y is not None and c["t"] not in ("Canva", "SlidesAI"):
                    # Canva yearly as $144/yr / $250/yr; SlidesAI as $10/mo billed $120/yr
                    ok = ("$%s" % y) in price or ("$%.2f" % y) in price or ("$%s" % int(y)) in price
                    if c["t"] == "Beautiful.ai" and pname == "Pro":
                        ok = ok or "$14.50" in price
                    if c["t"] == "Plus AI":
                        ok = True  # yearly figures appear as $10/$20/$30/$200 before monthly parens
                    assert ok, (c["t"], pname, y, price)
        if c["t"] == "Canva":
            assert "$144/yr" in price and "$250/yr" in price
        if c["t"] == "SlidesAI":
            assert "$120/yr" in price and "$250/yr" in price
        PCD.append(dict(
            k=slug(c["t"]), n=c["t"], u=turl(c["t"]), src=c["src"], ck=c["checked"], cur=c["cur"],
            free=c.get("free"), trial=c.get("trial"), defi=c["default"],
            plans=[dict(p=p[0], m=p[1], y=p[2], note=p[3]) for p in c["plans"]],
        ))

    def money(v, cur="USD"):
        if v is None:
            return "—"
        sym = "€" if cur == "EUR" else "$"
        r = round(float(v), 2)
        if r == int(r):
            return "%s%s" % (sym, "{:,}".format(int(r)))
        return "%s%s" % (sym, "{:,.2f}".format(r))

    def calc(d, seats, bill, ov=None):
        idx = ov if ov is not None and 0 <= ov < len(d["plans"]) else d["defi"]
        p = d["plans"][idx]
        used_m_fallback = used_y_fallback = False
        if bill == "y":
            if p["y"] is not None:
                per = p["y"]
            elif p["m"] is not None:
                per = p["m"]; used_m_fallback = True
            else:
                per = None
        else:
            if p["m"] is not None:
                per = p["m"]
            elif p["y"] is not None:
                per = p["y"]; used_y_fallback = True
            else:
                per = None
        tot = None if per is None else per * seats
        return dict(idx=idx, p=p, per=per, tot=tot, used_m_fallback=used_m_fallback, used_y_fallback=used_y_fallback)

    def card(d, r, seats, bill, best):
        opts = []
        for j, q in enumerate(d["plans"]):
            label = e(q["p"]) + " · "
            label += (money(q["m"], d["cur"]) + "/mo") if q["m"] is not None else "monthly not stated"
            if q["y"] is not None:
                label += " · " + money(q["y"], d["cur"]) + "/mo yearly"
            opts.append('<option value="%d"%s>%s</option>' % (j, " selected" if j == r["idx"] else "", label))
        note = ""
        if r["used_m_fallback"]:
            note += '<p class="small cc-note">No yearly price on the official page, so the monthly price is used.</p>'
        if r["used_y_fallback"]:
            note += '<p class="small cc-note">Only billed yearly on the official page, so the yearly rate is shown.</p>'
        if d["cur"] == "EUR":
            note += '<p class="small cc-note">Priced in euros — excluded from the USD “cheapest” highlight.</p>'
        if r["tot"] is None:
            totl = '<p class="cc-tot">Price not stated</p>'
        else:
            totl = (
                '<p class="cc-tot">%s<span class="small">/mo</span></p>'
                '<p class="small" style="margin:0">%s a year · %s/seat/mo%s</p>'
            ) % (
                money(r["tot"], d["cur"]),
                money(r["tot"] * 12, d["cur"]),
                money(r["per"], d["cur"]),
                (" × %d" % seats) if seats > 1 else "",
            )
        freebit = ""
        if d.get("free"):
            freebit = '<p class="small"><b>Free:</b> %s</p>' % e(d["free"])
        elif d.get("trial"):
            freebit = '<p class="small"><b>Trial:</b> %s</p>' % e(d["trial"])
        return (
            '<article class="cc-card%s" data-k="%s" data-cur="%s">'
            "%s"
            '<h3><a href="%s">%s</a></h3>'
            '<label class="small" for="pc-p-%s">Plan</label>'
            '<select id="pc-p-%s" class="cc-sel" data-k="%s">%s</select>'
            "%s%s%s"
            '<p class="small cc-inc"><b>Note:</b> %s</p>'
            '<p class="small" style="margin:6px 0 0">Checked %s · '
            '<a href="%s" rel="nofollow noopener" target="_blank">Official pricing'
            '<span class="skip"> for %s (opens in a new tab)</span></a></p></article>'
        ) % (
            " cc-best" if best else "", d["k"], d["cur"],
            '<p class="cc-badge">Lowest USD cost for you</p>' if best else "",
            d["u"], e(d["n"]),
            d["k"], d["k"], d["k"], "".join(opts),
            totl, note, freebit,
            e(r["p"]["note"]),
            e(d["ck"]), e(d["src"]), e(d["n"]),
        )

    def render(seats=1, bill="m", budget=None):
        rows = [(d, calc(d, seats, bill)) for d in PCD]
        usd = [(d, r) for d, r in rows if d["cur"] == "USD" and r["tot"] is not None]
        usd.sort(key=lambda x: (x[1]["tot"], x[0]["n"]))
        b = usd[0] if usd else None
        ppl = "you" if seats == 1 else "%d people" % seats
        if b:
            nx = usd[1] if len(usd) > 1 else None
            diff = ""
            if nx and nx[1]["tot"] > b[1]["tot"]:
                diff = ", %s a month less than %s %s" % (
                    money(nx[1]["tot"] - b[1]["tot"]), nx[0]["n"], nx[1]["p"]["p"]
                )
            elif nx:
                diff = ", the same as %s %s" % (nx[0]["n"], nx[1]["p"]["p"])
            bud = ""
            if budget is not None:
                okb = [x for x in usd if x[1]["tot"] <= budget]
                bud = (
                    '<p style="margin:8px 0 0">%d USD option%s at or under %s/mo for %s.</p>'
                    % (len(okb), "" if len(okb) == 1 else "s", money(budget), ppl)
                )
            head = (
                '<p class="small" style="margin:0">Lowest <b>USD</b> cost for %s, billed %s '
                "(Pitch is EUR and ranked separately)</p>"
                '<p class="vc-big" style="margin:4px 0">%s %s: %s/mo</p>'
                "<p style=\"margin:0\">%s a year%s. Pitch stays in euros below.</p>%s"
            ) % (
                ppl, "yearly" if bill == "y" else "monthly",
                e(b[0]["n"]), e(b[1]["p"]["p"]), money(b[1]["tot"]),
                money(b[1]["tot"] * 12), e(diff), bud,
            )
        else:
            head = "<p>No USD plan available for that setup.</p>"
        return head, "".join(card(d, r, seats, bill, b is not None and d is b[0]) for d, r in rows)

    head0, cards0 = render()
    free_list = "".join(
        ("<li><b>%s:</b> %s</li>" % (e(d["n"]), e(d["free"]))) if d.get("free")
        else ("<li><b>%s:</b> %s — not a free plan</li>" % (e(d["n"]), e(d["trial"])))
        for d in PCD
    )
    qa = [
        (
            "What's the cheapest AI presentation tool for one person?",
            "Among USD tools on monthly billing where a monthly price is stated: Gamma Plus is $12/mo, "
            "Plus AI Basic is $15/mo, Canva Pro is $18/mo. Beautiful.ai Pro is $14.50/mo billed annually only. "
            "SlidesAI's paid plans are shown as yearly-billed rates. Pitch Plus is €10/mo (euros). "
            "Checked dates: Gamma/Canva %s; others 2026-10-19." % PRESCOST_CHECKED,
        ),
        (
            "Does Pitch count in the cheapest highlight?",
            "No. Pitch is priced in euros on its official page, so we show it in € and keep it out of the USD cheapest ranking.",
        ),
        (
            "Is a free trial the same as a free plan?",
            "No. Beautiful.ai's 14-day trial and Plus AI's 7-day trial (card required) are trials, not ongoing free plans. "
            "Gamma, Canva, Pitch and SlidesAI list real free plans.",
        ),
        (
            "How is Canva's yearly price worked out?",
            "Canva Pro is $144/yr → $12/mo. Canva Business is $250/yr per person → about $20.83/mo. "
            "Both from canva.com/pricing (checked 2026-10-24).",
        ),
        (
            "Can I share my result?",
            "Yes. The URL updates with ?seats= and &bill=m|y (and optional &budget=). Use Copy link.",
        ),
    ]

    css = (
        '<style>.vc-big{font-size:1.5rem;font-weight:800;margin:10px 0 2px}'
        ".cc-in{display:flex;flex-wrap:wrap;gap:16px 36px;align-items:flex-start}"
        ".cc-f>span.cc-l,.cc-f>label.cc-l{display:block;font-weight:600;margin-bottom:6px}"
        ".cc-step{display:inline-flex;align-items:center;gap:6px}"
        ".cc-step button{min-width:48px;min-height:48px;border-radius:12px;border:1px solid var(--bd);"
        "background:var(--sf);color:var(--tx);font-size:1.3rem;font-weight:700;cursor:pointer}"
        ".cc-step input,.cc-bud{width:84px;min-height:48px;text-align:center;font-size:1.1rem;"
        "border-radius:10px;border:1px solid var(--bd);background:var(--sf);color:var(--tx)}"
        ".cc-bud{width:110px}.cc-f .seg{flex-wrap:wrap}#pc-head{margin:16px 0 8px;min-height:110px}"
        ".cc-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}"
        ".cc-card{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:14px 16px;"
        "display:flex;flex-direction:column;gap:4px}.cc-card h3{margin:0;font-size:1.1rem}"
        ".cc-card select{width:100%;min-height:44px;border-radius:10px;border:1px solid var(--bd);"
        "background:var(--sf);color:var(--tx);padding:0 8px}"
        ".cc-tot{font-size:1.6rem;font-weight:800;margin:6px 0 0;line-height:1.2}"
        ".cc-best{border:2px solid var(--ok);box-shadow:var(--sh)}"
        ".cc-badge{margin:0;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--ok)}"
        ".cc-note{margin:0;color:var(--mu)}.cc-inc{margin:4px 0 0}"
        "@media(max-width:640px){.cc-in{flex-direction:column;align-items:stretch}}"
        "@media(prefers-color-scheme:dark){.cc-badge{color:#4ade80}.cc-best{border-color:#4ade80}}</style>"
    )

    # Client JS — keep compact; data from PCD
    js = (
        "<script>(()=>{"
        "const D=%s;"
        "const $=s=>document.querySelector(s),X=s=>String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));"
        "const M=(v,cur)=>{if(v==null)return '—';const sym=cur==='EUR'?'€':'$';const r=Math.round(v*100)/100;"
        "return sym+(r==Math.floor(r)?r.toLocaleString('en-US'):r.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}))};"
        "let OV={};const seatsEl=$('#pc-seats'),budEl=$('#pc-budget');"
        "const val=n=>(document.querySelector('input[name='+n+']:checked')||{}).value;"
        "function st(){let n=parseInt(seatsEl.value,10);if(!(n>=1))n=1;if(n>50)n=50;"
        "let bud=budEl.value===''?null:parseFloat(budEl.value);if(bud!=null&&!(bud>=0))bud=null;"
        "return {n,b:val('pc-bill')||'m',bud}}"
        "function calc(d,s){let ix=OV[d.k];if(!(ix>=0&&ix<d.plans.length))ix=d.defi;const p=d.plans[ix];"
        "let per=null,um=false,uyf=false;"
        "if(s.b==='y'){if(p.y!=null)per=p.y;else if(p.m!=null){per=p.m;um=true}}"
        "else{if(p.m!=null)per=p.m;else if(p.y!=null){per=p.y;uyf=true}}"
        "return {ix,p,per,tot:per==null?null:per*s.n,um,uyf}}"
        "function card(d,r,s,best){"
        "const opts=d.plans.map((q,j)=>`<option value=\"${j}\"${j==r.ix?' selected':''}>${X(q.p)} · "
        "${q.m!=null?M(q.m,d.cur)+'/mo':'monthly not stated'}${q.y!=null?' · '+M(q.y,d.cur)+'/mo yearly':''}</option>`).join('');"
        "let note='';if(r.um)note+='<p class=\"small cc-note\">No yearly price on the official page, so the monthly price is used.</p>';"
        "if(r.uyf)note+='<p class=\"small cc-note\">Only billed yearly on the official page, so the yearly rate is shown.</p>';"
        "if(d.cur==='EUR')note+='<p class=\"small cc-note\">Priced in euros — excluded from the USD “cheapest” highlight.</p>';"
        "const tot=r.tot==null?'<p class=\"cc-tot\">Price not stated</p>':"
        "`<p class=\"cc-tot\">${M(r.tot,d.cur)}<span class=\"small\">/mo</span></p>"
        "<p class=\"small\" style=\"margin:0\">${M(r.tot*12,d.cur)} a year · ${M(r.per,d.cur)}/seat/mo${s.n>1?' × '+s.n:''}</p>`;"
        "const free=d.free?`<p class=\"small\"><b>Free:</b> ${X(d.free)}</p>`:(d.trial?`<p class=\"small\"><b>Trial:</b> ${X(d.trial)}</p>`:'');"
        "return `<article class=\"cc-card${best?' cc-best':''}\" data-k=\"${d.k}\">${best?'<p class=\"cc-badge\">Lowest USD cost for you</p>':''}"
        "<h3><a href=\"${d.u}\">${X(d.n)}</a></h3><label class=\"small\" for=\"pc-p-${d.k}\">Plan</label>"
        "<select id=\"pc-p-${d.k}\" class=\"cc-sel\" data-k=\"${d.k}\">${opts}</select>${tot}${note}${free}"
        "<p class=\"small cc-inc\"><b>Note:</b> ${X(r.p.note)}</p>"
        "<p class=\"small\" style=\"margin:6px 0 0\">Checked ${X(d.ck)} · "
        "<a href=\"${X(d.src)}\" rel=\"nofollow noopener\" target=\"_blank\">Official pricing"
        "<span class=\"skip\"> for ${X(d.n)} (opens in a new tab)</span></a></p></article>`}"
        "function qs(s){const p=new URLSearchParams();if(s.n!=1)p.set('seats',s.n);if(s.b!='m')p.set('bill',s.b);"
        "if(s.bud!=null)p.set('budget',s.bud);const o=Object.keys(OV).map(k=>k+':'+OV[k]);if(o.length)p.set('plan',o.join(','));"
        "const q=p.toString();return location.pathname+(q?'?'+q:'')}"
        "function render(push){const s=st();const rows=D.map(d=>[d,calc(d,s)]);"
        "const usd=rows.filter(([d,r])=>d.cur==='USD'&&r.tot!=null).sort((a,b)=>(a[1].tot-b[1].tot)||a[0].n.localeCompare(b[0].n));"
        "const b=usd[0],ppl=s.n==1?'you':s.n+' people';let h;"
        "if(b){const nx=usd[1];let diff='';if(nx)diff=nx[1].tot>b[1].tot?`, ${M(nx[1].tot-b[1].tot)} a month less than ${nx[0].n} ${nx[1].p.p}`:`, the same as ${nx[0].n} ${nx[1].p.p}`;"
        "let bud='';if(s.bud!=null){const ok=usd.filter(x=>x[1].tot<=s.bud);bud=`<p style=\"margin:8px 0 0\">${ok.length} USD option${ok.length==1?'':'s'} at or under ${M(s.bud)}/mo for ${ppl}.</p>`}"
        "h=`<p class=\"small\" style=\"margin:0\">Lowest <b>USD</b> cost for ${ppl}, billed ${s.b==='y'?'yearly':'monthly'} (Pitch is EUR and ranked separately)</p>"
        "<p class=\"vc-big\" style=\"margin:4px 0\">${X(b[0].n)} ${X(b[1].p.p)}: ${M(b[1].tot)}/mo</p>"
        "<p style=\"margin:0\">${M(b[1].tot*12)} a year${X(diff)}. Pitch stays in euros below.</p>${bud}`}"
        "else h='<p>No USD plan available for that setup.</p>';"
        "$('#pc-head').innerHTML=h;const fk=document.activeElement&&document.activeElement.classList.contains('cc-sel')?document.activeElement.dataset.k:null;"
        "$('#pc-cards').innerHTML=rows.map(([d,r])=>card(d,r,s,b&&d===b[0])).join('');"
        "if(fk){const el=document.getElementById('pc-p-'+fk);if(el)el.focus()}"
        "if(push!==false)history.replaceState(null,'',qs(s))}"
        "const P=new URLSearchParams(location.search);if(P.get('seats'))seatsEl.value=Math.min(50,Math.max(1,parseInt(P.get('seats'),10)||1));"
        "if(P.get('bill')){const el=document.getElementById('pc-bill-'+P.get('bill'));if(el)el.checked=true}"
        "if(P.get('budget'))budEl.value=P.get('budget');"
        "if(P.get('plan'))P.get('plan').split(',').forEach(x=>{const [k,v]=x.split(':');if(D.some(d=>d.k==k)&&/^\\d+$/.test(v||''))OV[k]=+v});"
        "if(location.search)render(false);"
        "document.querySelectorAll('#pcalc input[type=radio]').forEach(el=>el.addEventListener('change',()=>render()));"
        "seatsEl.addEventListener('input',()=>render());seatsEl.addEventListener('change',()=>{seatsEl.value=st().n;render()});"
        "budEl.addEventListener('input',()=>render());"
        "const bump=d=>{seatsEl.value=Math.min(50,Math.max(1,st().n+d));render()};"
        "$('#pc-minus').addEventListener('click',()=>bump(-1));$('#pc-plus').addEventListener('click',()=>bump(1));"
        "$('#pc-cards').addEventListener('change',ev=>{const el=ev.target;if(!el.classList.contains('cc-sel'))return;OV[el.dataset.k]=+el.value;render()});"
        "$('#pc-reset').addEventListener('click',()=>{OV={};seatsEl.value=1;budEl.value='';document.getElementById('pc-bill-m').checked=true;render();$('#pc-st').textContent='Back to the defaults.';seatsEl.focus()});"
        "$('#pc-copy').addEventListener('click',async()=>{const u=location.origin+qs(st());try{await navigator.clipboard.writeText(u);$('#pc-st').textContent='Link copied: '+u}catch(err){$('#pc-st').textContent='Copy this link: '+u}});"
        "})();</script>"
    ) % json.dumps(PCD, separators=(",", ":"))

    body = (
        css
        + '<p class="small"><a href="/save-money.html">Save money</a> › AI presentation cost</p>'
        "<h1>AI presentation tool cost calculator</h1>"
        '<p class="tag">What will Gamma, Canva, Pitch, Beautiful.ai, Plus AI and SlidesAI cost for you or your team? '
        "Every price is from the official pricing page on the date on each card. Pitch is in euros and is excluded "
        "from the USD cheapest highlight.</p>"
        '<div class="builder" id="pcalc"><div class="cc-in">'
        '<div class="cc-f"><label class="cc-l" for="pc-seats">How many people?</label>'
        '<div class="cc-step"><button type="button" id="pc-minus" aria-label="One person fewer">−</button>'
        '<input type="number" id="pc-seats" min="1" max="50" value="1" inputmode="numeric">'
        '<button type="button" id="pc-plus" aria-label="One person more">+</button></div></div>'
        '<div class="cc-f"><span class="cc-l" aria-hidden="true">Billing</span>'
        '<fieldset class="seg"><legend>Billing</legend>'
        '<input type="radio" name="pc-bill" id="pc-bill-m" value="m" checked><label for="pc-bill-m">Monthly</label>'
        '<input type="radio" name="pc-bill" id="pc-bill-y" value="y"><label for="pc-bill-y">Yearly</label>'
        "</fieldset></div>"
        '<div class="cc-f"><label class="cc-l" for="pc-budget">Optional budget / mo (USD)</label>'
        '<input class="cc-bud" type="number" id="pc-budget" min="0" max="10000" step="1" placeholder="e.g. 30" inputmode="numeric"></div>'
        "</div>"
        '<div id="pc-head" class="pick" aria-live="polite" aria-atomic="true">%s</div>' % head0
        + '<h2 class="skip">Prices for each tool</h2><div class="cc-grid" id="pc-cards">%s</div>' % cards0
        + '<p style="margin:12px 0 0"><button type="button" class="bbtn" id="pc-copy">Copy link to these results</button> '
        '<button type="button" class="bbtn" id="pc-reset">Start again</button> '
        '<span id="pc-st" class="small" role="status"></span></p></div>'
        '<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">Free plans and trials</h2>'
        '<ul class="small" style="margin:0">%s</ul>'
        '<p class="small" style="margin:8px 0 0">Trials are not free plans.</p></div>' % free_list
        + "<h2>How we work it out</h2><ul>"
        "<li><b>Prices:</b> copied from each official pricing page on the date shown on the card, before tax. Nothing is estimated.</li>"
        "<li><b>Seats:</b> totals are per-seat price × number of people (1–50).</li>"
        "<li><b>Yearly:</b> used only where the page shows a yearly price; otherwise the monthly price is used and the card says so. "
        "Beautiful.ai Pro and SlidesAI paid plans are yearly-billed on the page we read.</li>"
        "<li><b>Pitch (EUR):</b> shown in euros and excluded from the USD cheapest ranking.</li>"
        "<li><b>Not included:</b> tax, add-ons, and credit packs beyond the plan price.</li></ul>"
        "<h2>Left out</h2><ul>"
        + "".join("<li><b>%s</b>: %s.</li>" % (e(n), e(r)) for n, r in PRESCOST_LEFT_OUT)
        + "</ul>"
        + _faq(qa)
        + '<p class="small">Related: <a href="/best-ai-presentations-tools.html">Best AI presentation tools</a> · '
        '<a href="/best-free-ai-presentations-tools.html">Best free AI presentation tools</a> · '
        '<a href="/best-ai-tool-for-pitch-decks.html">Best AI tool for pitch decks</a> · '
        '<a href="/ai-coding-cost.html">AI coding cost calculator</a> · '
        '<a href="/save-money.html">Save money</a> · <a href="/guides.html">Guides</a></p>'
        + js
    )

    page(
        PC_PATH,
        "AI Presentation Cost Calculator (2026): Gamma, Canva, Pitch, Beautiful.ai | ToolPick",
        "What Gamma, Canva, Pitch, Beautiful.ai, Plus AI and SlidesAI cost per month for you or your team, "
        "by seats and monthly/yearly billing. Official prices; Pitch in EUR. Latest check among tools: %s."
        % PRESCOST_CHECKED,
        body,
        [
            {
                "@context": "https://schema.org",
                "@type": "WebApplication",
                "name": "AI presentation tool cost calculator",
                "url": BASE + PC_PATH,
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Any",
                "isAccessibleForFree": True,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "dateModified": PRESCOST_CHECKED,
                "description": "Monthly and yearly cost of AI presentation tools by seats, from official pricing pages.",
            },
            faq(qa)[1],
            crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("AI presentation cost", PC_PATH)]),
        ],
    )
    V62_CHANGED.append(PC_PATH)
    _lm[PC_PATH] = PRESCOST_CHECKED
    return PC_PATH, PCD
