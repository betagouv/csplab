---
titre: "Offres : une offre hors de France est acceptée"
type: corrige
date: 2026-11-02
pr: 2210
liens:
  - https://github.com/betagouv/csplab/issues/2205
---

`POST /api/v1/offres/creer_modifier` : une offre localisée hors de France (`pays`
différent de `FRA`, `region` et `departement` vides) est enregistrée. Elle était
jusqu'ici rejetée dans `errors`. Une offre hors de France qui renseigne `region` ou
`departement` est rejetée dans `errors`. `GET /api/v1/offres` renvoie `region` et
`departement` vides pour ces offres, et `GET /api/fake-ts/offersummaries` et
`GET /api/fake-ts/offers/getoffer` renvoient `region` et `department` vides (`[]`).

`POST /api/v1/organismes/creer_modifier` : la même règle s'applique aux organismes.
`region` et `departement` sont obligatoires pour `FRA` et doivent être vides pour tout
autre pays. Un organisme qui ne la respecte pas est rejeté dans `errors`, avec un
message explicite. Un organisme hors de France avec une région et un département, jusqu'ici
enregistré, est désormais rejeté.
