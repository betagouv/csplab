---
titre: "Offres et organismes : `region` et `departement` à `null` hors de France"
type: non_retrocompatible
date: 2026-11-03
pr: 2236
liens:
  - https://github.com/betagouv/csplab/issues/2219
---

`POST /api/v1/offres/creer_modifier` et `POST /api/v1/organismes/creer_modifier` :
pour une localisation hors de France, `localisation.region` et
`localisation.departement` valent `null`. `""` est désormais rejeté dans `errors`.
