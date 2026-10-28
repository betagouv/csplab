---
type: corrige
date: 2026-10-22
pr: 2046
liens:
  - https://github.com/betagouv/csplab/issues/2035
---

- `GET /api/v1/metiers` : `code_emploi_csp` est désormais toujours renseigné. Les
  métiers qui n'avaient pas de code ne sont plus renvoyés : ils ne pouvaient pas être
  utilisés dans `profession.metier` de `POST /api/v1/offres/creer_modifier`. L'enquête
  sur les 8 métiers concernés est suivie dans
  [l'issue #2035](https://github.com/betagouv/csplab/issues/2035).
