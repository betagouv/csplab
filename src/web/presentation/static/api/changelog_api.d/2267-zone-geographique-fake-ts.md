---
type: ajoute
date: 2026-11-04
pr: 2268
liens:
  - https://github.com/betagouv/csplab/issues/2267
---

`GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
`geographicalLocation` contient désormais un élément par zone géographique distincte
parmi les lieux de l'offre, dans l'ordre des lieux. `clientCode` est le nom de la zone,
comme dans le filtre `area` et `GET /api/fake-ts/referentials/area` (`EUROPE`, `AFRIQUE`,
`AMERIQUE`, `ASIE`, `MOYEN_ORIENT_AFRIQUE_DU_NORD`, `OCEANIE`), et `code` reste `null`.
Le champ était jusqu'ici toujours `[]`.
