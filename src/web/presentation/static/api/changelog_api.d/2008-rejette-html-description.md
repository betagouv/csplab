---
type: non_retrocompatible
date: 2026-10-20
pr: 2008
liens:
  - https://github.com/betagouv/csplab/issues/1803
---

`POST /api/v1/offres/creer_modifier` : une offre dont un champ du bloc `description`
contient une balise HTML ou un lien autre que `http`, `https` ou `mailto` est
désormais rejetée. Elle apparaît dans `errors`, avec un message qui cite l'élément
refusé. Jusqu'ici, ce texte était accepté tel quel.

### Compatibilité

En dehors du rejet du HTML et des liens non autorisés, un texte brut reste un
Markdown valide. Seuls quelques caractères (`*`, `_`, `#`, `1.` en début de ligne)
sont désormais interprétés comme de la mise en forme.
