# Changelog de l'API CSPLab

Ce changelog liste les changements de l'API publique CSPLab (routes `/api/v1/…` et
`/api/fake-ts/…`) qui concernent les partenaires qui l'utilisent. Le détail des
champs et de leurs règles se trouve dans le [guide de l'API](/pages/guide_api).

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## 2026-10-09

### ⚠️ Changements non rétrocompatibles

`GET /api/v1/offres` : les champs renvoyés et deux filtres sont renommés en français,
avec les noms déjà utilisés par `POST /api/v1/offres/creer_modifier`.

- Champs de chaque offre renvoyée :
  - `title` devient `titre` ;
  - `organization` devient `organisation` ;
  - `offer_nature` devient `nature_offre` ;
  - `category` devient `categorie` ;
  - `publication_date` devient `debut_publication` ;
  - `offer_url` devient `url_offre` ;
  - `archived_at` devient `date_archivage`.

  `reference` et `source_id` ne changent pas, ni les valeurs renvoyées.
- Filtres :
  - `organisme` devient `organisation` (ex. `?organisation=ORG1&organisation=ORG2`) ;
  - `date_publication` devient `debut_publication` (ex. `?debut_publication=-7`).

> **Attention :** les anciens noms de filtre ne sont plus reconnus et sont ignorés
> sans erreur : un appel qui les utilise encore renvoie les offres **non filtrées**.

`GET /api/v1/offres/sources/{source_id}` : les champs renvoyés sont renommés en
français, avec les noms déjà utilisés par `POST /api/v1/offres/creer_modifier`.

- `title` devient `titre` ;
- `long_title` devient `titre_long` ;
- `organization` devient `organisation` ;
- `employer` devient `employeur` ;
- `profile` devient `profil` ;
- `exercise_conditions` devient `conditions_exercice` ;
- `service_description` devient `descriptif_service` ;
- `verse` devient `versant` ;
- `category` devient `categorie` ;
- `offer_nature` devient `nature_offre` ;
- `contract_kind` devient `type_contrat` ;
- `job_vacancy` devient `vacance_poste` ;
- `offer_url` devient `url_offre` ;
- `application_url` devient `url_candidature` ;
- `criteria` devient `criteres` ;
- `publication_date` devient `debut_publication` ;
- `beginning_date` devient `debut_contrat` ;
- `application_deadline` devient `fin_candidature` ;
- `job_vacancy_date` devient `debut_vacance_poste` ;
- `archived_at` devient `date_archivage`.

`reference`, `source_id`, `mission`, `complements`, `localisation`, `conditions` et
`contacts` ne changent pas, ni leurs sous-champs, ni les valeurs renvoyées.

`POST /api/v1/offres/archiver` : le champ `status` de la réponse devient `statut`.
La valeur renvoyée (`ok`) ne change pas.

`POST /api/v1/offres/creer_modifier` : les champs de la réponse et les valeurs de
`offres[].statut` sont renommés en français.

- `created` devient `creees` ;
- `updated` devient `mises_a_jour` ;
- dans chaque élément de `offres`, la valeur de `statut` `created` devient `creee`
  et `updated` devient `mise_a_jour` ;
- dans chaque élément de `errors`, `offer` devient `offre`.

`offres` et ses sous-champs `index`, `reference` et `statut` gardent leur nom.
`errors` et `errors[].error` sont renommés plus bas, avec les autres champs d'erreur.

Pagination de `GET /api/v1/offres`, `GET /api/v1/offres/sources/{source_id}` et
`GET /api/v1/metiers` : les champs de l'enveloppe sont renommés en français.

- `count` devient `total` ;
- `next` devient `page_suivante` ;
- `previous` devient `page_precedente` ;
- `results` devient `resultats`.

Les paramètres `page` et `taille` ne changent pas.

Erreurs de toutes les routes `/api/v1/…` : une réponse d'erreur contient désormais
un champ `erreur`.

- `error` devient `erreur` ;
- `detail` devient `erreur` (authentification absente, source non autorisée,
  action interdite, offre introuvable, limite d'appels dépassée…) ;
- jeton JWT invalide ou expiré (`401`) : la réponse devient
  `{"erreur": "…", "code": "token_not_valid"}`, `detail` devient `erreur`, `code`
  ne change pas et `messages` est supprimé.

Les erreurs de validation des champs du corps de la requête (`400`) gardent leur
format, une liste de messages par nom de champ.

Listes d'erreurs des réponses de `POST /api/v1/offres/creer_modifier`,
`POST /api/v1/organismes/creer_modifier` et
`POST /api/v1/talentsoft_organisme/creer_modifier` :

- `errors` devient `erreurs` ;
- dans chaque élément de `erreurs`, `error` devient `erreur`.

Les autres champs propres à chaque route (`created`, `updated`, `validation_errors`…)
ne changent pas pour l'instant. Les routes `/api/token` et `/api/fake-ts/…` gardent
leur format d'erreur.

## 2026-10-08

### Ajouté

- `POST /api/v1/offres/creer_modifier` : le champ `publication.debut_vacance_poste`
  (date à partir de laquelle le poste est vacant) est désormais enregistré. Il était
  accepté jusqu'ici, mais ignoré.
- `GET /api/v1/offres/sources/{source_id}` : chaque offre renvoyée contient un nouveau
  champ `job_vacancy_date`, valeur de `publication.debut_vacance_poste` (date ISO
  8601), à `null` si l'information n'a pas été transmise.

### Modifié

- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `professionalCategory` n'est plus toujours `null`. C'est un objet codé qui reprend
  `vacance_poste` : `clientCode` vaut `STATUT01` (poste vacant) ou `STATUT02` (poste
  susceptible d'être vacant). Il reste à `null` si la vacance de poste n'est pas
  renseignée.

### Compatibilité

Ces changements sont rétrocompatibles : un appel valide avant ces changements reste
valide, et le champ ajouté dans les réponses n'en retire aucun. `professionalCategory`
passe d'une chaîne toujours `null` à un objet codé, comme dans l'API Talentsoft.

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
