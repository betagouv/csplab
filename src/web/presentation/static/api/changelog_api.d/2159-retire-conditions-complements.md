---
type: retire
date: 2026-10-29
pr: 2161
liens:
  - https://github.com/betagouv/csplab/issues/2159
---

`POST /api/v1/offres/creer_modifier` : `conditions.complements` est retiré, il faisait
doublon avec `description.complements`. Un `conditions.complements` envoyé est ignoré et
n'est plus enregistré.

### Compatibilité

Envoyez les informations complémentaires dans `description.complements`, en Markdown.
