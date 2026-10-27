---
type: ajoute
date: 2026-10-05
pr: 1727
---

- `POST /api/v1/offres/creer_modifier` : deux nouveaux champs **facultatifs** dans le
  bloc `description` :
  - `conditions_exercice` : conditions particulières d'exercice du poste (texte,
    10 000 caractères maximum, peut être vide) ;
  - `descriptif_service` : description du service qui recrute (texte, 10 000
    caractères maximum, peut être vide).
- `POST /api/v1/offres/creer_modifier` : le champ `publication.fin_candidature` (date
  limite de candidature) est désormais enregistré. Il était accepté jusqu'ici, mais
  ignoré.
- `GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient trois
  nouveaux champs, à `null` si l'information n'a pas été transmise :
  - `exercise_conditions` : valeur de `description.conditions_exercice` ;
  - `service_description` : valeur de `description.descriptif_service` ;
  - `application_deadline` : valeur de `publication.fin_candidature` (date ISO 8601).
- `GET /api/fake-ts/offers/getoffer` : `customFields` n'est plus toujours `null`. Il
  reprend la structure des champs personnalisés Talentsoft :
  - `offer.date1` : date limite de candidature ;
  - `description.longText1` : présentation de l'employeur ;
  - `description.longText2` : conditions particulières d'exercice ;
  - `description.longText3` : description du service ;
  - `location.shortText1` : libellé de la localisation ;
  - `offerCustomBlock1.longText1` : informations complémentaires.

  Les autres clés de chaque bloc (`date1`, `shortText1`, `longText1` à `longText3`)
  valent `null`.
- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `contractDuration` renvoie la durée du contrat (`conditions.duree_contrat`) au lieu
  de `null`.

### Compatibilité

Ces changements sont rétrocompatibles : un appel valide avant ces changements reste
valide, et les champs ajoutés dans les réponses n'en retirent aucun.
