# Documentation API — Dépôt d'offres d'emploi

> **Version** 1.2 · **Mise à jour** mars 2026
> Cette API remplace le dépôt de fichiers CSV par FTP. Elle permet de créer, mettre à jour et publier vos offres d'emploi directement via des appels HTTP.

---

## Sommaire

1. [Authentification](#1-authentification)
2. [Vos références](#2-vos-références)
3. [Déposer une offre](#3-déposer-une-offre)
4. [Déposer plusieurs offres en une seule fois](#4-déposer-plusieurs-offres-en-une-seule-fois)
5. [Modifier une offre](#5-modifier-une-offre)
6. [Publier une offre](#6-publier-une-offre)
7. [Dépublier une offre](#7-dépublier-une-offre)
8. [Consulter une offre](#8-consulter-une-offre)
9. [Lister vos offres](#9-lister-vos-offres)
10. [Consulter les référentiels](#10-consulter-les-référentiels)
11. [Codes d'erreur](#11-codes-derreur)
12. [Correspondance avec les fichiers FTP](#12-correspondance-avec-les-fichiers-ftp)

---

## 1. Authentification

Toutes les requêtes doivent inclure un token Bearer dans le header HTTP.

```
Authorization: Bearer <votre_token>
```

Votre token est propre à votre organisation. Il détermine l'espace dans lequel vos offres sont isolées — deux organisations peuvent utiliser les mêmes références sans risque de collision. Contactez votre administrateur pour obtenir votre token d'accès.

---

## 2. Vos références

Vous devez utiliser vos propres références pour identifier vos offres, sans avoir à gérer les références internes du système.

### Principe

Lors de la création d'une offre, vous alimentez un champ `offer_reference` avec la référence de votre choix (identifiant de votre SIRH, numéro de poste, code interne, etc.). Cette référence doit être unique dans votre espace.

### Règles

- `offer_reference` est obligatoire, elle permet d'identifier vos offres d'emploi.
- Elle doit être unique **dans votre espace**. Deux organisations différentes peuvent avoir la même valeur sans conflit.
- Elle ne peut pas être modifiée après création.
- Les identifiants internes du système (UUID) ne sont jamais exposés dans les réponses de l'API.

### Utilisation dans les URLs

```
GET /api/offres/MININT-RH-2026-047/
PATCH /api/offres/MININT-RH-2026-047/
POST  /api/offres/MININT-RH-2026-047/publier/
POST  /api/offres/MININT-RH-2026-047/depublier/
```

---

## 3. Déposer une offre

Crée une nouvelle offre dans le système. Équivaut au dépôt simultané de tous les fichiers CSV sur le FTP.

**Requête**

```
POST /api/offres/
Content-Type: application/json
```

**Corps de la requête**

```json
{
  "offer_reference": "MININT-RH-2026-047",
  "intitule": "Chargé de mission RH - Transformation numérique",
  "nombre_postes": 1,
  "date_prise_poste": "2026-06-01",
  "date_debut_publication": "2026-03-15",
  "date_fin_publication": "2026-04-30",
  "url_redirection_candidat": "https://ministere.gouv.fr/offre/123",
  "is_extern": false,
  "regular_offer": true,

  "entite_id": 42,
  "versant_id": "Versant_FPT",
  "nature_contrat_id": "NAT_TITULAIRE_CONTRACTUEL",
  "domaine_id": 7,
  "metier_id": "ERDOC006",
  "categorie_id": 3,
  "statut_poste_id": 1,
  "niveau_etudes_id": 6,
  "niveau_experience_id": 1,
  "departement_id": 75,

  "description": {
    "description1": "Au sein de la DRH, vous pilotez les projets de transformation...",
    "description2": "Diplômé d'un Bac+5 en RH ou management public...",
    "temps_plein": 1,
    "categorie_emploi": 3
  },

  "conditions": {
    "type_contrat": 3,
    "teletravail": true,
    "management": false,
    "remuneration": "Selon grille indiciaire + IFSE"
  },

  "criteres": {
    "documents": 2,
    "info_complementaire": "Merci de joindre vos 3 derniers bulletins de salaire."
  },

  "responsable": {
    "login_gestionnaire": "marie.dupont",
    "nom_manager": "Dupont",
    "prenom_manager": "Marie",
    "telephone_manager": "+33 1 23 45 67 89",
    "email_manager": "marie.dupont@ministere.gouv.fr"
  },

  "langues": [
    { "langue": 12, "niveau": 4 },
    { "langue": 33, "niveau": 2 }
  ],

  "specialisations": [
    { "specialisation": 8 }
  ],

  "localisations": [
    { "departement": 75, "region": null, "pays": null }
  ]
}
```

**Champs obligatoires**

| Champ | Description |
|---|---|
| `intitule` | Intitulé du poste (max. 255 caractères) |
| `entite_id` | ID de l'organisme de rattachement |
| `versant_id` | ID du versant (FPE, FPH, FPT) |
| `nature_contrat_id` | ID de la nature du contrat |
| `statut_poste_id` | ID du statut du poste (Vacant, Susceptible d'être vacant) |

**Champs facultatifs notables**

| Champ | Description |
|---|---|
| `offer_reference` | Votre référence interne (voir [section 2](#2-vos-références)) |

**Réponse — 201 Created**

```json
{
  "offer_reference": "MININT-RH-2026-047",
  "creation_date": "2026-03-02T09:14:22Z",
  "modification_date": "2026-03-02T09:14:22Z",
  "intitule": "Chargé de mission RH - Transformation numérique",
  "entite": {
    "id": 42,
    "entity_code": "DGAFP",
    "name": "Direction Générale de l'Administration et de la Fonction Publique"
  },
  "versant": {
    "id": 1,
    "code_client": "Versant_FPE",
    "libelle": "Fonction publique de l'Etat"
  },
  "langues": [
    { "langue": 12, "langue_display": "Anglais", "niveau": 4, "niveau_display": "Avancé ou indépendant" },
    { "langue": 33, "langue_display": "Espagnol", "niveau": 2, "niveau_display": "Intermédiaire ou de survie" }
  ],
  "publications": [],
  "events": []
}
```

> **À noter :** La référence système (`reference`) est générée automatiquement. Si vous avez fourni une `offer_reference`, les deux sont utilisables pour toutes les opérations ultérieures.

---

## 4. Déposer plusieurs offres en une seule fois

Permet de créer jusqu'à 100 offres en un seul appel HTTP. Chaque offre est traitée indépendamment et le résultat détaillé par offre est retourné dans la réponse.

### Mode standard — traitement indépendant

Les offres valides sont créées même si d'autres échouent dans le même lot.

**Requête**

```
POST /api/offres/bulk/
Content-Type: application/json
```

```json
[
  {
    "offer_reference": "MININT-RH-2026-047",
    "intitule": "Chargé de mission RH",
    "entite_id": 42,
    "versant_id": 1,
    "nature_contrat_id": 2,
    "statut_poste_id": 1,
    "description": {
      "description1": "Au sein de la DRH..."
    }
  },
  {
    "offer_reference": "MININT-RH-2026-048",
    "intitule": "Responsable achats",
    "entite_id": 42,
    "versant_id": 1,
    "nature_contrat_id": 2,
    "statut_poste_id": 1
  }
]
```

**Réponse — 207 Multi-Status**

```json
{
  "total": 2,
  "succes": 2,
  "erreurs": 0,
  "resultats": [
    {
      "index": 0,
      "statut": "created",
      "offer_reference": "MININT-RH-2026-047"
    },
    {
      "index": 1,
      "statut": "created",
      "offer_reference": "MININT-RH-2026-048"
    }
  ]
}
```

**Exemple avec une offre en erreur**

```json
{
  "total": 2,
  "succes": 1,
  "erreurs": 1,
  "resultats": [
    {
      "index": 0,
      "statut": "created",
      "offer_reference": "MININT-RH-2026-047"
    },
    {
      "index": 1,
      "statut": "error",
      "offer_reference": "MININT-RH-2026-048",
      "erreurs": {
        "versant_id": ["Invalid pk \"99\" - object does not exist."]
      }
    }
  ]
}
```

### Mode atomique — tout ou rien

Avec le paramètre `?atomic=true`, si une seule offre est invalide, **aucune** offre du lot n'est créée. Utile pour garantir la cohérence d'un ensemble d'offres liées.

**Requête**

```
POST /api/offres/bulk/?atomic=true
```

**Réponse en cas d'erreur — 422 Unprocessable Entity**

```json
{
  "message": "Dépôt annulé — 1 offre invalide sur 2. Aucune offre créée.",
  "total": 2,
  "succes": 0,
  "erreurs": 1,
  "resultats": [
    {
      "index": 0,
      "statut": "annulé"
    },
    {
      "index": 1,
      "statut": "error",
      "offer_reference": "MININT-RH-2026-048",
      "erreurs": {
        "versant_id": ["Invalid pk \"99\" - object does not exist."]
      }
    }
  ]
}
```

### Limites

| Limite | Valeur |
|---|---|
| Nombre maximum d'offres par appel | 100 |
| Taille maximale de la requête | 5 Mo |

> Au-delà de 100 offres, découpez votre lot en plusieurs appels successifs.

---

## 5. Modifier une offre

Met à jour une offre existante. Vous pouvez envoyer uniquement les champs à modifier.

**Requête**

```
PATCH /api/offres/{offer_reference}/
Content-Type: application/json
```

**Exemple — prolonger la publication et ajouter une langue**

```bash
PATCH /api/offres/MININT-RH-2026-047/
```

```json
{
  "date_fin_publication": "2026-05-31",

  "langues": [
    { "langue": 12, "niveau": 4 },
    { "langue": 33, "niveau": 2 },
    { "langue": 55, "niveau": 3 }
  ]
}
```

> ⚠️ **Important — champs de type liste** (`langues`, `specialisations`, `localisations`) : ces champs appliquent un remplacement complet. Vous devez envoyer la liste entière des valeurs souhaitées, pas uniquement les ajouts ou suppressions. Exemple : pour ajouter une 3e langue, renvoyez les 2 langues existantes + la nouvelle.

**Réponse — 200 OK**

L'objet complet de l'offre est retourné avec les modifications appliquées.

---

## 6. Publier une offre

Déclenche la publication de l'offre sur le portail. Équivaut au dépôt du fichier `Publication.csv` et `Offerevent.csv` avec le statut `Publié`.

**Requête**

```
POST /api/offres/{offer_reference}/publier/
Content-Type: application/json
```

```bash
POST /api/offres/MININT-RH-2026-047/publier/
```

**Corps de la requête**

```json
{
  "date_debut": "2026-03-15",
  "date_fin": "2026-04-30",
  "login": "marie.dupont"
}
```

| Champ | Obligatoire | Description |
|---|---|---|
| `date_debut` | Oui | Date de début de publication (format `AAAA-MM-JJ`) |
| `date_fin` | Non | Date de fin de publication (format `AAAA-MM-JJ`) |
| `login` | Oui | Login de l'agent qui déclenche la publication |

**Réponse — 200 OK**

```json
{
  "offer_reference": "MININT-RH-2026-047",
  "publication": {
    "id": 91,
    "publication_key": "a3f2c1d4-89ab-4e56-b012-3f4a5b6c7d8e",
    "statut": "publie",
    "date_debut": "2026-03-15",
    "date_fin": "2026-04-30"
  },
  "event": {
    "type_event": "debut_diffusion",
    "event_date": "2026-03-02",
    "login": "marie.dupont",
    "creation_date": "2026-03-02T10:05:00Z"
  }
}
```

---

## 7. Dépublier une offre

Retire l'offre du portail. Équivaut au dépôt des fichiers `Publication.csv` et `Offerevent.csv` avec le statut `Non publié`.

**Requête**

```
POST /api/offres/{offer_reference}/depublier/
Content-Type: application/json
```

**Corps de la requête**

```json
{
  "login": "marie.dupont",
  "commentaire": "Poste pourvu en interne."
}
```

| Champ | Obligatoire | Description |
|---|---|---|
| `login` | Oui | Login de l'agent qui déclenche la dépublication |
| `commentaire` | Non | Motif de dépublication |

**Réponse — 200 OK**

```json
{
  "offer_reference": "MININT-RH-2026-047",
  "publication": {
    "id": 91,
    "statut": "non_publie",
    "date_fin": "2026-03-02"
  },
  "event": {
    "type_event": "arret_diffusion",
    "event_date": "2026-03-02",
    "login": "marie.dupont",
    "commentaire": "Poste pourvu en interne."
  }
}
```

---

## 8. Consulter une offre

Retourne le détail complet d'une offre, avec tous ses sous-ensembles (langues, localisations, historique de publication, etc.).

**Requête**

```
GET /api/offres/{offer_reference}/
```

**Réponse — 200 OK**

```json
{
  "offer_reference": "MININT-RH-2026-047",
  "intitule": "Chargé de mission RH - Transformation numérique",
  "creation_date": "2026-03-02T09:14:22Z",
  "modification_date": "2026-03-02T10:05:00Z",
  "nombre_postes": 1,
  "versant": { "code_client": "Versant_FPE", "libelle": "Fonction publique de l'Etat" },
  "metier": { "code_client": "ERHRH012", "libelle": "Chargé de mission RH" },
  "description": {
    "description1": "Au sein de la DRH...",
    "description2": "Diplômé d'un Bac+5...",
    "temps_plein_display": "Oui"
  },
  "conditions": {
    "teletravail": true,
    "management": false,
    "type_contrat_display": "CDD de 2 ans"
  },
  "langues": [
    { "langue_display": "Anglais", "niveau_display": "Avancé ou indépendant" }
  ],
  "publications": [
    {
      "statut": "publie",
      "date_debut": "2026-03-15",
      "date_fin": "2026-04-30"
    }
  ],
  "events": [
    {
      "type_event": "debut_diffusion",
      "event_date": "2026-03-02",
      "login": "marie.dupont"
    }
  ]
}
```

---

## 9. Lister vos offres

Retourne la liste paginée de vos offres, avec des filtres disponibles. Seules les offres de votre organisation sont retournées.

**Requête**

```
GET /api/offres/?{filtres}
```

**Filtres disponibles**

| Paramètre | Description | Exemple |
|---|---|---|
| `versant` | Filtrer par versant | `versant=Versant_FPE` |
| `departement` | Filtrer par code département | `departement=75` |
| `statut` | Filtrer par statut de publication | `statut=publie` |
| `metier` | Filtrer par code métier | `metier=ERHRH012` |
| `page` | Numéro de page | `page=2` |
| `page_size` | Nombre de résultats par page (défaut : 20) | `page_size=50` |

**Exemple**

```
GET /api/offres/?versant=Versant_FPE&departement=75&statut=publie&page=1
```

**Réponse — 200 OK**

```json
{
  "count": 143,
  "next": "/api/offres/?versant=Versant_FPE&departement=75&statut=publie&page=2",
  "previous": null,
  "results": [
    {
      "offer_reference": "MININT-RH-2026-047",
      "intitule": "Chargé de mission RH - Transformation numérique",
      "entite": { "entity_code": "DGAFP", "name": "DGAFP" },
      "versant": { "code_client": "Versant_FPE", "libelle": "Fonction publique de l'Etat" },
      "metier": { "code_client": "ERHRH012", "libelle": "Chargé de mission RH" },
      "departement": { "code": "75", "libelle": "Paris (75)" },
      "date_debut_publication": "2026-03-15",
      "date_fin_publication": "2026-04-30",
      "nombre_postes": 1
    }
  ]
}
```

---

## 10. Consulter les référentiels

Les référentiels contiennent les valeurs autorisées pour les champs à liste de sélection. Utilisez les `id` retournés pour alimenter vos requêtes de création ou de modification d'offres.

### Liste d'un référentiel

```
GET /api/referentiels/{type}/
```

Types disponibles : `versants`, `categories`, `nature-contrats`, `type-contrats`, `domaines`, `metiers`, `niveau-etudes`, `niveau-experience`, `specialisations`, `statut-postes`, `diplomes-etat`, `langues`, `niveau-langue`, `documents-transmettre`

**Exemple — récupérer les métiers d'un domaine**

```
GET /api/referentiels/metiers/?domaine=ERHRH
```

**Réponse — 200 OK**

```json
[
  { "id": 101, "code_client": "ERHRH001", "libelle": "Directeur des ressources humaines" },
  { "id": 102, "code_client": "ERHRH002", "libelle": "Responsable RH" },
  { "id": 103, "code_client": "ERHRH012", "libelle": "Chargé de mission RH" }
]
```

### Arbre des entités organisationnelles

```
GET /api/referentiels/entites/?parent=FPE&depth=2
```

**Réponse — 200 OK**

```json
{
  "id": 2,
  "entity_code": "FPE",
  "name": "Fonction Publique d'Etat",
  "enfants": [
    {
      "id": 10,
      "entity_code": "MININT",
      "name": "Ministère de l'Intérieur",
      "enfants": [
        { "id": 55, "entity_code": "DGPN", "name": "Direction Générale de la Police Nationale" },
        { "id": 56, "entity_code": "DGGN", "name": "Direction Générale de la Gendarmerie Nationale" }
      ]
    }
  ]
}
```

### Référentiel de localisation

```
GET /api/referentiels/localisation/
```

Retourne la hiérarchie complète Continents → Pays / Régions → Départements.

---

## 11. Codes d'erreur

| Code HTTP | Signification | Que faire |
|---|---|---|
| `400 Bad Request` | Données invalides ou référentiel introuvable | Vérifiez les IDs envoyés et consultez le référentiel correspondant |
| `401 Unauthorized` | Token manquant ou invalide | Vérifiez votre token d'authentification |
| `403 Forbidden` | Vous n'avez pas accès à cette ressource | Contactez votre administrateur |
| `404 Not Found` | Référence d'offre introuvable | Vérifiez la référence utilisée (système ou tiers) |
| `422 Unprocessable Entity` | Erreur de cohérence métier ou lot atomique rejeté | Lisez le détail de l'erreur dans la réponse |

### Exemples de réponses d'erreur

**Référentiel inactif ou inexistant — 400**

```json
{
  "nature_contrat_id": [
    "Invalid pk \"99\" - object does not exist."
  ]
}
```

> Un référentiel peut être désactivé par un administrateur. Consultez `/api/referentiels/{type}/` pour obtenir les valeurs actives.

**Référence tiers déjà utilisée — 400**

```json
{
  "offer_reference": [
    "La référence 'MININT-RH-2026-047' existe déjà dans votre espace."
  ]
}
```

**Incohérence métier/domaine — 422**

```json
{
  "metier": [
    "Ce métier n'appartient pas au domaine sélectionné."
  ]
}
```

**Offre introuvable — 404**

Retourné que vous utilisiez une référence système ou une référence tiers inconnue. Le système ne distingue pas les deux cas pour ne pas confirmer l'existence d'une offre appartenant à une autre organisation.

---

## 12. Correspondance avec les fichiers FTP

Le tableau ci-dessous indique comment chaque fichier CSV du FTP correspond aux champs de l'API.

| Fichier FTP | Section API | Champ de la requête |
|---|---|---|
| `Offer.csv` | Corps principal | Champs racine de l'offre (`intitule`, `versant_id`, etc.) |
| `OfferJobdescriptionCustomfields.csv` | Description | Bloc `description` |
| `OfferCustomBlock1Customfields.csv` | Conditions | Bloc `conditions` |
| `OfferCustomFields.csv` | Champs libres | Bloc `custom_fields` |
| `OfferLocationCustomFields.csv` | Localisations | Tableau `localisations` |
| `OfferLanguage.csv` | Langues | Tableau `langues` |
| `OfferSpecialisation.csv` | Spécialisations | Tableau `specialisations` |
| `OfferApplicantCriteria.csv` | Critères candidature | Bloc `criteres` |
| `Publication.csv` | Publication | Endpoint `POST /publier/` |
| `Offerevent.csv` | Événements | Généré automatiquement par `/publier/` et `/depublier/` |
| `Offeruser.csv` | Responsable | Bloc `responsable` |
| Tous les `OF_*.csv` | Référentiels | `GET /api/referentiels/{type}/` |

> **Migration depuis le FTP :** Chaque dépôt multi-fichiers sur le FTP est remplacé par un seul appel `POST /api/offres/`. Votre champ `OfferReference` des fichiers CSV devient le champ `offer_reference` de l'API.
