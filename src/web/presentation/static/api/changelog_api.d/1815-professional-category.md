---
type: modifie
date: 2026-10-08
pr: 1815
liens:
  - https://github.com/betagouv/csplab/issues/1799
---

- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `professionalCategory` n'est plus toujours `null`. C'est un objet codé qui reprend
  `vacance_poste` : `clientCode` vaut `STATUT01` (poste vacant) ou `STATUT02` (poste
  susceptible d'être vacant). Il reste à `null` si la vacance de poste n'est pas
  renseignée.
