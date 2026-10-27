---
type: non_retrocompatible
date: 2026-10-13
pr: 1852
liens:
  - https://github.com/betagouv/csplab/issues/1830
---

`POST /api/v1/offres/creer_modifier` : les champs de la réponse et les valeurs de
`offres[].statut` sont renommés en français.

- `created` devient `creees` ;
- `updated` devient `mises_a_jour` ;
- dans chaque élément de `offres`, la valeur de `statut` `created` devient `creee`
  et `updated` devient `mise_a_jour` ;
- dans chaque élément de `errors`, `offer` devient `offre`.

`offres` et ses sous-champs `index`, `reference` et `statut` gardent leur nom.
`errors` et `errors[].error` ne changent pas pour l'instant.
