---
type: corrige
date: 2026-10-26
pr: 2082
liens:
  - https://github.com/betagouv/csplab/issues/2080
---

- `POST /api/v1/offres/creer_modifier` : `latitude` et `longitude` peuvent désormais
  être omises dans un élément de `localisation`, comme l'indique le guide de l'API.
  Jusqu'ici, une offre sans ces clés était rejetée avec « Ce champ est obligatoire. »,
  et il fallait les envoyer à `null`. Les deux écritures sont acceptées et donnent une
  localisation sans coordonnées.
