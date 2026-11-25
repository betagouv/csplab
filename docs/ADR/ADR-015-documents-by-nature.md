---
status: proposé
date: 2026-11-25
decision-makers: Équipe
---

# ADR-015 : Ranger chaque document selon sa nature

## Contexte et problème

Dans quel fichier une personne qui arrive, ou un agent de code, cherche-t-il une règle, un mode d'emploi ou la raison d'un choix ? Le dépôt contient des décisions, des conventions, des guides et un glossaire, que les agents de code de chaque membre parcourent à chaque tâche. Quand on écrit un même contenu dans deux documents, les deux versions deviennent contradictoires.

Le relevé de l'existant est dans l'[epic de la documentation](https://github.com/betagouv/csplab/issues/2529).

## Options considérées

1. La liste à plat de `docs/`, avec un index où on écrit la nature de chaque document : on garde tous les liens, et on ouvre l'index pour connaître la nature d'un document.
2. Un dossier par nature. C'est l'option retenue.
3. Une troisième série de décisions pour les choix d'outils : on reconnaît la nature d'une décision à son dossier, et l'équipe suit trois numérotations.

## Décision

Dans `docs/`, on range chaque document dans un de ces quatre dossiers, d'après sa nature. On scinde un document qui mêle deux natures, et on ajoute un dossier par une ADR qui amende celle-ci.

- `docs/decisions/` : les ADR, pour les décisions d'architecture, les choix d'outils et les contrats d'API, au format de l'[ADR-014](ADR-014-recording-decisions.md) ;
- `docs/conventions/` : les règles qu'on applique en écrivant le code ;
- `docs/guides/` : le mode d'emploi ou la référence d'un outil, d'une opération ou de l'API ;
- `docs/domain/` : les documents du domaine dont on se sert en écrivant le code, comme le glossaire.

Dans l'ADR d'un outil, on écrit l'usage que l'équipe attend de l'outil, si elle considère ce choix comme ferme ou à l'essai, et ce qui l'amènerait à le réviser. Dans le guide de l'outil, on écrit son mode d'emploi et on renvoie à l'ADR. On écrit aussi un changement de contrat d'API dans le [changelog de l'API](../changelog_api.md), qu'on range dans `docs/guides/`.

On laisse à leur place le sous-module `docs/dat` et les exports de `docs/notebook/`. On range hors de `docs/` les documents de trois natures :

- règle de produit : dans l'issue où on la tranche ;
- décision de design (interaction, composition des composants, sens d'un élément visuel, ergonomie, choix d'un kit de design) : dans le Storybook, `src/web/frontend/src/stories/ddr/`, où les personnes du produit et du design la consultent ;
- processus d'équipe : `CONTRIBUTING.md`, à la racine du dépôt.

## Conséquences

- Une personne qui arrive ou un agent de code reconnaît la nature d'un document à son dossier.
- Pour un outil qui a une ADR, on lit les raisons du choix dans l'ADR et le mode d'emploi dans le guide.
- L'auteur d'un document choisit son dossier, et scinde un document qui mêle deux natures.
- On déplace les documents de `docs/`, ADR comprises. Les liens écrits dans les PR fusionnées et hors du dépôt cessent de fonctionner.

## Confirmation

La CI vérifie par `mise run check` que chaque document de `docs/` est dans un des quatre dossiers, hors du sous-module `docs/dat` et des exports de `docs/notebook/`, en erreur. Le relecteur d'une PR vérifie à la main la nature du document.
