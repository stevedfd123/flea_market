"Noor" pitch page — ostra studio
================================

Open:   /noor/            (e.g. http://127.0.0.1:8000/noor/)
Serve:  python3 serve.py 8000   (from the repo root)

File:   noor/index.html          single page: HTML + CSS + JS
        noor/three.module.js     three.js 0.160.0, vendored (no CDN dependency)

What it does
------------
* Photo globe built from 46 curved, rounded tiles (9 latitude bands) sampled
  from 8 photo sheets, each tile showing one quadrant of a sheet.
* Load intro: the globe rises squashed from the bottom, inflates and spins in,
  then tiles fade onto the surface ring by ring, bottom to top (~2.5s).
* Scroll spins the globe; drag spins and tilts it with momentum.
* Click a globe cell  -> that cell bursts into ~42 curved shards that push
  outward and dissolve while a ripple expands; the full photograph then opens
  enlarged. Close with the x, the backdrop or Escape.
* Click a work card   -> the card's quadrant bursts into 30 shards and the cell
  dissolves, then the photograph opens enlarged.
* Auto-sliding work row (one card every 2.4s) and the text reveals.

Notes
-----
* Captions are stripped at boot: every element carrying data-cap has the
  attribute removed and <html> gets .no-caps, so no caption text is drawn.
* Photos come from images.higgs.ai (CORS-enabled, needed for WebGL textures)
  and are used live, never re-hosted. If those URLs are unreachable the globe
  tiles stay blank and work cards stay stone-coloured — the layout is intact.
* Base64 photos are NOT inlined here: the sheets are several MB each and the
  page needs the proxied URLs for CORS anyway.
