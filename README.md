# LIGHT ON BIKE · Pierre-Percée**

Site statique (HTML/CSS/JS) de LIGHT ON BIKE Pierre-Percée**, construit sur la base du site LIGHT ON TRAIL (même CSS, même double menu, mêmes composants). Le site LIGHT ON TRAIL n'est pas modifié.

Aperçu local : `python3 -m http.server 8080` à la racine, puis http://localhost:8080.

## Modifier le site

Les pages `*.html` sont générées : ne pas les éditer à la main.

- `tools/build.py` : gabarit commun (head, menu, pied de page) et **bloc `SITE`** où renseigner date, lieu, tarifs, lien d'inscription, adresse du site. Une valeur vide affiche « À confirmer ». `wip: False` retire le bandeau « version de travail » et le `noindex`.
- `tools/pages.py` : contenu de chaque page.
- `tools/build_routes.py` : GPX, données de carte et chiffres des parcours, à partir des tracés OpenRunner (`tools/data/`).
- `tools/build_photos.py` : photos (déposer les originaux dans `photos-source/`, voir la liste des emplacements dans le script).
- `tools/build_logo.py` + `tools/export_logo_png.js` : logo LIGHT ON BIKE (SVG + PNG).

Après une modification : `python3 tools/build.py`, et changer `v` dans `SITE` si le CSS ou le JS a bougé.

## Conventions

- Épreuves : **80 KM\*** et **145 KM\*\*** ; événement : **LIGHT ON BIKE Pierre-Percée\*\*** ; organisateur : **LIGHT ON**.
- Horaires : 145 KM** à 8h, 80 KM* à 9h.
- Chiffres des parcours : ceux des tracés OpenRunner (79,1 km / 1 158 m D+ ; 146,5 km / 2 425 m D+). Ne rien inventer : ce qui n'est pas validé reste « À confirmer ».
- DA et ton : identiques à LIGHT ON TRAIL (noir `#232323`, orange `#ed5f3e`, Lemon Milk + Roboto, pas de tirets longs, pas de superlatifs).
- Photos : vélo uniquement.

## Logo

`livrables/logo/` : SVG et PNG transparents (blanc/orange pour fonds sombres, noir/orange pour fonds clairs). Seul le mot « TRAIL » du logo d'origine a été remplacé par « BIKE » (Lemon Milk, même hauteur, même ligne de base, même interlettrage).
