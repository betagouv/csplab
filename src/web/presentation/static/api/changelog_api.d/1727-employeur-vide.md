---
type: modifie
date: 2026-10-05
pr: 1727
---

- `POST /api/v1/offres/creer_modifier` : `description.employeur` accepte maintenant un
  texte vide. Le champ reste obligatoire. Une offre dont l'employeur est vide n'est
  plus rejetée, et `employer` vaut alors `null` dans les réponses.
