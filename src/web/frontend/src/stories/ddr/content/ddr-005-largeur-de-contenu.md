---
title: "DDR-005 : Largeur de contenu des pages"
created: 2026-07-23
status: accepté
---

## Contexte

Le contenu des pages s'étirait sur toute la largeur disponible : lignes
illisibles sur grands écrans, colonnes latérales écrasées sur petits,
gouttières identiques de 1024px à 2560px. Les systèmes de référence
plafonnent leur contenu (Primer : 1280px, conteneur DSFR : 1248px).

## Décision

Chaque page choisit un régime de largeur ; aucune ne s'étire sans borne.

- **reading** (68rem) : contenus de gestion, formulaires, listes.
- **wide** (90rem, défaut) : surfaces denses, tableaux multi-colonnes.
- **full** : réservé aux surfaces à défilement interne (kanban).

Les gouttières s'adaptent à la taille de l'écran. Les seuils de mise en page
réagissent à la largeur réellement disponible pour le contenu, pas à celle du
viewport : une page se réorganise de la même façon que la place manque à
cause de l'écran ou d'un panneau ouvert. Les colonnes latérales (aside,
callout) passent sous le contenu principal au seuil de 64rem.

Pas de grille numérique : les mises en page multi-colonnes se décrivent en
régions (contenu principal, aside) qui se réorganisent au seuil.

## Conséquences

- Une nouvelle page déclare son régime de largeur.
- Les composants larges gèrent leur débordement par défilement interne,
  jamais par débordement de page.
- Les valeurs des bornes sont centralisées ; un ajustement de doctrine ne
  touche aucun écran.
