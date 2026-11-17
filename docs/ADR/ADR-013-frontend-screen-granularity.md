# ADR-013 : Granularité et nommage des écrans du front

**Statut:** Proposé
**Date:** 2026.11.17
**Decideurs:** Équipe front
**Tags:** conventions, naming, frontend

---

## Contexte

Le code emploie page, vue, section, onglet et panneau sans définition commune, et un même mot désigne des choses différentes :

- `View` nomme une page (`RecrutementView`), un onglet (`ActivitesTachesView`, `CandidaturesTabView`), un mode d'affichage (`CandidaturesKanbanView`, `CandidaturesListeView`) et un tiroir (`CandidaturePanelView`).
- `Section` nomme un onglet (`EquipeRecrutementSection`, `OrganismeAgentsSection`, `TagsSection`), le corps d'une page (`OrganismesSection`), le contenu d'un onglet du panneau (`MessagesSection`) et une zone de la barre latérale (`ORGANISME_SECTION_ROUTE_NAMES`).
- Un composant que le routeur monte est rangé tantôt dans `views/`, tantôt dans `components/`. `EtapesRecrutementList` est un onglet nommé comme une liste.

Les onglets routés suivent trois modèles :

1. une route enfant par onglet, qui monte son propre composant dans le `<router-view>` du parent (organisme, recrutement) ;
2. deux routes qui montent la même page, qui lit l'onglet dans `meta` (recrutements actifs et archivés) ;
3. huit routes qui montent toutes `CandidaturePanelView`, qui affiche lui-même l'onglet demandé.

Le troisième modèle explique la taille du panneau : 495 lignes, une quarantaine d'imports, le contenu de tous ses onglets. L'[ADR-012](ADR-012-frontend-testing-strategy.md) monte directement « le composant qu'une route affiche » : la règle ne s'applique que si on sait reconnaître ce composant.

## Options Considérées

1. Un glossaire, sans toucher au code : les mots sont définis, mais les fichiers continuent de dire autre chose.
2. Un suffixe par rôle (`Page`, `Tab`, `Panel`) : précis, mais presque tous les écrans changent de nom, et un onglet promu en page change encore de nom.
3. Le routeur tranche : tout composant monté par une route est un écran, rangé dans `views/` et suffixé `View`. Son rôle se lit dans l'arbre des routes. Les autres composants sont nommés par leur forme.

## Décision

Option 3.

Un **écran** est un composant que le routeur monte. Il est rangé dans le dossier `views/` de sa feature et son nom finit par `View`. Son rôle dépend de sa place dans l'arbre des routes :

| Rôle | Monté par | Exemple |
|---|---|---|
| Page | une route sous le shell ; affiche `CspPageContainer` | `RecrutementView` |
| Onglet | une route enfant, affichée dans le `<router-view>` d'une page ou d'un panneau, qu'on la choisisse par des onglets ou par un sélecteur (kanban / liste) | `ActivitesTachesView` |
| Panneau | une route enfant qui ouvre un `CspDrawer` au-dessus de la page, qui reste montée dessous | `CandidaturePanelView` |

Une page ou un panneau fixe le titre du document, un onglet ne le fait pas. Un écran ne monte pas un autre écran, sauf par `<router-view>`, et sauf les pages d'erreur de `views/` (`ForbiddenView`, `NotFoundView`), qu'une page affiche à la place de son contenu.

Tout autre composant de feature est rangé dans `components/`, et son nom ne finit jamais par `View`. Les formes courantes ont leur suffixe :

| Suffixe | Ce que c'est |
|---|---|
| `Section` | un bloc d'un écran, non routé |
| `Dialog`, `Drawer`, `Popover` | un conteneur qu'un écran ouvre |
| `Form` | un formulaire placé dans un tiroir, un popover ou un dialogue |
| `List`, `Card`, `Column`, `Cell` | un élément de liste, de tableau ou de kanban |

Un composant qui n'a pas de forme listée garde un nom qui dit ce qu'il fait (`CandidaturesToolbar`, `TagPicker`).

Un onglet routé est toujours une route enfant qui monte son propre composant : le parent affiche `<router-view />` et ne choisit pas lui-même le contenu de l'onglet. Les sous-routes d'un onglet (`notes/nouvelle`, `messages/nouveau`, `messages/:conversationUuid`) sont des routes enfants de cet onglet.

On migre en deux temps : une PR de déplacements et de renommages, sans changement de comportement, puis une PR par écran à découper, en commençant par le panneau de candidature.

Dans [`frontend_conventions.md`](../frontend_conventions.md), les tableaux ci-dessus remplacent la ligne « Page/View » de « Component Naming », et la phrase de « Routing » qui permet à une route de monter un onglet depuis `components/` disparaît.

## Conséquences

- Le dossier dit comment tester un composant, au sens de l'ADR-012 : un écran de `views/` se monte directement, un composant de `components/` se teste par l'écran qui l'ouvre, sauf s'il a un contrat propre ou des branches coûteuses à atteindre.
- `routes.test.ts` peut vérifier que le nom de chaque composant monté par `routes.ts` finit par `View`.
- Les onglets rangés dans `components/` deviennent des écrans :

  | Aujourd'hui | Devient |
  |---|---|
  | `equipe-recrutement/components/EquipeRecrutementSection` | `equipe-recrutement/views/EquipeRecrutementView` |
  | `organismes/components/OrganismeAgentsSection` | `organismes/views/OrganismeAgentsView` |
  | `tags/components/TagsSection` | `tags/views/TagsView` |
  | `etapes-recrutement/components/EtapesRecrutementList` (onglet de l'organisme) | `etapes-recrutement/views/OrganismeEtapesView`, qui affiche `EtapesRecrutementSection` |

  `EtapesRecrutementList` est aussi affiché par `OffreEtapesRecrutementView`. Il reste donc un composant, renommé `EtapesRecrutementSection`, et l'onglet de l'organisme devient un écran mince qui l'affiche.
- `CandidaturePanelView` garde le tiroir, l'en-tête, la navigation entre candidatures, la liste des onglets et la colonne de suivi, qu'il affiche ou masque selon l'onglet de la route. Chaque onglet devient un écran (`CandidatureCvView`, `CandidatureHistoriqueView`, `CandidatureDocumentsView`, `CandidatureNotesView`, `CandidatureMessagesView`), qui se teste seul.
- `RecrutementsView` (426 lignes) se découpe aussi en `RecrutementsActifsView` et `RecrutementsArchivesView`. Les deux onglets partagent une requête et un état d'erreur : la page les garde.
- « View » étant réservé aux écrans, le mode kanban / liste s'appelle « layout » dans le code : `CANDIDATURES_VIEW_ROUTE_NAMES` devient `CANDIDATURES_LAYOUT_ROUTE_NAMES`, `CandidaturesViewName` devient `CandidaturesLayoutName` et `CandidaturesViewSwitch` devient `CandidaturesLayoutSwitch`. L'interface garde « vue kanban » et « vue liste ».
- « Section » étant réservé à un bloc non routé, `ORGANISME_SECTION_ROUTE_NAMES` devient `ORGANISME_NAV_ROUTE_NAMES` : ces routes ne servent qu'au `match` des `NavItem` de `app/navigation.ts`.

## Points ouverts
- **Préfixe `Csp`** : les conventions le prévoient aussi pour des composants métier (`CspCandidatCard`), mais aucun composant de feature ne le porte. À aligner sur le code : `Csp` est réservé à `components/`.
