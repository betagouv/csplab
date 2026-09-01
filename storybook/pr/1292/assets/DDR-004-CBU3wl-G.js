import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{M as t,N as n,a as r,b as i,o as a,s as o}from"./blocks-BPs1W3_x.js";var s;function c(){return(c=e((()=>{s=`---
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
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(a,{title:`Système de design/DDR/DDR-004 : Pas de transitions décoratives`}),`
`,(0,d.jsx)(r,{children:s})]})}function u(e={}){let{wrapper:t}={...n(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=i(),t(),o(),c()})))()}f();export{u as default};