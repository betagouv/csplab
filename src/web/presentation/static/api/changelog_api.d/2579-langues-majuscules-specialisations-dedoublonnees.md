---
titre: "Offres : codes de langue en majuscules, spécialisations sans doublon"
type: modifie
date: 2026-11-23
pr: 2580
liens:
  - https://github.com/betagouv/csplab/issues/2579
---

`POST /api/v1/offres/creer_modifier` :

- `criteres.langues[].iso_code` est enregistré en majuscules : `en` devient `EN`.
  Les routes de lecture des offres et l'API fake-ts (`languageName.clientCode`)
  renvoient donc toujours un code en majuscules ;
- les doublons de `criteres.specialisations` sont retirés, dans l'ordre reçu, comme
  ceux de `contacts[].emails`.
