import os, json, qrcode
cfg = json.load(open('tools/qr_config.json'))
out = 'docs/assets/qr'; os.makedirs(out, exist_ok=True)
base = cfg['base_url'].rstrip('/')
for t in cfg['targets']:
    url = f"{base}/{t['url'].lstrip('/')}"
    img = qrcode.make(url)
    path = os.path.join(out, f"qr_{t['name']}.png")
    img.save(path)
    print("Wrote", path, "->", url)
