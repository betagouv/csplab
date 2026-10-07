# Correspondance offre TalentSoft (Format TS) → offre API v1

_Dernière mise à jour : 2026-10-07_

Conversion d'une offre au format TalentSoft en offre envoyée à l'API.
Voir `docs/talentsoft_webhooks.md` pour le côté webhooks.

Notation : `a.b` désigne un objet imbriqué, `a[]` une liste, `a[0]` son premier élément. Tout objet codé (`contractType`, `offerFamilyCategory`, `educationLevel`, `diploma`, `experienceLevel`, `country`, `region`, `department`, `specialisations[]`, `languages[].languageName|languageLevel`) est lu par son `clientCode` ; ses autres clés (`code`, `label`, `active`, `parentCode`, `type`, `parentType`, `hasChildren`) sont ignorées.

## 1. Champs reliés

| Format TS Offer | Offer API v1 | Note |
|---|---|---|
| `reference` | `identification.reference` | |
| `salaryRange.clientCode` | `identification.versant` | Dans Format TS, `salaryRange` est une simple chaîne, toujours `null` : le versant est alors déduit de `reference` (`APHP`/`MENJ`). Les valeurs contenant `FPT`/`FPH`/`FPE` donnent un `Verse`. |
| `title` | `titre` | Copié aussi dans `titre_long`. |
| `organisationName` | `organisation.nom` | |
| `organisation.entityCode` | `organisation.talentsoft_organisme_entity_code` | Lien vers l'organisme Talentsoft, vide s'il est inconnu. |
| `contractType.clientCode` | `nature_offre` | Traduit par le transcodeur de la source. |
| `offerFamilyCategory.clientCode` | `profession.metier` | `profession.domaine` correspond à ses 3 premiers caractères, après retrait d'un `ER` initial. |
| `description1` | `description.mission` | |
| `description2` | `description.profil` | |
| `customFields.description.longText1` | `description.employeur` | |
| `customFields.description.longText2` | `description.conditions_exercice` | |
| `customFields.description.longText3` | `description.descriptif_service` | |
| `customFields.offerCustomBlock1.longText1` | `description.complements` | |
| `offerUrl` | `url_offre` | |
| `urlRedirectionApplicant` | `url_candidature` | Repli sur `applicationUrl`. |
| `geographicalLocation[0].clientCode` | `localisation[0].zone_geographique` | Format TS renvoie toujours `[]` : aucune `localisation` n'est donc produite à partir de lui. Toute la `localisation` est abandonnée si la zone, le pays, la région ou le département manque. |
| `country[0].clientCode` | `localisation[0].pays` | |
| `region[0].clientCode` | `localisation[0].region` | Les préfixes `_TS_CO_Region_` et `R` sont retirés pour obtenir le code INSEE. |
| `department[0].clientCode` | `localisation[0].departement` | Cas particulier de la Nouvelle-Calédonie (`988`). |
| `latitude`, `longitude` | `localisation[0].latitude`, `localisation[0].longitude` | Repli sur `geolocation`, puis sur `organisation.geolocation`. |
| `customFields.location.shortText1` | `localisation[0].localisation_label` | |
| `startPublicationDate` | `publication.debut_publication` | |
| `endPublicationDate` | `publication.fin_publication` | Repli sur `beginningDate`, puis sur `debut_publication` + 365 jours. Le `OfferInputMapper` du web ne lit jamais `fin_publication`. |
| `customFields.offer.date1` | `publication.fin_candidature` | |
| `beginningDate` | `conditions.debut_contrat` | Sert aussi de repli pour `fin_publication`. |
| `contractDuration` | `conditions.duree_contrat` | |
| `educationLevel.clientCode` | `criteres.diplome_niveau` | Lettres `A`-`H` ou `NIV_DIPL<n>` converties en niveau. |
| `diploma.clientCode` | `criteres.diplome` | |
| `experienceLevel.clientCode` | `criteres.experience` | Converti en nom d'`ExperienceLevel`. |
| `specialisations[].clientCode` | `criteres.specialisations` | Remplacé par le libellé de la spécialisation. |
| `languages[].languageName.clientCode` | `criteres.langues[].iso_code` | |
| `languages[].languageLevel.clientCode` | `criteres.langues[].niveau` | |

`criteres` n'est envoyé que si au moins un des champs niveau de diplôme, diplôme, expérience, spécialisations ou langues est renseigné.

## 2. Champs Format TS sans équivalent dans l'API v1

| Format TS Offer | Note |
|---|---|
| `isTopOffer` | Toujours `false` dans Format TS. |
| `location` | Libellé d'affichage ; le libellé repris vient de `customFields.location.shortText1`. |
| `modificationDate` | |
| `contractTypeCountry` | |
| `organisationDescription` | Capturé nulle part dans la chaîne. |
| `organisationLogoUrl` | |
| `description1Formatted`, `description2Formatted` | Variantes HTML de `description1` / `description2`, non utilisées. |
| `professionalCategory` | |
| `_links`, `_format`, `_metadata` | Métadonnées de transport. |
| `urlRedirectionEmployee` | |
| `locations` | |
| `geolocation` | Simple repli de coordonnées pour `localisation[0]`. |
| `isAnonymousOrganisation` | |
| `organisation.name`, `.description`, `.url`, `.phoneNumber`, `.postCode`, `.geolocation`, `.parentName`, `.logoUrl`, `.maxDelayForConsent`, `.retentionPeriod`, `.generalConditions`, `.personalDataConsent` | Données d'organisme, synchronisées par l'upsert séparé des organismes Talentsoft (`TalentsoftOrganismeUpsertInputSerializer`), pas par le payload d'offre. |
| `operationalManager` | Jamais lu : `contacts` vaut toujours `null`. |
| `applicationQuestions`, `attachedFilesUrls` | |
| `customFields.offer.shortText1`, `.longText1`, `.longText2`, `.longText3` | |
| `customFields.description.date1`, `.shortText1` | |
| `customFields.location.date1`, `.longText1`, `.longText2`, `.longText3` | |
| `customFields.offerCustomBlock1.date1`, `.shortText1`, `.longText2`, `.longText3` | |
| `code`, `label`, `active`, `parentCode`, `type`, `parentType`, `hasChildren` (tout objet codé) | Seul `clientCode` est lu. |

## 3. Champs de l'API v1 sans équivalent dans le Format TS

| Offer API v1 | Note |
|---|---|
| `categories` | Lu par l'ingestion dans `customFields.description.customCodeTable1`, que le serializer Format TS n'expose pas (`CAT-A`/`B`/`C` ; `CAT-AEF`/`ESD`/`ES` → `APLUS`). Le web garde `sorted(categories)[0]`. |
| `type_contrat` | Lu dans `customFields.offer.customCodeTable2` (absent de Format TS) : `CDD*`, `CDI`, `PERMANENT`, `VACATION`. |
| `vacance_poste` | Jamais renseigné par l'ingestion (vide), stocké à `null`. |
| `organisation.siret` | Jamais renseigné par l'ingestion (vide) ; le rapprochement d'organisme passe par `talentsoft_organisme_entity_code`. |
| `profession.referentiel` | Constante `RMFPv2`. |
| `profession.code_emploi_local` | Jamais renseigné, `local_job_code` reste à `null`. |
| `criteres.documents_requis`, `criteres.competences_requises` | Jamais renseignés par l'ingestion. |
| `conditions.temps_travail` | Lu dans `customFields.description.customCodeTable3` (absent de Format TS), `NON_DEFINI` par défaut. |
| `conditions.lieu_de_travail` | Lu dans `customFields.offerCustomBlock1.customCodeTable2` (absent du Format TS) : `reponse_oui` → `TELETRAVAIL`, `reponse_non` → `SUR_SITE`, sinon `NON_DEFINI`. |
| `conditions.management` | Lu dans `customFields.offerCustomBlock1.customCodeTable1` (absent du Format TS) : `reponse_oui` → `AVEC`, `reponse_non` → `SANS`. |
| `conditions.salaire_titulaire`, `.salaire_contractuel`, `.fin_contrat`, `.ouvert_aux_militaires`, `.complements`, `.bases_legales`, `.note_ouverture_poste_url` | Jamais renseignés par l'ingestion. |
| `contacts[].email` | Toujours `null` côté ingestion. |
| `publication.debut_vacance_poste` | Jamais renseigné par l'ingestion, et ignoré par le mapper du web. |
