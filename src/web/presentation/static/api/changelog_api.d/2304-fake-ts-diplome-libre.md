---
type: modifie
date: 2026-11-05
pr: 0
liens:
  - https://github.com/betagouv/csplab/issues/2304
---

`GET /api/fake-ts/offers/getoffer` renvoie aussi un diplôme saisi en texte libre dans
`criteres.diplome` : `customFields.offerCustomBlock1.customCodeTable3` est un objet codé
de type « Diplômes d'Etat » avec `label` = `criteres.diplome` et `clientCode` vide. Il
valait `null`. Un diplôme du référentiel des diplômes d'État garde son code Talentsoft
(ex. `CSPU0002`), et `customCodeTable3` vaut toujours `null` si `criteres.diplome` est vide.
