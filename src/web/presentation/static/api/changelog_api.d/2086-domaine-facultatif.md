---
type: modifie
date: 2026-10-28
pr: 2086
liens:
  - https://github.com/betagouv/csplab/issues/2070
---

- `POST /api/v1/offres/creer_modifier` : `profession.domaine` devient facultatif.
  Absent, il est déduit du métier. Il reste obligatoire lorsque le code métier relève
  de plusieurs domaines (aujourd'hui `ERJUS008` : `JUS` ou `CTL`, et `ERTRA007` :
  `SEC` ou `TRA`) : il doit alors être l'un d'eux.
