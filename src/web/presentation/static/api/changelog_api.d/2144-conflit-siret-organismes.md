---
type: corrige
date: 2026-10-29
pr: 2144
liens:
  - https://github.com/betagouv/csplab/issues/2140
---

- `POST /api/v1/organismes/creer_modifier` : un organisme dont le SIRET est déjà
  porté par un organisme d'un autre référentiel n'est plus ignoré silencieusement.
  Le référentiel qui fait foi l'emporte (DILA, puis FINESS, puis GIPCDG) : l'autre
  organisme est supprimé et ses agents, recrutements, étiquettes et sous-organismes
  sont rattachés à l'organisme reçu. Sinon, l'organisme reçu est rejeté dans
  `errors`, sous la forme `{"entity_id", "error"}`, et n'est plus compté dans
  `created`.
