---
titre: "Lecture des offres : choix des champs renvoyés avec l'en-tête `X-Fields`"
type: ajoute
date: 2026-11-28
pr: 2708
liens:
  - https://github.com/betagouv/csplab/issues/2682
---

`GET /api/v1/offres` : l'en-tête `X-Fields` choisit les champs renvoyés pour chaque
offre, par exemple `X-Fields: reference,titre,localisation{departement}`, et `*`
renvoie tous les champs. Il donne aussi accès aux textes longs, aux critères, aux
autres conditions et aux dates de création et de mise à jour, absents par défaut.
Un champ inconnu ou non disponible renvoie une erreur `400`.
