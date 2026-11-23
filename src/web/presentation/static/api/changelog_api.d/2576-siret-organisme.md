---
titre: "Offres : `organisation.siret` vérifié et relié à l'organisme"
type: non_retrocompatible
date: 2026-11-23
pr: 2586
liens:
  - https://github.com/betagouv/csplab/issues/2576
---

`POST /api/v1/offres/creer_modifier` : `organisation.siret`, jusqu'ici accepté sans
contrôle puis ignoré, rattache désormais l'offre à l'organisme de ce SIRET, tel que le
renvoie `GET /api/v1/organismes`. Une offre est rejetée, et apparaît dans `errors`, si
son SIRET :

- est vide, avec le message « SIRET obligatoire : retrouvez-le avec
  `GET /api/v1/organismes`. » ;
- n'est pas composé de 14 chiffres avec une clé de contrôle valide, avec le message
  « SIRET invalide : 14 chiffres avec une clé de contrôle valide attendus. » ;
- ne correspond à aucun organisme, avec le message « Aucun organisme avec ce SIRET :
  retrouvez-le avec `GET /api/v1/organismes`. ».

### Compatibilité

Renseignez le `siret` renvoyé par `GET /api/v1/organismes` : un SIRET vide n'est plus
accepté.
