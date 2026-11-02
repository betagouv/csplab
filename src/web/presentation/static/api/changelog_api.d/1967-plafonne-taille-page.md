---
type: modifie
date: 2026-10-15
pr: 1967
liens:
  - https://github.com/betagouv/csplab/issues/1962
---

`GET /api/v1/offres`, `GET /api/v1/offres/sources/{source_id}` et
`GET /api/v1/metiers` : le paramètre `taille` est plafonné à `1000`. Une valeur
supérieure est ramenée à `1000`, et le lien `next` reprend cette taille. Pour
récupérer plus d'éléments, suivez le lien `next`. Une valeur de `taille` ou `page`
non numérique ou inférieure à `1` est remplacée par la valeur par défaut, au lieu
de renvoyer une erreur `500`.

`GET /api/fake-ts/offersummaries` : le paramètre `count` est plafonné à
`1000`, comme `taille`. Une valeur non numérique ou inférieure à `1` pour `count`,
ou inférieure à `0` pour `start`, est remplacée par la valeur par défaut (`100`
pour `count`, `0` pour `start`).
