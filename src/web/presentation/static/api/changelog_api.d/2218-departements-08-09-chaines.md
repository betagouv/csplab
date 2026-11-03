---
type: corrige
date: 2026-11-03
pr: 2224
liens:
  - https://github.com/betagouv/csplab/issues/2218
---

Schéma OpenAPI : les départements `08` (Ardennes) et `09` (Ariège) sont des chaînes,
comme les autres codes de département. Un client généré depuis le schéma les typait
comme les entiers `8` et `9`, pour le champ `departement` des offres et des organismes
et pour le filtre `departement` de `GET /api/v1/offres` et `GET /api/v1/organismes`.
