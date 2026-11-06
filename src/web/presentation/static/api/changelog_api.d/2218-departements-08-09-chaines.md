---
titre: "Schéma OpenAPI : départements 08 et 09 typés comme des chaînes"
type: corrige
date: 2026-11-03
pr: 2224
liens:
  - https://github.com/betagouv/csplab/issues/2218
---

Schéma OpenAPI au format YAML : les départements `08` (Ardennes) et `09` (Ariège) sont
entre guillemets, comme les autres codes de département. Un client généré depuis le
fichier YAML par un outil qui suit YAML 1.2 les typait comme les entiers `8` et `9`, pour
le champ `departement` des offres et des organismes et pour le filtre `departement` de
`GET /api/v1/offres` et `GET /api/v1/organismes`. Le schéma JSON chargé par la
documentation renvoyait déjà des chaînes et ne change pas.
