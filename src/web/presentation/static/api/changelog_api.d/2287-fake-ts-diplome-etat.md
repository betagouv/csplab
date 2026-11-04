---
type: modifie
date: 2026-11-04
pr: 0
liens:
  - https://github.com/betagouv/csplab/issues/2287
---

`GET /api/fake-ts/offers/getoffer` renvoie le diplôme d'État exigé dans
`customFields.offerCustomBlock1.customCodeTable3`, comme Talentsoft : objet codé de type
« Diplômes d'Etat », `label` = `criteres.diplome` et `clientCode` = son code Talentsoft
(ex. `CSPU0002` pour « Diplôme d'Etat d'infirmier »). Il vaut `null` si
`criteres.diplome` est vide ou n'est pas l'un des 23 diplômes d'État du référentiel
Talentsoft.

`diploma` vaut désormais toujours `null`, comme dans Talentsoft : il reprenait
`criteres.diplome`.
