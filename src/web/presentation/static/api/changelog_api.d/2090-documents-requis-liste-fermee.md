---
type: non_retrocompatible
date: 2026-10-28
pr: 2091
liens:
  - https://github.com/betagouv/csplab/issues/2090
---

`POST /api/v1/offres/creer_modifier` : `criteres.documents_requis` n'accepte plus de
texte libre. Chaque élément doit être l'une des valeurs `CV`, `LETTRE_MOTIVATION` ou
`PORTFOLIO`, et chaque document ne peut être cité qu'une fois. Une offre avec une autre
valeur ou un doublon est rejetée et apparaît dans `errors`.

### Compatibilité

Remplacez le texte libre de `criteres.documents_requis` par les codes ci-dessus. Les
autres documents ne peuvent pas encore être transmis dans ce champ.
