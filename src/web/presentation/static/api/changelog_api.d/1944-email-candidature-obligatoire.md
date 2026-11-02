---
type: non_retrocompatible
date: 2026-10-14
pr: 1944
---

`POST /api/v1/offres/creer_modifier` : une offre doit renseigner **soit**
`url_candidature`, **soit** le nouveau champ `email_candidature` (adresse email
valide), mais pas les deux. Une offre sans aucun des deux, ou avec les deux, est
rejetée. Jusqu'ici, `url_candidature` pouvait être vide.
