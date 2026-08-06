# Guide de l'API CSPLab — Version non technique

> Ce document explique, en langage accessible, ce que permet de faire l'API de CSPLab,
> à qui elle s'adresse, et **quelles sont les règles métier** à respecter sur chaque
> donnée envoyée ou reçue. Il est destiné aux personnes non techniques (métier,
> partenaires, gestion de projet) qui ont besoin de comprendre le fonctionnement de
> l'API sans lire de code.



## Sommaire

- [Qu'est-ce qu'une API, en deux phrases ?](#quest-ce-quune-api-en-deux-phrases-)
- [À qui s'adresse cette API ?](#à-qui-sadresse-cette-api-)
- [Comment fonctionne l'authentification ?](#comment-fonctionne-lauthentification-)
  - [Obtenir un jeton — `POST /api/token/`](#obtenir-un-jeton--post-apitoken)
  - [Rafraîchir un jeton — `POST /api/token/refresh/`](#rafraîchir-un-jeton--post-apitokenrefresh)
- [Limitations d'usage (quotas)](#limitations-dusage-quotas)
- [Les fonctionnalités de l'API](#les-fonctionnalités-de-lapi)
  - [1. Consulter les offres d'emploi — `GET /api/v1/offres/`](#1-consulter-les-offres-demploi--get-apiv1offres)
    - [Filtres disponibles](#filtres-disponibles)
  - [2. Consulter les offres d'une source — `GET /api/v1/offres/sources/{source_id}`](#2-consulter-les-offres-dune-source--get-apiv1offressourcessource_id)
  - [3. Archiver une offre — `POST /api/v1/offres/archiver`](#3-archiver-une-offre--post-apiv1offresarchiver)
  - [4. Créer ou modifier des offres — `POST /api/v1/offres/creer_modifier/`](#4-créer-ou-modifier-des-offres--post-apiv1offrescreer_modifier)
    - [Structure d'une offre et contraintes sur les champs](#structure-dune-offre-et-contraintes-sur-les-champs)
    - [En cas de problème](#en-cas-de-problème)
  - [5. Consulter les métiers — `GET /api/v1/metiers/`](#5-consulter-les-métiers--get-apiv1metiers)
  - [6. Importer des concours (fichier CSV) — `POST /api/v1/concours/upload/`](#6-importer-des-concours-fichier-csv--post-apiv1concoursupload)
    - [Format du fichier attendu](#format-du-fichier-attendu)
    - [Colonnes obligatoires](#colonnes-obligatoires)
    - [Comment se passe le traitement ?](#comment-se-passe-le-traitement-)
    - [Réponses possibles](#réponses-possibles)
- [Annexe — Les codes de réponse, en clair](#annexe--les-codes-de-réponse-en-clair)
- [Annexe — Récapitulatif des listes de valeurs autorisées](#annexe--récapitulatif-des-listes-de-valeurs-autorisées)
  - [Domaine fonctionnel (référentiel RMFPv2)](#domaine-fonctionnel-référentiel-rmfpv2)



## Qu'est-ce qu'une API, en deux phrases ?

Une API est une « porte d'entrée » automatisée qui permet à deux logiciels de
s'échanger des informations sans intervention humaine. Ici, l'API CSPLab permet à des
partenaires autorisés (par exemple des plateformes d'emploi public) de **transmettre
des offres d'emploi et des concours**, et de **consulter les offres et les métiers**
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



## Limitations d'usage (quotas)

Pour préserver le service, le nombre d'appels est plafonné :

- **120 appels par minute et par utilisateur** sur les routes de consultation et
  d'ingestion d'offres et de métiers.
- **100 offres maximum par appel** lors d'une création/modification groupée d'offres.



# Les fonctionnalités de l'API

L'API est organisée en quatre grands domaines :

| Domaine | À quoi ça sert |
|---|---|
| **Authentification** (`token`) | Obtenir et renouveler les jetons d'accès |
| **Offres** (`offres`) | Consulter, créer/modifier et archiver des offres d'emploi |
| **Métiers** (`metiers`) | Consulter le référentiel des métiers de la Fonction Publique |
| **Concours** (`concours`) | Importer des données de concours via un fichier CSV |



## 1. Consulter les offres d'emploi — `GET /api/v1/offres/`

Retourne la liste des offres d'emploi de la Fonction Publique, **paginée** (renvoyée
par lots plutôt qu'en une seule fois). La pagination se pilote avec les paramètres
`page` (numéro de page, défaut `1`) et `taille` (nombre d'éléments par page, défaut
`100`).

### Filtres disponibles

| Paramètre | Rôle | Format |
|---|---|---|
| `actif` | Ne retourner que les offres actives (`true`, valeur par défaut) ou archivées (`false`) | Booléen |
| `categorie` | Filtrer par catégorie(s) | Liste séparée par virgules parmi APLUS, A, B, C |
| `versant` | Filtrer par versant(s) | Liste séparée par virgules parmi FPT, FPE, FPH |
| `type_contrat` | Filtrer par type(s) de contrat | Liste séparée par virgules parmi TITULAIRE_CONTRACTUEL, CONTRACTUELS, TERRITORIAL |
| `niveau_experience` | Filtrer par niveau(x) d'expérience | Liste séparée par virgules parmi DEBUTANT, CONFIRME, EXPERT |
| `lieu_de_travail` | Filtrer par mode de travail | Liste séparée par virgules parmi NON_DEFINI, SUR_SITE, TELETRAVAIL |
| `management` | Filtrer selon la présence de management | Liste séparée par virgules parmi SANS, AVEC |
| `region` | Filtrer par code(s) région officiel(s) | Liste séparée par virgules (ex. `11,84`) |
| `departement` | Filtrer par code(s) département officiel(s) | Liste séparée par virgules (ex. `75,69`) |
| `pays` | Filtrer par code(s) pays alpha-3 | Liste séparée par virgules (ex. `FRA,BEL`) |
| `domaine` | Filtrer par code(s) de domaine fonctionnel | Liste séparée par virgules (ex. `NUM,ACH`) |
| `organisme` | Filtrer par nom exact d'organisme | Répéter le paramètre pour en filtrer plusieurs (ex. `?organisme=Foo&organisme=Bar`) — ne pas séparer les valeurs par une virgule, un nom d'organisme pouvant en contenir une |
| `date_publication` | Ne retourner que les offres publiées au cours des N derniers jours | Entier négatif (ex. `-7`) |
| `latitude`, `longitude`, `radius` | Filtre géographique par rayon autour d'un point — **les trois doivent être fournis ensemble** | `latitude`/`longitude` en degrés décimaux, `radius` en kilomètres (entier positif) |

> Les filtres à valeurs multiples acceptent une liste de valeurs séparées par une
> virgule. Une valeur invalide pour l'un de ces filtres renvoie une erreur `400`.

Chaque offre renvoyée contient notamment :

| Information | Signification | Peut être vide ? |
|---|---|---|
| `external_id` | Identifiant unique de l'offre dans le système | Non |
| `reference` | Référence d'origine de l'offre | Non |
| `source_id` | Identifiant de la source ayant transmis l'offre | Non |
| `title` | Intitulé du poste | Non |
| `organization` | Organisme employeur | Non |
| `contract_type` | Type de contrat | Oui |
| `category` | Catégorie (A+, A, B, C…) | Oui |
| `publication_date` | Date de publication | Non |
| `offer_url` | Lien vers l'annonce | Oui |
| `archived_at` | Date d'archivage de l'offre | Oui |

> **Règle métier clé :** une offre dont `archived_at` est **vide** est **active** ;
> une offre dont `archived_at` est **renseigné** est **archivée**.



## 2. Consulter les offres d'une source — `GET /api/v1/offres/sources/{source_id}`

Retourne, **paginée**, la liste complète des offres d'emploi rattachées à la source
identifiée par son identifiant unique (`source_id`, UUID). La pagination fonctionne
comme pour la liste principale des offres (paramètres `page` et `taille`).

> **Règle métier :** l'accès à une source non autorisée pour l'utilisateur authentifié
> renvoie une erreur `401`, même si la source existe.

Chaque offre renvoyée contient, en plus des informations de la liste principale
(voir section précédente), le détail complet de l'offre : `long_title`, `employer`,
`profile`, `mission`, `complements`, `verse`, `contract_kind`, `job_vacancy`,
`application_url`, `localisation`, `criteria`, `conditions`, `contacts`,
`beginning_date`.

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



## 4. Créer ou modifier des offres — `POST /api/v1/offres/creer_modifier/`

C'est la fonctionnalité la plus riche. Elle permet d'envoyer **entre 1 et 100 offres**
en un seul appel.

> **Règle métier centrale (« upsert ») :** chaque offre est identifiée par le couple
> **`identification.reference` + source**. Si une offre portant cette référence existe
> déjà, elle est **mise à jour** ; sinon, elle est **créée**.

La réponse indique combien d'offres ont été **créées**, **mises à jour**, et la liste
des offres **rejetées** avec le détail de l'erreur. Une offre rejetée n'empêche pas les
autres d'être traitées.

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
| `titre_long` | Obligatoire. **1 500 caractères maximum.** |
| `url_offre` | Lien web. Peut être vide. |
| `url_candidature` | Lien web. Peut être vide. |

#### Bloc « Organisation » (`organisation`) — obligatoire
| Champ | Règle |
|---|---|
| `nom` | Obligatoire. Nom de l'organisme. |
| `siret` | Obligatoire. **14 caractères maximum.** |

#### Bloc « Profession » (`profession`) — obligatoire
| Champ | Règle |
|---|---|
| `referentiel` | Référentiel utilisé. Valeur par défaut : **RMFPv2**. |
| `domaine` | Obligatoire. Code du domaine fonctionnel (vérifié uniquement si `referentiel=RMFPv2`). **3 caractères maximum.** |
| `metier` | Obligatoire. Code métier. **8 caractères maximum.** |
| `code_emploi_local` | Code emploi local propre au partenaire. Peut être vide. **50 caractères maximum.** |

#### Catégorie et contrat
| Champ | Règle |
|---|---|
| `categories` | Liste. Valeurs autorisées : **APLUS, A, B, C, HORS_CATEGORIE** (ou vide). |
| `type_contrat` | Valeurs autorisées : **TITULAIRE_CONTRACTUEL, CONTRACTUELS, TERRITORIAL**. |
| `forme_contrat` | Liste. Valeurs autorisées : **CDD, CDI, PERMANENT, VACATION** (ou vide). |
| `vacance_poste` | **OUI** = poste vacant ; **NON** = poste susceptible d'être vacant (ou vide). |

#### Bloc « Description » (`description`) — obligatoire
Tous les champs ci-dessous sont obligatoires.

| Champ | Règle |
|---|---|
| `mission` | **10 000 caractères maximum.** |
| `profil` | **10 000 caractères maximum.** |
| `employeur` | **3 000 caractères maximum.** |
| `complements` | **5 000 caractères maximum.** |

#### Bloc « Localisation » (`localisation`) — liste, peut être vide
| Champ | Règle |
|---|---|
| `zone_geographique` | Obligatoire dans chaque localisation. Valeurs : **AF** (Afrique), **EU** (Europe), **AS** (Asie), **AM** (Amérique), **OC** (Océanie), **AN** (Antarctique). |
| `pays` | Obligatoire. Code pays sur **exactement 3 caractères**. |
| `region` | Code région officiel, ou vide. |
| `departement` | Code département officiel (`01` à `95`, `2A`, `2B`, DOM-TOM, `SPM`, `WLF`…), ou vide. |
| `localisation_label` | Libellé du lieu. **500 caractères maximum.** |
| `latitude` / `longitude` | Coordonnées géographiques. Peuvent être vides. |

#### Bloc « Critères » (`criteres`) — peut être vide
| Champ | Règle |
|---|---|
| `diplome_niveau` | Nombre entier **entre 1 et 8** (niveaux de diplôme). |
| `experience` | Valeurs : **DEBUTANT, CONFIRME, EXPERT**. |
| `specialisations` | Liste de textes. |
| `diplome` | Texte. |
| `documents_requis` | Liste de textes. |
| `competences_requises` | Liste de textes. |
| `langues` | Liste de langues, chacune avec un **code ISO sur 2 caractères** et un **niveau** (**A1, A2, B1, B2, C1, C2**). |

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
| `management` | Obligatoire. **AVEC** ou **SANS** management. |
| `complements` | **1 500 caractères maximum.** |
| `bases_legales` | **1 500 caractères maximum.** |
| `note_ouverture_poste_url` | Lien web. |

#### Bloc « Contacts » (`contacts`) — liste, peut être vide
| Champ | Règle |
|---|---|
| `email` | Obligatoire dans chaque contact. Doit être une **adresse email valide**. |

#### Bloc « Publication » (`publication`) — obligatoire
| Champ | Règle |
|---|---|
| `debut_publication` | Obligatoire. Date. |
| `fin_publication` | Obligatoire. Date. |
| `fin_candidature` | Date. Peut être vide. |
| `debut_vacance_poste` | Date. Peut être vide. |

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
| `offer_family_code` | Code de la famille d'offres (peut être vide) |



## 6. Importer des concours (fichier CSV) — `POST /api/v1/concours/upload/`

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
| **Type de contrat** | TITULAIRE_CONTRACTUEL, CONTRACTUELS, TERRITORIAL |
| **Forme de contrat** | CDD, CDI, PERMANENT, VACATION |
| **Vacance de poste** | OUI (vacant), NON (susceptible d'être vacant) |
| **Expérience** | DEBUTANT, CONFIRME, EXPERT |
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



*Document généré à partir du [schéma OpenAPI officiel](`/static/api/schema.yaml`). En cas de divergence, le schéma fait foi.*
