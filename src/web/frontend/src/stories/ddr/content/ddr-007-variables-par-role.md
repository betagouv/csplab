---
title: "DDR-007 : Variables CSS nommées par rôle"
created: 2026-10-19
status: proposé
---

## Contexte

Les composants lisaient directement les jetons du DSFR et des valeurs écrites en dur. Pour changer une décision d'interface, comme la couleur des colonnes du kanban ou le rayon des champs, il fallait retrouver chaque composant qui la portait.

## Décision

On nomme les variables CSS du kit sur trois niveaux.

- Primitives : les jetons du DSFR, dans `src/styles/dsfr-tokens-options.css` et `dsfr-tokens-decisions.css`, et les échelles du kit (`--csp-space-*`, `--csp-font-size-*`, `--csp-shadow-*`).
- Rôles, déclarés dans `src/styles/csp-variables.css` : `--csp-<rôle>-<propriété>`, avec l'état en dernier (`-hover`, `-drag`, `-current`, `-disabled`). La valeur d'un rôle est une primitive ou un autre rôle.
- Variables de composant : `--csp-<composant>-<partie>-<propriété>`, comme `--csp-kanban-column-padding`. Celles qu'on règle depuis l'extérieur du composant sont déclarées dans `csp-variables.css`, les autres dans le composant.

Les rôles désignent ces éléments :

- `canvas` : le fond de la page.
- `chrome` : l'en-tête de page, le fond de sa barre d'onglets et la barre du haut sur téléphone.
- `nav` : la barre latérale de navigation.
- `region` : une zone qui regroupe des cartes, comme une colonne du kanban.
- `aside` : la colonne secondaire d'un panneau, comme la colonne de droite du panneau de candidature.
- `surface` : un bloc encadré, comme une carte, un tableau ou le cadre d'un document.
- `raised` : une carte qu'on déplace, comme une carte du kanban ou un élément d'une liste triable.
- `overlap` : une couche posée près de son déclencheur, comme une liste de choix, un menu, une infobulle ou une notification.
- `lifted` : une couche modale, comme un dialogue, un tiroir ou la barre latérale sur téléphone.
- `divider` : un filet à l'intérieur d'un bloc.
- `neutral` : le fond gris d'un badge, d'une étiquette, d'un avatar ou d'un squelette de chargement.
- `action` : le rayon des boutons et des éléments de la barre latérale, et les couleurs du bouton secondaire.
- `field` : les champs de formulaire et la barre de recherche.
- `control` : le bouton tertiaire et le contrôle segmenté.
- `indicator` : la case à cocher et le contour de focus du tri d'un tableau.
- `text-<rôle>` : les textes, du titre de page à la légende.
- `category-<catégorie>` : les catégories d'étape d'un recrutement.
- `message` : les encarts et les notifications.

Un composant lit un rôle quand la valeur a le même sens ailleurs dans l'interface, et une variable de composant quand elle lui est propre. Un composant qui propose plusieurs tailles garde ses propres tailles de texte.

Quand le kit dessine un rôle avec des valeurs différentes selon les composants, on déclare le rôle avec la valeur `initial`, et chaque composant donne sa propre valeur en repli de `var()`. Donner une seule valeur à ce rôle change l'apparence des composants qui le lisent : on le décide dans une PR de design, captures à l'appui.

On applique un thème sur la racine de la page. Il redéfinit des variables déclarées dans `csp-variables.css` et des jetons de décision du DSFR, jamais un jeton d'option du DSFR ni une variable déclarée dans un composant.

## Conséquences

- Les rôles déclarés `initial` dans `csp-variables.css` signalent les écarts du kit.
- Un nouveau composant reprend un rôle existant avant de déclarer une variable à lui.
