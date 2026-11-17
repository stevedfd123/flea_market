#!/usr/bin/env python3
"""Build index.html: the Ceylon Flea Market landing page.

Sources: noor/index.html (globe + motion engine) and market-cells/*.jpg.
The build re-brands the page, drops every letter/text block, inlines the
photos as data URIs and writes a single self-contained file.
"""
import base64
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "noor", "index.html")
CELLS = os.path.join(ROOT, "market-cells")
OUT = os.path.join(ROOT, "index.html")

html = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- head / meta
html = html.replace("<title>ostra · For Noor</title>", "<title>Ceylon Flea Market — Good things come around again</title>")
html = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Ceylon Flea Market: a happy place for pre-loved treasures, local makers and the little stories that bring us together. Colombo, Sri Lanka.">',
              html)
html = html.replace('<meta name="theme-color" content="#E4DED3">', '<meta name="theme-color" content="#294633">')

# ---------------------------------------------------------------- palette
html = html.replace("--paper: #E4DED3;", "--paper: #F8F6EF;")
html = html.replace("--stone: #C9C3B8;", "--stone: #DCDED2;")
html = html.replace("--ink: #1B1815;", "--ink: #203B2C;")
html = html.replace("--body: #5E574F;", "--body: #4C5A4E;")
html = html.replace("--oxblood: #8A0B12;", "--oxblood: #294633;")
html = html.replace("--oxblood-deep: #6E070D;", "--oxblood-deep: #1D3325;")
html = html.replace("::selection { background: var(--oxblood); color: #F4EEE6; }",
                    "::selection { background: var(--green, #294633); color: #FFFDF6; }")
html = html.replace("const PAPER = new THREE.Color(0xE4DED3);", "const PAPER = new THREE.Color(0xF8F6EF);")
html = html.replace("background: rgba(228, 222, 211, 0.78);", "background: rgba(248, 246, 239, 0.82);")
html = html.replace("background: radial-gradient(circle at 50% 45%, #d3c8b8, #c4b6a2 70%);",
                    "background: radial-gradient(circle at 50% 45%, #e3e6d9, #cfd6c6 70%);")
html = html.replace("rgba(138, 11, 18, 0.34)", "rgba(189, 103, 70, 0.42)")
html = html.replace("box-shadow: 0 1px 2px rgba(27, 24, 21, 0.12);", "box-shadow: 0 1px 2px rgba(32, 59, 44, 0.14);")
html = html.replace("box-shadow: 0 30px 80px rgba(27, 24, 21, 0.28);", "box-shadow: 0 30px 80px rgba(32, 59, 44, 0.30);")
html = html.replace("background: #FBF8F3;\n    color: #1B1815;", "background: #F8F6ED;\n    color: #203B2C;")
html = html.replace("color: #FBF8F3;\n    background: rgba(27, 24, 21, 0.55);", "color: #FFFDF6;\n    background: rgba(32, 59, 44, 0.6);")
html = html.replace(".cell-close {\n    position: absolute;\n    top: 12px;\n    right: 12px;\n    width: 34px;\n    height: 34px;\n    border-radius: 50%;\n    border: 0;\n    background: #FBF8F3;\n    color: #1B1815;",
                    ".cell-close {\n    position: absolute;\n    top: 12px;\n    right: 12px;\n    width: 34px;\n    height: 34px;\n    border-radius: 50%;\n    border: 0;\n    background: #F8F6ED;\n    color: #203B2C;")
html = html.replace("border-color: rgba(27, 24, 21, 0.42); color: #3A342E;", "border-color: rgba(32, 59, 44, 0.42); color: #294633;")

# fonts: keep the site's own families, drop the script signature face
html = html.replace("""    font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;""",
                    """    font-family: "DM Sans", "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;""")

# ---------------------------------------------------------------- CSS: new hero styles
HERO_CSS = """
  /* ---------- brand hero (replaces the letter) ---------- */
  .hero { padding: 64px 0 0; }
  .hero .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font-size: 10px;
    line-height: 1.4;
    letter-spacing: 0.15em;
    font-weight: 700;
    color: #9A563E;
  }
  .hero .eyebrow-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #BD6746;
    flex: none;
  }
  .hero h1 {
    margin: 14px 0 0;
    font-family: "DM Serif Display", Georgia, serif;
    font-weight: 400;
    font-size: clamp(38px, 5.4vw, 76px);
    line-height: 1.03;
    letter-spacing: -0.025em;
    color: var(--ink);
  }
  .hero h1 em { font-style: italic; color: #BD6746; }
  .hero .hero-lede {
    margin: 20px 0 0;
    max-width: 92%;
    font-size: clamp(14px, 1.04vw, 17px);
    line-height: 1.55;
    color: var(--body);
  }
  .hero-actions { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 30px; }
  .hero-action {
    height: 46px;
    padding: 0 28px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 13.5px;
    font-weight: 600;
    letter-spacing: -0.005em;
    transition: background-color .25s, color .25s, border-color .25s, transform .25s;
  }
  .hero-action:hover { transform: translateY(-2px); }
  .hero-action.primary { background: var(--ink); color: #FFFDF6; }
  .hero-action.primary:hover { background: var(--oxblood-deep); }
  .hero-action.ghost { border: 1px solid rgba(41, 70, 51, 0.34); color: var(--ink); }
  .hero-action.ghost:hover { border-color: var(--ink); }
  .hero-actions .arrow { font-size: 15px; line-height: 1; }

  .globe-hint {
    margin: 14px auto 0;
    width: clamp(300px, 45vw, 860px);
    text-align: center;
    font-size: 10.5px;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: #8A9488;
  }

  /* ---------- work row (market stalls) ---------- */
  .work-head {
    padding-top: 92px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 24px;
  }
  .work-head h2 {
    margin: 12px 0 0;
    font-family: "DM Serif Display", Georgia, serif;
    font-weight: 400;
    font-size: clamp(28px, 3vw, 44px);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: var(--ink);
  }
  .work-head h2 em { font-style: italic; color: #BD6746; }
  .work-head .work-link {
    font-size: 12px;
    font-weight: 700;
    color: var(--ink);
    border-bottom: 1px solid currentColor;
    padding-bottom: 6px;
    white-space: nowrap;
  }

  /* ---------- sign-off ---------- */
  .signoff { padding: 72px 0 96px; }
  .signoff .thanks {
    margin: 0;
    font-size: clamp(14px, 1.04vw, 17px);
    line-height: 1.5;
    color: var(--body);
    max-width: 92%;
  }
  .footer-line {
    margin-top: 40px;
    padding-top: 22px;
    border-top: 1px solid var(--line, #DCDED2);
    display: flex;
    flex-wrap: wrap;
    gap: 10px 26px;
    justify-content: space-between;
    font-size: 10px;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: #8A9488;
  }
  .footer-line a:hover { color: var(--ink); }

  @media (max-width: 820px) {
    .hero { padding-top: 44px; }
    .hero .hero-lede { max-width: 100%; }
    .globe-hint { width: calc(100vw - 24px); margin-top: 10px; }
    .work-head { padding-top: 62px; display: block; }
    .work-head .work-link { display: inline-block; margin-top: 14px; }
    .signoff { padding: 52px 0 72px; }
  }
"""
html = html.replace("  /* ---------- captions (removed at boot) ---------- */", HERO_CSS + "\n  /* ---------- captions (removed at boot) ---------- */")

# ---------------------------------------------------------------- markup
NEW_BODY_START = """<header class="masthead col">
  <a class="logo" href="#top" aria-label="Ceylon Flea Market, home">
    <svg width="34" height="30" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M24 2.5 28.2 14l11.1-5.4-5.4 11.1L45.5 24 33.9 28.2l5.4 11.1-11.1-5.4L24 45.5l-4.2-11.6-11.1 5.4 5.4-11.1L2.5 24l11.6-4.3-5.4-11.1L19.8 14 24 2.5Z" fill="#294633"/>
      <circle cx="24" cy="24" r="4.5" fill="#EDC878"/>
    </svg>
    <span class="wordmark">ceylon <small>flea market</small></span>
  </a>
</header>

<section class="hero col" id="top">
  <div class="eyebrow"><span class="eyebrow-dot"></span> COLOMBO'S COMMUNITY FLEA MARKET</div>
  <h1>Good things<br><em>come around</em><br>again.</h1>
  <p class="hero-lede">Pre-loved treasures, local makers and the little stories that bring us together. Every stall holds a story waiting to be discovered.</p>
  <div class="hero-actions">
    <a class="hero-action primary" href="#marketplace">Explore the market <span class="arrow">↗</span></a>
    <a class="hero-action ghost" href="#marketplace">Sell your treasures <span class="arrow">→</span></a>
  </div>
</section>

<div class="globe-wrap" id="globeWrap">
  <div class="globe-fallback"></div>
  <canvas id="globeCanvas" role="img"
    aria-label="A slowly turning globe of photographs from the market: pre-loved clothes on rails, vintage books and records, handmade jewellery, clay cups of tea, terracotta pots and stalls under the trees. Drag to spin it, click a photo to enlarge it."></canvas>
</div>
<p class="globe-hint">DRAG TO SPIN · CLICK A PHOTO TO ENLARGE</p>

<section class="col" id="marketplace">
  <div class="work-head">
    <div>
      <div class="eyebrow"><span class="eyebrow-dot"></span> FROM THE STALLS</div>
      <h2>What you'll <em>find.</em></h2>
    </div>
    <a class="work-link" href="#marketplace">View all stalls</a>
  </div>
</section>

<div class="work" id="workRail">
  <div class="work-track" id="workTrack"></div>
</div>

<section class="signoff col">
  <p class="thanks">Come for the treasure hunting. Stay for the neighbours, stories and good energy.</p>
  <div class="buttons">
    <a class="btn btn-primary" href="#top">Back to the market</a>
    <a class="btn btn-ghost" href="#marketplace">See the stalls</a>
  </div>
  <div class="footer-line">
    <span>CEYLON FLEA MARKET · COLOMBO, SRI LANKA</span>
    <a href="#top">EST. 2024</a>
  </div>
</section>
"""

start = html.index('<header class="masthead col">')
end = html.index('<div class="cell-overlay" id="cellOverlay" hidden>')
html = html[:start] + NEW_BODY_START + "\n" + html[end:]

# wordmark styling for the two-part brand
html = html.replace(""".wordmark {
    margin-left: 11px;
    font-size: 18px;
    font-weight: 450;
    letter-spacing: -0.01em;
    color: var(--ink);
  }""",
""".wordmark {
    margin-left: 11px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--ink);
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
  }
  .wordmark small {
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8A9488;
  }""")

# ---------------------------------------------------------------- data: cells + cards
cells = []
for i in range(1, 9):
    with open(os.path.join(CELLS, f"m{i}.jpg"), "rb") as fh:
        cells.append("data:image/jpeg;base64," + base64.b64encode(fh.read()).decode())

cell_js = "const CELL_IMAGES = [\n" + ",\n".join('  "%s"' % c for c in cells) + "\n];\n"

CARDS = [
    ("01", 0, "Preloved racks"),
    ("02", 1, "Books & records"),
    ("03", 2, "Handmade jewellery"),
    ("04", 3, "Tea & short eats"),
    ("05", 4, "Plants & pots"),
    ("06", 5, "Ceramics corner"),
    ("07", 6, "The market day"),
    ("08", 7, "Baskets & linen"),
]

# replace the old SHEETS + WORK sheet + CARDS block with data-URI versions
start = html.index("const SHEETS = [")
end = html.index("const reduceMotion =")
new_data = cell_js + """
/* Each cell is a single photo; globe tiles and stall cards sample the same set. */
const SHEETS = CELL_IMAGES;

/* Cards: full-cell quadrants so every card shows one complete photo. */
const SHEET_QUAD = "0% 0%";
const CARDS = [
""" + ",\n".join('  { n: "%s", sheet: CELL_IMAGES[%d], pos: SHEET_QUAD, name: "%s" }' % (n, i, t) for n, i, t in CARDS) + """
];

""" + "const reduceMotion ="
html = html[:start] + new_data + html[end + len("const reduceMotion ="):]

open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html), "bytes")
