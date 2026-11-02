---
type: non_retrocompatible
date: 2026-10-22
pr: 2051
liens:
  - https://github.com/betagouv/csplab/issues/1833
---

`GET /api/v1/metiers` : le champ `offer_family_code` de chaque métier renvoyé devient
`code_emploi_csp`, du nom du « Code CSP » du RMFP. Sa valeur ne change pas : c'est
toujours le code à renseigner dans `profession.metier` de
`POST /api/v1/offres/creer_modifier`. Les autres champs d'un métier ne changent pas.

### Compatibilité

Lisez désormais le code dans `code_emploi_csp` : `offer_family_code` n'est
plus renvoyé.
