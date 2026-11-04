---
type: modifie
date: 2026-11-04
pr: 0
liens:
  - https://github.com/betagouv/csplab/issues/1796
---

`GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
`salaryRange` est un objet codé portant le versant (`clientCode` = `FPE`, `FPT` ou
`FPH`, `label` = son libellé), comme dans Talentsoft. Il valait toujours `null`.

### Compatibilité

Un client qui typait `salaryRange` comme une chaîne doit le lire comme un objet codé.
