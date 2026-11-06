---
type: ajoute
date: 2026-11-06
pr: 2351
liens:
  - https://github.com/betagouv/csplab/issues/2348
---

`GET /api/v1/metiers` :

- chaque métier renvoyé contient deux nouveaux champs :
  - `actif` : `true` si le métier est actif, `false` s'il est archivé ;
  - `referentiel` : référentiel du `code_emploi_csp` (`RMFPv2`), à renseigner dans
    `profession.referentiel` de `POST /api/v1/offres/creer_modifier` ;
- nouveaux filtres, qui se combinent :
  - `domaine` accepte plusieurs codes séparés par une virgule (ex. `JUS,CTL`) ;
  - `code_emploi_csp` : un ou plusieurs codes séparés par une virgule (ex.
    `ERJUS008,ERNUM001`) ;
  - `actif` : `true` ou `false` ;
  - `versant` : `FPE`, `FPT` ou `FPH`.

### Compatibilité

Sans filtre, la route renvoie toujours tous les métiers, actifs ou archivés. Un code
`domaine` inconnu renvoie désormais une erreur `400` qui liste les codes refusés, au
lieu d'une liste vide.
