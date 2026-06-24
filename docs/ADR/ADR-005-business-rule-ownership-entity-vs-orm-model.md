# ADR-005: Responsabilité des règles métier — entité de domaine vs modèle ORM

## Status
Accepted

## Context

Dans notre architecture DDD, une même donnée existe sous deux formes :
- une **entité de domaine** (ex. `Source` dans `libs/referentiel`), pure, sans Django, qui porte les invariants métier ;
- un **modèle ORM Django** (ex. `SourceModel` dans `infrastructure/django_apps/`), qui porte la persistance.

Par exemple, l'entité `Source` encode une règle métier dans son `__post_init__` : une source de type `TALENTSOFT` doit obligatoirement renseigner ses quatre champs `client_id_*` / `base_url_*`, sinon `MissingTalentsoftFieldsError` est levée.

Le problème : **le modèle ORM offre plusieurs chemins d'écriture, et tous ne passent pas par l'entité.**

- Le chemin « formulaire » (admin Django, `ModelForm`) appelle `full_clean()`, qui appelle à son tour `clean()`. `Model.clean()` délègue à `to_entity()`, donc la règle de l'entité est bien exécutée.
- Mais `Model.objects.create(...)`, `instance.save()` (sans `full_clean()`) et surtout `Model.objects.bulk_create([...])` **court-circuitent `clean()`** et écrivent en base une source incohérente (ex. une `TALENTSOFT` sans `base_url`).

Deux tentations à écarter :
1. **Ne rien valider hors du formulaire** : on persiste des données qui violent un invariant.
2. **Ré-encoder la règle dans le modèle** (dans `save()`, un `CheckConstraint`, un validateur) : la règle métier existe alors à deux endroits, qui dérivent inévitablement l'un de l'autre.

La question : **qui est responsable du contrôle des règles métier, et comment garantir que ce contrôle ne soit ni dupliqué, ni contournable ?**

## Decision

### 1. L'entité de domaine est l'unique propriétaire des règles métier

Les invariants métier sont encodés **une seule fois**, dans l'entité (`__post_init__`, value objects, méthodes de domaine). Le modèle ORM ne ré-implémente **aucune** règle métier : il ne connaît que la persistance (types de colonnes, `unique`, `null`, longueurs).

### 2. Le modèle ne valide pas — il *route* vers l'entité

Quand le modèle a besoin d'exposer la validation métier à un chemin Django (typiquement la validation de formulaire), il ne duplique pas la règle : il **construit l'entité** et laisse celle-ci échouer, puis traduit l'erreur de domaine en erreur Django.

```python
# SourceModel.clean()
def clean(self) -> None:
    try:
        self.to_entity()                       # la règle vit dans l'entité
    except MissingTalentsoftFieldsError as e:
        raise ValidationError(e.message) from e  # traduction domaine → Django
```

`clean()` est un **confort UX** (afficher une erreur propre dans un formulaire), pas la ligne de défense. Il ne faut jamais s'y reposer pour garantir l'intégrité, car `save()` / `create()` / `bulk_create()` ne l'appellent pas.

### 3. La garantie réelle : toute écriture métier passe par `from_entity()`

La seule manière fiable de garantir qu'un invariant est respecté est de **forcer le passage par le constructeur de l'entité**. On construit toujours l'entité d'abord (ce qui exécute `__post_init__`), puis on mappe vers le modèle via `from_entity()` :

```python
source = Source(type=SourceType.TALENTSOFT, ...)   # __post_init__ valide ici
model = SourceModel.from_entity(source)            # mapping pur, déjà validé
model.save()
```

Si l'entité est invalide, l'exception est levée **avant** toute écriture : il est structurellement impossible d'atteindre `from_entity()` avec une entité incohérente.

> **Note — pourquoi « construire l'entité » suffit à valider.** La garantie repose sur le contrat des dataclasses : `__post_init__` est appelé automatiquement par le `__init__` généré, donc **tout `Source(...)` rejoue les invariants**. Ce n'est pas un nom arbitraire (le renommer le rendrait silencieux) et ce n'est pas non plus infaillible : seuls les chemins qui passent par `__init__` le déclenchent. `Source(...)`, `to_entity()` et `dataclasses.replace()` l'exécutent ; un `object.__new__` + affectation directe, ou `@dataclass(init=False)`, le contourneraient. Nos deux chemins sont sûrs : `to_entity()` fait un `Source(...)` classique, et `from_entity()` reçoit une entité déjà construite (donc déjà validée).

**Règle d'écriture** : le code métier (repositories, use cases, admin) ne fait jamais `Model.objects.create(...)` ni `bulk_create([...])` avec des données métier brutes. Il construit des entités validées puis appelle `from_entity()`. Le `create()`/`bulk_create()` brut reste réservé aux données purement techniques sans invariant (logs, agrégations…).

### 4. L'admin Django fait partie de la couche de présentation

L'admin n'est pas un outil neutre de manipulation de la base : c'est une **interface de présentation** et il doit respecter les frontières de couches au même titre qu'une vue DRF. Pour `Source` (et tout modèle portant des invariants métier), trois niveaux selon le besoin :

| Besoin                                              | Décision admin                                                         |
| --------------------------------------------------- | ---------------------------------------------------------------------- |
| Aucun intérêt d'exploitation à créer l'instance     | **Bloquer la création** : `has_add_permission(...) => False`            |
| Création nécessaire, règles **simples**             | Forcer le passage par `from_entity()` (construire l'entité dans `save_model`) |
| Création nécessaire, règles **complexes**           | Forcer la réutilisation d'un **use case** (via le container DI)        |


```python
# Cas "règles simples" : l'admin route via l'entité
def save_model(self, request, obj, form, change):
    source = obj.to_entity()          # invariants garantis
    obj = SourceModel.from_entity(source)
    super().save_model(request, obj, form, change)

# Cas "règles complexes" : l'admin invoque le use case
def save_model(self, request, obj, form, change):
    container = create_ingestion_container()
    container.create_source_use_case().execute(...)
```

## Rationale

### Une seule source de vérité, validée au plus près de la donnée

Encoder la règle uniquement dans l'entité évite le « double encodage » et sa dérive inévitable. Le modèle, le formulaire et l'admin ne sont que des **chemins d'accès** à cette unique règle ; ils la déclenchent via la construction d'entité, ils ne la copient pas.

C'est cohérent avec l'ADR-004 : là, la règle métier (« pas de candidature orpheline ») est encodée au niveau le plus fiable (la contrainte FK) et *révélée* dans le domaine par le repository. Ici, la règle (« une Talentsoft est complète ») est encodée au niveau le plus expressif (l'entité) et *appliquée* à chaque écriture par le passage obligé via `from_entity()`. Dans les deux cas : une seule définition, plusieurs points qui la révèlent ou l'appliquent, aucune duplication.

### `clean()` est un filet UX, pas une garantie

S'appuyer sur `clean()` pour l'intégrité est un faux ami : Django ne l'appelle qu'au sein de la validation de formulaire. `save()`, `create()` et `bulk_create()` l'ignorent. On clarifie donc son rôle (UX) et on déplace la garantie réelle sur le constructeur d'entité, qu'aucun chemin ne peut contourner.

### L'admin est une couche de présentation, pas une porte dérobée

Traiter l'admin comme un client de présentation (et non comme un accès SQL privilégié) évite qu'il devienne le trou dans la raquette qui écrit des données invalides. Les trois niveaux (bloquer / `from_entity()` / use case) graduent l'effort selon le besoin réel, sans jamais autoriser une écriture qui ne respecte pas les invariants.

## Consequences

### Positives
- **Règle unique** : l'invariant n'existe qu'à un seul endroit — l'entité.
- **Écriture infranchissable** : impossible de persister une entité incohérente dès lors que toute écriture passe par `from_entity()`.
- **Modèle mince** : le modèle Django reste un mapping de persistance, sans logique métier.
- **Admin discipliné** : l'admin respecte les couches et ne contourne plus les invariants.

### Negatives
- **Discipline requise** : rien dans Django n'empêche techniquement un développeur d'écrire `Model.objects.create(...)`. La règle « toujours passer par `from_entity()` » repose sur la convention, la revue et les tests (cf. ADR-003, même limite sur l'encapsulation Python).
- **Plus de code dans l'admin** : surcharger `save_model()` (ou bloquer l'ajout) est plus  verbeux qu'un `ModelAdmin` par défaut.
- **`bulk_create` perd la validation** : les imports de masse doivent construire les entités en amont (et donc renoncer à l'écriture en lot naïve) ou accepter explicitement le compromis pour des données sans invariant.

### Neutres
- **Pattern réplicable** : « invariant dans l'entité + `clean()` qui route + écriture via `from_entity()` + admin discipliné » s'applique à tout modèle ORM adossé à une entité de domaine portant des règles métier.
