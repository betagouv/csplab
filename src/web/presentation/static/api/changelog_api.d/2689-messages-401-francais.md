---
titre: "Authentification : les messages de refus sont en français"
type: modifie
date: 2026-11-27
pr: 2694
liens:
  - https://github.com/betagouv/csplab/issues/2689
---

Le champ `detail` d'une réponse `401` est désormais en français :

- clé d'API invalide : `Clé d'API invalide.` au lieu de `Invalid API key.` ;
- clé d'API utilisée depuis une adresse IP non autorisée : `Adresse IP non autorisée.`
  au lieu de `IP address not allowed.` ;
- jeton JWT utilisé depuis une adresse IP non autorisée, sur une route ou sur
  `POST /api/token/refresh` : `Échec de l'authentification.` au lieu de
  `Authentication failed.`.

Le code de réponse ne change pas. Pour distinguer les cas, fiez-vous au code `401`
plutôt qu'au texte du message.
