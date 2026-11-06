---
titre: "Comptes partenaires restreints à une liste d'adresses IP"
type: ajoute
date: 2026-11-05
pr: 2325
liens:
  - https://github.com/betagouv/csplab/issues/2322
---

Un compte partenaire peut être restreint, sur demande, à une liste d'adresses IP ou de
plages CIDR. Depuis une autre adresse, `POST /api/token`, `POST /api/token/refresh` et
toute route appelée avec un jeton JWT renvoient `401`. Un compte sans plage n'est pas
concerné.
