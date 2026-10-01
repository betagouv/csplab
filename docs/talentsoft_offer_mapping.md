# TalentSoft → web offer field mapping

This documents how a job offer fetched from TalentSoft (TS) becomes an `OfferModel` row in
`src/web`. See `docs/talentsoft_webhooks.md` for the webhook subscription side of the
integration.

## Pipeline

```
TalentSoft API/webhook
  → TalentsoftDetailOffer (src/ingestion/infrastructure/external_gateways/dtos/talentsoft_dtos.py)
  → OffersCleaner._map_talentsoft_to_offer() (src/ingestion/infrastructure/gateways/offers_cleaner.py)
  → ingestion domain Offer (src/ingestion/domain/entities/offer.py)
  → OfferUpsertPayload.from_offer() (src/ingestion/infrastructure/external_gateways/dtos/offer_upsert_payload.py)
  → POST /offres/creer_modifier (WebPublishOfferGateway.publish())
  → OffersInputSerializer (src/web/presentation/ingestion/serializers.py)
  → OfferInputMapper.to_domain() (src/web/presentation/ingestion/mappers.py)
  → web domain Offer (libs/referentiel/entities/offer.py)
  → OfferMapper.from_domain() (src/web/infrastructure/mappers/offer_mapper.py)
  → OfferModel (src/web/infrastructure/django_apps/referentiel/models/offer.py)
```

## Field mapping

| TalentSoft raw field | Transformation | Ingestion `Offer` field | JSON payload field (`/offres/creer_modifier`) | Web `OfferModel` field | Notes |
|---|---|---|---|---|---|
| `reference` (of the `RawOffer`, itself the TS `reference`) | passthrough | `reference` | `identification.reference` | `reference` | |
| `salaryRange.clientCode` (+ `reference` substring `APHP`/`MENJ` as fallback) | `_map_verse`: substring match `FPT`/`FPH`/`FPE` → `Verse` enum | `verse` | `identification.versant` | `verse` | Ingestion's own `external_id` (`f"{raw_salaryRange_code}-{reference}"`) is **not** transmitted — web recomputes its canonical `external_id` as `f"{versant}-{reference}"` from the clean `Verse` value, so the two `external_id` computations differ in what they use as prefix; only the web-side one is persisted. |
| `title` | passthrough | `title` | `titre` (and duplicated into `titre_long`) | `title`, `long_title` | TS has no separate "long title" concept — both payload fields get the same value. |
| `organisationName` | passthrough | `organization` | `organisation.nom` (duplicated into `description.employeur`) | `organization`, `employer` | `organisationDescription` (raw TS field) is **not captured** anywhere in this pipeline. |
| `offerUrl` | parsed as URL | `offer_url` | `url_offre` | `offer_url` | |
| `applicationUrl` (detail only) | parsed as URL | `application_url` | `url_candidature` | `application_url` | |
| `offerFamilyCategory.clientCode` | passthrough | `family_code` | `profession.metier`; also derives `profession.domaine` (first 3 chars of `family_code` after stripping a leading `"ER"`) | `job_family_referential`, `local_job_code`, `functional_area_code` | `profession.referentiel` payload field is a hardcoded `"RMFPv2"` constant, not sourced from TS. `local_job_code` (`profession.code_emploi_local`) is never set by the ingestion payload → always `None` from this source. `code_emploi_csp` on `OfferModel` is **not populated** by this pipeline at all (set elsewhere). |
| `customFields.description.customCodeTable1.clientCode` (`CAT-A`/`CAT-B`/`CAT-C`/`CAT-AEF`/`CAT-ESD`/`CAT-ES`) | `_parse_category` → `Category` enum (`CAT-AEF/ESD/ES` all collapse to `APLUS`) | `category` | `categories` (single-item list) | `category` | Web picks `sorted(categories)[0]` — a `# todo handle multiple categories later` in `OfferInputMapper`, currently only one category is ever sent anyway. |
| `contractType.clientCode` | `_map_contract_type`: `_ARS_CONTRACT_TYPE_MAPPING` dict, else substring `TITULAIRE`/`CONTRACTUEL`/`TERRITORIAL` | `contract_type` | `type_contrat` | `contract_type` | |
| `customFields.offer.customCodeTable2.clientCode` | `_map_contract_kind`: `CDD*` prefix, or `CDI`/`PERMANENT`/`VACATION` map | `contract_kind` (single value) | `forme_contrat` (single-item list) | `contract_kind` (list) | |
| `description1` | passthrough | `mission` | `description.mission` | `mission` | |
| `description2` | passthrough | `profile` | `description.profil` | `profile` | `description1Formatted`/`description2Formatted` (HTML variants) are **not used** anywhere. |
| — (not sourced from TS) | — | — | `description.complements` (always `""`) | `complements` | |
| `geographicalLocation[0]`, `country[0]`, `region[0]`, `department[0]` (`clientCode`s), `latitude`/`longitude` (or `geolocation`, or `organisation.geolocation` as fallbacks) | `_map_localisation_from_arrays`: area via `_TALENTSOFT_TO_AREA` dict, region code stripped of `_TS_CO_Region_`/leading `R` prefix → INSEE code, department special-cased for Nouvelle-Calédonie (`988`); returns `None` if any of area/country/region/department is missing or area is unmapped | `localisation` (`Localisation` value object) | `localisation[0]` (`zone_geographique`, `pays`, `region`, `departement`, `latitude`, `longitude`) | `area`, `country`, `region`, `department`, `latitude`, `longitude` | `localisation_label` is never sent by the payload → `OfferModel.location_label` is always `None` from this pipeline. |
| `startPublicationDate` | ISO-8601 parse (`Z` → `+00:00`) | `publication_date` | `publication.debut_publication` | `publication_date` | |
| `endPublicationDate` (detail only) | ISO-8601 parse if present | `end_publication_date` | folded into `publication.fin_publication` fallback chain (`end_publication_date` → `beginning_date` → `publication_date + 365 days`) | *(none)* | `OfferModel` has no "end publication" field — `fin_publication` is computed and sent but **silently dropped** by `OfferInputMapper`, which only reads `debut_publication`. |
| `beginningDate` | ISO-8601 parse → `LimitDate` | `beginning_date` | only used as a fallback input to `publication.fin_publication` (see above) — **not** sent as its own field | `beginning_date` | `OfferInputMapper.beginning_date` is populated from `conditions.debut_contrat`, but `ConditionsPayload` never sets that key — so `OfferModel.beginning_date` is effectively **always unset** via this pipeline. |
| `educationLevel.clientCode` | `_map_education_level`: single-letter `A`-`H` map, or `NIV_DIPL(\d)` pattern with digit overrides | `education_level` (int) | `criteres.diplome_niveau` | `criteria.diplome_niveau` (via `OfferCriteria.from_dict`, JSON field `criteria`) | `criteres` block is only sent if at least one of education/diploma/experience/specialisations/languages is present. |
| `diploma.clientCode` | passthrough | `diploma` | `criteres.diplome` | `criteria.diplome` | |
| `experienceLevel.clientCode` | `_map_experience` literal dict → `ExperienceLevel` enum or `None` | `experience` | `criteres.experience` | `criteria.experience_level` | |
| `specialisations[].clientCode` | list passthrough | `specialisations` | `criteres.specialisations` | `criteria.specialisations` | |
| `languages[].languageName.clientCode` / `.languageLevel.clientCode` | `Language(iso_code, LanguageLevel(...))` | `languages` | `criteres.langues[].{iso_code, niveau}` | `criteria.languages` | |
| — (never sourced from TS: `documents_requis`, `competences_requises`) | — | — | `criteres.documents_requis`, `criteres.competences_requises` (always empty, dropped by serializer) | *(none)* | |
| `customFields.offerCustomBlock1.customCodeTable2.clientCode` | `_map_working_place`: `reponse_oui`→`TELETRAVAIL`, `reponse_non`→`SUR_SITE`, else `NON_DEFINI` | `working_place` | `conditions.lieu_de_travail` | `conditions["lieu_de_travail"]` (raw dict on `conditions` JSON field) | |
| `customFields.offerCustomBlock1.customCodeTable1.clientCode` | `_map_management`: `reponse_non`→`SANS`, `reponse_oui`→`AVEC`, else `None` | `management` | `conditions.management` | `conditions["management"]` | |
| `contractDuration` | **not used** | — | `conditions.temps_travail` is a hardcoded `WorkingTime.NON_DEFINI` constant, not sourced from TS | `conditions["temps_travail"]` | |
| — (TS `operationalManager` exists but is never read) | — | — | `contacts` (always `None`) | `contacts` | Always `None` via this pipeline. |
| — (not sourced from TS) | — | — | `vacance_poste` (default `""`) | `job_vacancy` | `"" or None` → `None`, so effectively never populated by this pipeline. |
| — (not sourced from TS; SIRET is matched via the separate organisme-upsert flow) | — | — | `organisation.siret` (default `""`) | *(not part of `Offer`, used for organisme matching upstream)* | |

Internal bookkeeping fields on `OfferModel` (`processing`, `processed_at`, `archived_at`,
`created_at`, `updated_at`, `source`) are set by the web-side usecase/repository, not derived
from TS data at all.
