---
type: ajoute
date: 2026-10-29
pr: 2166
liens:
  - https://github.com/betagouv/csplab/issues/2158
  - https://github.com/betagouv/csplab/issues/1796
---

`GET /api/fake-ts/offers/getoffer` : `customFields.offerCustomBlock1.longText2` contient
le fondement juridique (`conditions.bases_legales`) en Markdown, et
`customFields.offerCustomBlock1.longText2Formatted` son rendu HTML. Les deux valent `null`
si l'offre n'en a pas.
