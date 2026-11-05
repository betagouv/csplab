# Guide de l'API CSPLab — Version non technique

> Ce document explique, en langage accessible, ce que permet de faire l'API de CSPLab,
> à qui elle s'adresse, et **quelles sont les règles métier** à respecter sur chaque
> donnée envoyée ou reçue. Il est destiné aux personnes non techniques (métier,
> partenaires, gestion de projet) qui ont besoin de comprendre le fonctionnement de
> l'API sans lire de code.



## Sommaire

- [Qu'est-ce qu'une API, en deux phrases ?](#quest-ce-quune-api-en-deux-phrases)
- [À qui s'adresse cette API ?](#a-qui-sadresse-cette-api)
- [Comment fonctionne l'authentification ?](#comment-fonctionne-lauthentification)
  - [Obtenir un jeton — `POST /api/token/`](#obtenir-un-jeton-post-apitoken)
  - [Rafraîchir un jeton — `POST /api/token/refresh/`](#rafraichir-un-jeton-post-apitokenrefresh)
- [Limitations d'usage (quotas)](#limitations-dusage-quotas)
- [Les fonctionnalités de l'API](#les-fonctionnalites-de-lapi)
  - [1. Consulter les offres d'emploi — `GET /api/v1/offres/`](#1-consulter-les-offres-demploi-get-apiv1offres)
    - [Filtres disponibles](#filtres-disponibles)
  - [2. Consulter les offres d'une source — `GET /api/v1/offres/sources/{source_id}`](#2-consulter-les-offres-dune-source-get-apiv1offressourcessource_id)
  - [3. Archiver une offre — `POST /api/v1/offres/archiver`](#3-archiver-une-offre-post-apiv1offresarchiver)
  - [4. Créer ou modifier des offres — `POST /api/v1/offres/creer_modifier/`](#4-creer-ou-modifier-des-offres-post-apiv1offrescreer_modifier)
    - [Structure d'une offre et contraintes sur les champs](#structure-dune-offre-et-contraintes-sur-les-champs)
    - [En cas de problème](#en-cas-de-probleme)
  - [5. Consulter les métiers — `GET /api/v1/metiers/`](#5-consulter-les-metiers-get-apiv1metiers)
  - [6. Consulter les organismes — `GET /api/v1/organismes/`](#6-consulter-les-organismes-get-apiv1organismes)
  - [7. Importer des concours (fichier CSV) — `POST /api/v1/concours/upload/`](#7-importer-des-concours-fichier-csv-post-apiv1concoursupload)
    - [Format du fichier attendu](#format-du-fichier-attendu)
    - [Colonnes obligatoires](#colonnes-obligatoires)
    - [Comment se passe le traitement ?](#comment-se-passe-le-traitement)
    - [Réponses possibles](#reponses-possibles)
- [Annexe — Les codes de réponse, en clair](#annexe-les-codes-de-reponse-en-clair)
- [Annexe — Récapitulatif des listes de valeurs autorisées](#annexe-recapitulatif-des-listes-de-valeurs-autorisees)
  - [Domaine fonctionnel (référentiel RMFPv2)](#domaine-fonctionnel-referentiel-rmfpv2)
- [Annexe — Correspondance entre le format Talentsoft et l'API v1](#annexe-correspondance-entre-le-format-talentsoft-et-lapi-v1)
  - [Champs reliés](#champs-relies)
  - [Champs Talentsoft sans équivalent dans l'API v1](#champs-talentsoft-sans-equivalent-dans-lapi-v1)
  - [Autres champs de l'API v1](#autres-champs-de-lapi-v1)
- [Annexe — Passer de l'API vacancies de Talentsoft à l'API v1](#annexe-passer-de-lapi-vacancies-de-talentsoft-a-lapi-v1)
  - [Champs de l'offre vacancies](#champs-de-loffre-vacancies)
  - [Valeurs des listes Talentsoft](#valeurs-des-listes-talentsoft)
  - [Champs vacancies sans équivalent dans l'API v1](#champs-vacancies-sans-equivalent-dans-lapi-v1)
  - [Champs de l'API v1 absents de l'offre vacancies](#champs-de-lapi-v1-absents-de-loffre-vacancies)



## Qu'est-ce qu'une API, en deux phrases ?

Une API est une « porte d'entrée » automatisée qui permet à deux logiciels de
s'échanger des informations sans intervention humaine. Ici, l'API CSPLab permet à des
partenaires autorisés (par exemple des plateformes d'emploi public) de **transmettre
des offres d'emploi et des concours**, et de **consulter les offres, les métiers et les organismes**
de la Fonction Publique.



## À qui s'adresse cette API ?

L'API est **à l'usage exclusif des personnes et partenaires autorisés**. Chaque
utilisateur dispose de son propre moyen d'identification (voir « Authentification »
ci-dessous). Aucun accès n'est possible sans autorisation préalable.



## Comment fonctionne l'authentification ?

Avant d'utiliser l'API, l'appelant doit prouver son identité. Trois moyens existent :

| Moyen | Description | Où est-il utilisé ? |
|---|---|---|
| **Jeton JWT** (`jwtAuth`) | Un jeton temporaire obtenu en échange d'un identifiant + mot de passe. Il expire au bout d'un certain temps et doit être renouvelé. | Toutes les routes protégées |
| **Clé d'API** (`ApiKeyAuth`) | Une clé permanente fournie au partenaire, à placer dans l'en-tête sous la forme `Api-Key <clé>`. | Consultation, création/modification et archivage d'offres |
| **Cookie de session** (`cookieAuth`) | Utilisé lorsqu'on est connecté via le site web. | Consultation des métiers et import de concours |

> **Règle générale :** un jeton invalide ou expiré entraîne systématiquement un refus
> (`401 Non autorisé`).

### Obtenir un jeton — `POST /api/token/`

On envoie un **email** et un **mot de passe**, et on reçoit en retour deux jetons :

- un jeton d'**accès** (`access`) — sert à appeler les autres routes ;
- un jeton de **rafraîchissement** (`refresh`) — sert à obtenir un nouveau jeton
  d'accès quand le premier expire, sans avoir à ressaisir le mot de passe.

### Rafraîchir un jeton — `POST /api/token/refresh/`

On envoie le jeton de rafraîchissement et on reçoit un nouveau jeton d'accès.

### Restreindre un compte à des adresses IP

Sur demande, un compte peut être limité à une liste d'adresses IP ou de plages CIDR
(ex. `203.0.113.10`, `203.0.113.0/24`, `2001:db8::/48`). Cette restriction est
facultative : un compte sans plage reste utilisable depuis n'importe quelle adresse.

- Communiquez vos IP de sortie (production et recette) à la création du compte.
- Prévenez-nous **avant** d'en changer : depuis une autre adresse, l'obtention d'un
  jeton, son rafraîchissement et chaque appel avec un jeton déjà obtenu sont refusés
  (`401 Non autorisé`), avec le même message qu'un identifiant invalide.



## Limitations d'usage (quotas)

Pour préserver le service, le nombre d'appels est plafonné :

- **120 appels par minute et par utilisateur** sur les routes de consultation et
  d'ingestion d'offres et de métiers.
- **100 offres maximum par appel** lors d'une création/modification groupée d'offres.



# Les fonctionnalités de l'API

L'API est organisée en cinq grands domaines :

| Domaine | À quoi ça sert |
|---|---|
| **Authentification** (`token`) | Obtenir et renouveler les jetons d'accès |
| **Offres** (`offres`) | Consulter, créer/modifier et archiver des offres d'emploi |
| **Métiers** (`metiers`) | Consulter le référentiel des métiers de la Fonction Publique |
| **Organismes** (`organismes`) | Consulter le référentiel des organismes de la Fonction Publique |
| **Concours** (`concours`) | Importer des données de concours via un fichier CSV |



## 1. Consulter les offres d'emploi — `GET /api/v1/offres/`

Retourne la liste des offres d'emploi de la Fonction Publique, **paginée** (renvoyée
par lots plutôt qu'en une seule fois). La pagination se pilote avec les paramètres
`page` (numéro de page, défaut `1`) et `taille` (nombre d'éléments par page, défaut
`100`, maximum `1000`). Une `taille` supérieure à `1000` est ramenée à `1000` ; une
`taille` non numérique ou inférieure à `1` est remplacée par la valeur par défaut. Une
`page` non numérique, inférieure à `1` ou au-delà de la dernière page renvoie une
erreur `404`. Pour parcourir toutes les offres, suivez le lien `next` de chaque
réponse jusqu'à ce qu'il vaille `null`.

### Filtres disponibles

| Paramètre | Rôle | Format |
|---|---|---|
| `actif` | Ne retourner que les offres actives (`true`, valeur par défaut) ou archivées (`false`) | Booléen |
| `categorie` | Filtrer par catégorie(s) : une offre est retournée si l'une de ses catégories fait partie du filtre | Liste séparée par virgules parmi APLUS, A, B, C |
| `versant` | Filtrer par versant(s) | Liste séparée par virgules parmi FPT, FPE, FPH |
| `nature_offre` | Filtrer par nature(s) d'offre | Liste séparée par virgules parmi TITULAIRE_CONTRACTUEL, CONTRACTUEL, TERRITORIAL |
| `niveau_experience` | Filtrer par niveau(x) d'expérience | Liste séparée par virgules parmi DEBUTANT, CONFIRME, EXPERT |
| `lieu_de_travail` | Filtrer par mode de travail | Liste séparée par virgules parmi NON_DEFINI, SUR_SITE, TELETRAVAIL |
| `management` | Filtrer selon la présence de management | Liste séparée par virgules parmi SANS, AVEC |
| `region` | Filtrer par code(s) région officiel(s). Pour une offre à plusieurs lieux, ce filtre, comme `departement`, `pays`, `zone` et le filtre par rayon, retient l'offre si l'un de ses lieux correspond | Liste séparée par virgules (ex. `11,84`) |
| `departement` | Filtrer par code(s) département officiel(s) | Liste séparée par virgules (ex. `75,69`) |
| `pays` | Filtrer par code(s) pays alpha-3 | Liste séparée par virgules (ex. `FRA,BEL`) |
| `zone` | Filtrer par zone(s) géographique(s) | Liste séparée par virgules parmi AFRIQUE, EUROPE, ASIE, AMERIQUE, OCEANIE, ANTARTIQUE, MOYEN_ORIENT_AFRIQUE_DU_NORD |
| `domaine` | Filtrer par code(s) de domaine fonctionnel | Liste séparée par virgules (ex. `NUM,ACH`) |
| `organisation` | Filtrer par code d'organisme Talentsoft (`entityCode`), tous ses organismes descendants inclus | Répéter le paramètre pour en filtrer plusieurs (ex. `?organisation=ORG1&organisation=ORG2`) |
| `debut_publication` | Ne retourner que les offres publiées au cours des N derniers jours | Entier négatif (ex. `-7`) |
| `latitude`, `longitude`, `radius` | Filtre géographique par rayon autour d'un point — **les trois doivent être fournis ensemble** | `latitude`/`longitude` en degrés décimaux, `radius` en kilomètres (entier positif) |
| `mots_cles` | Recherche plein texte (en français) sur le titre, l'intitulé long, la mission, le profil, l'organisme, l'employeur et les compléments de l'offre | Texte libre |

> Les filtres à valeurs multiples acceptent une liste de valeurs séparées par une
> virgule. Une valeur invalide pour l'un de ces filtres renvoie une erreur `400`.

Chaque offre renvoyée contient notamment :

| Information | Signification | Peut être vide ? |
|---|---|---|
| `reference` | Référence d'origine de l'offre | Non |
| `source_id` | Identifiant de la source ayant transmis l'offre | Non |
| `titre` | Intitulé du poste | Non |
| `organisation` | Organisme employeur | Non |
| `nature_offre` | Nature de l'offre | Oui |
| `categories` | Catégories (A+, A, B, C…), dans l'ordre d'envoi | Non |
| `debut_publication` | Date de début de publication | Non |
| `url_offre` | Lien vers l'annonce | Oui |
| `date_archivage` | Date d'archivage de l'offre | Oui |

> **Règle métier clé :** une offre dont `date_archivage` est **vide** est **active** ;
> une offre dont `date_archivage` est **renseigné** est **archivée**.



## 2. Consulter les offres d'une source — `GET /api/v1/offres/sources/{source_id}`

Retourne, **paginée**, la liste complète des offres d'emploi rattachées à la source
identifiée par son identifiant unique (`source_id`, UUID). La pagination fonctionne
comme pour la liste principale des offres (paramètres `page` et `taille`).

> **Règle métier :** l'accès à une source non autorisée pour l'utilisateur authentifié
> renvoie une erreur `401`, même si la source existe.

Chaque offre renvoyée contient, en plus des informations de la liste principale
(voir section précédente), le détail complet de l'offre. Les champs reprennent les
noms utilisés par `POST /api/v1/offres/creer_modifier` (voir section 4) :
`employeur`, `profil`, `mission`, `complements`, `conditions_exercice` et
`descriptif_service` sont renvoyés tels qu'ils ont été transmis, en Markdown (voir
le bloc « Description » de la section 4).

| Champ | Signification | Peut être vide ? |
|---|---|---|
| `titre_long` | Intitulé long du poste | Oui |
| `employeur` | Présentation de l'employeur | Oui |
| `profil` | Profil recherché | Non |
| `mission` | Missions du poste | Non |
| `complements` | Informations complémentaires | Oui |
| `conditions_exercice` | Conditions particulières d'exercice | Oui |
| `descriptif_service` | Description du service | Oui |
| `versant` | Versant de la fonction publique | Oui |
| `type_contrat` | Type de contrat | Oui |
| `vacance_poste` | Vacance du poste | Oui |
| `url_candidature` | Lien pour candidater. Vide si `email_candidature` est renseigné. | Oui |
| `email_candidature` | Adresse email pour candidater. Vide si `url_candidature` est renseigné. | Oui |
| `localisation` | Liste des lieux de l'offre, dans l'ordre d'envoi, le premier étant le lieu principal (`zone_geographique`, `pays`, `region`, `departement`, `localisation_label`, `latitude`, `longitude`). Liste vide si l'offre n'est pas localisée | Oui |
| `criteres` | Critères de l'offre (diplôme, expérience, langues…) | Oui |
| `conditions` | Conditions de l'offre (rémunération, temps de travail…) | Oui |
| `contacts` | Contacts de l'offre (`role`, `texte`, `emails`), `principal` puis `autre` | Oui |
| `fin_publication` | Date de fin de publication | Oui |
| `debut_contrat` | Date de début du contrat | Oui |
| `fin_candidature` | Date limite de candidature | Oui |
| `debut_vacance_poste` | Date à partir de laquelle le poste est vacant | Oui |

**Réponses possibles :**

| Code | Signification |
|---|---|
| `200 OK` | La liste des offres de la source est renvoyée |
| `401` | Authentification absente/invalide, ou source non autorisée pour l'utilisateur |
| `500` | Erreur inattendue du serveur |



## 3. Archiver une offre — `POST /api/v1/offres/archiver`

Permet de retirer une offre de la liste des offres actives, en l'identifiant par sa
référence.

**Informations à fournir (les deux sont obligatoires) :**

| Champ | Signification | Format |
|---|---|---|
| `reference` | Référence de l'offre à archiver (ex. `2026-999999`) | Texte |
| `source_id` | Identifiant de la source ayant émis la demande | Identifiant unique (UUID) |

**Réponses possibles :**

| Code | Signification |
|---|---|
| `200 OK` | L'offre a bien été archivée |
| `400` | Champ manquant ou requête mal formée |
| `401` | Authentification absente ou invalide |
| `403` | Action interdite pour cet utilisateur |
| `404` | Aucune offre ne correspond à cette référence |

En cas de succès, la réponse contient un champ `statut` qui vaut `ok` :

```json
{"statut": "ok"}
```



## 4. Créer ou modifier des offres — `POST /api/v1/offres/creer_modifier/`

C'est la fonctionnalité la plus riche. Elle permet d'envoyer **entre 1 et 100 offres**
en un seul appel.

> **Règle métier centrale (« upsert ») :** chaque offre est identifiée par le couple
> **`identification.reference` + source**. Si une offre portant cette référence existe
> déjà, elle est **mise à jour** ; sinon, elle est **créée**.

La réponse indique combien d'offres ont été **créées**, **mises à jour**, et la liste
des offres **rejetées** avec le détail de l'erreur. Une offre rejetée n'empêche pas les
autres d'être traitées.

| Champ | Signification |
|---|---|
| `creees` | Nombre d'offres créées |
| `mises_a_jour` | Nombre d'offres mises à jour |
| `offres` | Offres créées ou mises à jour : `index` (position dans le tableau `offres` envoyé, à partir de 0), `reference` et `statut` (`creee` ou `mise_a_jour`) |
| `errors` | Offres rejetées : `index`, `offre` (bloc `identification` envoyé) et `error` (détail de l'erreur) |

Exemple de réponse :

```json
{
  "creees": 1,
  "mises_a_jour": 1,
  "offres": [
    {"index": 0, "reference": "REF-001", "statut": "mise_a_jour"},
    {"index": 2, "reference": "CSP-2026-000042", "statut": "creee"}
  ],
  "errors": [
    {
      "index": 1,
      "offre": {"reference": "auto", "versant": "FPE"},
      "error": {"titre": ["Ce champ ne peut être nul."]}
    }
  ]
}
```

> Vous partez d'une offre au format Talentsoft ? Consultez l'[annexe de correspondance
> entre le format Talentsoft et l'API v1](#annexe-correspondance-entre-le-format-talentsoft-et-lapi-v1).
> Vous publiez vos offres avec l'API Talentsoft `api/v1/vacancies/{vacancyReference}` ?
> Consultez l'[annexe de passage de l'API vacancies à l'API v1](#annexe-passer-de-lapi-vacancies-de-talentsoft-a-lapi-v1).

> **Consulter les offres transmises :** sur l'environnement de démonstration
> uniquement, les offres transmises peuvent être consultées dans l'interface « Fret » :
> [https://demo.csplab.beta.gouv.fr/fret](https://demo.csplab.beta.gouv.fr/fret).

### Structure d'une offre et contraintes sur les champs

Une offre est composée de plusieurs blocs. Voici le détail, avec les **contraintes de
longueur et de valeurs autorisées**.

#### Bloc « Identification » (`identification`) — obligatoire
| Champ | Règle |
|---|---|
| `reference` | Obligatoire. Référence de l'offre. |
| `versant` | Obligatoire. Valeurs autorisées : **FPT** (Territoriale), **FPE** (État), **FPH** (Hospitalière). |

#### Informations générales
| Champ | Règle |
|---|---|
| `titre` | Obligatoire. **150 caractères maximum.** |
| `titre_long` | Facultatif. Intitulé long, à ne renseigner que s'il diffère de `titre` : une offre dont le `titre_long` est identique à `titre` est rejetée. Peut être vide. **1 500 caractères maximum.** |
| `url_offre` | Lien web. Peut être vide. |
| `url_candidature` | Lien web pour candidater. Voir la règle ci-dessous. |
| `email_candidature` | Adresse email valide pour candidater. Voir la règle ci-dessous. |

> **Règle métier :** renseigner **soit** `url_candidature`, **soit**
> `email_candidature`, mais pas les deux. Une offre qui contient les deux, ou aucun
> des deux, est rejetée.

#### Bloc « Organisation » (`organisation`) — obligatoire
| Champ | Règle |
|---|---|
| `nom` | Obligatoire. Nom de l'organisme. Reprendre de préférence le `nom` renvoyé par [`GET /api/v1/organismes/`](#6-consulter-les-organismes-get-apiv1organismes). |
| `siret` | Obligatoire. **14 caractères maximum.** Le SIRET se retrouve avec [`GET /api/v1/organismes/`](#6-consulter-les-organismes-get-apiv1organismes), grâce aux filtres `nom` et `siret`. |

#### Bloc « Profession » (`profession`) — obligatoire
| Champ | Règle |
|---|---|
| `referentiel` | Référentiel utilisé. Valeur par défaut : **RMFPv2**. |
| `domaine` | Facultatif. Code du domaine fonctionnel. Absent, il est déduit du métier ; renseigné, il doit correspondre au `domaine_fonctionnel_code` du métier, sinon l'offre est rejetée. Obligatoire lorsque le code métier relève de plusieurs domaines (ex. `ERJUS008`, `ERTRA007`) : il doit alors être l'un d'eux. Vérifié uniquement si `referentiel=RMFPv2`. **3 caractères maximum.** |
| `metier` | Obligatoire. Code métier : valeur du champ `code_emploi_csp` d'un métier renvoyé par [`GET /api/v1/metiers/`](#5-consulter-les-metiers-get-apiv1metiers), par exemple `ERAMT001` (vérifié uniquement si `referentiel=RMFPv2`). **8 caractères maximum.** |
| `code_emploi_local` | Code emploi local propre au partenaire. Peut être vide. **50 caractères maximum.** |

#### Catégorie et contrat
| Champ | Règle |
|---|---|
| `categories` | Obligatoire. Liste d'au moins une valeur : une offre sans catégorie est rejetée. Valeurs autorisées : **APLUS, A, B, C, HORS_CATEGORIE**. Toutes les catégories sont enregistrées, dans l'ordre d'envoi (doublons retirés). |
| `nature_offre` | Obligatoire. Public visé par l'offre. Valeurs autorisées : **TITULAIRE_CONTRACTUEL, CONTRACTUEL, TERRITORIAL**. |
| `type_contrat` | Facultatif. Une seule valeur parmi **CDD, CDI, CDD_CDI, CONTRAT_PROJET, VACATION** (ou vide / `null` si l'offre n'est pas soumise à contractualisation). |
| `vacance_poste` | **OUI** = poste vacant ; **NON** = poste susceptible d'être vacant (ou vide). |

#### Bloc « Description » (`description`) — obligatoire
Les champs `mission`, `profil`, `employeur` et `complements` sont obligatoires, mais
peuvent être des textes vides.

Les six champs du bloc acceptent du **Markdown** ([CommonMark](https://commonmark.org/help/)),
pour conserver la mise en forme de l'offre : gras (`**texte**`), italique
(`*texte*`), listes (`- élément`, `1. élément`), titres (`## Titre`), liens
(`[libellé](https://…)`). Un texte brut reste valide, mais quelques caractères en
début de ligne ou autour d'un mot (`*`, `_`, `#`, `1.`) sont interprétés : précédez-les
d'une barre oblique inverse (`\*`) pour les garder tels quels. La limite de
caractères s'applique au texte Markdown, syntaxe comprise.

> **Règle métier :** une offre dont la description contient une balise HTML (`<b>`,
> `<!-- … -->`…) ou un lien autre que `http`, `https` ou `mailto` (`javascript:`,
> lien relatif…) est rejetée, avec un message qui cite l'élément refusé. Pour écrire
> le caractère `<` devant une lettre, précédez-le d'une barre oblique inverse (`\<`).
> Un `<` suivi d'une espace ou d'un chiffre (« salaire < 2000 € ») est accepté.

| Champ | Règle |
|---|---|
| `mission` | **10 000 caractères maximum.** |
| `profil` | **10 000 caractères maximum.** |
| `employeur` | Présentation de l'employeur. **3 000 caractères maximum.** |
| `complements` | **5 000 caractères maximum.** |
| `conditions_exercice` | Facultatif. Conditions particulières d'exercice. **10 000 caractères maximum.** |
| `descriptif_service` | Facultatif. Description du service qui recrute. **10 000 caractères maximum.** |

#### Bloc « Localisation » (`localisation`) — liste, peut être vide
Une offre peut se dérouler en plusieurs lieux : **50 lieux au plus**, tous conservés dans l'ordre d'envoi. Le premier est le lieu principal. Un même lieu ne peut figurer qu'une fois : deux lieux avec les mêmes `pays`, `region`, `departement` et `localisation_label` (quelles que soient leurs coordonnées) rejettent l'offre dans `errors`.

| Champ | Règle |
|---|---|
| `zone_geographique` | Obligatoire dans chaque localisation. Valeurs : **AF** (Afrique), **EU** (Europe), **AS** (Asie), **AM** (Amérique), **OC** (Océanie), **AN** (Antarctique), **MO** (Moyen-Orient et Afrique du Nord). |
| `pays` | Obligatoire. Code pays ISO 3166-1 alpha-3, **en majuscules** (ex. `FRA`). Un code en minuscules (`fra`) est rejeté. Pour `FRA`, `region` et `departement` sont obligatoires. Pour une offre à l'étranger (tout autre pays), ils valent `null` : la `zone_geographique` et le `localisation_label` situent l'offre. L'outre-mer est en `FRA`, avec son département : région `DOM` pour les départements d'outre-mer (Guadeloupe `971`, Martinique `972`, Guyane `973`, La Réunion `974`, Mayotte `976`), région `TOM` pour les collectivités d'outre-mer (Saint-Pierre-et-Miquelon `975`, Saint-Barthélemy `977`, Saint-Martin `978`, Wallis-et-Futuna `986`, Polynésie française `987`, Nouvelle-Calédonie `988`). Une offre dont le `pays` est le code ISO de l'un de ces territoires (`GLP`, `MTQ`, `GUF`, `REU`, `MYT`, `SPM`, `BLM`, `MAF`, `WLF`, `PYF`, `NCL`) est rejetée, avec un message qui donne la `region` et le `departement` attendus. `DOM` est le code de la République dominicaine, et `ATF` (Terres australes et antarctiques françaises), sans département, reste accepté comme pays. |
| `region` | Code région INSEE officiel, `DOM`, `TOM`, ou `null` hors de France. Si `departement` est renseigné, doit être la région de ce département : code INSEE de la région ou `DOM` pour `971` à `974` et `976`, `TOM` pour `975`, `977`, `978`, `986`, `987`, `988`, `SPM` et `WLF`. |
| `departement` | Code département officiel (`01` à `95`, `2A`, `2B`, DOM-TOM dont `977` Saint-Barthélemy et `978` Saint-Martin, `SPM`, `WLF`…), ou `null` hors de France. Doit appartenir à `region`. |
| `localisation_label` | Libellé du lieu. **500 caractères maximum.** |
| `latitude` / `longitude` | Coordonnées géographiques. Facultatives : peuvent être absentes ou `null`. |

#### Bloc « Critères » (`criteres`) — peut être vide
| Champ | Règle |
|---|---|
| `diplome_niveau` | Nombre entier **entre 1 et 8** (niveaux de diplôme). |
| `experience` | Valeurs : **DEBUTANT, CONFIRME, EXPERT**. |
| `specialisations` | Liste de textes. |
| `diplome` | Texte libre. Indiquez de préférence l'un des libellés du référentiel des diplômes d'État (liste ci-dessous), à l'identique. |
| `documents_requis` | Liste de documents à transmettre pour candidater. Valeurs : **CV, LETTRE_MOTIVATION, PORTFOLIO**. Chaque document ne peut être cité qu'une fois. |
| `competences_requises` | Texte libre en Markdown, **2 000 caractères maximum**. Peut être vide ou `null`. |
| `langues` | Liste de langues, chacune avec un **code ISO sur 2 caractères** et un **niveau** (**A1, A2, B1, B2, C1, C2**). |

Valeurs indicatives de `diplome`, libellés du référentiel des diplômes d'État (toute autre valeur reste acceptée) :

- `Diplôme d'Etat d'infirmier`
- `Diplôme d'Etat d'aide-soignant`
- `Diplôme d'Etat d'éducateur spécialisé`
- `Diplôme d'Etat français d'assistant de service social`
- `Diplôme d'Etat de masseur-kinésithérapeute`
- `Diplôme d'Etat d'aide médico psychologique`
- `Diplôme d'Etat d'ergothérapeute`
- `Diplôme d'Etat de moniteur éducateur`
- `Diplôme d'Etat d'infirmier en pratique avancée`
- `Diplôme d'Etat de psychomotricien`
- `Diplôme d'Etat d'auxiliaire de puériculture`
- `Diplôme d'Etat de sage-femme`
- `Diplôme d'Etat d'infirmier de bloc opératoire`
- `Diplôme d'Etat de la jeunesse, de l'éducation populaire et du sport`
- `Diplôme d'Etat d'éducateur de jeunes enfants`
- `Diplôme d'Etat de manipulateur d'électroradiologie médicale`
- `Diplôme d'Etat d'infirmier anesthésiste`
- `Diplôme d'Etat d'ambulancier`
- `Diplôme d'Etat de conseiller en économie sociale familiale`
- `Diplôme d'Etat de puéricultrice`
- `Diplôme d'Etat de technicien de laboratoire médical`
- `Diplôme d'Etat d'éducateur technique spécialisé`
- `Diplôme d'Etat de pédicure-podologue`
- `Diplôme d'Etat d'audioprothésiste`
- `Diplôme d'Etat français de diététicien`
- `Diplôme d'Etat d'audio-protésiste`

#### Bloc « Conditions » (`conditions`) — peut être vide
| Champ | Règle |
|---|---|
| `salaire_titulaire` | **100 caractères maximum.** |
| `salaire_contractuel` | **100 caractères maximum.** |
| `debut_contrat` / `fin_contrat` | Dates. Peuvent être vides. |
| `duree_contrat` | Texte. |
| `temps_travail` | Obligatoire. Valeurs : **NON_DEFINI, TEMPS_PLEIN, TEMPS_PARTIEL**. |
| `ouvert_aux_militaires` | **OUI** ou **NON**. |
| `lieu_de_travail` | Obligatoire. Valeurs : **NON_DEFINI, SUR_SITE, TELETRAVAIL**. |
| `management` | Facultatif. **AVEC** ou **SANS** management. |
| `bases_legales` | Texte libre en Markdown, **1 500 caractères maximum**. |
| `note_ouverture_poste_url` | Lien **`https`** vers l'avis de vacance publié au Journal officiel, sur **`legifrance.gouv.fr`** ou **`www.legifrance.gouv.fr`** (ex. `https://www.legifrance.gouv.fr/jorf/id/JORFTEXT…`). Une offre avec un lien `http` ou vers un autre site est rejetée. |

#### Bloc « Contacts » (`contacts`) — liste, peut être vide
Au plus un contact par rôle. Les contacts sont renvoyés dans l'ordre `principal` puis `autre`.

| Champ | Règle |
|---|---|
| `role` | Obligatoire. Valeurs : **principal** (personne à contacter), **autre** (autre personne à contacter). |
| `texte` | Obligatoire. Contact en texte libre (nom, fonction, e-mail, téléphone…). **100 caractères maximum**, au moins une lettre ou un chiffre. Les espaces en début et fin sont retirés. |
| `emails` | Obligatoire, peut être vide. Liste d'**adresses email valides** présentes dans `texte`, dans l'ordre d'apparition. Les doublons sont retirés. |

Exemple :

```json
"contacts": [
  {
    "role": "principal",
    "texte": "Camille Martin, cheffe du bureau RH : camille.martin@exemple.gouv.fr",
    "emails": ["camille.martin@exemple.gouv.fr"]
  },
  {
    "role": "autre",
    "texte": "recrutement@exemple.gouv.fr",
    "emails": ["recrutement@exemple.gouv.fr"]
  }
]
```

#### Bloc « Publication » (`publication`) — obligatoire
| Champ | Règle |
|---|---|
| `debut_publication` | Obligatoire. Date. |
| `fin_publication` | Obligatoire. Date. |
| `fin_candidature` | Date limite de candidature. Peut être vide. |
| `debut_vacance_poste` | Date à partir de laquelle le poste est vacant. Peut être vide. |

### En cas de problème
| Code | Signification |
|---|---|
| `201` | Traitement effectué (voir le détail créées / mises à jour / rejetées) |
| `400` | Requête globalement invalide |
| `401` | Authentification absente ou invalide |
| `403` | Action interdite pour cet utilisateur |
| `500` | Erreur inattendue du serveur |



## 5. Consulter les métiers — `GET /api/v1/metiers/`

Retourne la liste **paginée** des métiers de la Fonction Publique (paramètres `page`
et `taille`, mêmes règles que pour la liste des offres). On peut filtrer par
**code de domaine fonctionnel** grâce au paramètre `domaine`.

> **Contrainte du filtre `domaine` :** texte de **1 à 3 caractères** (ex. `AMT`, `AGR`).

Chaque métier renvoyé contient :

| Information | Signification |
|---|---|
| `libelle` | Intitulé du métier |
| `description` | Description du métier |
| `domaine_fonctionnel_code` | Code du domaine fonctionnel |
| `versants` | Versants concernés (FPE, FPT, FPH) |
| `activites` | Liste des activités (peut être vide) |
| `conditions_particulieres` | Conditions particulières (peut être vide) |
| `code_emploi_csp` | Code CSP du RMFP, à renseigner dans `profession.metier` lors de l'envoi d'une offre. Plusieurs métiers peuvent partager le même code. Toujours renseigné. |



## 6. Consulter les organismes — `GET /api/v1/organismes/`

Retourne la liste **paginée** des organismes du référentiel CSPLab, alimenté par les
référentiels FINESS, GIPCDG et DILA (paramètres `page` et `taille`). Les organismes
supprimés ne sont pas renvoyés. La liste est triée par nom, puis par identifiant :
l'ordre ne change pas d'un appel à l'autre.

Cette route n'est accessible qu'avec un **jeton** (voir « Authentification »).

> **Page hors limites :** contrairement à la liste des métiers, une page au-delà de la
> dernière renvoie une erreur `404`.

Les valeurs `nom` et `siret` d'un organisme sont celles à reprendre dans le bloc
`organisation` d'une offre envoyée avec `POST /api/v1/offres/creer_modifier/`.

### Filtres disponibles

| Filtre | Effet | Contrainte |
|---|---|---|
| `versant` | Filtrer par versant | `FPE`, `FPT` ou `FPH`. Plusieurs valeurs séparées par une virgule (ex. `FPE,FPT`) |
| `siret` | Retrouver un organisme par son SIRET, par exemple pour vérifier un SIRET avant d'envoyer une offre | Exactement **14 caractères** |
| `nom` | Rechercher un organisme par une partie de son nom, sans tenir compte des majuscules ni des accents (`hopital` trouve « Hôpital ») | 255 caractères maximum |
| `departement` | Filtrer par département de l'organisme | Code de département (ex. `75`, `2A`, `971`) |
| `referentiel` | Filtrer par référentiel source | `FINESS`, `GIPCDG` ou `DILA` |

Un filtre invalide (par exemple un versant inconnu) renvoie une erreur `400`.

### Informations renvoyées

| Information | Signification |
|---|---|
| `id` | Identifiant de l'organisme dans CSPLab |
| `nom` | Nom de référence de l'organisme, à reprendre dans `organisation.nom` d'une offre |
| `versant` | `FPE`, `FPT` ou `FPH` |
| `siret` | SIRET de l'organisme, à renseigner dans `organisation.siret` d'une offre |
| `parent_id` | Identifiant de l'organisme parent, ou vide |
| `referentiel` | Référentiel source : `FINESS`, `GIPCDG` ou `DILA`. Avec `external_id`, c'est la clé utilisée pour créer, mettre à jour ou supprimer un organisme |
| `external_id` | Identifiant de l'organisme dans le référentiel source |
| `millesime` | Version du référentiel source dont provient l'organisme (peut être vide) |
| `localisation` | Vide, ou `zone_geographique`, `pays`, `region` et `departement` de l'organisme. `region` et `departement` valent `null` hors de France |



## 7. Importer des concours (fichier CSV) — `POST /api/v1/concours/upload/`

Permet d'importer en masse des données de concours **GRECO** via un fichier CSV.

### Format du fichier attendu
- **Encodage :** UTF-8
- **Séparateur :** point-virgule (`;`)

### Colonnes obligatoires
| Colonne | Rôle |
|---|---|
| `N° NOR` | **Identifiant unique de l'arrêté** — sert de clé : une ligne avec un NOR déjà connu **met à jour**, un NOR inconnu **crée**. |
| `Corps` | Obligatoire |
| `Grade` | Obligatoire |
| `Ministère` | Obligatoire |

### Comment se passe le traitement ?
- Chaque ligne est **validée individuellement**.
- Les lignes **valides** sont créées ou mises à jour.
- Les lignes **invalides** sont **ignorées** mais listées dans `validation_errors`
  (avec le numéro de ligne et le motif), afin de pouvoir les corriger.

> **Règle métier importante :** un import peut être **partiellement réussi**. Si
> certaines lignes sont invalides, les lignes valides sont **quand même enregistrées**.
> L'import n'échoue (`400`) que si **aucune** ligne n'est valide, ou si le fichier est
> absent, n'est pas un `.csv`, ou est mal formé.

### Réponses possibles
| Code | Signification |
|---|---|
| `201` | Au moins une ligne valide a été traitée (voir le détail créées / mises à jour / erreurs) |
| `400` | Fichier absent, mauvais format, ou aucune ligne valide |
| `401` | Authentification absente ou invalide |
| `500` | Erreur inattendue du serveur |

La réponse de succès détaille : nombre total de lignes, lignes valides, lignes
invalides, lignes créées, lignes mises à jour, et la liste éventuelle des erreurs.



# Annexe — Les codes de réponse, en clair

| Code | Famille | Signification générale |
|---|---|---|
| `200` / `201` | Succès | La demande a été traitée |
| `400` | Erreur de la demande | Données envoyées invalides ou incomplètes |
| `401` | Authentification | Identité non prouvée (jeton manquant/expiré) |
| `403` | Autorisation | Identité prouvée, mais action non permise |
| `404` | Introuvable | L'élément demandé n'existe pas |
| `500` | Erreur serveur | Problème inattendu côté CSPLab |



# Annexe — Récapitulatif des listes de valeurs autorisées

| Notion | Valeurs possibles |
|---|---|
| **Versant** | FPT (Territoriale), FPE (État), FPH (Hospitalière) |
| **Catégorie** | APLUS, A, B, C, HORS_CATEGORIE |
| **Nature de l'offre** | TITULAIRE_CONTRACTUEL, CONTRACTUEL, TERRITORIAL |
| **Type de contrat** | CDD, CDI, CDD_CDI (CDD ou CDI), CONTRAT_PROJET (contrat de projet), VACATION (payés à l'acte) |
| **Vacance de poste** | OUI (vacant), NON (susceptible d'être vacant) |
| **Expérience** | DEBUTANT, CONFIRME, EXPERT |
| **Documents requis** | CV, LETTRE_MOTIVATION (lettre de motivation), PORTFOLIO |
| **Niveau de langue** | A1, A2, B1, B2, C1, C2 |
| **Temps de travail** | NON_DEFINI, TEMPS_PLEIN, TEMPS_PARTIEL |
| **Lieu de travail** | NON_DEFINI, SUR_SITE, TELETRAVAIL |
| **Management** | AVEC, SANS |
| **Ouvert aux militaires** | OUI, NON |
| **Zone géographique** | AF, EU, AS, AM, OC, AN |
| **Niveau de diplôme** | Entier de 1 à 8 |
| **Domaine fonctionnel** | Voir tableau ci-dessous |

### Domaine fonctionnel (référentiel RMFPv2)

Utilisé dans le bloc `profession.domaine` (création/modification d'offres) et dans le
filtre `domaine` des routes de consultation des offres et des métiers.

| Code | Libellé |
|---|---|
| `ACH` | Achat |
| `AGR` | Agriculture |
| `AMT` | Aménagement et développement durable du territoire |
| `ASP` | Animation, jeunesse et sports |
| `BAT` | Bâtiment |
| `COM` | Communication |
| `CTL` | Organisation, contrôle et évaluation |
| `CUL` | Culture et Patrimoine |
| `DEF` | Défense |
| `DIR` | Direction et pilotage des politiques publiques |
| `DOC` | Lecture publique et Documentation |
| `ENS` | Enseignement et Formation |
| `ENV` | Environnement |
| `FIP` | Finances publiques |
| `GBF` | Gestion budgétaire et financière |
| `GRH` | Ressources humaines |
| `INT` | International |
| `JUR` | Affaires juridiques |
| `JUS` | Justice |
| `LOG` | Interventions techniques et logistiques |
| `MED` | Médical et paramédical |
| `NUM` | Numérique |
| `RCH` | Recherche |
| `REN` | Renseignement |
| `SAN` | Prévention, conseil et pilotage en santé |
| `SEC` | Sécurité |
| `SOC` | Social, enfance et famille |
| `TRA` | Transports |
| `USA` | Relation à l'usager |



# Annexe — Correspondance entre le format Talentsoft et l'API v1

Cette annexe est destinée aux intégrateurs qui alimentent l'API à partir d'offres au format Talentsoft. Elle indique, pour chaque champ d'une offre Talentsoft, le champ correspondant de l'offre envoyée à `POST /api/v1/offres/creer_modifier/` (« Offer API v1 »), ainsi que les champs sans équivalent des deux côtés. Les champs de l'API v1 lus dans des champs personnalisés (`customFields`) ou jamais renseignés par l'ingestion sont décrits dans la dernière section. Les notes « API fake-ts » décrivent les offres renvoyées par l'API fake-ts (`/api/fake-ts/`), qui expose les offres de CSPLab au format Talentsoft.

Notation : `a.b` désigne un objet imbriqué, `a[]` une liste, `a[0]` son premier élément. Tout objet codé (`contractType`, `offerFamilyCategory`, `professionalCategory`, `educationLevel`, `diploma`, `experienceLevel`, `country`, `region`, `department`, `specialisations[]`, `languages[].languageName|languageLevel`) est lu par son `clientCode`, sauf `diploma` lu par son `label` ; ses autres clés (`code`, `label`, `active`, `parentCode`, `type`, `parentType`, `hasChildren`) sont ignorées.

### Champs reliés

| Offre Talentsoft | Offer API v1 | Note |
|---|---|---|
| `reference` | `identification.reference` | |
| `salaryRange.clientCode` | `identification.versant` | Les valeurs contenant `FPT`/`FPH`/`FPE` donnent un `Verse` ; sans `salaryRange`, le versant est déduit de `reference` (`APHP`/`MENJ`/`OFII`). API fake-ts : objet codé, `clientCode` = `identification.versant` (`FPE`, `FPT`, `FPH`), `label` = son libellé (« Fonction publique de l'État »…). |
| `title` | `titre` | |
| `organisationName` | `organisation.nom` | |
| `organisation.entityCode` | `organisation.talentsoft_organisme_entity_code` | Réservé au service ingestion de CSPLab : laissez ce champ vide, une offre qui le renseigne est rejetée. API fake-ts : reprend l'organisme Talentsoft lié à l'offre. Toute offre est liée à un organisme Talentsoft. |
| `contractType.clientCode` | `nature_offre` | Traduit par le transcodeur de la source. |
| `professionalCategory.clientCode` | `vacance_poste` | `STATUT01` → `OUI` (poste vacant), `STATUT02` → `NON` (poste susceptible d'être vacant), sinon vide. Malgré son nom, c'est le « Statut du poste » affiché par l'ancien site WordPress. API fake-ts : `OUI` → `STATUT01`, `NON` → `STATUT02`, sinon `null`. |
| `offerFamilyCategory.clientCode` | `profession.metier` | `profession.domaine` n'est envoyé que pour les métiers relevant de plusieurs domaines (`ERJUS008`, `ERTRA007`) : il reprend alors les caractères 3 à 5 du code (`JUS`, `TRA`). Sinon, il est déduit du métier. API fake-ts : renvoie la catégorie principale de l'offre, pas le métier. |
| `description1Formatted` | `description.mission` | Converti du HTML en Markdown, repli sur le texte brut `description1` s'il est vide. API fake-ts : `description1` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `description2Formatted` | `description.profil` | Converti du HTML en Markdown, repli sur le texte brut `description2` s'il est vide. API fake-ts : `description2` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.description.longText1Formatted` | `description.employeur` | Converti du HTML en Markdown, repli sur le texte brut `customFields.description.longText1` s'il est vide. API fake-ts : `customFields.description.longText1` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.description.longText2Formatted` | `description.conditions_exercice` | Converti du HTML en Markdown, repli sur le texte brut `customFields.description.longText2` s'il est vide. API fake-ts : `customFields.description.longText2` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.description.longText3Formatted` | `description.descriptif_service` | Converti du HTML en Markdown, repli sur le texte brut `customFields.description.longText3` s'il est vide. API fake-ts : `customFields.description.longText3` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.offerCustomBlock1.longText1Formatted` | `description.complements` | Converti du HTML en Markdown, repli sur le texte brut `customFields.offerCustomBlock1.longText1` s'il est vide. API fake-ts : `customFields.offerCustomBlock1.longText1` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.applicantCriteria.longText1Formatted` | `criteres.competences_requises` | « Compétences attendues ». Converti du HTML en Markdown, repli sur le texte brut `customFields.applicantCriteria.longText1` s'il est vide ; sans les espaces en début et fin, non envoyé s'il est vide. API fake-ts : `customFields.applicantCriteria.longText1` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `customFields.offerCustomBlock1.longText2Formatted` | `conditions.bases_legales` | « Fondement juridique ». Converti du HTML en Markdown, repli sur le texte brut `customFields.offerCustomBlock1.longText2` s'il est vide ; sans les espaces en début et fin, non envoyé s'il est vide. API fake-ts : `customFields.offerCustomBlock1.longText2` contient le Markdown, la variante `Formatted` le HTML (titres rendus en paragraphes en gras), `null` si le champ est vide. |
| `offerUrl` | `url_offre` | |
| `urlRedirectionApplicant` | `url_candidature` | Prioritaire sur `customFields.origin.shortText1` et `applicationUrl`. |
| `customFields.origin.shortText1` | `email_candidature` | Texte libre (« adresse de candidature »). Lu seulement si `urlRedirectionApplicant` est vide : le premier e-mail valide trouvé devient `email_candidature`, et `url_candidature` reste vide. API fake-ts : reprend `email_candidature`, `null` si l'offre se candidate par lien. |
| `applicationUrl` | `url_candidature` | Dernier recours, si `urlRedirectionApplicant` est vide et que `customFields.origin.shortText1` ne contient aucun e-mail valide. Toujours rempli dans Talentsoft (page de candidature générique). API fake-ts : reprend `url_candidature`, `null` si l'offre se candidate par e-mail. |
| `geographicalLocation[0].clientCode` | `localisation[0].zone_geographique` | En France, ignoré : la zone est déduite du département, car Talentsoft range presque tout l'outre-mer en `Europe`. `EUROPE` en métropole, `AMERIQUE` (971, 972, 973) ou `AFRIQUE` (974, 976) pour les DOM, `AMERIQUE` (975, 977, 978, `SPM`) ou `OCEANIE` (986, `WLF`, 987, 988) pour les collectivités d'outre-mer. À l'étranger, lu : `_TS_CO_GeographicalArea_Europe` → `EU`, `_TS_CO_GeographicalArea_MoyenOrientAfriqueduNord` → `MO`, `_TS_CO_GeographicalArea_AmriquesCaraibe` → `AM`, `_TS_CO_GeographicalArea_Ocanie` → `OC`, `_TS_CO_GeographicalArea_Asie` → `AS`, `_TS_CO_GeographicalArea_Afrique` → `AF`. Toute la `localisation` est abandonnée si le pays manque, si, en France, la région manque, si elle est inconnue et que le département n'est pas en outre-mer (sinon, la région est déduite du département), si le département manque et que la région est `DOM` ou `TOM`, ou si le département est inconnu, ou si, à l'étranger, la zone est absente ou inconnue (« Monde »). Talentsoft n'envoie qu'un lieu en pratique (aucune offre à plusieurs lieux au 02/11/2026) : les éléments suivants de la liste sont ignorés, mais signalés dans Sentry. API fake-ts : un élément par zone distincte parmi les lieux de l'offre, `clientCode` étant le nom de la zone, comme dans le filtre `area` et `referentials/area` (`EUROPE` pour `EU`, `AFRIQUE` pour `AF`…), et `code` restant `null`. |
| `country[0].clientCode` | `localisation[0].pays` | Un territoire d'outre-mer saisi comme un pays, sans région ni département, est ramené à `FRA` et à son département : `GLP` → `971`, `MTQ` → `972`, `GUF` → `973`, `REU` → `974`, `SPM` → `975`, `MYT` → `976`, `BLM` → `977`, `MAF` → `978`, `WLF` → `WLF`, `PYF` → `987`, `NCL` → `988`. Tout autre pays que `FRA` est une offre à l'étranger. Talentsoft n'envoie qu'un lieu en pratique (aucune offre à plusieurs lieux au 02/11/2026) : les éléments suivants de la liste sont ignorés, mais signalés dans Sentry. |
| `region[0].clientCode` | `localisation[0].region` | Les préfixes `_TS_CO_Region_` et `R` sont retirés pour obtenir le code INSEE. Ignoré pour l'outre-mer : `DOM` pour les départements 971 à 974 et 976, `TOM` pour 975, 977, 978, 986, 987, 988, `SPM` et `WLF`. Ignoré à l'étranger : `region` à `null`. Talentsoft n'envoie qu'un lieu en pratique (aucune offre à plusieurs lieux au 02/11/2026) : les éléments suivants de la liste sont ignorés, mais signalés dans Sentry. |
| `department[0].clientCode` | `localisation[0].departement` | Cas particuliers de la Nouvelle-Calédonie (`988`), et de Saint-Barthélemy (`977`) et Saint-Martin (`978`), saisis avec un identifiant interne de l'instance Talentsoft. En France, si le département manque, le département chef-lieu de la région est retenu (75, 45, 21, 76, 59, 67, 44, 35, 33, 31, 69, 13, 2A, et le département unique des régions d'outre-mer). Ignoré à l'étranger : `departement` à `null`. Talentsoft n'envoie qu'un lieu en pratique (aucune offre à plusieurs lieux au 02/11/2026) : les éléments suivants de la liste sont ignorés, mais signalés dans Sentry. |
| `geolocation.latitude` | `localisation[0].latitude` | Repli sur `latitude`, puis, en France seulement, sur `organisation.geolocation.latitude` (à l'étranger, c'est en général le siège en France). |
| `geolocation.longitude` | `localisation[0].longitude` | Repli sur `longitude`, puis, en France seulement, sur `organisation.geolocation.longitude`. |
| `customFields.location.shortText1` | `localisation[0].localisation_label` | |
| `startPublicationDate` | `publication.debut_publication` | |
| `endPublicationDate` | `publication.fin_publication` | Repli sur `beginningDate`, puis sur `debut_publication` + 365 jours. API fake-ts : reprend `fin_publication`, `null` pour les offres reçues avant son enregistrement. |
| `customFields.offer.date1` | `publication.fin_candidature` | |
| `beginningDate` | `conditions.debut_contrat` | Sert aussi de repli pour `fin_publication`. |
| `beginningDate` | `publication.debut_vacance_poste` | Comme l'ancien site WordPress (« Vacant à partir du … », « Poste à pourvoir le … »). |
| `contractDuration` | `conditions.duree_contrat` | |
| `educationLevel.clientCode` | `criteres.diplome_niveau` | Lettres `A`-`H` ou `NIV_DIPL<n>` converties en niveau. |
| `diploma.label` | `criteres.diplome` | Libellé reçu, comme pour le diplôme d'État. Prioritaire sur `customFields.offerCustomBlock1.customCodeTable3` ; en pratique, Talentsoft ne renseigne jamais `diploma`. API fake-ts : toujours `null`, comme dans Talentsoft ; le diplôme est renvoyé dans `customFields.offerCustomBlock1.customCodeTable3`. |
| `customFields.offerCustomBlock1.customCodeTable3.label` | `criteres.diplome` | « Diplômes d'Etat requis », référentiel Talentsoft « Diplômes d'Etat » (`type`) de 26 codes, ex. `CSPU0002` « Diplôme d'Etat d'infirmier ». `criteres.diplome` reprend le libellé du référentiel pour un `clientCode` connu, sinon le `label` reçu. Utilisé seulement si `diploma` est absent. Une valeur du référentiel « Quotité de temps de travail » (`type`, codes `Temps_plein`, `Temps_noncomplet`) saisie par erreur est rejetée (passée à `null`, l'offre reste ingérée) et signalée dans Sentry ; elle n'est pas reprise dans `conditions.temps_travail`. API fake-ts : objet codé de type « Diplômes d'Etat », `label` = `criteres.diplome`, `clientCode` = son code Talentsoft retrouvé par le libellé, ou chaîne vide si `criteres.diplome` n'est pas l'un des 26 libellés du référentiel (texte libre d'un autre intégrateur, par exemple) ; `null` si `criteres.diplome` est vide. |
| `experienceLevel.clientCode` | `criteres.experience` | Converti en nom d'`ExperienceLevel`. |
| `specialisations[].clientCode` | `criteres.specialisations` | Remplacé par le libellé de la spécialisation. |
| `languages[].languageName.clientCode` | `criteres.langues[].iso_code` | |
| `languages[].languageLevel.clientCode` | `criteres.langues[].niveau` | |

`criteres` n'est envoyé que si au moins un des champs niveau de diplôme, diplôme, expérience, spécialisations, langues, compétences requises ou documents requis est renseigné.

**Offre à plusieurs lieux (API fake-ts).** `geographicalLocation`, `country`, `region` et `department` contiennent un élément par valeur distincte parmi tous les lieux de l'offre, dans l'ordre des lieux. `location`, `latitude`, `longitude`, `geolocation` et `customFields.location.shortText1` reprennent le lieu principal (le premier). `locations` reste `[]`.

### Champs Talentsoft sans équivalent dans l'API v1

| Offre Talentsoft | Note |
|---|---|
| `isTopOffer` | Toujours `false` dans l'API fake-ts. |
| `location` | Libellé d'affichage ; le libellé repris vient de `customFields.location.shortText1`. |
| `modificationDate` | |
| `contractTypeCountry` | |
| `organisationDescription` | Capturé nulle part dans la chaîne. API fake-ts : reprend la description de l'organisme Talentsoft lié à l'offre (comme `organisation.description`). |
| `organisationLogoUrl` | |
| `_links` | Métadonnées de transport. |
| `_format` | Métadonnées de transport. |
| `_metadata` | Métadonnées de transport. |
| `urlRedirectionEmployee` | |
| `locations` | Non lu : la localisation vient de `country`, `region` et `department`. Toujours vide en pratique dans les offres Talentsoft (au 02/11/2026) : s'il est rempli, l'offre est signalée dans Sentry. API fake-ts : toujours `[]`. |
| `isAnonymousOrganisation` | |
| `offerTime` | Non lu : `conditions.temps_travail` vient de `customFields.description.customCodeTable3`. |
| `numberOfVacancies` | Nombre de postes à pourvoir. Toujours `null` en pratique dans les offres Talentsoft. |
| `organisation.name` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.description` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.url` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.phoneNumber` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.postCode` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.parentName` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.logoUrl` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.maxDelayForConsent` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.retentionPeriod` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.generalConditions` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `organisation.personalDataConsent` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `operationalManager` | Non lu : `contacts` vient de `customFields.origin` (voir plus bas). |
| `applicationQuestions` | |
| `attachedFilesUrls` | |
| `skillCollection[]` | Non lu : `criteres.competences_requises` vient de `customFields.applicantCriteria.longText1Formatted` (voir « Champs reliés »). Toujours vide en pratique dans les offres Talentsoft. |
| `customFields.offer.shortText1` | |
| `customFields.offer.longText1` | |
| `customFields.offer.longText2` | |
| `customFields.offer.longText3` | |
| `customFields.description.date1` | |
| `customFields.description.shortText1` | |
| `customFields.location.date1` | |
| `customFields.location.longText1` | |
| `customFields.location.longText2` | |
| `customFields.location.longText3` | |
| `customFields.offerCustomBlock1.date1` | |
| `customFields.offerCustomBlock1.shortText1` | |
| `customFields.offerCustomBlock1.longText3Formatted` | Non lu : seul le texte brut `customFields.offerCustomBlock1.longText3` est repris. API fake-ts : `conditions.note_ouverture_poste_url` en HTML. |
| `code` | Clé de tout objet codé : seul `clientCode` est lu. |
| `label` | Clé de tout objet codé : seul `clientCode` est lu. |
| `active` | Clé de tout objet codé : seul `clientCode` est lu. |
| `parentCode` | Clé de tout objet codé : seul `clientCode` est lu. |
| `type` | Clé de tout objet codé : seul `clientCode` est lu. |
| `parentType` | Clé de tout objet codé : seul `clientCode` est lu. |
| `hasChildren` | Clé de tout objet codé : seul `clientCode` est lu. |

### Autres champs de l'API v1

| Offer API v1 | Note |
|---|---|
| `categories` | Lu par l'ingestion dans `customFields.description.customCodeTable1` (`CAT-A`/`B`/`C` ; `CAT-AEF`/`ESD`/`ES` → `APLUS`). API fake-ts : `customFields.description.customCodeTable1` contient la première catégorie (`clientCode` = `APLUS`, `A`, `B`, `C` ou `HORS_CATEGORIE`, `label` = son libellé, ex. « Catégorie A (cadre) »), `null` sans catégorie ; le filtre `category` de `offer_summaries` retourne une offre si l'une de ses catégories en fait partie. |
| `type_contrat` | Lu dans `customFields.offer.customCodeTable2` : `CDD*`, `CDI`. API fake-ts : `clientCode` = `type_contrat` (`CDD`, `CDI`, `CDD_CDI`, `CONTRAT_PROJET`, `VACATION`), `label` = son libellé, `null` sans type de contrat. |
| `titre_long` | Jamais renseigné par l'ingestion : Talentsoft n'a pas de titre long. |
| `organisation.siret` | Jamais renseigné par l'ingestion (vide) ; le rapprochement d'organisme passe par `talentsoft_organisme_entity_code`. |
| `profession.referentiel` | Constante `RMFPv2`. |
| `profession.code_emploi_local` | Jamais renseigné, `local_job_code` reste à `null`. |
| `criteres.documents_requis` | Lu dans `customFields.applicantCriteria.customCodeTable1` (« Documents à transmettre ») : `Doc_CV` → `[CV]`, `Doc_CV_LM` → `[CV, LETTRE_MOTIVATION]`, `Doc_CV_PF` → `[CV, PORTFOLIO]`, `Doc_CV_LM_PF` → `[CV, LETTRE_MOTIVATION, PORTFOLIO]`. Absent, `null` ou code inconnu → non envoyé. API fake-ts : renvoyé dans `customFields.applicantCriteria.customCodeTable1`, valeur du référentiel Talentsoft « Documents à transmettre » : `[CV]` → `Doc_CV`, `[CV, LETTRE_MOTIVATION]` → `Doc_CV_LM`, `[CV, PORTFOLIO]` → `Doc_CV_PF`, `[CV, LETTRE_MOTIVATION, PORTFOLIO]` → `Doc_CV_LM_PF`, quel que soit l'ordre. `null` pour une liste vide ou une autre combinaison. Le `label` reprend le libellé Talentsoft, que le WordPress BIEP affiche après « Pour postuler à cette offre, ». |
| `conditions.temps_travail` | Lu dans `customFields.description.customCodeTable3` (« Temps plein » oui/non) : `reponse_oui` → `TEMPS_PLEIN`, `reponse_non` → `TEMPS_PARTIEL`, sinon `NON_DEFINI`. API fake-ts : `clientCode` = `TEMPS_PLEIN` ou `TEMPS_PARTIEL`, `label` = son libellé, `null` pour `NON_DEFINI`. `customFields.offerCustomBlock1.customCodeTable3` est le diplôme d'État exigé, repris dans `criteres.diplome`. |
| `conditions.lieu_de_travail` | Lu dans `customFields.offerCustomBlock1.customCodeTable2` : `reponse_oui` → `TELETRAVAIL`, `reponse_non` → `SUR_SITE`, sinon `NON_DEFINI`. API fake-ts : `clientCode` = `TELETRAVAIL` ou `SUR_SITE`, `label` = son libellé, `null` pour `NON_DEFINI`. |
| `conditions.management` | Lu dans `customFields.offerCustomBlock1.customCodeTable1` : `reponse_oui` → `AVEC`, `reponse_non` → `SANS`. API fake-ts : `clientCode` = `AVEC` ou `SANS`, `label` = son libellé, `null` si absent. |
| `conditions.salaire_titulaire` | Jamais renseigné par l'ingestion. |
| `conditions.salaire_contractuel` | Jamais renseigné par l'ingestion. |
| `conditions.fin_contrat` | Jamais renseigné par l'ingestion. |
| `conditions.ouvert_aux_militaires` | Jamais renseigné par l'ingestion. |
| `conditions.note_ouverture_poste_url` | Lu dans `customFields.offerCustomBlock1.longText3` (« Avis de vacance au JO ») : premier lien `legifrance.gouv.fr` présent dans le texte, passé en `https`. `null` si le texte ne contient aucun lien Legifrance (les liens vers une page de candidature sont ignorés). API fake-ts : `longText3` contient le lien, `longText3Formatted` le même texte en HTML. |
| `contacts` | Lu dans `customFields.origin.shortText2` et `customFields.origin.shortText3` : `shortText2` (« Personnes à contacter ») → contact `principal`, `shortText3` (« Autre personne à contacter ») → contact `autre`. `texte` reprend la valeur sans les espaces en début et fin ; une valeur sans lettre ni chiffre est ignorée. `emails` contient les adresses email présentes dans le texte, dédoublonnées, dans l'ordre d'apparition. `null` si aucun contact. API fake-ts : `shortText2` = `texte` du contact `principal`, `shortText3` = `texte` du contact `autre`, `null` sans contact de ce rôle. |



# Annexe — Passer de l'API vacancies de Talentsoft à l'API v1

Cette annexe s'adresse aux employeurs qui publient aujourd'hui leurs offres dans le Back Office Talentsoft de la PEP avec l'API Talentsoft `PUT api/v1/vacancies/{vacancyReference}`, et qui envoient désormais ces offres à `POST /api/v1/offres/creer_modifier/`. Elle indique, pour chaque champ de l'offre envoyée à Talentsoft, le champ correspondant de l'API v1 et la conversion des valeurs. Les libellés entre guillemets sont ceux du formulaire offre du Back Office (fichier DGAFP « champs Offre BO V3 »).

Notation : `a.b` désigne un objet imbriqué, `a[]` une liste. Les champs `…Id` contiennent le code client d'une liste Talentsoft (colonne « Codeclient » du fichier DGAFP), converti selon la section « [Valeurs des listes Talentsoft](#valeurs-des-listes-talentsoft) ». Un texte HTML (`…HTML`) doit être converti en Markdown : l'API v1 rejette les balises HTML (voir le bloc « Description »). Les dates sont envoyées à l'API v1 au format ISO 8601 avec l'heure (`2026-11-05T00:00:00Z`).

Les blocs `localisation`, `criteres`, `conditions` et `contacts`, ainsi que `url_offre`, doivent figurer dans chaque offre, même sans valeur (`null`). Le bloc `conditions` exige `temps_travail` et `lieu_de_travail` : envoyez `NON_DEFINI` si le champ Talentsoft est vide.

### Champs de l'offre vacancies

| Offre vacancies | Offer API v1 | Note |
|---|---|---|
| `reference` | `identification.reference` | Le paramètre `{vacancyReference}` de l'URL Talentsoft. Une offre déjà envoyée avec la même référence est mise à jour. |
| `jobDescription.salaryRangeId` | `identification.versant` | « Versant » : `Versant_FPE` → `FPE`, `Versant_FPH` → `FPH`, `Versant_FPT` → `FPT`. |
| `jobDescription.title` | `titre` | « Intitulé du poste ». 104 caractères dans Talentsoft, 150 dans l'API v1. |
| `organisationId` | `organisation.nom` et `organisation.siret` | « Organisme de rattachement ». L'API v1 n'utilise pas le code d'entité Talentsoft : retrouvez l'organisme avec [`GET /api/v1/organismes/`](#6-consulter-les-organismes-get-apiv1organismes) (filtres `nom`, `siret`) et reprenez son `nom` et son `siret`. |
| `candidateRedirectionUrl` | `url_candidature` | « URL pour postuler candidat ». Renseigné, `email_candidature` reste vide. |
| `requestingParty.requestingPartyCustomFields.shortText1` | `email_candidature` | « Personne à qui adresser les candidatures ». Ne reprendre que l'adresse email, et seulement si `candidateRedirectionUrl` est vide : l'API v1 attend l'un ou l'autre, jamais les deux. |
| `requestingParty.requestingPartyCustomFields.shortText2` | `contacts[]` avec `role` = `principal` | « Contact 1 ». La valeur va dans `texte`, les adresses email qu'elle contient dans `emails`. Valeur vide : pas de contact. |
| `requestingParty.requestingPartyCustomFields.shortText3` | `contacts[]` avec `role` = `autre` | « Contact 2 ». Même règle que `shortText2`. |
| `requestingParty.beginningDate` | `publication.debut_vacance_poste` | « Date de vacance de l'emploi ». Peut aussi alimenter `conditions.debut_contrat`. |
| `jobDescription.primaryProfileId` | `profession.metier` | « Domaine et métier » : code métier RMFP (`ERACH001`…), à reprendre tel quel. `profession.domaine` est déduit du métier ; il n'est à envoyer que pour les métiers relevant de plusieurs domaines (`ERJUS008` → `JUS`, `ERTRA007` → `TRA`). `profession.referentiel` vaut `RMFPv2`. |
| `jobDescription.professionalCategoryId` | `vacance_poste` | « Statut du poste » : `STATUT01` (vacant) → `OUI`, `STATUT02` (susceptible d'être vacant) → `NON`. |
| `jobDescription.contractTypeId` | `nature_offre` | « Nature de l'emploi » : `NAT_TITULAIRE_CONTRACTUEL` → `TITULAIRE_CONTRACTUEL`, `NAT_CONTRACTUELS` → `CONTRACTUEL`. |
| `jobDescription.jobDescriptionCustomFields.customCodeTable1Id` | `categories` | « Catégorie », liste d'une seule valeur : `CAT-A` → `[A]`, `CAT-B` → `[B]`, `CAT-C` → `[C]`, `CAT-AEF` et `CAT-ESD` (encadrement supérieur) → `[APLUS]`. |
| `generalInformationCustomFields.customCodeTable2Id` | `type_contrat` | « Nature de contrat » : `CDD_6M`, `CDD_1A`, `CDD_2A`, `CDD_3A` → `CDD` ; `CDI` → `CDI`. Vide : `null`. La durée du CDD peut être reprise dans `conditions.duree_contrat` (« 6 mois », « 1 an »…). |
| `generalInformationCustomFields.date1` | `publication.fin_candidature` | « Date limite de candidature ». |
| `jobDescription.description1HTML` | `description.mission` | « Description du poste ». HTML converti en Markdown. |
| `jobDescription.description2HTML` | `description.profil` | « Descriptif du profil recherché ». HTML converti en Markdown ; texte vide s'il est absent. |
| `jobDescription.jobDescriptionCustomFields.longText1HTML` | `description.employeur` | « Descriptif de l'employeur ». HTML converti en Markdown ; texte vide s'il est absent. |
| `jobDescription.jobDescriptionCustomFields.longText2HTML` | `description.conditions_exercice` | « Conditions particulières d'exercice ». HTML converti en Markdown. |
| `jobDescription.jobDescriptionCustomFields.longText3HTML` | `description.descriptif_service` | « Descriptif du service ». HTML converti en Markdown. |
| `customBlock1CustomFields.longText1HTML` | `description.complements` | « Informations complémentaires ». HTML converti en Markdown ; texte vide s'il est absent. |
| `customBlock1CustomFields.longText2` | `conditions.bases_legales` | « Fondement juridique du recrutement ». Texte brut, accepté tel quel s'il ne contient pas de caractère interprété comme du Markdown. |
| `jobDescription.jobDescriptionCustomFields.shortText3` | `conditions.salaire_contractuel` | « Rémunération "contractuels" (en € brut/an) ». |
| `jobDescription.jobDescriptionCustomFields.customCodeTable3Id` | `conditions.temps_travail` | « Temps plein » : `reponse_oui` → `TEMPS_PLEIN`, `reponse_non` → `TEMPS_PARTIEL`, vide → `NON_DEFINI`. |
| `customBlock1CustomFields.customCodeTable2Id` | `conditions.lieu_de_travail` | « Télétravail » : `reponse_oui` → `TELETRAVAIL`, `reponse_non` → `SUR_SITE`, vide → `NON_DEFINI`. |
| `customBlock1CustomFields.customCodeTable1Id` | `conditions.management` | « Management » : `reponse_oui` → `AVEC`, `reponse_non` → `SANS`. Vide : ne pas envoyer le champ. |
| `criteria.criteriaCustomFields.customCodeTable1Id` | `criteres.documents_requis` | « Documents à transmettre » : `Doc_CV` → `[CV]`, `Doc_CV_LM` → `[CV, LETTRE_MOTIVATION]`, `Doc_CV_PF` → `[CV, PORTFOLIO]`, `Doc_CV_LM_PF` → `[CV, LETTRE_MOTIVATION, PORTFOLIO]`. `Doc_CV_BD` et `Doc_CV_LM_BD` (bande démo) n'ont pas d'équivalent : n'envoyer que `CV` et `LETTRE_MOTIVATION`. |
| `languages[]` | `criteres.langues[]` | Une entrée par langue : la langue (code ISO sur 2 caractères de la liste « Langues », par exemple `EN`) dans `iso_code`, le niveau (`A1` à `C2`, identiques dans les deux API) dans `niveau`. |
| `location.countryId` | `localisation[0].pays` | Code pays ISO 3166-1 alpha-3, identique dans les deux API (`FRA`, `DEU`…). |
| `location.regionId` | `localisation[0].region` | `R84` → `84` (préfixe `R` retiré pour obtenir le code INSEE), `_TS_CO_Region_DOM` → `DOM`, `_TS_CO_Region_TOM` (« COM ») → `TOM`. `null` hors de France. |
| `location.departmentId` | `localisation[0].departement` | Code département, identique dans les deux API (`01`, `2A`, `971`…). `null` hors de France. |
| `location.locationCustomFields.shortText1` | `localisation[0].localisation_label` | « Lieu d'affectation (sans géolocalisation) ». |
| `location.address` | `localisation[0].localisation_label` | « Lieu d'affectation ». À utiliser seulement si `shortText1` est vide. |

**Zone géographique.** L'offre vacancies n'a pas de zone géographique, obligatoire dans chaque `localisation` de l'API v1. En France, elle se déduit du département : `EU` en métropole, `AM` pour 971, 972, 973, 975, 977 et 978, `AF` pour 974 et 976, `OC` pour 986, 987, 988 et `WLF`. À l'étranger, elle se déduit du pays (`DEU` → `EU`, `MAR` → `MO`…).

### Valeurs des listes Talentsoft

| Liste Talentsoft | Conversion |
|---|---|
| Pays, départements, métiers, langues, niveaux de langue | Codes repris tels quels. |
| Régions | Préfixe `R` retiré (`R11` → `11`) ; `_TS_CO_Region_DOM` → `DOM`, `_TS_CO_Region_TOM` → `TOM`. |
| Versant, statut du poste, nature de l'emploi, catégorie, nature de contrat, documents à transmettre | Valeur API v1 indiquée dans le tableau ci-dessus. |
| Listes « Oui » / « Non » (`reponse_oui`, `reponse_non`) : temps plein, télétravail, management | Valeur explicite de l'API v1 (`TEMPS_PLEIN`, `TELETRAVAIL`, `AVEC`…), indiquée dans le tableau ci-dessus. |

### Champs vacancies sans équivalent dans l'API v1

| Offre vacancies | Note |
|---|---|
| `vacancyCategoryId` | Catégorie d'offre Talentsoft (`_TS_CO_OfferCategory_Standard`). |
| `vacancyViewId` | Paramétrage d'affichage du Back Office Talentsoft. |
| `candidateViewId` | Paramétrage d'affichage du Back Office Talentsoft. |
| `jobDescription.countryId` | Pays du type de contrat Talentsoft. Le pays de l'offre vient de `location.countryId`. |
| `jobDescription.jobDescriptionCustomFields.shortText1` | « Référence interne ». La référence de l'offre est `reference`. |
| `jobDescription.jobDescriptionCustomFields.t1htmlHasBeenShortened` | Indicateur Talentsoft de texte tronqué. Les limites de l'API v1 sont plus larges (voir le bloc « Description ») : envoyez le texte complet. |
| `jobDescription.jobDescriptionCustomFields.t2htmlHasBeenShortened` | Idem. |
| `jobDescription.jobDescriptionCustomFields.t3htmlHasBeenShortened` | Idem. |

### Champs de l'API v1 absents de l'offre vacancies

| Offer API v1 | Note |
|---|---|
| `publication.debut_publication` | **Obligatoire.** Dans Talentsoft, la publication passe par un appel séparé (fichiers `Publication.csv` et `Offerevent.csv`, dates de publication par défaut). Reprendre la date de début de publication. |
| `publication.fin_publication` | **Obligatoire.** Reprendre la date de fin de publication. |
| `localisation[].zone_geographique` | **Obligatoire.** Voir « Zone géographique » ci-dessus. |
| `titre_long` | « Intitulé long de l'offre » (`OfferCustomFields` `LongText1` dans le Back Office), absent de l'offre vacancies. À ne renseigner que s'il diffère de `titre`. |
| `conditions.salaire_titulaire` | « Rémunération "fonctionnaires" » (`jobDescriptionCustomFields.shortText2` dans le Back Office), absent du squelette vacancies. Le reprendre s'il est disponible. |
| `conditions.note_ouverture_poste_url` | « Avis de vacance au JO » (`customBlock1CustomFields.longText3` dans le Back Office) : lien `https` vers `legifrance.gouv.fr`. |
| `criteres.competences_requises` | « Compétences attendues » (`OfferApplicantCriteria` `LongText1` dans le Back Office). |
| `criteres.diplome_niveau` | « Niveau d'études » : `A` à `H` → `1` à `8`. |
| `criteres.experience` | « Niveau d'expérience » : `debutant` → `DEBUTANT`, `confirme` → `CONFIRME`, `expert` → `EXPERT`. |
| `criteres.specialisations` | « Spécialisation » : libellé de la spécialisation (`_TS_CO_Specialisation_6` → « Mathématiques »). |
| `criteres.diplome` | « Diplôme d'État requis » : libellé du diplôme. |
| `conditions.duree_contrat` | « Durée du contrat ». |
| `conditions.ouvert_aux_militaires` | `OUI` ou `NON`. |
| `conditions.fin_contrat` | Date de fin du contrat. |
| `url_offre` | Lien vers l'offre sur le site de l'employeur. Champ à envoyer dans chaque offre : `null` à défaut de lien. |
| `localisation[].latitude` / `longitude` | Coordonnées du lieu, facultatives. |
| `profession.code_emploi_local` | Code emploi propre à l'employeur, facultatif. |



*Document généré à partir du [schéma OpenAPI officiel](/static/api/schema.yaml). En cas de divergence, le schéma fait foi.*
