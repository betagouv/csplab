# ADR-006 : Les use cases de lecture retournent des Read Models, pas des entités du domaine

## Status

Accepted

## Context

Dans le cadre de l'implémentation du use case `ListerMesRecrutementsUsecase`, une question architecturale s'est posée : **le use case doit-il retourner des entités du domaine (aggregate `Recrutement`) ou des Read Models (DTOs) ?**

Il a été suggéré que le use case retourne des entités du domaine, parce que le code serait ainsi plus homogène et que la couche présentation pourrait accéder aux données dont elle a besoin via les propriétés de l'entité.

Deux positions s'affrontent :

- **Position A** : le use case retourne des aggregates/entités du domaine, que la présentation transforme ensuite
- **Position B** : le use case retourne des Read Models (DTOs), construits spécifiquement pour les besoins de la vue

### Analyse des besoins de la vue

La vue liste des recrutements actifs attend les données suivantes (extrait des données statiques de `RecrutementsActifsView`) :

```python
{
    "offer_id": UUID,
    "intitule": str,                      # titre de l'offre (OfferModel.title)
    "reference_csp": str,                 # code emploi CSP (OfferModel.code_emploi_csp)
    "type_contrat": str,                  # type de contrat (OfferModel.contract_type)
    "date_publication": datetime,          # date de publication (OfferModel.publication_date)
    "responsables": [{"nom": "Dupont"}],  # noms des agents responsables (UserModel)
    "derniere_activite": datetime,         # date max des candidatures
    "candidatures": {"total": 5, "a_traiter": 2, "en_cours": 1},  # agrégation SQL
}
```

L'entité `Recrutement` (aggregate) expose quant à elle :

```python
offre_id: UUID          # pas le titre, ni le type contrat
organisme_id: UUID
etapes: tuple[EtapeRecrutement, ...]
candidatures: tuple[UUID, ...]   # juste des UUIDs, pas des compteurs
responsables: tuple[UUID, ...]   # juste des UUIDs, pas des noms
status: StatutRecrutement
candidat_recrute_id: UUID | None
derniere_activite_le: datetime | None
```

**Aucun champ de la vue n'est directement disponible sur l'aggregate.** Tous les champs de la vue proviennent soit d'autres entités (`Offer`), soit d'agrégations SQL (compteurs), soit de données de présentation (formatage des noms).

## Decision

### Principe : séparation entre le modèle de commande et le modèle de lecture

Le pattern **CQRS** préconise de séparer les modèles utilisés pour les écritures de ceux utilisés pour les lectures :

- **Écritures (commands)** : manipulent les aggregates, protègent les invariants, exécutent des règles métier
- **Lectures (queries)** : retournent des Read Models, optimisés pour la restitution des données, sans comportement métier

Dans notre implémentation :

```
Commande : CreerRecrutementUsecase → manipule l'aggregate Recrutement → IRecrutementRepository
Requête  : ListerMesRecrutementsUsecase → interroge IRecrutementQueryService → RecrutementActifsReadModel
```

### L'Application Layer compose des DTOs pour la UI

Conformément à Vaughn Vernon (*Implementing Domain-Driven Design*, Chapter 14), l'Application Layer a pour rôle de composer des données issues de différents modèles en un format cohérent pour la UI :

> *"Services in that single layer are devoid of business domain logic. It will only serve to aggregate objects from each model into cohesive ones that the user interface needs."*

C'est exactement ce que fait notre `PostgresRecrutementQueryService` dans l'infrastructure : il agrège les données de `RecrutementModel`, `OfferModel`, `ProfilAgentModel` et des annotations SQL en un Read Model cohérent pour la UI.

### Mais attention à ne pas créer un Anemic Domain Model

Vernon met en garde :

> *"Here the Application Services manage a merger of various DTOs, which mimic a sort of Anemic Domain Model."*

C'est une mise en garde importante : si les DTOs deviennent trop complexes, on recrée un domaine anémique dans l'application. Pour éviter cela, on limite les Read Models à leur strict nécessaire (un fichier de ~40 lignes) et on ne les utilise que pour les queries, pas pour les commands.

### Où placer les Read Models

Les Read Models sont placés dans la couche **application** :

```
src/web/application/recruteur/dtos/recrutement_read_models.py
```

Ils sont définis au plus proche du use case qui les consomme. L'interface du query service (`IRecrutementQueryService`) est également dans la couche application (`application/recruteur/services/`), car c'est un **port** technique, pas un concept métier.

**Pourquoi pas dans le domaine ?** Le domaine doit rester pur — il ne doit pas être modelé par les besoins de la UI. Comme le dit Eric Evans (*Domain-Driven Design*, Chapter 4) :

> *"The MODEL in the domain layer should capture the essential concepts of the domain, not be shaped by the needs of the UI or infrastructure."*

Si on ajoutait des champs comme `candidatures_total` à l'aggregate `Recrutement` pour satisfaire la vue, le modèle serait contaminé par la présentation.

### Pourquoi ne pas retourner des entités du domaine ?

L'aggregate `Recrutement` utilise des **références par identifiant** (UUIDs) pour ses relations avec d'autres aggregates (`offre_id`, `responsables: tuple[UUID, ...]`). C'est une pratique standard en DDD (Vernon, *Implementing Domain-Driven Design*, Chapter 10) pour éviter de charger tout le graphe d'objets et pour maintenir les frontières d'aggregates.

Il ne contient donc pas les données nécessaires à la vue (titre de l'offre, noms des responsables, compteurs de candidatures). Pour que le use case retourne des entités, deux options problématiques :

1. **Enrichir l'aggregate** avec des champs de présentation (`intitule`, `candidatures_total`, etc.) → contamination du domaine
2. **Charger les données manquantes dans la présentation** → N+1 queries et fuite de responsabilité

### Mapping vers la vue

La couche présentation applique une dernière transformation via des mappers dédiés (ex. `RecrutementsActifsMapper`) pour convertir les Read Models typés en dictionnaires compatibles avec les serializers DRF. Ce mapping est une **simple traduction de format**, pas une récupération de données supplémentaires.

## Rationale

### 1. Vaughn Vernon — Implementing Domain-Driven Design (2013)

Deux citations encadrent notre décision :

La première justifie le rôle de l'Application Layer comme compositeur de DTOs pour la UI (Chapter 14) :

> *"Services in that single layer are devoid of business domain logic. It will only serve to aggregate objects from each model into cohesive ones that the user interface needs."*

La seconde met en garde contre l'Anemic Domain Model (Chapter 14) :

> *"Here the Application Services manage a merger of various DTOs, which mimic a sort of Anemic Domain Model."*

Ces deux citations ensemble décrivent notre situation : nous composons des DTOs dans l'application pour la UI, mais nous sommes conscients du risque d'Anemic Domain Model et nous le limitons en restreignant les DTOs aux seules queries.

### 2. Références par identifiant (Vernon, Ch. 10)

L'aggregate `Recrutement` référence ses relations par UUIDs plutôt que par objets. Cette pratique est conforme au DDD pour respecter les frontières d'aggregates et éviter le chargement excessif du graphe d'objets. Comme les données de la vue ne sont pas dans l'aggregate, un Read Model est nécessaire.

### 3. Eric Evans — Domain-Driven Design (2003)

> *"The MODEL in the domain layer should capture the essential concepts of the domain, not be shaped by the needs of the UI or infrastructure."*

Si on modifiait l'aggregate `Recrutement` pour exposer les champs nécessaires à la vue, le domaine serait contaminé par la présentation. Les Read Models dans l'application protègent le domaine de cette contamination.

### 4. Argument pragmatique : performance

Avec un Read Model, on peut écrire une requête ciblée :

```python
RecrutementModel.objects
    .filter(organisme_id=...)
    .select_related("offre")
    .prefetch_related("responsables_liaisons")
    .annotate(candidatures_total=Count("etapes__candidatures"))
# → Une seule requête SQL par table accédée
```

Cette approche est structurellement plus efficace que de charger un aggregate complet pour n'en utiliser que quelques champs.

### 5. Argument DRY

Le Read Model est défini **une seule fois** dans la couche application. Il sert à la fois :

- De type de retour pour le use case
- De type pour l'interface du query service
- De contrat typé entre l'application et la présentation

Sans lui, le typage serait perdu (`list[dict]`) ou la présentation devrait importer directement depuis l'infrastructure (violation de Clean Architecture).

## Consequences

### Positives

- **Séparation des responsabilités** : le modèle de lecture n'impacte pas le modèle d'écriture
- **Performance** : les requêtes de lecture sont optimisées pour les besoins de la vue
- **Domaine protégé** : l'aggregate n'est pas contaminé par des champs de présentation
- **Évolution découplée** : on peut modifier les Read Models sans changer l'aggregate, et vice-versa
- **Typage fort** : les Read Models sont des dataclasses typées, documentant exactement ce que la vue attend
- **DRY** : un seul fichier de types pour toutes les couches
- **Respect de la Dependency Rule** : la couche application ne dépend pas de l'infrastructure

### Négatives

- **Un fichier supplémentaire** : un fichier de ~40 lignes pour les Read Models
- **Risque d'Anemic Domain Model** si on étend trop les DTOs (Vernon nous met en garde)

## References

| Auteur | Ouvrage | Citation |
|---|---|---|
| Vaughn Vernon | *Implementing Domain-Driven Design* (2013), Ch. 14 | *"Services in that single layer are devoid of business domain logic. It will only serve to aggregate objects from each model into cohesive ones that the user interface needs."* |
| Vaughn Vernon | *Implementing Domain-Driven Design* (2013), Ch. 14 | *"Here the Application Services manage a merger of various DTOs, which mimic a sort of Anemic Domain Model."* |
| Vaughn Vernon | *Implementing Domain-Driven Design* (2013), Ch. 10 | Références par identifiant entre aggregates (principe général du chapitre) |
| Eric Evans | *Domain-Driven Design* (2003), Ch. 4 | *"The MODEL in the domain layer should capture the essential concepts of the domain, not be shaped by the needs of the UI or infrastructure."* |

## Notes

Cette décision ne concerne que les **queries** (lectures). Les **commandes** (écritures) continuent d'utiliser les aggregates du domaine via les repositories (`IRecrutementRepository`). Le pattern est cohérent avec les ADR précédentes :

- **ADR-003** (aggregate root pattern) : définit comment les aggregates protègent les invariants en écriture
- **ADR-004** (foreign keys & error mapping) : traite des contraintes d'intégrité entre bounded contexts
- **ADR-005** (business rule ownership) : établit que les règles métier vivent dans les entités du domaine
- **La présente ADR** : établit que les lectures n'utilisent pas les aggregates mais des Read Models dédiés qui sontdéfinies dans la couche application.
