# ADR-013 : Granularité et nommage des écrans du front

**Statut:** Proposé
**Date:** 2026.11.17
**Decideurs:** Équipe front
**Tags:** conventions, naming, frontend

---

## Contexte

Le code emploie page, vue, section, onglet et panneau sans définition commune, et un même mot désigne des choses différentes :

- `View` nomme aussi bien une page, un onglet, un mode d'affichage (kanban, liste) qu'un tiroir.
- `Section` nomme aussi bien un onglet, le corps d'une page, une partie d'un onglet qu'une zone de la barre latérale.
- Un composant que le routeur monte est rangé tantôt dans `views/`, tantôt dans `components/`.

Les onglets routés suivent trois modèles :

1. une route enfant par onglet, qui monte son propre composant dans le `<router-view>` du parent (organisme, recrutement) ;
2. deux routes qui montent la même page, qui lit l'onglet dans `meta` (recrutements actifs et archivés) ;
3. huit routes qui montent toutes `CandidaturePanelView`, qui affiche lui-même l'onglet demandé.

Le troisième modèle explique la taille du panneau, qui porte le contenu de tous ses onglets. L'[ADR-012](ADR-012-frontend-testing-strategy.md) monte directement « le composant qu'une route affiche » : la règle ne s'applique que si on sait reconnaître ce composant.

## Options Considérées

1. Un glossaire, sans toucher au code : les mots sont définis, mais les fichiers continuent de dire autre chose.
2. Un suffixe par rôle (`Page`, `Tab`, `Panel`) : précis, mais presque tous les écrans changent de nom, et un onglet promu en page change encore de nom.
3. Le routeur tranche : tout composant monté par une route est un écran, rangé dans `views/` et suffixé `View`. Son rôle se lit dans l'arbre des routes. Les autres composants sont nommés par leur forme.

## Décision

Option 3.

Un **écran** est un composant que le routeur monte. Il est rangé dans le dossier `views/` de sa feature et son nom finit par `View`. Son rôle dépend de sa place dans l'arbre des routes :

- **Page** : montée par une route sous le shell.
- **Onglet** : monté par une route enfant dans le `<router-view>` d'une page ou d'un panneau.
- **Panneau** : monté par une route enfant qui ouvre un tiroir au-dessus de la page, qui reste montée dessous.

Tout autre composant de feature est rangé dans `components/` et son nom ne finit jamais par `View`.

Un onglet routé est toujours une route enfant qui monte son propre écran : le parent affiche `<router-view />` et ne choisit pas lui-même le contenu de l'onglet.

Les définitions des rôles et des suffixes vivent dans [`frontend_conventions.md`](../frontend_conventions.md), sections « Component Naming » et « Routing ».

On migre en deux temps : une PR de déplacements et de renommages, sans changement de comportement, puis une PR par écran à découper, en commençant par le panneau de candidature.

## Conséquences

- Le dossier dit comment tester un composant, au sens de l'ADR-012 : un écran de `views/` se monte directement, un composant de `components/` se teste par l'écran qui l'ouvre, sauf s'il a un contrat propre ou des branches coûteuses à atteindre.
- `routes.test.ts` peut vérifier que le nom de chaque composant monté par `routes.ts` finit par `View`.
- Les onglets rangés dans `components/` deviennent des écrans de `views/`.
- `CandidaturePanelView` et `RecrutementsView` se découpent en un écran par onglet. Le parent garde ce que ses onglets partagent : le tiroir, l'en-tête et la navigation pour le panneau, la requête et l'état d'erreur pour les recrutements.
- Les noms qui emploient `View` ou `Section` dans un autre sens sont renommés.

## Points ouverts
- **Préfixe `Csp`** : les conventions le prévoient aussi pour des composants métier (`CspCandidatCard`), mais aucun composant de feature ne le porte. À aligner sur le code : `Csp` est réservé à `components/`.
