import{i as e}from"./preload-helper-Ct_ODC0V.js";import{a as t,o as n,s as r,y as i}from"./blocks-CfxKHqI8.js";import{s as a}from"./chunk-LITCR56V-BZt4lqKh.js";import{t as o}from"./mdx-react-shim-B7kYLE1B.js";var s,c=e((()=>{s=`---
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
`}));function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(n,{title:`Système de design/DDR/DDR-002 : Ossature de page configurée`}),`
`,(0,d.jsx)(t,{children:s})]})}function u(e={}){let{wrapper:t}={...i(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;e((()=>{d=a(),o(),r(),c()}))();export{u as default};