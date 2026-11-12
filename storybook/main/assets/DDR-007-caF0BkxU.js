import{n as e}from"./rolldown-runtime-sJBDdmOt.js";import{M as t,N as n,a as r,j as i,o as a,s as o}from"./blocks-BMzR7YlN.js";var s;function c(){return(c=e((()=>{s=`---
title: "DDR-007 : Un seul dessin par rôle"
created: 2026-11-11
status: proposé
---

## Contexte

Quand chaque composant choisit les valeurs qui le dessinent, un même type d'élément, comme un champ de formulaire, reçoit des dessins différents d'un composant à l'autre. Changer le dessin de ce type d'élément demande alors de retrouver chaque composant qui le dessine.

## Décision

L'interface est faite de rôles. Un rôle est un type d'élément que plusieurs composants dessinent, comme un champ de formulaire, un bloc encadré ou un filet à l'intérieur d'un bloc.

Un rôle a le même dessin dans tous les composants qui le dessinent. On nomme un rôle quand au moins deux composants le dessinent.

Un dessin différent pour un même rôle est un choix de design : on le décide avec des captures des composants concernés.

## Conséquences

- On change le dessin d'un rôle en un seul endroit, et tous les composants qui le dessinent prennent le nouveau dessin.
- Un nouveau composant reprend le dessin d'un rôle existant avant d'en proposer un autre.
`})))()}function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(a,{title:`Système de design/DDR/DDR-007 : Un seul dessin par rôle`}),`
`,(0,d.jsx)(r,{children:s})]})}function u(e={}){let{wrapper:n}={...t(),...e.components};return n?(0,d.jsx)(n,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;function f(){return(f=e((()=>{d=n(),i(),o(),c()})))()}f();export{u as default};