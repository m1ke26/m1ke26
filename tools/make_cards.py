"""Gera os cartões SVG dos projetos em cards/.

Edita a lista PROJECTS e corre:  python tools/make_cards.py
Se "cover" apontar para uma imagem (jpg/png), é embutida no cartão;
caso contrário é desenhada uma capa placeholder.
"focus" (0 = topo, 1 = fundo) escolhe que parte vertical da imagem aparece.
"""
import base64
import html
import io
import re
import textwrap
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
ACCENT = "#d4d4d4"
ACCENT_LIGHT = "#404040"

PROJECTS = [
    {"file": "nutricode", "title": "NutriCode", "desc": "Mobile app that scans product barcodes and flags harmful ingredients and allergens.", "tags": ["Dart", "Flutter"], "cover": "assets/covers/es.png", "focus": 0.3},
    {"file": "minix-grand-prix", "title": "MINIX Grand Prix", "desc": "Racing game for MINIX with custom timer, keyboard, mouse, video and RTC drivers.", "tags": ["C"], "cover": "assets/covers/lcom.png"},
    {"file": "real-estate-db", "title": "Real Estate Agency DB", "desc": "Database for a real estate agency, from UML model to a SQLite schema and data.", "tags": ["SQL", "SQLite"], "cover": "assets/covers/bd.png"},
    {"file": "gymmaxxing", "title": "GymMaxxing", "desc": "Gym web app with class scheduling, trainer profiles, reviews and membership tiers.", "tags": ["PHP", "JavaScript", "HTML", "CSS"], "cover": "assets/covers/ltw.png", "focus": 0.1},
]

SHOW_TAGS = False  # mostra as tags (linguagens) nos cartões

SANS = "font-family:ui-sans-serif,-apple-system,'Segoe UI',system-ui,sans-serif"


def cover_markup(cover, title, uid, focus=0.5):
    if cover:
        # recorta ao formato da capa (340x140, a 2x) e comprime, para o SVG não ficar enorme
        im = ImageOps.fit(Image.open(ROOT / cover).convert("RGB"), (680, 280), Image.LANCZOS, centering=(0.5, focus))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80)
        data = base64.b64encode(buf.getvalue()).decode()
        return (f'<g clip-path="url(#imgClip_{uid})"><image href="data:image/jpeg;base64,{data}" '
                f'x="0" y="0" width="340" height="140" preserveAspectRatio="xMidYMid slice"/></g>')
    return (f'<g clip-path="url(#imgClip_{uid})">'
            f'<rect x="0" y="0" width="340" height="140" fill="url(#coverGrad_{uid})"/>'
            f'<text x="170" y="78" text-anchor="middle" style="{SANS};font-size:13px;font-weight:700;fill:#ffffffb3">[imagem de capa]</text></g>')


def make_card(p):
    uid = re.sub(r"\W+", "_", p["file"])
    title = html.escape(p["title"])
    lines = textwrap.wrap(p["desc"], 48)[:2]
    desc = "".join(
        f'<text x="18" y="{190 + 17 * i}" class="desc" style="{SANS};font-size:11.5px">{html.escape(l)}</text>'
        for i, l in enumerate(lines))
    pills, x = [], 18
    for tag in p["tags"] if SHOW_TAGS else []:
        w = max(52, 7 * len(tag) + 24)
        pills.append(f'<rect x="{x}" y="218" width="{w}" height="22" rx="11" class="pill"/>'
                     f'<text x="{x + w / 2}" y="233" text-anchor="middle" class="accent" '
                     f'style="font-size:10px;font-weight:700">{html.escape(tag)}</text>')
        x += w + 8
    # sem tags, sobe o rodapé e encolhe o cartão para não ficar um buraco
    off = 0 if pills else 30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="360" height="{300 - off}" viewBox="0 0 360 {300 - off}" role="img" aria-label="{title}">
<defs>
  <style>
    text {{ font-family: ui-monospace, 'Cascadia Code', 'JetBrains Mono', Consolas, monospace; fill: #ffffff; }}
    .card-bg {{ fill: #111111; stroke: #ffffff1f; }}
    .title {{ fill: #ffffff; }}
    .desc {{ fill: #a3a3a3; }}
    .accent {{ fill: {ACCENT}; }}
    .pill {{ fill: #1c1c1c; stroke: #ffffff14; }}
    .divider {{ stroke: #ffffff14; }}
    @media (prefers-color-scheme: light) {{
      text {{ fill: #1f2328; }}
      .card-bg {{ fill: #ffffff; stroke: #d0d7de; }}
      .title {{ fill: #1f2328; }}
      .desc {{ fill: #59636e; }}
      .accent {{ fill: {ACCENT_LIGHT}; }}
      .pill {{ fill: #f6f8fa; stroke: #d0d7de; }}
      .divider {{ stroke: #d0d7de; }}
    }}
  </style>
  <linearGradient id="coverGrad_{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#3a3a3a"/><stop offset="1" stop-color="#0a0a0a"/>
  </linearGradient>
  <clipPath id="imgClip_{uid}"><path d="M0 14 a14 14 0 0 1 14 -14 h312 a14 14 0 0 1 14 14 v126 h-340 z"/></clipPath>
</defs>
<g transform="translate(10, 10)">
<rect x="0.5" y="0.5" width="339" height="{279 - off}" rx="14" class="card-bg"/>
{cover_markup(p["cover"], title, uid, p.get("focus", 0.5))}
<text x="18" y="166" class="title" style="{SANS};font-size:16px;font-weight:800">{title}</text>
{desc}
{"".join(pills)}
<line x1="18" y1="{252 - off}" x2="322" y2="{252 - off}" class="divider"/>
<text x="18" y="{270 - off}" class="accent" style="{SANS};font-size:11.5px;font-weight:700">View project &#8594;</text>
</g>
</svg>
"""


if __name__ == "__main__":
    out = ROOT / "cards"
    out.mkdir(exist_ok=True)
    for p in PROJECTS:
        (out / f"{p['file']}.svg").write_text(make_card(p), encoding="utf-8")
        print("cards/" + p["file"] + ".svg")
