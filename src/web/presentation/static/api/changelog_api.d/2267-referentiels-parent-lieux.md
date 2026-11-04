---
type: modifie
date: 2026-11-04
pr: 2270
liens:
  - https://github.com/betagouv/csplab/issues/2267
---

`GET /api/fake-ts/referentials/{type}` : les lieux sont désormais rattachés à leur parent.
Un département a pour parent sa région (`parentType: region`, `DOM` ou `TOM` outre-mer), une
région `FRA` (`parentType: country`), un pays sa zone (`parentType: area`, ex. `EUROPE`).
Pour les lieux, `code` restant `null`, `parentCode` est le `clientCode` du parent : il est
donc une chaîne, alors qu'il reste un entier pour les organisations. `hasChildren` indique
si une zone, un pays ou une région a des descendants.
