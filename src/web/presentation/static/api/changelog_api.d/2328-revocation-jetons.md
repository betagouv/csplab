---
type: ajoute
date: 2026-11-05
pr: 2328
liens:
  - https://github.com/betagouv/csplab/issues/2328
---

Les jetons de rafraîchissement d'un compte partenaire peuvent être révoqués par l'équipe
CSPLab, par exemple après un accès depuis une adresse IP non autorisée.
`POST /api/token/refresh` renvoie alors `401` avec le code `token_not_valid` : il faut
obtenir un nouveau jeton avec `POST /api/token`.
