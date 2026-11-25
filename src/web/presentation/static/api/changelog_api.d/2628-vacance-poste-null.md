---
titre: "Offres : `vacance_poste` devient facultatif et vaut `null` s'il n'est pas connu"
type: non_retrocompatible
date: 2026-11-25
pr: 2631
liens:
  - https://github.com/betagouv/csplab/issues/2628
---

`POST /api/v1/offres/creer_modifier` : `vacance_poste` devient facultatif. Si
l'information n'est pas connue, omettez-le ou envoyez `null`, comme le renvoie
`GET /api/v1/offres/sources/{source_id}`. `""` est désormais rejeté dans `errors`.
