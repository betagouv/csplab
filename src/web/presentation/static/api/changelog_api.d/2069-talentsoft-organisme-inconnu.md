---
type: corrige
date: 2026-10-27
pr: 2069
liens:
  - https://github.com/betagouv/csplab/issues/2068
---

- `POST /api/v1/offres/creer_modifier` : un code `talentsoft_organisme_entity_code`
  inconnu ne fait plus échouer toute la requête avec une erreur 500. Seule l'offre
  concernée est rejetée, dans `errors`, et les autres offres du lot sont enregistrées.
