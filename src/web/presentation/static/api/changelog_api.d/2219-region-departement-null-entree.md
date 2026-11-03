---
type: ajoute
date: 2026-11-03
pr: 2236
liens:
  - https://github.com/betagouv/csplab/issues/2219
---

`POST /api/v1/offres/creer_modifier` et `POST /api/v1/organismes/creer_modifier` :
`localisation.region` et `localisation.departement` acceptent `null` pour une
localisation hors de France. `""` reste accepté.
