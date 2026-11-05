---
type: non_retrocompatible
date: 2026-11-05
pr: 2313
liens:
  - https://github.com/betagouv/csplab/issues/2309
---

`POST /api/v1/offres/creer_modifier` : une offre dont le `pays` d'une localisation est
le code ISO d'un département ou d'une collectivité d'outre-mer (`GLP`, `MTQ`, `GUF`,
`REU`, `MYT`, `SPM`, `BLM`, `MAF`, `WLF`, `PYF`, `NCL`) est désormais rejetée. Elle
apparaît dans `errors`, avec un message qui donne les valeurs attendues, par exemple
« Guadeloupe : renseigner `pays` = `FRA`, `region` = `DOM`, `departement` = `971`. ».
Jusqu'ici, elle était enregistrée comme une offre à l'étranger, sans région ni
département, et n'apparaissait pas dans les filtres `region` et `departement`.

### Compatibilité

Renseignez l'outre-mer en `FRA`, avec son département :

- départements d'outre-mer (`971` à `974`, `976`) : région `DOM` ou code INSEE de la
  région (`01` à `04`, `06`) ;
- collectivités d'outre-mer (`975`, `977`, `978`, `986`, `987`, `988`, `SPM`, `WLF`) :
  région `TOM`.

`DOM` (République dominicaine) et `ATF` (Terres australes et antarctiques françaises)
restent acceptés comme pays.
