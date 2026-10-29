---
type: non_retrocompatible
date: 2026-10-29
pr: 2143
liens:
  - https://github.com/betagouv/csplab/issues/2142
---

`POST /api/v1/offres/creer_modifier` : une offre dont `categories` est absente ou vide
(`[]`) est désormais rejetée. Elle apparaît dans `errors`, avec le message « Au moins
une catégorie est obligatoire. ». L'article
[D.311-8 du CGFP](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051961567)
impose qu'une offre indique sa catégorie hiérarchique.

Les offres déjà enregistrées sans catégorie, actives comme archivées, sont supprimées :
`GET /api/v1/offres` ne retourne plus d'offre dont `categories` est vide.

### Compatibilité

Renseignez dans `categories` au moins une valeur parmi `APLUS`, `A`, `B`, `C` et
`HORS_CATEGORIE`.
