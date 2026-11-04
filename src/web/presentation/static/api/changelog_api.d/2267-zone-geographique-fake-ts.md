---
type: ajoute
date: 2026-11-04
pr: 2268
liens:
  - https://github.com/betagouv/csplab/issues/2267
---

`GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
`geographicalLocation` contient désormais un élément par zone géographique distincte
parmi les lieux de l'offre, dans l'ordre des lieux. `clientCode` reprend le code de la
zone (`EU`, `AF`, `AM`, `AS`, `MO`, `OC`) et `code` reste `null`. Le champ était
jusqu'ici toujours `[]`.
