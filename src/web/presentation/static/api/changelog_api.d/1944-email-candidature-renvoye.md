---
type: ajoute
date: 2026-10-14
pr: 1944
---

`GET /api/v1/offres/sources/{source_id}` : nouveau champ `email_candidature`, vide si
l'offre se candidate par lien (`url_candidature`).

`GET /api/fake-ts/offers/getoffer` : l'adresse email de candidature est
renvoyée dans `customFields.origin.shortText1`, comme dans Talentsoft.
