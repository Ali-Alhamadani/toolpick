"""ToolPick data. Edit this file, then run build.py.
price: exactly what the official pricing page showed on `checked`; use "check site" if not verifiable.
"""
CHECKED = "2026-10-14"
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
 {"id":"writing","name":"Writing","need":"Write, edit or brainstorm text","best":"Claude","free":["ChatGPT","Gemini","Grammarly"],"tools":[
  {"name":"Claude","url":"https://claude.ai","pricing":"https://claude.com/pricing","price":"Pro $20/mo ($17/mo billed yearly); Max from $100/mo","free":"Free plan: $0","about":"Strong long-form writing, editing and analysis assistant.","why":"Pro is $17-20/mo with a usable free tier, and is excellent at long, natural-sounding drafts."},
  {"name":"ChatGPT","url":"https://chatgpt.com","pricing":"https://chatgpt.com/pricing","price":"check site","free":"Free plan with unlimited text chats on GPT-6 (limits on tools)","about":"General-purpose AI assistant: writing, research, images, voice."},
  {"name":"Google Gemini","url":"https://gemini.google.com","pricing":"https://one.google.com/about/ai-premium","price":"Google AI plans starting at $8/mo (other tiers: check site)","free":"Gemini app is free to use","about":"Google's assistant, integrated with Gmail, Docs and Drive."},
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
