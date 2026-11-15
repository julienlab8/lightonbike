#!/usr/bin/env python3
"""Génère les pages HTML de LIGHT ON BIKE Pierre-Percée**.

Le site reste 100 % statique (HTML/CSS/JS, comme LIGHT ON TRAIL) : ce script
assemble seulement l'en-tête, le menu et le pied de page communs autour du
contenu de chaque page (tools/pages.py), pour ne pas les dupliquer à la main.

    python3 tools/build_routes.py   # si un tracé change
    python3 tools/build.py          # après toute modification de contenu

Tout ce qui attend une validation est centralisé dans SITE ci-dessous :
renseigner une valeur fait disparaître la mention « À confirmer » partout.
"""
import html, json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# ----------------------------------------------------------------------------
# Informations de l'événement. Chaîne vide = « À confirmer » sur le site.
# ----------------------------------------------------------------------------
SITE = {
    "wip": False,                # bandeau « version de travail » + noindex ; passer à False à la publication
    "base_url": "https://www.lightonbike.com/",
    "registration_url": "",      # lien d'inscription (à venir) ; vide = aucun lien externe, boutons vers infos.html#inscriptions
    "registration_opens": "mardi 8 décembre 2026 - 20h",
    "places": "400 places par format",
    "date": "Dimanche 5 septembre 2027",
    "date_short": "5 septembre 2027",
    "date_iso": "2027-09-05",
    "place": "Base de Loisirs Pierre-Percée",
    "place_near": "à proximité de Celles-sur-Plaine",
    "status": "Cyclosportive chronométrée",
    "price_80": "39&nbsp;€", "price_145": "49&nbsp;€",
    "email": "hello@lightontri.com",
    "phone": "03 74 47 56 52", "phone_href": "+33374475652",
    "v": "20261115c",            # à changer après chaque modification CSS/JS
}
START = {"80": "9h", "145": "8h"}          # horaires de départ confirmés
# Étoiles : les textes sont écrits avec « 80 KM* », « 145 KM** » et « Pierre-Percée** » ;
# finalize() applique ensuite les étoiles ci-dessous partout (pages, titres, recherche).
STARS = {"80": "*", "145": "***"}
EVENT_STARS = "***"
EVENT = "LIGHT ON BIKE Pierre-Percée" + EVENT_STARS
PARTNERS = [  # (nom, lien, logo sur fond clair, logo blanc pour le bandeau, classe)
    ("Pierre-Percée Pays des Lacs", "https://www.paysdeslacs.com/", "assets/partners/pierre-percee.png", "assets/partners/pierre-percee.png", "pp"),
    ("N2A Expertises", "https://www.n2aexpertises.fr/", "assets/partners/n2a.svg", "assets/partners/n2a.svg", ""),
    ("Activa Location de véhicules", "https://activa-location.com/", "assets/partners/activa.png", "assets/partners/white/activa.png", ""),
    ("Europe 2", "https://www.europe2.fr/", "assets/partners/europe2.png", "assets/partners/white/europe2.png", ""),
]

R = json.loads((ROOT / "tools/data/routes-built.json").read_text())

# Chiffres des tracés, insérés dans les textes par finalize() : [[km80]], [[up145]]...
NUMS = {}
for _k in ("80", "145"):
    NUMS["km" + _k] = R[_k]["km"]
    NUMS["kmr" + _k] = str(round(R[_k]["km_num"]))
    NUMS["up" + _k] = ("{:,}".format(R[_k]["ascent"])).replace(",", "&nbsp;")
    NUMS["upraw" + _k] = str(R[_k]["ascent"])
    NUMS["donon" + _k] = str(round([c for c in R[_k]["cols"] if "Donon" in c["n"]][0]["km"]))
NUMS["kmdiff"] = str(round(R["145"]["km_num"] - R["80"]["km_num"]))
NUMS["col1"] = str(round(R["80"]["cols"][0]["km"]))

def finalize(s):
    """Insère les chiffres des tracés et applique les étoiles configurées."""
    for k, v in NUMS.items():
        s = s.replace("[[%s]]" % k, v)
    s = re.sub(r"145 KM(<em>)?\*+", lambda m: "145 KM" + (m.group(1) or "") + STARS["145"], s)
    s = re.sub(r"80 KM(<em>)?\*+", lambda m: "80 KM" + (m.group(1) or "") + STARS["80"], s)
    return re.sub(r"(Pierre-Percée|PIERRE-PERCÉE|Les parcours<em>)\*+", lambda m: m.group(1) + EVENT_STARS, s)


# ----------------------------------------------------------------------------
# Petits utilitaires
# ----------------------------------------------------------------------------
def tbc(label="À confirmer"):
    if not SITE["wip"]:
        label = "À venir"          # site public : une seule mention, plus naturelle pour les visiteurs
    return '<span class="tbc">%s</span>' % label

def val(key, label="À confirmer"):
    return SITE[key] or tbc(label)

def num(n):
    return ("{:,}".format(n)).replace(",", "&nbsp;")

ARROW = '<svg class="ico" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWN = '<svg class="ico" viewBox="0 0 24 24" fill="none"><path d="M12 4v11m0 0l-4-4m4 4l4-4M5 19h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PICTO = '<svg class="picto" viewBox="420 220 550 940" aria-hidden="true"><polygon class="p1" points="894.16 379.47 885.15 426.63 906.5 426.63 906.5 851.64 679.12 851.64 670.11 898.8 953.66 898.8 953.66 379.47 894.16 379.47"/><polygon class="p1" points="481.54 426.63 722.44 426.63 731.45 379.47 434.37 379.47 434.37 898.8 507.4 898.8 516.41 851.64 481.54 851.64 481.54 426.63"/><polygon class="p2" points="861.4 229.3 820.4 229.3 737.01 650.75 638.85 525.16 523.33 1149.33 564.19 1149.33 659.9 627.39 758.19 753.11 861.4 229.3"/></svg>'
BOLT = '<svg class="bolt" viewBox="500 220 380 940" aria-hidden="true"><polygon fill="#ed5f3e" points="861.4 229.3 820.4 229.3 737.01 650.75 638.85 525.16 523.33 1149.33 564.19 1149.33 659.9 627.39 758.19 753.11 861.4 229.3"/></svg>'

def reg(label="S'inscrire", cls="btn btn-primary btn-go"):
    """Bouton d'inscription. Sans lien confirmé : renvoi vers le point d'étape des inscriptions (aucun faux lien)."""
    if SITE["registration_url"]:
        return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, html.escape(SITE["registration_url"]), label)
    return '<a class="%s" href="infos.html#inscriptions">%s</a>' % (cls, label)

def photo(slot, alt="", sizes="100vw", cls="", style="", eager=False):
    """<picture> si la photo existe (assets/img/<slot>.jpg + déclinaisons WebP), sinon chaîne vide."""
    jpg = ROOT / "assets/img" / (slot + ".jpg")
    if not jpg.exists():
        return ""
    meta = json.loads((ROOT / "assets/img/photos.json").read_text()).get(slot, {})
    srcset = ", ".join("assets/img/webp/%s-%d.webp %dw" % (slot, w, w) for w in meta.get("webp", []))
    src = '<source type="image/webp" srcset="%s" sizes="%s" />' % (srcset, sizes) if srcset else ""
    return '<picture>%s<img %swidth="%s" height="%s"%s src="assets/img/%s.jpg" alt="%s"%s%s /></picture>' % (
        src, 'fetchpriority="high" ' if eager else "", meta.get("w", ""), meta.get("h", ""),
        ' class="%s"' % cls if cls else "", slot, html.escape(alt), ' style="%s"' % style if style else "",
        "" if eager else ' loading="lazy"')

def wait(text="Photo vélo à venir"):
    return '<div class="ph-wait"><span><b>Emplacement photo</b>%s</span></div>' % text

def _dp(pts, tol):
    keep = [False] * len(pts); keep[0] = keep[-1] = True; stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop(); (x1, y1), (x2, y2) = pts[a], pts[b]; dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-12
        best, bi = 0, None
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / n
            if d > best: best, bi = d, i
        if bi is not None and best > tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

def trace(keys, w=800, h=500, pad=28, frame=None, dots=True, label=False):
    """Aperçu SVG d'un ou plusieurs tracés, dans le même cadre géographique."""
    fx = frame or keys
    minx = min(R[k]["bbox"][0] for k in fx); miny = min(R[k]["bbox"][1] for k in fx)
    maxx = max(R[k]["bbox"][2] for k in fx); maxy = max(R[k]["bbox"][3] for k in fx)
    s = min((w - 2 * pad) / (maxx - minx), (h - 2 * pad) / (maxy - miny))
    ox = (w - (maxx - minx) * s) / 2; oy = (h - (maxy - miny) * s) / 2
    P = lambda p: ((p[0] - minx) * s + ox, (p[1] - miny) * s + oy)
    out = ['<svg class="trace-art" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' % (w, h)]
    for i, k in enumerate(keys):
        pts = _dp([P(p) for p in R[k]["xy"]], 0.6)
        d = "M" + "L".join("%.1f %.1f" % p for p in pts)
        cls = "t-line" + (" alt" if (len(keys) > 1 and k == "80") else "")
        out.append('<path class="%s" d="%s"/>' % (cls, d))
    if dots:
        x, y = P(R[keys[0]]["xy"][0])
        out.append('<circle class="t-dot" cx="%.1f" cy="%.1f" r="6"/>' % (x, y))
        if label:
            out.append('<text x="%.1f" y="%.1f">Départ</text>' % (x + 14, y + 4))
    out.append("</svg>")
    return "".join(out)

def profile_static(key, w=1200, h=260):
    """Profil simplifié, affiché tant que le script n'a pas dessiné la version interactive."""
    el = R[key]["el"]; lo = min(el) // 100 * 100; hi = -(-max(el) // 100) * 100
    pts = [(i / (len(el) - 1) * w, h - 10 - (e - lo) / (hi - lo) * (h - 40)) for i, e in enumerate(el)]
    pts = _dp(pts, 0.8)
    d = "M" + "L".join("%.1f %.1f" % p for p in pts)
    return ('<svg viewBox="0 0 %d %d" preserveAspectRatio="none" role="img" aria-label="Profil altimétrique"><path class="p-area" d="%sL%d %dL0 %dZ"/>'
            '<path class="p-line" d="%s" vector-effect="non-scaling-stroke"/></svg>') % (w, h, d, w, h, h, d)


# ----------------------------------------------------------------------------
# Gabarit commun : <head>, double menu, pied de page
# ----------------------------------------------------------------------------
NAV_GROUPS = {"parcours": ("parcours.html", "parcours-80-km.html", "parcours-145-km.html"),
              "infos": ("infos.html", "faq.html", "reglement.html"),
              "contact": ("contact.html", "partenaires.html")}

def head(p):
    base = SITE["base_url"]
    url = (base + ("" if p["file"] == "index.html" else p["file"])) if base else ""
    seo = ""
    if url:
        seo = ('<link rel="canonical" href="%s" />\n<meta property="og:url" content="%s" />\n' % (url, url))
    robots = '<meta name="robots" content="noindex, nofollow" />\n' if SITE["wip"] else ""
    extra = p.get("head", "")
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%(title)s</title>
%(robots)s%(seo)s<meta property="og:type" content="website" />
<meta property="og:locale" content="fr_FR" />
<meta property="og:site_name" content="LIGHT ON BIKE Pierre-Percée**" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
%(ogimg)s<meta name="twitter:card" content="summary_large_image" />
<meta name="description" content="%(desc)s" />
<link rel="icon" type="image/svg+xml" href="assets/logo/favicon.svg?v=3" />
<link rel="icon" type="image/png" sizes="48x48" href="assets/logo/favicon-48.png?v=3" />
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png?v=2" />
<meta name="theme-color" content="#232323" />
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/LemonMilkBold.woff2" crossorigin />
<link rel="stylesheet" href="assets/css/site.css?v=%(v)s" />
<link rel="stylesheet" href="assets/css/bike.css?v=%(v)s" />
%(extra)s</head>
""" % {"title": p["title"], "desc": p["desc"], "seo": seo, "robots": robots, "v": SITE["v"], "extra": extra,
       "ogimg": ('<meta property="og:image" content="%sassets/img/partage.jpg" />\n<meta property="og:image:width" content="1200" />\n<meta property="og:image:height" content="630" />\n' % base) if base else ""}

def header(p):
    f = p["file"]
    cur = lambda group: ' aria-current="page"' if f in NAV_GROUPS[group] else ""
    wip = ('<div class="wip-bar"><b>Version de travail</b> - les mentions « À confirmer » signalent les informations en attente de validation.</div>\n'
           if SITE["wip"] else "")
    return """<body>
<a class="skip" href="#top">Aller au contenu</a>
%(wip)s
<!-- ============ TOPBAR / ACCÈS RAPIDE ============ -->
<div class="topbar">
  <div class="wrap topbar-inner">
    <nav class="topbar-links" aria-label="Accès rapide">
      <a href="faq.html">FAQ</a>
      <a href="reglement.html">Règlement</a>
      <a href="partenaires.html">Partenaires</a>
      <a href="contact.html">Contact</a>
    </nav>
  </div>
</div>

<!-- ============ NAV ============ -->
<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="./" aria-label="LIGHT ON BIKE accueil">
      <img src="assets/logo/logo-header.svg?v=%(v)s" alt="LIGHT ON BIKE" width="178" height="100" />
    </a>
    <nav class="nav-links" id="navLinks" aria-label="Navigation principale">
      <div class="nav-item">
        <a href="parcours.html" class="nav-parent"%(c1)s>PIERRE-PERCÉE**</a>
        <div class="nav-drop mega">
          <div class="mega-col">
            <a class="mega-head" href="parcours.html">Les Parcours →</a>
            <a href="parcours-80-km.html">80 KM*</a>
            <a href="parcours-145-km.html">145 KM**</a>
            <a href="parcours.html#comparatif">Comparatif</a>
          </div>
          <div class="mega-col">
            <a class="mega-head" href="./#evenement">L'Événement →</a>
            <a href="infos.html#programme">Le programme</a>
            <a href="infos.html#inscriptions">Inscriptions</a>
            <a href="reglement.html">Règlement</a>
            <a href="partenaires.html">Partenaires</a>
          </div>
          <a class="mega-promo" href="parcours.html">
            <span class="mega-trace">%(promo)s</span>
            <span class="mega-promo-cap">
              <span class="mp-k">5 septembre 2027</span>
              <span class="mp-t">80 KM* · 145 KM**</span>
            </span>
          </a>
        </div>
      </div>
      <div class="nav-item">
        <a href="infos.html" class="nav-parent"%(c2)s>Infos pratiques</a>
        <div class="nav-drop">
          <a href="infos.html#programme">Programme</a>
          <a href="infos.html#inscriptions">Inscriptions</a>
          <a href="infos.html#acces">Accès &amp; stationnement</a>
          <a href="infos.html#dossards">Retrait des dossards</a>
          <a href="infos.html#ravitaillements">Ravitaillements</a>
          <a href="infos.html#materiel">Matériel</a>
          <a href="faq.html">FAQ</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="contact.html" class="nav-parent"%(c3)s>Rejoindre l'aventure</a>
        <div class="nav-drop">
          <a href="partenaires.html">Partenaires</a>
          <a href="partenaires.html#devenir">Devenir partenaire</a>
          <a href="contact.html#benevole">Devenir bénévole</a>
          <a href="contact.html#contact">Contact</a>
        </div>
      </div>
    </nav>
    <div class="nav-cta">
      <button class="nav-search-btn" type="button" data-search-open aria-label="Rechercher sur le site" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.2-3.2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
      %(reg)s
      <button class="nav-toggle" id="navToggle" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="navLinks">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>
""" % {"wip": wip, "v": SITE["v"], "c1": cur("parcours"), "c2": cur("infos"), "c3": cur("contact"),
       "promo": trace(["145", "80"], 432, 300, 26, dots=False), "reg": reg()}

def footer(p):
    scripts = '<script src="assets/js/site.js?v=%s"></script>\n<script src="assets/js/search.js?v=%s"></script>\n' % (SITE["v"], SITE["v"])
    scripts += p.get("scripts", "")
    return """
<!-- ============ FOOTER ============ -->
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="./">
          <img src="assets/logo/logo-blanc-orange.svg?v=%(v)s" alt="LIGHT ON BIKE" width="200" height="33" style="height:52px;" />
        </a>
        <p>LIGHT ON BIKE Pierre-Percée**&nbsp;: cyclosportive chronométrée, 80 ou 145 KM au départ de la Base de Loisirs Pierre-Percée, dimanche 5 septembre 2027. Un événement LIGHT ON. Le goût de l'effort, grandeur nature.</p>
      </div>
      <div class="foot-col">
        <p class="foot-h">Naviguer</p>
        <a href="parcours.html">Les Parcours</a>
        <a href="parcours-80-km.html">80 KM*</a>
        <a href="parcours-145-km.html">145 KM**</a>
        <a href="infos.html">Infos pratiques</a>
        <a href="faq.html">FAQ</a>
        <a href="reglement.html">Règlement de l'épreuve</a>
      </div>
      <div class="foot-col">
        <p class="foot-h">Rejoindre</p>
        <a href="partenaires.html">Partenaires</a>
        <a href="contact.html#benevole">Devenir bénévole</a>
        <a href="https://www.openrunner.com/route-details/%(id80)s" target="_blank" rel="noopener">Trace 80 KM* · OpenRunner</a>
        <a href="https://www.openrunner.com/route-details/%(id145)s" target="_blank" rel="noopener">Trace 145 KM** · OpenRunner</a>
        %(reg)s
      </div>
      <div class="foot-col">
        <p class="foot-h">Contact</p>
        <a href="mailto:%(email)s">%(email)s</a>
        <a href="tel:%(tel)s">%(phone)s</a>
        <a href="contact.html">Nous écrire</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 LIGHT ON. Tous droits réservés. · <a href="mentions-legales.html">Mentions légales &amp; confidentialité</a></span>
    </div>
  </div>
</footer>

%(scripts)s</body>
</html>
""" % {"v": SITE["v"], "id80": R["80"]["id"], "id145": R["145"]["id"], "reg": reg("S'inscrire", ""),
       "email": SITE["email"], "phone": SITE["phone"], "tel": SITE["phone_href"], "scripts": scripts}


# ----------------------------------------------------------------------------
# Assemblage + index de recherche
# ----------------------------------------------------------------------------
def text_of(fragment):
    t = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", fragment, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

def main():
    import pages
    built, index = [], []
    for p in pages.all_pages(sys.modules[__name__]):
        for key in ("title", "desc", "body"):
            p[key] = finalize(p[key])
        doc = finalize(head(p) + header(p)) + '\n<main id="top">\n' + p["body"] + "\n</main>\n" + finalize(footer(p))
        left = re.findall(r"\[\[\w+\]\]", doc)
        assert not left, (p["file"], left)
        (ROOT / p["file"]).write_text(doc, encoding="utf-8")
        built.append(p["file"])
        if p.get("search", True):
            heads = [text_of(h) for h in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", p["body"], flags=re.S)]
            index.append({"u": "" if p["file"] == "index.html" else p["file"], "t": html.unescape(p["title"]),
                          "d": html.unescape(p["desc"]), "h": heads, "b": text_of(p["body"])})
    (ROOT / "assets/search-index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    base = SITE["base_url"]
    if base:
        urls = [base + ("" if f == "index.html" else f) for f in built if f != "404.html"]
        (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join("  <url><loc>%s</loc></url>\n" % u for u in urls) + "</urlset>\n", encoding="utf-8")
    print("pages :", ", ".join(built))
    todo = sum(len(re.findall(r'class="tbc"', (ROOT / f).read_text())) for f in built)
    print("mentions « À confirmer / À venir » restantes :", todo)

if __name__ == "__main__":
    main()
