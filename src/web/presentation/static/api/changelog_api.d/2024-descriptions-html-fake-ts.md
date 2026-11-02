---
type: modifie
date: 2026-10-21
pr: 2024
liens:
  - https://github.com/betagouv/csplab/issues/2020
---

- `GET /api/fake-ts/offersummaries` et `GET /api/fake-ts/offers/getoffer` :
  `description1Formatted` et `description2Formatted` contiennent désormais la
  description convertie du Markdown en HTML, au lieu de `null`.
- `GET /api/fake-ts/offers/getoffer` : chaque bloc de `customFields` contient les
  champs `longText1Formatted`, `longText2Formatted` et `longText3Formatted`. Ceux qui
  correspondent à une description (`description.longText1Formatted` à
  `longText3Formatted`, `offerCustomBlock1.longText1Formatted`) contiennent le HTML,
  les autres sont à `null`.
- `GET /api/fake-ts/offers/getoffer` : `customFields` contient un nouveau bloc
  `applicantCriteria`, dont tous les champs sont à `null`.

Le HTML produit se limite aux paragraphes, sauts de ligne, gras, italique, listes et
liens `http`, `https` et `mailto` (ouverts dans un nouvel onglet). Les titres Markdown
sont rendus en paragraphes en gras. Un champ vide donne `null`.

Les champs texte brut des descriptions (`description1`, `description2`,
`customFields.description.longText1` à `longText3`,
`customFields.offerCustomBlock1.longText1`) contiennent toujours le Markdown.

### Compatibilité

Ces changements sont rétrocompatibles : les champs ajoutés ne retirent aucun champ
existant.
