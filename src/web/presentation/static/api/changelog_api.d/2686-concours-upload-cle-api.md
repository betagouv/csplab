---
titre: "Concours : l'import de concours est réservé à CSPLab"
type: non_retrocompatible
date: 2026-11-27
pr: 2688
liens:
  - https://github.com/betagouv/csplab/issues/2686
---

`POST /api/v1/concours/upload` n'accepte plus que la clé d'API de CSPLab : un appel
avec un jeton JWT renvoie `401`. La route sert à alimenter le référentiel des
concours et ne concerne pas les partenaires.
