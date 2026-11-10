---
type: ajoute
date: 2026-11-04
pr: 2283
liens:
  - https://github.com/betagouv/csplab/issues/1796
---

`GET /api/fake-ts/offers/getoffer` renvoie les champs de l'offre déjà enregistrés, aux
emplacements où l'ingestion les lit dans une offre Talentsoft. Les objets codés portent
les valeurs de l'API v1 (`clientCode`) et leur libellé (`label`) :

- `customFields.offer.customCodeTable2` : `type_contrat` ;
- `customFields.description.customCodeTable1` : première valeur de `categories` ;
- `customFields.description.customCodeTable3` : `conditions.temps_travail`, `null` pour
  `NON_DEFINI` ;
- `customFields.offerCustomBlock1.customCodeTable1` : `conditions.management` ;
- `customFields.offerCustomBlock1.customCodeTable2` : `conditions.lieu_de_travail`,
  `null` pour `NON_DEFINI` ;
- `customFields.offerCustomBlock1.longText3` : `conditions.note_ouverture_poste_url`,
  et `longText3Formatted` le même texte en HTML ;
- `customFields.origin.shortText2` et `shortText3` : `texte` des contacts `principal`
  et `autre`.

Chaque bloc de `customFields` contient désormais les clés `shortText2`, `shortText3` et
`customCodeTable1` à `customCodeTable3`, à `null` quand l'offre n'a pas de valeur.
