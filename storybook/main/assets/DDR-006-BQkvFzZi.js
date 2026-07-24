import{i as e}from"./preload-helper-Ct_ODC0V.js";import{a as t,o as n,s as r,y as i}from"./blocks-z20IZeGz.js";import{s as a}from"./chunk-LITCR56V-BaK8unLH.js";import{t as o}from"./mdx-react-shim-DHqcVG7s.js";var s,c=e((()=>{s=`---
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
`}));function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(n,{title:`Système de design/DDR/DDR-006 : États d'exception des zones de données`}),`
`,(0,d.jsx)(t,{children:s})]})}function u(e={}){let{wrapper:t}={...i(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;e((()=>{d=a(),o(),r(),c()}))();export{u as default};