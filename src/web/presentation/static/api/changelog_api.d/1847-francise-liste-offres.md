---
type: non_retrocompatible
date: 2026-10-13
pr: 1847
liens:
  - https://github.com/betagouv/csplab/issues/1827
---

`GET /api/v1/offres` : les champs renvoyés et deux filtres sont renommés en français,
avec les noms déjà utilisés par `POST /api/v1/offres/creer_modifier`.

- Champs de chaque offre renvoyée :
  - `title` devient `titre` ;
  - `organization` devient `organisation` ;
  - `offer_nature` devient `nature_offre` ;
  - `category` devient `categorie` ;
  - `publication_date` devient `debut_publication` ;
  - `offer_url` devient `url_offre` ;
  - `archived_at` devient `date_archivage`.

  `reference` et `source_id` ne changent pas, ni les valeurs renvoyées.
- Filtres :
  - `organisme` devient `organisation` (ex. `?organisation=ORG1&organisation=ORG2`) ;
  - `date_publication` devient `debut_publication` (ex. `?debut_publication=-7`).

> **Attention :** les anciens noms de filtre ne sont plus reconnus et sont ignorés
> sans erreur : un appel qui les utilise encore renvoie les offres **non filtrées**.
