#!/usr/bin/env python3
"""Prépare les photos du site : recadrage léger, JPEG optimisé et déclinaisons WebP.

Déposer les originaux (photos de vélo uniquement) dans photos-source/ en les
nommant d'après leur emplacement, puis lancer :

    python3 tools/build_photos.py && python3 tools/build.py

Emplacements reconnus (nom de fichier sans extension) :
  hero-accueil, parcours-80, parcours-145, evenement, depart,
  hero-parcours-80, hero-parcours-145, hero-infos,
  acces, dossards, ravitaillement, materiel
Une photo absente laisse simplement la mise en page sans photo.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "photos-source", ROOT / "assets/img"
WIDTHS = (640, 1280, 1920)
meta = {}
(OUT / "webp").mkdir(parents=True, exist_ok=True)
for f in sorted(SRC.glob("*")) if SRC.exists() else []:
    if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue
    im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    if im.width > 2000:
        im = im.resize((2000, round(im.height * 2000 / im.width)), Image.LANCZOS)
    im.save(OUT / (f.stem + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)
    widths = [w for w in WIDTHS if w <= im.width] or [im.width]
    for w in widths:
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(OUT / "webp" / ("%s-%d.webp" % (f.stem, w)), "WEBP", quality=74, method=6)
    meta[f.stem] = {"w": im.width, "h": im.height, "webp": widths}
    print("photo", f.stem, im.size, widths)
(OUT / "photos.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
print(len(meta), "photo(s) prête(s)")
