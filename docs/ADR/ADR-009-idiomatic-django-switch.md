# ADR-009 : Retour à un Django idiomatique — abandon de la clean architecture stricte

**Status:** Accepté
**Date:** 2026.09.02
**Deciders:** Vincent P
**Tags:** django, architecture, refactoring, supersedes

---

## Context

Le service `src/web` applique depuis ses débuts une clean architecture stricte : quatre
couches (`domain`, `application`, `infrastructure`, `presentation`) adossées à une
bibliothèque maison `libs/ddd` (`AggregateRoot`, `Entity`, `IUsecase`, `IRepository`,
`IMapper`, `IPage`, `UnitOfWork`), avec injection de dépendances par
`dependency-injector`.

### Ce que cette architecture coûte, mesuré sur `main`

| Élément | Volume |
|---|---|
| `domain/` | 112 fichiers / 1 979 LOC |
| `application/` | 73 fichiers / 2 417 LOC |
| `infrastructure/` | 290 fichiers / 14 145 LOC |
| Interfaces de repository (`Protocol`) | 22, pour 22 implémentations uniques |
| Mappers ORM ↔ entité | 14 |
| Fichiers DI (containers + factories) | 11 |
| Agrégats portant du comportement | 6, pour 11 méthodes |
| **Dont méthodes encodant un invariant réel** | **5** |

Soit environ 4 400 LOC de `domain` + `application` pour cinq règles métier. Le reste est
de la traduction entre représentations et de la déclaration de providers.

### Les symptômes

1. **Revues longues.** Le layering n'est *enforced* par aucun outil — il n'existe aucun
   contrat `import-linter` dans le dépôt. Les frontières sont tenues à la main, en revue,
   par des humains.
2. **Impacts nombreux.** Un endpoint touche huit artefacts dans quatre couches : entité,
   `Protocol`, implémentation `Postgres*`, mapper, use case, provider, read model,
   serializer.
3. **Abstractions sans contrepartie.** Aucun des 22 `Protocol` de repository n'a jamais eu
   deux implémentations. Une abstraction se paie par la substituabilité qu'elle procure ;
   celle-ci n'en procure aucune.
4. **Bus factor de 1.** Les conventions du dépôt (`@factory`, `@mutate`,
   `__init_subclass__` policier dans `AggregateRoot`) exigent un savoir maîtrisé par une
   seule personne, qui quitte le projet.

### Le signal déjà présent dans nos propres ADR

L'ADR-005 reconnaît, dans ses conséquences négatives, que sa règle centrale « toute
écriture passe par `from_entity()` » **repose sur la convention, la revue et les tests**,
et que « rien dans Django n'empêche techniquement un développeur d'écrire
`Model.objects.create(...)` ».

Ce coût de discipline, accepté à l'époque, est devenu le coût principal. Et
l'accumulation de dette a produit une garantie plus faible que celle que l'ADR-004
obtenait gratuitement avec une contrainte FK.

---

## Decision Drivers

- Réduire le nombre d'artefacts touchés par un changement fonctionnel.
- Rendre les frontières d'architecture vérifiables par la CI plutôt que par la revue.
- Ne perdre aucun invariant métier, et si possible en renforcer la garantie.
- Ramener le codebase dans un vocabulaire connu de toute l'équipe et embauchable.
- Ne pas geler la livraison pendant la transition.

---

## Considered Options

1. **Option A — Statu quo + montée en compétence de l'équipe.**
   Conserve l'existant, transfère le savoir avant le départ.
2. **Option B — Alléger le DDD.**
   Conserver les agrégats et les read models, supprimer les `Protocol` de repository
   et la DI.
3. **Option C — Django idiomatique, couches conservées sans abstraction entre elles.**
   Les `QuerySet` transitent des managers vers les vues via les services ; DRF seul
   sérialise ; suppression de `libs/ddd`, des mappers et de la DI.
4. **Option D — Django « plein ».**
   Fat models et vues, suppression de la couche `application`.

**Option retenue : C.**

L'option A ne traite aucun des quatre symptômes : elle transforme un problème
d'architecture en problème de recrutement. L'option B laisse en place les agrégats —
donc les mappers, donc la moitié du coût — pour six classes dont cinq méthodes portent
une règle. L'option D supprime la couche `application`, qui est justement le seul point
de passage obligé pour le RBAC, la transaction et l'audit : ce serait échanger notre
problème de verbosité contre un problème de sécurité.

---

## Decision

### 1. Le `QuerySet` est le contrat entre les couches

Les services retournent des `QuerySet[Model]`, que la vue consomme directement. On ne les
convertit pas en liste et on ne les enveloppe pas : la pagination DRF a besoin de
`count()` et du slicing.

La construction des querysets (`select_related`, `prefetch_related`, `annotate`) vit dans
un `QuerySet` custom sur le modèle, exposé par `objects = XQuerySet.as_manager()`. Le
service compose deux ou trois méthodes ; il ne devient pas une usine à querysets.

### 2. Le `Model` Django est l'entité

Une seule représentation par notion métier. Les mappers `to_domain` / `from_domain`
disparaissent, ainsi que la règle `from_entity()` de l'ADR-005.

### 3. Doctrine des invariants — remplace l'ADR-005

Un invariant est encodé au **mécanisme d'application le plus fort disponible**, dans cet
ordre :

1. **Contrainte de base de données** (`UniqueConstraint`, `CheckConstraint`,
   `on_delete=PROTECT`) — infaillible, y compris pour `bulk_update` et l'admin.
2. **Méthode de modèle ou de manager** — contournable par `.objects.update()`, donc
   réservée aux règles sans équivalent en base.
3. **Fonction pure** appelée par le service — pour les règles portant sur une collection
   ou une séquence, qu'aucune contrainte SQL n'exprime.
4. **Garde de service** — pour ce qui exige le contexte d'appel (permissions,
   orchestration multi-agrégats).

C'est l'inverse de l'ADR-005, qui plaçait l'entité comme propriétaire unique de tous les
invariants. C'est en revanche la **généralisation de l'ADR-004**, qui avait déjà retenu
la contrainte FK comme « ligne de défense la plus basse, qui s'applique même si la couche
application faillit ».

Application aux cinq invariants existants :

| # | Invariant | Mécanisme cible | Statut |
|---|---|---|---|
| I1 | Étape non supprimable si candidatures | `on_delete=PROTECT` | déjà garanti |
| I2 | Dossier de candidature ≥ 1 document | méthode `CandidatureModel.soumettre()` | niveau 2 |
| I3 | Pas de double soumission | `UPDATE` conditionnel atomique, puis contrainte | à trancher, cf. Notes |
| I4 | Déplacement confiné au recrutement | filtre de queryset sur la chaîne de FK | déjà garanti |
| I5 | Séquence d'étapes bien formée | fonction pure `etapes_rules.py` | niveau 3 |

### 4. DRF est seul responsable de la sérialisation — amende l'ADR-006

Le principe de séparation lecture / écriture est conservé : les besoins d'un tableau de
bord (compteurs agrégés, `Max(updated_at)`) ne sont pas ceux d'un agrégat. Seule
l'implémentation change — `QuerySet` custom + `ModelSerializer` avec `source=`, au lieu
de query service + read model dataclass.

### 5. La traçabilité passe par un appel explicite — amende l'ADR-003

`AuditLogWriter.log_action()` est appelé explicitement par le service après écriture. Les
domain events et `drain_events()` sont supprimés. On n'introduit **pas** de signal Django
en remplacement : ce serait réintroduire l'implicite qu'on cherche à retirer, et perdre
l'identité de l'utilisateur auteur de l'action.

### 6. Suppression de l'injection de dépendances

Les vues et les services importent directement ce dont ils ont besoin. Les containers
`dependency-injector` et leurs factories sont supprimés.

### 7. Les frontières sont vérifiées par la CI, pas par la revue

- Deux contrats `import-linter` : sens unique `presentation` → `application` →
  `infrastructure` ; interdiction de `rest_framework` et `django.http` dans
  `application`.
- Un contrôle refusant `.objects.` dans `presentation/` — c'est-à-dire une vue qui
  requête. Le *type* du modèle, lui, reste importable par la présentation : c'est la
  contrepartie assumée du transit de queryset.
- Un contrôle refusant `patch("presentation…")`, `patch("application…")` et
  `patch("infrastructure.di…")` dans `tests/`.

Corollaire : **ce qu'on ne peut pas outiller, on ne l'écrit pas comme règle
d'architecture.**

---

## Rationale

### Une abstraction se paie par la substituabilité qu'elle procure

Vingt-deux `Protocol` pour vingt-deux implémentations : le prix a été payé, la
contrepartie jamais encaissée. L'ORM Django *est* déjà la couche d'abstraction sur
PostgreSQL ; nous en avions empilé une seconde par-dessus.

### L'invariant le plus solide est celui que le code ne peut pas contourner

L'ADR-005 confiait les invariants à l'entité, en reconnaissant que rien n'empêchait de
l'esquiver. Trois de nos cinq invariants sont déjà, ou deviennent, des garanties de base
de données — plus fortes que ce que l'agrégat offrait. Le cas d'I3 est éclairant : le
`read-then-check` de `Candidature.soumettre_candidature()` est racé, là où un `UPDATE`
conditionnel ne l'est pas.

### Le découpage vertical faisait le gros du travail, pas le DDD

La navigabilité du code et la capacité à travailler à plusieurs viennent des bounded
contexts et des use cases nommés en français métier — pas des agrégats ni des mappers.
Ces deux acquis sont conservés intégralement.

### Le coût est déjà payé, la dette non

Six agrégats, cinq règles. Un d'entre eux (`Note`) est **déjà court-circuité par son
propre repository**, qui écrit via `.update()` sans passer par le mapper. Nous maintenons
donc un formalisme que le code lui-même n'honore plus.

---

## Consequences

### Positives

- **Diff par changement fonctionnel divisé** : quatre artefacts au lieu de huit, dans un
  seul bounded context.
- **Frontières vérifiées automatiquement** : la revue se recentre sur le métier.
- **Invariants renforcés** : trois des cinq reposent sur des garanties de base de données.
- **Codebase embauchable** : Django/DRF plutôt qu'un dialecte DDD maison.
- **Faux positifs de tests supprimés par construction** : sans read model intermédiaire,
  un test de vue ne s'écrit plus qu'avec `APIClient` et une vraie base.
- **Typage assaini** : les 23 `type: ignore[attr-defined]` actuels, presque tous liés au
  remapping manuel d'annotations, disparaissent avec lui.

### Negatives

- **Perte du point d'entrée unique.** `.objects.update()` et `bulk_update()`
  court-circuitent toute règle écrite en Python. C'est précisément le risque que
  l'ADR-005 identifiait déjà, et la raison pour laquelle les invariants remontent vers la
  base.
- **Le RBAC devient le point de vigilance n°1.** `est_autorise()` était l'unique barrière,
  au sein du use case. Il est doublé d'un scoping de queryset (`.visibles_par(user)`) pour
  qu'un oubli dans une vue ne puisse pas ouvrir de fuite de données.
- **Les tests reposant sur des mocks d'interfaces sont à réécrire.** Portée limitée : trois
  fichiers utilisent `create_interface_aware_mock`.
- **Un lot de tests de vues est à reconstruire avant migration.** Neuf fichiers de
  `tests/presentation` patchent un container et ne constituent pas un harnais de
  non-régression.
- **Coût de transition non nul** : six étapes, une PR par bounded context.

### Neutres

- **Les couches restent.** `presentation` / `application` / `infrastructure` conservent
  leur rôle et leur sens de dépendance. Seules les abstractions entre elles disparaissent.
- **Les enums / value objects restent** où ils sont, déjà consommés comme `choices` par
  les modèles Django.
- **`libs/referentiel` n'est pas concerné** : c'est un shared kernel entre `web` et
  `ingestion`, orthogonal à ce choix.

---

## Impact sur les ADR existantes

Deux ADR sont remplacées, cinq sont conservées ou amendées : la présente décision
resserre le périmètre du DDD, elle n'annule pas le travail d'architecture antérieur.

| ADR | Devenir |
|---|---|
| ADR-001 — Testing strategy | **Amendée.** Trois niveaux (fonctions pures / service+DB / vue+DB) au lieu d'un découpage par couche. |
| ADR-002 — Repository mocking | **Amendée.** Le découpage à trois niveaux et le principe « factories plutôt que fixtures JSON » sont conservés. Seule tombe la stratégie de mocking par interface : `create_interface_aware_mock` est supprimé, et les tests de use case deviennent des tests de service sur base réelle. |
| ADR-003 — Aggregate root pattern | **Superseded.** |
| ADR-004 — FK cross-BC et mapping d'erreurs | **Conservée et généralisée.** Sa doctrine (« encoder la règle au niveau le plus fiable ») devient la règle générale, section Decision §3. |
| ADR-005 — Business rule ownership | **Superseded.** Décision inversée. |
| ADR-006 — CQRS et read models | **Amendée.** Principe conservé, implémentation remplacée. |
| ADR-007 — `can_execute` | **Amendée.** Les préconditions restent en tête de service ; seule la signature liée à `IUsecase` disparaît. |
| ADR-008 — Erreurs de cohérence applicative | **Conservée.** La couche application demeure. |

---

## Notes

### Trois points à acter

1. **I3 — décision produit.** Le domaine lève
   `CandidatureDejaSoumise(candidat_id, offre_id)` tandis que `CandidatureModel.Meta`
   porte `UniqueConstraint(candidat_id, etape_id)`. Les deux règles se contredisent, et la
   contradiction préexiste à cette ADR. Si la règle est « par offre », il faut dénormaliser
   un `offre_id` sur `CandidatureModel` — une `UniqueConstraint` ne traverse pas les
   relations.
2. **I5 — connaissance métier.** `OrganismeRecruteur._validate()` dit *quoi* ; le *pourquoi*
   n'est écrit nulle part, ni le comportement attendu pour les recrutements en cours
   lorsqu'un organisme modifie sa séquence.
3. **I1 — vérification.** `EtapeRecrutement.delete()` lève dès que
   `_candidatures is not None`, donc y compris sur une liste vide, là où `PROTECT` ne
   bloque que s'il existe des lignes. L'un des deux comportements est un défaut.

### Migration

Progressive, un bounded context par PR, jamais deux en vol : socle outillé → filet de
tests `APIClient` + `db` **avant** migration → `recruteur` lecture → `recruteur` écriture →
`identite` → `candidate` → `ingestion` → suppression de `libs/ddd`.

Garde-fou de non-régression : le passage des read models aux serializers ne doit produire
**aucun diff** sur `schema.yaml` et `internal-schema.yaml`, que la CI vérifie déjà.

Pendant la transition, les deux styles cohabitent. Le code neuf suit la présente ADR ;
l'ancien n'est migré que lorsque c'est le tour de son contexte, ou lorsqu'une évolution
fonctionnelle l'impose — pas au détour d'un passage dans le fichier.

