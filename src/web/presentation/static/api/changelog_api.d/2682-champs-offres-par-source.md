---
titre: "Lecture des offres : `profession`, `organisation_siret` et dates de l'offre"
type: ajoute
date: 2026-11-28
pr: 2707
liens:
  - https://github.com/betagouv/csplab/issues/2682
---

`GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient quatre
nouveaux champs :

- `profession` : `referentiel`, `domaine`, `metier`, comme envoyés à
  `POST /api/v1/offres/creer_modifier`, et `metier_libelle`, libellé du métier dans
  `GET /api/v1/metiers` (`null` si le métier n'y figure pas) ;
- `organisation_siret` : SIRET de l'organisme de l'offre, `null` pour une offre
  Talentsoft dont l'organisme n'est pas encore relié au référentiel ;
- `date_creation` et `date_mise_a_jour` : dates de création et de dernière
  modification de l'offre dans CSPLab (ISO 8601).
