---
type: non_retrocompatible
date: 2026-10-14
pr: 1941
---

`GET /api/v1/offres/sources/{source_id}` : l'accès à une source non autorisée pour
l'utilisateur authentifié renvoie désormais une erreur `403 Forbidden` au lieu de
`401 Unauthorized`, comme `POST /api/v1/offres/creer_modifier` et
`POST /api/v1/offres/archiver`. Le corps de la réponse ne change pas. Le code `401`
ne signale plus qu'une authentification manquante ou invalide.
