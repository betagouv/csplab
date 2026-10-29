---
type: ajoute
date: 2026-10-29
pr: 2157
liens:
  - https://github.com/betagouv/csplab/issues/2152
  - https://github.com/betagouv/csplab/issues/1796
---

`GET /api/fake-ts/offers/getoffer` : `customFields.applicantCriteria.longText1` contient
les compétences attendues (`criteres.competences_requises`) en Markdown, et
`customFields.applicantCriteria.longText1Formatted` leur rendu HTML. Les deux valent
`null` si l'offre n'en a pas.
