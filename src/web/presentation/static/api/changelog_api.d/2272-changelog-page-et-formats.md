---
type: ajoute
date: 2026-11-05
pr: 2298
liens:
  - https://github.com/betagouv/csplab/issues/2272
---

Le changelog est publié sur une page du site, `/pages/changelog_api`, filtrable par type de changement, par route et par date, avec un lien vers chaque
changement. Il est aussi disponible pour les outils et les agents :

- `GET /api/changelog.md` : le changelog en Markdown ;
- `GET /api/changelog.json` : une entrée par changement, avec ses routes, sa PR et ses
  tickets ;
- `GET /api/changelog.atom` : un flux Atom, pour être prévenu des nouveaux changements.

Ces trois routes acceptent les filtres `type` (répétable), `route` et `depuis`
(AAAA-MM-JJ), par exemple
`/api/changelog.md?type=non_retrocompatible&depuis=2026-10-15`. Le guide de l'API est
aussi disponible en Markdown, `GET /api/guide.md`, et `/llms.txt` liste ces documents.
