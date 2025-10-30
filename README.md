# SimPatient — Tele‑visit Role‑play

See docs/ for site.


## Publish on GitHub Pages (in minutes)
1) Create a new GitHub repo (e.g., `simpatient-exercise`), upload contents.  
2) In **Settings → Pages**, choose **Deploy from a branch**, **Branch: `main`**, **Folder: `/docs`**.  
3) Optional: generate QR codes
```bash
pip install qrcode[pil] pillow
python tools/make_qr_images.py   # edit tools/qr_config.json first
```
4) Share the link `https://<username>.github.io/<repo>/copyblocks.html` during the workshop.
