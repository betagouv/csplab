---
type: non_retrocompatible
date: 2026-10-26
pr: 2073
liens:
  - https://github.com/betagouv/csplab/issues/2071
---

`POST /api/v1/offres/creer_modifier` : une offre dont `localisation[].pays` n'est pas
en majuscules (`fra`, `Fra`…) est désormais rejetée. Elle apparaît dans `errors`, avec
le message « Code pays invalide, un code ISO 3166-1 alpha-3 en majuscules est attendu
(ex. FRA). ». Jusqu'ici, le code était enregistré tel quel et la règle « région et
département obligatoires pour une offre en France » ne s'appliquait pas.

### Compatibilité

Envoyez un code pays ISO 3166-1 alpha-3 existant, en majuscules (`FRA`, `BEL`…).
