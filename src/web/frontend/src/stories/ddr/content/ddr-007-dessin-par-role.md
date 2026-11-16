---
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
