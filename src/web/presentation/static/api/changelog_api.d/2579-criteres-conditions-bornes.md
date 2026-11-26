---
titre: "Offres : diplôme, spécialisations, durée du contrat et langues bornés"
type: non_retrocompatible
date: 2026-11-23
pr: 2580
liens:
  - https://github.com/betagouv/csplab/issues/2579
---

`POST /api/v1/offres/creer_modifier` : une offre est désormais rejetée, et apparaît
dans `errors`, si :

- `criteres.diplome` dépasse 255 caractères ;
- `criteres.specialisations` contient plus de 20 éléments, ou un élément de plus de
  255 caractères ;
- `conditions.duree_contrat` dépasse 100 caractères ;
- un `criteres.langues[].iso_code` n'est pas un code ISO 639-1 (ex. `E`, `XX`), avec
  le message « Code de langue invalide, un code ISO 639-1 sur 2 lettres est attendu
  (ex. EN). » ;
- une même langue est citée plusieurs fois dans `criteres.langues`, avec le message
  « Chaque langue ne peut être citée qu'une fois. ».

### Compatibilité

Respectez ces longueurs et envoyez chaque langue une seule fois, avec un code ISO
639-1 existant.
