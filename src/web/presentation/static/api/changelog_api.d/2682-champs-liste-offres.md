---
titre: "Lecture des offres : la liste renvoie versant, lieux, métier, salaires et dates"
type: ajoute
date: 2026-11-28
pr: 2710
liens:
  - https://github.com/betagouv/csplab/issues/2682
---

`GET /api/v1/offres` : chaque offre contient désormais, en plus des champs actuels,
inchangés, `organisation_siret`, `versant`, `type_contrat`, `vacance_poste`,
`profession`, `localisation`, `fin_publication`, `debut_contrat`, `fin_candidature`,
`debut_vacance_poste` et les salaires (`conditions.salaire_titulaire`,
`conditions.salaire_contractuel`), au format de
`GET /api/v1/offres/sources/{source_id}`.
