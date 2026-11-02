---
type: non_retrocompatible
date: 2026-10-27
pr: 2069
liens:
  - https://github.com/betagouv/csplab/issues/2068
---

`POST /api/v1/offres/creer_modifier` : une offre dont
`organisation.talentsoft_organisme_entity_code` est renseigné est désormais rejetée
avec une authentification par JWT. Elle apparaît dans `errors`, avec le message
« Champ réservé au service ingestion de CSPLab. ». Ce champ n'a jamais été destiné aux
partenaires.

### Compatibilité

Laissez `organisation.talentsoft_organisme_entity_code` vide ou ne l'envoyez pas.
