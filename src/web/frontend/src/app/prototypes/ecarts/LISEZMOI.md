# Écarts du kit

Prototype Storybook sous `Prototypes/Écarts du kit`. Chaque écart a une story par état et une planche qui affiche ces stories côte à côte. Chaque story d'option pose un attribut `data-ecart` sur `<html>`, et `ecarts.css` contient les surcharges de chaque valeur de cet attribut. Les chemins partent de `src/web/frontend/src/` et les lignes sont celles de `main` au 11 novembre 2026.

## Couches proches

Valeurs actuelles :

- `components/base/CspSelect/CspSelect.vue:263`, `border-radius: 0.25rem`, liste de la liste déroulante.
- `components/base/CspCombobox/CspCombobox.vue:223`, `border-radius: 0.25rem`, liste de la combobox.
- `components/base/CspTooltip/CspTooltip.vue:68`, `border-radius: 0.25rem`, infobulle.
- `components/base/CspDropdownMenu/CspDropdownMenu.vue:71`, `.csp-dropdown`, sans rayon.
- `components/base/CspPopover/CspPopover.vue:55`, `.csp-popover`, sans rayon.
- `components/base/CspToast/CspToast.vue:157`, `.csp-toast`, sans rayon.

Pour tout mettre à `0.25rem` (`couches-tout-arrondi`), on ajoute `border-radius: 0.25rem` dans les trois règles sans rayon. La règle `.csp-toast` a déjà `overflow: hidden`, et sa bordure gauche de 4 px suit l'arrondi.

Pour tout mettre à angles droits (`couches-tout-droit`), on retire les trois déclarations `border-radius: 0.25rem`.

## Blocs encadrés

Valeurs actuelles :

- `components/base/CspCard/CspCard.vue:136`, `--csp-card-radius: 0.25rem`, lu à la ligne 129.
- `components/base/CspSortableList/CspSortableListItem.vue:181`, `border-radius: 0.25rem`, sur `.csp-sortable-list-item__content`.
- `components/base/CspSkeleton/CspSkeletonSortableList.vue:87`, `border-radius: 0.25rem`, squelette de la liste triable.
- `features/agents/components/AgentRechercheForm.vue:96`, `border-radius: 0.25rem`, cadre de l'agent trouvé.
- `components/base/CspDataTable/CspDataTable.vue:456`, `.csp-table-wrapper`, bordure à la ligne 458, sans rayon.
- `components/base/CspSkeleton/CspSkeletonTable.vue:83`, bordure du squelette de tableau, sans rayon.
- `features/candidatures/components/CandidatureDocuments.vue:149`, bordure de `.candidature-documents__list`, sans rayon.
- `features/messages/components/MessagesSection.vue:146` et `features/messages/components/NewConversationForm.vue:190`, bordures de cadre, sans rayon.

La scène reproduit le cadre de `.candidature-documents__list` dans `.ecarts-blocs__list`, car ce cadre appartient à une feature.

Pour tout mettre à `0.25rem` (`blocs-tout-arrondi`), on ajoute `border-radius: 0.25rem` à `.csp-table-wrapper`, au squelette de tableau et aux trois cadres des features. `.csp-table-wrapper` a déjà `overflow: hidden`.

Pour tout mettre à angles droits (`blocs-tout-droit`), on passe `--csp-card-radius` à `0` et on retire les trois autres `border-radius: 0.25rem`.

## Couches modales

Valeurs actuelles :

- `components/base/CspDialog/CspDialog.vue:163`, `border-radius: 0.25rem`, dialogue.
- `components/base/CspDrawer/CspDrawer.vue:193`, `.csp-drawer`, sans rayon.
- `components/layout/CspSidebar/CspSidebar.vue:153`, `.csp-sidebar--mobile`, sans rayon.

Pour mettre le dialogue à angles droits (`modales-dialogue-droit`), on retire `CspDialog.vue:163`.

## Contrôles

Valeurs actuelles :

- `components/base/CspSegmentedControl/CspSegmentedControl.vue:119`, `border-radius: 0.25rem`, cadre.
- `components/base/CspSegmentedControl/CspSegmentedControl.vue:145`, `border-radius: 0.25rem`, segment.
- `components/base/CspSegmentedControl/CspSegmentedControl.vue:159`, `border-radius: 0.25rem`, fond de survol du segment.
- `components/base/CspButton/CspButton.vue:59`, `.csp-btn`, sans rayon, pour toutes les variantes.

Pour mettre le contrôle segmenté à angles droits (`controles-segmente-droit`), on retire les trois déclarations de `CspSegmentedControl.vue`.

Pour mettre les boutons à `0.25rem` (`controles-boutons-arrondis`), on ajoute `border-radius: 0.25rem` à `.csp-btn`, `CspButton.vue:59`.

## Bouton de repli de la barre latérale

Valeurs actuelles :

- `components/layout/CspSidebar/CspSidebar.vue:216`, `border-radius: 0.375rem`, bouton de repli.
- `components/layout/CspSidebar/CspSidebar.vue:227`, `background: var(--background-default-grey-hover)`, survol du bouton de repli.
- `components/layout/CspSidebar/CspSidebarItem.vue:61`, `.csp-sidebar-item`, sans rayon ; survol à la ligne 91, `var(--background-alt-grey-hover)`, appui à la ligne 95, `var(--background-alt-grey-active)`.
- `components/layout/CspSidebar/CspSidebarButton.vue:62`, survol `var(--background-alt-grey-hover)` ; appui à la ligne 66, `var(--background-alt-grey-active)`.

Sur le fond de la barre latérale, `var(--background-alt-grey)` à `CspSidebar.vue:146`, le survol actuel du bouton de repli donne en thème clair `rgb(246, 246, 246)`, la couleur de ce fond.

Pour dessiner le bouton de repli comme ses voisins (`repli-comme-ses-voisins`), on retire `CspSidebar.vue:216`, on remplace la valeur de `CspSidebar.vue:227` par `var(--background-alt-grey-hover)` et on ajoute un état `:active` sur `var(--background-alt-grey-active)`.

La scène affiche le survol du bouton de repli, d'un élément et du bouton de l'utilisateur sans pointeur, par la classe `ecarts-survol`, qui reprend les valeurs de survol ci-dessus.

## Gris neutres

Valeurs actuelles :

- `components/base/CspSkeleton/CspSkeleton.vue:29`, `background: var(--background-alt-grey)`, squelette par défaut.
- `components/base/CspSkeleton/CspSkeletonTable.vue:102`, `var(--background-contrast-grey)`, squelette dans l'en-tête et le pied du tableau.
- `components/base/CspSkeleton/CspSkeletonKanban.vue:81`, `var(--background-contrast-grey)`, squelette dans l'en-tête d'une colonne.
- `components/base/CspAvatar/CspAvatar.vue:56`, `var(--background-contrast-grey)`.
- `components/base/CspBadge/CspBadge.vue:90`, `--badge-default-bg: var(--background-contrast-grey)`.
- `components/base/CspTag/CspTag.vue:172`, `var(--background-contrast-grey)`.
- `features/candidatures/components/CandidatureActivitesList.vue:127`, `var(--background-alt-grey)`, disque de l'icône d'une activité.

Pour poser le squelette par défaut sur le gris des avatars et des badges (`gris-squelette-contraste`), on remplace la valeur de `CspSkeleton.vue:29` par `var(--background-contrast-grey)`. Les surcharges de `CspSkeletonTable.vue:102` et `CspSkeletonKanban.vue:81` deviennent alors identiques à la valeur par défaut et peuvent être retirées.

## Cases et boutons radio

Valeurs actuelles :

- `components/base/CspCheckbox/CspCheckbox.vue:152`, `border: 1px solid var(--border-action-high-blue-france)`.
- `components/base/CspRadio/CspRadio.vue:103`, `border: 1px solid var(--border-action-high-blue-france)`.
- `features/candidatures/components/ChangerEtapeDrawer.vue:255`, même bordure, bouton radio du choix d'étape.
- `components/base/CspInput/CspInput.vue:112`, `--csp-input-border: var(--border-default-grey)`.
- `components/base/CspTextarea/CspTextarea.vue:106`, `--csp-textarea-border: var(--border-default-grey)`.
- `components/base/CspSelect/CspSelect.vue:155`, `box-shadow: inset 0 0 0 1px var(--border-default-grey)`.

Une case cochée garde sa bordure `--border-active-blue-france` (`CspCheckbox.vue:160`), comme un bouton radio coché (`CspRadio.vue:109`).

Pour une bordure grise sur les cases et les boutons radio (`cases-bordure-grise`), on remplace `var(--border-action-high-blue-france)` par `var(--border-default-grey)` dans les trois déclarations. Les états coché, erreur et désactivé gardent leurs règles.
