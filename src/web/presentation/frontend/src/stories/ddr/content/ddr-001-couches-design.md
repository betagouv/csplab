---
title: DDR-001 — Couches de composition et frontières
created: 2026-05-12
status: accepté
---

## Contexte

Un design system accumule rapidement des dizaines de composants sans que leur niveau de composition soit toujours explicite. Plusieurs composants se retrouvent à la frontière entre des catégories. Il faut une grille de lecture stable, indépendante du framework UI sous-jacent et exprimable dans le Storybook.

## Décision

Sept couches de description du design sytem, de la plus atomique à la plus composite :

| Couche | Caractéristique distinctive |
|---|---|
| **01 Fondations** | Pas un composant : tokens, échelles, palettes, états transverses |
| **02 Atomes** | Une seule responsabilité, API plate (props scalaires), aucune connaissance du domaine |
| **03 Molécules** | Composition d'atomes via slots ou sous-composants, toujours générique |
| **04 Composants métier** | Atomes ou molécules spécialisés pour le domaine ATS (statuts, scores, étapes) |
| **05 Sections génériques** | Blocs fonctionnels d'une webapp métier, réutilisables hors ATS (sidebar, toolbar) |
| **06 Sections ATS** | Assemblages métier riches portant un cas d'usage complet (kanban, fiche) |
| **07 Vues ATS** | Pages assemblées, équivalent visuel d'une route |

### Critères de classement

- Un composant **monte** d'une couche en présence de certains indices, comme :
  - un slot nommé (atome → molécule),
  - une référence à un type métier (`Candidature`, `Offre`, `Etape`) - sauf wrapper trivial (molécule → composant métier),
  - une consommation directe d'un store Pinia (molécule → section),
  - un assemblage de plusieurs sections (section → vue).

### Frontière « générique vs ATS » pour les sections

Une section est **générique** si elle pourrait apparaître dans n'importe quelle webapp métier (`Sidebar`, `PageToolbar`, `BulkActionBar`). Elle est **ATS** si son rôle UX est spécifique au métier (`KanbanBoard` pour pipeline de recrutement, `EvaluationForm` pour notation post-entretien).

## Conséquences

- Toute story déclare son titre selon le pattern `NN - Couche/Catégorie/Composant`. La numérotation force l'ordre dans la sidebar Storybook.
- Le découpage facilite une migration future : les couches 01-03 sont les seules exposées théoriquement à un changement de framework. Les couches 04+ restent stables tant que la logique métier ne change pas.

## Alternatives écartées

- **Atomic design stricte (atoms / molecules / organisms / templates / pages)** - la frontière organisme/template est floue dans une webapp métier dense ; la distinction « générique webapp vs ATS » est plus utile au quotidien.
- **Découpage par feature uniquement** (`pipeline/`, `candidatures/`, `entretiens/`) - perd l'axe « échelle de composition », ce qui empêche de raisonner sur la réutilisation inter-features.
