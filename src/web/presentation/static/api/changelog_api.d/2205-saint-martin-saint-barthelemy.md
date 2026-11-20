---
titre: "Offres et organismes : Saint-Barthélemy et Saint-Martin acceptés"
type: ajoute
date: 2026-11-02
pr: 2208
liens:
  - https://github.com/betagouv/csplab/issues/2205
---

`POST /api/v1/offres/creer_modifier` et `POST /api/v1/organismes/creer_modifier` :
les départements `977` (Saint-Barthélemy) et `978` (Saint-Martin) sont acceptés, avec
la région `TOM` et la zone géographique `AM`. Le filtre `departement` de
`GET /api/v1/offres` et `GET /api/v1/organismes` les accepte aussi, et le référentiel
`GET /api/fake-ts/referentials/department` les liste.
