# ARS transcoding tables

Source slug: `ars` (see `infrastructure.gateways.transcoding`). Each CSV in
this directory is a transcoding table for one `Offer` field, keyed by the
CSV's filename (its stem) — e.g. `types_de_contrat.csv` is consulted as
`transcoder.translate("types_de_contrat", ...)` in
`infrastructure/gateways/offers_cleaner.py`.

## Used

| CSV | Offer field |
| --- | --- |
| `types_de_contrat.csv` | `contract_type` |
| `niveaux_de_diplome.csv` | `education_level` |
| `niveaux_d_experience.csv` | `experience` |
| `regions.csv` | `localisation.region` |
| `departements.csv` | `localisation.department` |
| `pays.csv` | `localisation.country` |
| `zones_geo.csv` | `localisation.area` |
| `verses.csv` | `verse` |
| `categories.csv` | `category` |
| `oui_non.csv` | `working_place`, `management` |
| `niveaux_de_langue.csv` | `languages[].language_level` |
| `metiers.csv` | `family_code` |

## Unused

Loaded into memory (via `load_transcoders_by_slug`) but never consulted by
`OffersCleaner`, because there's no corresponding field on `Offer`, or the
field is populated without transcoding:

- `categories_d_offre.csv` — "offer category" (e.g. `Standard`); no field on
  `Offer` or `TalentsoftDetailOffer` consumption corresponds to it today.
- `evenements_offre.csv` — offer lifecycle events (validation, archiving,
  etc.); not modeled on `Offer`.
- `specialisations.csv` — `specialisations` is populated with the raw
  `clientCode` values verbatim, unmapped.
- `temps_de_travail.csv` — full/part-time; not modeled on `Offer`.

If a new use case needs one of these, wire it in `OffersCleaner` following
the same pattern as the "Used" table, then move it up here.

## Adding a new Source

Drop a `data/<slug>/<field>.csv` directory next to this one, following the
same `intitule;code_client;mappe_sur_code_client_dgafp` schema — no code
change is required to load it (`load_transcoders_by_slug` auto-discovers
every `data/<slug>/` directory). Document its used/unused fields in a
README here, mirroring this one.
