import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{a as t,o as n,s as r}from"./blocks-Bne63Cl1.js";import{s as i}from"./chunk-W22LQPXL-Dg9Nzqvg.js";import{i as a,r as o}from"./react-Bl2r1tuC.js";var s;function c(){return(c=e((()=>{s=`---
title: "DDR-004 : Mouvement réglé par rôle"
created: 2026-07-23
status: accepté
---

## Contexte

- Plusieurs composants animaient leurs changements d'état par des transitions codées de manière disparate : survol, repli de la barre latérale, rotation de chevron.
- Le DSFR, sur lequel repose notre design system, n'emploie presque pas de transitions.
- Le 27 octobre 2026, l'équipe a retenu le mouvement et les ombres du kit de La Suite numérique, essayés dans un prototype de thèmes, pour rendre l'interface plus conviviale.

## Décision

Le mouvement de l'interface signale un changement d'état ou une continuité : survol, ouverture d'un menu, d'un dialogue ou d'un panneau, dépôt d'une carte du kanban. On le règle globalement, par rôle, dans les variables \`--csp-motion-*\` de \`src/styles/csp-variables.css\`, avec les durées et les courbes du kit de La Suite numérique. La notification garde sa propre animation d'entrée et de sortie.

Quand le système demande un mouvement réduit, on coupe les animations et les transitions. Le contour de la carte déposée reste, parce qu'il montre où la carte est arrivée. Le balayage qui ferme une notification reste aussi, parce qu'il suit le geste de la personne.

## Conséquences

- Un thème change le mouvement de tous les rôles en redéfinissant ces variables.
- Un nouveau composant animé lit une variable de rôle existante, ou en ajoute une dans \`csp-variables.css\`.
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(n,{title:`Système de design/DDR/DDR-004 : Mouvement réglé par rôle`}),`
`,(0,d.jsx)(t,{children:s})]})}function u(e={}){let{wrapper:t}={...a(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=i(),o(),r(),c()})))()}f();export{u as default};