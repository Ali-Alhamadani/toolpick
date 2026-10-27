"""ToolPick data. Edit this file, then run build.py.
price: exactly what the official pricing page showed on `checked`; use "check site" if not verifiable.
"""
CHECKED = "2026-10-19"
CATEGORIES = [
 {"id":"video","name":"Video","need":"Make or edit videos","best":"Runway","free":["CapCut","HeyGen","Synthesia"],"tools":[
  {"name":"Runway","url":"https://runwayml.com","pricing":"https://runwayml.com/pricing","price":"Standard $15/mo ($12/mo billed yearly); Pro $35 ($28); Max $95 ($76)","free":"Free plan: one-time 125 credits","about":"Gen-4.5 text/image-to-video plus image and audio models in one app.","why":"A full generative video studio, with one-time free credits to test it first."},
  {"name":"Pika","url":"https://pika.art","pricing":"https://pika.art/pricing","price":"Starter $10/mo ($8 yearly); Creator $35 ($28); Fancy $95-$880","free":"Free plan: $0, credit packs only, no commercial license","about":"Short AI video clips from text or images."},
  {"name":"Luma Dream Machine","url":"https://lumalabs.ai","pricing":"https://lumalabs.ai/pricing","price":"Plus $30/mo ($25 yearly); Pro $90 ($75); Ultra $300 ($250)","free":"No free plan listed on pricing page","about":"Ray models plus third-party video/image models, commercial use on Plus."},
  {"name":"Kling AI","url":"https://klingai.com","pricing":"https://klingai.com/global/membership/membership-plan","price":"check site","free":"check site","about":"Text/image-to-video generator (pricing page loads via app, could not verify)."},
  {"name":"HeyGen","url":"https://www.heygen.com","pricing":"https://www.heygen.com/pricing","price":"Creator $29/mo ($24 yearly); Pro from $49; Business $149 + $20/seat","free":"Free: 3 videos/mo, up to 1 min each","about":"AI avatar videos, voice cloning and video translation."},
  {"name":"Synthesia","url":"https://www.synthesia.io","pricing":"https://www.synthesia.io/pricing","price":"Starter $29/mo (yearly from $18/mo); Pro $89/mo ($64 yearly)","free":"Basic free: 10 min video/mo + 500 credits, watermarked","about":"Business/training videos with AI presenters in 140+ languages."},
  {"name":"Descript","url":"https://www.descript.com","pricing":"https://www.descript.com/pricing","price":"Hobbyist $24/mo ($16 yearly); Creator $35 ($24); Business $65 ($50)","free":"Free: 1 media hour/mo, 720p export","about":"Edit video by editing the transcript; AI clean-up tools."},
  {"name":"CapCut","url":"https://www.capcut.com","pricing":"https://www.capcut.com/pricing","price":"Pro $19.99/mo; Ultra $79/mo; Teams $12.49/seat/mo","free":"Free plan with basic editing and templates","about":"Easy editor for short-form social video, AI features built in."},
  {"name":"InVideo","url":"https://invideo.io","pricing":"https://invideo.io/pricing","price":"Starter $20/mo ($10 yearly); Plus $60 ($30); higher tiers from $150","free":"Free editor available","about":"Prompt-to-video for explainer and social videos."},
 ]},
 {"id":"writing","name":"Writing","need":"Write, edit or brainstorm text","best":"Claude","free":["ChatGPT","Google Gemini","Grammarly"],"tools":[
  {"name":"Claude","url":"https://claude.ai","pricing":"https://claude.com/pricing","price":"Pro $20/mo ($17/mo billed yearly); Max from $100/mo","free":"Free plan: $0","about":"Strong long-form writing, editing and analysis assistant.","why":"Pro is $17-20/mo with a usable free tier, and is excellent at long, natural-sounding drafts."},
  {"name":"ChatGPT","url":"https://chatgpt.com","pricing":"https://chatgpt.com/pricing","price":"check site","free":"Free plan with unlimited text chats on GPT-6 (limits on tools)","about":"General-purpose AI assistant: writing, research, images, voice."},
  {"name":"Google Gemini","url":"https://gemini.google.com","pricing":"https://one.google.com/about/ai-premium","price":"Paid tiers $4.99/mo, $19.99/mo, Ultra from $99.99/mo","free":"Gemini app is free to use","about":"Google's assistant, integrated with Gmail, Docs and Drive."},
  {"name":"Grammarly","url":"https://www.grammarly.com","pricing":"https://www.grammarly.com/plans","price":"Pro $30/mo ($12/mo billed yearly, $144/yr; $60 quarterly) (checked 2026-10-23)","free":"Free: $0 spelling & grammar checks","about":"Grammar, clarity and tone fixes everywhere you type."},
  {"name":"Notion AI","url":"https://www.notion.com","pricing":"https://www.notion.com/pricing","price":"Plus $12/member/mo ($10 billed yearly); Business $24/member/mo ($20 billed yearly) (checked 2026-10-23)","free":"Free plan: $0 (AI trial only)","about":"AI writing inside your notes, docs and wikis."},
  {"name":"Copy.ai","url":"https://www.copy.ai","pricing":"https://www.copy.ai/prices","price":"Chat $29/mo ($24 yearly); team plans from $1,000/mo","free":"Free trial available","about":"Marketing copy and GTM workflow automation."},
  {"name":"Jasper","url":"https://www.jasper.ai","pricing":"https://www.jasper.ai/pricing","price":"check site","free":"7-day free trial of Pro","about":"On-brand marketing content for teams."},
 ]},
 {"id":"coding","name":"Coding","need":"Write code or build an app","best":"GitHub Copilot","free":["GitHub Copilot","Windsurf","v0"],"tools":[
  {"name":"GitHub Copilot","url":"https://github.com/features/copilot","pricing":"https://github.com/features/copilot/plans","price":"Pro $10/mo; Pro+ $39/mo; Max $100/mo","free":"Free plan: $0","about":"AI pair programmer in VS Code, JetBrains and GitHub.","why":"Paid plan from $10/mo and a real free tier, and it works in the editor you already use."},
  {"name":"Cursor","url":"https://cursor.com","pricing":"https://cursor.com/pricing","price":"Plus $8/mo; Premium $30/mo; Super $100; Ultra $200; Teams $30/user","free":"Free: $0 with limited agent requests","about":"AI-first code editor with agents."},
  {"name":"Windsurf","url":"https://windsurf.com","pricing":"https://windsurf.com/pricing","price":"Pro $20/mo; Max $200/mo; Teams $80/mo + $40/seat","free":"Free: $0","about":"Agentic AI IDE."},
  {"name":"Claude (Pro)","url":"https://claude.ai","pricing":"https://claude.com/pricing","price":"Pro $20/mo ($17 yearly); Max from $100/mo","free":"Free plan: $0","about":"Strong coding model for chat-based and agentic coding."},
  {"name":"Bolt","url":"https://bolt.new","pricing":"https://bolt.new/pricing","price":"Pro $25/mo ($18/mo billed yearly, $216/yr); Teams $30/member/mo ($27/member/mo billed yearly) (checked 2026-10-22)","free":"Free: 300K tokens/day, 1M/month","about":"Build full-stack web apps from a prompt in the browser."},
  {"name":"v0","url":"https://v0.app","pricing":"https://v0.app/pricing","price":"Team $30/user/mo; Business $100/user/mo","free":"Free: $0 with daily credits","about":"Vercel's AI app/UI builder, deploys to Vercel."},
  {"name":"Lovable","url":"https://lovable.dev","pricing":"https://lovable.dev/pricing","price":"check site","free":"Free: 5 build credits/day (up to 30/mo)","about":"Prompt-to-app builder for non-developers."},
 ]},
 {"id":"images","name":"Images","need":"Generate or design images","best":"Leonardo","free":["Leonardo","Krea","Ideogram"],"tools":[
  {"name":"Leonardo","url":"https://leonardo.ai","pricing":"https://leonardo.ai/pricing","price":"Essential $12/mo; Premium $30; Ultimate $60","free":"Free: 150 fast tokens/day","about":"Image and video generation with presets and custom model training.","why":"Generous daily free tokens and a $12 entry plan; Premium adds unlimited relaxed image generation."},
  {"name":"Midjourney","url":"https://www.midjourney.com","pricing":"https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans","price":"Basic $10/mo ($8 yearly); Standard $30 ($24); Pro $60 ($48); Mega $120 ($96)","free":"No free plan (subscription only)","about":"Top-tier artistic image quality, plus video."},
  {"name":"Ideogram","url":"https://ideogram.ai","pricing":"https://ideogram.ai/pricing","price":"Plus $20/mo ($15 yearly); Pro $60 ($42); Team $30/user ($20)","free":"Free weekly credits for eligible accounts","about":"Best-in-class text rendering in images (logos, posters)."},
  {"name":"Krea","url":"https://www.krea.ai","pricing":"https://www.krea.ai/pricing","price":"Basic $9/mo; Pro $35/mo ($21 yearly); Max $105 ($63); $200 ($160) (checked 2026-10-22)","free":"Free: 100 units/day","about":"Real-time generation, many models, upscaling."},
  {"name":"Canva","url":"https://www.canva.com","pricing":"https://www.canva.com/pricing/","price":"check site","free":"Free plan available","about":"Design tool with built-in AI image generation."},
  {"name":"Recraft","url":"https://www.recraft.ai","pricing":"https://www.recraft.ai/pricing","price":"check site","free":"Free plan (images not licensed for commercial use)","about":"Vector and brand-style image generation."},
 ]},
 {"id":"audio","name":"Audio","need":"Voice, music or transcription","best":"ElevenLabs","free":["ElevenLabs","Suno","Otter"],"tools":[
  {"name":"ElevenLabs","url":"https://elevenlabs.io","pricing":"https://elevenlabs.io/pricing","price":"Starter $6/mo; Creator $22; Pro $99; Scale $299 (intro discounts shown on site)","free":"Free: $0","about":"Realistic text-to-speech, voice cloning, dubbing, SFX.","why":"$6/mo Starter includes a commercial license; quality leader with a free tier."},
  {"name":"Suno","url":"https://suno.com","pricing":"https://suno.com/pricing","price":"Pro $8/mo; Premier $24/mo (yearly billing prices)","free":"Free: 50 credits/day","about":"Full songs with vocals from a text prompt."},
  {"name":"Murf","url":"https://murf.ai","pricing":"https://murf.ai/pricing","price":"API pay-as-you-go from $0.01/1,000 chars (Studio plans: check site)","free":"$10 free API credit","about":"Studio voiceovers and TTS API."},
  {"name":"Speechify","url":"https://speechify.com","pricing":"https://speechify.com/pricing/","price":"Premium $29/mo (billed monthly)","free":"Free plan, speeds up to 1.5x","about":"Listen to any text read aloud."},
  {"name":"Otter","url":"https://otter.ai","pricing":"https://otter.ai/pricing","price":"Pro $16.99/user/mo ($8.33 yearly); Business $30 ($19.99 yearly)","free":"Basic: free forever","about":"Meeting transcription and notes."},
  {"name":"Descript","url":"https://www.descript.com","pricing":"https://www.descript.com/pricing","price":"Hobbyist $24/mo ($16 yearly); Creator $35 ($24)","free":"Free: 1 media hour/mo","about":"Podcast editing by text, Studio Sound clean-up."},
  {"name":"Udio","url":"https://www.udio.com","pricing":"https://www.udio.com/pricing","price":"check site","free":"check site","about":"AI music generation."},
 ]},
]

CATEGORIES += [
 {"id":"presentations","name":"Presentations","need":"Make slides and pitch decks","best":"Pitch","free":["Pitch","SlidesAI","Canva"],"tools":[
  {"name":"Pitch","url":"https://pitch.com","pricing":"https://pitch.com/pricing","price":"Plus €10/mo; Team €15/mo; Business €20/mo","free":"Free forever: unlimited presentations","about":"Collaborative presentation software with AI credits on paid plans.","why":"Free plan with unlimited presentations, and a paid tier at €10/mo."},
  {"name":"Beautiful.ai","url":"https://www.beautiful.ai","pricing":"https://www.beautiful.ai/pricing","price":"Pro $14.50/mo (billed annually); Team $40/user/mo yearly ($50 monthly)","free":"14-day free trial","about":"Smart Slide layouts that auto-format as you type; PowerPoint import/export."},
  {"name":"Plus AI","url":"https://plusai.com","pricing":"https://plusai.com/pricing","price":"Basic $10/user/mo yearly ($15 monthly); Pro $20 ($25); Team $30 ($40); Max $200 ($240)","free":"7-day free trial (card required)","about":"AI slide generation inside Google Slides and PowerPoint."},
  {"name":"SlidesAI","url":"https://www.slidesai.io","pricing":"https://www.slidesai.io/pricing","price":"$10/mo (billed $120/yr); $20.83/mo (billed $250/yr)","free":"Basic $0: 12 presentations/year","about":"Turns text into Google Slides presentations."},
  {"name":"Gamma","url":"https://gamma.app","pricing":"https://gamma.app/pricing","price":"check site","free":"check site","about":"AI-generated decks, docs and web pages from a prompt."},
  {"name":"Canva","url":"https://www.canva.com","pricing":"https://www.canva.com/pricing/","price":"check site","free":"Free plan available","about":"Design tool with presentation templates and AI features."},
 ]},
 {"id":"assistants","name":"AI Assistants","need":"Chat with an AI assistant","best":"Le Chat (Mistral)","free":["ChatGPT","Claude","Google Gemini"],"tools":[
  {"name":"Le Chat (Mistral)","url":"https://chat.mistral.ai","pricing":"https://mistral.ai/pricing","price":"Pro $14.99/mo; Team $24.99/user/mo (excl. tax)","free":"Free plan with limited access","about":"Mistral's assistant with web search, image generation and the Vibe coding agent.","why":"Pro at $14.99/mo, plus a free plan."},
  {"name":"ChatGPT","url":"https://chatgpt.com","pricing":"https://chatgpt.com/pricing","price":"check site","free":"Free plan with unlimited text chats on GPT-6 (limits on tools)","about":"General-purpose AI assistant: writing, research, images, voice."},
  {"name":"Claude","url":"https://claude.ai","pricing":"https://claude.com/pricing","price":"Pro $20/mo ($17/mo billed yearly); Max from $100/mo","free":"Free plan: $0","about":"Assistant known for long-form writing, analysis and coding."},
  {"name":"Google Gemini","url":"https://gemini.google.com","pricing":"https://one.google.com/about/ai-premium","price":"Paid tiers $4.99/mo, $19.99/mo, Ultra from $99.99/mo","free":"Gemini app is free to use","about":"Google's assistant, integrated with Gmail, Docs and Drive."},
  {"name":"Perplexity","url":"https://www.perplexity.ai","pricing":"https://www.perplexity.ai/pricing","price":"check site","free":"check site","about":"Answer engine that cites web sources."},
  {"name":"Microsoft Copilot","url":"https://copilot.microsoft.com","pricing":"https://www.microsoft.com/en-us/microsoft-365/copilot/pricing","price":"check site","free":"check site","about":"Microsoft's assistant, built into Windows and Microsoft 365."},
 ]},
]

COMPARISONS = [
 ("runway-vs-kling","Runway vs Kling AI","Runway","Kling AI","video"),
 ("claude-vs-chatgpt-for-writing","Claude vs ChatGPT for writing","Claude","ChatGPT","writing"),
 ("github-copilot-vs-cursor","GitHub Copilot vs Cursor","GitHub Copilot","Cursor","coding"),
 ("midjourney-vs-leonardo","Midjourney vs Leonardo","Midjourney","Leonardo","images"),
 ("elevenlabs-vs-murf","ElevenLabs vs Murf","ElevenLabs","Murf","audio"),
 ("heygen-vs-synthesia","HeyGen vs Synthesia","HeyGen","Synthesia","video"),
 ("pitch-vs-beautiful-ai","Pitch vs Beautiful.ai","Pitch","Beautiful.ai","presentations"),
]

def T(name,url,pricing,price,free,about,why=None,**kw):
    d=dict(name=name,url=url,pricing=pricing,price=price,free=free,about=about,**kw)
    if why: d["why"]=why
    return d
CK="check site"
_extra = {
 "video":[T("Opus Clip","https://www.opus.pro","https://www.opus.pro/pricing","Paid from $15/mo billed monthly","Free forever plan ($0)","Turns long videos into short viral clips automatically."),
          T("Captions","https://www.captions.ai","https://www.captions.ai/pricing","From $24.99/mo; higher tiers $69.99, $139.99, $279.99/mo",CK,"AI video editing, captions and AI actors for creators.")],
 "writing":[T("Wordtune","https://www.wordtune.com","https://www.wordtune.com/plans","From $6.99/mo ($4.89/mo with yearly discount); next tier $9.99 ($6.99)","Basic $0 (limited)","Rewrites sentences for clarity and tone."),
            T("Rytr","https://rytr.me","https://rytr.me/pricing","$7.50/mo; $24.16/mo for multiple brands","Free forever, no card","Budget AI writer for short-form content.")],
 "coding":[T("Warp","https://www.warp.dev","https://www.warp.dev/pricing","$20/mo (includes $20 of agent usage)","Free: $0","AI-powered terminal with coding agents."),
           T("Qodo","https://www.qodo.ai","https://www.qodo.ai/pricing/","Pro Team $30 (per user/mo)",CK,"AI code review and test generation.")],
 "images":[T("Magnific","https://www.magnific.com","https://www.magnific.com/pricing","$20/mo ($14.50 yearly); $45 ($33.75); $110 ($82.50)",CK,"AI image/video generation plus stock content."),
           T("Photoroom","https://www.photoroom.com","https://www.photoroom.com/pricing","Pro $7.50/mo; Max $20.99/mo; Ultra $82.50/mo (billed yearly)",CK,"Product photos: background removal and AI scenes.")],
 "audio":[T("Riverside","https://riverside.com","https://riverside.com/pricing","Paid plans billed $288/yr or $408/yr","Free: $0","Studio-quality remote podcast/video recording with AI editing."),
          T("Krisp","https://krisp.ai","https://krisp.ai/pricing/","$16/user/mo ($8/user/mo billed yearly)","Free plan: $0","AI noise cancellation and meeting notes.")],
}
for c in CATEGORIES:
    c["tools"] += _extra.get(c["id"], [])

CATEGORIES += [
 {"id":"marketing","name":"Marketing & SEO","need":"Market, do SEO or post on social","best":"Buffer","free":["Buffer","Surfer","Writesonic"],"tools":[
  T("Buffer","https://buffer.com","https://buffer.com/pricing","Essentials $5/mo per channel ($60/yr billed yearly); Team $10/mo per channel","Free plan available","Schedule social posts with an AI assistant.","Real social scheduling from $5/mo per channel, plus a free plan."),
  T("Surfer","https://surferseo.com","https://surferseo.com/pricing/","AI visibility tracking from $82/mo billed yearly; Standard $99/mo billed yearly","Start for free","SEO content optimization and AI-search visibility tracking."),
  T("Writesonic","https://writesonic.com","https://writesonic.com/pricing","Starter $79/mo billed annually; $199; $399","Start free","AI-search visibility (GEO) and SEO content platform."),
  T("Frase","https://www.frase.io","https://www.frase.io/pricing","$49/mo month-to-month ($39 billed yearly); team $129 ($103)","7-day free trial, no card","SEO briefs and content optimization."),
  T("Predis.ai","https://predis.ai","https://predis.ai/pricing/","Rise $79/mo ($474/yr billed yearly)","3-day trial","AI social media posts, carousels and ads."),
  T("Ocoya","https://www.ocoya.com","https://www.ocoya.com/pricing","Starter $29/mo; Team $79/mo (billed monthly)","Free trial","AI copy + social scheduling."),
  T("Copy.ai","https://www.copy.ai","https://www.copy.ai/prices","Chat $29/mo ($24 yearly)","Free trial available","Marketing copy and GTM workflow automation."),
  T("Jasper","https://www.jasper.ai","https://www.jasper.ai/pricing",CK,"7-day free trial of Pro","On-brand marketing content for teams."),
 ]},
 {"id":"research","name":"Research","need":"Research papers and sources","best":"Elicit","free":["Consensus","Elicit","ResearchRabbit"],"tools":[
  T("Elicit","https://elicit.com","https://elicit.com/pricing","From $11/user/mo billed annually ($132/yr); $39; $89",CK,"AI research assistant for papers and systematic reviews.","Entry tier is $11/mo billed yearly, built specifically for academic literature."),
  T("Scite","https://scite.ai","https://scite.ai/pricing","Basic $12/mo; Pro $40/mo","7-day free trial","Shows whether papers support or contrast a claim."),
  T("Consensus","https://consensus.app","https://consensus.app/pricing/",CK,CK,"Search engine that answers from peer-reviewed research."),
  T("SciSpace","https://scispace.com","https://scispace.com/pricing",CK,CK,"Read, explain and search research papers."),
  T("Humata","https://www.humata.ai","https://www.humata.ai/pricing","Extra pages $0.01-$0.02/page (plans: check site)",CK,"Chat with your PDFs and documents."),
  T("You.com API","https://you.com","https://you.com/plans","Web search API $5 per 1,000 calls",CK,"Search and research APIs for building AI apps."),
  T("Perplexity","https://www.perplexity.ai","https://www.perplexity.ai/pricing",CK,CK,"Answer engine that cites web sources."),
  T("ResearchRabbit","https://www.researchrabbit.ai","https://www.researchrabbit.ai/pricing","ResearchRabbit+ $10/mo (annual plan) or $12.50/mo (monthly plan)","Free: $0, forever","Discover and map related papers and authors."),
  T("Scholarcy","https://www.scholarcy.com","https://www.scholarcy.com/pricing",CK,"Free Article Summarizer: $0 (1 summary/day); 7-day trial of full app","Summarizes research articles into flashcards."),
 ]},
 {"id":"productivity","name":"Productivity & Meetings","need":"Save time on meetings, tasks and email","best":"Fireflies","free":["Fireflies","Zapier","Superhuman"],"tools":[
  T("Fireflies","https://fireflies.ai","https://fireflies.ai/pricing","Pro $18/seat/mo ($10 billed annually); Business $29 ($19)","Free forever: $0","AI meeting notes and transcription.","Free-forever tier plus a $10/mo (billed yearly) Pro with full meeting-assistant features."),
  T("Fathom","https://www.fathom.ai","https://www.fathom.ai/pricing","From $15/user/mo; Business $25-$34/user/mo","Free plan","AI meeting recorder and summaries."),
  T("Otter","https://otter.ai","https://otter.ai/pricing","Pro $16.99/user/mo ($8.33 yearly); Business $30 ($19.99 yearly)","Basic: free forever","Meeting transcription and notes."),
  T("Motion","https://www.usemotion.com","https://www.usemotion.com/pricing","Pro AI $19/seat/mo; Business AI $29/seat/mo","Free trial","AI calendar that auto-schedules your tasks."),
  T("Reclaim","https://reclaim.ai","https://reclaim.ai/pricing","$10/seat/mo for small teams",CK,"Smart calendar scheduling for habits and tasks."),
  T("ClickUp","https://clickup.com","https://clickup.com/pricing","Unlimited $10/user/mo ($7 yearly); Business $19 ($12 yearly)","Free plan","Project management with built-in AI."),
  T("Taskade","https://www.taskade.com","https://www.taskade.com/pricing","Pro $10/mo (yearly, 10 users incl.); $25; $100; $250","Free: $0","Projects, notes and AI agents in one workspace."),
  T("Superhuman","https://superhuman.com","https://superhuman.com/plans","$12/member/mo yearly ($15 monthly); $33 ($40)","Free: $0","AI assistance across your apps (includes Grammarly)."),
  T("Zapier","https://zapier.com","https://zapier.com/pricing","Professional from $19.99/mo; Team from $69/mo","Free forever: 100 tasks/mo","Automate workflows between 7,000+ apps with AI."),
  T("Notion AI","https://www.notion.com","https://www.notion.com/pricing","Plus $12/member/mo ($10 billed yearly); Business $24/member/mo ($20 billed yearly) (checked 2026-10-23)","Free plan: $0 (AI trial only)","AI writing inside your notes, docs and wikis."),
 ]},
 {"id":"agents","name":"Chatbots & Agents","need":"Build a chatbot or AI agent","best":"Botpress","free":["Botpress","Lindy","Zapier Agents"],"tools":[
  T("Botpress","https://botpress.com","https://botpress.com/pricing","Plus $150/mo billed annually (250 conversations); extra $0.65/conversation","Free: $0, 100 conversations","Build and deploy AI chatbots and agents.","Free tier with 100 conversations and transparent per-conversation pricing."),
  T("Chatbase","https://www.chatbase.co","https://www.chatbase.co/pricing","Hobby $40/mo ($32 yearly); Standard $150 ($120)",CK,"Train a support chatbot on your own content."),
  T("Lindy","https://www.lindy.ai","https://www.lindy.ai/pricing","Credit tiers from $29.99/mo","Start with $50 in free credits, no card","No-code AI agents for email, meetings and ops."),
  T("Zapier Agents","https://zapier.com","https://zapier.com/pricing","Professional from $19.99/mo; Team from $69/mo","Free forever: 100 tasks/mo","Automations and AI agents connected to 7,000+ apps."),
  T("Relevance AI","https://relevanceai.com","https://relevanceai.com/pricing",CK,CK,"Build an AI workforce of agents."),
  T("Voiceflow","https://www.voiceflow.com","https://www.voiceflow.com/pricing","Usage-based; businesses request pricing","Free trial, no credit card","Design chat and voice AI agents."),
  T("n8n","https://n8n.io","https://n8n.io/pricing/","Starter €20/mo, Pro €50/mo, Business €667/mo (billed annually)","Free self-hosted Community Edition; cloud trial, no card","Workflow automation with AI agents."),
 ]},
]
for _c in CATEGORIES:
    if _c["id"]=="assistants": _c["free"]=["ChatGPT","Claude","Google Gemini"]

# Entry paid plan: (monthly billing, per-month when billed yearly, cost per output). None = not verified.
PRICE_TABLE = {
 "Runway":(15,12,"Gen-4.5: 60 credits per 5s; Standard's 625 credits ≈ 52s of Gen-4.5"),"Pika":(10,8,"Seedance 2.5 720p 5s = 122 credits; Starter 900 credits ≈ 7 clips"),
 "Luma Dream Machine":(30,25,None),"HeyGen":(29,24,None),"Synthesia":(29,18,"~100 credits per finished video minute"),"Descript":(24,16,None),"CapCut":(19.99,None,None),
 "InVideo":(20,10,None),"Claude":(20,17,None),"Claude (Pro)":(20,17,None),"Grammarly":(30,12,None),"Notion AI":(12,10,None),"Copy.ai":(29,24,None),"GitHub Copilot":(10,None,None),
 "Cursor":(8,None,None),"Windsurf":(20,None,None),"Bolt":(25,18,None),"v0":(30,None,None),"Leonardo":(12,None,None),"Midjourney":(10,8,"Extra Fast GPU time $4/hr"),
 "Ideogram":(20,15,"Pay-as-you-go 1¢ per credit"),"Krea":(9,None,None),"ElevenLabs":(6,None,None),"Suno":(None,8,None),"Murf":(None,None,"$0.01-$0.03 per 1,000 characters (API)"),
 "Speechify":(29,None,None),"Otter":(16.99,8.33,None),"Pitch":("€10",None,None),"Beautiful.ai":(None,14.50,None),"Plus AI":(15,10,None),"SlidesAI":(None,10,None),"Le Chat (Mistral)":(14.99,None,None),
 "Opus Clip":(15,None,None),"Captions":(24.99,None,None),"Wordtune":(6.99,4.89,None),"Rytr":(7.50,None,None),"Warp":(20,None,None),"Qodo":(30,None,None),"Magnific":(20,14.50,None),
 "Photoroom":(None,7.50,None),"Riverside":(None,24,None),"Krisp":(16,8,None),"Buffer":(5,None,"per channel"),"Surfer":(None,82,None),"Writesonic":(None,79,None),"Frase":(49,39,None),
 "Predis.ai":(79,39.50,None),"Ocoya":(29,None,None),"Elicit":(None,11,None),"Scite":(12,None,None),"Humata":(None,None,"$0.01-$0.02 per extra page"),"You.com API":(None,None,"$5 per 1,000 search calls"),
 "Fireflies":(18,10,None),"Fathom":(None,None,None),"Motion":(19,None,None),"Reclaim":(10,None,None),"ClickUp":(10,7,None),"Taskade":(None,10,None),"Superhuman":(15,12,None),
 "Zapier":(19.99,None,"Free tier: 100 tasks/mo"),"Zapier Agents":(19.99,None,None),"Botpress":(None,150,"$0.65 per extra conversation (pack of 100 for $65)"),"Chatbase":(40,32,None),"Lindy":(29.99,None,None),"ResearchRabbit":(12.50,10,None),"Google Gemini":(4.99,None,None),"n8n":(None,"€20",None),
}
# Jobs pages: "best AI tool for [job]" -> (title, category id, intro, tool names in ranked order)
JOBS = [
 ("youtube-shorts","making YouTube Shorts & TikToks","video",["Opus Clip","CapCut","Captions"]),
 ("podcast-editing","editing a podcast","audio",["Descript","Riverside","Krisp"]),
 ("voiceovers","voiceovers & text-to-speech","audio",["ElevenLabs","Murf","Speechify"]),
 ("pitch-decks","making a pitch deck","presentations",["Pitch","Beautiful.ai","Plus AI"]),
 ("blog-seo","writing SEO blog posts","marketing",["Frase","Surfer","Writesonic"]),
 ("meeting-notes","meeting notes","productivity",["Fireflies","Otter","Fathom"]),
 ("customer-support-bot","a customer-support chatbot","agents",["Botpress","Chatbase","Lindy"]),
 ("literature-review","a literature review","research",["Elicit","Scite","Consensus"]),
 ("logos-text-in-images","logos & text in images","images",["Ideogram","Recraft","Leonardo"]),
 ("product-photos","e-commerce product photos","images",["Photoroom","Magnific","Leonardo"]),
 ("beginner-coding","learning to code / beginners","coding",["GitHub Copilot","Bolt","v0"]),
 ("ai-avatar-videos","AI avatar / training videos","video",["HeyGen","Synthesia","Captions"]),
]
COMPARISONS += [
 ("fireflies-vs-otter","Fireflies vs Otter","Fireflies","Otter","productivity"),
 ("botpress-vs-chatbase","Botpress vs Chatbase","Botpress","Chatbase","agents"),
 ("frase-vs-surfer","Frase vs Surfer","Frase","Surfer","marketing"),
 ("elicit-vs-scite","Elicit vs Scite","Elicit","Scite","research"),
 ("opus-clip-vs-capcut","Opus Clip vs CapCut","Opus Clip","CapCut","video"),
]
SPONSOR_TIERS = [("Category Sponsor","Labelled slot on one category page, its best-free page and matching job pages.","Contact for pricing"),
 ("Sitewide Sponsor","One labelled slot on every page (one sponsor at a time).","Contact for pricing")]

JOBS += [
 ("text-to-video","text-to-video generation","video",["Runway","Pika","Luma Dream Machine"]),
 ("video-editing-beginners","easy video editing for beginners","video",["CapCut","Descript","InVideo"]),
 ("explainer-videos","explainer videos from a prompt","video",["InVideo","Synthesia","HeyGen"]),
 ("grammar-checking","grammar & spelling checks","writing",["Grammarly","Wordtune","Superhuman"]),
 ("rewriting-paraphrasing","rewriting & paraphrasing","writing",["Wordtune","Rytr","Claude"]),
 ("long-form-writing","long-form writing & drafts","writing",["Claude","ChatGPT","Google Gemini"]),
 ("building-web-apps-no-code","building a web app without coding","coding",["Lovable","Bolt","v0"]),
 ("code-autocomplete","code autocomplete in your editor","coding",["GitHub Copilot","Cursor","Windsurf"]),
 ("code-review","AI code review","coding",["Qodo","GitHub Copilot","Cursor"]),
 ("ai-art","AI art & illustrations","images",["Midjourney","Leonardo","Krea"]),
 ("social-media-graphics","social media graphics","images",["Canva","Magnific","Ideogram"]),
 ("ai-music","making AI music & songs","audio",["Suno","Udio","ElevenLabs"]),
 ("noise-removal","removing background noise from calls","audio",["Krisp","Descript","Riverside"]),
 ("transcription","transcribing audio","audio",["Otter","Fireflies","Descript"]),
 ("class-presentations","school & class presentations","presentations",["SlidesAI","Canva","Pitch"]),
 ("google-slides","AI in Google Slides","presentations",["Plus AI","SlidesAI","Pitch"]),
 ("social-scheduling","scheduling social media posts","marketing",["Buffer","Ocoya","Predis.ai"]),
 ("ai-search-visibility","ranking in AI search (GEO)","marketing",["Writesonic","Surfer","Frase"]),
 ("research-with-citations","research answers with citations","research",["Perplexity","Consensus","Scite"]),
 ("chat-with-pdfs","chatting with PDFs","research",["Humata","SciSpace","Claude"]),
 ("calendar-scheduling","auto-scheduling your calendar","productivity",["Motion","Reclaim","ClickUp"]),
 ("workflow-automation","automating workflows","agents",["Zapier Agents","n8n","Lindy"]),
 ("email-assistant","email & inbox help","productivity",["Superhuman","Lindy","Google Gemini"]),
]
# Paid tools to build "free alternative to X" pages for (alternatives = same-category tools with a verified free tier)
FREE_ALT_FOR = ["Midjourney","Luma Dream Machine","Runway","Synthesia","HeyGen","Descript","Captions","Jasper","Copy.ai","Grammarly","Cursor","Bolt",
 "Ideogram","Magnific","Photoroom","Speechify","Murf","Beautiful.ai","Plus AI","Frase","Predis.ai","Ocoya","Elicit","Scite","Motion","Chatbase","Otter","Le Chat (Mistral)"]

COMPARISONS += [
 ("chatgpt-vs-claude-vs-gemini","ChatGPT vs Claude vs Gemini",["ChatGPT","Claude","Google Gemini"],None,"assistants"),
 ("cursor-vs-windsurf","Cursor vs Windsurf","Cursor","Windsurf","coding"),
 ("midjourney-vs-ideogram","Midjourney vs Ideogram","Midjourney","Ideogram","images"),
 ("descript-vs-capcut","Descript vs CapCut","Descript","CapCut","video"),
 ("perplexity-vs-chatgpt","Perplexity vs ChatGPT","Perplexity","ChatGPT","assistants"),
 ("gamma-vs-beautiful-ai","Gamma vs Beautiful.ai","Gamma","Beautiful.ai","presentations"),
 ("researchrabbit-vs-elicit","ResearchRabbit vs Elicit","ResearchRabbit","Elicit","research"),
]
FREE_ALT_FOR += ["Pika","InVideo","Writesonic","Surfer","Krea","Notion AI","Claude","ClickUp","Fathom","Zapier","Warp","Qodo","Lindy"]

# Browser-verified 2026-10-15 (official pricing pages)
_BV = {
 "Otter": dict(price="List prices: Pro $16.99/user/mo ($8.33/mo yearly); Business $30/user/mo ($19.99/mo yearly). Promotional (first-time subscribers): Pro $8.49/mo monthly or $4.17/mo yearly (save 50%); Business $24/user/mo for 3 months (20% off) (checked 2026-10-21)"),
 "ChatGPT": dict(price="Go $8/mo; Plus $20/mo; Pro from $100/mo (3 tiers); Business $25/seat/mo ($20 billed annually); monthly billing (checked 2026-10-24)", free="Free: $0 (unlimited text chats on GPT-6, limits on tools)"),
 "Perplexity": dict(price="Pro $17/mo billed annually; Max $167/mo billed annually; monthly prices not shown (checked 2026-10-24)", free="Free tier available"),
 "Gamma": dict(price="Plus $12/mo ($9/mo yearly, $108/yr); Pro $25 ($18, $216/yr); Ultra $100 ($90, $1,080/yr); per seat (checked 2026-10-24)", free="Free plan available"),
 "Canva": dict(price="Pro $18/mo or $144/yr; Business $25/mo or $250/yr per person (checked 2026-10-24)", free="Free plan available"),
 "Kling AI": dict(pricing="https://kling.ai/app/membership/membership-plan", price="List prices: Standard $10/mo ($79.20/yr); Pro $37/mo ($293.04/yr); Premier $207/mo ($1,490/yr); Ultra+ $619/mo ($4,457/yr). Promotional: Standard $6.99 first month then $8.8/mo; Pro $25.99 first month then $32.56/mo; Premier $135 first month then $181.99/mo; Ultra+ $402 first month then $544.99/mo (checked 2026-10-17)", free="Basic: free", about="Text/image-to-video generator."),
}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _BV: _t.update(_BV[_t["name"]])
PRICE_TABLE.update({"ChatGPT":(8,None,None),"Perplexity":(None,17,None),"Gamma":(12,9,None),"Canva":(18,12,None),"Kling AI":(10,6.60,None)})

# Browser-verified 2026-10-15, batch 2 (official pages)
_BV2 = {
 "Captions": dict(price="Max $24.99/mo; Frontier $69.99/mo (iOS prices per page footnote)", free="Free plan available"),
 "Jasper": dict(price="Pro $69/seat/mo ($59/seat/mo billed yearly) (checked 2026-10-23)", free="No free plan; 7-day free trial"),
 "Lovable": dict(price="Pro $25/mo ($21/mo billed annually); Business $50/mo ($42 annually)", free="Free: $0 (5 build credits/day, up to 30/mo)"),
 "Qodo": dict(price="Credit-based: $0.012 per credit (packs of 2,500, 5,000, 20,000)", free="No free plan; 14-day trial"),
 "Recraft": dict(price="Basic $10/mo billed annually ($120/yr); Pro $16/mo annually ($192/yr); Teams $18/seat annually", free="Free plan (images not licensed for commercial use)"),
 "Magnific": dict(price="Premium $20/mo ($14.50 annually); Premium+ $45 ($33.75); Pro Starter $110 ($82.50)", free="No free plan shown", about="Formerly Freepik AI: AI image/video generation and upscaling."),
 "Photoroom": dict(price="Pro $7.50/mo billed yearly (list $12.99); Max $20.99 (list $34.99); Ultra $82.50 (list $99)", free="No free plan; trial available"),
 "Murf": dict(price="Studio: Creator $19/mo ($228 billed annually); Business $66/mo ($792 annually). API from $0.01/1,000 chars", free="Free: 10 minutes of voice generation"),
 "Udio": dict(price="Standard $10/mo ($8 annually); Pro $30/mo ($24 annually)", free="Free: 100 credits/mo"),
 "Microsoft Copilot": dict(price="Copilot Pro appears discontinued; Microsoft 365 Personal $9.99/mo; Microsoft 365 Premium $19.99/mo ($199.99/yr)", free="Free Copilot available", about="Microsoft's assistant; paid AI features come with Microsoft 365 plans."),
 "Elicit": dict(price="Pro $49/user/mo billed annually; Scale $169/user/mo annually", free="Basic: free"),
 "Consensus": dict(price="Pro $20/mo ($12/mo annually); higher plan $65/mo ($45 annually)", free="Free plan available"),
 "SciSpace": dict(price="Premium from $12/mo billed yearly (monthly price: check site)", free="No free plan shown"),
 "Humata": dict(price="Expert $9.99/mo; Team $49/user/mo", free="Free: 60 pages/mo"),
 "You.com API": dict(price="API only: Search $5 per 1,000 calls", free="$100 free API credit", about="Search and research APIs for building AI apps (consumer plan pricing not listed)."),
 "Scholarcy": dict(price="$9.99/month (1-week trial)", free="Free Article Summarizer (limited, 1 summary/day)"),
 "Reclaim": dict(price="Starter $12/seat/mo ($10 yearly); Business $18 ($15 yearly)", free="Lite: free forever"),
 "Chatbase": dict(price="Hobby $32/mo; Standard $120/mo; Pro $400/mo (billed yearly)", free="No free plan; 7-day trial"),
 "Relevance AI": dict(price="Enterprise only (custom pricing)", free="No free plan shown"),
}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _BV2: _t.update(_BV2[_t["name"]])
PRICE_TABLE.update({"Captions":(24.99,None,None),"Jasper":(69,59,None),"Lovable":(25,21,None),"Qodo":(None,None,"$0.012 per credit"),"Recraft":(None,10,None),
 "Magnific":(20,14.50,None),"Photoroom":(12.99,7.50,None),"Murf":(None,19,"API $0.01-$0.03 per 1,000 characters"),"Udio":(10,8,None),"Microsoft Copilot":(9.99,None,None),
 "Elicit":(None,49,None),"Consensus":(20,12,None),"SciSpace":(None,12,None),"Humata":(9.99,None,"Extra pages $0.01-$0.02/page"),"Scholarcy":(9.99,None,None),
 "Reclaim":(12,10,None),"Chatbase":(None,32,None),"Relevance AI":(None,None,None)})

# Elicit, browser-checked 2026-10-15
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] == "Elicit":
            _t["price"] = "Industry: Pro $75/mo ($49/mo yearly, $588/yr); Scale $279/mo ($169 yearly, $2,028/yr). Academic: Plus from $11/mo yearly ($19 monthly); Pro $69 ($39); Scale $149 ($89)"
            _t["free"] = "Basic: free"
PRICE_TABLE["Elicit"] = (75, 49, None)

# Per-tool checked dates (default CHECKED)
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _BV or _t["name"] in _BV2 or _t["name"] == "Elicit": _t["checked"] = "2026-10-15"
        if _t["name"] == "Kling AI": _t["checked"] = "2026-10-17"
        if _t["name"] == "ElevenLabs":
            _t["price"] = "List prices: Starter $6/mo; Creator $22/mo; Pro $99/mo; Scale $299/mo; Business $990/mo. Promotional: Starter $1 first month (83% off, until Oct 18); Creator $11 first month (50% off)"

# Old URL -> new URL (renamed/removed pages); build.py writes redirect stubs
REDIRECTS = {
 "/tools/freepik-ai.html": "/tools/magnific.html",
 "/free-alternative-to-freepik-ai.html": "/free-alternative-to-magnific.html",
}

COMPARISONS += [
 ("chatgpt-vs-claude","ChatGPT vs Claude","ChatGPT","Claude","assistants"),
 ("chatgpt-vs-gemini","ChatGPT vs Gemini","ChatGPT","Google Gemini","assistants"),
 ("claude-vs-gemini","Claude vs Gemini","Claude","Google Gemini","assistants"),
 ("chatgpt-vs-le-chat","ChatGPT vs Le Chat (Mistral)","ChatGPT","Le Chat (Mistral)","assistants"),
 ("jasper-vs-copy-ai","Jasper vs Copy.ai","Jasper","Copy.ai","marketing"),
 ("lovable-vs-bolt","Lovable vs Bolt","Lovable","Bolt","coding"),
 ("lovable-vs-v0","Lovable vs v0","Lovable","v0","coding"),
 ("bolt-vs-v0","Bolt vs v0","Bolt","v0","coding"),
 ("github-copilot-vs-windsurf","GitHub Copilot vs Windsurf","GitHub Copilot","Windsurf","coding"),
 ("canva-vs-gamma","Canva vs Gamma","Canva","Gamma","presentations"),
 ("gamma-vs-pitch","Gamma vs Pitch","Gamma","Pitch","presentations"),
 ("perplexity-vs-consensus","Perplexity vs Consensus","Perplexity","Consensus","research"),
 ("elicit-vs-consensus","Elicit vs Consensus","Elicit","Consensus","research"),
 ("notion-ai-vs-clickup","Notion AI vs ClickUp","Notion AI","ClickUp","productivity"),
 ("motion-vs-reclaim","Motion vs Reclaim","Motion","Reclaim","productivity"),
 ("fathom-vs-fireflies","Fathom vs Fireflies","Fathom","Fireflies","productivity"),
 ("zapier-vs-n8n","Zapier vs n8n","Zapier Agents","n8n","agents"),
 ("lindy-vs-zapier","Lindy vs Zapier Agents","Lindy","Zapier Agents","agents"),
 ("suno-vs-udio","Suno vs Udio","Suno","Udio","audio"),
 ("elevenlabs-vs-speechify","ElevenLabs vs Speechify","ElevenLabs","Speechify","audio"),
 ("descript-vs-riverside","Descript vs Riverside","Descript","Riverside","audio"),
 ("runway-vs-pika","Runway vs Pika","Runway","Pika","video"),
 ("runway-vs-luma","Runway vs Luma Dream Machine","Runway","Luma Dream Machine","video"),
 ("kling-vs-pika","Kling vs Pika","Kling AI","Pika","video"),
 ("captions-vs-opus-clip","Captions vs Opus Clip","Captions","Opus Clip","video"),
 ("leonardo-vs-ideogram","Leonardo vs Ideogram","Leonardo","Ideogram","images"),
 ("midjourney-vs-krea","Midjourney vs Krea","Midjourney","Krea","images"),
 ("grammarly-vs-wordtune","Grammarly vs Wordtune","Grammarly","Wordtune","writing"),
 ("surfer-vs-writesonic","Surfer vs Writesonic","Surfer","Writesonic","marketing"),
 ("buffer-vs-ocoya","Buffer vs Ocoya","Buffer","Ocoya","marketing"),
]

# v7: more high-intent comparisons (verified tools only)
COMPARISONS += [
 ("chatgpt-vs-perplexity-vs-claude","ChatGPT vs Perplexity vs Claude",["ChatGPT","Perplexity","Claude"],None,"assistants"),
 ("chatgpt-vs-microsoft-copilot","ChatGPT vs Microsoft Copilot","ChatGPT","Microsoft Copilot","assistants"),
 ("gemini-vs-microsoft-copilot","Google Gemini vs Microsoft Copilot","Google Gemini","Microsoft Copilot","assistants"),
 ("perplexity-vs-gemini","Perplexity vs Google Gemini","Perplexity","Google Gemini","assistants"),
 ("cursor-vs-github-copilot-vs-windsurf","Cursor vs GitHub Copilot vs Windsurf",["Cursor","GitHub Copilot","Windsurf"],None,"coding"),
 ("cursor-vs-lovable","Cursor vs Lovable","Cursor","Lovable","coding"),
 ("warp-vs-cursor","Warp vs Cursor","Warp","Cursor","coding"),
 ("heygen-vs-captions","HeyGen vs Captions","HeyGen","Captions","video"),
 ("capcut-vs-invideo","CapCut vs InVideo","CapCut","InVideo","video"),
 ("synthesia-vs-invideo","Synthesia vs InVideo","Synthesia","InVideo","video"),
 ("elevenlabs-vs-murf-vs-speechify","ElevenLabs vs Murf vs Speechify",["ElevenLabs","Murf","Speechify"],None,"audio"),
 ("otter-vs-fathom","Otter vs Fathom","Otter","Fathom","productivity"),
 ("canva-vs-recraft","Canva vs Recraft","Canva","Recraft","images"),
 ("ideogram-vs-recraft","Ideogram vs Recraft","Ideogram","Recraft","images"),
 ("rytr-vs-copy-ai","Rytr vs Copy.ai","Rytr","Copy.ai","writing"),
 ("botpress-vs-voiceflow","Botpress vs Voiceflow","Botpress","Voiceflow","agents"),
]

# Weekly price pass 2026-10-19 (official pricing pages; static HTML or rendered page text)
CATEGORIES[2]["tools"].append(T("Replit","https://replit.com","https://replit.com/pricing","Core $20/mo ($18/mo billed annually); Pro $100/mo ($90/mo billed annually); Enterprise custom",CK,"Build and deploy apps by describing them to Replit's AI agent, all in the browser."))
_W1019 = {
 "ElevenLabs": dict(price="Starter $6/mo ($5/mo billed yearly); Creator $22 ($18.33); Pro $99 ($82.50); Scale $299 ($249.17); Business $990 ($825). Promotional: Starter $1 first month (until Nov 1), Creator $11 first month (50% off) (checked 2026-10-26)"),
 "Rytr": dict(price="Lite $9/mo; Personal $19/mo; Pro $49/mo (monthly prices; yearly billing saves 20%)", free="Free forever: 10,000 characters/mo", about="AI writing in your own voice, plus relationship and follow-up tools."),
 "Qodo": dict(price="Pro Team $30 (up to 30 users); credit packs at $0.012/credit (2,500, 5,000 or 20,000 credits)", free="14-day free trial, no card; free for open source projects"),
 "Surfer": dict(price="Discovery $49/mo; AI Search Analytics $82/mo; Standard $99/mo; Pro $182/mo; Peace of Mind $299/mo (all billed yearly)"),
 "n8n": dict(price="Starter $20/mo; Pro $50/mo; Business $800/mo (billed annually, USD)"),
}
PRICE_TABLE.update({"ElevenLabs":(6,5,None),"Rytr":(9,None,None),"Qodo":(30,None,"$0.012 per credit"),"Surfer":(None,49,None),"n8n":(None,20,None),"Replit":(20,18,None)})
_V1019 = {"Runway","Pika","Luma Dream Machine","HeyGen","InVideo","Opus Clip","Captions","Claude","Claude (Pro)","Grammarly","Notion AI","Copy.ai","Jasper","Wordtune",
 "GitHub Copilot","Cursor","Windsurf","Bolt","v0","Warp","Krea","Suno","Speechify","Riverside","Krisp","Pitch","Beautiful.ai","Plus AI","SlidesAI","Le Chat (Mistral)",
 "Writesonic","Frase","Predis.ai","Ocoya","Scite","You.com API","ResearchRabbit","Fireflies","Fathom","Reclaim","ClickUp","Taskade","Superhuman","Zapier","Zapier Agents",
 "Botpress","Chatbase","Lindy","Descript","Magnific","Otter","Buffer","Humata","Midjourney","Ideogram","Udio","SciSpace","Motion","Replit"} | set(_W1019)
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _W1019: _t.update(_W1019[_t["name"]])
        _t["checked"] = "2026-10-19" if _t["name"] in _V1019 else _t.get("checked", "2026-10-14")
# Daily ops 2026-10-23: monthly-billing prices re-read on official pricing pages.
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in ("Grammarly","Notion AI","Jasper"): _t["checked"] = "2026-10-23"
COMPARISONS += [
 ("replit-vs-lovable","Replit vs Lovable","Replit","Lovable","coding"),
 ("replit-vs-bolt","Replit vs Bolt","Replit","Bolt","coding"),
 ("replit-vs-cursor","Replit vs Cursor","Replit","Cursor","coding"),
]
FREE_ALT_FOR += [n for n in ["Replit","ElevenLabs","Surfer","n8n","Otter"] if n not in FREE_ALT_FOR]

# Price-change notes for /price-changes.html (build.py diffs price_history.json snapshots automatically).
# Key "YYYY-MM-DD|Tool" = snapshot date the change was first recorded. Value = (tag, plain-English summary).
# Tags: up, down, newplan, correction, currency, changed. Un-noted diffs still appear with an automatic tag/summary.
# Every note must restate only the documented before/after text in price_history.json (and git history).
PRICE_NOTES = {
 "2026-10-17|Kling AI": ("correction", "We corrected Kling AI's top plans: Premier is $207/mo and Ultra+ is $619/mo. We had listed Premier at $92/mo and Ultra at $180/mo."),
 "2026-10-19|ElevenLabs": ("up", "ElevenLabs' $1 first-month Starter offer has ended. Starter is now $6/mo, or $5/mo billed yearly."),
 "2026-10-19|Rytr": ("up", "Rytr's top plan is now $49/mo (Pro), with Lite at $9/mo and Personal at $19/mo. Before, it listed $7.50/mo and $24.16/mo for multiple brands."),
 "2026-10-19|Qodo": ("newplan", "Qodo now has a Pro Team plan at $30 (up to 30 users). Before, it only sold credit packs at $0.012 per credit."),
 "2026-10-19|Surfer": ("newplan", "Surfer now has a Discovery plan at $49/mo billed yearly. Before, its cheapest listed plan was $82/mo billed yearly."),
 "2026-10-19|n8n": ("currency", "n8n now shows US dollar prices: Starter $20/mo, Pro $50/mo, Business $800/mo, billed yearly. Before, we listed euro prices (€20, €50, €667), so this is not a like-for-like price change."),
 "2026-10-22|Bolt": ("changed", "Bolt's monthly prices are unchanged (Pro $25/mo, Teams $30/member/mo). We now also show the yearly prices: Pro $18/mo ($216/yr) and Teams $27/member/mo."),
 "2026-10-22|Krea": ("newplan", "Krea now has a Basic plan at $9/mo (5,000 units a month). Before, its cheapest paid plan was Pro at $35/mo."),
 "2026-10-23|Grammarly": ("correction", "Grammarly Pro is $30/mo billed monthly. The $12/mo we showed before is the yearly price ($144/yr); a quarterly plan is $60."),
 "2026-10-23|Notion AI": ("correction", "Notion billed monthly is Plus $12/member/mo and Business $24/member/mo. The $10 and $20 we showed before are the yearly-billing prices."),
 "2026-10-23|Jasper": ("correction", "Jasper Pro is $69/seat/mo billed monthly, or $59/seat/mo billed yearly. Before, we only showed the $59 yearly price."),
 "2026-10-21|Otter": ("changed", "Otter's list prices are unchanged (Pro $16.99/user/mo, Business $30/user/mo). New: a first-time-subscriber offer, Pro at $8.49/mo monthly or $4.17/mo yearly (50% off) and Business at $24/user/mo for 3 months (20% off)."),
}
# Snapshot diffs known to be artifacts, not real changes (never shown).
PRICE_SKIP = {
 "2026-10-15|Kling AI": "The 2026-10-14 snapshot was rewritten with text from the 2026-10-17 check, so this diff runs backwards in time.",
 "2026-10-21|Microsoft Copilot": "Wording-only rewrite from the 2026-10-20 tier-matching update; prices unchanged.",
 "2026-10-21|Google Gemini": "Wording-only rewrite from the 2026-10-20 tier-matching update; prices unchanged.",
}

# --- v24-fix: merge the "Claude (Pro)" duplicate into Claude (same product, same pricing page) ---
_claude = next(t for c in CATEGORIES for t in c["tools"] if t["name"] == "Claude")
for _c in CATEGORIES:
    _c["tools"] = [(_claude if t["name"] == "Claude (Pro)" else t) for t in _c["tools"]]
    _c["free"] = [("Claude" if n == "Claude (Pro)" else n) for n in _c["free"]]
    if _c.get("best") == "Claude (Pro)": _c["best"] = "Claude"
PRICE_TABLE.pop("Claude (Pro)", None)
REDIRECTS["/tools/claude-pro.html"] = "/tools/claude.html"

# --- v24-fix: short plan list for tool pages (same verified 2026-10-17 Kling list prices; yearly totals / 12) ---
PLANS_SHORT = {
 "Kling AI": "Standard $10/mo ($6.60/mo billed yearly) · Pro $37/mo ($24.42) · Premier $207/mo ($124.17) · Ultra+ $619/mo ($371.42). First-month discounts are offered on every plan — see the official page.",
}

# --- v24-fix: capability tags. FIRST tag = the tool's PRIMARY capability (what "same job" means sitewide).
# Each tag comes only from what the tool's own site says (homepage title/description fetched 2026-10-20,
# or, where the homepage blocked our fetch, the tool's own docs/help pages on its domain, re-checked 2026-10-20). All 82 confirmed; none rely on a saved description.
CAPS = {
 "Runway": ["video-generation", "image-generation"],          # runwayml.com: text/image-to-video (Gen-4.5) plus image models
 "Pika": ["video-generation"],                                 # pika.art: AI video clips from text or images
 "Luma Dream Machine": ["video-generation", "image-generation"],# lumalabs.ai: "platform for video generation and image creation"
 "Kling AI": ["video-generation", "image-generation"],         # klingai.com: "AI Video & Image Generator"
 "HeyGen": ["avatar-video", "voice-cloning"],                  # heygen.com: "AI videos with your Personal Avatar — your face and voice"
 "Synthesia": ["avatar-video"],                                # synthesia.io: AI video platform with AI presenters for business/training
 "Descript": ["edit-by-transcript", "video-editing", "transcription", "podcast-recording"],  # descript.com: "editing as easy as editing text. Record, transcribe, edit"
 "CapCut": ["video-editing"],                                  # capcut.com: "AI Video Editor"
 "InVideo": ["video-generation", "video-editing"],             # invideo.io: "Create & edit AI videos"
 "Opus Clip": ["video-clipping", "video-editing"],             # opus.pro: "turns long videos into ... viral clips"
 "Captions": ["video-editing", "video-generation"],            # captions.ai: "AI video generator and editor"
 "Claude": ["general-chatbot", "writing-assistant", "code-assistant"],  # anthropic.com/claude (fetched 2026-10-20): "the AI assistant for work"; "reasoning, coding, and writing"; Claude Code writes code
 "ChatGPT": ["general-chatbot", "writing-assistant", "image-generation", "code-assistant"],  # chatgpt.com: "answer questions, write, create images ... and code"
 "Google Gemini": ["general-chatbot"],                         # gemini.google.com: "Google's AI assistant ... writing, planning, brainstorming"
 "Grammarly": ["writing-assistant"],                           # grammarly.com: "AI Writing Assistance"
 "Notion AI": ["docs-workspace", "ai-agents"],                 # notion.com: "The AI workspace" with custom agents
 "Copy.ai": ["gtm-automation", "marketing-copy"],              # copy.ai: "GTM AI platform"
 "Jasper": ["marketing-content", "ai-agents"],                 # jasper.ai: AI agents for marketing workflows
 "Wordtune": ["writing-assistant"],                            # wordtune.com: "AI writer that can paraphrase, rewrite, correct your grammar"
 "Rytr": ["writing-assistant", "follow-up-assistant"],         # rytr.me: drafts follow-ups "in your voice"; now pitches itself as an AI relationship manager
 "GitHub Copilot": ["code-assistant"],                         # github.com/features/copilot: "Your AI coding agent" in editor/terminal/GitHub
 "Cursor": ["code-assistant"],                                 # cursor.com: "AI Coding Agent"
 "Windsurf": ["code-assistant"],                               # windsurf.com (now Devin Desktop): local/cloud coding agents in your editor
 "Bolt": ["app-builder", "website-builder"],                   # bolt.new: "AI builder: Websites, apps & prototypes"
 "v0": ["app-builder", "website-builder"],                     # v0.app: "Build Full-Stack Web Apps with AI"
 "Lovable": ["app-builder", "website-builder"],                # docs.lovable.dev (fetched 2026-10-20): "full-stack AI development platform for building ... web applications using natural language"
 "Warp": ["code-assistant"],                                   # warp.dev: agentic software development platform / AI terminal
 "Qodo": ["code-review"],                                      # qodo.ai: "AI Code Review"
 "Replit": ["app-builder", "website-builder"],                 # docs.replit.com/features/agent (2026-10-20): Agent "turns your ideas into apps"; Design for "polished websites"
 "Leonardo": ["image-generation"],                             # docs.leonardo.ai (fetched 2026-10-20): "generating your first images" with the Leonardo.Ai API
 "Midjourney": ["image-generation"],                           # docs.midjourney.com Getting Started (2026-10-20): "transforming text into amazing images and videos"
 "Ideogram": ["image-generation", "logo-design"],              # docs.ideogram.ai (fetched 2026-10-20): "create and edit AI images and videos ... text and logo workflows"
 "Krea": ["image-generation"],                                 # krea.ai (fetched 2026-10-20): "Generate, edit, and enhance images and videos"
 "Canva": ["graphic-design", "logo-design", "presentations", "image-generation"],  # canva.com: "create social media posts, presentations, posters, videos, logos"
 "Recraft": ["image-generation", "vector-design"],             # recraft.ai: "text-to-image model and design platform ... vector generation"
 "Magnific": ["image-generation", "image-upscaling"],          # magnific.com/ai and /ai/docs/image-upscaler (2026-10-20): Image Generator, Image Editor, Image Upscaler up to 16x
 "Photoroom": ["photo-editing"],                               # photoroom.com: "AI-Powered Photo Editor" for product photos
 "ElevenLabs": ["text-to-speech", "voice-cloning", "voice-agents"],  # elevenlabs.io: "AI Voice Generator & Voice Agents"
 "Suno": ["music-generation"],                                 # suno.com: "AI Music Generator"
 "Murf": ["text-to-speech", "voice-agents"],                   # murf.ai: "Generate human-like speech and deploy conversational agents"
 "Speechify": ["text-to-speech"],                              # speechify.com: "Text to Speech ... reads anything aloud"
 "Otter": ["meeting-notes", "transcription"],                  # otter.ai: "AI Notetaker, Transcription"
 "Udio": ["music-generation"],                                 # udio.com: "AI Music Generator"
 "Riverside": ["podcast-recording", "video-editing"],          # riverside.com: "podcast and video recording and editing"
 "Krisp": ["noise-cancellation", "meeting-notes"],             # krisp.ai: "Noise Cancellation & AI Note Taker"
 "Pitch": ["presentations"],                                   # pitch.com: "AI presentation workspace"
 "Beautiful.ai": ["presentations"],                            # beautiful.ai: "AI Presentation Software"
 "Plus AI": ["presentations"],                                 # plusai.com: AI presentation maker for PowerPoint and Slides
 "SlidesAI": ["presentations"],                                # slidesai.io: turn text into presentations
 "Gamma": ["presentations", "website-builder"],                # gamma.app: "creating effortless presentations, websites, and more"
 "Le Chat (Mistral)": ["general-chatbot", "code-assistant"],                     # mistral.ai/products/le-chat (fetched 2026-10-20): "Mistral Vibe (formerly Le Chat) - AI chat and coding agent"
 "Perplexity": ["answer-engine", "general-chatbot"],           # perplexity.ai help center (2026-10-20): "answers your questions with cited sources"; "an answer engine"
 "Microsoft Copilot": ["general-chatbot"],                     # copilot.microsoft.com: "AI chat that works across your day"
 "Buffer": ["social-scheduling"],                              # buffer.com: social media management
 "Surfer": ["seo-content"],                                    # surferseo.com: brand visibility across Google and AI search
 "Writesonic": ["seo-content"],                                # writesonic.com: "AI Search Growth Engine" (GEO/AEO)
 "Frase": ["seo-content"],                                     # frase.io: "SEO & GEO Content Platform"
 "Predis.ai": ["ad-creative", "social-content"],               # predis.ai: "AI Ad Generator"
 "Ocoya": ["social-scheduling", "social-content"],             # ocoya.com: social media scheduling and content creation
 "Elicit": ["research-assistant"],                             # elicit.com: "AI for research & decision-making"
 "Scite": ["citation-check", "paper-search"],                  # scite.ai: citation-backed answers, supported or disputed
 "Consensus": ["paper-search"],                                # consensus.app: "AI academic search engine for peer-reviewed literature"
 "SciSpace": ["paper-reader", "paper-search"],                 # scispace.com/pricing FAQ (2026-10-20): "discovering, analyzing, and writing scientific literature"; Literature Review, Chat with PDF
 "Humata": ["doc-chat"],                                       # humata.ai: turns your documents into an AI knowledge base
 "You.com API": ["search-api"],                                # you.com: "Web Search APIs for AI"
 "ResearchRabbit": ["literature-mapping", "paper-search"],      # researchrabbit.ai: related papers, citation maps
 "Scholarcy": ["paper-summaries"],                             # scholarcy.com: "Summarize anything, understand complex research"
 "Fireflies": ["meeting-notes", "transcription"],              # fireflies.ai (2026-10-20): "AI Note Taker to Transcribe, Summarize, Analyze Meetings"
 "Fathom": ["meeting-notes", "transcription"],                 # fathom.ai: "captures, transcribes, and summarizes" calls
 "Motion": ["ai-calendar", "project-management"],              # usemotion.com: AI calendar, projects, tasks
 "Reclaim": ["ai-calendar"],                                   # reclaim.ai: "AI Calendar"
 "ClickUp": ["project-management"],                            # clickup.com: tasks, docs, goals, chat
 "Taskade": ["ai-agents", "project-management"],               # taskade.com: AI apps, agents and workflows
 "Superhuman": ["productivity-suite", "writing-assistant"],    # superhuman.com: "Docs, Mail, and AI" (includes Grammarly)
 "Zapier": ["workflow-automation", "ai-agents"],               # zapier.com: "Automate AI Workflows, Agents, and Apps"
 "Zapier Agents": ["ai-agents", "workflow-automation"],        # zapier.com: AI agents across 9,000+ apps
 "n8n": ["workflow-automation", "ai-agents"],                  # n8n.io: "AI Workflow Automation Platform"
 "Botpress": ["support-chatbot", "ai-agents"],                 # botpress.com: AI agent platform for customer support
 "Chatbase": ["support-chatbot", "ai-agents"],                 # chatbase.co: AI agents for customer support
 "Lindy": ["ai-agents"],                                       # lindy.ai: "AI employee that connects to all your tools"
 "Relevance AI": ["ai-agents"],                                # relevanceai.com: specialist AI agents
 "Voiceflow": ["support-chatbot", "ai-agents"],                # voiceflow.com: chat and voice AI agents for customer support
}
CAP_LABEL = {k: k.replace("-", " ") for v in CAPS.values() for k in v}
CAP_LABEL.update({"edit-by-transcript": "edit by transcript", "text-to-speech": "text to speech", "general-chatbot": "general AI chatbot", "code-assistant": "AI coding assistant", "app-builder": "app builder", "website-builder": "website builder", "ai-agents": "AI agents", "gtm-automation": "go-to-market automation", "seo-content": "SEO content", "ai-calendar": "AI calendar"})
# Entry plans that are a LOWER tier than the usual paid plan (from the plan names on the official pricing pages):
LOWER_TIER = {
 "Google Gemini": "$4.99/mo is Google's entry AI tier, below its $19.99/mo Pro tier",
 "ChatGPT": "$8/mo is the Go tier, below the $20/mo Plus tier",
}

# v31 (2026-10-20): Google Gemini re-verified on https://one.google.com/about/google-ai-plans/ (region shown: "United States"):
# "Google AI Plus $4.99/mo" · "Google AI Pro $19.99/mo" · "Google AI Ultra 5x $99.99/mo" · "Google AI Ultra 20x $199.99/mo".
# Plan table: Plus has "Higher Usage Limits 2x*" and Gemini 3.6 Flash; Pro has "Access to Gemini 4 Argon" (frontier model), 4x limits, 1M context.
# FAQ: "The Google AI Premium plan has a new name: Google AI Plus." -> old pricing URL /about/ai-premium replaced.
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] == "Google Gemini":
            _t["pricing"] = "https://one.google.com/about/google-ai-plans/"
            _t["price"] = "Google AI Plus $4.99/mo (Flash model, lighter tier); Google AI Pro $19.99/mo; Ultra from $99.99/mo (US prices)"
            _t["checked"] = "2026-10-20"
LOWER_TIER["Google Gemini"] = "$4.99/mo is Google AI Plus, a lighter tier below Google AI Pro ($19.99/mo)"
# Like-for-like matching tier: when a lower-tier entry plan is compared with a tool whose entry plan is a full tier
# (e.g. Claude Pro), we compare that tool's comparable full tier instead (monthly price from the same official page).
TIER_MATCH = {"Google Gemini": ("Google AI Pro", 19.99), "ChatGPT": ("Plus", 20)}
# Microsoft Copilot: our saved checked entry ($9.99) is Microsoft 365 Personal, a bundle tier below Microsoft 365 Premium
# ($19.99/mo, same saved check). Treated like the other lower tiers so it is not ranked against Claude Pro-class plans.
LOWER_TIER["Microsoft Copilot"] = "$9.99/mo is Microsoft 365 Personal, below Microsoft 365 Premium ($19.99/mo)"
TIER_MATCH["Microsoft Copilot"] = ("Microsoft 365 Premium", 19.99)

# v32 (2026-10-20): Microsoft Copilot re-verified on https://www.microsoft.com/en-us/microsoft-365/buy/compare-all-microsoft-365-products (en-us):
# "Microsoft 365 Personal $9.99/month $99.99/year" · "Microsoft 365 Family $12.99/month $129.99/year" ·
# "Microsoft 365 Premium $19.99/month $199.99/year Everything in Microsoft 365 Family, plus: Advanced Copilot chat ...".
# Copilot Pro: Microsoft blog 2025-10-01 (microsoft.com/en-us/copilot/blog/2025/10/01/meet-microsoft-365-premium-your-ai-and-productivity-powerhouse/):
# "we'll no longer sell Copilot Pro -- Copilot Pro subscribers can switch to Microsoft 365 Premium". Prices unchanged vs saved data.
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] == "Microsoft Copilot":
            _t["pricing"] = "https://www.microsoft.com/en-us/microsoft-365/buy/compare-all-microsoft-365-products"
            _t["price"] = "Copilot Pro no longer sold; Microsoft 365 Personal $9.99/mo ($99.99/yr); Microsoft 365 Premium $19.99/mo ($199.99/yr), advanced Copilot (US prices)"
            _t["checked"] = "2026-10-20"

# v37 (2026-10-20): AI video credit costs, copied from each official pricing page (monthly billing; credits per month).
# Runway https://runwayml.com/pricing : "Standard $15 ... 625 credits /mo"; "Pro $35 ... 2250 credits /mo"; "Max $95 ... 9500 credits /mo";
#   "Gen-4.5 60 credits/5s"; FAQ "Gen-4.5 uses 12 credits per second"; "Seedance 2.0 Pro 1080p 160 credits/4s"; "Seedance 2.0 Fast 116 credits/4s";
#   "minimum purchase is 1,000 credits" (top-up price not shown). Free: "125 one-time credits".
# Pika https://pika.art/pricing : "Starter 900 credits / month $10"; "Creator 3,150 credits / month $35"; "Fancy 8,550 credits / month $95";
#   "Seedance 2.5 Video · 720p · 5s 122"; "Wan 3.0 Video · 720p · 5s 33"; "One-time top up 60 credits per $1"; Free "0 credits / month · packs only".
# Luma https://lumalabs.ai/pricing : "Plus $30 /month ... 10,000 credits"; "Pro $90 /month ... 40,000 credits"; "Ultra $300 /month ... 150,000 credits";
#   Ray3.14 Text-to-Video "720p - 20 credits/sec", "1080p - 80 credits/sec"; Seedance 2.5 "720p Yes 78 credits/sec"; Kling 3.0 "720p - 30 credits/sec".
VIDEO_CHECKED = "2026-10-20"
VIDEO_CREDITS = {
 "Runway": dict(pricing="https://runwayml.com/pricing", free="125 one-time credits",
   plans=[("Standard",15,625),("Pro",35,2250),("Max",95,9500)], topup=None, topup_note="extra credits from 1,000 (price not shown on the pricing page)",
   models=[("Gen-4.5","",12.0),("Seedance 2.0 Fast","",29.0),("Seedance 2.0 Pro","1080p",40.0)]),
 "Pika": dict(pricing="https://pika.art/pricing", free="0 credits a month (credit packs only)",
   plans=[("Starter",10,900),("Creator",35,3150),("Fancy",95,8550)], topup=60, topup_note="one-time top-ups at 60 credits per $1",
   models=[("Seedance 2.5","720p",24.4),("Wan 3.0","720p",6.6)]),
 "Luma Dream Machine": dict(pricing="https://lumalabs.ai/pricing", free="no free plan listed",
   plans=[("Plus",30,10000),("Pro",90,40000),("Ultra",300,150000)], topup=None, topup_note="no top-up price shown on the pricing page",
   models=[("Seedance 2.5","720p",78.0),("Ray3.14","720p",20.0),("Kling 3.0","720p",30.0),("Ray3.14","1080p",80.0)]),
}

# v38 (2026-10-20): AI voice (text-to-speech) costs, from each official pricing page (monthly billing).
# ElevenLabs https://elevenlabs.io/pricing FAQ: "Monthly price and included credits per plan: Free $0 (10,000 credits); Starter $6 (30,000 credits);
#   Creator $22 (121,000 credits, $11 for the first month); Pro $99 (600,000 credits); Scale $299 (1,800,000 credits, 3 seats); Business $990 (6,000,000 credits, 10 seats)";
#   "Text to Speech 1 credit per character"; plan table "Text to Speech (UI) Minutes included / Extra minute": ~10 / ~$0.36, ~30 / ~$0.20, ~121 / ~$0.18,
#   ~600 / ~$0.17, ~1,800 / ~$0.17, ~6,000 / ~$0.17 (Free, Starter, Creator, Pro, Scale, Business) -> ~1,000 characters per minute (ElevenLabs' own estimate).
# Runway https://runwayml.com/pricing : "Text to Speech 1 credit/50 chars"; Standard $15 625 credits/mo, Pro $35 2,250, Max $95 9,500; top-up price not shown.
# Luma https://lumalabs.ai/pricing : "ElevenLabs v3 text-to-speech 21 credits/1000 characters"; Plus $30 10,000 credits, Pro $90 40,000, Ultra $300 150,000.
# Left out: Murf (https://murf.ai/pricing shows API pay-as-you-go "$0.03 / 1000 characters", no monthly Studio quota shown);
#   Speechify (https://speechify.com/pricing/ is a read-aloud app: "Premium $29 /Month", no generation quota).
VOICE_CHECKED = "2026-10-20"
VOICE_CPM = 1000  # characters per minute, ElevenLabs' stated estimate (10,000 credits ~ 10 min)
VOICE_COSTS = {
 "ElevenLabs": dict(pricing="https://elevenlabs.io/pricing", free="10,000 credits a month (~10 min)", model="Eleven v3 / v4 (Studio)", same="ElevenLabs v3",
   plans=[("Starter",6,30000,0.20),("Creator",22,121000,0.18),("Pro",99,600000,0.17),("Scale",299,1800000,0.17),("Business",990,6000000,0.17)],
   note="Scale includes 3 seats and Business 10.", topup_note="extra minutes at the per-plan rate shown on the pricing page"),
 "Luma Dream Machine": dict(pricing="https://lumalabs.ai/pricing", free="no free plan listed", model="ElevenLabs v3", same="ElevenLabs v3",
   plans=[("Plus",30,int(10000/21*1000),None),("Pro",90,int(40000/21*1000),None),("Ultra",300,int(150000/21*1000),None)],
   note="Luma is a video tool; its credits are shared with video and images.", topup_note="no top-up price shown on the pricing page"),
 "Runway": dict(pricing="https://runwayml.com/pricing", free="125 one-time credits", model="Runway text to speech (model not named)", same=None,
   plans=[("Standard",15,625*50,None),("Pro",35,2250*50,None),("Max",95,9500*50,None)],
   note="Runway is a video tool; its credits are shared with video and images.", topup_note="extra credits from 1,000 (price not shown on the pricing page)"),
}
VOICE_LEFT_OUT = [("Murf","its pricing page shows only pay-as-you-go API rates ($0.03 per 1,000 characters), not a monthly plan quota"),
                  ("Speechify","it's a read-aloud app with unlimited listening, not a voice-generation quota"),
                  ("Descript","its plans count media minutes for editing and transcription, not a text-to-speech character quota")]

# v41 (2026-10-21): AI coding plan prices re-verified today on each official pricing page (monthly billing unless marked).
# Cursor https://cursor.com/pricing : "Free $0 /month", "Plus $8 /month ... *Only Grok models are available on this plan", "Premium Most popular $30 /month",
#   "Super $100 /month", "Ultra $200/month", "Teams $30+/user/month".
# GitHub Copilot https://github.com/features/copilot/plans : "Free $0", "Pro $10 per month", "Pro+ $39 per month", "Max $100 per month".
# Windsurf https://windsurf.com/pricing : "Free $0", "Pro POPULAR $20 PER MONTH", "Max NEW $200 PER MONTH", "Teams $80 /MONTH FOR TEAM PLAN + $40/MO PER FULL DEV SEAT".
# Claude https://claude.com/pricing : Pro "$17 Per month with annual subscription discount ($200 billed up front). $20 if billed monthly."; FAQ: Pro "includes Claude Code";
#   features table "Claude Code No Yes Yes Yes" (Free/Pro/Max 5x/Max 20x); Max "From $100".
# Warp https://www.warp.dev/pricing : "Free $0/mo", "Build Starts at $20/mo" ("$18 /month" annual plan), "$20 of agent usage included each month", "Max Starts at $200/mo".
# Left out: Replit (https://replit.com/pricing showed a Cloudflare "Performing security verification" page today, price not verifiable);
#   Qodo (https://www.qodo.ai/pricing/ is a team PR-review plan, "Pro Team" on credits at "$.012/credit", a different job and billing).
CODING_CHECKED = "2026-10-21"
CODING_V41 = [
 dict(n="Cursor", pr="https://cursor.com/pricing", free="Free $0 (limited AI usage)", entry=("Plus", 8, "only Grok models on this plan"), main=("Premium", 30, "most popular plan"), top=("Super", 100, ""), yearly=None),
 dict(n="GitHub Copilot", pr="https://github.com/features/copilot/plans", free="Free $0 (limited chat and agent usage)", entry=("Pro", 10, ""), main=("Pro+", 39, ""), top=("Max", 100, ""), yearly=None),
 dict(n="Windsurf", pr="https://windsurf.com/pricing", free="Free $0 (light agent quota, unlimited Tab completions)", entry=("Pro", 20, ""), main=("Pro", 20, ""), top=("Max", 200, ""), yearly=None),
 dict(n="Claude", label="Claude Code (Claude Pro)", pr="https://claude.com/pricing", free="Free plan $0, but no Claude Code", entry=("Pro", 20, "includes Claude Code"), main=("Pro", 20, "includes Claude Code"), top=("Max", 100, "from $100"), yearly=("Pro", 17)),
 dict(n="Warp", pr="https://www.warp.dev/pricing", free="Free $0", entry=("Build", 20, "includes $20 of agent usage a month"), main=("Build", 20, "includes $20 of agent usage a month"), top=("Max", 200, ""), yearly=("Build", 18)),
]
CODING_LEFT_OUT = [("Replit", "its pricing page showed a security check today, so we couldn't verify the price"),
                   ("Qodo", "it's a team code-review product billed in credits, a different job and billing")]

# v42 (2026-10-22): Free plan limits, side by side. Every value read today on the official pricing page in FREE_SRC; "not stated" = not on the page.
# Text tools have no watermark ("n/a (text)"). Quotes kept short in each cell; monthly step-up price read with the page's Monthly toggle.
FREE_CHECKED = "2026-10-22"
NS = "not stated"
FREE_LIMITS = [
 # name, includes, main limit, watermark, commercial use, cheapest paid step-up (monthly)
 ("Claude", "Chat on web, desktop and mobile; web search, files and code; memory; Artifacts", NS, "n/a (text)", NS, "Pro $20/mo"),
 ("Le Chat (Mistral)", "Web and mobile; basic image generation and editing; 100+ connectors", "“Limited messages and web searches”", "n/a (text)", NS, "Pro $14.99/mo (excl. tax)"),
 ("Cursor", "Limited AI usage, agent and chat requests", "“Limited agent requests” (no number stated)", "n/a (text)", NS, "Plus $8/mo (only Grok models)"),
 ("GitHub Copilot", "Entry-level models; community support", "2,000 completions per month", "n/a (text)", NS, "Pro $10/mo"),
 ("Lovable", "Unlimited collaborators; 5 lovable.app domains; invite-only publishing", NS, "Lovable badge (removal is a Pro feature)", NS, "Pro $25/mo"),
 ("Bolt", "Public and private projects; unlimited databases; website hosting", "1M tokens per month, with daily limits", "Bolt branding on websites", NS, NS),
 ("Grammarly", "Spelling and grammar checks; tone detection", "100 AI prompts", "n/a (text)", NS, NS),
 ("Notion AI", "Notion for individuals; basic forms and sites", "Notion AI is a trial only", "n/a (text)", NS, NS),
 ("Otter", "Live transcription for Zoom, Teams and Meet; AI chat; speaker identification", "300 transcription minutes a month; 3 lifetime file imports", "n/a (text)", NS, "Pro $16.99/user/mo"),
 ("Fathom", "Unlimited recordings; instant call summaries", NS, "n/a (text)", NS, "Premium $20/mo"),
 ("Canva", "1,000+ design types; 1.6M+ templates; 5GB storage", "Up to 20 Standard or Premium AI uses", "On Pro content only", "Yes, Free content in your designs (e.g. marketing, merchandise)", NS),
 ("Krea", "Selected models and features", "100 units a day", NS, "Not included (paid plans only, per pricing FAQ)", "Basic $9/mo"),
 ("Runway", "A selection of generative models; 5GB storage", "125 credits, one time only", "Yes, videos carry a Runway watermark", "Yes, on every plan including Free", "Standard $15/mo"),
 ("Pika", "All models; credit packs only", "0 credits a month (buy packs)", "No watermark", "No commercial license", "Starter $10/mo"),
 ("Kling AI", "Basic plan at $0", NS, NS, NS, "Standard $10/mo ($6.99 first month)"),
 ("HeyGen", "Avatar IV and Video Agent; 1 custom video avatar", "3 videos a month, up to 1 minute each", "Yes, watermarked", "No (personal, non-commercial use only, per terms)", "Creator $29/mo"),
 ("Descript", "Text-based editing; AI tools to try", "60 media minutes a month; 720p export", NS, NS, "Hobbyist $24/mo"),
 ("CapCut", "Free templates; basic editing tools", NS, NS, NS, "Pro $19.99/mo"),
 ("ElevenLabs", "Text to speech, speech to text, sound effects, voice design, music; 3 Studio projects", "10,000 credits a month", "n/a (audio)", "No (commercial license starts at Starter)", "Starter $6/mo"),
 ("Suno", "Free models; standard features; upload up to 8 min of audio", "50 credits a day; no monthly song downloads", NS, "No commercial rights", "Pro $10/mo"),
 ("Udio", "Basic features; up to 4 songs at once", "10 credits a day, 100 a month; 3 full-length songs a day", NS, NS, "Standard $10/mo"),
 ("Gamma", "Presentations, docs, websites, social and images; PDF/PPTX import and export", "400 credits at signup; up to 10 slides per prompt", "Gamma branding (removed on Plus)", NS, "Plus $12/mo"),
]
FREE_SRC = {"Claude": "https://claude.com/pricing", "Le Chat (Mistral)": "https://mistral.ai/pricing", "Cursor": "https://cursor.com/pricing", "GitHub Copilot": "https://github.com/features/copilot/plans",
 "Lovable": "https://lovable.dev/pricing", "Bolt": "https://bolt.new/pricing", "Grammarly": "https://www.grammarly.com/plans", "Notion AI": "https://www.notion.com/pricing", "Otter": "https://otter.ai/pricing",
 "Fathom": "https://www.fathom.ai/pricing", "Canva": "https://www.canva.com/pricing/", "Krea": "https://www.krea.ai/pricing", "Runway": "https://runwayml.com/pricing", "Pika": "https://pika.art/pricing",
 "Kling AI": "https://kling.ai/app/membership/membership-plan", "HeyGen": "https://www.heygen.com/pricing", "Descript": "https://www.descript.com/pricing", "CapCut": "https://www.capcut.com/pricing",
 "ElevenLabs": "https://elevenlabs.io/pricing", "Suno": "https://suno.com/pricing", "Udio": "https://www.udio.com/pricing", "Gamma": "https://gamma.app/pricing"}
FREE_BEST = {"coding": ("GitHub Copilot", "its free plan states a clear allowance: 2,000 completions a month"),
 "writing": ("Grammarly", "free spelling and grammar checks, plus 100 AI prompts"),
 "images": ("Krea", "100 units every day, rather than a one-time grant"),
 "video": ("Descript", "60 media minutes a month with 720p export"),
 "audio": ("ElevenLabs", "10,000 credits every month across text to speech, sound effects and music"),
 "productivity": ("Fathom", "unlimited recordings and instant call summaries"),
 "presentations": ("Gamma", "400 credits at signup and PDF/PPTX export (with Gamma branding)"),
 "assistants": ("Le Chat (Mistral)", "web and mobile access with image generation and 100+ connectors")}
FREE_LEFT_OUT = [("ChatGPT", "its pricing page redirected to a login screen today, so we couldn't read it"),
 ("Perplexity", "its pricing page didn't load its plan details for us today (JavaScript-heavy)"),
 ("Google Gemini", "the Google AI plans page describes the paid plans, not the free Gemini limits"),
 ("Microsoft Copilot", "the Microsoft 365 page we use doesn't describe free Copilot's limits"),
 ("Ideogram", "its pricing page doesn't describe a free plan"),
 ("Midjourney", "no free plan"), ("Luma Dream Machine", "no free plan listed on its pricing page")]
FREE_SRC2 = {"Runway": "https://help.runwayml.com/hc/en-us/articles/50404627334547-Free-plan-details", "Canva": "https://www.canva.com/licensing-explained/", "HeyGen": "https://www.heygen.com/terms"}
# Runway help: "All videos generated on a Free plan feature a Runway watermark"; usage rights: "the content you create using Runway is yours to use without any non-commercial restrictions" (all plans).
# Canva licensing: "If you're a free user, you'll see a watermark on Pro content"; "You can use our content in a Canva design, for a wide range of personal and commercial uses."
# HeyGen terms s.4 (Free Plan): output licensed "solely for personal, non-commercial, and internal evaluation purposes".

# v44 (2026-10-22): Cursor pricing explained, re-read today on https://cursor.com/pricing:
# "Free $0 /month ... Limited AI usage ... Limited agent requests"; "Plus $8 /month ... Shared AI usage pool ... *Only Grok models are available on this plan";
# "Premium Most popular $30 /month ... 4x more usage compared to Plus ... Cloud agents & automations, Code hosting & AI code reviews, Third-party models at API list price";
# "Super $100 /month ... 15x more usage compared to Plus ... Priority model access at peak times"; compare table: "Ultra $200/month", "Teams $30+/user/month",
# "Usage Limited Basic 4x Plus 15x Plus 50x Plus 4-50x Plus Pooled"; "Third Party model usage in Cursor is not included in the monthly prices shown and must be purchased separately";
# "Prices shown do not include applicable taxes or fees (e.g. VAT)."
CURSOR_CHECKED = "2026-10-22"
CURSOR_PLANS = [  # plan, $/mo, usage vs Plus, what the page says it adds
 ("Free", 0, "Limited", "Limited AI usage, agent and chat requests"),
 ("Plus", 8, "Basic (shared usage pool)", "Only Grok models are available on this plan"),
 ("Premium", 30, "4x Plus", "Cloud agents and automations, code hosting, AI code reviews (Bugbot), third-party models at API list price"),
 ("Super", 100, "15x Plus", "Priority model access at peak times"),
 ("Ultra", 200, "50x Plus", "not stated beyond usage"),
 ("Teams", "30+ per user", "4-50x Plus, pooled", "Team plan; price shown as $30+/user/month"),
]
# v44: AI subscription costs per month. Each price is copied from the tool's verified tools.py entry (date shown per row); build.py asserts the text exists there.
SUB_COSTS = [  # tool, plan, $/mo (monthly billing), quote that must appear in the tool's tools.py price text, checked date source
 ("ChatGPT", "Plus", 20, "Plus $20/mo"), ("Claude", "Pro", 20, "Pro $20/mo"), ("Google Gemini", "Google AI Pro", 19.99, "Google AI Pro $19.99/mo"),
 ("Microsoft Copilot", "Microsoft 365 Personal", 9.99, "Microsoft 365 Personal $9.99/mo"), ("Le Chat (Mistral)", "Pro", 14.99, "Pro $14.99/mo"),
 ("Cursor", "Premium", 30, "Premium $30/mo"), ("GitHub Copilot", "Pro", 10, "Pro $10/mo"), ("Windsurf", "Pro", 20, "Pro $20/mo"),
 ("Midjourney", "Basic", 10, "Basic $10/mo"), ("Canva", "Pro", 18, "Pro $18/mo"), ("Ideogram", "Plus", 20, "Plus $20/mo"),
 ("ElevenLabs", "Starter", 6, "Starter $6/mo"), ("Runway", "Standard", 15, "Standard $15/mo"), ("Descript", "Hobbyist", 24, "Hobbyist $24/mo"),
 ("HeyGen", "Creator", 29, "Creator $29/mo"), ("Grammarly", "Pro", 30, "Pro $30/mo"), ("Notion AI", "Plus", 12, "Plus $12/member/mo"),
 ("Otter", "Pro", 16.99, "Pro $16.99/user/mo"), ("Gamma", "Plus", 12, "Plus $12/mo"),
]
SUB_NOT_STATED = [("Perplexity", "its pricing page shows Pro only billed annually ($17/mo); a monthly price isn't stated")]
SUB_STACKS = [("Writer", ["ChatGPT", "Grammarly"]), ("Developer", ["Cursor", "Claude"]), ("Video creator", ["Descript", "ElevenLabs", "Canva"]), ("Designer", ["Midjourney", "Canva"]), ("Meetings and notes", ["Otter", "Notion AI"])]

# v47 (2026-10-23): ChatGPT pricing, browser-free fetch of https://openai.com/chatgpt/pricing/ (WebFetch) + curl of https://chatgpt.com/pricing today.
# Today's fetch lists plans Free, Go, Plus, Pro (+ Business/Enterprise in FAQ) and features, but the dollar prices are filled in client-side by country:
# the static HTML only shows "Pro ... priceHeader From" with label "Pro $100"; Business shows placeholders "{prices.chatgpt.team.monthly.2026}".
# So: Pro "from $100/mo" confirmed today; Go $8 and Plus $20 are from our 2026-10-15 check (tools.py ChatGPT entry); Business price not stated today.
# FAQ today: "Paid plans (Go, Plus, Business, and Enterprise) are priced per user per month. We offer monthly plans for Go, Plus and Business and annual plans for Business and Enterprise."
# "Business plans are available starting at 2 users." Go: "This plan may include ads."
CHATGPT_CHECKED = "2026-10-24"
CHATGPT_PLANS = [  # plan, price text, price source date, best for (page), key points (page)
 ("Free", "$0", "2026-10-24", "Best for trying out ChatGPT", "Unlimited text chats with GPT-6; limited uploads, image creation, voice, deep research, memory and Codex"),
 ("Go", "$8/mo", "2026-10-24", "Best for longer conversations", "More messages with tools, uploads, image creation and voice; longer memory; may include ads"),
 ("Plus", "$20/mo", "2026-10-24", "Best for advanced work and productivity", "Advanced reasoning with GPT-6; expanded deep research, memory, Codex; projects, scheduled tasks and custom GPTs"),
 ("Pro", "from $100/mo", "2026-10-24", "Best for research and coding", "Choice of 3 usage tiers; Pro reasoning (GPT-6 Astra); maximum deep research and memory; unlimited, faster image creation"),
 ("Business", "$25/seat/mo ($20 billed annually); Premium seat $125/mo ($100 annually)", "2026-10-24", "For businesses, from 2 users", "Priced per user per month; monthly or annual billing"),
]
CHATGPT_FEATURES = [  # row, Free, Go, Plus, Pro (from today's comparison table; "" = not stated for that plan)
 ("GPT Instant context window", "27K", "54K", "54K", "128K"),
 ("GPT Reasoning context window", "Varies", "256K", "256K", "400K"),
 ("Deep research", "Limited", "Limited", "Yes", "Yes"),
 ("Codex", "Limited", "Limited", "Yes", "Expanded"),
 ("Image generation", "Limited", "Yes", "Yes", "Yes"),
 ("Image generation with Thinking", "No", "No", "Yes", "Yes"),
 ("Voice", "Yes", "Expanded", "Expanded", "Unlimited*"),
 ("Memory", "Limited", "Yes", "Expanded", "not stated"),
 ("Scheduled tasks", "No", "Yes", "Yes", "not stated"),
 ("Developer mode (beta)", "No", "No", "Yes", "Yes"),
]
# Claude Pro, https://claude.com/pricing (WebFetch today): Pro "$17 Per month with annual subscription discount ($200 billed up front). $20 if billed monthly.";
# Max "From $100 Per month", "Choose 5x or 20x more usage than Pro"; FAQ "Pro gives you at least 5x more usage per 5-hour session than Free";
# "Claude Code is included in all paid plans"; Free: Projects "Up to 5", Research "No", Opus "No"; Pro: Opus Yes, Research Yes, Claude in Chrome / Microsoft 365 Yes;
# "Usage limits apply. Prices shown don't include applicable tax."
CLAUDE_CHECKED = "2026-10-23"

# v48 (2026-10-24): Student & teacher discounts. Every offer read today on the tool's own official page (src); quote = exact text on that page.
# kind: free | off | ask. who: s = students, t = teachers/educators. save = (formula, $ year-one saving) only when the page states the plan and both prices
# are known (regular price must appear in the tools.py price text, asserted in build.py). end = offer is time-limited (show renewal reminder).
STUDENT_CHECKED = "2026-10-24"
STUDENT_OFFERS = [
 dict(k="google-gemini", tool="Google Gemini", kind="free", badge="Free for 1 year", offer="Google AI Pro free for 1 year",
      gets="4x higher usage limits in Gemini, 5 TB storage, Gemini Spark and Gemini Omni", who="s",
      elig="Eligible U.S. college students ages 18+ (new users, or students whose 2025 AI Pro trial expired). Re-verify every year.",
      claim="Claim the free student plan on gemini.google/students. Redeem by December 31, 2026; a valid form of payment is required.",
      src="https://gemini.google/students/", quote="The free Google AI Pro student offer is available to eligible U.S. college students ages 18+.",
      reg="Google AI Pro $19.99/mo", save=("Google AI Pro $19.99/mo × 12 months", 239.88), end=True),
 dict(k="github-copilot", tool="GitHub Copilot", kind="free", badge="Free", offer="Copilot Student plan, free while you're a student",
      gets="Unlimited code completions and an allowance of GitHub AI Credits, plus limited chat and agent usage (auto model selection only)", who="s",
      elig="Verified students on GitHub Education. GitHub re-checks eligibility every month.",
      claim="Apply to GitHub Education as a student, then activate Copilot Student. Activation can take several days after approval.",
      src="https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students",
      quote="Verified students on GitHub Education get free access to Copilot's features.", reg="Pro $10/mo", save=None, end=False,
      src2="https://education.github.com/pack"),
 dict(k="github-copilot-teachers", tool="GitHub Copilot", kind="free", badge="Free", offer="Copilot Pro free for verified teachers",
      gets="The full Copilot Pro plan", who="t",
      elig="Verified teachers on GitHub Education (maintainers of popular open-source projects also qualify). Eligibility is re-checked every month.",
      claim="Apply to GitHub Education as a teacher, then follow the “Accessing Copilot Pro for free” steps in GitHub Docs.",
      src="https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers",
      quote="Get free access to Copilot Pro as a verified teacher or open-source maintainer.", reg="Pro $10/mo", save=("Copilot Pro $10/mo × 12 months", 120), end=False),
 dict(k="notion-ai", tool="Notion AI", kind="free", badge="Free", offer="Education Plan: Notion's Plus plan free for 1 member",
      gets="Unlimited pages and blocks, file uploads, more site customization and 30-day version history. Notion AI itself isn't mentioned in the student offer (on the Free plan AI is a trial only).", who="st",
      elig="Students and educators at an accredited college or university with a school email address (student IDs aren't accepted).",
      claim="Sign up or log in to Notion with your school email; the plan applies right away.",
      src="https://www.notion.com/pricing", quote="The Plus Plan (with a 1-member limit) is free for students and educators.",
      reg="Plus $12/member/mo ($10 billed yearly)", save=("Plus at $10/mo billed yearly × 12 months", 120), end=False),
 dict(k="beautiful-ai", tool="Beautiful.ai", kind="free", badge="Free for 1 year", offer="Beautiful.ai Pro free for 1 year",
      gets="A free annual Pro subscription", who="s",
      elig="Students with a verified .edu email address. New student subscribers only.",
      claim="Verify your .edu email on beautiful.ai/education. The offer lasts 12 months from activation.",
      src="https://www.beautiful.ai/education", quote="Students with a verified .edu email address can receive a free annual Pro subscription to Beautiful.ai.",
      reg="Pro $14.50/mo (billed annually)", save=("Pro $14.50/mo billed annually × 12 months", 174), end=True),
 dict(k="v0", tool="v0", kind="free", badge="Free for 1 year", offer="1 year of complimentary v0 access",
      gets="v0 access for 1 year (the page doesn't name the plan)", who="s",
      elig="Students currently enrolled at one of v0's active schools, with a valid student email. 15 schools are listed today, e.g. Stanford, MIT, UC Berkeley, NYU, Arizona State and Waterloo.",
      claim="Choose “Join with student email” on v0.app/students.",
      src="https://v0.app/students", quote="Get 1 year of complimentary v0 access when you verify your student status at an active school",
      reg="Team $30/user/mo", save=None, end=True),
 dict(k="elevenlabs", tool="ElevenLabs", kind="free", badge="Free for 3 months", offer="Creator plan free for 3 months",
      gets="The ElevenLabs Creator plan for 3 months. Also on the page: 1 year of ElevenReader Ultra free with a .edu (or equivalent) email.", who="s",
      elig="Students who verify their student status.",
      claim="Verify your student status on elevenlabs.io/students to claim.",
      src="https://elevenlabs.io/students", quote="The ElevenLabs Creator plan, free for 3 months. Verify your student status to claim.",
      reg="Creator $22", save=("Creator $22/mo × 3 months", 66), end=True),
 dict(k="le-chat-mistral", tool="Le Chat (Mistral)", kind="off", badge="$5.99/mo", offer="Mistral Pro for $5.99/mo instead of $14.99",
      gets="Le Chat Pro: more messages and web searches, faster responses, coding and better image generation", who="s",
      elig="Verified students.", claim="On mistral.ai/pricing, choose “I'm a student” under the Pro plan and verify.",
      src="https://mistral.ai/pricing/", quote="Verified students can get Mistral Pro for $5.99 / month (normally $14.99).",
      reg="Pro $14.99/mo", save=("($14.99 − $5.99) × 12 months", 108), end=False),
 dict(k="perplexity", tool="Perplexity", kind="off", badge="$10/mo", offer="Perplexity Pro for $10/month",
      gets="Perplexity Pro at a student price", who="s",
      elig="Students. Sign up with any email, then verify your student status.", claim="Sign in on perplexity.ai/students and verify your student status.",
      src="https://www.perplexity.ai/students", quote="Verify your student status to get Pro for $10/month",
      reg="Pro $17/mo billed annually", save=None, end=False, note="We don't show a saving: the regular Pro price we checked is billed annually, the student price is monthly."),
 dict(k="lovable", tool="Lovable", kind="off", badge="50% off", offer="50% off Lovable Pro for up to 12 months",
      gets="Every Pro feature with 100 credits a month: $25 → $12.50 a month", who="s",
      elig="Enrolled students who log in with the email their school gave them (personal addresses like Gmail can't be verified).",
      claim="Log in with your school email on lovable.dev/students and select “Verify student status”.",
      src="https://lovable.dev/students", quote="You get 50% off Lovable Pro for up to 12 months, with 100 credits a month and every Pro feature.",
      reg="Pro $25/mo", save=("($25 − $12.50) × 12 months", 150), end=True),
 dict(k="microsoft-copilot", tool="Microsoft Copilot", kind="off", badge="50% off", offer="50% off Microsoft 365 Personal (includes Copilot)",
      gets="Word, Excel, PowerPoint, OneNote and Outlook with Copilot in the desktop apps, 1 TB of cloud storage and advanced security", who="s",
      elig="Full- and part-time students at accredited universities and colleges. Re-verify every year; the price rises to full price if you're no longer eligible.",
      claim="Sign in with a personal Microsoft account (not an EDU account), add payment info, then verify with your EDU email or student documents.",
      src="https://www.microsoft.com/en-us/microsoft-365/college-student-pricing", quote="Students save 50% on Microsoft 365 Personal",
      reg="Microsoft 365 Personal $9.99/mo", save=None, end=False),
 dict(k="reclaim", tool="Reclaim", kind="off", badge="50% off", offer="50% off Reclaim for 12 months",
      gets="Half price on a paid Reclaim plan for 12 months", who="st",
      elig="Students, educators and faculty.", claim="On reclaim.ai/pricing, open Discounts → Student Discount → Apply now.",
      src="https://reclaim.ai/pricing", quote="50% discount for 12 months for students, educators, and faculty.",
      reg="Starter $12/seat/mo ($10 yearly)", save=None, end=True),
 dict(k="consensus", tool="Consensus", kind="off", badge="Up to 40% off", offer="Up to 40% off a Consensus subscription",
      gets="A discounted Consensus subscription (the page says “up to”, so the exact rate shows when you claim)", who="st",
      elig="Students and faculty with a valid school email.", claim="Select “Claim” under the student/faculty banner on consensus.app/pricing.",
      src="https://consensus.app/pricing/", quote="Students and faculty with a valid school email and US HCPs with a valid NPI number can get up to 40% off a subscription.",
      reg="Pro $20/mo ($12/mo annually)", save=None, end=False),
 dict(k="wordtune", tool="Wordtune", kind="off", badge="30% off", offer="30% off Wordtune monthly and annual plans",
      gets="30% off any paid plan", who="st",
      elig="Students or educators with a valid .edu email address, enrolled at or working at an academic institution.", claim="Contact Wordtune support to apply.",
      src="https://www.wordtune.com/plans", quote="you are eligible for a 30% discount on both our annual and monthly plans",
      reg="From $6.99/mo ($4.89/mo with yearly discount)", save=None, end=False),
 dict(k="otter", tool="Otter", kind="off", badge="20% off", offer="20% off Otter Pro: $13.59/mo, or $6.67/mo billed $79.99 a year",
      gets="Otter Pro at a student price", who="st",
      elig="Individual students and teachers with an email address ending in .edu.",
      claim="Sign up with your .edu email → click your name → Upgrade plan → “Student & Teacher Discount” (below the Pro plan).",
      src="https://otter.ai/pricing", quote="we offer a 20% discount on Otter Pro Monthly and Otter Pro Annual plans for individual students and teachers",
      reg="Pro $16.99/user/mo", save=("($16.99 − $13.59) × 12 months, monthly billing", 40.80), end=False,
      note="Otter's first-time promo (Pro $8.49/mo, checked 2026-10-21) was lower than the student price, so compare both before you pay."),
 dict(k="canva", tool="Canva", kind="free", badge="Free", offer="Canva for Education: free for K-12 teachers and their students",
      gets="Canva's free education plan for classrooms", who="st",
      elig="K-12 (primary and secondary) educators, their students, and qualified schools and districts. Not for individual college students: universities use Canva Campus through the institution.",
      claim="Teachers sign up with an education email or upload proof of employment on canva.com/education; verification takes a few days.",
      src="https://www.canva.com/pricing/", quote="Canva Education is available for K-12 (primary and secondary) educators, their students, and qualified school districts and institutions.",
      reg="Pro $18/mo", save=None, end=False),
 dict(k="descript", tool="Descript", kind="ask", badge="Ask", offer="Special rates for students and educators, by application",
      gets="A special rate (amount not stated on the page)", who="st",
      elig="Students, educators and non-profits.", claim="Fill out the form linked in the FAQ on descript.com/pricing.",
      src="https://www.descript.com/pricing", quote="Do you offer special rates for students, educators, and non-profits? Yes, fill out this form",
      reg="Hobbyist $24/mo", save=None, end=False),
 dict(k="udio", tool="Udio", kind="ask", badge="Ask", offer="Discounted student pricing (shown after login)",
      gets="A student price; the amount is only shown after you log in, so we couldn't verify it", who="s",
      elig="Students.", claim="Follow “Check out our discounted student pricing” on udio.com/pricing and log in.",
      src="https://www.udio.com/pricing", quote="Are you a student? Check out our discounted student pricing",
      reg="Standard $10/mo", save=None, end=False),
]
STUDENT_SCHOOL_ONLY = [  # tool, what, src, quote
 ("Claude", "Education plan: a university-wide plan bought by the institution for its students, faculty and staff. No individual student discount is listed.", "https://claude.com/pricing", "Get a comprehensive university‐wide plan for an institution, including its students, faculty, and staff."),
 ("Grammarly", "Discounts for educational institutions (Grammarly for Education), not individual students.", "https://www.grammarly.com/plans", "Do you offer discounts for educational institutions? Yes!"),
 ("Canva", "Canva Campus for universities and colleges, set up by the institution.", "https://www.canva.com/pricing/", "Canva Campus empowers higher education students, faculty staff, plus campus administrators"),
 ("Scite", "A discount code if you recommend Scite to your institution (email them with your institution in cc).", "https://scite.ai/pricing", "We do offer discounts for students and academics if you recommend Scite to your institution."),
]
STUDENT_NONE = [  # tool, what the official page says today, src
 ("ChatGPT", "No student plan or discount on its pricing page today; it only mentions a Rosalind Academic Plan for life-sciences research.", "https://chatgpt.com/pricing"),
 ("Cursor", "No standing discount: “Anyone can get started with Cursor for free. To upgrade your access, look out for promotions at our on-campus and online events.”", "https://cursor.com/students"),
 ("Warp", "“At this time, Warp does not offer discounts for students, non-profits, or open-source teams.” It points to the Free plan instead.", "https://www.warp.dev/pricing"),
]

# Daily ops 2026-10-24: browser re-check of chatgpt.com/pricing, perplexity.ai/pro, gamma.app/pricing, canva.com/pricing; prices unchanged, ChatGPT Business now shown.
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in ("ChatGPT","Perplexity","Gamma","Canva"): _t["checked"] = "2026-10-24"
PRICE_NOTES["2026-10-24|ChatGPT"] = ("changed", "ChatGPT's prices are unchanged (Go $8/mo, Plus $20/mo, Pro from $100/mo). New: we now also show Business at $25/seat/mo billed monthly, or $20 billed annually.")
for _n in ("Perplexity", "Gamma", "Canva"):
    PRICE_SKIP[f"2026-10-24|{_n}"] = "Re-checked 2026-10-24; only the checked date changed, prices unchanged."

# --- v50: AI team plan costs (/ai-team-plans.html) ---
# Every row read on the official pricing page on TEAM_CHECKED (curl + headless-Chrome render, text saved in /workspace/v50/raw).
# m = $ per seat per month billed monthly; y = $ per seat per month billed yearly (None = not stated on the page today).
# base = fixed $/mo for the workspace on top of seats; flat = one price for the whole workspace (seats don't multiply);
# mn/mx = seat minimum/maximum stated on the page; frm = page says "from"/"+"; addon = needs another paid plan (never ranked).
# q = exact text from the page (whitespace-normalised) that the numbers come from; build.py asserts the numbers appear in it.
TEAM_CHECKED = "2026-10-26"
TEAM_GROUPS = [("assistants", "AI assistants"), ("coding", "AI coding"), ("apps", "App builders"), ("meetings", "Meeting notes"),
               ("docs", "Docs & notes"), ("slides", "Presentations"), ("design", "Design & images"), ("video", "Video editing")]
TEAM_PLANS = [
 dict(t="ChatGPT", plan="Business (standard seat)", g="assistants", m=25, y=20, mn=2, mx=200, src="https://chatgpt.com/pricing",
      q=["$20/month if billed annually. $25/month if billed monthly.", "For teams of 2–200 employees."],
      note="Premium seat (5x usage) $125/mo, or $100 billed yearly. Mix seat types."),
 dict(t="Claude", plan="Team (standard seat)", g="assistants", m=25, y=20, mn=2, mx=150, src="https://claude.com/pricing",
      q=["For teams of 2 to 150", "$20 Per seat / month if billed annually. $25 if billed monthly."],
      note="Premium seat (5x usage) $125/mo, or $100 billed yearly. Mix seat types."),
 dict(t="Le Chat (Mistral)", plan="Team", g="assistants", m=24.99, y=None, src="https://mistral.ai/pricing",
      q=["Team Secure, collaborative workspace for teams building with AI. $24.99 /user/mo Excluding taxes"],
      note="Price excludes tax. A yearly price isn't stated."),
 dict(t="Perplexity", plan="Enterprise Pro", g="assistants", m=None, y=34, src="https://www.perplexity.ai/enterprise/pricing",
      q=["$34 / month per seat when billed annually"], note="Only a billed-yearly price is shown."),
 dict(t="Microsoft Copilot", plan="Microsoft 365 Copilot Business (add-on)", g="assistants", m=25.20, y=21, addon=True,
      src="https://www.microsoft.com/en-us/microsoft-365-copilot/pricing",
      q=["Microsoft 365 Copilot Business (add-on) AI built for work to help drive productivity, clarity and impact across your existing Microsoft 365 experience $25.20 user/month Monthly subscription",
         "Originally starting from $21.00 now starting from $18.00 $21.00 $18.00 user/month, paid yearly"],
      note="Add-on: you also need a Microsoft 365 business plan (not included), so it isn't ranked. Yearly list price $21; the page shows a limited offer of $18."),
 dict(t="GitHub Copilot", plan="Business", g="coding", m=19, y=None, src="https://github.com/features/copilot/plans",
      q=["Business $19 per user / month"], note="Pooled credits for the team. A yearly price isn't stated."),
 dict(t="Cursor", plan="Teams", g="coding", m=30, y=None, frm=True, src="https://cursor.com/pricing",
      q=["Teams $30 +/user/month"], note="Shown as $30+ per user; usage is pooled. A yearly price isn't stated."),
 dict(t="Windsurf", plan="Teams", g="coding", m=40, y=None, base=80, mx=200, src="https://windsurf.com/pricing",
      q=["Teams $80 /month for team plan + $40/mo per full dev seat", "Up to 200 users"],
      note="$80/mo team plan fee plus $40/mo per full dev seat."),
 dict(t="Bolt", plan="Teams", g="apps", m=30, y=27, src="https://bolt.new/pricing",
      q=["Teams $30 * /month Per member, billed monthly", "Teams $27 * /month Total of $324"], note="$324 per member per year billed yearly."),
 dict(t="Lovable", plan="Business", g="apps", m=50, y=None, flat=True, frm=True, src="https://lovable.dev/pricing",
      q=["Business Advanced controls and power features for growing departments $50 / month 100 monthly credits Get started Unlimited users"],
      note="One price for the whole workspace with unlimited users; the 100 monthly credits are shared. Pro ($25/mo) also allows unlimited users."),
 dict(t="Otter", plan="Business", g="meetings", m=30, y=19.99, mx=25, src="https://otter.ai/pricing",
      q=["Business Best Value For medium-sized teams $30 $24 /user/month 20% off for 3 months", "Business Best Value For medium-sized teams $19 .99 /user/month", "Max workspace members 5 5 billed users 25 billed users"],
      note="Up to 25 billed users. New subscribers: $24/user/mo for the first 3 months on monthly billing."),
 dict(t="Fireflies", plan="Business", g="meetings", m=29, y=19, src="https://fireflies.ai/pricing",
      q=["Business For fast growing businesses $29 $19 per seat / month, billed annually"], note=""),
 dict(t="Fathom", plan="Team", g="meetings", m=19, y=15, mn=2, src="https://www.fathom.ai/pricing",
      q=["FOR TEAMS Team $ 19 $15 $19 /month / per user (2 user min"], note="Business plan (CRM sync, coaching): $34/user/mo, or $25 billed yearly."),
 dict(t="Notion AI", plan="Business", g="docs", m=24, y=20, src="https://www.notion.com/pricing",
      q=["Business $24 per seat/month", "Business $20 per seat/month"],
      note="Full Notion AI starts on Business. Plus ($12, or $10 billed yearly) only includes an AI trial."),
 dict(t="Gamma", plan="Business", g="slides", m=None, y=40, src="https://gamma.app/pricing",
      q=["Business For organizations ready to make it official with Gamma $40 / seat / month $480 per seat, billed annually"],
      note="$480 per seat per year. Plus ($9) and Pro ($18) are also per seat, billed yearly."),
 dict(t="Beautiful.ai", plan="Team", g="slides", m=50, y=40, mn=2, mx=20, src="https://www.beautiful.ai/pricing",
      q=["Teams of 2 to 20 pay $40 per user per month billed annually, or $50 billed monthly."], note="For 2 to 20 seats."),
 dict(t="Plus AI", plan="Team", g="slides", m=40, y=30, src="https://plusai.com/pricing",
      q=["Team $30 per user/month, billed annually. $40/user billed monthly."], note="Works inside Google Slides and PowerPoint."),
 dict(t="Canva", plan="Business", g="design", m=None, y=250/12, yr=250, src="https://www.canva.com/pricing/",
      q=["Business Create content faster, market smarter, and grow your business with advanced tools. US$ 250 /year per person"],
      note="$250 per person per year. We couldn't read a monthly price today."),
 dict(t="Ideogram", plan="Team", g="design", m=30, y=20, src="https://ideogram.ai/pricing",
      q=["Team Best for teams creating together $30 per user/month, $240 billed annually", "Team $20/user/mo"], note="$240 per user per year billed yearly."),
 dict(t="Recraft", plan="Teams", g="design", m=None, y=18, src="https://www.recraft.ai/pricing",
      q=["Teams For teams collaborating on shared creative workflows. $18 per month per seat billed annually"], note="Only a billed-yearly price is shown."),
 dict(t="Descript", plan="Business", g="video", m=65, y=50, src="https://www.descript.com/pricing",
      q=["Business $ 50 $ 65 per person / month Scale to a team of 5 (billed separately)"], note="The page says “Scale to a team of 5 (billed separately)”."),
 dict(t="CapCut", plan="Teams", g="video", m=12.49, y=None, src="https://www.capcut.com/pricing",
      q=["Teams USD 12.49 /month per seat"], note="The yearly price changes with seat count on the page, so we show monthly only."),
]
TEAM_LEFT_OUT = [  # tool, why (all read on TEAM_CHECKED)
 ("Google Gemini", "Gemini for teams comes inside Google Workspace plans; today's page showed introductory offers and footnoted prices, so we couldn't state a clean per-seat price"),
 ("HeyGen", "Business is $149/mo plus $20 per seat, but the page doesn't say whether the $149 includes the first seat"),
 ("Jasper", "Pro includes 1 seat; adding teammates needs the Business plan, which has custom pricing"),
 ("v0", "the Team plan card showed two different per-user prices, so we couldn't tell which applies"),
 ("Zapier", "Team is “from $69/month” for 25 users, but the page doesn't say which billing period that is"),
 ("Grammarly", "the page shows Pro at $12 per member but didn't state the billing period in the text we could read"),
 ("ClickUp", "its AI is a separate per-user add-on on top of the workspace plan"),
 ("Replit", "its pricing page showed a security check today"),
]

# v51 (2026-10-26): ElevenLabs, https://elevenlabs.io/pricing (WebFetch, "Monthly billing"). FAQ: "Free $0 (10,000 credits); Starter $6 (30,000 credits);
# Creator $22 (121,000 credits, $11 for the first month); Pro $99 (600,000 credits); Scale $299 (1,800,000 credits, 3 seats); Business $990 (6,000,000 credits, 10 seats); Enterprise is custom."
# Starter card: "Until Nov 1 $6 First month 83% off $1per month" (a stale banner on the same page says "Ends September 30"; we use the plan card).
# Annual: "annual price = monthly price x 10 ... $5 Starter, $18.33 Creator, $82.50 Pro, $249.17 Scale, $825 Business".
# Compare table: TTS minutes included ~10/~30/~121/~600/~1,800/~6,000 (Free..Business). The "Extra minute" row is ambiguous in the fetched text (values shifted), so not used.
# Credits: TTS 1 credit/character (V2 Multilingual); STT 330/min; Music 900/min; SFX 200/generation; Voice Changer & Isolator 1,000/min; Dubbing 2,000-10,000/min.
# Rollover: unused credits roll over up to 2 months (max 3x quota) on active paid plans; not on Free. "Prices exclude all taxes, levies and duties."
EL_CHECKED = "2026-10-26"
EL_PLANS = [  # plan, monthly $, yearly $/mo, credits, ~TTS minutes (UI), first-month promo, key adds
 ("Free", 0, None, "10,000", "~10", "", "Text to speech, speech to text, sound effects, music; 3 Studio projects; no commercial license"),
 ("Starter", 6, 5, "30,000", "~30", "$1 first month (until Nov 1)", "Commercial license, Instant Voice Cloning, Dubbing Studio, 20 Studio projects"),
 ("Creator", 22, 18.33, "121,000", "~121", "$11 first month (50% off)", "Professional Voice Cloning, additional credits"),
 ("Pro", 99, 82.50, "600,000", "~600", "", "44.1kHz PCM output via API, 192kbps audio"),
 ("Scale", 299, 249.17, "1,800,000", "~1,800", "", "3 workspace seats, team collaboration, 3 Professional Voice Clones"),
 ("Business", 990, 825, "6,000,000", "~6,000", "", "10 seats, 10 Professional Voice Clones, low-latency TTS from 5c/minute"),
 ("Enterprise", None, None, "Custom", "Custom", "", "Custom terms, SSO, more seats; contact sales"),
]
EL_CREDITS = [("Text to speech", "1 credit per character (V2 Multilingual)"), ("Speech to text", "330 credits per minute"), ("Music", "900 credits per minute"),
 ("Sound effects", "200 credits per generation"), ("Voice changer / isolator", "1,000 credits per minute"), ("Dubbing", "2,000-10,000 credits per minute (watermark and Studio options)")]

# --- v52: refund & cancel rules, read on each tool's official help page on REFUND_CHECKED ---
# k: "w" = stated refund window/conditions, "c" = case by case, "n" = no refunds (except where the law requires)
# wm/wy = refund window in hours for monthly / yearly billing (None = no time window stated). q = exact words on the page.
REFUND_CHECKED = "2026-10-27"
REFUNDS = [
 {"t": "ChatGPT", "k": "w", "wm": 168, "wy": 168, "cond": "unused individual subscription, current billing period only, no substantial use; it's at their discretion and repeat refunds are limited",
  "how": "Log in, open the Help Center chat widget and ask for a refund. It shows your eligibility first.", "eu": "EU, UK and Turkey: prorated refund if you cancel within 14 days of purchase.",
  "cancel": "Settings → Billing (or Account) → Cancel plan → Cancel", "notice": "at least 24 hours before your next billing date",
  "after": "Paid features stay until the end of the period you paid for.", "app": 1,
  "q": "Payments are generally non-refundable. … For an unused individual subscription purchase, a discretionary refund may be available if you contact us within seven days of the charge.",
  "sr": "https://help.openai.com/en/articles/7232895-how-do-i-request-a-refund-for-my-chatgpt-subscription", "sc": "https://help.openai.com/en/articles/7232927-canceling-your-chatgpt-subscription"},
 {"t": "Claude", "k": "c", "wm": None, "wy": None, "cond": "only payments their Consumer Terms call refundable, or where the law requires",
  "how": "Get help → Send us a message → “Claude Refund Request”. It checks eligibility.", "eu": "EEA and UK: refund within 14 days, reduced for what you used.",
  "cancel": "Settings → Billing → Cancel", "notice": "at least 24 hours before your next billing date",
  "after": "Your plan runs to the end of the period, then the account moves to Free.", "app": 1,
  "q": "Except as expressly provided in our Consumer Terms of Service or where required by law, all payments are non-refundable.",
  "sr": "https://support.claude.com/en/articles/12386328-request-a-refund-for-a-paid-claude-plan", "sc": "https://support.claude.com/en/articles/8325617-cancel-your-pro-or-max-subscription"},
 {"t": "Perplexity", "k": "w", "wm": 24, "wy": 72, "cond": "monthly: ask within 24 hours of purchase; yearly: full refund within 72 hours, no exceptions after that; only one refund per account",
  "how": "perplexity.ai/pro → Manage Subscription → Cancel Plan; the refund option appears there.", "eu": "EU, UK and Turkey: 14 days. South Korea and Brazil: 7 days.",
  "cancel": "Settings → Subscription → Manage Subscription → Cancel subscription", "notice": "",
  "after": "Bought in the iPhone or Android app? Cancel in the App Store or Google Play; the option isn't in Perplexity Settings.", "app": 1,
  "q": "Monthly subscriptions: You can request a refund up to 24 hours after the purchase date. … Annual subscriptions: You are eligible for a full refund within 72 hours of the original purchase date and time.",
  "sr": "https://www.perplexity.ai/help-center/en/articles/10354288-refunds", "sc": "https://www.perplexity.ai/help-center/en/articles/10354283-canceling-a-subscription"},
 {"t": "Midjourney", "k": "w", "wm": None, "wy": None, "cond": "you've used less than 20 GPU minutes in your account's whole lifetime (Fast, Turbo and Relax all count). No time limit is stated",
  "how": "If you qualify, a refund option appears when you cancel. No option means no refund.", "eu": "",
  "cancel": "Manage Subscription page → Cancel Plan", "notice": "",
  "after": "Cancelling takes effect at the end of your billing cycle; your images aren't deleted.", "app": 0,
  "q": "You're eligible for a refund only if you've used less than 20 GPU minutes throughout the lifetime of your account.",
  "sr": "https://docs.midjourney.com/hc/en-us/articles/25386088618253-Requesting-a-Refund", "sc": "https://docs.midjourney.com/hc/en-us/articles/25384024738573-Canceling-Your-Subscription"},
 {"t": "Cursor", "k": "w", "wm": 336, "wy": 336, "cond": "your most recent payment, charged in the last 14 days, and you haven't used the subscription that billing period (individual plans)",
  "how": "Contact Cursor support; they review your account.", "eu": "",
  "cancel": "cursor.com/dashboard → Billing → Manage (Stripe) → Cancel subscription", "notice": "",
  "after": "Paid access stays until the period ends, then the account goes back to the free plan. No prorated refund for downgrading.", "app": 0,
  "q": "Outside the 14-day window, or with usage during the period, that payment is generally not refundable and you are committed for the current billing period.",
  "sr": "https://cursor.com/help/account-and-billing/refunds", "sc": "https://cursor.com/help/account-and-billing/cancel"},
 {"t": "GitHub Copilot", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "", "eu": "",
  "cancel": "GitHub Settings → Billing & licensing → Licensing → Manage subscription → Cancel subscription", "notice": "",
  "after": "Access stays until the end of the billing cycle, then you move to Copilot Free.", "app": 0,
  "q": "Downgrading/canceling: Access remains until the end of the current billing cycle. No refund for unused time.",
  "sr": "https://docs.github.com/en/copilot/reference/copilot-billing/license-changes", "sc": "https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan"},
 {"t": "ElevenLabs", "k": "w", "wm": 336, "wy": 336, "cond": "you ask within 14 days of payment and haven't used any credits in that period",
  "how": "Email support@elevenlabs.io from your account email.", "eu": "",
  "cancel": "Profile → Subscription → Billing → Modify Plan → Cancel Plan → Proceed → Cancel Subscription", "notice": "",
  "after": "Ends at the end of the billing cycle and moves you to Free. Unused credits are lost.", "app": 0,
  "q": "You are eligible for a refund if a request is filed within 14 days of payment and no credit quota was used in the period for which you are seeking the refund.",
  "sr": "https://elevenlabs.io/docs/help-center/account/cancellation-refunds/what-is-your-refund-policy", "sc": "https://elevenlabs.io/docs/help-center/account/cancellation-refunds/how-do-i-cancel-my-subscription"},
 {"t": "Canva", "k": "c", "wm": None, "wy": None, "cond": "Canva reviews every request but says most subscriptions aren't refundable",
  "how": "Contact Canva support. Bought on iPhone? Apple handles it.", "eu": "",
  "cancel": "Profile → Settings → Billing → Cancel plan → Continue cancellation → pick a reason → Cancel subscription", "notice": "",
  "after": "Access stays until the period ends. You can pause Pro, Teams or Business for up to 3 months instead. Cancelling Canva Teams is permanent.", "app": 1,
  "q": "In most cases, Canva subscriptions aren’t refundable",
  "sr": "https://www.canva.com/help/subscription-refunds/", "sc": "https://www.canva.com/help/cancel-canva-plan/"},
 {"t": "Grammarly", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "", "eu": "",
  "cancel": "Account → Your account → Subscription → Cancel Subscription → Continue → pick a reason → Cancel Subscription", "notice": "",
  "after": "Premium stays until the end of the period you paid for.", "app": 1,
  "q": "refunds are issued only if required by law",
  "sr": "https://support.grammarly.com/hc/en-us/articles/360049189071-Can-I-get-a-refund", "sc": "https://support.grammarly.com/hc/en-us/articles/115000090172-How-do-I-cancel-my-subscription"},
 {"t": "Notion AI", "k": "w", "wm": 72, "wy": 720, "cond": "monthly: within 3 days of the invoice date; yearly: within 30 days. The request must come from the workspace owner or billing email. Unused purchased credits are refundable",
  "how": "Contact support from inside the app, from the owner or billing email.", "eu": "",
  "cancel": "Settings → Billing → Change plan → pick Free (desktop or web only)", "notice": "",
  "after": "Your paid plan stays until the end of the billing cycle.", "app": 1,
  "q": "In most cases, we can process a refund if you contact us within three days of the date your invoice is issued for monthly billing, or within 30 days of the date your invoice is issued for annual billing.",
  "sr": "https://www.notion.com/help/refunds", "sc": "https://www.notion.com/help/upgrade-or-downgrade-your-plan"},
 {"t": "Runway", "k": "w", "wm": 720, "wy": 720, "cond": "bought or renewed in the last 30 days and unused or close to unused (Runway decides). Picked annual instead of monthly by mistake? They refund the difference",
  "how": "Profile → Plans and Billing → help icon. The assistant checks eligibility.", "eu": "",
  "cancel": "app.runwayml.com/settings/billing → Cancel plan → Continue to cancel plan → confirm in Stripe", "notice": "",
  "after": "Access stays until the billing cycle ends. If a refund is granted, the plan and its unused credits end at once.", "app": 1,
  "q": "You purchased or renewed your subscription within the last 30 days, and since the time of initial purchase or renewal, your subscription to the Services is unused, or close to unused (as determined by Runway in its discretion).",
  "sr": "https://help.runwayml.com/hc/en-us/articles/24343363554067-Requesting-a-refund-for-your-plan-or-payment", "sc": "https://help.runwayml.com/hc/en-us/articles/21668396605971-How-do-I-cancel-my-plan"},
 {"t": "Suno", "k": "c", "wm": None, "wy": None, "cond": "Suno decides. Their examples: a subscription with zero songs made is likely refunded, an accidental yearly payment may get a partial refund, “changed your mind” isn't",
  "how": "Email support@suno.com.", "eu": "",
  "cancel": "suno.com/account → manage your subscription (app purchases: App Store or Google Play)", "notice": "",
  "after": "", "app": 1,
  "q": "Payments made by you hereunder are final and non-refundable, unless otherwise determined by Suno.",
  "sr": "https://help.suno.com/en/articles/2550209", "sc": "https://help.suno.com/en/articles/2410369"},
 {"t": "Descript", "k": "w", "wm": 48, "wy": 48, "cond": "plan refunds within 48 hours of the invoice date; extra editor seats within 7 days; top-ups are non-refundable",
  "how": "Send a request to Descript support from your account email.", "eu": "",
  "cancel": "App Settings (Cmd/Ctrl + ,) → Plan → Change plan → Downgrade to Free → reason → Cancel subscription", "notice": "",
  "after": "Your plan stays active until the end of the term. No prorated refunds for unused time.", "app": 0,
  "q": "Plan refunds: Available within 48 hours of the invoice date",
  "sr": "https://help.descript.com/billing-payments-plans/refund-policy", "sc": "https://help.descript.com/billing-payments-plans/cancel"},
 {"t": "Gamma", "k": "w", "wm": 72, "wy": 72, "cond": "only within the first 3 days of subscribing, only by contacting support, and under the credit limit: Plus under 200, Pro under 600, Team under 900, Business under 1,000, Ultra under 2,000 credits used",
  "how": "Contact Gamma support. Cancelling alone doesn't refund you.", "eu": "",
  "cancel": "Settings → Billing → Cancel subscription (billing admin)", "notice": "at least 30 days before your renewal date",
  "after": "Your subscription stays active until the current term ends. No pause option.", "app": 0,
  "q": "Beginning December 1, 2025, Gamma will offer refunds only within the first 3 days of subscribing to one of our paid plans, for both monthly and annual billing options, and only upon contacting Customer Support.",
  "sr": "https://help.gamma.app/en/articles/11048496-what-is-gamma-s-refund-policy-and-how-do-i-request-a-refund", "sc": "https://help.gamma.app/en/articles/8568920-how-do-i-manage-or-cancel-my-gamma-subscription"},
 {"t": "Otter", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "", "eu": "",
  "cancel": "Account Settings → Billing → Cancel plan → reason → Cancel subscription", "notice": "at least 24 hours before your next billing date",
  "after": "You can pause your plan once instead (Account Settings → Plan → Pause Plan).", "app": 1,
  "q": "Subscriptions are non-refundable as explained in the Otter Terms of Service.",
  "sr": "https://help.otter.ai/hc/en-us/articles/23346776714903-Cancel-an-Otter-subscription", "sc": "https://help.otter.ai/hc/en-us/articles/23346776714903-Cancel-an-Otter-subscription"},
 {"t": "Lovable", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "Contact support only for billing errors.", "eu": "",
  "cancel": "Workspace settings → Plans & credit usage → Manage → Downgrade to free (not in the mobile app)", "notice": "",
  "after": "Unused plan and rollover credits are frozen, not refunded.", "app": 0,
  "q": "No. When you cancel, Lovable stops future charges but does not refund the current billing period.",
  "sr": "https://docs.lovable.dev/introduction/manage-subscription", "sc": "https://docs.lovable.dev/introduction/manage-subscription"},
 {"t": "HeyGen", "k": "c", "wm": 360, "wy": 360, "cond": "if the app didn't suit your needs, purchases on HeyGen or Google Play may be refunded within 15 days (Apple: 14 days), case by case; less likely if you used a lot of credits",
  "how": "Live chat in HeyGen or email support@heygen.com with your reason and invoice.", "eu": "",
  "cancel": "Settings → Plan & Billing → arrow next to Manage Billing → Cancel Plan (or Pause Plan)", "notice": "",
  "after": "Access stays until the billing cycle ends. No prorated refunds; unused credits expire when you downgrade.", "app": 1,
  "q": "HeyGen and Google Play purchases may be refunded within 15 days, while Apple App Store purchases may be refunded within 14 days.",
  "sr": "https://help.heygen.com/en/articles/8304807-refund-process-and-policy", "sc": "https://help.heygen.com/en/articles/8304328-how-to-cancel-or-pause-your-heygen-subscription"},
 {"t": "Synthesia", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "Charged while a confirmed technical issue locked you out? Email support@synthesia.io.", "eu": "",
  "cancel": "Profile → Account info → Billing → ⋯ menu → Cancel your subscription → confirm", "notice": "",
  "after": "Access stays until the period ends, then you lose access to Synthesia and every video in your account. Export first.", "app": 0,
  "q": "all purchases are non-cancelable and, except where the Contract expressly states otherwise, non-refundable.",
  "sr": "https://help.synthesia.io/en/articles/15972602-what-is-synthesia-s-refund-and-billing-policy", "sc": "https://help.synthesia.io/en/articles/15972027-how-do-i-manage-my-synthesia-plan-and-billing"},
 {"t": "Jasper", "k": "w", "wm": 168, "wy": 168, "cond": "you email within 7 days of the charge; only the current subscription charge. Cancel first, refunds aren't automatic",
  "how": "Cancel, then email hey@jasper.ai.", "eu": "",
  "cancel": "Workspace name → Workspace Settings → Plans → scroll down → Cancel → follow the prompts", "notice": "",
  "after": "You keep access until the billing cycle ends. You can pause for 30, 60 or 90 days instead.", "app": 0,
  "q": "You will need to contact us directly within seven days of the charge to receive a refund.",
  "sr": "https://help.jasper.ai/hc/en-us/articles/18618699843739-Refund-Policy", "sc": "https://help.jasper.ai/hc/en-us/articles/18618705279899-Cancel-Your-Account-Pro-Plan"},
 {"t": "Fireflies", "k": "w", "wm": 168, "wy": 168, "cond": "monthly: within 7 days, full refund with 3 or fewer meetings, otherwise pro-rated; yearly: within 7 days and 20 or fewer meetings, no pro-rated refunds. AI Credits are non-refundable",
  "how": "Purple chat widget in the Fireflies app → Contact Support.", "eu": "",
  "cancel": "Settings → Account → Subscriptions → Cancel → reason → Proceed With Cancellation → Cancel Subscription", "notice": "",
  "after": "Paid features stay until the cycle ends, then you move to Free. Your meetings and transcripts stay.", "app": 0,
  "q": "Pro-rated refunds are not available on annual plans",
  "sr": "https://guide.fireflies.ai/articles/8731544498-fireflies-refund-policy", "sc": "https://guide.fireflies.ai/articles/6637635140-how-to-cancel-fireflies-subscription"},
 {"t": "Ideogram", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "Charged twice? Email support@ideogram.ai.", "eu": "",
  "cancel": "Avatar → Wallet & Billing → Manage plan & billing → Cancel subscription → reason → Cancel subscription", "notice": "at least 5 days before your renewal date",
  "after": "Benefits stay until the paid period ends. Unused monthly credits end with the plan.", "app": 1,
  "q": "Ideogram doesn't offer refunds. This covers subscription payments, renewals, credit purchases and partly used billing periods.",
  "sr": "https://docs.ideogram.ai/plans-and-billing/billing-and-subscriptions/refunds", "sc": "https://docs.ideogram.ai/plans-and-billing/billing-and-subscriptions/cancelling-your-subscription"},
 {"t": "Bolt", "k": "n", "wm": None, "wy": None, "cond": "",
  "how": "Questions: support@bolt.new from your paid account's email.", "eu": "",
  "cancel": "Profile icon → Subscription → Billing details → Cancel subscription → follow the StackBlitz billing portal", "notice": "",
  "after": "Your paid plan stays until the next billing period, then moves to Free. You can undo before then.", "app": 0,
  "q": "Bolt subscriptions are non-refundable, as stated in our Terms of Service.",
  "sr": "https://support.bolt.new/account/billing", "sc": "https://support.bolt.new/account/billing"},
]
REFUND_LEFT_OUT = [("Google Gemini", "Google's refund page covers Google One storage plans and doesn't clearly state the rule for Google AI Pro"),
                   ("Leonardo", "its help page says refunds are reviewed by a person but we couldn't read a clear rule")]
