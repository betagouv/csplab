import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{M as t,N as n,a as r,b as i,o as a,s as o}from"./blocks-BPs1W3_x.js";var s;function c(){return(c=e((()=>{s=`---
title: "DDR-006 : États d'exception des zones de données"
created: 2026-07-23
status: accepté
---

## Contexte

Une zone qui charge des données peut échouer ou n'avoir rien à afficher. Ces
situations étaient traitées au cas par cas : un texte brut ici, rien du tout
là.

## Décision

Une zone de données se conçoit avec ses quatre états : chargement, erreur,
vide, nominal.

- L'erreur s'affiche à l'endroit où le contenu était attendu, avec un
  encombrement comparable, et est annoncée aux technologies d'assistance.
- L'état vide dit ce qui est absent et, quand une action permet d'y remédier,
  la propose.
- La forme de ces états est la même dans toute l'application ; seuls les
  libellés changent, et ils parlent métier.

## Conséquences

- Une maquette ou un écran qui ne prévoit que l'état nominal est incomplet.
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(a,{title:`Système de design/DDR/DDR-006 : États d'exception des zones de données`}),`
`,(0,d.jsx)(r,{children:s})]})}function u(e={}){let{wrapper:t}={...n(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=i(),t(),o(),c()})))()}f();export{u as default};