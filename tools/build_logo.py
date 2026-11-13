#!/usr/bin/env python3
"""Compose le logo LIGHT ON BIKE à partir du logo LIGHT ON TRAIL.

Seul le mot du bandeau change : « TRAIL » devient « BIKE », composé en
Lemon Milk (regular, la graisse du mot d'origine) à la même hauteur, sur la
même ligne de base, avec le même interlettrage, aligné à gauche au même
endroit. Symbole, « LIGHT ON », éclair, couleurs et proportions : inchangés.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "assets/fonts/LemonMilk.otf"
WORD = "BIKE"
BASELINE, CAP_TOP, LEFT = 1003.25, 888.33, 298.0   # relevés sur « TRAIL »
TRACK = 123                                        # interlettrage de « TRAIL », en unités de police

f = TTFont(FONT); gs = f.getGlyphSet(); cmap = f.getBestCmap()
scale = (BASELINE - CAP_TOP) / 1612                # hauteur de capitale Lemon Milk = 1612
def bounds(ch):
    bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp); return bp.bounds
x = LEFT - bounds(WORD[0])[0] * scale
parts = []
for ch in WORD:
    g = gs[cmap[ord(ch)]]
    pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    g.draw(TransformPen(pen, (scale, 0, 0, -scale, x, BASELINE)))
    parts.append(pen.getCommands())
    right = x + bounds(ch)[2] * scale
    x += (g.width + TRACK) * scale
print("mot : x %.1f -> %.1f" % (LEFT, right))

BAND = "M201.11,426.64H1571l9-47.17H154V891.8h-.23v157.41H1328.07l28.81-155.13,8.11-42.44H201.11Z"
REST = '''<polygon class="a" points="1742.74 379.47 1733.73 426.63 1755.08 426.63 1755.08 851.64 1527.7 851.64 1518.69 898.8 1802.24 898.8 1802.24 379.47 1742.74 379.47"/><polygon class="a" points="305.98 529.78 305.98 748.63 437.94 748.63 437.94 704.92 349.97 704.92 349.97 529.78 305.98 529.78"/><rect class="a" x="462.51" y="529.78" width="43.99" height="218.85"/><path class="a" d="M642.39,572.55q27,0,47,19.68l31.36-31.36c-17.88-17.56-44.82-32.45-78.61-32.45L642,528q-46,0-78.34,32.72-32.58,32.85-32.58,78.6,0,46.15,32.58,78.47,32.18,32.46,78.34,32.45,45.75,0,78.47-32.45c21.61-21.45,35-51.14,31.9-92H640v42H702.4a66.39,66.39,0,0,1-60,38.28q-27.69,0-47-19.55-19.54-19.55-19.55-47.11t19.55-47.11Q614.83,572.55,642.39,572.55Z"/><polygon class="a" points="938.22 748.63 938.22 529.78 894.37 529.78 894.37 617.35 821.19 617.35 821.19 529.78 777.34 529.78 777.34 748.63 821.19 748.63 821.19 660.93 894.37 660.93 894.37 748.63 938.22 748.63"/><polygon class="a" points="1060.81 748.63 1060.81 573.36 1114.57 573.36 1114.57 529.78 962.79 529.78 962.79 573.36 1016.68 573.36 1016.68 748.63 1060.81 748.63"/><path class="a" d="M1358.13,528c-28.38,0-54.72,10.86-79.29,32.72s-39.64,48.06-45.62,78.6-1,56.75,15.07,78.47Q1272.13,750,1315,750.13c28.51,0,54.85-10.73,79.29-32.32s39.64-47.79,45.62-78.47,1-56.75-15.07-78.6S1386.5,528,1358.13,528Zm40.45,111.05c-3.53,18.46-12.89,34.21-27.56,47.11s-30.41,19.41-47.38,19.41-30.54-6.51-40.05-19.41-12.62-28.78-9.09-47.11,12.76-33.94,27.42-47.11,30.27-19.55,47.52-19.55q25.45,0,39.91,19.55C1399,605.13,1402.11,620.74,1398.58,639.07Z"/><polygon class="b" points="1709.98 229.3 1668.98 229.3 1585.59 650.75 1487.43 525.16 1371.9 1149.33 1412.77 1149.33 1508.47 627.39 1606.77 753.11 1709.98 229.3"/>'''

def svg(viewbox, ink):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s"><title>LIGHT ON BIKE</title>'
            '<path fill="%s" fill-rule="evenodd" d="%s%s"/>%s</svg>\n') % (viewbox, ink, BAND, "".join(parts), REST.replace('class="a"', 'fill="%s"' % ink).replace('class="b"', 'fill="#ed5f3e"'))

TIGHT, WIDE = "145 220 1670 940", "0 0 2000 1300"
out = {
    "assets/logo/logo-header.svg": svg(TIGHT, "#fff"),
    "assets/logo/logo-blanc-orange.svg": svg(WIDE, "#fff"),
    "assets/logo/logo-noir-orange.svg": svg(TIGHT, "#232323"),
    "livrables/logo/light-on-bike-blanc-orange.svg": svg(TIGHT, "#fff"),
    "livrables/logo/light-on-bike-noir-orange.svg": svg(TIGHT, "#232323"),
}
for p, s in out.items():
    (ROOT / p).parent.mkdir(parents=True, exist_ok=True); (ROOT / p).write_text(s, encoding="utf-8"); print("écrit", p)
