---
type: non_retrocompatible
date: 2026-10-13
pr: 1935
---

`POST /api/v1/offres/creer_modifier` et `GET /api/v1/offres/sources/{source_id}` :
le format de `contacts` change. Chaque contact ne contient plus seulement `email`,
mais :

- `role` : `principal` (personne à contacter) ou `autre` (autre personne à
  contacter), au plus un contact par rôle ;
- `texte` : le contact en texte libre (nom, fonction, e-mail, téléphone…),
  100 caractères maximum ;
- `emails` : la liste des adresses email présentes dans `texte`, vide si aucune.

Les contacts sont renvoyés dans l'ordre `principal` puis `autre`. Un contact au
format précédent (`{"email": "…"}`) est rejeté.
