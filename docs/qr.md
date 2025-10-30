---
layout: page
title: QR setup
permalink: /qr.html
---

## QR codes for workshop handouts

1. Edit `tools/qr_config.json` to set your GitHub Pages **base_url**, e.g.  
   `https://<your-username>.github.io/<repo>`
2. Run:
```
pip install qrcode[pil] pillow
python tools/make_qr_images.py
```
3. The script writes PNGs to `docs/assets/qr/` for these targets:
   - **copyblocks** → `copyblocks.html`
   - **personas** → `personas.html`
   - **prompts** → `prompts.html`

Place the PNGs on slides or handouts. Commit, push, and your site will serve the images.
