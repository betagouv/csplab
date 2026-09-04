---
title: "DDR-002 : Ossature de page pilotée par la configuration"
created: 2026-07-23
status: accepté
---

## Contexte

Les écrans de l'ATS partagent la même ossature : en-tête (fil d'Ariane, titre,
sous-titre, actions, retour), barre d'onglets, contenu. Si chaque écran
réassemble cette ossature à la main, la logique se duplique, les écrans se
désynchronisent et dérivent visuellement.

## Décision

L'ossature de page est **détenue par des composants de layout**, pas recomposée
écran par écran. Un écran **déclare son intention** par configuration (« cette
page a un titre, un retour, deux onglets »).

- La structure (en-tête, onglets, contenu) et le **rythme spatial** sont portés
  par les composants de layout : l'en-tête est *full-bleed* et le contenu
  s'aligne sur une même gouttière, définie à un seul endroit.
- L'usage **par configuration** est le défaut. La **composition manuelle** reste
  possible, mais doit être l'exception, justifiée par un vrai besoin particulier.

## Alternatives considérées

- **Recomposer l'ossature dans chaque écran** : flexibilité maximale, mais
  duplication et dérive visuelle garanties à moyen terme.
- **Un composant de page monolithique fermé** : cohérent mais rigide ; aucune
  porte de sortie pour les écrans réellement atypiques.

## Conséquences

- Les écrans sont courts et déclaratifs ; l'ossature vit à un seul endroit.
- La cohérence spatiale entre écrans est acquise par construction.
- Un écran atypique fournit une exception explicite plutôt que de contourner le
  composant.
