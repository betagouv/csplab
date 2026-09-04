import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{M as t,N as n,a as r,j as i,o as a,s as o}from"./blocks-DU5bsEVW.js";var s;function c(){return(c=e((()=>{s=`---
title: "DDR-003 : Stabilité visuelle au chargement"
created: 2026-07-23
status: accepté
---

## Contexte

Le contenu de certaines zones (titre, sous-titre, tableaux, listes) arrive de
façon asynchrone. Sans précaution, l'interface saute à l'arrivée des données
(*layout shift*) et les indicateurs de chargement clignotent d'un écran à
l'autre.

## Décision

La stabilité visuelle au chargement est un objectif de premier ordre, traité par conception :

- **Espace réservé** : une zone asynchrone occupe son emplacement *avant* l'arrivée de
  la donnée ; le contenu s'y insère sans déplacer le reste, car on aura anticipé
  la taille du contenu final, notamment par des hauteurs minimales.
- **Skeletons fidèles** : un indicateur de chargement reproduit la forme et la
  taille du contenu final.
- **Durée d'affichage minimale** : un skeleton reste visible assez longtemps
  pour éviter le clignotement, y compris quand la donnée arrive vite.

## Conséquences

- La navigation est sans saut ni clignotement.
- Les états de chargement sont conçus en même temps que l'état nominal.
- Les dimensions réservées doivent suivre l'évolution du contenu réel pour
  éviter un vide ou un débordement.
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(a,{title:`Système de design/DDR/DDR-003 : Stabilité visuelle au chargement`}),`
`,(0,d.jsx)(r,{children:s})]})}function u(e={}){let{wrapper:n}={...t(),...e.components};return n?(0,d.jsx)(n,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=n(),i(),o(),c()})))()}f();export{u as default};