---
type: non_retrocompatible
date: 2026-10-22
pr: 2043
liens:
  - https://github.com/betagouv/csplab/issues/2033
---

`POST /api/v1/offres/creer_modifier` : une offre dont `conditions.note_ouverture_poste_url`
n'est pas un lien `https` vers `legifrance.gouv.fr` ou `www.legifrance.gouv.fr` est
désormais rejetée. Elle apparaît dans `errors`, avec le message « Le lien doit être en
https et pointer vers l'avis de vacance publié sur legifrance.gouv.fr. ». Jusqu'ici,
n'importe quel lien web était accepté.

### Compatibilité

`conditions.note_ouverture_poste_url` doit contenir le lien vers l'avis de vacance
publié au Journal officiel. Ne le renseignez pas si l'offre n'a pas d'avis de vacance :
la page de candidature se transmet dans `url_candidature`.
