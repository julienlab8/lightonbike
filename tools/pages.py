"""Contenu des pages de LIGHT ON BIKE Pierre-Percée** (assemblées par tools/build.py).

Règle de rédaction : rien d'inventé. Ce qui n'est pas confirmé par LIGHT ON
(date, tarifs, lien d'inscription, ravitaillements, règlement...) apparaît avec
la mention « À confirmer » ; les chiffres des parcours viennent des tracés
OpenRunner (tools/build_routes.py).
"""

import json

TXT = {
    "80": {
        "kicker": "Parcours · 80 KM*",
        "h1": 'Le Donon pour <span class="nw"><em>dessert</em><span class="sq">.</span></span>',
        "lede": "Trois cols, [[up80]] m de D+ et le Donon au km [[donon80]]. La version courte, pas la version plate.",
        "card": "Trois cols dont le Donon, [[up80]] m de D+ sur [[kmr80]] km. La version courte, pas la version plate.",
        "intro": "Deux cols pour se mettre en jambes, puis le Donon au km [[donon80]] avant de redescendre vers l'arrivée. [[kmr80]] km qui ne laissent pas beaucoup de plat.",
        "who": "Pour celles et ceux qui roulent régulièrement et veulent des cols sans y passer la journée. [[kmr80]] km et [[up80]] m de D+&nbsp;: ça se prépare, et ça se savoure.",
        "cols_intro": "Trois cols répertoriés sur le tracé. Le Donon arrive en dernier&nbsp;: gardez-en un peu.",
        "meta": "Parcours 80 KM* de LIGHT ON BIKE Pierre-Percée** : [[km80]] km, [[upraw80]] m de D+, trois cols dont le Donon. Départ à 9h. Carte, profil altimétrique et trace GPX.",
    },
    "145": {
        "kicker": "Parcours · 145 KM**",
        "h1": 'La grosse <span class="nw"><em>journée</em><span class="sq">.</span></span>',
        "lede": "Six cols, [[up145]] m de D+ et le Donon pour finir. Départ à 8h&nbsp;: prévoyez le café avant.",
        "card": "Six cols, [[up145]] m de D+ et le Donon au km [[donon145]]. Départ à 8h&nbsp;: prévoyez le café avant.",
        "intro": "Le grand format part vers le nord, enchaîne Saint-Léon, le Valsberg et les Pandours, puis revient par le Donon. [[km145]] km au compteur, et une bonne raison de bien manger la veille.",
        "who": "Pour les habitués des longues sorties. [[km145]] km et [[up145]] m de D+&nbsp;: mieux vaut arriver avec des kilomètres dans les jambes.",
        "cols_intro": "Six cols répertoriés sur le tracé, de la Meurthe-et-Moselle au Bas-Rhin en passant par la Moselle. Le Donon est le dernier, au km [[donon145]].",
        "meta": "Parcours 145 KM** de LIGHT ON BIKE Pierre-Percée** : [[km145]] km, [[upraw145]] m de D+, six cols dont le Donon. Départ à 8h. Carte, profil altimétrique et trace GPX.",
    },
}


def all_pages(b):
    R, SITE, START, STARS = b.R, b.SITE, b.START, b.STARS
    tbc, val, num, reg, photo, wait, trace = b.tbc, b.val, b.num, b.reg, b.photo, b.wait, b.trace
    ARROW, DOWN = b.ARROW, b.DOWN
    mail = SITE["email"]
    date = val("date", "Date à confirmer")
    MAP_HEAD = '<link rel="stylesheet" href="assets/vendor/leaflet/leaflet.css" />\n'
    MAP_JS = ('<script src="assets/vendor/leaflet/leaflet.js"></script>\n<script src="assets/data/routes.js?v=%s"></script>\n'
              '<script src="assets/js/parcours.js?v=%s"></script>\n') % (SITE["v"], SITE["v"])
    PROFILE_JS = ('<script src="assets/data/routes.js?v=%s"></script>\n<script src="assets/js/parcours.js?v=%s"></script>\n') % (SITE["v"], SITE["v"])
    OR = lambda k: "https://www.openrunner.com/route-details/%d" % R[k]["id"]
    GPX = lambda k: "assets/gpx/%s.gpx" % R[k]["slug"]
    name = lambda k: "%s KM%s" % (k, {"80": "*", "145": "**"}[k])   # écriture source ; finalize() applique les étoiles configurées
    pages = []

    def cta_slim(title, text, second=""):
        return """
  <!-- ============ CTA SLIM ============ -->
  <section class="cta-slim">
    <div class="wrap">
      <div class="reveal">
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <div class="hero-actions">
        %s
        %s
      </div>
    </div>
  </section>""" % (title, text, reg(), second)

    def facts(k, price=True):
        s = '<div><span>Distance</span>%s km</div><div><span>Dénivelé</span>%s m D+</div><div><span>Départ</span>%s</div>' % (
            R[k]["km"], num(R[k]["ascent"]), START[k])
        if price:
            s += '<div><span>Tarif</span>%s</div>' % val("price_" + k)
        return '<div class="facts">%s</div>' % s

    # ------------------------------------------------------------------ ACCUEIL
    hero_photo = photo("hero-accueil", "", "100vw", eager=True)
    hero_visual = hero_photo or ('<div class="hero-art">%s</div><div class="hero-legend"><span><i></i>145 KM**</span><span><i class="o"></i>80 KM*</span></div>'
                                 % trace(["145", "80"], 1000, 640, 20, label=True))
    def race(k):
        ph = photo("parcours-%s" % k, "", "(max-width: 860px) 100vw, 50vw")
        ph = '<div class="ph">%s</div>' % ph if ph else '<div class="ph is-trace">%s</div>' % trace([k], 640, 480, 24, frame=["145"])
        return """
      <a class="h-race" href="parcours-%(k)s-km.html">
        <div class="num">%(k)s<small> KM</small><span class="star">%(st)s</span></div>
        <div class="info">
          <p>%(card)s</p>
          %(facts)s
          <span class="go">Voir le parcours →</span>
        </div>
        %(ph)s
      </a>""" % {"k": k, "st": STARS[k], "card": TXT[k]["card"], "facts": facts(k, price=False), "ph": ph}

    ev_photo = photo("evenement", "", "(max-width: 860px) 100vw, 40vw")
    ev_visual = '<div class="ev-visual has-photo brk-in">%s</div>' % ev_photo if ev_photo else '<div class="ev-visual brk-in">%s</div>' % b.PICTO
    cta_photo = photo("depart", "", "100vw")

    gal = [photo("galerie-%d" % i, alt, "(max-width: 860px) 50vw, 25vw") for i, alt in enumerate(
        ["Cycliste en danseuse sur une route forestière", "Cycliste dans un virage en forêt", "Cycliste souriante en pleine montée",
         "Cycliste en descente sur route humide", "Cycliste au cœur de la forêt vosgienne"], 1)]
    gallery = ""
    if all(gal):
        gallery = """
  <!-- ============ EN IMAGES ============ -->
  <section class="h-retour">
    <div class="wrap sec-top">
      <div><span class="idx"><b>03</b> En images</span><h2>Sur les routes de <span class="nw"><em>Pierre-Percée</em><span class="sq">.</span></span></h2><p class="sub">Les routes du secteur, photographiées lors d'un précédent événement LIGHT ON à Pierre-Percée. La forêt est fournie avec.</p></div>
    </div>
    <div class="h-photos">
      %s
    </div>
  </section>
""" % "\n      ".join(g.replace("<img ", '<img class="big" ', 1) if i == 0 else g for i, g in enumerate(gal))
    track = "".join('<a href="%s" target="_blank" rel="noopener"%s><img src="%s" alt="%s"%s loading="lazy" /></a>' % (
        url, hid, white, "" if hid else name, ' class="%s"' % cls if cls else "")
        for hid in ("",) + (' aria-hidden="true" tabindex="-1"',) * 3 for name, url, logo, white, cls in b.PARTNERS)
    ticker = """
  <!-- ============ PARTENAIRES ============ -->
  <section class="h-partners" aria-label="Nos partenaires">
    <a class="tag" href="partenaires.html">Ils nous <br />soutiennent</a>
    <div class="ticker">
      <div class="track">%s</div>
    </div>
  </section>""" % track
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "SportsOrganization", "@id": SITE["base_url"] + "#organisation", "name": "LIGHT ON", "legalName": "Association Woippy Triathlon",
         "url": SITE["base_url"], "email": SITE["email"], "telephone": SITE["phone_href"],
         "address": {"@type": "PostalAddress", "streetAddress": "7 rue Paul Déroulède", "postalCode": "57140", "addressLocality": "Woippy", "addressCountry": "FR"}},
        {"@type": "SportsEvent", "@id": SITE["base_url"] + "#evenement", "name": "LIGHT ON BIKE Pierre-Percée** 2027", "sport": "Cycling",
         "description": "Cyclosportive chronométrée au départ de la Base de Loisirs Pierre-Percée : 80 KM* et 145 KM**, le dimanche 5 septembre 2027.",
         "startDate": SITE["date_iso"] + "T08:00:00+02:00", "endDate": SITE["date_iso"],
         "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
         "location": {"@type": "Place", "name": SITE["place"], "geo": {"@type": "GeoCoordinates", "latitude": round(R["80"]["start"][0], 4), "longitude": round(R["80"]["start"][1], 4)}},
         "image": [SITE["base_url"] + "assets/img/partage.jpg"], "organizer": {"@id": SITE["base_url"] + "#organisation"}, "url": SITE["base_url"]}]},
        ensure_ascii=False, indent=1)
    body = """
  <!-- ============ HERO ============ -->
  <section class="h-hero cut">
    <span class="geo">Départ · 48.45° N · 6.93° E</span>
    %(hero)s
    <div class="inner wrap">
      <div class="when"><b>%(date)s</b> - %(place)s</div>
      <h1><span class="nw">Light On Bike</span> <span class="place nw">Pierre-Percée**</span></h1>
      <div class="row">
        <div class="actions">
          %(reg)s
          <a class="btn btn-ghost" href="parcours.html">Voir les parcours →</a>
        </div>
        <div class="dist brk">80 · 145 KM<span>%(status)s</span></div>
      </div>
    </div>
  </section>

  <!-- ============ COMPTE À REBOURS ============ -->
  <section class="count-band">
    <div class="wrap count-inner">
      <div class="count-lab">Prochain départ <b>%(date)s · 8h</b></div>
      <div class="count-units" id="countdown" data-target="%(iso)sT08:00:00" role="timer" aria-label="Compte à rebours avant le départ">
        <div class="cu brk"><span class="cn" data-cd="d">00</span><span class="cl">Jours</span></div>
        <div class="cu"><span class="cn" data-cd="h">00</span><span class="cl">Heures</span></div>
        <div class="cu"><span class="cn" data-cd="m">00</span><span class="cl">Minutes</span></div>
        <div class="cu"><span class="cn" data-cd="s">00</span><span class="cl">Secondes</span></div>
      </div>
    </div>
  </section>

  <!-- ============ MANIFESTE ============ -->
  <section class="h-manifeste">
    <div class="wrap">
      <p>80 ou 145 KM&nbsp;: deux façons de rouler à <span class="nw">Pierre-Percée<span class="sq">.</span></span><br />Une seule règle&nbsp;: <em>en </em><span class="nw"><em>profiter</em><span class="sq">.</span></span></p>
    </div>
    %(bolt)s
  </section>

  <!-- ============ L'ESSENTIEL ============ -->
  <section class="h-facts" aria-labelledby="essentiel">
    <div class="wrap">
      <h2 class="facts-title" id="essentiel">L'essentiel</h2>
      <dl class="facts-grid">
        <div><dt>Date</dt><dd>%(date)s</dd></div>
        <div><dt>Lieu</dt><dd>%(place)s<span>Départ et arrivée, %(near)s</span></dd></div>
        <div><dt>Format</dt><dd>%(status)s<span>Routes ouvertes, avec priorités de passage</span></dd></div>
        <div><dt>Distances</dt><dd>80 KM* · 145 KM**<span>%(up80)s m et %(up145)s m de D+. Trois cols sur le 80, six sur le 145</span></dd></div>
        <div><dt>Départs</dt><dd>8h · 9h<span>Le 145 part en premier, le 80 une heure après</span></dd></div>
        <div><dt>Inscriptions</dt><dd>%(opens)s<span>%(places)s. Tarifs %(tbc)s</span></dd></div>
      </dl>
    </div>
  </section>

  <!-- ============ LES PARCOURS ============ -->
  <section class="h-courses" id="apercu">
    <div class="wrap">
      <div class="sec-top lead"><div><span class="idx"><b>01</b> Un départ, deux distances</span><h2>Les parcours<em>**</em></h2></div><a href="parcours.html">Cartes, profils et traces GPX →</a></div>
%(race80)s
%(race145)s
    </div>
  </section>

  <!-- ============ LE PROFIL ============ -->
  <section class="h-profile" data-route="145">
    <span class="geo">Col du Donon · 727 m</span>
    <div class="wrap">
      <div class="top">
        <h2>Le goût de l'<em>effort</em>, grandeur <span class="nw"><em>nature</em><span class="sq">.</span></span></h2>
        <p>Voilà le profil du 145 KM**. Six cols, [[up145]] m de D+, et le Donon gardé pour la fin&nbsp;: il est aussi au menu du 80 KM*.</p>
      </div>
      <div class="rm-profile">%(prof)s</div>
      <p class="rm-read">Profil du 145 KM** · survolez pour lire les altitudes</p>
    </div>
  </section>

  <!-- ============ L'ÉVÉNEMENT ============ -->
  <section class="h-event" id="evenement">
    <div class="wrap grid">
      %(ev_visual)s
      <div>
        <span class="idx"><b>02</b> L'événement</span>
        <h2>La sortie, et tout ce qu'il y a <span class="nw"><em>autour</em><span class="sq">.</span></span></h2>
        <p class="intro">LIGHT ON BIKE, c'est LIGHT ON qui passe sur deux roues. Premier rendez-vous le %(date_low)s à la %(place)s&nbsp;: une cyclosportive chronométrée, entre lacs, forêt vosgienne et cols. Les supporters sont les bienvenus (leurs encouragements aussi).</p>
        <div class="h-list">
          <a href="infos.html#programme"><div><h3>Le programme</h3><p>%(date)s&nbsp;: départ du 145 KM** à 8h, du 80 KM* à 9h. Le reste de la journée arrive bientôt.</p></div><span class="arr">→</span></a>
          <a href="infos.html"><div><h3>Préparer sa venue</h3><p>Accès, stationnement, dossards, ravitaillements, matériel&nbsp;: l'essentiel avant de clipser.</p></div><span class="arr">→</span></a>
          <a href="faq.html"><div><h3>Les questions fréquentes</h3><p>Quel parcours choisir, où trouver la trace GPX, comment s'inscrire.</p></div><span class="arr">→</span></a>
        </div>
      </div>
    </div>
  </section>

%(gallery)s
  <!-- ============ APPEL FINAL ============ -->
  <section class="h-cta" id="inscription">
    %(cta_bg)s
    <div class="wrap">
      <div>
        <span class="eyebrow">%(date)s · 8h</span>
        <h2>On se voit sur la <em>ligne de départ</em>&nbsp;?</h2>
        <p>Choisissez votre distance. Les cols, eux, sont déjà en place. Inscriptions à partir du %(opens)s.</p>
        <div class="btns">
          %(reg)s
          <a class="btn btn-ghost" href="parcours.html#comparatif">Comparer les parcours</a>
        </div>
      </div>
      %(picto)s
    </div>
  </section>
%(ticker)s
""" % {"hero": hero_visual, "date": date, "place": SITE["place"], "near": SITE["place_near"], "status": SITE["status"], "iso": SITE["date_iso"],
       "opens": SITE["registration_opens"], "places": SITE["places"], "date_low": SITE["date"].lower(), "gallery": gallery, "ticker": ticker,
       "reg": reg(), "bolt": b.BOLT, "tbc": tbc(), "km80": R["80"]["km"], "km145": R["145"]["km"],
       "up80": num(R["80"]["ascent"]), "up145": num(R["145"]["ascent"]), "race80": race("80"), "race145": race("145"),
       "prof": b.profile_static("145"), "ev_visual": ev_visual,
       "cta_bg": cta_photo or '<div class="cta-art">%s</div>' % trace(["145", "80"], 1000, 640, 10, dots=False), "picto": b.PICTO}
    pages.append({"file": "index.html", "title": "LIGHT ON BIKE Pierre-Percée** · Cyclosportive 80 et 145 km · 5 septembre 2027",
                  "desc": "LIGHT ON BIKE Pierre-Percée** : cyclosportive chronométrée le dimanche 5 septembre 2027, 80 KM* ou 145 KM** au départ de la Base de Loisirs Pierre-Percée. Inscriptions dès le 7 décembre 2026.",
                  "body": body, "scripts": PROFILE_JS,
                  "head": '<link rel="preload" as="image" href="assets/img/webp/hero-accueil-1280.webp" fetchpriority="high" />\n<script type="application/ld+json">\n%s\n</script>\n' % ld})

    # ------------------------------------------------------------------ PARCOURS (comparatif)
    def duo(k):
        ph = photo("parcours-%s" % k, "", "(max-width: 760px) 100vw, 50vw") or trace([k], 640, 400, 20, frame=["145"])
        return """
        <a class="duo-card" href="parcours-%(k)s-km.html">
          <div class="tr">%(ph)s</div>
          <div class="c-num">%(k)s<small> KM</small><span class="star">%(st)s</span></div>
          <p>%(card)s</p>
          <span class="go">Carte, profil et cols →</span>
        </a>""" % {"k": k, "ph": ph, "st": STARS[k], "card": TXT[k]["card"]}
    cols_cell = lambda k: ", ".join(c["n"].replace("Col ", "", 1) if i else c["n"] for i, c in enumerate(R[k]["cols"]))
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero cut">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Les parcours · 80 et 145 KM</span> À vous <em>de </em><span class="nw"><em>choisir</em><span class="sq">.</span></span></h1>
      <p class="lede">Le 80 KM* pour trois cols et une belle matinée, le 145 KM** pour voir les choses en grand. Dans les deux cas, le Donon est sur la route.</p>
    </div>
  </section>

  <!-- ============ LES DEUX FORMATS ============ -->
  <section class="pad" id="formats">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Deux formats</span>
        <h2 class="h-sec" style="max-width:20ch;">Même départ, deux <span class="nw">journées<span class="sq">.</span></span></h2>
        <p class="lede">Deux boucles au départ de la Base de Loisirs Pierre-Percée, uniquement sur route. Le 145 KM** s'élance à 8h, le 80 KM* à 9h, le dimanche 5 septembre 2027.</p>
      </div>
      <div class="duo">%(duo80)s%(duo145)s
      </div>
    </div>
  </section>

  <!-- ============ COMPARATIF ============ -->
  <section class="pad" id="comparatif" style="padding-top:0;">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Comparatif</span>
        <h2 class="h-sec" style="max-width:20ch;">Les deux formats en un coup <span class="nw">d'œil<span class="sq">.</span></span></h2>
        <p class="lede">Distances, dénivelés et altitudes sont ceux des tracés publiés sur OpenRunner. Les lignes marquées «&nbsp;À confirmer&nbsp;» seront complétées par l'organisation.</p>
      </div>
      <div class="cmp-wrap">
        <table class="cmp two">
          <caption>Comparatif des parcours de LIGHT ON BIKE Pierre-Percée**</caption>
          <thead>
            <tr><td></td><th scope="col"><a href="parcours-80-km.html">80 KM<em>*</em></a></th><th scope="col"><a href="parcours-145-km.html">145 KM<em>**</em></a></th></tr>
          </thead>
          <tbody>
            <tr><th scope="row">Distance exacte</th><td>%(km80)s km</td><td>%(km145)s km</td></tr>
            <tr><th scope="row">Dénivelé positif</th><td>%(up80)s m</td><td>%(up145)s m</td></tr>
            <tr><th scope="row">Départ</th><td>9h</td><td>8h</td></tr>
            <tr><th scope="row">Tarif</th><td>%(p80)s</td><td>%(p145)s</td></tr>
            <tr><th scope="row">Dénivelé négatif</th><td>%(dn80)s m</td><td>%(dn145)s m</td></tr>
            <tr><th scope="row">Altitude</th><td>De %(min80)s à %(max80)s m</td><td>De %(min145)s à %(max145)s m</td></tr>
            <tr><th scope="row">Cols</th><td>3&nbsp;: %(cols80)s</td><td>6&nbsp;: %(cols145)s</td></tr>
            <tr><th scope="row">Places</th><td>400</td><td>400</td></tr>
            <tr><th scope="row">Chronométrage</th><td>Oui</td><td>Oui</td></tr>
            <tr><th scope="row">Ravitaillements</th><td>%(soon)s</td><td>%(soon)s</td></tr>
            <tr><th scope="row">Temps limite</th><td>%(tbc)s</td><td>%(tbc)s</td></tr>
            <tr><th scope="row">Pour qui&nbsp;?</th><td>Cyclistes réguliers, envie de cols sans y passer la journée</td><td>Habitués des longues sorties et du dénivelé</td></tr>
            <tr><th scope="row">Trace</th><td><a class="ln" href="%(or80)s" target="_blank" rel="noopener">OpenRunner</a> · <a class="ln" href="%(gpx80)s" download>GPX</a></td><td><a class="ln" href="%(or145)s" target="_blank" rel="noopener">OpenRunner</a> · <a class="ln" href="%(gpx145)s" download>GPX</a></td></tr>
          </tbody>
        </table>
      </div>
      <p class="swipe-hint">Glissez pour voir les deux formats</p>
    </div>
  </section>

  <!-- ============ RÈGLEMENT ============ -->
  <section class="pad" id="reglement" style="padding-top:0;">
    <div class="wrap">
      <div class="icard reglement-card reveal">
        <div>
          <span class="eyebrow">Règlement</span>
          <h3>Avant de prendre le départ</h3>
          <p>Conditions de participation, matériel, circulation sur route ouverte&nbsp;: tout sera dans le règlement.</p>
        </div>
        <a class="btn btn-ghost" href="reglement.html">Lire le règlement
          %(arrow)s
        </a>
      </div>
    </div>
  </section>
%(cta)s
""" % {"duo80": duo("80"), "duo145": duo("145"), "km80": R["80"]["km"], "km145": R["145"]["km"],
       "up80": num(R["80"]["ascent"]), "up145": num(R["145"]["ascent"]), "dn80": num(R["80"]["descent"]), "dn145": num(R["145"]["descent"]),
       "min80": R["80"]["min"], "max80": R["80"]["max"], "min145": R["145"]["min"], "max145": R["145"]["max"],
       "p80": val("price_80"), "p145": val("price_145"), "cols80": cols_cell("80"), "cols145": cols_cell("145"),
       "tbc": tbc(), "soon": tbc("À venir"), "or80": OR("80"), "or145": OR("145"), "gpx80": GPX("80"), "gpx145": GPX("145"), "arrow": ARROW,
       "cta": cta_slim('Vous avez choisi votre distance<em class="pt">&nbsp;?</em>', "Dimanche 5 septembre 2027&nbsp;: le 145 KM** part à 8h, le 80 KM* à 9h. Il ne manque plus que vous.",
                       '<a class="btn btn-ghost" href="infos.html">Infos pratiques</a>')}
    pages.append({"file": "parcours.html", "title": "Les parcours · 80 KM* et 145 KM** · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "80 KM* ([[km80]] km, [[upraw80]] m D+) et 145 KM** ([[km145]] km, [[upraw145]] m D+) : comparatif des deux parcours de LIGHT ON BIKE Pierre-Percée**, horaires, cols et traces GPX.",
                  "body": body})

    # ------------------------------------------------------------------ PAGES PARCOURS
    for k in ("80", "145"):
        r, t, other = R[k], TXT[k], ("145" if k == "80" else "80")
        hero_img = photo("hero-parcours-%s" % k, "", "100vw", cls="ph-bg", eager=True)
        side = photo("parcours-%s" % k, "", "(max-width: 860px) 100vw, 50vw")
        cols = "".join('<li><span class="c-name">%s</span><span class="c-km">km %s</span><span class="c-alt">%s m</span></li>'
                       % (c["n"], ("%.1f" % c["km"]).replace(".", ","), c["alt"]) for c in r["cols"])
        body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero%(hasimg)s cut">
    %(hero_img)s
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">%(kicker)s</span> %(h1)s</h1>
      <p class="lede">%(lede)s</p>
    </div>
  </section>

  <!-- ============ LE FORMAT ============ -->
  <section class="pad" id="format">
    <div class="wrap">
      <div class="c-head">
        <h2 class="c-num">%(k)s<small> KM</small><span class="star">%(st)s</span></h2>
        <div class="c-intro">
          <p>%(intro)s</p>
          %(facts)s
        </div>
      </div>
      <div class="hero-actions" style="margin-top:32px;">
        %(reg)s
        <a class="btn btn-gpx" href="%(or)s" target="_blank" rel="noopener">Voir la trace · OpenRunner
          %(arrow)s
        </a>
        <a class="btn btn-ghost" href="%(gpx)s" download>Télécharger le GPX
          %(down)s
        </a>
      </div>

      <dl class="keyfigs">
        <div><dt>Distance exacte</dt><dd>%(km)s km</dd></div>
        <div><dt>Dénivelé positif</dt><dd>%(up)s m</dd></div>
        <div><dt>Dénivelé négatif</dt><dd>%(dn)s m</dd></div>
        <div><dt>Point haut</dt><dd>%(max)s m<small>au km %(maxkm)s</small></dd></div>
        <div><dt>Point bas</dt><dd>%(min)s m</dd></div>
        <div><dt>Départ</dt><dd>%(start)s<small>%(startnote)s</small></dd></div>
      </dl>
    </div>
  </section>

  <!-- ============ CARTE & PROFIL ============ -->
  <section class="pad" id="carte" style="padding-top:0;">
    <div class="wrap">
      <figure class="route-map" data-route="%(k)s">
        <div class="rm-head"><h3>Carte &amp; profil</h3><a href="%(or)s" target="_blank" rel="noopener">Ouvrir sur OpenRunner →</a></div>
        <div class="rm-map"><div class="rm-nojs">%(trace)s</div></div>
        <div class="rm-profile">%(prof)s</div>
        <p class="rm-read">Survolez ou touchez le profil pour suivre le parcours sur la carte</p>
        <figcaption>Tracé et profil altimétrique du %(name)s, d'après le parcours publié sur <a href="%(or)s" target="_blank" rel="noopener">OpenRunner</a> (mise à jour du %(upd)s). D&nbsp;: départ et arrivée, à la Base de Loisirs Pierre-Percée. Les numéros repèrent les cols. Le tracé définitif sera confirmé avant l'événement.</figcaption>
      </figure>
    </div>
  </section>

  <!-- ============ LES COLS ============ -->
  <section class="pad" id="cols" style="padding-top:0;">
    <div class="wrap">
      <div class="sec-split%(nophoto)s reveal">
        <div class="sec-head">
          <span class="eyebrow">Les cols</span>
          <h2 class="h-sec" style="max-width:18ch;">Ce qui vous attend <span class="nw">là-haut<span class="sq">.</span></span></h2>
          <p class="lede">%(cols_intro)s</p>
        </div>
        %(side)s
      </div>
      <ol class="cols-list">%(cols)s</ol>
    </div>
  </section>

  <!-- ============ INFOS DU FORMAT ============ -->
  <section class="pad" id="infos-format" style="padding-top:0;">
    <div class="wrap">
      <div class="icard-grid three">
        <div class="icard reveal"><h3>Pour qui&nbsp;?</h3><p>%(who)s</p></div>
        <div class="icard reveal"><h3>Ravitaillements</h3><p>Nombre et emplacements des ravitaillements&nbsp;: %(soon)s Ils seront reportés sur la carte dès qu'ils sont fixés.</p></div>
        <div class="icard reveal"><h3>Chrono &amp; circulation</h3><p>Épreuve chronométrée, sur routes ouvertes à la circulation avec priorités de passage. Temps limite&nbsp;: %(tbc)s Le détail sera dans le <a class="ln" href="reglement.html">règlement</a>.</p></div>
      </div>
      <div class="other-format reveal" style="margin-top:clamp(40px,5vw,64px);">
        <div><span class="c-lab">L'autre format</span><p>%(other_txt)s</p></div>
        <a class="btn btn-ghost" href="parcours-%(other)s-km.html">Voir le %(other_name)s
          %(arrow)s
        </a>
      </div>
    </div>
  </section>
%(cta)s
""" % {"hasimg": " has-img" if hero_img else "", "hero_img": hero_img, "kicker": t["kicker"], "h1": t["h1"], "lede": t["lede"],
       "k": k, "st": STARS[k], "intro": t["intro"], "facts": facts(k), "reg": reg("S'inscrire sur le %s" % name(k)),
       "or": OR(k), "gpx": GPX(k), "arrow": ARROW, "down": DOWN, "km": r["km"], "up": num(r["ascent"]), "dn": num(r["descent"]),
       "max": r["max"], "maxkm": ("%.1f" % r["max_km"]).replace(".", ","), "min": r["min"], "start": START[k],
       "startnote": "Le premier départ de la journée" if k == "145" else "Une heure après le 145 KM**",
       "trace": trace([k], 900, 520, 30), "prof": b.profile_static(k), "name": name(k),
       "upd": "/".join(reversed(r["updated"].split("-"))), "nophoto": "" if side else " no-photo",
       "side": '<figure class="sec-photo brk-in">%s</figure>' % side if side else "", "cols_intro": t["cols_intro"], "cols": cols,
       "who": t["who"], "tbc": tbc(), "soon": tbc("À venir"), "other": other, "other_name": name(other),
       "other_txt": ("Envie d'en voir plus&nbsp;? Le 145 KM** ajoute trois cols et [[kmdiff]] km." if k == "80"
                     else "Envie d'une version plus courte&nbsp;? Le 80 KM* garde le Donon et s'arrête à trois cols."),
       "cta": cta_slim('Le %s vous <em class="pt">tente&nbsp;?</em>' % name(k), "Dimanche 5 septembre 2027, départ à %s. Inscriptions dès le 7 décembre 2026 - 20h." % START[k],
                       '<a class="btn btn-ghost" href="parcours.html#comparatif">Comparer les deux formats</a>')}
        pages.append({"file": "parcours-%s-km.html" % k, "title": "Parcours %s · %s km, %s m D+ · LIGHT ON BIKE Pierre-Percée**" % (name(k), r["km"], r["ascent"]),
                      "desc": t["meta"], "body": body, "head": MAP_HEAD, "scripts": MAP_JS})

    # ------------------------------------------------------------------ INFOS PRATIQUES
    def sec(id_, eyebrow, title, lede, cards, slot=None, flip=False, first=False):
        ph = photo(slot, "", "(max-width: 860px) 100vw, 50vw") if slot else ""
        head_ = '<div class="sec-head">\n        <span class="eyebrow">%s</span>\n        <h2 class="h-sec" style="max-width:18ch;">%s</h2>\n        <p class="lede">%s</p>\n      </div>' % (eyebrow, title, lede)
        if ph:
            head_ = '<div class="sec-split%s reveal">\n      %s\n        <figure class="sec-photo brk-in">%s</figure>\n      </div>' % (" flip" if flip else "", head_, ph)
        grid = '<div class="icard-grid %s">%s</div>' % ("three" if len(cards) == 3 else "rows",
               "".join('<div class="icard reveal"><h3>%s</h3><p>%s</p></div>' % c for c in cards))
        return '\n  <section class="pad" id="%s"%s>\n    <div class="wrap">\n      %s\n      %s\n    </div>\n  </section>\n' % (
            id_, "" if first else ' style="padding-top:0;"', head_, grid)

    reg_state = ("Les inscriptions sont ouvertes." if SITE["registration_url"] else "Ouverture des inscriptions le %s." % SITE["registration_opens"])
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero%(hasimg)s cut">
    %(hero_img)s
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Infos pratiques · préparer sa venue</span> Tout pour prendre <em>le </em><span class="nw"><em>départ</em><span class="sq">.</span></span></h1>
      <p class="lede">Programme, accès, dossards, ravitaillements, matériel&nbsp;: ce qu'il faut savoir avant de clipser. Le reste, c'est vos jambes.</p>
    </div>
  </section>

  <!-- ============ PROGRAMME ============ -->
  <section class="pad" id="programme">
    <div class="wrap">
      <div class="tl-head reveal">
        <span class="eyebrow">Programme</span>
        <h2 class="h-sec" style="max-width:18ch;">Le déroulé de la <span class="nw">journée<span class="sq">.</span></span></h2>
        <p class="lede">La date et les départs sont fixés. Le reste du programme sera publié ici dès qu'il est validé.</p>
      </div>
      <div class="timeline">
        <div class="tl-group reveal">
          <div class="tl-dayhead"><span class="d">%(date)s</span><span class="d-sub">Jour de course</span></div>
          <div class="tl-row"><div class="tl-time">%(tbc_s)s</div><div><div class="tl-title">Accueil &amp; retrait des dossards</div><div class="tl-desc">À la Base de Loisirs Pierre-Percée. Horaires à confirmer.</div></div><span class="tl-tag">Base de Loisirs</span></div>
          <div class="tl-row"><div class="tl-time">08:00</div><div><div class="tl-title">Départ · 145 KM**</div><div class="tl-desc">Le grand format part en premier.</div></div><span class="tl-tag">145 KM**</span></div>
          <div class="tl-row"><div class="tl-time">09:00</div><div><div class="tl-title">Départ · 80 KM*</div><div class="tl-desc">Une heure plus tard, c'est au tour du 80.</div></div><span class="tl-tag">80 KM*</span></div>
          <div class="tl-row"><div class="tl-time">%(tbc_s)s</div><div><div class="tl-title">Arrivées &amp; après-course</div><div class="tl-desc">Retour à la Base de Loisirs Pierre-Percée. Temps limites et suite du programme à confirmer.</div></div><span class="tl-tag">Arrivée</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ INSCRIPTIONS ============ -->
  <section class="pad" id="inscriptions" style="padding-top:0;">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Inscriptions</span>
        <h2 class="h-sec" style="max-width:18ch;">S'inscrire à <span class="nw">l'épreuve<span class="sq">.</span></span></h2>
        <p class="lede">400 places sur le 80 KM*, 400 sur le 145 KM**. Ouverture des inscriptions le %(opens)s&nbsp;: mettez un rappel.</p>
      </div>
      <div class="reg-box reveal">
        <div><span class="lab">Où en est-on&nbsp;?</span><p>%(reg_state)s<small>%(reg_note)s</small></p></div>
        %(reg_btn)s
      </div>
      <div class="icard-grid three steps">
        <div class="icard reveal"><h3>Choisir son parcours</h3><p><a class="ln" href="parcours-80-km.html">80 KM*</a> ou <a class="ln" href="parcours-145-km.html">145 KM**</a>&nbsp;: cartes, profils et traces GPX sont en ligne pour vous décider.</p></div>
        <div class="icard reveal"><h3>Ouverture &amp; places</h3><p>Ouverture le %(opens)s, en ligne. 400 places par format. Tarifs&nbsp;: %(tbc)s</p></div>
        <div class="icard reveal"><h3>Conditions de participation</h3><p>Âge minimum, licence ou justificatif médical&nbsp;: %(soon)s Ils figureront dans le <a class="ln" href="reglement.html">règlement</a>.</p></div>
      </div>
    </div>
  </section>
%(acces)s%(dossards)s%(ravitos)s%(materiel)s
  <!-- ============ FAQ ============ -->
  <section class="pad" id="faq" style="padding-top:0;">
    <div class="wrap">
      <div class="icard reglement-card reveal">
        <div>
          <span class="eyebrow">FAQ</span>
          <h3>Encore une question&nbsp;?</h3>
          <p>Quel parcours choisir, où trouver la trace, comment nous joindre&nbsp;: les réponses sont dans la FAQ.</p>
        </div>
        <a class="btn btn-ghost" href="faq.html">Lire la FAQ
          %(arrow)s
        </a>
      </div>
    </div>
  </section>
%(cta)s
""" % {"hasimg": " has-img" if photo("hero-infos") else "", "hero_img": photo("hero-infos", "", "100vw", cls="ph-bg", eager=True),
       "date": date, "tbc_s": tbc("À venir"), "tbc": tbc(), "soon": tbc("À venir"), "opens": SITE["registration_opens"], "arrow": ARROW, "reg_state": reg_state,
       "reg_note": ("Rendez-vous sur la plateforme d'inscription." if SITE["registration_url"]
                    else "400 places par format. Le lien d'inscription et les tarifs seront publiés ici. Une question d'ici là&nbsp;? <a class=\"ln\" href=\"contact.html\">Écrivez-nous</a>."),
       "reg_btn": (reg() if SITE["registration_url"] else '<a class="btn btn-ghost" href="contact.html">Nous écrire</a>'),
       "acces": sec("acces", "Accès &amp; stationnement", 'Rejoindre le <span class="nw">départ<span class="sq">.</span></span>',
                    "Départ, arrivée et retrait des dossards au même endroit&nbsp;: la Base de Loisirs Pierre-Percée, à proximité de Celles-sur-Plaine.",
                    [("Le lieu", "Base de Loisirs Pierre-Percée, à proximité de Celles-sur-Plaine. Les deux parcours sont des boucles&nbsp;: on repart de là où on est arrivé, pratique pour retrouver la voiture."),
                     ("En voiture", "<a class=\"ln\" href=\"https://www.google.com/maps/dir/?api=1&amp;destination=%.5f,%.5f\" target=\"_blank\" rel=\"noopener\">Itinéraire vers le départ</a>. Covoiturer entre cyclistes, c'est moins de voitures sur place et plus de monde pour porter les vélos." % tuple(R["80"]["start"])),
                     ("Stationnement", "Parkings, fléchage et consignes d'arrivée&nbsp;: %s" % tbc())], slot="acces"),
       "dossards": sec("dossards", "Retrait des dossards", 'Récupérer son <span class="nw">dossard<span class="sq">.</span></span>',
                       "Le retrait se fait à la Base de Loisirs Pierre-Percée, là où tout se passe&nbsp;: départ, arrivée, dossards.",
                       [("Où", "À la Base de Loisirs Pierre-Percée, à proximité de Celles-sur-Plaine."),
                        ("Quand", "Jours et horaires de retrait, pièces à présenter&nbsp;: %s" % tbc()),
                        ("À prévoir large", "Le 145 KM** part à 8h, le 80 KM* à 9h. Mieux vaut arriver avec de l'avance&nbsp;: un pneu à regonfler prend toujours plus de temps que prévu.")], flip=True),
       "ravitos": sec("ravitaillements", "Ravitaillements", 'Manger et boire en <span class="nw">route<span class="sq">.</span></span>',
                      "[[kmr80]] km pour l'un, [[kmr145]] km pour l'autre&nbsp;: les bidons ne suffiront pas. Le plan des ravitaillements sera publié avec le programme.",
                      [("Sur les parcours", "Nombre, emplacements et contenu des ravitaillements&nbsp;: %s" % tbc("À venir")),
                       ("À l'arrivée", "Ravitaillement d'arrivée et restauration sur place&nbsp;: %s" % tbc("À venir")),
                       ("En attendant", "Partez avec vos bidons pleins et de quoi manger dans les poches&nbsp;: le premier col arrive dès le km [[col1]], sur les deux parcours.")]),
       "materiel": sec("materiel", "Matériel", 'Préparer son <span class="nw">vélo<span class="sq">.</span></span>',
                       "Les deux parcours empruntent uniquement des routes, ouvertes à la circulation. La liste du matériel obligatoire sera fixée par le règlement.",
                       [("Le vélo", "Deux tracés 100&nbsp;%% route, avec %s m de D+ sur le 80 KM* et %s m sur le 145 KM**&nbsp;: un vélo révisé et des freins en forme, c'est le minimum." % (num(R["80"]["ascent"]), num(R["145"]["ascent"]))),
                        ("Matériel obligatoire", "Casque, éclairage, nécessaire de réparation, types de vélos acceptés&nbsp;: %s" % tbc()),
                        ("La trace", "Les fichiers GPX des deux parcours sont en ligne&nbsp;: <a class=\"ln\" href=\"%s\" download>80 KM*</a> et <a class=\"ln\" href=\"%s\" download>145 KM**</a>. À charger dans votre compteur avant le départ." % (GPX("80"), GPX("145")))], slot="materiel", flip=True),
       "cta": cta_slim('Une question avant de vous inscrire<em class="pt">&nbsp;?</em>', "Écrivez-nous, on répond.", '<a class="btn btn-ghost" href="contact.html">Nous écrire</a>')}
    pages.append({"file": "infos.html", "title": "Infos pratiques · programme, accès, dossards · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Programme, accès, stationnement, retrait des dossards, ravitaillements et matériel : préparer sa venue à LIGHT ON BIKE Pierre-Percée**, dimanche 5 septembre 2027. Départs à 8h (145 KM**) et 9h (80 KM*).",
                  "body": body})

    # ------------------------------------------------------------------ FAQ
    Q = [
        ("Quels sont les parcours proposés&nbsp;?", "Deux parcours à vélo de route&nbsp;: le <a class=\"ln\" href=\"parcours-80-km.html\">80 KM*</a> (%s km, %s m de D+) et le <a class=\"ln\" href=\"parcours-145-km.html\">145 KM**</a> (%s km, %s m de D+)." % (R["80"]["km"], num(R["80"]["ascent"]), R["145"]["km"], num(R["145"]["ascent"]))),
        ("À quelle heure sont les départs&nbsp;?", "Le 145 KM** part à 8h, le 80 KM* à 9h."),
        ("Quel parcours choisir&nbsp;?", "Le 80 KM* compte trois cols, dont le Donon, pour [[up80]] m de D+&nbsp;: le bon format si vous roulez régulièrement. Le 145 KM** en compte six pour [[up145]] m de D+&nbsp;: à réserver aux habitués des longues sorties. Le <a class=\"ln\" href=\"parcours.html#comparatif\">comparatif</a> met les deux côte à côte."),
        ("Où trouver la trace GPX&nbsp;?", "Sur la page de chaque parcours, avec la carte et le profil. Téléchargement direct&nbsp;: <a class=\"ln\" href=\"%s\" download>GPX du 80 KM*</a> et <a class=\"ln\" href=\"%s\" download>GPX du 145 KM**</a>. Les deux tracés sont aussi consultables sur OpenRunner." % (GPX("80"), GPX("145"))),
        ("Quels cols sont au programme&nbsp;?", "Sur le 80 KM*&nbsp;: %s. Sur le 145 KM**&nbsp;: %s." % (cols_cell("80"), cols_cell("145"))),
        ("Quand et où a lieu l'événement&nbsp;?", "Le dimanche 5 septembre 2027, à la Base de Loisirs Pierre-Percée, à proximité de Celles-sur-Plaine. Départ et arrivée au même endroit."),
        ("Comment s'inscrire&nbsp;?", "Les inscriptions ouvrent le %s, en ligne, avec 400 places par format. Le lien d'inscription sera publié sur la page <a class=\"ln\" href=\"infos.html#inscriptions\">Infos pratiques</a>. Tarifs&nbsp;: %s" % (SITE["registration_opens"], tbc())),
        ("L'épreuve est-elle chronométrée&nbsp;?", "Oui&nbsp;: LIGHT ON BIKE Pierre-Percée** est une cyclosportive chronométrée, sur les deux formats. On peut viser un temps, ou juste viser le sommet du Donon."),
        ("Les routes sont-elles fermées à la circulation&nbsp;?", "Non&nbsp;: les parcours empruntent des routes ouvertes à la circulation, avec priorités de passage. Le dispositif sera détaillé dans le <a class=\"ln\" href=\"reglement.html\">règlement</a>."),
        ("Où retirer son dossard&nbsp;?", "À la Base de Loisirs Pierre-Percée. Jours et horaires de retrait&nbsp;: %s" % tbc()),
        ("Faut-il une licence ou un certificat médical&nbsp;?", "Les conditions de participation (âge, licence, justificatif médical)&nbsp;: %s Elles seront précisées dans le <a class=\"ln\" href=\"reglement.html\">règlement</a>." % tbc("À venir")),
        ("Y a-t-il des ravitaillements&nbsp;?", "Le nombre et l'emplacement des ravitaillements&nbsp;: %s" % tbc("À venir")),
        ("Quel matériel est obligatoire&nbsp;?", "La liste du matériel obligatoire et des vélos acceptés&nbsp;: %s" % tbc()),
        ("Une autre question&nbsp;?", "Écrivez-nous à <a href=\"mailto:%s\" style=\"color:var(--accent);\">%s</a> ou au <a href=\"tel:%s\" style=\"color:var(--accent);\">%s</a>. On vous répond." % (mail, mail, SITE["phone_href"], SITE["phone"])),
    ]
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">FAQ</span> Les questions <span class="nw"><em>fréquentes</em><span class="sq">.</span></span></h1>
      <p class="lede">Ce qu'on sait déjà, et ce qui arrive. Les réponses se complètent au fil des annonces.</p>
    </div>
  </section>

  <section class="pad" id="faq">
    <div class="wrap">
      <div class="faq-list">
        %s
      </div>
    </div>
  </section>
%s
""" % ("\n        ".join('<details class="faq-item"><summary>%s</summary><p>%s</p></details>' % q for q in Q),
       cta_slim('On se retrouve au <em class="pt">départ&nbsp;?</em>', "Dimanche 5 septembre 2027&nbsp;: 145 KM** à 8h, 80 KM* à 9h.", '<a class="btn btn-ghost" href="contact.html">Nous écrire</a>'))
    pages.append({"file": "faq.html", "title": "FAQ · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Parcours, horaires de départ, traces GPX, inscriptions : les questions fréquentes sur LIGHT ON BIKE Pierre-Percée**.", "body": body})

    # ------------------------------------------------------------------ RÈGLEMENT
    pend = lambda what: '<p class="pending">%s&nbsp;: %s</p>' % (what, tbc())
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Règlement</span> Le <span class="nw"><em>règlement</em><span class="sq">.</span></span></h1>
      <p class="lede">Le règlement de l'épreuve est en cours de rédaction. Voici sa trame et les éléments déjà fixés&nbsp;; les articles en attente sont signalés.</p>
    </div>
  </section>

  <section class="pad">
    <div class="wrap prose">

      <h2>Article 1 · Épreuve</h2>
      <p><strong>LIGHT ON BIKE Pierre-Percée**</strong> est une cyclosportive chronométrée organisée par LIGHT ON, le <strong>dimanche 5 septembre 2027</strong>. Départ et arrivée&nbsp;: Base de Loisirs Pierre-Percée, à proximité de Celles-sur-Plaine.</p>
      <p>La participation implique la connaissance et l'acceptation du présent règlement.</p>

      <h2>Article 2 · Parcours</h2>
      <ul>
        <li><strong>80 KM*</strong>&nbsp;: %(km80)s km, %(up80)s m de dénivelé positif.</li>
        <li><strong>145 KM**</strong>&nbsp;: %(km145)s km, %(up145)s m de dénivelé positif.</li>
      </ul>
      <p>Les deux parcours sont des boucles et empruntent uniquement des routes. Les tracés sont publiés sur les pages <a href="parcours-80-km.html">80 KM*</a> et <a href="parcours-145-km.html">145 KM**</a>. Tout participant s'engage à respecter le parcours dans sa totalité.</p>

      <h2>Article 3 · Horaires</h2>
      <ul>
        <li>8h00&nbsp;: départ du 145 KM**</li>
        <li>9h00&nbsp;: départ du 80 KM*</li>
      </ul>
      %(a3)s

      <h2>Article 4 · Conditions de participation</h2>
      %(a4)s

      <h2>Article 5 · Inscriptions et tarifs</h2>
      <p>Les inscriptions se font en ligne et ouvrent le %(opens)s. Le nombre de places est limité à 400 par format.</p>
      %(a5)s

      <h2>Article 6 · Retrait des dossards</h2>
      <p>Le retrait des dossards se fait à la Base de Loisirs Pierre-Percée.</p>
      %(a6)s

      <h2>Article 7 · Matériel</h2>
      %(a7)s

      <h2>Article 8 · Circulation et sécurité</h2>
      <p>L'épreuve se déroule sur des routes ouvertes à la circulation, avec priorités de passage.</p>
      %(a8)s

      <h2>Article 9 · Ravitaillements</h2>
      %(a9)s

      <h2>Article 10 · Temps limites</h2>
      %(a10)s

      <h2>Article 11 · Assurances</h2>
      %(a11)s

      <h2>Article 12 · Annulation, remboursement et transfert</h2>
      %(a12)s

      <h2>Article 13 · Environnement</h2>
      %(a13)s

      <h2>Article 14 · Droit à l'image et données personnelles</h2>
      %(a14)s

      <h2>Contact</h2>
      <p>Une question sur le règlement&nbsp;? <a href="mailto:%(mail)s">%(mail)s</a></p>
    </div>
  </section>
%(cta)s
""" % {"opens": SITE["registration_opens"],
       "km80": R["80"]["km"], "up80": num(R["80"]["ascent"]), "km145": R["145"]["km"], "up145": num(R["145"]["ascent"]),
       "a3": pend("Reste du programme (accueil, arrivées, classements et récompenses)"),
       "a4": pend("Âge minimum, licences acceptées, justificatif médical"),
       "a5": pend("Plateforme d'inscription, tarifs et date de clôture"),
       "a6": pend("Jours, horaires et pièces à présenter"),
       "a7": pend("Matériel obligatoire (casque, éclairage, réparation), vélos acceptés"),
       "a8": pend("Détail des priorités de passage, signaleurs, assistance médicale"),
       "a9": pend("Nombre et emplacements des ravitaillements"),
       "a10": pend("Temps limites et véhicule de fin de course"),
       "a11": pend("Responsabilité civile de l'organisation, assurance individuelle des participants"),
       "a12": pend("Conditions d'annulation, de remboursement et de transfert de dossard"),
       "a13": pend("Engagements environnementaux et zones de déchets"),
       "a14": pend("Droit à l'image et traitement des données des participants"),
       "mail": mail, "cta": cta_slim('Prêt à choisir votre <em class="pt">distance&nbsp;?</em>', "80 KM* ou 145 KM**&nbsp;: les deux parcours sont en ligne.",
                                     '<a class="btn btn-ghost" href="parcours.html">Voir les parcours</a>')}
    pages.append({"file": "reglement.html", "title": "Règlement · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Règlement de LIGHT ON BIKE Pierre-Percée**, cyclosportive chronométrée du 5 septembre 2027 : parcours 80 KM* et 145 KM**, horaires, inscriptions.", "body": body})

    # ------------------------------------------------------------------ PARTENAIRES
    subj = "?subject=Partenariat%20LIGHT%20ON%20BIKE%20Pierre-Perc%C3%A9e"
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero cut">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Partenaires</span> Rouler <span class="nw"><em>ensemble</em><span class="sq">.</span></span></h1>
      <p class="lede">Un événement vélo, ça se monte à plusieurs&nbsp;: collectivités, entreprises, clubs. Voici celles et ceux qui embarquent avec LIGHT ON BIKE.</p>
    </div>
  </section>

  <!-- ============ PARTENAIRES ============ -->
  <section class="pad partners" id="partenaires">
    <div class="wrap">
      <div class="sec-head reveal" style="margin-inline:auto;">
        <span class="eyebrow">Ils nous soutiennent</span>
        <h2 class="h-sec" style="max-width:18ch; margin-inline:auto;">Nos <span class="nw">partenaires<span class="sq">.</span></span></h2>
      </div>
      <p class="lede reveal" style="margin-inline:auto;">Les premiers à embarquer sur LIGHT ON BIKE Pierre-Percée**. La liste s'allonge au fil des annonces.</p>
      <div class="partner-tier reveal">
        <div class="partner-row">%(logos)s
        </div>
      </div>
    </div>
  </section>

  <!-- ============ DEVENIR PARTENAIRE ============ -->
  <section class="pad" id="devenir" style="padding-top:0;">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">Devenir partenaire</span>
        <h2 class="h-sec" style="max-width:18ch;">Une place dans le <span class="nw">peloton<span class="sq">.</span></span></h2>
        <p class="lede">LIGHT ON BIKE est la nouvelle marque d'événements cyclistes de LIGHT ON. Première étape&nbsp;: Pierre-Percée, deux parcours, six cols.</p>
      </div>
      <div class="icard-grid three swipe">
        <div class="icard reveal"><h3>Sur les parcours</h3><p>Ravitaillements, cols, ligne d'arrivée&nbsp;: [[kmr80]] et [[kmr145]] km de route, ça laisse de la place pour être vu.</p></div>
        <div class="icard reveal"><h3>Sur le terrain</h3><p>Un stand, une animation, une dotation&nbsp;: on construit le format avec vous, à la mesure de votre structure.</p></div>
        <div class="icard reveal"><h3>On en parle&nbsp;?</h3><p>Écrivez-nous à <a class="ln" href="mailto:%(mail)s%(subj)s">%(mail)s</a>. On vous envoie le dossier de partenariat et on cale un échange.</p></div>
      </div>
      <div class="hero-actions reveal" style="margin-top:32px;">
        <a class="btn btn-primary" href="mailto:%(mail)s%(subj)s">Devenir partenaire</a>
      </div>
    </div>
  </section>
%(cta)s
""" % {"mail": mail, "subj": subj,
       "logos": "".join('\n          <a class="partner" href="%s" target="_blank" rel="noopener" aria-label="%s (nouvel onglet)"><img src="%s" alt="%s" loading="lazy" /></a>' % (url, name, logo, name)
                        for name, url, logo, white, cls in b.PARTNERS),
       "cta": cta_slim('Et côté selle<em class="pt">&nbsp;?</em>', "80 KM* ou 145 KM**&nbsp;: les parcours sont en ligne.", '<a class="btn btn-ghost" href="parcours.html">Voir les parcours</a>')}
    pages.append({"file": "partenaires.html", "title": "Partenaires · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Les partenaires de LIGHT ON BIKE Pierre-Percée** : Pierre-Percée Pays des Lacs, N2A Expertises, Activa, Europe 2. Et comment rejoindre l'événement.", "body": body})

    # ------------------------------------------------------------------ CONTACT
    q = "?subject=LIGHT%20ON%20BIKE%20%3A%20j%27ai%20une%20question"
    body = """
  <!-- ============ PAGE HERO ============ -->
  <section class="page-hero cut">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Contact</span> Une question&nbsp;? On vous <span class="nw"><em>répond</em><span class="sq">.</span></span></h1>
      <p class="lede">Parcours, inscriptions, bénévolat, partenariat&nbsp;: une seule adresse pour tout LIGHT ON BIKE Pierre-Percée**.</p>
    </div>
  </section>

  <!-- ============ CONTACT ============ -->
  <section class="pad" id="contact">
    <div class="wrap">
      <div class="icard-grid rows">
        <div class="icard reveal"><h3>E-mail</h3><p><a class="contact-big" href="mailto:%(mail)s%(q)s">%(mail)s</a></p></div>
        <div class="icard reveal"><h3>Téléphone</h3><p><a class="contact-big nw" href="tel:%(tel)s">%(phone)s</a></p></div>
      </div>
      <div class="hero-actions reveal" style="margin-top:32px;">
        <a class="btn btn-primary" href="mailto:%(mail)s%(q)s">Nous écrire</a>
        <a class="btn btn-ghost" href="faq.html">Lire la FAQ</a>
      </div>
    </div>
  </section>

  <!-- ============ PARTICIPER AUTREMENT ============ -->
  <section class="pad" id="participer" style="padding-top:0;">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">Participer autrement</span>
        <h2 class="h-sec" style="max-width:18ch;">Pas besoin de <span class="nw">dossard<span class="sq">.</span></span></h2>
        <p class="lede">On peut faire partie de LIGHT ON BIKE Pierre-Percée**, le 5 septembre 2027, sans donner un seul coup de pédale.</p>
      </div>
      <div class="icard-grid three swipe">
        <div class="icard reveal" id="benevole"><h3>Devenir bénévole</h3><p>Accueil, ravitaillements, carrefours à sécuriser&nbsp;: sans bénévoles, pas de départ. Envie d'en être&nbsp;? <a class="ln" href="mailto:%(mail)s?subject=B%%C3%%A9n%%C3%%A9vole%%20LIGHT%%20ON%%20BIKE%%20%%3A%%20je%%20suis%%20partant">Écrivez-nous</a>.</p></div>
        <div class="icard reveal" id="partenaire"><h3>Devenir partenaire</h3><p>Entreprise, collectivité, club&nbsp;: on construit le partenariat avec vous. Tout est sur la page <a class="ln" href="partenaires.html#devenir">Partenaires</a>.</p></div>
        <div class="icard reveal" id="presse"><h3>Presse</h3><p>Journalistes et médias&nbsp;: dossier, visuels et accréditations sur demande, en précisant votre média à <a class="ln" href="mailto:%(mail)s?subject=Presse%%20%%3A%%20LIGHT%%20ON%%20BIKE%%20Pierre-Perc%%C3%%A9e">%(mail)s</a>.</p></div>
      </div>
    </div>
  </section>
%(cta)s
""" % {"mail": mail, "q": q, "tel": SITE["phone_href"], "phone": SITE["phone"],
       "cta": cta_slim('Et sinon, on <em class="pt">roule&nbsp;?</em>', "80 KM* ou 145 KM**&nbsp;: les parcours sont en ligne.", '<a class="btn btn-ghost" href="parcours.html">Voir les parcours</a>')}
    pages.append({"file": "contact.html", "title": "Contact · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Contacter l'équipe LIGHT ON BIKE Pierre-Percée** : questions sur les parcours, les inscriptions, le bénévolat ou un partenariat.", "body": body})

    # ------------------------------------------------------------------ MENTIONS LÉGALES
    body = """
  <section class="page-hero">
    <div class="glow a" aria-hidden="true"></div>
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Mentions légales</span> Mentions légales &amp; <span class="nw"><em>confidentialité</em><span class="sq">.</span></span></h1>
      <p class="lede">Qui édite ce site, qui l'héberge et ce que l'on fait (et ne fait pas) de vos données.</p>
    </div>
  </section>

  <section class="pad">
    <div class="wrap prose">
      <h2>Éditeur du site</h2>
      <p>Le site www.lightonbike.com est édité par l'<strong>Association Woippy Triathlon</strong>, organisatrice des événements LIGHT ON.</p>
      <p>Association de droit local (Alsace-Moselle)<br />Siège social&nbsp;: 7 rue Paul Déroulède, 57140 Woippy<br />SIRET&nbsp;: 814 799 482 00017<br />Code NAF/APE&nbsp;: 93.12Z (activités de clubs de sports)</p>
      <p>Directeur de la publication&nbsp;: Julien Labdant.</p>
      <p>Contact&nbsp;: <a href="mailto:%(mail)s">%(mail)s</a> · <a href="tel:%(tel)s">%(phone)s</a></p>

      <h2>Hébergement</h2>
      <p>Hostinger International Ltd<br />61 Lordou Vironos Street, 6023 Larnaca, Chypre<br /><a href="https://www.hostinger.fr/" target="_blank" rel="noopener">www.hostinger.fr</a></p>

      <h2>Propriété intellectuelle</h2>
      <p>Les textes, logos, photos et éléments graphiques de ce site appartiennent à LIGHT ON ou à leurs auteurs respectifs. Toute reproduction, même partielle, nécessite une autorisation préalable.</p>
      <p>Une photo de vous sur le site que vous souhaitez voir retirée&nbsp;? <a href="mailto:%(mail)s">Écrivez-nous</a>, on s'en occupe.</p>

      <h2>Données personnelles</h2>
      <p>Ce site ne comporte pas d'espace personnel. Les e-mails que vous nous envoyez servent uniquement à vous répondre. Le traitement des données liées aux inscriptions sera détaillé ici et dans le <a href="reglement.html">règlement</a> dès que la plateforme d'inscription est choisie.</p>
      <p>Conformément au RGPD et à la loi Informatique et Libertés, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition&nbsp;: il suffit d'écrire à <a href="mailto:%(mail)s">%(mail)s</a>. Vous pouvez aussi adresser une réclamation à la <a href="https://www.cnil.fr/" target="_blank" rel="noopener">CNIL</a>.</p>

      <h2>Cookies et services tiers</h2>
      <p>Ce site n'utilise ni outil de mesure d'audience ni cookie publicitaire. Les fonds de carte des pages parcours sont chargés depuis les serveurs d'OpenStreetMap&nbsp;; les tracés proviennent des parcours publiés sur OpenRunner.</p>
    </div>
  </section>
""" % {"mail": mail, "tel": SITE["phone_href"], "phone": SITE["phone"]}
    pages.append({"file": "mentions-legales.html", "title": "Mentions légales · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Mentions légales et confidentialité du site LIGHT ON BIKE Pierre-Percée**.", "body": body})

    # ------------------------------------------------------------------ 404
    body = """
  <section class="page-hero">
    <div class="wrap">
      <h1><span class="eyebrow page-kicker">Erreur 404</span> Hors <span class="nw"><em>parcours</em><span class="sq">.</span></span></h1>
      <p class="lede">Cette page n'existe pas, ou plus. Pas de panique, demi-tour par ici&nbsp;:</p>
      <div class="hero-actions" style="margin-top:32px;">
        <a class="btn btn-primary" href="./">Retour à l'accueil</a>
        <a class="btn btn-ghost" href="parcours.html">Voir les parcours</a>
        <a class="btn btn-ghost" href="infos.html">Infos pratiques</a>
      </div>
    </div>
  </section>
"""
    pages.append({"file": "404.html", "title": "Page introuvable · LIGHT ON BIKE Pierre-Percée**",
                  "desc": "Cette page n'existe pas.", "body": body, "search": False})
    return pages
