# Changelog de l'API CSPLab

Ce changelog liste les changements de l'API publique CSPLab (routes `/api/v1/…` et
`/api/fake-ts/…`) qui concernent les partenaires qui l'utilisent. Le détail des
champs et de leurs règles se trouve dans le [guide de l'API](/pages/guide_api).

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## 2026-10-07

### Ajouté

- `POST /api/v1/offres/creer_modifier` : `identification.reference` accepte la valeur
  `"auto"`. CSPLab génère alors une référence au format `CSP-AAAA-NNNNNN` (par
  exemple `CSP-2026-000042`), unique sur toute la plateforme. `"auto"` crée toujours une nouvelle
  offre : pour la mettre à jour ensuite, renvoyez la référence générée. Une
  référence au format `CSP-AAAA-NNNNNN` qui ne désigne pas une offre existante de
  la source est rejetée dans `errors`.
- `POST /api/v1/offres/creer_modifier` : la réponse contient un nouveau champ
  `offres`, qui donne pour chaque offre créée ou mise à jour son `index` dans le
  payload, sa `reference` finale et son `statut` (`created` ou `updated`).
- `POST /api/v1/offres/creer_modifier` : chaque entrée de `errors` contient un
  nouveau champ `index`, la position de l'offre rejetée dans le payload.

## 2026-10-06

### ⚠️ Changements non rétrocompatibles

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

## 2026-10-05

### Ajouté

- `POST /api/v1/offres/creer_modifier` : deux nouveaux champs **facultatifs** dans le
  bloc `description` :
  - `conditions_exercice` : conditions particulières d'exercice du poste (texte,
    10 000 caractères maximum, peut être vide) ;
  - `descriptif_service` : description du service qui recrute (texte, 10 000
    caractères maximum, peut être vide).
- `POST /api/v1/offres/creer_modifier` : le champ `publication.fin_candidature` (date
  limite de candidature) est désormais enregistré. Il était accepté jusqu'ici, mais
  ignoré.
- `GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient trois
  nouveaux champs, à `null` si l'information n'a pas été transmise :
  - `exercise_conditions` : valeur de `description.conditions_exercice` ;
  - `service_description` : valeur de `description.descriptif_service` ;
  - `application_deadline` : valeur de `publication.fin_candidature` (date ISO 8601).
- `GET /api/fake-ts/offers/getoffer` : `customFields` n'est plus toujours `null`. Il
  reprend la structure des champs personnalisés Talentsoft :
  - `offer.date1` : date limite de candidature ;
  - `description.longText1` : présentation de l'employeur ;
  - `description.longText2` : conditions particulières d'exercice ;
  - `description.longText3` : description du service ;
  - `location.shortText1` : libellé de la localisation ;
  - `offerCustomBlock1.longText1` : informations complémentaires.

  Les autres clés de chaque bloc (`date1`, `shortText1`, `longText1` à `longText3`)
  valent `null`.
- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `contractDuration` renvoie la durée du contrat (`conditions.duree_contrat`) au lieu
  de `null`.

### Modifié

- `POST /api/v1/offres/creer_modifier` : `description.employeur` accepte maintenant un
  texte vide. Le champ reste obligatoire. Une offre dont l'employeur est vide n'est
  plus rejetée, et `employer` vaut alors `null` dans les réponses.

### Compatibilité

Ces changements sont rétrocompatibles : un appel valide avant ces changements reste
valide, et les champs ajoutés dans les réponses n'en retirent aucun.
