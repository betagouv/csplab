---
type: modifie
date: 2026-10-21
pr: 2028
liens:
  - https://github.com/betagouv/csplab/issues/2023
---

- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `organisationDescription` reprend désormais la description de l'organisme Talentsoft
  lié à l'offre. Il reprenait jusqu'ici la présentation de l'employeur
  (`description.employeur`), toujours disponible dans
  `customFields.description.longText1`.
