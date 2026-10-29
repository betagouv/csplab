---
type: non_retrocompatible
date: 2026-10-29
pr: 2166
liens:
  - https://github.com/betagouv/csplab/issues/2158
---

`POST /api/v1/offres/creer_modifier` : `conditions.bases_legales` est désormais un texte
libre en Markdown, validé comme les champs du bloc `description`. Une offre dont
`conditions.bases_legales` contient une balise HTML ou un lien autre que `http`, `https`
ou `mailto` est rejetée et apparaît dans `errors`. La limite de 1 500 caractères est
inchangée et s'applique au texte Markdown, syntaxe comprise.

### Compatibilité

En dehors du rejet du HTML et des liens non autorisés, un texte brut reste un Markdown
valide. Pour qu'un retour à la ligne soit conservé à l'affichage, séparez les lignes par
une ligne vide ou écrivez-les comme une liste (`- 1° aux fonctionnaires…`).
