---
type: non_retrocompatible
date: 2026-10-28
pr: 2086
liens:
  - https://github.com/betagouv/csplab/issues/2070
---

`POST /api/v1/offres/creer_modifier` : une offre dont `profession.domaine` ne correspond
pas au domaine du métier `profession.metier` est désormais rejetée. Elle apparaît dans
`errors`, avec un message tel que « Le domaine COM ne correspond pas au métier ERACH001
(ACH). ». Jusqu'ici, le domaine et le métier étaient vérifiés séparément.

### Compatibilité

Le domaine d'un métier est le champ `domaine_fonctionnel_code` renvoyé par
`GET /api/v1/metiers`. Le plus simple est de ne plus envoyer `profession.domaine`, sauf
pour les codes métier qui relèvent de plusieurs domaines.
