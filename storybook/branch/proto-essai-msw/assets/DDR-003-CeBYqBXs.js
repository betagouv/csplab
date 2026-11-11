import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{a as t,o as n,s as r}from"./blocks-Bne63Cl1.js";import{s as i}from"./chunk-W22LQPXL-Dg9Nzqvg.js";import{i as a,r as o}from"./react-Bl2r1tuC.js";var s;function c(){return(c=e((()=>{s=`---
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
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(n,{title:`Système de design/DDR/DDR-003 : Stabilité visuelle au chargement`}),`
`,(0,d.jsx)(t,{children:s})]})}function u(e={}){let{wrapper:t}={...a(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=i(),o(),r(),c()})))()}f();export{u as default};