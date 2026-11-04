---
type: corrige
date: 2026-11-04
pr: 2263
liens:
  - https://github.com/betagouv/csplab/issues/1793
---

`POST /api/v1/offres/creer_modifier` : tous les lieux envoyés dans `localisation` sont
enregistrés, dans l'ordre d'envoi. Jusqu'ici, seul le premier était conservé, sans que
l'API le signale. Le premier lieu reste le lieu principal.
