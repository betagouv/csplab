---
type: modifie
date: 2026-10-28
pr: 2108
liens:
  - https://github.com/betagouv/csplab/issues/2079
---

- `POST /api/v1/offres/creer_modifier` : une offre enregistre désormais toutes les
  catégories reçues dans `categories`, dans l'ordre d'envoi. Seule la première par
  ordre alphabétique était conservée jusqu'ici.
- `GET /api/v1/offres` (filtre `categorie`) et `GET /api/fake-ts/offersummaries`
  (filtre `category`) : une offre est retournée si l'une de ses catégories fait partie
  du filtre.
