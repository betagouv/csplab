---
type: ajoute
date: 2026-10-19
pr: 1990
liens:
  - https://github.com/betagouv/csplab/issues/1791
---

- `POST /api/v1/offres/creer_modifier` : le champ obligatoire
  `publication.fin_publication` (date de fin de publication) est désormais
  enregistré. Il était exigé jusqu'ici, mais ignoré.
- `GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient un nouveau
  champ `fin_publication` (date ISO 8601), à `null` pour les offres transmises avant
  ce changement.

### Compatibilité

Ces changements sont rétrocompatibles : un appel valide avant ces changements reste
valide, et le champ ajouté dans les réponses n'en retire aucun.
