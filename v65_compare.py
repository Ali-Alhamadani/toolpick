"""v65: Compare builder 2.0 - any 2-3 tools, every verified fact side by side (price, free plan, yearly saving,
student deal, team seats, refunds, data training, usage limits), an 'Ahead' mark per row by the same fixed rules as the
/compare/ pages (v57), a 'What matters to you?' tally and a plain-language 'Which should you pick?' verdict.
Reuses only facts already verified on official pages (each cell keeps its own source link and checked date).
Also upgrades every /compare/X-vs-Y page with 'add a third tool' links into the builder (want= priorities carried over)."""
import json, os, re

V65_DATE = "2026-11-08"
PATH = "/compare-builder.html"


def build_v65(ctx):
    page = ctx["page"]; e = ctx["e"]; turl = ctx["turl"]; slug = ctx["slug"]; BASE = ctx["BASE"]
    crumbs = ctx["crumbs"]; faq = ctx["faq"]; _lm = ctx["_lm"]; URLS = ctx["URLS"]
    _row57 = ctx["_row57"]; ROWS57 = ctx["ROWS57"]; WANT57 = ctx["WANT57"]; _P57CSS = ctx["_P57CSS"]
    bmap = ctx["_bmap"]; BOPTS = ctx["BOPTS"]; CAPS = ctx["CAPS"]; CAP_LABEL = ctx["CAP_LABEL"]
    USAGE = ctx["USAGE"]; USAGE_CHECKED = ctx["USAGE_CHECKED"]; COMPARISONS = ctx["COMPARISONS"]; cnames = ctx["cnames"]
    CATEGORIES = ctx["CATEGORIES"]
    changed = []

    # ---------- per-tool verified facts (same cells as the /compare/ pages) ----------
    names = {v["s"]: v["n"] for v in bmap.values()}
    UB = {u["t"]: u for u in USAGE}
    FX = {}
    cover = {k: 0 for k, *_ in ROWS57}; cover["usage"] = 0
    for s, n in names.items():
        rows = {}
        for key, *_ in ROWS57:
            c = _row57(key, n)
            na = c.get("r") is None and not c.get("plan") and "na57" in c["h"]
            d = {"h": c["h"]}
            if na: d["na"] = 1
            else: cover[key] += 1
            for f in ("r", "why", "m", "y", "plan", "odd", "soft"):
                if c.get(f) not in (None, False, ""): d[f] = c[f]
            rows[key] = d
        o = {"r": rows, "c": [CAP_LABEL.get(x, x) for x in CAPS[n]]}
        u = UB.get(n)
        if u:
            cover["usage"] += 1
            o["u"] = (f'<b>How it’s counted:</b> {e(u["unit"])}<br><span class="small"><b>Resets:</b> {e(u["reset"])}</span>'
                      + (f'<br><span class="small"><b>Extra usage:</b> {e(u["extra"])}</span>' if u.get("extra") else "")
                      + f'<span class="s57"><a href="{e(u["src"][0][1])}" rel="noopener" target="_blank">source<span class="skip"> for {e(n)} (opens in a new tab)</span></a> · checked {USAGE_CHECKED} · '
                      f'<a href="/ai-usage-limits.html?tool={slug(n)}&amp;use=daily#picker">which plan for my usage?</a></span>')
        FX[s] = o
    # ready-made /compare/ pages by tool set
    CP = {}
    for x in COMPARISONS:
        ns = cnames(x)
        if os.path.exists(f"public/compare/{x[0]}.html"):
            CP[",".join(sorted(slug(n) for n in ns))] = [x[0], x[1]]
    ROWDEF = [[k, lab, href, hl] for k, lab, href, hl in ROWS57]
    WANT = dict(WANT57); WANT = {"price": "Lower price", **WANT}
    FXJ = json.dumps({"f": FX, "cp": CP, "rows": ROWDEF, "want": WANT}, separators=(",", ":")).replace("</", "<\\/")

    # ---------- page ----------
    ex = [("chatgpt,claude,google-gemini", "privacy,price", "ChatGPT vs Claude vs Gemini (privacy + price)"),
          ("cursor,github-copilot,windsurf", "price,refund", "Cursor vs GitHub Copilot vs Windsurf (price + refunds)"),
          ("elevenlabs,murf,speechify", "free,yearly", "ElevenLabs vs Murf vs Speechify (free plan + yearly)")]
    exl = " · ".join(f'<a href="{PATH}?tools={t}&amp;want={w}">{e(l)}</a>' for t, w, l in ex)
    readymade = sorted(((x[1], x[0]) for x in COMPARISONS if os.path.exists(f"public/compare/{x[0]}.html")), key=lambda z: z[0].lower())
    nos = ('<noscript><div class="bnote"><h2 style="margin-top:0;font-size:1.05rem">The builder needs JavaScript</h2><p class="small">Every ready-made comparison below works without it and has the same side-by-side facts, “Ahead” marks and “Pick X if…” advice:</p><ul class="v65nj">'
           + "".join(f'<li><a href="/compare/{s}.html">{e(t)}</a></li>' for t, s in readymade) + '</ul></div></noscript>')
    css = _P57CSS + ('<style>.v65v{border:2px solid var(--ac);border-radius:var(--r);padding:var(--s4);background:var(--sf);margin:var(--s4) 0}.v65v h2{margin:0 0 6px;font-size:1.2rem}'
           '.v65q{font-size:1.05rem;margin:0 0 8px}.v65sug{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 0}.v65sug .chip{cursor:pointer}'
           '.v65nj{columns:2;column-gap:24px}@media(max-width:640px){.v65nj{columns:1}}#builder-out h2:focus{outline:none}.bp57 td .a57{margin-bottom:2px}'
           '.bp57 tr.hl57 a{color:var(--tx)}.v65rb th{white-space:normal}.v65lk{margin:var(--s3) 0}.v65lk a{margin-right:6px}</style>')
    body = f"""{css}<h1>Compare any AI tools side by side</h1><p class="tag">Pick 2 or 3 of our {len(bmap)} tools. You get every fact we’ve checked on their official pages, side by side: price, free plan, yearly saving, student and team deals, refunds, whether they train on your data and usage limits. Then a plain-language answer to “which should I pick?” for what matters to you.</p>
<p class="small v50">Buying for a team? <a href="/ai-team-plans.html">See what AI team plans cost for your team size →</a></p>
<div class="builder"><form id="bform" action="{PATH}" method="get"><fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-bottom:12px">Choose 2–3 tools to compare</legend><div class="bform">
<div><label for="tool1">Tool 1 (required)</label><select id="tool1" name="tool1"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool2">Tool 2 (required)</label><select id="tool2" name="tool2"><option value="">Select a tool…</option>{BOPTS}</select></div>
<div><label for="tool3">Tool 3 (optional)</label><select id="tool3" name="tool3"><option value="">Select a tool…</option>{BOPTS}</select></div>
</div></fieldset><div class="bactions"><button type="submit" class="bbtn primary">Compare tools</button><button type="button" class="bbtn" id="copyBtn">Copy share link</button><button type="button" class="bbtn" id="clearBtn">Clear</button><span class="small bstatus" id="bstatus" role="status"></span></div><div id="sugg" class="v65sug" hidden></div></form></div>
{nos}
<div id="builder-out"><p class="small">Pick at least 2 different tools above to see your comparison. Or try: {exl}.</p></div>
<details class="bnote"><summary><h2 style="display:inline;margin:0;font-size:1.05rem">How the “Ahead” marks and the verdict work</h2></summary><p class="small" style="margin:8px 0 0">Each row is called by a fixed rule, using only facts read on the tool’s official page (each cell shows its source and checked date): <b>price</b> only when the tools do the same main job, on the same billing (monthly with monthly, or billed-yearly with billed-yearly), lighter tiers compared at their comparable tier; a free plan beats none; the bigger yearly saving; a free student plan, then a discount; the lower per-seat team price on the same billing; a stated refund window, then case by case, then none; not training on your data, then opt-in, then opt-out, then no opt-out. No row is called when a tool hasn’t been checked, and usage limits are shown but never ranked (each tool counts usage differently). The verdict tallies the rows you say matter to you; with none picked it tallies every row we could call. It never uses reviews, ratings or features we haven’t checked. <a href="/how-we-pick.html">How we pick</a>.</p><p class="small" style="margin:12px 0 0">True totals by seats and billing: <a href="/cost-calculator.html">cost calculator →</a> · Filter all tools by dealbreakers: <a href="/tools.html?train=off">tools directory →</a></p></details>
<script>const BD={ctx["BDATA"]};const FX={FXJ};
{JS}
</script>"""
    qas = [("How does the ToolPick compare builder pick a winner?", "Row by row, with fixed rules and only facts read on each tool's official page: the lower price on the same billing (only for tools that do the same main job), a free plan over none, the bigger yearly saving, a free student plan then a discount, the lower per-seat team price, a stated refund window, and not training on your data by default. You choose which rows matter; the builder tallies them. Rows are never called for tools we haven't checked."),
           ("Can I share a comparison?", f"Yes. The address updates as you pick, for example {BASE}{PATH}?tools=chatgpt,claude&want=privacy,price, and the Copy share link button copies it."),
           ("Which facts are compared?", f"Price and cheapest checked plan, free plan limits, yearly billing saving, student deal, team per-seat price, refund window and how to cancel, whether your data trains their AI, and usage limits for {cover['usage']} chat and coding assistants (checked {USAGE_CHECKED}).")]
    fh, fl = faq(qas)
    body = body + fh
    while PATH in URLS: URLS.remove(PATH)
    page(PATH, "Compare AI Tools Side by Side: Price, Privacy, Refunds & Which to Pick | ToolPick",
         "Pick any 2–3 AI tools and compare price, free plan, yearly saving, student and team deals, refunds, data training and usage limits side by side, with a plain-language pick for what matters to you. Shareable link; facts from official pages.",
         body,
         [{"@context": "https://schema.org", "@type": "WebApplication", "name": "ToolPick compare builder", "url": BASE + PATH, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "description": "Compare any 2-3 AI tools on verified price, free plan, yearly saving, student and team deals, refunds, data training and usage limits, with a which-to-pick verdict."},
          fl, crumbs([("ToolPick", "/"), ("Compare builder", PATH)])])
    _lm[PATH] = V65_DATE
    changed.append(PATH)

    # ---------- upgrade /compare/ pages: add-a-third-tool links into the builder ----------
    same = {v["s"]: v.get("al") or [] for v in bmap.values()}
    for x in COMPARISONS:
        fp = f"public/compare/{x[0]}.html"
        if not os.path.exists(fp): continue
        h = open(fp).read()
        if ' v65"' in h: continue
        ss = [slug(n) for n in cnames(x)]
        if any(s not in names for s in ss): continue
        base = ",".join(ss)
        add = []
        if len(ss) < 3:
            for s in ss:
                for a in same.get(s, []):
                    if a not in ss and a not in add and a in names: add.append(a)
            add = add[:3]
        al = " ".join(f'<a class="chip" data-v65 href="{PATH}?tools={base},{a}">+ {e(names[a])}</a>' for a in add)
        snip = (f'<div class="bnote v65" style="margin:var(--s4) 0"><p style="margin:0 0 6px"><b>Weigh this for your needs{" or add a third tool" if add else ""}</b></p>'
                f'<p class="small" style="margin:0 0 8px">Open {e(" vs ".join(cnames(x)))} in the compare builder to tally only what matters to you{", or add a same-job tool" if add else ""}. Your picks above carry over.</p>'
                f'<p class="v65lk" style="margin:0"><a class="bbtn" data-v65 href="{PATH}?tools={base}">Open in compare builder →</a> {al}</p></div>'
                '<style>.bp57 tr.hl57 a{color:var(--tx)}</style><script>(function(){var L=document.querySelectorAll("a[data-v65]");function u(){var w=new URLSearchParams(location.search).get("want");L.forEach(function(a){var h=a.getAttribute("href").replace(/&want=[^&]*/,"");a.setAttribute("href",w?h+"&want="+w:h)})}u();document.addEventListener("click",function(ev){if(ev.target.closest("[data-w57]"))setTimeout(u,0)})})();</script>')
        if '<h2 class="h3">Who should pick which</h2>' in h:
            h2 = h.replace('<h2 class="h3">Who should pick which</h2>', snip + '<h2 class="h3">Who should pick which</h2>', 1)
        elif '</section><p class="small">More:' in h:
            h2 = h.replace('</section><p class="small">More:', snip + '</section><p class="small">More:', 1)
        elif '<p class="small">More:' in h:
            h2 = h.replace('<p class="small">More:', snip + '<p class="small">More:', 1)
        else:
            continue
        open(fp, "w").write(h2); changed.append(f"/compare/{x[0]}.html")
    return changed, cover, len(FXJ)


JS = r"""const bySlug={};BD.forEach(t=>bySlug[t.s]=t);
const X=v=>String(v==null?'':v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const $=id=>document.getElementById(id);
const sels=()=>['tool1','tool2','tool3'].map(id=>$(id));
const WK=Object.keys(FX.want);let want=new Set();
function selected(){const seen=new Set(),out=[];sels().forEach(s=>{if(s.value&&!seen.has(s.value)&&bySlug[s.value]){seen.add(s.value);out.push(bySlug[s.value])}});return out}
function sameJob(l){return l.every(t=>t.cap==l[0].cap)}
function basis(l){return l.every(t=>t.mm!=null)?'mm':(l.every(t=>t.ma!=null)?'ma':null)}
function adj(l){return l.some(x=>!x.lt)?l.map(t=>t.mf!=null&&t.mm!=null?Object.assign({},t,{mm:t.mf,n:t.n+' ('+t.mp+')',lt:null}):t):l}
function m$(v){const r=Math.round(v*100)/100;return '$'+(Number.isInteger(r)?r:r.toFixed(2))}
function entry(t){const p=[];if(t.mm!=null)p.push(m$(t.mm)+'/mo monthly');if(t.ma!=null)p.push(m$(t.ma)+'/mo billed yearly');return p.length?p.join(' · '):'<span class="na57">Not in a form we can compare (“check site”, euros or usage-based)</span>'}
/* price row: same rule as the rest of ToolPick (same main job, same billing, comparable tier) */
function priceCall(list){const a=adj(list);if(!sameJob(list))return {w:null,st:null,note:'different main jobs, so price isn’t compared'};const B=basis(a);if(!B)return {w:null,st:null,note:'not every price is checked on the same billing'};
const r=a.slice().sort((x,y)=>x[B]-y[B]);const d=Math.round((r[1][B]-r[0][B])*100)/100;const BL=B=='mm'?'monthly':'billed-yearly';
if(d<=0)return {w:null,st:'tie',note:'same price on '+BL+' billing'};const tn=a.some(t=>t.lt)&&!a.every(t=>t.lt)?' Different tier: compare features before switching.':'';
return {w:r[0].s,st:'same',why:'price matters most: '+r[0].n+' is '+m$(d)+'/mo ('+m$(d*12)+'/yr) less than '+r[1].n+' on '+BL+' billing'+tn,line:r.map(t=>X(t.n)+' '+m$(t[B])+'/mo').join(' · ')+' ('+BL+')'+tn}}
/* other rows: port of the v57 rules used on every /compare/ page */
function rowCall(key,list){const cells={};list.forEach(t=>cells[t.s]=FX.f[t.s].r[key]);const N=list.length;
if(key=='team'){if(!sameJob(list))return {w:null,st:null,dj:1};for(const f of ['m','y']){const vs=list.filter(t=>cells[t.s][f]);const wp=list.filter(t=>cells[t.s].plan);if(vs.length>=2&&vs.length==wp.length){const lo=Math.min(...vs.map(t=>cells[t.s][f]));const w=vs.filter(t=>cells[t.s][f]==lo);
if(w.length==1&&vs.length==N&&!cells[w[0].s].soft&&!list.some(t=>cells[t.s].odd)){const oth=vs.filter(t=>t!==w[0]).map(t=>t.n+' '+m$(cells[t.s][f])).join(', ');return {w:w[0].s,st:'same',why:'you’re buying seats: '+cells[w[0].s].plan+' is '+m$(lo)+'/seat/mo on '+(f=='m'?'monthly':'yearly')+' billing (vs '+oth+')'}}
return {w:null,st:vs.length==N?'tie':null}}}return {w:null,st:null}}
const rs=list.filter(t=>cells[t.s].r!=null);if(rs.length<2||rs.length<N)return {w:null,st:null};const hi=Math.max(...rs.map(t=>cells[t.s].r));const w=rs.filter(t=>cells[t.s].r==hi);
if(w.length==1&&hi>0)return {w:w[0].s,st:'same',why:cells[w[0].s].why||''};return {w:null,st:'tie'}}
function analyse(list){const calls={price:priceCall(list)};const rows=[];FX.rows.forEach(([k,lab,href,hl])=>{const cs=list.map(t=>FX.f[t.s].r[k]);if(cs.every(c=>c.na))return;rows.push([k,lab,href,hl]);calls[k]=rowCall(k,list)});return {calls,rows}}
function cap(s){return s?s[0].toUpperCase()+s.slice(1):s}
function verdict(list,A){const nm=s=>bySlug[s].n;const keys=Object.keys(A.calls).filter(k=>WK.includes(k));
const usable=keys.filter(k=>A.calls[k].w||A.calls[k].st=='tie');const pick=want.size?[...want].filter(k=>keys.includes(k)):usable;
const tally={},ties=[],none=[];pick.forEach(k=>{const c=A.calls[k];if(c.w)(tally[c.w]=tally[c.w]||[]).push(FX.want[k]);else if(c.st=='tie')ties.push(FX.want[k]);else none.push(FX.want[k])});
const r=Object.entries(tally).sort((a,b)=>b[1].length-a[1].length);let q;
const dj=!sameJob(list);
if(dj)q='<b>These do different jobs, so pick by job first:</b> '+list.map(t=>X(t.n)+' for '+X(t.cl)).join(', ')+'.'+(r.length?' On the policy facts we checked, '+r.map(x=>X(nm(x[0]))+' is ahead on '+x[1].length).join(', ')+'.':'');
else if(!pick.length)q='<b>Not enough checked facts to call a winner on what you picked.</b> Compare the details below.';
else if(!r.length)q='<b>No clear winner'+(want.size?' on what you picked':'')+'.</b> They’re level on the facts we could check.';
else{const top=r[0];const tie=r.length>1&&r[1][1].length==top[1].length;
q=tie?'<b>It’s close.</b> '+r.filter(x=>x[1].length==top[1].length).map(x=>X(nm(x[0]))).join(' and ')+' are ahead on '+top[1].length+' each.':(want.size?'<b>Our pick for you: <a href="'+bySlug[top[0]].u+'">'+X(nm(top[0]))+'</a></b> — ahead on '+top[1].map(X).join(', ')+' ('+top[1].length+' of the '+pick.length+' thing'+(pick.length==1?'':'s')+' you picked).':'<b><a href="'+bySlug[top[0]].u+'">'+X(nm(top[0]))+'</a> is ahead on more of the facts we checked</b> ('+top[1].length+' of '+pick.length+'). Tap what matters to you to make it your pick.')}
let det=r.map(x=>X(nm(x[0]))+' is ahead on: '+x[1].map(X).join(', ')+'.').join(' ');if(ties.length)det+=' Level on: '+ties.map(X).join(', ')+'.';if(none.length)det+=' Can’t call (not checked for every tool, or not comparable): '+none.map(X).join(', ')+'.';
if(dj)det+=' Price and team seats aren’t compared across different jobs.';
const chips=keys.filter(k=>A.calls[k].w||A.calls[k].st=='tie'||want.has(k)).map(k=>'<button type="button" class="chip" data-want="'+k+'" aria-pressed="'+want.has(k)+'">'+X(FX.want[k])+'</button>').join('');
const why={};list.forEach(t=>why[t.s]=[]);Object.values(A.calls).forEach(c=>{if(c.w&&c.why)why[c.w].push(c.why)});
list.forEach(t=>{const mine=FX.f[t.s].c.filter(c=>list.every(o=>o===t||!FX.f[o.s].c.includes(c)));if(mine.length)why[t.s].push('you also need '+mine.slice(0,2).join(' and ')+' (from what its own site says it does)')});
const picks=list.map(t=>'<article class="card"><h3>Pick <a href="'+t.u+'">'+X(t.n)+'</a> if…</h3>'+(why[t.s].length?'<ul>'+why[t.s].map(w=>'<li>'+X(cap(w).replace(/\.$/,''))+'.</li>').join('')+'</ul>':'<p class="small">No clear edge in the facts we checked. Decide on features and the details below.</p>')+'</article>').join('');
return {q,det,chips,picks,text:q.replace(/<[^>]+>/g,'')}}
function cellsRow(lab,sub,list,fn,win){return '<tr><th scope="row">'+lab+(sub?'<br>'+sub:'')+'</th>'+list.map(t=>'<td data-t="'+X(t.n)+'">'+(win&&win==t.s?'<span class="a57">Ahead</span><br>':'')+fn(t)+'</td>').join('')+'</tr>'}
function suggest(list){const box=$('sugg');if(!list.length||list.length>=3){box.hidden=true;box.innerHTML='';return}const have=new Set(list.map(t=>t.s));const out=[];list.forEach(t=>(t.al||[]).forEach(a=>{if(!have.has(a)&&bySlug[a]&&!out.includes(a))out.push(a)}));
const s=out.slice(0,4);if(!s.length){box.hidden=true;return}box.hidden=false;box.innerHTML='<span class="small">'+(list.length==1?'Compare '+X(list[0].n)+' with a tool that does the same job:':'Add a third tool that does the same job:')+'</span>'+s.map(a=>'<button type="button" class="chip" data-add="'+a+'">+ '+X(bySlug[a].n)+'</button>').join('')}
function url(list){let s='?tools='+list.map(t=>t.s).join(',');if(want.size)s+='&want='+[...want].join(',');return s}
let last='';
function render(push=true,focus=false){const list=selected();const out=$('builder-out');const st=$('bstatus');suggest(list);
if(list.length<2){out.innerHTML='<div class="pick"><b>Pick at least 2 different tools to compare.</b><p class="small" style="margin-bottom:0">You have selected '+list.length+' tool'+(list.length==1?'':'s')+'. Choose '+(2-list.length)+' more above'+(list.length==1?' or tap a suggestion':'')+' — comparisons work with 2 or 3 tools.</p></div>';if(push)history.replaceState(null,'',list.length?url(list):location.pathname);return}
const A=analyse(list);const V=verdict(list,A);const pc=A.calls.price;
const key=list.map(t=>t.s).sort().join(',');const cp=FX.cp[key];
const head='<tr><th scope="col">What you get</th>'+list.map(t=>'<th scope="col"><a href="'+t.u+'">'+X(t.n)+'</a></th>').join('')+'</tr>';
let rows=cellsRow('Main job','',list,t=>X(t.cl)+'<br><span class="small">'+X(t.d)+'</span>');
rows+=cellsRow('Price','<a href="/cost-calculator.html">Cost calculator →</a>',list,t=>X(t.p)+'<br><span class="small"><b>Cheapest checked:</b> '+entry(t)+'</span><span class="s57"><a href="'+X(t.pr)+'" rel="noopener" target="_blank">source<span class="skip"> for '+X(t.n)+' (opens in a new tab)</span></a> · checked '+X(t.k)+'</span>',pc.w).replace('<tr>','<tr data-r65="price">');
A.rows.forEach(([k,lab,href,hl])=>{rows+=cellsRow(X(lab),'<a href="'+href+'">'+X(hl)+' →</a>',list,t=>FX.f[t.s].r[k].h,A.calls[k].w).replace('<tr>','<tr data-r65="'+k+'">')});
if(list.some(t=>FX.f[t.s].u))rows+=cellsRow('Usage limits','<a href="/ai-usage-limits.html">Usage limits →</a>',list,t=>FX.f[t.s].u||'<span class="na57">Not in our usage-limit checks (we cover chat and coding assistants)</span>');
const tbl='<section class="bp57 v65rb" aria-labelledby="sbsh"><h2 id="sbsh">Side by side: every fact we checked</h2><p class="small">“Ahead” means better on that row only, by the rules below the builder. Each cell links its official source and the date we read it.</p><div class="tw"><table><caption class="skip">'+list.map(t=>X(t.n)).join(' vs ')+': price, free plan, yearly billing, student deal, team plan, refunds, data training, usage limits</caption><thead>'+head+'</thead><tbody>'+rows+'</tbody></table></div></section>';
const links='<p class="small v65lk">'+(cp?'<a href="/compare/'+cp[0]+'.html">Read the full '+X(cp[1])+' page →</a> · ':'')+'<a href="/cost-calculator.html?tool='+list[0].s+'&amp;seats=1&amp;billing=monthly">True cost by seats →</a> · Share: <a href="'+url(list).replace(/&/g,'&amp;')+'">'+X(location.origin+location.pathname+url(list))+'</a></p>';
const vbox='<section class="v65v" aria-labelledby="v65h"><h2 id="v65h" tabindex="-1">Which should you pick?</h2><p class="v65q" id="v65q">'+V.q+'</p><p class="small" style="margin:0 0 8px">'+V.det+'</p>'+(pc.line?'<p class="small" style="margin:0 0 8px"><b>Price, like for like:</b> '+pc.line+'</p>':(pc.note?'<p class="small" style="margin:0 0 8px"><b>Price:</b> not compared — '+X(pc.note)+'.</p>':''))+
(V.chips?'<p style="margin:12px 0 0;font-weight:600" id="w65l">What matters to you?</p><div class="w57" role="group" aria-labelledby="w65l">'+V.chips+(want.size?'<button type="button" class="chip" data-want="">Clear</button>':'')+'</div>':'')+'<div class="pk57">'+V.picks+'</div></section>';
out.innerHTML='<h2 class="skip" id="res-h">Your comparison: '+list.map(t=>X(t.n)).join(' vs ')+'</h2>'+vbox+tbl+links;
document.querySelectorAll('tr[data-r65]').forEach(r=>r.classList.toggle('hl57',want.has(r.dataset.r65)));
if(push)history.replaceState(null,'',url(list));
const msg=list.length+' tools compared. '+V.text;if(msg!=last){st.textContent=msg;last=msg}
document.title=list.map(t=>t.n).join(' vs ')+': which to pick? | ToolPick compare builder';
if(focus)$('v65h').focus()}
$('bform').addEventListener('submit',ev=>{ev.preventDefault();render(true,true)});
sels().forEach(s=>s.addEventListener('change',()=>render()));
document.addEventListener('click',ev=>{const w=ev.target.closest('[data-want]');if(w){const k=w.dataset.want;if(!k)want.clear();else want.has(k)?want.delete(k):want.add(k);render();const b=document.querySelector('[data-want="'+k+'"]')||$('v65h');b.focus();return}
const a=ev.target.closest('[data-add]');if(a&&a.closest('#sugg')){const free=sels().find(s=>!s.value);if(free){free.value=a.dataset.add;render(true,selected().length>=2)}}});
$('clearBtn').addEventListener('click',()=>{sels().forEach(s=>s.value='');want.clear();render();$('bstatus').textContent='Cleared. Pick at least 2 tools.';last='';sels()[0].focus()});
$('copyBtn').addEventListener('click',async()=>{const list=selected();const st=$('bstatus');if(list.length<2){st.textContent='Pick at least 2 tools before copying a share link.';return}const u=location.origin+location.pathname+url(list);try{await navigator.clipboard.writeText(u);st.textContent='Share link copied: '+u}catch(err){st.textContent='Copy this share link: '+u;window.prompt('Copy this share link',u)}});
(function init(){const p=new URLSearchParams(location.search);let q=p.get('tools');if(!q){const t=['tool1','tool2','tool3'].map(k=>p.get(k)).filter(Boolean);if(t.length)q=t.join(',')}
(p.get('want')||'').split(',').forEach(k=>{if(WK.includes(k))want.add(k)});
if(q){q.split(',').map(x=>x.trim()).filter(x=>bySlug[x]).slice(0,3).forEach((v,i)=>{if(sels()[i])sels()[i].value=v})}
if(q||selected().length)render(true);})();"""
