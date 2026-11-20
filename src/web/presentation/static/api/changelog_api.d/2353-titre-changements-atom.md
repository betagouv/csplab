---
titre: "Changelog : le flux Atom titre chaque entrée par ce qui change"
type: modifie
date: 2026-11-18
pr: 2356
liens:
  - https://github.com/betagouv/csplab/issues/2353
---

`GET /api/changelog.atom` : le titre de chaque entrée est le titre du changement, sans
ses backticks, précédé de ⚠️ pour un changement non rétrocompatible ou retiré, au lieu
du type et des routes. Le type reste dans les catégories de l'entrée.

### Compatibilité

Le titre des entrées déjà publiées change, leur `id` reste le même : certains lecteurs de
flux peuvent les afficher une fois comme modifiées.
