# LIGHT ON BIKE Pierre-Percée - informations en attente

Liste tenue à jour à chaque échange. Sur le site, ces points portent la mention « À confirmer » ou « À venir ».
Dernière mise à jour : 13/11/2026.

## À redemander (annoncé « à venir » ou « plus tard »)

- [ ] **Lien d'inscription** (ouverture le 7 décembre 2026 - 20h) -> `registration_url` dans `tools/build.py`
- [ ] **Conditions de participation** : âge minimum, licence, justificatif médical
- [ ] **Ravitaillements** : nombre, emplacements (km), contenu, ravitaillement d'arrivée
- [ ] **Réseaux sociaux** de LIGHT ON BIKE (Instagram, Facebook...) : aucun lien affiché pour l'instant
- [ ] **Newsletter** (formulaire Brevo du site trail) : à reprendre ou non
- [ ] **Versions EN / DE** du site : à faire ou non
- [ ] **Photos** : validation de la sélection (voir ci-dessous) et, si possible, photos propres à l'épreuve

## Sans réponse pour l'instant

- [ ] **Tarifs** du 80 KM et du 145 KM
- [ ] **Matériel obligatoire** (casque, éclairage, réparation) et vélos acceptés
- [ ] **Règlement** : texte complet (la page n'en contient que la trame et les éléments confirmés)
- [ ] **Retrait des dossards** : jours, horaires, pièces à présenter (lieu confirmé : Base de Loisirs Pierre-Percée)
- [ ] **Programme** : horaires d'accueil, temps limites, classements et récompenses
- [ ] **Stationnement** : parkings et consignes d'arrivée
- [ ] **Date de clôture** des inscriptions
- [ ] **Partenaires** : niveaux éventuels (institutionnel, majeur...) ; affichés sans hiérarchie pour l'instant

## À vérifier

- [ ] **Étoiles de l'événement** : formats en 80 KM* et 145 KM***, événement encore écrit « Pierre-Percée** ». Passer à « Pierre-Percée*** » ? (`EVENT_STARS` dans `tools/build.py`)
- [ ] **Jour d'ouverture des inscriptions** : le 7 décembre 2026 tombe un lundi (et non un mardi). Le site affiche « 7 décembre 2026 - 20h », sans jour.
- [ ] **Distance du 145 KM** : le tracé OpenRunner mis à jour mesure 147,9 km (2 439 m D+). L'appellation reste 145 KM, la distance exacte est affichée sur la page du parcours.
- [ ] **Priorités de passage** : formulation reprise telle quelle (« routes ouvertes à la circulation, avec priorités de passage ») ; détail à préciser dans le règlement.

## Photos utilisées

Dossier Drive « PP 2022 - Photos Manu », séquence vélo uniquement (n° PierrePerce2022-xxx) :
455 (accueil), 480 (80 KM), 572 (145 KM), 487 (événement), 598 (appel final), 565 et 508 (en-têtes parcours), 465 (infos), 494 (accès), 442 (matériel), 503, 518, 535, 552, 580 (galerie).

## Avant la mise en ligne

- [ ] `wip: False` dans `tools/build.py` (retire le bandeau « version de travail » et le `noindex`)
- [ ] Déposer le contenu du dossier sur Hostinger (sans `tools/`, `photos-source/`, `livrables/`)
- [ ] Déclarer www.lightonbike.com et le sitemap dans Google Search Console
