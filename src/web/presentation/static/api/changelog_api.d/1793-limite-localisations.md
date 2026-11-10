---
type: non_retrocompatible
date: 2026-11-04
pr: 2263
liens:
  - https://github.com/betagouv/csplab/issues/1793
---

`POST /api/v1/offres/creer_modifier` : une offre est rejetée dans `errors` si elle envoie
plus de 50 lieux, ou deux fois le même lieu (mêmes `pays`, `region`, `departement` et
`localisation_label`, quelles que soient la latitude et la longitude).

### Compatibilité

Une offre avec plus de 50 lieux ou un lieu en double, jusqu'ici acceptée (seul le premier
lieu était gardé), est désormais rejetée. Envoyez au plus 50 lieux, tous distincts.
