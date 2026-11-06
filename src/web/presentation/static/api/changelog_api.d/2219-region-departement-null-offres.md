---
titre: "Lecture des offres : `region` et `departement` à `null` hors de France"
type: non_retrocompatible
date: 2026-11-03
pr: 2236
liens:
  - https://github.com/betagouv/csplab/issues/2219
---

`GET /api/v1/offres` : pour une offre localisée hors de France, `region` et
`departement` valent désormais `null`, et non plus `""`. `GET /api/v1/organismes`
renvoyait déjà `null` pour un organisme hors de France : le schéma le déclare
désormais.
