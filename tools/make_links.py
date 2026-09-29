"""Gera os "links" do perfil (ícone + nome) como SVGs em icons/link-<nome>.svg.

O texto vai dentro do SVG para ficar cinzento/branco (no README o GitHub pintava-o de azul).
Corre:  python tools/make_links.py
"""
import re
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "icons"

# ordem igual à do portfolio
LINKS = [
    ("linkedin", "LinkedIn"),
    ("medium", "Medium"),
    ("portfolio", "Portfolio"),
    ("tryhackme", "TryHackMe"),
    ("email", "Email"),
]

H, ICON, GAP, FONT = 34, 22, 8, 18
MEASURE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", FONT)


def icon_parts(name):
    svg = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    paths = "".join(re.findall(r"<path[^>]*/>", svg))
    return vb, paths


def make(name, label):
    vb, paths = icon_parts(name)
    text_w = MEASURE.getlength(label)
    w = round(ICON + GAP + text_w + 4)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{label}">
<style>
  path {{ fill: #ffffff; }}
  text {{ fill: #c9d1d9; font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; font-size: {FONT}px; }}
  @media (prefers-color-scheme: light) {{ path {{ fill: #1f2328; }} text {{ fill: #1f2328; }} }}
</style>
<svg x="0" y="{(H - ICON) / 2}" width="{ICON}" height="{ICON}" viewBox="{vb}">{paths}</svg>
<text x="{ICON + GAP}" y="{H / 2 + FONT * 0.35:.1f}">{label}</text>
</svg>
""", w


if __name__ == "__main__":
    for name, label in LINKS:
        svg, w = make(name, label)
        (ICONS / f"link-{name}.svg").write_text(svg, encoding="utf-8")
        print(f"icons/link-{name}.svg", w)
