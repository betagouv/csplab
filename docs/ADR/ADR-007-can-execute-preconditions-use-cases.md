# ADR-007 : `can_execute` — préconditions de coordination des use cases

**Status:** Proposal — Amended by ADR-009
**Date:** 2026.08.18
**Deciders:** Élodie R
**Tags:** ddd, application, architecture

---

> ⚠️ **Amendée par [ADR-009](./ADR-009-idiomatic-django-switch.md)**. Voir la section « Impact sur les ADR existantes » d'ADR-009.

## Context

Les use cases de commande (écritures) doivent valider qu'une commande est possible et
cohérente **avant** de coordonner les agrégats. Deux familles de vérifications se
présentent :

1. **Droits / permissions** (contexte utilisateur) — `est_autorise(...)`
2. **Cohérence de coordination** (multi-agrégats + états impossibles) —
   ex. `organisme != recrutement.organisme` → `OrganismeRecrutementIncoherents`,
   ou `organisme.etapes is None` → fail-fast

Le problème : où placer ces vérifications, et comment éviter que le use case ne
devienne une **béquille** qui compense un invariant métier non garanti à la source ?

---

## Decision

### 1. Les préconditions de coordination vivent dans la couche application

Le use case expose une méthode unique `can_execute(command)` qui, dans l'ordre :

1. charge les agrégats (via les repositories),
   _(obsolète : accès direct via `QuerySet`, cf. [ADR-009 §1](./ADR-009-idiomatic-django-switch.md#1-le-queryset-est-le-contrat-entre-les-couches))_
2. vérifie la **cohérence de coordination** (multi-agrégats et fail-fast),
3. vérifie les **droits / permissions**,
4. **lève** une erreur si une vérification échoue,
5. retourne le contexte (agrégats chargés) pour `execute`.

### 2. Cohérence et droits restent ensemble dans `can_execute`

Pas de séparation en deux méthodes. Les deux familles valident la même pré-condition
de coordination et s'exécutent **avant toute mutation**. L'ordre est logique et constant
d'un use case à l'autre.

### 3. Ne jamais muter dans `can_execute`

Un garde ne **répare jamais** (ex. initialiser les étapes ici). Le fail-fast doit
**lever** (`raise`) plutôt que réparer silencieusement, pour révéler l'état incohérent.

### 4. Ne pas y déplacer les invariants d'un seul agrégat

`can_execute` valide la **coordination**, pas les règles métier d'un agrégat.
Un invariant (ex. « un organisme ATS a des étapes ») est posé **à la création** dans le
domaine (ADR-003 / ADR-005), déclenché par son use case dédié
(`InitializeOrganismeStepsUsecase`). Si un `etapes is None` subsiste en aval, c'est un
**fail-fast de cohérence applicative** (état corrompu / bug), pas une règle métier.

> 🔗 Les renvois à ADR-003/ADR-005 ci-dessus et ci-dessous pointent des ADR superseded —
> voir désormais [ADR-009 §3 « Doctrine des invariants »](./ADR-009-idiomatic-django-switch.md#3-doctrine-des-invariants--remplace-ladr-005).
> Le principe (`can_execute` en tête de service, sans lien à `IUsecase`) reste valide,
> cf. [tableau « Impact »](./ADR-009-idiomatic-django-switch.md#impact-sur-les-adr-existantes).

---

## Rationale

| Principe | Source | Application |
|---|---|---|
| La couche application coordonne sans logique métier | Vernon *IDDD* (2013), Ch. 14 (cf. ADR-006) | Guards de précondition dans `can_execute` |
| Les invariants vivent dans le domaine | Evans *DDD* (2003), Ch. 4 (cf. ADR-006) | Le fail-fast n'est pas un invariant : il est posé à la création |
| Le use case vérifie avant de coordonner | Vernon *IDDD* (2013), Ch. 14 | `can_execute` = gatekeeper |
| Préconditions explicites qui lèvent | Meyer, *Design by Contract* (1997) | `raise` plutôt que réparer silencieusement |

---

## Consequences

### Positives

- Rôle clair et constant du use case : `can_execute` (préconditions) → `execute` (coordination)
- Fail-fast : les états incohérents sont révélés (erreur + audit), pas masqués
- Pas de béquille : les invariants restent dans le domaine

### Negatives

- Discipline requise : rien d'impératif n'empêche un garde de muter ou de compenser
  un invariant (convention + tests, cf. ADR-003 / ADR-005)
- `can_execute` fait plusieurs choses (charger + vérifier) — acceptable tant que
  le use case reste simple

### Neutres

- Pattern réplicable à tous les use cases de commande
