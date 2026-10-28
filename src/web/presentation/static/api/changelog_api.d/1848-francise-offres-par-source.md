---
type: non_retrocompatible
date: 2026-10-13
pr: 1848
liens:
  - https://github.com/betagouv/csplab/issues/1828
---

`GET /api/v1/offres/sources/{source_id}` : les champs renvoyés sont renommés en
français, avec les noms déjà utilisés par `POST /api/v1/offres/creer_modifier`.

- `title` devient `titre` ;
- `long_title` devient `titre_long` ;
- `organization` devient `organisation` ;
- `employer` devient `employeur` ;
- `profile` devient `profil` ;
- `exercise_conditions` devient `conditions_exercice` ;
- `service_description` devient `descriptif_service` ;
- `verse` devient `versant` ;
- `category` devient `categorie` ;
- `offer_nature` devient `nature_offre` ;
- `contract_kind` devient `type_contrat` ;
- `job_vacancy` devient `vacance_poste` ;
- `offer_url` devient `url_offre` ;
- `application_url` devient `url_candidature` ;
- `criteria` devient `criteres` ;
- `publication_date` devient `debut_publication` ;
- `beginning_date` devient `debut_contrat` ;
- `application_deadline` devient `fin_candidature` ;
- `job_vacancy_date` devient `debut_vacance_poste` ;
- `archived_at` devient `date_archivage`.

`reference`, `source_id`, `mission`, `complements`, `localisation` et `conditions`
ne changent pas, ni leurs sous-champs, ni les valeurs renvoyées. `contacts` garde son
nom, mais son format change (voir plus bas).
