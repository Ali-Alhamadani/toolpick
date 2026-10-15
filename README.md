# ToolPick
Needs-based AI tool finder (video, writing, coding, images, audio) with verified prices, a best-value pick and free alternatives.
- `tools.py` — all data (edit prices here; set `CHECKED` date; use "check site" if unverified)
- `build.py` — `BASE=https://<site> python3 build.py` writes static files into `public/`
- Live: https://toolpick-ai-alhamdaniali10-7277.vercel.app
- Deploy: upload `public/` files to Vercel project `toolpick-ai` (target production, framework none) via Vercel create_deployment.
