---
type: ajoute
date: 2026-10-28
pr: 2091
liens:
  - https://github.com/betagouv/csplab/issues/2090
---

`GET /api/fake-ts/offers/getoffer` : `customFields.applicantCriteria.customCodeTable1`
contient les documents à transmettre, au format du référentiel Talentsoft « Documents
à transmettre » (`Doc_CV`, `Doc_CV_LM`, `Doc_CV_PF`, `Doc_CV_LM_PF`). Il vaut `null`
si l'offre ne demande aucun document ou si la combinaison n'existe pas dans ce
référentiel (par exemple une lettre de motivation sans CV).
