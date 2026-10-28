---
type: modifie
date: 2026-10-19
pr: 1990
liens:
  - https://github.com/betagouv/csplab/issues/1791
---

- `GET /api/fake-ts/offers/getoffer` : `endPublicationDate` n'est plus toujours
  `null`. Il reprend `fin_publication`, et reste à `null` pour les offres transmises
  avant ce changement.
