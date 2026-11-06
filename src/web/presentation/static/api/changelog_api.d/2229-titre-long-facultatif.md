---
titre: "Offres : le titre long devient facultatif"
type: modifie
date: 2026-11-03
pr: 2229
liens:
  - https://github.com/betagouv/csplab/issues/2202
---

- `POST /api/v1/offres/creer_modifier` : `titre_long` devient facultatif. Il peut
  être omis, envoyé à `null` ou vide : l'offre n'a alors pas de titre long, et
  `titre_long` vaut `null` dans `GET /api/v1/offres/sources/{source_id}`. Ne le
  renseignez que s'il diffère de `titre`.
- `POST /api/v1/offres/creer_modifier` : une offre dont le `titre_long` est
  identique à `titre` est rejetée, avec une erreur sur `titre_long`.
- Les titres longs identiques au titre de l'offre ont été effacés : `titre_long` vaut
  désormais `null` pour ces offres.
