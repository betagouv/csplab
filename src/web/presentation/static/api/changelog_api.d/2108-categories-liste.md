---
type: non_retrocompatible
date: 2026-10-28
pr: 2108
liens:
  - https://github.com/betagouv/csplab/issues/2079
---

`GET /api/v1/offres` et `GET /api/v1/offres/sources/{source_id}` : le champ
`categorie` est remplacé par `categories`, la liste des catégories de l'offre dans
l'ordre d'envoi.

`POST /api/v1/offres/creer_modifier` : une offre dont `categories` contient une valeur
vide (`[""]`) est désormais rejetée et apparaît dans `errors`. Une liste vide (`[]`)
reste acceptée pour une offre sans catégorie.

### Compatibilité

Lisez les catégories d'une offre dans `categories` au lieu de `categorie`.
