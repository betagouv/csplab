---
titre: "Documentation : les réponses `401` suivent le mode d'authentification"
type: corrige
date: 2026-11-27
pr: 2694
liens:
  - https://github.com/betagouv/csplab/issues/2689
---

La documentation Redoc décrit la réponse `401` de chaque route selon les modes
d'authentification qu'elle accepte : un exemple par refus (jeton JWT invalide ou expiré,
clé d'API invalide, adresse IP non autorisée) et le schéma du corps renvoyé.

`POST /api/v1/organismes/creer_modifier`, `PUT /api/v1/organismes` et
`POST /api/v1/talentsoft_organisme/creer_modifier` documentaient un corps `{"error": …}` :
l'API renvoie `{"detail": …}`. Le comportement de l'API ne change pas.
