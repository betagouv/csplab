---
type: non_retrocompatible
date: 2026-10-26
pr: 2076
liens:
  - https://github.com/betagouv/csplab/issues/2072
---

`POST /api/v1/offres/creer_modifier` : une offre dont le `departement` d'une localisation
n'appartient pas à sa `region` est désormais rejetée. Elle apparaît dans `errors`, avec
un message du type « Le département 13 (Bouches-du-Rhône) n'appartient pas à la région
11 (Île-de-France). ». Jusqu'ici, la région et le département étaient vérifiés
séparément : `region` `01` (Guadeloupe) et `departement` `01` (Ain) étaient acceptés
ensemble.

### Compatibilité

Renseignez dans `region` le code INSEE de la région du département, et non le code du
département. Pour l'outre-mer :

- départements et régions d'outre-mer (`971` à `974`, `976`) : le code INSEE de la
  région (`01` à `04`, `06`) ou `DOM` ;
- collectivités d'outre-mer (`975`, `986`, `987`, `988`, `SPM`, `WLF`) : `TOM`.
