---
type: modifie
date: 2026-10-20
pr: 2008
liens:
  - https://github.com/betagouv/csplab/issues/1803
---

- `POST /api/v1/offres/creer_modifier` : les six champs du bloc `description`
  (`mission`, `profil`, `employeur`, `complements`, `conditions_exercice`,
  `descriptif_service`) acceptent du Markdown (CommonMark), pour conserver la mise en
  forme des offres (gras, listes, liens). Le détail se trouve dans le
  [guide de l'API](/pages/guide_api).
- `GET /api/v1/offres/sources/{source_id}` : ces mêmes champs sont renvoyés en
  Markdown, tels qu'ils ont été transmis.
- `GET /api/fake-ts/offers/getoffer` : `description1`, `description2` et les
  `longTextN` correspondants contiennent ce Markdown. Les variantes `Formatted`
  restent à `null`.
