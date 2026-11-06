---
titre: "fake-ts : référentiels filtrables par `parentCode`"
type: ajoute
date: 2026-11-04
pr: 2270
liens:
  - https://github.com/betagouv/csplab/issues/2267
---

`GET /api/fake-ts/referentials/{type}` accepte un filtre `parentCode` : par exemple,
`referentials/department?parentCode=11` renvoie les départements d'Île-de-France.
