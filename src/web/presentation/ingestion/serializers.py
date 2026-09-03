import gettext

import pycountry
from drf_spectacular.utils import extend_schema_field
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.domaine_fonctionnel import DomaineFonctionnel
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.job_family_referential import JobFamilyReferential
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_conditions import (
    JobVacancy,
    Management,
    OpenToMilitary,
    WorkingPlace,
    WorkingTime,
)
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import serializers

from presentation.api.serializers import GenericErrorSerializer
from presentation.commons.serializers import LocalisationSerializer, OrganismeSerializer
from presentation.ingestion.legacy_client_aliases import (
    AREA_CODE_ALIASES,
    CATEGORY_CODE_ALIASES,
    CONTRACT_TYPE_CODE_ALIASES,
    COUNTRY_CODE_ALIASES,
    DEPARTMENT_CODE_ALIASES,
    DOMAIN_CODE_ALIASES,
    EXPERIENCE_LEVEL_CODE_ALIASES,
    MANAGEMENT_CODE_ALIASES,
    PUBLICATION_DATE_ALIASES,
    REGION_CODE_ALIASES,
    WORKING_PLACE_CODE_ALIASES,
)


def _parse_enum_list(value, enum_cls, error_label, excluded=frozenset(), aliases=None):
    if not value:
        return None

    allowed = {e.name for e in enum_cls if e not in excluded}
    requested = [part.strip() for part in value.split(",") if part.strip()]
    if aliases:
        requested = [aliases.get(part, part) for part in requested]
    invalid = [part for part in requested if part not in allowed]
    if invalid:
        raise serializers.ValidationError(
            "Valeurs de {} invalides : {}. Valeurs autorisées : {}.".format(
                error_label, ", ".join(invalid), ", ".join(sorted(allowed))
            )
        )

    return [enum_cls[part] for part in requested]


class _CommaSeparatedEnumField(serializers.MultipleChoiceField):
    def __init__(
        self, enum_cls, error_label, excluded=frozenset(), aliases=None, **kwargs
    ):
        self.enum_cls = enum_cls
        self.error_label = error_label
        self.excluded = excluded
        self.aliases = aliases
        choices = [(e.name, e.value) for e in enum_cls if e not in excluded]
        kwargs.setdefault("default", None)
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            data = ",".join(data)
        return _parse_enum_list(
            data, self.enum_cls, self.error_label, self.excluded, self.aliases
        )


_fr_country_names = gettext.translation(
    "iso3166-1", pycountry.LOCALES_DIR, languages=["fr"]
).gettext
COUNTRY_NAMES = {c.alpha_3: _fr_country_names(c.name) for c in pycountry.countries}
COUNTRY_CODES = frozenset(COUNTRY_NAMES)
REGION_NAMES = {code: Region.NAMES.get(code, code) for code in Region.VALID_CODES}
DEPARTMENT_NAMES = {
    code: Department.NAMES.get(code, code) for code in Department.VALID_CODES
}
DOMAIN_NAMES = {e.value: e.label for e in DomaineFonctionnel}


def _parse_code_list(value, valid_codes, error_label, aliases=None):
    if not value:
        return None

    requested = [part.strip().upper() for part in value.split(",") if part.strip()]
    if aliases:
        requested = [aliases.get(part, part) for part in requested]
    invalid = [part for part in requested if part not in valid_codes]
    if invalid:
        raise serializers.ValidationError(
            "Valeurs de {} invalides : {}.".format(error_label, ", ".join(invalid))
        )

    return requested


class _CommaSeparatedCodeField(serializers.MultipleChoiceField):
    def __init__(
        self, code_labels, error_label, to_value_object, aliases=None, **kwargs
    ):
        self.valid_codes = frozenset(code_labels)
        self.error_label = error_label
        self.to_value_object = to_value_object
        self.aliases = aliases
        kwargs.setdefault("default", None)
        choices = sorted(code_labels.items(), key=lambda item: item[0])
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            data = ",".join(data)
        codes = _parse_code_list(data, self.valid_codes, self.error_label, self.aliases)
        return [self.to_value_object(code) for code in codes] if codes else None


def _resolve_location_codes(value):
    """
    For each legacy client identifier provided in `locations`, detects
    whether it refers to a country, a region, a department or a
    geographical area, then translates it to the corresponding target
    code. Legacy identifiers are unique across the four referentials, so a
    given identifier can only match one type.
    """
    requested = [part.strip() for part in value.split(",") if part.strip()]

    countries, regions, departments, areas, invalid = [], [], [], [], []
    for code in requested:
        if code in COUNTRY_CODE_ALIASES:
            countries.append(COUNTRY_CODE_ALIASES[code])
        elif code in REGION_CODE_ALIASES:
            regions.append(REGION_CODE_ALIASES[code])
        elif code in DEPARTMENT_CODE_ALIASES:
            departments.append(DEPARTMENT_CODE_ALIASES[code])
        elif code in AREA_CODE_ALIASES:
            areas.append(AREA_CODE_ALIASES[code])
        else:
            invalid.append(code)

    if invalid:
        raise serializers.ValidationError(
            "Valeurs de localisation invalides : {}.".format(", ".join(invalid))
        )

    return countries, regions, departments, areas


class _AliasedIntegerField(serializers.IntegerField):
    def __init__(self, aliases=None, **kwargs):
        self.aliases = aliases or {}
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str) and data in self.aliases:
            data = self.aliases[data]
        return super().to_internal_value(data)


class ValidationErrorSerializer(GenericErrorSerializer):
    row = serializers.IntegerField()


class NoValidRowsErrorSerializer(GenericErrorSerializer):
    validation_errors = ValidationErrorSerializer(many=True)


class ConcoursUploadResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    total_rows = serializers.IntegerField()
    valid_rows = serializers.IntegerField()
    invalid_rows = serializers.IntegerField()
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    validation_errors = ValidationErrorSerializer(many=True, allow_null=True)


class ListOffersResponseSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    reference = serializers.CharField()
    source_id = serializers.UUIDField()
    title = serializers.CharField()
    organization = serializers.CharField()
    contract_type = serializers.CharField(allow_null=True)
    category = serializers.CharField(allow_null=True)
    publication_date = serializers.DateTimeField()
    offer_url = serializers.CharField(allow_null=True)
    archived_at = serializers.DateTimeField(allow_null=True)


class ListOffersFiltersSerializer(serializers.Serializer):
    actif = serializers.BooleanField(default=True, source="active")
    categorie = _CommaSeparatedEnumField(
        Category,
        "catégorie",
        excluded={Category.HORS_CATEGORIE},
        help_text="Valeurs séparées par une virgule (ex. `A,B`).",
        source="category",
    )
    versant = _CommaSeparatedEnumField(
        Verse,
        "versant",
        help_text="Valeurs séparées par une virgule (ex. `FPE,FPT`).",
        source="verse",
    )
    type_contrat = _CommaSeparatedEnumField(
        ContractType,
        "type de contrat",
        help_text="Valeurs séparées par une virgule (ex. `TITULAIRE_CONTRACTUEL`).",
        source="contract_type",
    )
    niveau_experience = _CommaSeparatedEnumField(
        ExperienceLevel,
        "niveau d'expérience",
        help_text="Valeurs séparées par une virgule (ex. `DEBUTANT,EXPERT`).",
        source="experience_level",
    )
    management = _CommaSeparatedEnumField(
        Management,
        "management",
        help_text="Valeurs séparées par une virgule (ex. `SANS,AVEC`).",
    )
    lieu_de_travail = _CommaSeparatedEnumField(
        WorkingPlace,
        "lieu de travail",
        help_text="Valeurs séparées par une virgule (ex. `SUR_SITE,TELETRAVAIL`).",
        source="working_place",
    )
    region = _CommaSeparatedCodeField(
        REGION_NAMES,
        "région",
        lambda code: Region(code=code),
        help_text="Valeurs séparées par une virgule (ex. `11,84`).",
    )
    departement = _CommaSeparatedCodeField(
        DEPARTMENT_NAMES,
        "département",
        lambda code: Department(code=code),
        help_text="Valeurs séparées par une virgule (ex. `75,69`).",
        source="department",
    )
    pays = _CommaSeparatedCodeField(
        COUNTRY_NAMES,
        "pays",
        Country,
        help_text="Valeurs séparées par une virgule (ex. `FRA,BEL`).",
        source="country",
    )
    zone = _CommaSeparatedEnumField(
        GeographicalArea,
        "zone géographique",
        help_text="Valeurs séparées par une virgule (ex. `EUROPE,ASIE`).",
        source="area",
    )
    domaine = _CommaSeparatedCodeField(
        DOMAIN_NAMES,
        "domaine",
        lambda code: code,
        help_text="Valeurs séparées par une virgule (ex. `NUM,ACH`).",
        source="domain",
    )
    organisme = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=None,
        source="organization",
        help_text=(
            "Filtre sur l'organisme (nom exact). Répéter le paramètre pour "
            "filtrer sur plusieurs organismes (ex. "
            "`?organisme=Foo&organisme=Bar`). Ne pas séparer les valeurs par "
            "une virgule, le nom d'un organisme pouvant en contenir une."
        ),
    )
    date_publication = serializers.IntegerField(
        required=False,
        max_value=-1,
        default=None,
        source="published_within_days",
        help_text=(
            "Filtre sur la date de publication : nombre de jours négatif "
            "pour ne retourner que les offres publiées au cours des N "
            "derniers jours (ex. `-7` pour les offres publiées ces 7 "
            "derniers jours)."
        ),
    )
    latitude = serializers.FloatField(
        required=False,
        min_value=-90,
        max_value=90,
        default=None,
        help_text=(
            "Filtre géographique : latitude du point en degrés décimaux "
            "(à fournir avec `longitude` et `radius`)."
        ),
    )
    longitude = serializers.FloatField(
        required=False,
        min_value=-180,
        max_value=180,
        default=None,
        help_text=(
            "Filtre géographique : longitude du point en degrés décimaux "
            "(à fournir avec `latitude` et `radius`)."
        ),
    )
    radius = serializers.IntegerField(
        required=False,
        min_value=1,
        default=None,
        source="radius_km",
        help_text=(
            "Filtre géographique : rayon de recherche en kilomètres "
            "(à fournir avec `latitude` et `longitude`)."
        ),
    )
    mots_cles = serializers.CharField(
        required=False,
        default=None,
        allow_blank=False,
        source="keywords",
        help_text=(
            "Recherche plein texte (en français) sur le titre, l'intitulé "
            "long, la mission, le profil, l'organisme, l'employeur et les "
            "compléments de l'offre."
        ),
    )

    _GEO_FIELDS = ("latitude", "longitude", "radius_km")

    def validate(self, data):
        provided = [key for key in self._GEO_FIELDS if data.get(key) is not None]
        if provided and len(provided) != len(self._GEO_FIELDS):
            raise serializers.ValidationError(
                "Les paramètres latitude, longitude et radius doivent être "
                "fournis ensemble."
            )
        return data


class OfferSummariesQuerySerializer(serializers.Serializer):
    keywords = serializers.CharField(
        required=False,
        default=None,
        allow_blank=False,
        help_text=(
            "Recherche plein texte (en français) sur le titre, l'intitulé "
            "long, la mission, le profil, l'organisme, l'employeur et les "
            "compléments de l'offre."
        ),
    )
    start = serializers.IntegerField(required=False, min_value=0, default=0)
    count = serializers.IntegerField(
        required=False, min_value=1, max_value=1_000, default=100
    )
    category = _CommaSeparatedEnumField(
        Category,
        "catégorie",
        excluded={Category.HORS_CATEGORIE},
        aliases=CATEGORY_CODE_ALIASES,
    )
    verse = _CommaSeparatedEnumField(Verse, "versant")
    contractType = _CommaSeparatedEnumField(
        ContractType,
        "type de contrat",
        source="contract_type",
        aliases=CONTRACT_TYPE_CODE_ALIASES,
    )
    experienceLevel = _CommaSeparatedEnumField(
        ExperienceLevel,
        "niveau d'expérience",
        source="experience_level",
        aliases=EXPERIENCE_LEVEL_CODE_ALIASES,
    )
    management = _CommaSeparatedEnumField(
        Management, "management", aliases=MANAGEMENT_CODE_ALIASES
    )
    workingPlace = _CommaSeparatedEnumField(
        WorkingPlace,
        "lieu de travail",
        source="working_place",
        aliases=WORKING_PLACE_CODE_ALIASES,
    )
    region = _CommaSeparatedCodeField(
        REGION_NAMES,
        "région",
        lambda code: Region(code=code),
        aliases=REGION_CODE_ALIASES,
    )
    department = _CommaSeparatedCodeField(
        DEPARTMENT_NAMES,
        "département",
        lambda code: Department(code=code),
        aliases=DEPARTMENT_CODE_ALIASES,
    )
    country = _CommaSeparatedCodeField(
        COUNTRY_NAMES, "pays", Country, aliases=COUNTRY_CODE_ALIASES
    )
    area = _CommaSeparatedEnumField(
        GeographicalArea, "zone géographique", aliases=AREA_CODE_ALIASES
    )
    domain = _CommaSeparatedCodeField(
        DOMAIN_NAMES, "domaine", lambda code: code, aliases=DOMAIN_CODE_ALIASES
    )
    locations = serializers.CharField(
        required=False,
        default=None,
        allow_blank=False,
        help_text=(
            "Filtre géographique par identifiants du référentiel legacy du "
            "client, séparés par une virgule (ex. `?locations=27,208,330`). "
            "Le type (pays, région, département ou zone géographique) de "
            "chaque identifiant est détecté automatiquement et vient "
            "compléter les filtres `country`, `region`, `department` et "
            "`area`."
        ),
    )
    organization = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=None,
        help_text=(
            "Filtre sur l'organisme (nom exact). Répéter le paramètre pour "
            "filtrer sur plusieurs organismes (ex. "
            "`?organization=Foo&organization=Bar`). Ne pas séparer les "
            "valeurs par une virgule, le nom d'un organisme pouvant en "
            "contenir une."
        ),
    )
    publicationDate = _AliasedIntegerField(
        aliases=PUBLICATION_DATE_ALIASES,
        required=False,
        max_value=-1,
        default=None,
        source="published_within_days",
        help_text=(
            "Filtre sur la date de publication : nombre de jours négatif "
            "pour ne retourner que les offres publiées au cours des N "
            "derniers jours (ex. `-7` pour les offres publiées ces 7 "
            "derniers jours)."
        ),
    )
    latitude = serializers.FloatField(
        required=False,
        min_value=-90,
        max_value=90,
        default=None,
        help_text=(
            "Filtre géographique : latitude du point en degrés décimaux "
            "(à fournir avec `longitude` et `radius`)."
        ),
    )
    longitude = serializers.FloatField(
        required=False,
        min_value=-180,
        max_value=180,
        default=None,
        help_text=(
            "Filtre géographique : longitude du point en degrés décimaux "
            "(à fournir avec `latitude` et `radius`)."
        ),
    )
    radius = serializers.IntegerField(
        required=False,
        min_value=1,
        default=None,
        source="radius_km",
        help_text=(
            "Filtre géographique : rayon de recherche en kilomètres "
            "(à fournir avec `latitude` et `longitude`)."
        ),
    )

    _GEO_FIELDS = ("latitude", "longitude", "radius_km")

    def validate(self, data):
        provided = [key for key in self._GEO_FIELDS if data.get(key) is not None]
        if provided and len(provided) != len(self._GEO_FIELDS):
            raise serializers.ValidationError(
                "Les paramètres latitude, longitude et radius doivent être "
                "fournis ensemble."
            )

        locations = data.pop("locations", None)
        if locations:
            country_codes, region_codes, department_codes, area_names = (
                _resolve_location_codes(locations)
            )
            if country_codes:
                data["country"] = (data.get("country") or []) + [
                    Country(code) for code in country_codes
                ]
            if region_codes:
                data["region"] = (data.get("region") or []) + [
                    Region(code=code) for code in region_codes
                ]
            if department_codes:
                data["department"] = (data.get("department") or []) + [
                    Department(code=code) for code in department_codes
                ]
            if area_names:
                data["area"] = (data.get("area") or []) + [
                    GeographicalArea[name] for name in area_names
                ]

        return data


class OfferDetailQuerySerializer(serializers.Serializer):
    reference = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="La référence de l'offre.",
    )


class FakeTsCodedObjectSerializer(serializers.Serializer):
    code = serializers.CharField(allow_null=True)
    clientCode = serializers.CharField()
    label = serializers.CharField()
    active = serializers.BooleanField()
    parentCode = serializers.CharField(allow_null=True)
    type = serializers.CharField()
    parentType = serializers.CharField(allow_blank=True)
    hasChildren = serializers.BooleanField()


class FakeTsGeolocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class FakeTsOfferSummarySerializer(serializers.Serializer):
    reference = serializers.CharField()
    isTopOffer = serializers.BooleanField()
    title = serializers.CharField()
    location = serializers.CharField(allow_null=True)
    modificationDate = serializers.CharField()
    contractType = FakeTsCodedObjectSerializer(allow_null=True)
    offerFamilyCategory = FakeTsCodedObjectSerializer(allow_null=True)
    organisationName = serializers.CharField()
    organisationDescription = serializers.CharField(allow_null=True)
    organisationLogoUrl = serializers.CharField(allow_null=True)
    contractDuration = serializers.CharField(allow_null=True)
    contractTypeCountry = serializers.CharField(allow_null=True)
    description1 = serializers.CharField()
    description2 = serializers.CharField()
    description1Formatted = serializers.CharField(allow_null=True)
    description2Formatted = serializers.CharField(allow_null=True)
    salaryRange = serializers.CharField(allow_null=True)
    geographicalLocation = serializers.ListField(child=serializers.DictField())
    country = FakeTsCodedObjectSerializer(many=True)
    region = FakeTsCodedObjectSerializer(many=True)
    department = FakeTsCodedObjectSerializer(many=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    professionalCategory = serializers.CharField(allow_null=True)
    _links = serializers.ListField(child=serializers.DictField(), label="_links")
    offerUrl = serializers.CharField(allow_null=True)
    _format = serializers.CharField(allow_null=True, label="_format")
    _metadata = serializers.DictField(allow_null=True, label="_metadata")
    urlRedirectionEmployee = serializers.CharField(allow_null=True)
    urlRedirectionApplicant = serializers.CharField(allow_null=True)
    startPublicationDate = serializers.CharField()
    beginningDate = serializers.CharField(allow_null=True)
    locations = serializers.ListField(child=serializers.DictField())


class FakeTsOrganisationSerializer(serializers.Serializer):
    entityCode = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    url = serializers.CharField(allow_null=True)
    phoneNumber = serializers.CharField(allow_null=True)
    postCode = serializers.CharField(allow_null=True)
    geolocation = FakeTsGeolocationSerializer(allow_null=True)
    parentName = serializers.CharField(allow_null=True)
    logoUrl = serializers.CharField(allow_null=True)
    maxDelayForConsent = serializers.CharField(allow_null=True)
    retentionPeriod = serializers.CharField(allow_null=True)
    generalConditions = serializers.CharField(allow_null=True)
    personalDataConsent = serializers.CharField(allow_null=True)


class FakeTsLanguageSerializer(serializers.Serializer):
    languageName = FakeTsCodedObjectSerializer()
    languageLevel = FakeTsCodedObjectSerializer()


class FakeTsOfferDetailSerializer(FakeTsOfferSummarySerializer):
    applicationUrl = serializers.CharField(allow_null=True)
    endPublicationDate = serializers.CharField(allow_null=True)
    isAnonymousOrganisation = serializers.BooleanField()
    organisation = FakeTsOrganisationSerializer()
    operationalManager = serializers.CharField(allow_null=True)
    educationLevel = FakeTsCodedObjectSerializer(allow_null=True)
    diploma = FakeTsCodedObjectSerializer(allow_null=True)
    experienceLevel = FakeTsCodedObjectSerializer(allow_null=True)
    languages = FakeTsLanguageSerializer(many=True)
    specialisations = FakeTsCodedObjectSerializer(many=True)
    applicationQuestions = serializers.ListField(child=serializers.DictField())
    attachedFilesUrls = serializers.ListField(child=serializers.CharField())
    geolocation = FakeTsGeolocationSerializer(allow_null=True)
    customFields = serializers.CharField(allow_null=True)


class LocalisationInputSerializer(LocalisationSerializer):
    def validate(self, data):
        if data.get("pays") == "FRA" and not (
            data.get("region") and data.get("departement")
        ):
            raise serializers.ValidationError(
                "La région et le département sont obligatoires"
                "pour une offre localisée en France."
            )
        return data


class OfferDetailResponseSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    reference = serializers.CharField()
    source_id = serializers.UUIDField()
    title = serializers.CharField()
    long_title = serializers.CharField(allow_null=True)
    organization = serializers.CharField()
    employer = serializers.CharField(allow_null=True)
    profile = serializers.CharField()
    mission = serializers.CharField()
    complements = serializers.CharField(allow_null=True)
    verse = serializers.CharField(allow_null=True)
    category = serializers.CharField(allow_null=True)
    contract_type = serializers.CharField(allow_null=True)
    contract_kind = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    job_vacancy = serializers.CharField(allow_null=True)
    offer_url = serializers.CharField(allow_null=True)
    application_url = serializers.CharField(allow_null=True)
    localisation = serializers.SerializerMethodField()
    criteria = serializers.SerializerMethodField()
    conditions = serializers.DictField(allow_null=True)
    contacts = serializers.ListField(child=serializers.DictField(), allow_null=True)
    publication_date = serializers.DateTimeField()
    beginning_date = serializers.SerializerMethodField()
    archived_at = serializers.DateTimeField(allow_null=True)

    @extend_schema_field(LocalisationSerializer(allow_null=True))
    def get_localisation(self, obj):
        if obj.localisation is None:
            return None
        loc = obj.localisation
        return {
            "zone_geographique": str(loc.area),
            "pays": str(loc.country),
            "region": loc.region.code,
            "departement": loc.department.code,
            "localisation_label": loc.label,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
        }

    @extend_schema_field(serializers.DictField(allow_null=True))
    def get_criteria(self, obj):
        return obj.criteria.to_dict() if obj.criteria else None

    @extend_schema_field(serializers.DateTimeField(allow_null=True))
    def get_beginning_date(self, obj):
        return obj.beginning_date.value if obj.beginning_date else None


class ListOffersErrorSerializer(serializers.Serializer):
    error = serializers.CharField


class ApiKeyErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class SourceSerializer(serializers.Serializer):
    source_id = serializers.UUIDField()
    slug = serializers.CharField()
    type = serializers.CharField(source="type.value")
    client_id_front = serializers.CharField(allow_null=True, required=False)
    client_id_back = serializers.CharField(allow_null=True, required=False)
    base_url_front = serializers.URLField(allow_null=True, required=False)
    base_url_back = serializers.URLField(allow_null=True, required=False)


class ArchiveOfferRequestSerializer(serializers.Serializer):
    reference = serializers.CharField()
    source_id = serializers.UUIDField()


class ArchiveOfferSuccessSerializer(serializers.Serializer):
    status = serializers.CharField()


class ListMetiersResponseSerializer(serializers.Serializer):
    libelle = serializers.CharField()
    description = serializers.CharField()
    domaine_fonctionnel_code = serializers.CharField()
    versants = serializers.ListField(child=serializers.CharField())
    activites = serializers.ListField(child=serializers.CharField(), allow_null=True)
    conditions_particulieres = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    offer_family_code = serializers.CharField(allow_null=True)


class ListMetiersFiltersSerializer(serializers.Serializer):
    domaine = serializers.CharField(default=None, max_length=3, source="domain")


class IdentityInputSerializer(serializers.Serializer):
    reference = serializers.CharField()
    versant = serializers.ChoiceField(choices=[v.value for v in Verse])


class OrganismeInputSerializer(OrganismeSerializer):
    siret = serializers.CharField(max_length=14, allow_blank=True)


class ProfessionInputSerializer(serializers.Serializer):
    referentiel = serializers.ChoiceField(
        choices=[e.value for e in JobFamilyReferential],
        default=JobFamilyReferential.RMFPV2.value,
    )
    domaine = serializers.CharField(
        max_length=3,
        help_text="Code domaine fonctionnel RMFP, vérifié uniquement si "
        f"referentiel={JobFamilyReferential.RMFPV2.value}. Valeurs possibles : "
        + ", ".join(f"{e.value} ({e.label})" for e in DomaineFonctionnel)
        + ".",
    )
    metier = serializers.CharField(max_length=8)
    code_emploi_local = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )

    def validate(self, data):
        if data.get("referentiel") != JobFamilyReferential.RMFPV2.value:
            return data

        domaine = data.get("domaine")
        if domaine not in {e.value for e in DomaineFonctionnel}:
            raise serializers.ValidationError(
                {"domaine": f"«\xa0{domaine}\xa0» n'est pas un choix valide."}
            )

        metier = data.get("metier")
        metiers_repository = self.context.get("metiers_repository")
        if metiers_repository is not None and not metiers_repository.get_filtered(
            {"offer_family_code": metier}
        ):
            raise serializers.ValidationError(
                {"metier": f"Code métier inconnu : {metier}."}
            )

        return data


class DescriptionInputSerializer(serializers.Serializer):
    mission = serializers.CharField(max_length=10000, allow_blank=True)
    profil = serializers.CharField(max_length=10000, allow_blank=True)
    employeur = serializers.CharField(max_length=3000)
    complements = serializers.CharField(max_length=5000, allow_blank=True)


class LanguageInputSerializer(serializers.Serializer):
    iso_code = serializers.CharField(max_length=2)
    niveau = serializers.ChoiceField(choices=[(c.name, c.value) for c in LanguageLevel])


class CriteriaInputSerializer(serializers.Serializer):
    diplome_niveau = serializers.IntegerField(
        min_value=Diploma.MIN_DIPLOMA_LEVEL,
        max_value=Diploma.MAX_DIPLOMA_LEVEL,
        required=False,
    )
    experience = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ExperienceLevel], required=False
    )
    specialisations = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    diplome = serializers.CharField(required=False)
    documents_requis = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    competences_requises = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    langues = LanguageInputSerializer(many=True, required=False)


class ConditionsInputSerializer(serializers.Serializer):
    salaire_titulaire = serializers.CharField(
        max_length=100, allow_blank=True, required=False
    )
    salaire_contractuel = serializers.CharField(
        max_length=100, allow_blank=True, required=False
    )
    debut_contrat = serializers.DateTimeField(allow_null=True, required=False)
    fin_contrat = serializers.DateTimeField(allow_null=True, required=False)
    duree_contrat = serializers.CharField(allow_blank=True, required=False)
    temps_travail = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in WorkingTime]
    )
    ouvert_aux_militaires = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in OpenToMilitary], required=False
    )
    lieu_de_travail = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in WorkingPlace],
    )
    management = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in Management], required=False
    )
    complements = serializers.CharField(max_length=1500, required=False)
    bases_legales = serializers.CharField(max_length=1500, required=False)
    note_ouverture_poste_url = serializers.URLField(required=False)


class ContactsInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PublicationInputSerializer(serializers.Serializer):
    debut_publication = serializers.DateTimeField()
    fin_publication = serializers.DateTimeField()
    fin_candidature = serializers.DateTimeField(allow_null=True, required=False)
    debut_vacance_poste = serializers.DateTimeField(allow_null=True, required=False)


class OffersInputSerializer(serializers.Serializer):
    identification = IdentityInputSerializer()

    # general infos
    titre = serializers.CharField(max_length=150)
    titre_long = serializers.CharField(max_length=1500)
    organisation = OrganismeInputSerializer()
    url_offre = serializers.URLField(allow_null=True)
    url_candidature = serializers.URLField(allow_null=True)

    # classification
    profession = ProfessionInputSerializer()
    categories = serializers.MultipleChoiceField(
        choices=[(c.name, c.value) for c in Category], allow_blank=True
    )
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractType]
    )
    forme_contrat = serializers.MultipleChoiceField(
        choices=[(c.name, c.value) for c in ContractKind], allow_blank=True
    )
    vacance_poste = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in JobVacancy], allow_blank=True
    )

    description = DescriptionInputSerializer()
    localisation = LocalisationInputSerializer(many=True, allow_null=True)
    criteres = CriteriaInputSerializer(allow_null=True)
    conditions = ConditionsInputSerializer(allow_null=True)
    contacts = ContactsInputSerializer(many=True, allow_null=True)
    publication = PublicationInputSerializer()


class UpsertOffersRequestSerializer(serializers.Serializer):
    source_id = serializers.UUIDField()
    offres = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
    )


class UpsertOffersResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.DictField())


class OrganismeLocalisationInputSerializer(serializers.Serializer):
    zone_geographique = serializers.ChoiceField(
        choices=[(c.value, c.name) for c in GeographicalArea]
    )
    pays = serializers.CharField(max_length=3, min_length=3)
    region = serializers.ChoiceField(
        choices=sorted(Region.VALID_CODES, key=lambda x: x),
        allow_blank=True,
    )
    departement = serializers.ChoiceField(
        choices=sorted(Department.VALID_CODES, key=lambda x: x), allow_blank=True
    )
    latitude = serializers.FloatField(
        allow_null=True, required=False, min_value=-90, max_value=90
    )
    longitude = serializers.FloatField(
        allow_null=True, required=False, min_value=-180, max_value=180
    )


class OrganismeUpsertInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, allow_null=True)
    nom = serializers.CharField(max_length=255)
    versant = serializers.ChoiceField(choices=[v.value for v in Verse])
    siret = serializers.CharField(max_length=14)
    parent_id = serializers.UUIDField(allow_null=True)
    external_id = serializers.CharField(max_length=50)
    referentiel = serializers.CharField(max_length=50)
    millesime = serializers.CharField(max_length=25)
    gestion_ats = serializers.BooleanField(required=False, allow_null=True)
    date_creation = serializers.DateField(required=False, allow_null=True)
    date_derniere_activite = serializers.DateField(required=False, allow_null=True)
    localisation = OrganismeLocalisationInputSerializer(required=False, allow_null=True)


class UpsertOrganismesRequestSerializer(serializers.Serializer):
    organismes = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
    )


class UpsertOrganismesResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.DictField())
