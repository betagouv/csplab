---
titre: "Changelog : un titre court pour chaque changement"
type: ajoute
date: 2026-11-06
pr: 2356
liens:
  - https://github.com/betagouv/csplab/issues/2353
---

`GET /api/changelog.json` : chaque entrée a un nouveau champ `titre`, une phrase courte
qui dit ce qui change, en Markdown (un nom de champ ou une valeur entre backticks).
`GET /api/changelog.atom` l'utilise, sans ses backticks, comme titre de chaque entrée,
précédé de ⚠️ pour un changement non rétrocompatible, au lieu du type et des routes. `GET /api/changelog.md` l'affiche en gras en tête de chaque
entrée.
