import{j as e,b as o,M as i}from"./index-Jlxhkxsv.js";import{useMDXComponents as r}from"./index-CxB4NT9C.js";import"./iframe-mwOhdPVH.js";import"./index-8_2S3kac.js";const a=`---
title: "DDR-001 : Niveaux de composition et frontières"
created: 2026-05-12
status: accepté
---

## Contexte

Le système de design, le Storybook et l'organisation du code doivent partager une même grille de lecture, sans confondre trois sujets distincts :

- l'architecture technique (primitives Reka UI, composants Vue) ;
- l'organisation du code source (\`shared\`, \`features\`, \`views\`) ;
- le niveau de composition des composants dans Storybook.

Il faut une taxonomie courte, compréhensible par une équipe mixte design/dev, et adaptée au domaine ATS.

## Décision

Le système de design est décrit selon deux axes.

### Axe principal : niveau de composition

| Niveau | Caractéristique distinctive |
|---|---|
| **01 Fondations** | Pas un composant : tokens, palettes, échelles, grilles, etc. |
| **02 Éléments** | Unité visuelle ou interactionnelle consommée comme telle |
| **03 Compositions** | Organisation de plusieurs éléments pour porter un rôle fonctionnel identifiable |
| **04 Écrans** | Assemblage final correspondant à une vue complète |

### Axe secondaire : portée

- **Générique** : réutilisable hors ATS, sans types, vocabulaire ni comportements métier.
- **ATS** : ancré dans le domaine recrutement par son nom, ses props, ses types ou son comportement.

L'axe secondaire s'applique aux **Éléments** et aux **Compositions**. Cette distinction est pragmatique pour le périmètre actuel : le besoin concret est de distinguer le générique du spécifique ATS. Une catégorie intermédiaire comme \`Domaine recrutement\` pourrait être introduite si des composants réellement partagés entre plusieurs contextes frontaux apparaissent.

### Exemples

| Catégorie | Exemples |
|---|---|
| **01 Fondations** | \`Tokens\`, \`Colors\`, \`Spacing\` |
| **02 Éléments/Générique** | \`Button\`, \`Badge\`, \`Dialog\` |
| **02 Éléments/ATS** | \`OffreStatusBadge\`, \`CandidateStateTag\`, \`ScoreIndicator\` |
| **03 Compositions/Générique** | \`Sidebar\`, \`PageToolbar\`, \`BulkActionBar\` |
| **03 Compositions/ATS** | \`KpiCard\`, \`CandidateDrawer\`, \`KanbanBoard\` |
| **04 Écrans/ATS** | \`DashboardView\`, \`PipelineView\`, \`CandidateListView\` |

### Storybook

Les titres suivent le pattern \`NN - Niveau/Portée/Composant\`.

Exemples :
- \`01 - Fondations/Tokens\`
- \`02 - Éléments/Générique/Button\`
- \`02 - Éléments/ATS/OffreStatusBadge\`
- \`03 - Compositions/Générique/Sidebar\`
- \`03 - Compositions/ATS/KanbanBoard\`
- \`04 - Écrans/ATS/PipelineView\`

### Organisation du code

L'arborescence source reste idiomatique Vue et pilotée par l'ownership :

- \`shared/components/\` pour les composants génériques partagés,
- \`features/*/components/\` pour les composants ATS liés à une feature,
- \`views/\` pour les écrans.

La hiérarchie des dossiers n'a pas à refléter exactement la taxonomie Storybook ; elle doit seulement rester cohérente avec elle.

## Conséquences

- Le Storybook, le système de design et le code source partagent le même vocabulaire.
- L'axe \`Générique / ATS\` répond au besoin actuel sans anticiper des frontières métier qui ne sont pas encore stabilisées.

## Alternatives écartées

- **Atomic design stricte** : trop de niveaux et trop d'arbitrages atome/molécule.
- **Axe secondaire \`Générique / Domaine recrutement / ATS\` dès maintenant** : plus prospectif que nécessaire à ce stade ; sans cas d'usage concret partagé hors ATS, il introduit surtout des débats de classement.
- **Découpage par feature uniquement** : bon pour l'ownership, insuffisant pour décrire l'échelle de composition.
- **Taxonomie calquée sur les dossiers** : crée des collisions de vocabulaire entre architecture technique, code source et système de design.
`;function s(n){return e.jsxs(e.Fragment,{children:[e.jsx(o,{title:"Système de design/DDR/DDR-001 : Niveaux de composition"}),`
`,e.jsx(i,{children:a})]})}function p(n={}){const{wrapper:t}={...r(),...n.components};return t?e.jsx(t,{...n,children:e.jsx(s,{...n})}):s()}export{p as default};
