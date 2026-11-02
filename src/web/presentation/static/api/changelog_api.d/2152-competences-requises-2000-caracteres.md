---
type: modifie
date: 2026-11-02
pr: 2160
liens:
  - https://github.com/betagouv/csplab/issues/2152
---

`POST /api/v1/offres/creer_modifier` : `criteres.competences_requises` accepte jusqu'à
2 000 caractères, au lieu de 1 500, syntaxe Markdown comprise. Une fois converties en
Markdown, les compétences saisies dans Talentsoft, limitées à 1 500 caractères en texte
brut, peuvent dépasser 1 500 caractères.
