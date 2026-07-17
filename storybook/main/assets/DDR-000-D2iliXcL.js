import{i as e}from"./preload-helper-Ct_ODC0V.js";import{a as t,o as n,s as r,y as i}from"./blocks-I9iJEQiC.js";import{s as a}from"./chunk-LITCR56V-B2DoJJcc.js";import{t as o}from"./mdx-react-shim-BvWfZu-H.js";var s,c=e((()=>{s=`---
title: "DDR-000 : Pourquoi des DDR (Design Decision Records)"
created: 2026-05-13
status: accepté
---

# DDR-000 : Pourquoi des DDR (Design Decision Records)

## Statut

Accepté

## Contexte

L'équipe souhaite s'appuyer sur un format analogue aux ADR (Architecture Decision Records), utilisés pour documenter les décisions d'architecture technique, afin d'expliciter et consigner certaines décisions de design qui structurent le frontend. Versionnée dans le repo mais aussi presentée dans un book, elles permettront d'être partagées avec les parties prenantes non techniques et de servir de référence pour les revues et les discussions d'implémentation.

## Décision

Nous adoptons un format **DDR** (Design Decision Record), calqué sur le format ADR mais
centré sur les décisions de design d'interaction, de composition de composants et d'ergonomie.

### Format d'un DDR

Chaque DDR est un fichier Markdown structuré avec les sections suivantes :
frontmatter YAML (\`title\`, \`created\`, \`status\`), puis les sections \`Statut\`, \`Contexte\`, \`Décision\`, \`Alternatives considérées\`, \`Conséquences\`.

### Ce qui relève d'un DDR

- Choix d'un pattern d'interaction
- Conventions de composition de composants
- Sémantique d'un élément visuel
- Décision d'ergonomie|

### Ce qui ne relève pas d'un DDR

- Les décisions réversibles sans coût significatif (couleur d'un bouton, libellé d'un label).
- Les détails d'implémentation purement techniques
- Les questions de stack

### Cycle de vie

Un DDR est créé **au moment de la décision**, pas a posteriori. Son statut évolue :

- **Proposé** — en discussion.
- **Accepté** — décision prise et appliquée.
- **Déprécié** — toujours en place mais plus recommandé pour les nouveaux développements.
- **Remplacé par DDR-XXX** — une décision ultérieure annule et remplace celle-ci.

## Alternatives considérées

### Ne rien formaliser

Rapide mais risque d'incohérence à moyen terme cohérences visuelles dégradent sans garde-fou documentaire.

### Wiki ou documentation séparée

Plus accessible pour les non-développeurs, mais découplé du code et du Storybook. Les DDR en Markdown vivent dans le repo, sont versionnés avec le code, et sont exposés directement dans le Storybook, un seul artefact de référence.

### Utiliser les ADR pour tout

Le format markdown versionné est peu consultable des parties prenantes non techniques, et les décisions de design d'interface sont plus nombreuses et plus légères que les décisions d'architecture technique.

## Conséquences

- Les décisions de design sont tracées, datées et référençables dans les tickets et les revues de code.
- Une story peut référencer un DDR pour expliciter les choix de design qui y sont appliqués.
`}));function l(e){return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(n,{title:`Système de design/DDR/DDR-000 : Pourquoi des DDR`}),`
`,(0,d.jsx)(t,{children:s})]})}function u(e={}){let{wrapper:t}={...i(),...e.components};return t?(0,d.jsx)(t,{...e,children:(0,d.jsx)(l,{...e})}):l(e)}var d;e((()=>{d=a(),o(),r(),c()}))();export{u as default};