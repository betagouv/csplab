---
type: non_retrocompatible
date: 2026-10-27
pr: 2067
liens:
  - https://github.com/betagouv/csplab/issues/2066
---

`GET /api/v1/offres`, `GET /api/v1/offres/sources/{source_id}` et `GET /api/v1/metiers`
changent de comportement de pagination :

- une `page` au-delà de la dernière renvoie une erreur `404`, au lieu d'une liste
  `results` vide ;
- une `page` non numérique ou inférieure à `1` renvoie une erreur `404`, au lieu de la
  première page ;
- les liens `next` et `previous` ne contiennent `taille` que s'il est passé dans la
  requête, et le lien vers la première page ne contient plus `page`.

Le format de la réponse (`count`, `next`, `previous`, `results`) ne change pas. Une
`taille` invalide est toujours remplacée par la valeur par défaut, et une `taille`
supérieure à `1000` toujours ramenée à `1000`.

### Compatibilité

Pour parcourir une liste, suivez le lien `next` jusqu'à ce qu'il vaille `null`, plutôt
que d'incrémenter `page` jusqu'à obtenir une liste vide.
