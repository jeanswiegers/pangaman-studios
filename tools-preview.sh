#!/usr/bin/env bash
# Full-page previews with headless Chrome: render tall, then trim the empty canvas below the footer.
cd "$(dirname "$0")"; mkdir -p preview
shoot() { # page width name
  google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=$2,9000 --screenshot="preview/$3.png" "file://$PWD/$1" >/dev/null 2>&1
  python3 - "preview/$3.png" <<'PY'
import sys
from PIL import Image
p = sys.argv[1]; im = Image.open(p).convert("RGB"); w, h = im.size; px = im.load()
bottom = px[w // 2, h - 1]
y = h - 1
while y > 0 and all(px[x, y] == bottom for x in range(0, w, 7)): y -= 1
im.crop((0, 0, w, y + 1)).save(p, optimize=True); print(p, (w, y + 1))
PY
}
for p in index coreclr-ready docs changelog support privacy how-we-build 404; do shoot $p.html 1280 $p; done
shoot index.html 390 index-mobile; shoot coreclr-ready.html 390 coreclr-ready-mobile
