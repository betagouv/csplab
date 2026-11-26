---
titre: "Offres : `organisation.siret` obligatoire et relié à l'organisme"
type: non_retrocompatible
date: 2026-11-25
pr: 2586
liens:
  - https://github.com/betagouv/csplab/issues/2576
---

`POST /api/v1/offres/creer_modifier` : l'offre est rattachée à l'organisme de son
`organisation.siret`, jusqu'ici ignoré. Une offre est rejetée dans `errors` si ce SIRET
est vide, invalide (14 chiffres, clé de contrôle comprise) ou ne correspond à aucun
organisme de `GET /api/v1/organismes`.

### Compatibilité

Renseignez le `siret` renvoyé par `GET /api/v1/organismes`.
