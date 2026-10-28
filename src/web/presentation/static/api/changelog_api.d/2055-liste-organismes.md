---
type: ajoute
date: 2026-10-22
pr: 2055
liens:
  - https://github.com/betagouv/csplab/issues/2053
---

- `GET /api/v1/organismes` : liste paginée (`page`, `taille`) des organismes du
  référentiel CSPLab (FINESS, GIPCDG et DILA), triée par nom. Accessible avec un jeton
  JWT uniquement. Filtres : `versant` (plusieurs valeurs séparées par une virgule),
  `siret`, `nom` (recherche partielle), `departement` et `referentiel`. Chaque
  organisme contient `id`, `nom`, `versant`, `siret`, `parent_id`, `referentiel`,
  `external_id`, `millesime` et `localisation`. Les valeurs `nom` et `siret` sont
  celles à reprendre dans le bloc `organisation` de
  `POST /api/v1/offres/creer_modifier`.
