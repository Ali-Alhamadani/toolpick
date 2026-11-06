"""v63 AI writing cost calculator page."""
import json
from tools import WRITECOST, WRITECOST_CHECKED, WRITECOST_LEFT_OUT


def build_writecost(ctx, V63_CHANGED):
    page = ctx["page"]; e = ctx["e"]; turl = ctx["turl"]; find = ctx["find"]; slug = ctx["slug"]
    BASE = ctx["BASE"]; _faq = ctx["_faq"]; crumbs = ctx["crumbs"]; faq = ctx["faq"]; _lm = ctx["_lm"]

    PC_PATH = "/ai-writing-cost.html"
    PCD = []
    for c in WRITECOST:
        t0 = find(c["t"])
        price = t0["price"]
        for pname, m, y, note in c["plans"]:
            if m is not None:
                ok = ("$%s" % m) in price or ("$%.2f" % m) in price
                if c["t"] == "ChatGPT" and pname == "Pro":
                    ok = ok or "$100" in price
                assert ok, (c["t"], pname, m, price)
            if y is not None:
                ok = ("$%s" % y) in price or ("$%.2f" % y) in price
                if isinstance(y, float) and abs(y - int(y)) < 1e-9:
                    ok = ok or ("$%s" % int(y)) in price
                if c["t"] == "Google Gemini" and pname == "Google AI Pro":
                    ok = ok or "16.67" in price or "199.99" in price
                assert ok, (c["t"], pname, y, price)
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
            '<label class="small" for="wc-p-%s">Plan</label>'
            '<select id="wc-p-%s" class="cc-sel" data-k="%s">%s</select>'
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
                "</p>"
                '<p class="vc-big" style="margin:4px 0">%s %s: %s/mo</p>'
                "<p style=\"margin:0\">%s a year%s.</p>%s"
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
            "What's the cheapest AI writing tool for one person?",
            "Among tools on this page with a monthly price: Google AI Plus is $4.99/mo, Wordtune Advanced is $6.99/mo, "
            "ChatGPT Go is $8/mo (verified 2026-10-24), Rytr Lite is $9/mo, Claude Pro is $20/mo, Grammarly Pro is $30/mo, "
            "Jasper Pro is $69/seat/mo. Latest check among tools: %s." % WRITECOST_CHECKED,
        ),
        (
            "Why is ChatGPT's Go/Plus check date older?",
            "chatgpt.com/pricing loads US dollar amounts for Go and Plus from CMS keys (not in the static HTML). "
            "We keep the last verified consumer prices from 2026-10-24. Pro “from $100” is confirmed in today's page HTML.",
        ),
        (
            "Is a free trial the same as a free plan?",
            "No. Jasper's 7-day Pro trial and Wordtune's 3-day trial are trials, not ongoing free plans. "
            "Grammarly, Rytr, Claude, ChatGPT, Notion and Gemini list real free options.",
        ),
        (
            "How is Google AI Pro's yearly price worked out?",
            "Google lists Google AI Pro at $19.99/mo or $199.99/yr on one.google.com/about/google-ai-plans/ "
            "(checked 2026-11-06). $199.99 ÷ 12 ≈ $16.67/mo.",
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
        ".cc-bud{width:110px}.cc-f .seg{flex-wrap:wrap}#wc-head{margin:16px 0 8px;min-height:110px}"
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
        "let OV={};const seatsEl=$('#wc-seats'),budEl=$('#wc-budget');"
        "const val=n=>(document.querySelector('input[name='+n+']:checked')||{}).value;"
        "function st(){let n=parseInt(seatsEl.value,10);if(!(n>=1))n=1;if(n>50)n=50;"
        "let bud=budEl.value===''?null:parseFloat(budEl.value);if(bud!=null&&!(bud>=0))bud=null;"
        "return {n,b:val('wc-bill')||'m',bud}}"
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
        "<h3><a href=\"${d.u}\">${X(d.n)}</a></h3><label class=\"small\" for=\"wc-p-${d.k}\">Plan</label>"
        "<select id=\"wc-p-${d.k}\" class=\"cc-sel\" data-k=\"${d.k}\">${opts}</select>${tot}${note}${free}"
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
        "h=`<p class=\"small\" style=\"margin:0\">Lowest <b>USD</b> cost for ${ppl}, billed ${s.b==='y'?'yearly':'monthly'}</p>"
        "<p class=\"vc-big\" style=\"margin:4px 0\">${X(b[0].n)} ${X(b[1].p.p)}: ${M(b[1].tot)}/mo</p>"
        "<p style=\"margin:0\">${M(b[1].tot*12)} a year${X(diff)}.</p>${bud}`}"
        "else h='<p>No USD plan available for that setup.</p>';"
        "$('#wc-head').innerHTML=h;const fk=document.activeElement&&document.activeElement.classList.contains('cc-sel')?document.activeElement.dataset.k:null;"
        "$('#wc-cards').innerHTML=rows.map(([d,r])=>card(d,r,s,b&&d===b[0])).join('');"
        "if(fk){const el=document.getElementById('wc-p-'+fk);if(el)el.focus()}"
        "if(push!==false)history.replaceState(null,'',qs(s))}"
        "const P=new URLSearchParams(location.search);if(P.get('seats'))seatsEl.value=Math.min(50,Math.max(1,parseInt(P.get('seats'),10)||1));"
        "if(P.get('bill')){const el=document.getElementById('wc-bill-'+P.get('bill'));if(el)el.checked=true}"
        "if(P.get('budget'))budEl.value=P.get('budget');"
        "if(P.get('plan'))P.get('plan').split(',').forEach(x=>{const [k,v]=x.split(':');if(D.some(d=>d.k==k)&&/^\\d+$/.test(v||''))OV[k]=+v});"
        "if(location.search)render(false);"
        "document.querySelectorAll('#wcalc input[type=radio]').forEach(el=>el.addEventListener('change',()=>render()));"
        "seatsEl.addEventListener('input',()=>render());seatsEl.addEventListener('change',()=>{seatsEl.value=st().n;render()});"
        "budEl.addEventListener('input',()=>render());"
        "const bump=d=>{seatsEl.value=Math.min(50,Math.max(1,st().n+d));render()};"
        "$('#wc-minus').addEventListener('click',()=>bump(-1));$('#wc-plus').addEventListener('click',()=>bump(1));"
        "$('#wc-cards').addEventListener('change',ev=>{const el=ev.target;if(!el.classList.contains('cc-sel'))return;OV[el.dataset.k]=+el.value;render()});"
        "$('#wc-reset').addEventListener('click',()=>{OV={};seatsEl.value=1;budEl.value='';document.getElementById('wc-bill-m').checked=true;render();$('#wc-st').textContent='Back to the defaults.';seatsEl.focus()});"
        "$('#wc-copy').addEventListener('click',async()=>{const u=location.origin+qs(st());try{await navigator.clipboard.writeText(u);$('#wc-st').textContent='Link copied: '+u}catch(err){$('#wc-st').textContent='Copy this link: '+u}});"
        "})();</script>"
    ) % json.dumps(PCD, separators=(",", ":"))

    body = (
        css
        + '<p class="small"><a href="/save-money.html">Save money</a> › AI writing cost</p>'
        "<h1>AI writing tool cost calculator</h1>"
        '<p class="tag">What will Grammarly, Wordtune, Rytr, Jasper, Copy.ai, Writesonic, Claude, ChatGPT, Notion AI '
        "and Google Gemini cost for you or your team? Every price is from the official pricing page on the date on each card.</p>"
        '<div class="builder" id="wcalc"><div class="cc-in">'
        '<div class="cc-f"><label class="cc-l" for="wc-seats">How many people?</label>'
        '<div class="cc-step"><button type="button" id="wc-minus" aria-label="One person fewer">−</button>'
        '<input type="number" id="wc-seats" min="1" max="50" value="1" inputmode="numeric">'
        '<button type="button" id="wc-plus" aria-label="One person more">+</button></div></div>'
        '<div class="cc-f"><span class="cc-l" aria-hidden="true">Billing</span>'
        '<fieldset class="seg"><legend>Billing</legend>'
        '<input type="radio" name="wc-bill" id="wc-bill-m" value="m" checked><label for="wc-bill-m">Monthly</label>'
        '<input type="radio" name="wc-bill" id="wc-bill-y" value="y"><label for="wc-bill-y">Yearly</label>'
        "</fieldset></div>"
        '<div class="cc-f"><label class="cc-l" for="wc-budget">Optional budget / mo (USD)</label>'
        '<input class="cc-bud" type="number" id="wc-budget" min="0" max="10000" step="1" placeholder="e.g. 30" inputmode="numeric"></div>'
        "</div>"
        '<div id="wc-head" class="pick" aria-live="polite" aria-atomic="true">%s</div>' % head0
        + '<h2 class="skip">Prices for each tool</h2><div class="cc-grid" id="wc-cards">%s</div>' % cards0
        + '<p style="margin:12px 0 0"><button type="button" class="bbtn" id="wc-copy">Copy link to these results</button> '
        '<button type="button" class="bbtn" id="wc-reset">Start again</button> '
        '<span id="wc-st" class="small" role="status"></span></p></div>'
        '<div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">Free plans and trials</h2>'
        '<ul class="small" style="margin:0">%s</ul>'
        '<p class="small" style="margin:8px 0 0">Trials are not free plans.</p></div>' % free_list
        + "<h2>How we work it out</h2><ul>"
        "<li><b>Prices:</b> copied from each official pricing page on the date shown on the card, before tax. Nothing is estimated.</li>"
        "<li><b>Seats:</b> totals are per-seat price × number of people (1–50).</li>"
        "<li><b>Yearly:</b> used only where the page shows a yearly price; otherwise the monthly price is used and the card says so. "
        "Rytr yearly is 20% off monthly (page wording). Google AI Pro yearly is $199.99/yr.</li>"
        "<li><b>ChatGPT Go/Plus:</b> US dollar amounts from our 2026-10-24 verified check (CMS-keyed on the live page today).</li>"
        "<li><b>Not included:</b> tax, add-ons, workflow credits beyond the plan, and custom/enterprise quotes.</li></ul>"
        "<h2>Left out</h2><ul>"
        + "".join("<li><b>%s</b>: %s.</li>" % (e(n), e(r)) for n, r in WRITECOST_LEFT_OUT)
        + "</ul>"
        + _faq(qa)
        + '<p class="small">Related: <a href="/best-ai-writing-tools.html">Best AI writing tools</a> · '
        '<a href="/compare/jasper-vs-copy-ai.html">Jasper vs Copy.ai</a> · '
        '<a href="/compare/grammarly-vs-wordtune.html">Grammarly vs Wordtune</a> · '
        '<a href="/compare/rytr-vs-copy-ai.html">Rytr vs Copy.ai</a> · '
        '<a href="/ai-presentation-cost.html">AI presentation cost</a> · '
        '<a href="/ai-coding-cost.html">AI coding cost</a> · '
        '<a href="/save-money.html">Save money</a> · <a href="/guides.html">Guides</a></p>'
        + js
    )

    page(
        PC_PATH,
        "AI Writing Cost Calculator (2026): Grammarly, Jasper, Claude, ChatGPT & More | ToolPick",
        "What Grammarly, Wordtune, Rytr, Jasper, Copy.ai, Writesonic, Claude, ChatGPT, Notion AI and Google Gemini "
        "cost per month for you or your team, by seats and monthly/yearly billing. Official prices. Latest check among tools: %s."
        % WRITECOST_CHECKED,
        body,
        [
            {
                "@context": "https://schema.org",
                "@type": "WebApplication",
                "name": "AI writing tool cost calculator",
                "url": BASE + PC_PATH,
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Any",
                "isAccessibleForFree": True,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "dateModified": WRITECOST_CHECKED,
                "description": "Monthly and yearly cost of AI writing tools by seats, from official pricing pages.",
            },
            faq(qa)[1],
            crumbs([("ToolPick", "/"), ("Save money", "/save-money.html"), ("AI writing cost", PC_PATH)]),
        ],
    )
    V63_CHANGED.append(PC_PATH)
    _lm[PC_PATH] = WRITECOST_CHECKED
    return PC_PATH, PCD
