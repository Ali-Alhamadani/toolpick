"""ToolPick data. Edit this file, then run build.py.
price: exactly what the official pricing page showed on `checked`; use "check site" if not verifiable.
"""
CHECKED = "2026-10-19"
CATEGORIES = [
 {"id":"video","name":"Video","need":"Make or edit videos","best":"Runway","free":["CapCut","HeyGen","Synthesia"],"tools":[
  {"name":"Runway","url":"https://runwayml.com","pricing":"https://runwayml.com/pricing","price":"Standard $15/mo ($12/mo billed yearly); Pro $35 ($28); Max $95 ($76)","free":"Free plan: one-time 125 credits","about":"Gen-4.5 text/image-to-video plus image and audio models in one app.","why":"Lowest-priced entry plan among the big generative video studios, with a free credit deposit to test first."},
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
  {"name":"Grammarly","url":"https://www.grammarly.com","pricing":"https://www.grammarly.com/plans","price":"Pro $12/mo","free":"Free: $0 spelling & grammar checks","about":"Grammar, clarity and tone fixes everywhere you type."},
  {"name":"Notion AI","url":"https://www.notion.com","pricing":"https://www.notion.com/pricing","price":"Plus $10/member/mo; Business $20/member/mo","free":"Free plan: $0 (AI trial only)","about":"AI writing inside your notes, docs and wikis."},
  {"name":"Copy.ai","url":"https://www.copy.ai","pricing":"https://www.copy.ai/prices","price":"Chat $29/mo ($24 yearly); team plans from $1,000/mo","free":"Free trial available","about":"Marketing copy and GTM workflow automation."},
  {"name":"Jasper","url":"https://www.jasper.ai","pricing":"https://www.jasper.ai/pricing","price":"check site","free":"7-day free trial of Pro","about":"On-brand marketing content for teams."},
 ]},
 {"id":"coding","name":"Coding","need":"Write code or build an app","best":"GitHub Copilot","free":["GitHub Copilot","Windsurf","v0"],"tools":[
  {"name":"GitHub Copilot","url":"https://github.com/features/copilot","pricing":"https://github.com/features/copilot/plans","price":"Pro $10/mo; Pro+ $39/mo; Max $100/mo","free":"Free plan: $0","about":"AI pair programmer in VS Code, JetBrains and GitHub.","why":"Cheapest serious paid plan ($10/mo) and a real free tier, works in the editor you already use."},
  {"name":"Cursor","url":"https://cursor.com","pricing":"https://cursor.com/pricing","price":"Plus $8/mo; Premium $30/mo; Super $100; Ultra $200; Teams $30/user","free":"Free: $0 with limited agent requests","about":"AI-first code editor with agents."},
  {"name":"Windsurf","url":"https://windsurf.com","pricing":"https://windsurf.com/pricing","price":"Pro $20/mo; Max $200/mo; Teams $80/mo + $40/seat","free":"Free: $0","about":"Agentic AI IDE."},
  {"name":"Claude (Pro)","url":"https://claude.ai","pricing":"https://claude.com/pricing","price":"Pro $20/mo ($17 yearly); Max from $100/mo","free":"Free plan: $0","about":"Strong coding model for chat-based and agentic coding."},
  {"name":"Bolt","url":"https://bolt.new","pricing":"https://bolt.new/pricing","price":"Pro $25/mo; Teams $30/member/mo","free":"Free: 300K tokens/day, 1M/month","about":"Build full-stack web apps from a prompt in the browser."},
  {"name":"v0","url":"https://v0.app","pricing":"https://v0.app/pricing","price":"Team $30/user/mo; Business $100/user/mo","free":"Free: $0 with daily credits","about":"Vercel's AI app/UI builder, deploys to Vercel."},
  {"name":"Lovable","url":"https://lovable.dev","pricing":"https://lovable.dev/pricing","price":"check site","free":"Free: 5 build credits/day (up to 30/mo)","about":"Prompt-to-app builder for non-developers."},
 ]},
 {"id":"images","name":"Images","need":"Generate or design images","best":"Leonardo","free":["Leonardo","Krea","Ideogram"],"tools":[
  {"name":"Leonardo","url":"https://leonardo.ai","pricing":"https://leonardo.ai/pricing","price":"Essential $12/mo; Premium $30; Ultimate $60","free":"Free: 150 fast tokens/day","about":"Image and video generation with presets and custom model training.","why":"Generous daily free tokens and a $12 entry plan; Premium adds unlimited relaxed image generation."},
  {"name":"Midjourney","url":"https://www.midjourney.com","pricing":"https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans","price":"Basic $10/mo ($8 yearly); Standard $30 ($24); Pro $60 ($48); Mega $120 ($96)","free":"No free plan (subscription only)","about":"Top-tier artistic image quality, plus video."},
  {"name":"Ideogram","url":"https://ideogram.ai","pricing":"https://ideogram.ai/pricing","price":"Plus $20/mo ($15 yearly); Pro $60 ($42); Team $30/user ($20)","free":"Free weekly credits for eligible accounts","about":"Best-in-class text rendering in images (logos, posters)."},
  {"name":"Krea","url":"https://www.krea.ai","pricing":"https://www.krea.ai/pricing","price":"From $35/mo ($21 yearly); $105 ($63); $200 ($160)","free":"Free: 100 units/day","about":"Real-time generation, many models, upscaling."},
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
  {"name":"Pitch","url":"https://pitch.com","pricing":"https://pitch.com/pricing","price":"Plus €10/mo; Team €15/mo; Business €20/mo","free":"Free forever: unlimited presentations","about":"Collaborative presentation software with AI credits on paid plans.","why":"Free plan with unlimited presentations, and the cheapest paid tier at €10/mo."},
  {"name":"Beautiful.ai","url":"https://www.beautiful.ai","pricing":"https://www.beautiful.ai/pricing","price":"Pro $14.50/mo (billed annually); Team $40/user/mo yearly ($50 monthly)","free":"14-day free trial","about":"Smart Slide layouts that auto-format as you type; PowerPoint import/export."},
  {"name":"Plus AI","url":"https://plusai.com","pricing":"https://plusai.com/pricing","price":"Basic $10/user/mo yearly ($15 monthly); Pro $20 ($25); Team $30 ($40); Max $200 ($240)","free":"7-day free trial (card required)","about":"AI slide generation inside Google Slides and PowerPoint."},
  {"name":"SlidesAI","url":"https://www.slidesai.io","pricing":"https://www.slidesai.io/pricing","price":"$10/mo (billed $120/yr); $20.83/mo (billed $250/yr)","free":"Basic $0: 12 presentations/year","about":"Turns text into Google Slides presentations."},
  {"name":"Gamma","url":"https://gamma.app","pricing":"https://gamma.app/pricing","price":"check site","free":"check site","about":"AI-generated decks, docs and web pages from a prompt."},
  {"name":"Canva","url":"https://www.canva.com","pricing":"https://www.canva.com/pricing/","price":"check site","free":"Free plan available","about":"Design tool with presentation templates and AI features."},
 ]},
 {"id":"assistants","name":"AI Assistants","need":"Chat with an AI assistant","best":"Le Chat (Mistral)","free":["ChatGPT","Claude","Google Gemini"],"tools":[
  {"name":"Le Chat (Mistral)","url":"https://chat.mistral.ai","pricing":"https://mistral.ai/pricing","price":"Pro $14.99/mo; Team $24.99/user/mo (excl. tax)","free":"Free plan with limited access","about":"Mistral's assistant with web search, image generation and the Vibe coding agent.","why":"Lowest-priced pro tier among the major assistants ($14.99/mo), plus a free plan."},
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
  T("Buffer","https://buffer.com","https://buffer.com/pricing","Essentials $5/mo per channel ($60/yr billed yearly); Team $10/mo per channel","Free plan available","Schedule social posts with an AI assistant.","Real social scheduling from $5/mo, the cheapest entry in this category."),
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
  T("Fireflies","https://fireflies.ai","https://fireflies.ai/pricing","Pro $18/seat/mo ($10 billed annually); Business $29 ($19)","Free forever: $0","AI meeting notes and transcription.","Free-forever tier plus a $10/mo (yearly) Pro, the cheapest full-featured meeting assistant here."),
  T("Fathom","https://www.fathom.ai","https://www.fathom.ai/pricing","From $15/user/mo; Business $25-$34/user/mo","Free plan","AI meeting recorder and summaries."),
  T("Otter","https://otter.ai","https://otter.ai/pricing","Pro $16.99/user/mo ($8.33 yearly); Business $30 ($19.99 yearly)","Basic: free forever","Meeting transcription and notes."),
  T("Motion","https://www.usemotion.com","https://www.usemotion.com/pricing","Pro AI $19/seat/mo; Business AI $29/seat/mo","Free trial","AI calendar that auto-schedules your tasks."),
  T("Reclaim","https://reclaim.ai","https://reclaim.ai/pricing","$10/seat/mo for small teams",CK,"Smart calendar scheduling for habits and tasks."),
  T("ClickUp","https://clickup.com","https://clickup.com/pricing","Unlimited $10/user/mo ($7 yearly); Business $19 ($12 yearly)","Free plan","Project management with built-in AI."),
  T("Taskade","https://www.taskade.com","https://www.taskade.com/pricing","Pro $10/mo (yearly, 10 users incl.); $25; $100; $250","Free: $0","Projects, notes and AI agents in one workspace."),
  T("Superhuman","https://superhuman.com","https://superhuman.com/plans","$12/member/mo yearly ($15 monthly); $33 ($40)","Free: $0","AI assistance across your apps (includes Grammarly)."),
  T("Zapier","https://zapier.com","https://zapier.com/pricing","Professional from $19.99/mo; Team from $69/mo","Free forever: 100 tasks/mo","Automate workflows between 7,000+ apps with AI."),
  T("Notion AI","https://www.notion.com","https://www.notion.com/pricing","Plus $10/member/mo; Business $20/member/mo","Free plan: $0 (AI trial only)","AI writing inside your notes, docs and wikis."),
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
 "InVideo":(20,10,None),"Claude":(20,17,None),"Claude (Pro)":(20,17,None),"Grammarly":(12,None,None),"Notion AI":(10,None,None),"Copy.ai":(29,24,None),"GitHub Copilot":(10,None,None),
 "Cursor":(8,None,None),"Windsurf":(20,None,None),"Bolt":(25,None,None),"v0":(30,None,None),"Leonardo":(12,None,None),"Midjourney":(10,8,"Extra Fast GPU time $4/hr"),
 "Ideogram":(20,15,"Pay-as-you-go 1¢ per credit"),"Krea":(35,21,None),"ElevenLabs":(6,None,None),"Suno":(None,8,None),"Murf":(None,None,"$0.01-$0.03 per 1,000 characters (API)"),
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
 "ChatGPT": dict(price="Go $8/mo; Plus $20/mo; Pro from $100/mo (3 tiers); monthly billing (checked 2026-10-15)", free="Free: $0 (unlimited text chats on GPT-6, limits on tools)"),
 "Perplexity": dict(price="Pro $17/mo billed annually; Max $167/mo billed annually; monthly prices not shown (checked 2026-10-15)", free="Free tier available"),
 "Gamma": dict(price="Plus $12/mo ($9/mo yearly, $108/yr); Pro $25 ($18, $216/yr); Ultra $100 ($90, $1,080/yr); per seat (checked 2026-10-15)", free="Free plan available"),
 "Canva": dict(price="Pro $18/mo or $144/yr; Business $25/mo or $250/yr per person (checked 2026-10-15)", free="Free plan available"),
 "Kling AI": dict(pricing="https://kling.ai/app/membership/membership-plan", price="List prices: Standard $10/mo ($79.20/yr); Pro $37/mo ($293.04/yr); Premier $207/mo ($1,490/yr); Ultra+ $619/mo ($4,457/yr). Promotional: Standard $6.99 first month then $8.8/mo; Pro $25.99 first month then $32.56/mo; Premier $135 first month then $181.99/mo; Ultra+ $402 first month then $544.99/mo (checked 2026-10-17)", free="Basic: free", about="Text/image-to-video generator."),
}
for _c in CATEGORIES:
    for _t in _c["tools"]:
        if _t["name"] in _BV: _t.update(_BV[_t["name"]])
PRICE_TABLE.update({"ChatGPT":(8,None,None),"Perplexity":(None,17,None),"Gamma":(12,9,None),"Canva":(18,12,None),"Kling AI":(10,6.60,None)})

# Browser-verified 2026-10-15, batch 2 (official pages)
_BV2 = {
 "Captions": dict(price="Max $24.99/mo; Frontier $69.99/mo (iOS prices per page footnote)", free="Free plan available"),
 "Jasper": dict(price="Pro $59/seat/mo", free="No free plan; 7-day free trial"),
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
PRICE_TABLE.update({"Captions":(24.99,None,None),"Jasper":(59,None,None),"Lovable":(25,21,None),"Qodo":(None,None,"$0.012 per credit"),"Recraft":(None,10,None),
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
 "ElevenLabs": dict(price="Starter $6/mo ($5/mo billed yearly); Creator $22 ($18.33); Pro $99 ($82.50); Scale $299 ($249.17); Business $990 ($825). Promotional: Creator $11 first month (50% off)"),
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
}
# Snapshot diffs known to be artifacts, not real changes (never shown).
PRICE_SKIP = {
 "2026-10-15|Kling AI": "The 2026-10-14 snapshot was rewritten with text from the 2026-10-17 check, so this diff runs backwards in time.",
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
