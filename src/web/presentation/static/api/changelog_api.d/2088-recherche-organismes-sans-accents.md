---
type: modifie
date: 2026-10-28
pr: 0
liens:
  - https://github.com/betagouv/csplab/issues/2088
---

`GET /api/v1/organismes` : le filtre `nom` ne tient plus compte des accents. `hopital`
trouve désormais « Hôpital … », et `hôpital` trouve « Hopital … ».
