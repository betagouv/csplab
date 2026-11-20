---
titre: "Lecture d'une offre : `localisation` devient une liste de lieux"
type: non_retrocompatible
date: 2026-11-04
pr: 2264
liens:
  - https://github.com/betagouv/csplab/issues/1793
---

`GET /api/v1/offres/sources/{source_id}` : `localisation` est désormais une **liste**
de lieux, comme en entrée de `POST /api/v1/offres/creer_modifier`, dans l'ordre d'envoi.
Le premier est le lieu principal. Une offre sans localisation renvoie `[]` au lieu de
`null`.

`GET /api/v1/offres` : les filtres `region`, `departement`, `pays`, `zone` et le filtre
par rayon (`latitude`, `longitude`, `radius`) retiennent une offre dont **l'un** des lieux
correspond. Les filtres `region`, `departement`, `pays` et `zone` portent sur un même
lieu.

`GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` : `country`,
`region` et `department` contiennent un élément par valeur distincte parmi les lieux de
l'offre. `location`, `latitude`, `longitude`, `geolocation` et
`customFields.location.shortText1` reprennent le lieu principal.

### Compatibilité

Changement **incompatible** pour `GET /api/v1/offres/sources/{source_id}` : un client qui
lit `localisation` comme un objet doit la lire comme une liste et prendre son premier
élément pour retrouver le comportement précédent. Les autres changements sont
rétrocompatibles.
