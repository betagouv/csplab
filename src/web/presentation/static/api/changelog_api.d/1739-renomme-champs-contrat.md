---
type: non_retrocompatible
date: 2026-10-06
pr: 1739
liens:
  - https://github.com/betagouv/csplab/issues/1696
  - https://github.com/betagouv/csplab/pull/1742
---

Les champs qui décrivent le contrat d'une offre sont renommés, pour mieux refléter la
fonction publique et les offres qui ne donnent pas lieu à un contrat.

> **Attention :** `type_contrat` existe toujours mais **change de sens**. Il désigne
> désormais la forme du contrat (ancien `forme_contrat`). L'ancienne valeur de
> `type_contrat` (ex. `TITULAIRE_CONTRACTUEL`) doit être envoyée dans `nature_offre`.

- `POST /api/v1/offres/creer_modifier` :
  - `type_contrat` est renommé `nature_offre` (obligatoire). Sa valeur `CONTRACTUELS`
    devient `CONTRACTUEL`. Valeurs : `TITULAIRE_CONTRACTUEL`, `CONTRACTUEL`,
    `TERRITORIAL` ;
  - `forme_contrat` est renommé `type_contrat`. Ce n'est plus une liste mais une valeur
    unique, facultative (vide ou `null` si l'offre n'est pas soumise à
    contractualisation). Valeurs : `CDD`, `CDI`, `CDD_CDI` (CDD ou CDI),
    `CONTRAT_PROJET` (contrat de projet), `VACATION`. La valeur `PERMANENT` est
    supprimée.
- `GET /api/v1/offres` : le filtre `type_contrat` est renommé `nature_offre`, et la
  valeur `CONTRACTUELS` devient `CONTRACTUEL`.
- `GET /api/v1/offres` et `GET /api/v1/offres/sources/{source_id}` : le champ
  `contract_type` est renommé `offer_nature`, et renvoie `CONTRACTUEL` au lieu de
  `CONTRACTUELS`.
- `GET /api/v1/offres/sources/{source_id}` : `contract_kind` n'est plus une liste mais
  une valeur unique ou `null` (`CDD`, `CDI`, `CDD ou CDI`, `Contrat de projet`,
  `Payés à l'acte`). La valeur `Vacation` devient `Payés à l'acte`.
- `/api/fake-ts/…` : le code `CONTRACTUELS` devient `CONTRACTUEL` dans le filtre
  `contractType` de `GET /api/fake-ts/offersummaries`, dans le champ `contractType`
  des offres renvoyées et dans `GET /api/fake-ts/referentials/contract_type`.
  Les libellés de ce référentiel changent aussi : « Ouvert aux fonctionnaires et aux
  contractuels », « Ouvert uniquement aux contractuels », « Ouvert aux fonctionnaires
  et lauréats d'un concours territorial ».

### Migration des offres existantes

- `CONTRACTUELS` devient `CONTRACTUEL`.
- Une offre avec les formes de contrat CDD et CDI passe à `CDD_CDI`.
- `PERMANENT` devient `CDI`.
