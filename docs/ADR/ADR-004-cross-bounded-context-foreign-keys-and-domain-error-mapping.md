# ADR-004: FK Cross-Bounded Context, Intégrité Référentielle et Mapping d'Erreurs Domaine

## Status
Accepted

## Context

Dans une architecture DDD avec bounded contexts distincts (candidate, identite, referentiel),
les modèles ORM Django de chaque BC doivent parfois référencer des entités d'autres BCs.
Le cas concret est `CandidatureModel` (BC candidate) qui référence :
- `ProfilCandidatModel` (BC identite) via `candidat_id`
- `OfferModel` (BC referentiel) via `offre_id`

Deux besoins motivent ces références :
1. **Intégrité référentielle** : empêcher la création d'une candidature pour une offre ou un candidat inexistants
2. **Performance** : permettre les jointures ORM (`select_related`) pour éviter les requêtes
   N+1. Une vue affichant N candidatures avec leurs données d'offre ferait sinon N+1 requêtes
   DB séparées au lieu d'une seule requête JOIN. La foreign key (FK) est la condition préalable à `select_related`,
   et Django crée automatiquement un index sur la colonne FK pour que ce JOIN reste efficace.

La tension architecturale : les FK Django créent un couplage au niveau infrastructure entre bounded contexts.
Ce couplage est-il légitime ? Comment s'assurer qu'il reste en phase avec le domaine ?

## Decision

### 1. FK réelles en base de données avec `on_delete=PROTECT`

On utilise des vraies FK PostgreSQL (pas `db_constraint=False`) pour garantir l'intégrité
même si la couche applicative faillit. `PROTECT` est choisi : toute suppression d'une offre
ou d'un profil candidat ayant des candidatures associées est bloquée avec une erreur explicite.

```python
# CandidatureModel
candidat = models.ForeignKey(
    ProfilCandidatModel,
    to_field="utilisateur_id",  # UUID-as-string, identifiant métier du candidat
    on_delete=models.PROTECT,
    db_column="candidat_id",
    related_name="candidatures",
)
offre = models.ForeignKey(
    referentiel.OfferModel,
    on_delete=models.PROTECT,
    db_column="offre_id",
    related_name="candidatures",
)
```

### 2. Le couplage cross-BC en infrastructure reflète une règle métier — et doit la révéler

Le fait qu'une `Candidature` ne puisse pas exister sans un candidat réel et une offre réelle
**est une règle métier**, pas un détail technique. On choisit délibérément d'encoder cette
règle au niveau le plus fiable : la contrainte FK en base de données.

Ce couplage infra est **assumé et revendiqué**, pas caché. Son rôle est d'être la ligne de
défense la plus basse, qui s'applique même si la couche application faillit.

Mais une contrainte FK nue ne parle pas le langage du domaine — elle lève une `IntegrityError`
PostgreSQL. Le **repository** est la couche qui traduit cette réalité DB en connaissance domaine :

```python
# PostgresCandidatureRepository
except IntegrityError as e:
    # Violation FK 23503 → erreur domaine
    if "candidat_id" in detail:
        raise CandidatInexistant(candidature.candidat_id) from e
    if "offre_id" in detail:
        raise OffreInexistante(candidature.offre_id) from e
```

Ces erreurs domaine vivent dans `domain/candidate/exceptions/` et peuvent être interceptées
dans les usecases. La règle métier — implicite dans la FK — est ainsi **rendue explicite et
lisible** à travers le domaine.

### 3. Identité des entités cross-BC : `to_field` sur l'identifiant métier

En DDD, l'`entity_id` d'une entité est son identité universelle à travers tous les BCs.
Le même UUID identifie la même personne qu'elle soit `Utilisateur`, `Candidat`, ou auteur
d'une `Candidature`.

`ProfilCandidatModel` n'a pas de colonne UUID native. Son identifiant métier est
`username` (la valeur de `UserModel.username`, un UUID stocké en VARCHAR(36)).

On utilise `to_field="username"` pour pointer vers cet identifiant sémantique,
préservant ainsi la cohérence de l'identité DDD entre BCs. La colonne `candidat_id` en DB
est VARCHAR(36) plutôt que UUID natif.

La conversion est gérée dans les méthodes de mapping du modèle ORM uniquement — le domaine
ne change pas :

```python
def to_entity(self) -> Candidature:
    return Candidature.build(
        candidat_id=UUID(self.candidat_id),  # VARCHAR(36) → UUID, zéro requête DB
        offre_id=self.offre_id,              # UUID natif, pas de conversion
        ...
    )

@classmethod
def from_entity(cls, candidature: Candidature) -> "CandidatureModel":
    return cls(
        candidat_id=str(candidature.candidat_id),  # UUID → VARCHAR(36), zéro requête DB
        offre_id=candidature.offre_id,
        ...
    )
```

### 4. Accès direct à la valeur brute — aucune jointure dans le hot path

Django génère deux accesseurs pour une FK nommée `candidat` :
- `self.candidat_id` → valeur brute de la colonne (**aucune requête DB**)
- `self.candidat` → objet lié via JOIN (requête DB uniquement si accédé explicitement)

`to_entity()` et `from_entity()` utilisent exclusivement les accesseurs bruts. La FK est
disponible pour des `select_related` explicites dans les vues, sans jamais impacter le hot path.

## Rationale

### Les contraintes DB encodent les règles métier, le repository les révèle dans le domaine

Ce pattern inverse la logique habituelle qui consiste à "cacher" l'infrastructure. Ici,
l'infrastructure *encode activement* une règle métier (une candidature requiert un candidat
et une offre existants). Le repository ne cache pas cette contrainte — il la rend lisible dans
le langage du domaine via le mapping d'erreurs.

Cela garantit :
- **Defense in depth** : la règle est appliquée au niveau DB (infaillible) ET au niveau domaine
  (lisible par les développeurs)
- **Documentation vivante** : `CandidatInexistant` et `OffreInexistante` documentent explicitement
  les invariants du bounded context

### Couplage de migration acceptable dans un monolithe

Dans un monolithe Django déployé en une seule unité, le couplage des fichiers de migration
entre apps est géré automatiquement par Django via le graphe de dépendances. Ce couplage ne
deviendrait problématique que dans un contexte de déploiement indépendant des BCs.

## Consequences

### Positive
- **Intégrité garantie** : impossible de créer une candidature orpheline, même avec du code bugué
- **Règle métier révélée** : `OffreInexistante` et `CandidatInexistant` expriment des invariants
  métier dans le langage du domaine
- **Domaine intact** : `Candidature`, `ICandidatureRepository` ignorent totalement Django et les FK
- **Performance préservée** : aucune requête DB supplémentaire dans `to_entity()` / `from_entity()`
- **Identité cohérente** : le même UUID identifie le même candidat dans tous les BCs

### Negative
- **Type mismatch toléré** : `candidat_id` est VARCHAR(36) en DB au lieu de UUID natif
  (conséquence de `UserModel.username` en CharField)
- **Couplage infra** : les migrations Django du BC candidate dépendent des BCs identite et
  referentiel
- **Détection FK violée** : repose sur le SQLSTATE PostgreSQL (23503) et le `message_detail`
  psycopg2, qui sont stables mais spécifiques à PostgreSQL

### Neutral
- **Pattern réplicable** : FK infra + mapping repository + erreurs domaine s'applique à tout
  modèle nécessitant une référence cross-BC avec intégrité référentielle
