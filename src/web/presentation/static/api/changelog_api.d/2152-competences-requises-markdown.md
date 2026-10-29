---
type: non_retrocompatible
date: 2026-10-29
pr: 2157
liens:
  - https://github.com/betagouv/csplab/issues/2152
---

`POST /api/v1/offres/creer_modifier` : `criteres.competences_requises` est désormais un
texte libre en Markdown de 1 500 caractères maximum, et non plus une liste de textes. Il
peut être vide ou `null`. Une offre qui envoie une liste est rejetée et apparaît dans
`errors`.

`GET /api/v1/offres` et `GET /api/v1/offres/sources/{source_id}` : `criteres.competences_requises`
est un texte en Markdown, ou `null`. Les listes déjà enregistrées ont été converties : une
liste vide devient `null`, les éléments d'une liste non vide sont séparés par des sauts
de ligne.

### Compatibilité

Envoyez les compétences attendues dans un seul texte en Markdown (par exemple une liste
`- Rigueur`) au lieu d'une liste de textes, et lisez-les comme un texte.
