---
titre: "Organismes : CSPLab attribue l'`id`, le parent est désigné par son external_id"
type: non_retrocompatible
date: 2026-11-25
pr: 2641
liens:
  - https://github.com/betagouv/csplab/issues/2621
---

`POST /api/v1/organismes/creer_modifier` :

- l'`id` d'un organisme créé est attribué par CSPLab. Un `id` envoyé est ignoré : il
  ne désigne plus l'organisme à créer ou à mettre à jour, toujours retrouvé par le
  couple (`referentiel`, `external_id`).
- `parent_id` est remplacé par `parent_external_id`, obligatoire, qui vaut
  l'`external_id` du parent dans le même référentiel, ou `null`. Le parent existe déjà
  (non supprimé) ou figure dans le même lot, dans n'importe quel ordre. Sinon
  l'organisme est rejeté dans `errors`, avec un `entity_id` à `null`. Un organisme ne
  peut pas être son propre parent, et les enfants d'un parent rejeté dans le même lot
  sont rejetés aussi.
- un même couple (`referentiel`, `external_id`) envoyé plusieurs fois dans un lot
  n'est enregistré qu'une fois : les entrées suivantes sont rejetées dans `errors`.

### Compatibilité

Envoyez `parent_external_id` à la place de `parent_id`. Un organisme sans
`parent_external_id` est rejeté.
