---
type: ajoute
date: 2026-10-08
pr: 1815
liens:
  - https://github.com/betagouv/csplab/issues/1799
---

- `POST /api/v1/offres/creer_modifier` : le champ `publication.debut_vacance_poste`
  (date à partir de laquelle le poste est vacant) est désormais enregistré. Il était
  accepté jusqu'ici, mais ignoré.
- `GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient un nouveau
  champ `job_vacancy_date`, valeur de `publication.debut_vacance_poste` (date ISO
  8601), à `null` si l'information n'a pas été transmise.

### Compatibilité

Ces changements sont rétrocompatibles : un appel valide avant ces changements reste
valide, et le champ ajouté dans les réponses n'en retire aucun. `professionalCategory`
passe d'une chaîne toujours `null` à un objet codé, comme dans l'API Talentsoft.
