"""Converte os PNGs de icons/png/ em SVGs vetoriais brancos em icons/.

Corre:  python tools/png_to_svg.py   (precisa de: pip install potracer pillow)
O ícone é o que for opaco no PNG; em tema claro do GitHub fica cinzento escuro.
"""
from pathlib import Path

import numpy as np
import potrace
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "icons" / "png", ROOT / "icons"

STYLE = ("<style>path{fill:#ffffff}"
         "@media (prefers-color-scheme: light){path{fill:#1f2328}}</style>")

# tamanho relativo de cada ícone (1 = ocupa a caixa toda); encolhe mantendo-o centrado
SCALE = {"email": 0.9, "portfolio": 0.75}


def trace(png):
    im = Image.open(png).convert("RGBA")
    rgba = np.asarray(im).astype(float)
    alpha = rgba[..., 3] / 255
    dark = 1 - rgba[..., :3].mean(axis=2) / 255
    # transparente -> usa o alfa; fundo opaco -> usa o que é escuro
    mask = alpha > 0.5 if alpha.min() < 0.5 else dark > 0.5
    plist = potrace.Bitmap(~mask).trace(  # potracer desenha os pixels False
        turdsize=4, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    for curve in plist:
        s = curve.start_point
        d.append(f"M{s.x:.2f} {s.y:.2f}")
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{seg.c.x:.2f} {seg.c.y:.2f}L{seg.end_point.x:.2f} {seg.end_point.y:.2f}")
            else:
                d.append(f"C{seg.c1.x:.2f} {seg.c1.y:.2f} {seg.c2.x:.2f} {seg.c2.y:.2f} "
                         f"{seg.end_point.x:.2f} {seg.end_point.y:.2f}")
        d.append("Z")
    w, h = im.size
    k = SCALE.get(png.stem, 1)
    pw, ph = w / k, h / k
    vb = f"{(w - pw) / 2:.1f} {(h - ph) / 2:.1f} {pw:.1f} {ph:.1f}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="{vb}" '
            f'role="img" aria-label="{png.stem}">{STYLE}<path fill-rule="evenodd" d="{"".join(d)}"/></svg>\n')


if __name__ == "__main__":
    for png in sorted(SRC.glob("*.png")):
        (OUT / f"{png.stem}.svg").write_text(trace(png), encoding="utf-8")
        print(f"icons/{png.stem}.svg")
