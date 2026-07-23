---
title: "DDR-004 : Pas de transitions décoratives"
created: 2026-07-23
status: accepté
---

## Contexte

- Plusieurs composants animaient leurs changements d'état par des transitions
décoratives, codées de manioère disparates dans les composants :
survol, repli de la barre latérale, rotation de chevron, etc..
- Le DSFR qui infuse notre design system ne repose sur quasiment aucune transition décorative.

## Décision

Les **transitions décoratives sont supprimées** : les changements d'état (hover, active) sont
**instantanés**.

Dans quelques rares exceptions (switch, toast), une animation réellement porteuse de sens
(guider l'attention, signaler une continuité), reste évaluable au cas par cas et ne relève pas de cette interdiction.

Si des transitions décoratives sont un jour amenées à être décidées, il faudra les configurer globalement
et les documenter dans le design system, plutôt que de les laisser se propager au fil de l'eau.

## Conséquences

- Interface plus nette et prévisible, sans latence perçue.
- Perte de l'affordance animée sur certains contrôles — assumée.
