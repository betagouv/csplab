---
type: ajoute
date: 2026-10-07
pr: 1748
liens:
  - https://github.com/betagouv/csplab/issues/1738
---

- `POST /api/v1/offres/creer_modifier` : `identification.reference` accepte la valeur
  `"auto"`. CSPLab génère alors une référence au format `CSP-AAAA-NNNNNN` (par
  exemple `CSP-2026-000042`), unique sur toute la plateforme. `"auto"` crée toujours une nouvelle
  offre : pour la mettre à jour ensuite, renvoyez la référence générée. Une
  référence au format `CSP-AAAA-NNNNNN` qui ne désigne pas une offre existante de
  la source est rejetée dans `errors`.
- `POST /api/v1/offres/creer_modifier` : la réponse contient un nouveau champ
  `offres`, qui donne pour chaque offre créée ou mise à jour son `index` dans le
  payload, sa `reference` finale et son `statut` (`created` ou `updated`).
- `POST /api/v1/offres/creer_modifier` : chaque entrée de `errors` contient un
  nouveau champ `index`, la position de l'offre rejetée dans le payload.
