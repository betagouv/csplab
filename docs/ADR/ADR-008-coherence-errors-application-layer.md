# ADR-008 : Erreurs de cohérence applicative dans la couche application

**Status:** Proposal
**Date:** 2026.08.18
**Deciders:** Élodie R
**Tags:** ddd, application, architecture, errors

---

## Context

Les use cases de commande lèvent des erreurs de deux natures différentes :

1. **Erreurs de règle métier** : un invariant violé par une saisie légitime et récupérable. Ex. `ConfigurationEtapesInvalide`, `ModificationEtapesImpossible`.

Elles sont levées par le **domaine** (invariants, `@mutate`) et représentent des flux métier que l'interface doit savoir gérer.

2. **Erreurs de cohérence applicative** : un état « should never happen » — bug ou données corrompues. Ex. un organisme ATS sans étapes par défaut
(`organisme.etapes is None`). Elles sont levées par la **couche application** (le use case, dans `can_execute`, cf. ADR-007).

La question : où ranger ces erreurs de cohérence applicative ?

---

## Decision

### 1. Les erreurs de cohérence applicative vivent dans la couche application

Elles sont placées dans la couche **application**, distinctes des erreurs de règle
métier du **domaine**. Une base commune est définie en application
(ex. `UsecaseError` / `ApplicationError` dans `application/`).

### 2. Le domaine n'expose que les erreurs de règle métier

Le domaine porte les invariants et les flux métier récupérables ; il n'a pas à connaître les gardes « should never happen » de la coordination. Cela garde le domaine purement métier (cf. ADR-003, ADR-005, ADR-006) et le débarrasse des préoccupations
d'état corrompu.

### 3. La dépendance est respectée

La couche application importe le domaine (normal, Clean Architecture), mais le domaine n'importe jamais l'application. Les erreurs de cohérence ne montant pas dans le domaine, aucune dépendance circulaire n'est créée.

---

## Rationale

| Principe | Source | Application |
|---|---|---|
| L'Application Layer gère coordination, sécurité, transactions | Vernon *IDDD* (2013), Ch. 14 | Les erreurs de coordination et leurs gardes y vivent |
| Le domaine n'est pas modelé par des besoins externes | Evans *DDD* (2003), Ch. 4 | Les gardes "should never happen" ne le contaminent pas |
| Dependency Rule : le domaine ignore l'application, l'inverse non | Uncle Bob, *Clean Architecture* | L'application connaît le domaine ; aucun cycle |
| Précondition = contrat d'appel | Meyer, *Design by Contract* (1997) | La précondition appartient à la frontière applicative |

---

## Consequences

### Positives

- **Debug plus clair** : une erreur d'application dans la bonne couche décrit le contexte d'exécution du use case, sans se confondre avec les règles métier que l'UI doit gérer.
- **Domaine épuré** : il ne porte que les invariants et flux métier, pas les états corrompus.
- **Séparation des responsabilités** : erreurs récupérables (domaine) ≠ erreurs "should never happen" (application).

### Negatives

- **Base d'erreurs applicatives supplémentaire** à définir et maintenir.
- **Cohérence** : certaines erreurs de coordination existent déjà dans le domaine (ex. `OrganismeRecrutementIncoherents`). Leur migration est optionnelle et se fera par une passe dédiée.

### Neutres

- Pattern réplicable : chaque use case définit ses erreurs de coordination dans `application/`, à côté du use case qui les lève.

---

## Référence

Ce choix s'appuie sur l'ADR-007 (`can_execute`), qui pose que les préconditions de
coordination et leurs erreurs vivent dans la couche application.
