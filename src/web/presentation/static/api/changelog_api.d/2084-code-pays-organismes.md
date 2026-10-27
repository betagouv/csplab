---
type: non_retrocompatible
date: 2026-10-26
pr: 2084
liens:
  - https://github.com/betagouv/csplab/issues/2074
---

`POST /api/v1/organismes/creer_modifier` : un organisme dont `localisation.pays` n'est pas
un code ISO 3166-1 alpha-3 en majuscules (`fra`, `XXX`…) est désormais rejeté. Il
apparaît dans `errors`, avec le message « Code pays invalide, un code ISO 3166-1 alpha-3
en majuscules est attendu (ex. FRA). ». Jusqu'ici, tout code de 3 caractères était
enregistré tel quel.
