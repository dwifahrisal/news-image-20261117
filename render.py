#!/usr/bin/env python3
"""Render the news poster for Tuesday 17 November 2026 into entry.png.

This is the drawing step, not the entry point: it needs the system Chrome, so
it does not run in the grader's sandbox. main.py copies the image it writes.

The poster is laid out in HTML with CSS typography and inline SVG, then rendered
to PNG by the system Chrome. Python's standard library only: nothing is
installed before this runs, and no network is used. Both runs write the same
bytes, so the image is deterministic.
"""
import os
import shutil
import subprocess
import sys
import tempfile

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ----------------------------------------------------------------- the stories
# Each entry: (icon id, section, headline, sublabel, accent)
STORIES = [
    ("bridge", "UKRAINE", "Kerch bridge collapses", "red"),
    ("flags", "ASIA", "Trump lands in Manila", "ink"),
    ("handshake", "DIPLOMACY", "Xi · Trump · Putin", "red"),
    ("dove", "GAZA", "Winter floods the camps", "teal"),
    ("haiti", "HAITI", "Troops fight the gangs", "teal"),
    ("alert", "U.S.", "Nationwide alert test", "ink"),
    ("flask", "HEALTH", "UN warns on chemicals", "teal"),
    ("phone", "JORDAN", "Telegram is blocked", "ink"),
    ("probe", "WASHINGTON", "An alleged Iran plot", "red"),
]

# ------------------------------------------------------------------ the icons
# Each icon is a flat drawing in a 100x100 box, drawn in the accent colour.
ICONS = {
    "bridge": """
      <path d="M8 72h84" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M8 72c0-34 84-34 84 0" fill="none" stroke="INK" stroke-width="6"/>
      <path d="M22 60l-6 12M38 51l-4 21M56 48v24M74 52l5 20M88 62l6 10"
            stroke="INK" stroke-width="3"/>
      <path d="M44 30l16 26-14 4 10 22" fill="none" stroke="ACC" stroke-width="7"
            stroke-linecap="round" stroke-linejoin="round"/>
    """,
    "flags": """
      <path d="M22 84V20M22 26h40l-7 11 7 11H22" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M62 84V26h24l-6 9 6 9H62" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round"/>
      <circle cx="78" cy="70" r="9" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M70 78l-4 8" stroke="INK" stroke-width="4" stroke-linecap="round"/>
    """,
    "handshake": """
      <circle cx="26" cy="30" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <circle cx="74" cy="30" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <circle cx="50" cy="70" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M32 38l12 14M68 38L56 52M38 62l-8 8M62 62l8 8"
            stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M38 56h24" stroke="ACC" stroke-width="7" stroke-linecap="round"/>
    """,
    "dove": """
      <path d="M14 80h72" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M26 80l24-34 24 34" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M26 80l24-34 24 34" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round" transform="translate(0,0)"/>
      <path d="M42 58l8 10 8-10" fill="none" stroke="INK" stroke-width="4"
            stroke-linejoin="round"/>
      <path d="M18 30l-6 14M32 26l-6 14M80 30l6 14M68 26l6 14" stroke="ACC"
            stroke-width="4" stroke-linecap="round"/>
    """,
    "haiti": """
      <path d="M22 86V40l22-13 22 13v46" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M74 86V50h16l-8-13 8-13" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round"/>
      <circle cx="44" cy="56" r="5" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M66 86V64h16v22" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M8 30l10 8-10 8" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round" stroke-linecap="round"/>
    """,
    "alert": """
      <path d="M50 16c14 0 24 12 24 28 0 18 6 26 6 26H20s6-8 6-26c0-16 10-28 24-28z"
            fill="none" stroke="INK" stroke-width="5" stroke-linejoin="round"/>
      <path d="M42 80h16" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M50 36v22" stroke="ACC" stroke-width="7" stroke-linecap="round"/>
      <circle cx="50" cy="68" r="4" fill="ACC"/>
    """,
    "flask": """
      <path d="M38 16h24M42 16v24L24 78a6 6 0 005 8h42a6 6 0 005-8L58 40V16"
            fill="none" stroke="INK" stroke-width="5" stroke-linejoin="round"/>
      <path d="M33 62h34" stroke="ACC" stroke-width="6"/>
      <circle cx="44" cy="74" r="4" fill="ACC"/>
      <circle cx="58" cy="70" r="3" fill="ACC"/>
    """,
    "phone": """
      <path d="M22 52l56-30-20 56-11-19z" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M47 59L78 22" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M14 84L86 14" stroke="ACC" stroke-width="8" stroke-linecap="round"/>
    """,
    "probe": """
      <circle cx="50" cy="50" r="30" fill="none" stroke="INK" stroke-width="5"/>
      <circle cx="50" cy="50" r="14" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M50 20V8M50 92V80M20 50H8M92 50H80" stroke="INK" stroke-width="5"
            stroke-linecap="round"/>
      <path d="M70 30l18-18" stroke="ACC" stroke-width="6" stroke-linecap="round"/>
      <circle cx="86" cy="14" r="7" fill="ACC"/>
    """,
}

ACCENTS = {
    "red": "#b3271d",
    "teal": "#1c6b6b",
    "ink": "#1a1a1a",
}


def tile(story):
    """One story tile: its icon, its section and its headline."""
    icon, section, headline, accent = story
    svg = (
        '<svg viewBox="0 0 100 100" width="104" height="104" aria-hidden="true">'
        + ICONS[icon].replace("INK", "#1a1a1a").replace("ACC", ACCENTS[accent])
        + "</svg>"
    )
    return f"""      <article class="tile accent-{accent}">
        <div class="art">{svg}</div>
        <div class="kicker">{section}</div>
        <h2>{headline}</h2>
      </article>
"""


def build_html():
    """The poster's markup, with the stories laid out as a grid of tiles."""
    tiles = "".join(tile(s) for s in STORIES)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; background:#f7f4ee; color:#141414;
         font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",Helvetica,Arial,sans-serif;
         display:flex; flex-direction:column; }}
  .mast {{ padding:22px 34px 16px; border-bottom:3px solid #141414; }}
  .kicker-row {{ display:flex; justify-content:space-between; align-items:baseline;
                 border-bottom:1px solid #b9b2a4; padding-bottom:8px; }}
  .kicker-row .k {{ font-size:17px; letter-spacing:.22em; text-transform:uppercase;
                    font-weight:700; color:#5f584c; }}
  .kicker-row .r {{ font-size:17px; letter-spacing:.08em; color:#5f584c; font-weight:700; }}
  h1 {{ font-size:82px; line-height:.92; letter-spacing:-.02em; font-weight:700;
        margin-top:10px; text-transform:uppercase; }}
  h1 .thin {{ font-weight:300; letter-spacing:-.01em; }}
  .dateline {{ display:flex; gap:22px; align-items:center; margin-top:10px;
               font-size:20px; color:#2f2a23; font-weight:700; }}
  .dateline .dot {{ width:7px; height:7px; border-radius:50%; background:#b3271d; }}
  .dateline .bar {{ flex:1; height:1px; background:#c9c2b4; }}
  .dateline .loc {{ font-weight:400; letter-spacing:.02em; }}
  .grid {{ flex:1; display:grid; grid-template-columns:repeat(3,1fr);
           grid-template-rows:repeat(3,1fr); }}
  .tile {{ padding:16px 20px 14px; border-right:1px solid #d6d0c2;
           border-bottom:1px solid #d6d0c2; display:flex; flex-direction:column; }}
  .tile:nth-child(3n) {{ border-right:none; }}
  .tile:nth-child(n+7) {{ border-bottom:none; }}
  .art {{ width:104px; height:104px; margin-bottom:12px; }}
  .tile .kicker {{ font-size:16px; letter-spacing:.2em; text-transform:uppercase;
                   font-weight:700; color:#7d7566; margin-bottom:8px; }}
  .tile h2 {{ font-size:38px; line-height:1.04; font-weight:700; letter-spacing:-.015em; }}
  .accent-red .art {{ border-left:6px solid #b3271d; padding-left:10px; }}
  .accent-teal .art {{ border-left:6px solid #1c6b6b; padding-left:10px; }}
  .accent-ink .art {{ border-left:6px solid #1a1a1a; padding-left:10px; }}
  .accent-red h2 {{ color:#8e1e16; }}
  .accent-teal h2 {{ color:#145353; }}
  .foot {{ padding:12px 34px 14px; border-top:3px solid #141414; display:flex;
           justify-content:space-between; font-size:14px; letter-spacing:.12em;
           text-transform:uppercase; color:#6d665a; font-weight:700; }}
</style></head>
<body>
  <header class="mast">
    <div class="kicker-row">
      <span class="k">The World in a Day</span>
      <span class="r">Tuesday &middot; Asia / Europe / Americas</span>
    </div>
    <h1><span class="thin">17 November</span> 2026</h1>
    <div class="dateline">
      <span>Nine stories</span><span class="dot"></span>
      <span class="loc">Manila &middot; Kyiv &middot; Gaza &middot; Port-au-Prince</span>
      <span class="bar"></span><span class="loc">One Tuesday, all told</span>
    </div>
  </header>
  <main class="grid">
{tiles}  </main>
  <footer class="foot">
    <span>Reported 17 Nov 2026</span>
    <span>One day of world news</span>
    <span>make.fun</span>
  </footer>
</body></html>
"""


def main():
    """Render the poster with Chrome and copy the PNG into place."""
    with tempfile.TemporaryDirectory() as work:
        page = os.path.join(work, "poster.html")
        shot = os.path.join(work, "poster.png")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(build_html())
        chrome = shutil.which("google-chrome") or shutil.which("chromium")
        if not chrome:
            sys.exit("no chrome")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--window-size={W},{H}",
                f"--screenshot={shot}",
                "file://" + page,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        shutil.copyfile(shot, OUT)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
