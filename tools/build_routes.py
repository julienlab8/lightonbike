#!/usr/bin/env python3
"""Prépare les données de parcours à partir des tracés OpenRunner.

Source : tools/data/openrunner-<id>.json (tracé, altitudes tous les 100 m,
cols), relevés sur les pages publiques OpenRunner des deux parcours.
Produit :
  - assets/gpx/*.gpx           fichiers GPX à télécharger
  - assets/data/routes.js      tracés + profils pour la carte interactive
  - tools/data/routes-built.json  chiffres et SVG repris par tools/build.py
"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTES = [
    {"key": "80", "id": 23378612, "slug": "light-on-bike-pierre-percee-80-km"},
    {"key": "145", "id": 23378617, "slug": "light-on-bike-pierre-percee-145-km"},
]

def hav(a, b):
    R = 6371000; p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def simplify(pts, tol):
    """Douglas-Peucker sur des points (x, y)."""
    keep = [False] * len(pts); keep[0] = keep[-1] = True; stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop(); (x1, y1), (x2, y2) = pts[a], pts[b]; dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-12
        best, bi = 0, None
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / n
            if d > best: best, bi = d, i
        if bi is not None and best > tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [i for i, k in enumerate(keep) if k]

def encode(pts):
    out = []; pl = pg = 0
    for la, lo in pts:
        a, g = round(la * 1e5), round(lo * 1e5)
        for v in (a - pl, g - pg):
            v = ~(v << 1) if v < 0 else v << 1
            while v >= 0x20: out.append(chr((0x20 | (v & 0x1f)) + 63)); v >>= 5
            out.append(chr(v + 63))
        pl, pg = a, g
    return "".join(out)

def fr(n, d=1):
    return ("%.*f" % (d, n)).replace(".", ",")

built, js = {}, {}
for r in ROUTES:
    src = json.loads((ROOT / "tools/data" / ("openrunner-%d.json" % r["id"])).read_text())
    pts, el, item = src["pts"], src["el"], src["item"]
    cum = [0.0]
    for i in range(1, len(pts)): cum.append(cum[-1] + hav(pts[i - 1], pts[i]))
    total = cum[-1]; step = item["elevation"]["interval"]
    def alt(d):
        x = min(max(d / step, 0), len(el) - 1); i = int(x); j = min(i + 1, len(el) - 1)
        return el[i] + (el[j] - el[i]) * (x - i)

    # --- GPX
    gpx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<gpx version="1.1" creator="LIGHT ON BIKE" xmlns="http://www.topografix.com/GPX/1/1">',
           '<metadata><name>LIGHT ON BIKE Pierre-Percée - %s KM</name><link href="https://www.openrunner.com/route-details/%d"><text>OpenRunner</text></link></metadata>' % (r["key"], r["id"]),
           '<trk><name>LIGHT ON BIKE Pierre-Percée - %s KM</name><type>cycling</type><trkseg>' % r["key"]]
    for p, d in zip(pts, cum):
        gpx.append('<trkpt lat="%.5f" lon="%.5f"><ele>%.0f</ele></trkpt>' % (p[0], p[1], alt(d)))
    gpx.append('</trkseg></trk></gpx>')
    (ROOT / "assets/gpx").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets/gpx" / (r["slug"] + ".gpx")).write_text("\n".join(gpx) + "\n", encoding="utf-8")

    # --- cols (position sur la trace)
    def at(d):
        lo, hi = 0, len(cum) - 1
        while lo < hi:
            m = (lo + hi) // 2
            if cum[m] < d: lo = m + 1
            else: hi = m
        return pts[lo]
    cols = [{"n": c["name"], "km": round(c["location_in_meter"] / 1000, 1), "alt": c["altitude_in_meter"],
             "ll": at(c["location_in_meter"]), "dep": c["id"].split("-")[1]} for c in item["passes"]]
    imax = max(range(len(el)), key=lambda i: el[i])

    # --- tracé simplifié (aperçu SVG)
    lat0 = math.radians(sum(p[0] for p in pts) / len(pts))
    xy = [(p[1] * math.cos(lat0), -p[0]) for p in pts]
    minx, maxx = min(x for x, _ in xy), max(x for x, _ in xy); miny, maxy = min(y for _, y in xy), max(y for _, y in xy)
    built[r["key"]] = {
        "id": r["id"], "slug": r["slug"], "name_openrunner": item["name"],
        "length_m": item["length"], "km": fr(item["length"] / 1000), "km_num": round(item["length"] / 1000, 1),
        "ascent": item["elevation"]["ascent"], "descent": item["elevation"]["descent"],
        "min": item["elevation"]["min"], "max": item["elevation"]["max"], "max_km": round(imax * step / 1000, 1),
        "start": pts[0], "end": pts[-1], "gap_m": round(hav(pts[0], pts[-1])),
        "cols": cols, "updated": item["updated_at"][:10],
        "xy": xy, "bbox": [minx, miny, maxx, maxy], "el": el, "step": step,
    }
    js[r["key"]] = {"km": round(total / 1000, 2), "line": encode(pts), "el": el, "step": step,
                    "cols": [{"n": c["n"], "km": c["km"], "alt": c["alt"], "ll": [round(c["ll"][0], 5), round(c["ll"][1], 5)]} for c in cols]}
    print(r["key"], built[r["key"]]["km"], "km  D+", item["elevation"]["ascent"], " cols", len(cols), " départ->arrivée", built[r["key"]]["gap_m"], "m")

(ROOT / "tools/data/routes-built.json").write_text(json.dumps(built), encoding="utf-8")
(ROOT / "assets/data").mkdir(parents=True, exist_ok=True)
(ROOT / "assets/data/routes.js").write_text("window.LOB_ROUTES=" + json.dumps(js, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
