# Notes — proto/tableau-de-bord

## Composant partagé modifié

- **`CspSidebarItem.vue`** : `inheritAttrs: false` était posé sans jamais rebinder `$attrs` quelque part dans le template, donc un `@click` passé à `<CspSidebarItem>` sans prop `to` (navigation pilotée par JS plutôt que par une vraie route) était silencieusement perdu. Ajouté `v-bind="$attrs"` sur le `<Primitive>` interne. Sans impact sur l'usage existant (`CspAppShell.vue`, seul consommateur, passe toujours `to`). Nécessaire ici : la nav du proto change de page via un état local (`page` dans `AtsShell.vue`), pas via de vraies routes.

Points à discuter côté intégration :

## Données manquantes au modèle actuel

- **Réf. RenoiRH** : le schéma API expose `reference_csp` (`RecrutementsActifs.reference_csp`), pas de champ RenoiRH. Le repère cité en test utilisateur (priorité 5 du brief) n'existe pas encore côté backend — à clarifier si RenoiRH est une référence externe à ajouter, ou si `reference_csp` doit être présenté autrement.
- **Service / direction** : absent de `RecrutementsActifs` / `RecrutementsArchives` (seul `responsables` existe, une liste de noms). Nécessaire pour l'identification sans ambiguïté d'un recrutement (priorité 5) — à ajouter au modèle si le produit veut l'afficher au-delà de ce prototype.
- **« Mes tâches »** : fonctionnalité entièrement absente du code actuel (`src/web/presentation/frontend/src/features/` n'a pas de dossier tâches). Le prototype mocke `TacheDashboard` avec `libelle`, `recrutementId`, `candidatNom`, `echeanceStatut`, `assigneA`, `fait` — à valider côté produit/backend si ce sujet est repris pour une session ATS dédiée (assignation, qui peut créer une tâche, notifications…).

## Pattern réutilisé, à envisager comme évolution de composant

- **Carte cliquable sans `href`** : `CspCard` ne propose de style « cliquable » (curseur, hover, focus) que via la prop `href` (rendu `<a>`). Dans ce proto, `RecrutementCard` s'appuie sur le fallthrough d'attributs (`@click`, `role="button"`, `tabindex`) + une classe locale pour simuler l'état cliquable sans navigation réelle. Si ce pattern (carte cliquable pilotée par JS plutôt que par une vraie URL) revient souvent dans l'ATS, il vaudrait le coup d'ajouter une prop type `onClick` / `clickable` à `CspCard` plutôt que de le refaire à chaque fois.

## Ce qui a bien fonctionné tel quel

- `CspMetaList` pour la ligne d'identification (réf. / service / type de contrat) — correspond exactement au besoin de la priorité 5, aucune adaptation nécessaire.
- `CspBadge type="new"` pour le tag « nouveaux CV », `CspSidebar*` pour la navigation à 3 entrées + profil en bas — repris tels quels.
