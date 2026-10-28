import gettext
from urllib.parse import urlparse

import pycountry
from drf_spectacular.utils import extend_schema_field
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.country import Country
from referentiel.value_objects.departement_region import (
    department_belongs_to_region,
)
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
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.required_document import RequiredDocument
from referentiel.value_objects.verse import Verse
from rest_framework import serializers

from application.ingestion.services.list_public_organismes import (
    PUBLIC_ORGANISME_REFERENTIELS,
)
from application.ingestion.services.metier_functional_areas import (
    get_metier_functional_areas,
)
from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from presentation.api.serializers import GenericErrorSerializer
from presentation.commons.markdown import forbidden_markdown
from presentation.commons.serializers import (
    LocalisationSerializer,
    OrganismeSerializer,
    validate_country_code,
)

LEGIFRANCE_HOSTS = frozenset({"legifrance.gouv.fr", "www.legifrance.gouv.fr"})


def _parse_enum_list(value, enum_cls, error_label, excluded=frozenset()):
    if not value:
        return None

    allowed = {e.name for e in enum_cls if e not in excluded}
    requested = [part.strip() for part in value.split(",") if part.strip()]
    invalid = [part for part in requested if part not in allowed]
    if invalid:
        raise serializers.ValidationError(
            "Valeurs de {} invalides : {}. Valeurs autorisées : {}.".format(
                error_label, ", ".join(invalid), ", ".join(sorted(allowed))
            )
        )

    return [enum_cls[part] for part in requested]


class _CommaSeparatedEnumField(serializers.MultipleChoiceField):
    def __init__(self, enum_cls, error_label, excluded=frozenset(), **kwargs):
        self.enum_cls = enum_cls
        self.error_label = error_label
        self.excluded = excluded
        choices = [(e.name, e.value) for e in enum_cls if e not in excluded]
        kwargs.setdefault("default", None)
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            data = ",".join(data)
        return _parse_enum_list(data, self.enum_cls, self.error_label, self.excluded)


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


def _parse_code_list(value, valid_codes, error_label):
    if not value:
        return None

    requested = [part.strip().upper() for part in value.split(",") if part.strip()]
    invalid = [part for part in requested if part not in valid_codes]
    if invalid:
        raise serializers.ValidationError(
            "Valeurs de {} invalides : {}.".format(error_label, ", ".join(invalid))
        )

    return requested


class _CommaSeparatedCodeField(serializers.MultipleChoiceField):
    def __init__(self, code_labels, error_label, to_value_object, **kwargs):
        self.valid_codes = frozenset(code_labels)
        self.error_label = error_label
        self.to_value_object = to_value_object
        kwargs.setdefault("default", None)
        choices = sorted(code_labels.items(), key=lambda item: item[0])
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, (list, tuple)):
            data = ",".join(data)
        codes = _parse_code_list(data, self.valid_codes, self.error_label)
        return [self.to_value_object(code) for code in codes] if codes else None


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
    reference = serializers.CharField()
    source_id = serializers.UUIDField()
    titre = serializers.CharField(source="title")
    organisation = serializers.CharField(source="organization")
    nature_offre = serializers.CharField(source="offer_nature", allow_null=True)
    categories = serializers.ListField(child=serializers.CharField())
    debut_publication = serializers.DateTimeField(source="publication_date")
    url_offre = serializers.CharField(source="offer_url", allow_null=True)
    date_archivage = serializers.DateTimeField(source="archived_at", allow_null=True)


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
    nature_offre = _CommaSeparatedEnumField(
        OfferNature,
        "nature de l'offre",
        help_text="Valeurs séparées par une virgule (ex. `TITULAIRE_CONTRACTUEL`).",
        source="offer_nature",
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
    organisation = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=None,
        source="organization",
        help_text=(
            "Filtre sur l'organisme Talentsoft (`entityCode`), en incluant tous "
            "ses organismes descendants. Répéter le paramètre pour filtrer sur "
            "plusieurs organismes (ex. `?organisation=ORG1&organisation=ORG2`)."
        ),
    )
    debut_publication = serializers.IntegerField(
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
        Category, "catégorie", excluded={Category.HORS_CATEGORIE}
    )
    verse = _CommaSeparatedEnumField(Verse, "versant")
    contractType = _CommaSeparatedEnumField(
        OfferNature, "type de contrat", source="offer_nature"
    )
    experienceLevel = _CommaSeparatedEnumField(
        ExperienceLevel, "niveau d'expérience", source="experience_level"
    )
    management = _CommaSeparatedEnumField(Management, "management")
    workingPlace = _CommaSeparatedEnumField(
        WorkingPlace, "lieu de travail", source="working_place"
    )
    region = _CommaSeparatedCodeField(
        REGION_NAMES, "région", lambda code: Region(code=code)
    )
    department = _CommaSeparatedCodeField(
        DEPARTMENT_NAMES, "département", lambda code: Department(code=code)
    )
    country = _CommaSeparatedCodeField(COUNTRY_NAMES, "pays", Country)
    area = _CommaSeparatedEnumField(GeographicalArea, "zone géographique")
    domain = _CommaSeparatedCodeField(DOMAIN_NAMES, "domaine", lambda code: code)
    organization = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=None,
        help_text=(
            "Filtre sur l'organisme Talentsoft (`entityCode`), en incluant tous "
            "ses organismes descendants. Répéter le paramètre pour filtrer sur "
            "plusieurs organismes (ex. `?organization=ORG1&organization=ORG2`)."
        ),
    )
    publicationDate = serializers.IntegerField(
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

        return data


class OfferDetailQuerySerializer(serializers.Serializer):
    reference = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="La référence de l'offre.",
    )


class FakeTsCodedObjectSerializer(serializers.Serializer):
    code = serializers.IntegerField(allow_null=True)
    clientCode = serializers.CharField()
    label = serializers.CharField()
    active = serializers.BooleanField()
    parentCode = serializers.IntegerField(allow_null=True)
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
    professionalCategory = FakeTsCodedObjectSerializer(allow_null=True)
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
    entityCode = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_null=True)
    url = serializers.CharField(required=False, allow_null=True)
    phoneNumber = serializers.CharField(required=False, allow_null=True)
    postCode = serializers.CharField(required=False, allow_null=True)
    geolocation = FakeTsGeolocationSerializer(required=False, allow_null=True)
    parentName = serializers.CharField(required=False, allow_null=True)
    logoUrl = serializers.CharField(required=False, allow_null=True)
    maxDelayForConsent = serializers.IntegerField(required=False, allow_null=True)
    retentionPeriod = serializers.IntegerField(required=False, allow_null=True)
    generalConditions = serializers.CharField(required=False, allow_null=True)
    personalDataConsent = serializers.CharField(required=False, allow_null=True)

    def to_representation(self, instance):
        if not instance:
            return {}
        return super().to_representation(instance)


class FakeTsTalentsoftOrganismeSerializer(serializers.Serializer):
    entityCode = serializers.CharField(source="entity_code")
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    url = serializers.CharField(allow_null=True)
    phoneNumber = serializers.CharField(source="phone_number", allow_null=True)
    postCode = serializers.CharField(source="post_code", allow_null=True)
    geolocation = serializers.SerializerMethodField()
    parentName = serializers.CharField(source="parent_name", allow_null=True)
    logoUrl = serializers.CharField(source="logo_url", allow_null=True)
    maxDelayForConsent = serializers.IntegerField(
        source="max_delay_for_consent", allow_null=True
    )
    retentionPeriod = serializers.IntegerField(
        source="retention_period", allow_null=True
    )
    generalConditions = serializers.CharField(
        source="general_conditions", allow_null=True
    )
    personalDataConsent = serializers.CharField(
        source="personal_data_consent", allow_null=True
    )

    @extend_schema_field(FakeTsGeolocationSerializer(allow_null=True))
    def get_geolocation(self, organisme: TalentsoftOrganismeModel) -> dict | None:
        if organisme.latitude is None or organisme.longitude is None:
            return None
        return {"latitude": organisme.latitude, "longitude": organisme.longitude}


class FakeTsLanguageSerializer(serializers.Serializer):
    languageName = FakeTsCodedObjectSerializer()
    languageLevel = FakeTsCodedObjectSerializer()


class FakeTsDynamicFieldSerializer(serializers.Serializer):
    date1 = serializers.CharField(allow_null=True)
    shortText1 = serializers.CharField(allow_null=True)
    longText1 = serializers.CharField(allow_null=True)
    longText2 = serializers.CharField(allow_null=True)
    longText3 = serializers.CharField(allow_null=True)
    longText1Formatted = serializers.CharField(allow_null=True)
    longText2Formatted = serializers.CharField(allow_null=True)
    longText3Formatted = serializers.CharField(allow_null=True)


class FakeTsApplicantCriteriaSerializer(FakeTsDynamicFieldSerializer):
    customCodeTable1 = FakeTsCodedObjectSerializer(
        allow_null=True,
        help_text="Documents à transmettre. `null` si l'offre n'en demande aucun "
        "ou si la combinaison n'existe pas dans le référentiel Talentsoft.",
    )


class FakeTsCustomFieldsSerializer(serializers.Serializer):
    offer = FakeTsDynamicFieldSerializer()
    description = FakeTsDynamicFieldSerializer()
    applicantCriteria = FakeTsApplicantCriteriaSerializer()
    location = FakeTsDynamicFieldSerializer()
    offerCustomBlock1 = FakeTsDynamicFieldSerializer()
    origin = FakeTsDynamicFieldSerializer()


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
    customFields = FakeTsCustomFieldsSerializer()


class LocalisationInputSerializer(LocalisationSerializer):
    pays = serializers.CharField(
        max_length=3,
        min_length=3,
        help_text="Code pays ISO 3166-1 alpha-3, en majuscules (ex. `FRA`).",
    )
    region = serializers.ChoiceField(
        choices=sorted(Region.VALID_CODES, key=lambda x: x),
        allow_blank=True,
        help_text=(
            "Code INSEE de la région, `DOM` ou `TOM`. Le département doit "
            "appartenir à cette région : `DOM` avec un département d'outre-mer, "
            "`TOM` avec une collectivité d'outre-mer."
        ),
    )
    latitude = serializers.FloatField(
        allow_null=True, required=False, min_value=-90, max_value=90
    )
    longitude = serializers.FloatField(
        allow_null=True, required=False, min_value=-180, max_value=180
    )

    def validate(self, data):
        if data.get("pays") == "FRA" and not (
            data.get("region") and data.get("departement")
        ):
            raise serializers.ValidationError(
                "La région et le département sont obligatoires "
                "pour une offre localisée en France."
            )
        if data.get("region") and data.get("departement"):
            region = Region(code=data["region"])
            department = Department(code=data["departement"])
            if not department_belongs_to_region(department, region):
                raise serializers.ValidationError(
                    f"Le département {_code_and_name(department)} "
                    f"n'appartient pas à la région {_code_and_name(region)}."
                )
        return data


def _code_and_name(value: Region | Department) -> str:
    if value.name == value.code:
        return value.code
    return f"{value.code} ({value.name})"


CONTACT_ROLES = ["principal", "autre"]


class ContactSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=CONTACT_ROLES)
    texte = serializers.CharField()
    emails = serializers.ListField(child=serializers.EmailField())


class OfferDetailResponseSerializer(serializers.Serializer):
    reference = serializers.CharField()
    source_id = serializers.UUIDField()
    titre = serializers.CharField(source="title")
    titre_long = serializers.CharField(source="long_title", allow_null=True)
    organisation = serializers.CharField(source="organization")
    employeur = serializers.CharField(source="employer", allow_null=True)
    profil = serializers.CharField(source="profile")
    mission = serializers.CharField()
    complements = serializers.CharField(allow_null=True)
    conditions_exercice = serializers.CharField(
        source="exercise_conditions", allow_null=True
    )
    descriptif_service = serializers.CharField(
        source="service_description", allow_null=True
    )
    versant = serializers.CharField(source="verse", allow_null=True)
    categories = serializers.ListField(child=serializers.CharField())
    nature_offre = serializers.CharField(source="offer_nature", allow_null=True)
    type_contrat = serializers.CharField(source="contract_kind", allow_null=True)
    vacance_poste = serializers.CharField(source="job_vacancy", allow_null=True)
    url_offre = serializers.CharField(source="offer_url", allow_null=True)
    url_candidature = serializers.CharField(source="application_url", allow_null=True)
    email_candidature = serializers.EmailField(
        source="application_email", allow_null=True
    )
    localisation = serializers.SerializerMethodField()
    criteres = serializers.SerializerMethodField()
    conditions = serializers.DictField(allow_null=True)
    contacts = ContactSerializer(many=True, allow_null=True)
    debut_publication = serializers.DateTimeField(source="publication_date")
    fin_publication = serializers.DateTimeField(
        source="end_publication_date", allow_null=True
    )
    debut_contrat = serializers.SerializerMethodField()
    fin_candidature = serializers.DateTimeField(
        source="application_deadline", allow_null=True
    )
    debut_vacance_poste = serializers.DateTimeField(
        source="job_vacancy_date", allow_null=True
    )
    date_archivage = serializers.DateTimeField(source="archived_at", allow_null=True)

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
    def get_criteres(self, obj):
        return obj.criteria.to_dict() if obj.criteria else None

    @extend_schema_field(serializers.DateTimeField(allow_null=True))
    def get_debut_contrat(self, obj):
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
    statut = serializers.CharField()


class ListMetiersResponseSerializer(serializers.Serializer):
    libelle = serializers.CharField()
    description = serializers.CharField()
    domaine_fonctionnel_code = serializers.CharField()
    versants = serializers.ListField(child=serializers.CharField())
    activites = serializers.ListField(child=serializers.CharField(), allow_null=True)
    conditions_particulieres = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    code_emploi_csp = serializers.CharField(
        source="offer_family_code",
        help_text="Code CSP du RMFP, à renseigner dans `profession.metier` de "
        "l'API d'ingestion d'offres. Plusieurs métiers peuvent partager le même "
        "code. Toujours renseigné.",
    )


class ListMetiersFiltersSerializer(serializers.Serializer):
    domaine = serializers.CharField(default=None, max_length=3, source="domain")


class IdentityInputSerializer(serializers.Serializer):
    reference = serializers.CharField(
        help_text="Référence de l'offre, unique par source. La valeur `auto` "
        "demande à CSPLab de générer une référence au format CSP-AAAA-NNNNNN : elle "
        "crée toujours une nouvelle offre. Une référence au format CSP-AAAA-NNNNNN "
        "n'est acceptée que si elle désigne une offre existante de la source."
    )
    versant = serializers.ChoiceField(choices=[v.value for v in Verse])


class OrganismeInputSerializer(OrganismeSerializer):
    nom = serializers.CharField(
        help_text="Nom de l'organisme. Reprendre de préférence le `nom` renvoyé par "
        "`GET /api/v1/organismes`."
    )
    siret = serializers.CharField(
        max_length=14,
        allow_blank=True,
        help_text="SIRET de l'organisme, à retrouver avec `GET /api/v1/organismes` "
        "(filtres `nom` et `siret`).",
    )
    talentsoft_organisme_entity_code = serializers.CharField(
        max_length=50,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Ne doit être renseigné que par le service ingestion de CSPLab : "
        "refusé pour une authentification par JWT.",
    )

    def validate_talentsoft_organisme_entity_code(self, value):
        if not value:
            return value
        if not self.context.get("allow_talentsoft_organisme", False):
            raise serializers.ValidationError(
                "Champ réservé au service ingestion de CSPLab."
            )
        if not TalentsoftOrganismeModel.objects.by_entity_code(value).exists():
            raise serializers.ValidationError(
                f"Organisme Talentsoft inconnu : {value}."
            )
        return value


class ProfessionInputSerializer(serializers.Serializer):
    referentiel = serializers.ChoiceField(
        choices=[e.value for e in JobFamilyReferential],
        default=JobFamilyReferential.RMFPV2.value,
    )
    domaine = serializers.CharField(
        max_length=3,
        required=False,
        help_text="Code domaine fonctionnel RMFP, vérifié uniquement si "
        f"referentiel={JobFamilyReferential.RMFPV2.value}. Absent, il est déduit "
        "du métier ; renseigné, il doit correspondre au domaine du métier. "
        "Obligatoire si le code métier relève de plusieurs domaines "
        "(ex. `ERJUS008`, `ERTRA007`). Valeurs possibles : "
        + ", ".join(f"{e.value} ({e.label})" for e in DomaineFonctionnel)
        + ".",
    )
    metier = serializers.CharField(
        max_length=8,
        help_text="Code métier, vérifié uniquement si "
        f"referentiel={JobFamilyReferential.RMFPV2.value} : valeur du champ "
        "`code_emploi_csp` d'un métier renvoyé par l'API `/api/v1/metiers` "
        "(exemple : `ERAMT001`).",
    )
    code_emploi_local = serializers.CharField(
        max_length=50, required=False, allow_null=True
    )

    def validate(self, data):
        if data.get("referentiel") != JobFamilyReferential.RMFPV2.value:
            return data

        domaine = data.get("domaine")
        if domaine is not None and domaine not in {e.value for e in DomaineFonctionnel}:
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

        domaines = get_metier_functional_areas(metier)
        if not domaines:
            return data

        domaines_libelle = ", ".join(sorted(domaines))
        if domaine is None:
            if len(domaines) > 1:
                raise serializers.ValidationError(
                    {
                        "domaine": f"Le métier {metier} relève de plusieurs "
                        f"domaines ({domaines_libelle}) : renseigner l'un d'eux."
                    }
                )
            data["domaine"] = domaines.pop()
        elif domaine not in domaines:
            raise serializers.ValidationError(
                {
                    "domaine": f"Le domaine {domaine} ne correspond pas au métier "
                    f"{metier} ({domaines_libelle})."
                }
            )

        return data


_MARKDOWN_HELP_TEXT = (
    "Markdown (CommonMark), syntaxe comprise dans la limite. Les balises HTML et "
    "les liens autres que http, https et mailto sont refusés."
)


def _validate_markdown(value: str) -> None:
    errors = forbidden_markdown(value)
    if errors:
        raise serializers.ValidationError(errors)


class DescriptionInputSerializer(serializers.Serializer):
    mission = serializers.CharField(
        max_length=10000,
        allow_blank=True,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )
    profil = serializers.CharField(
        max_length=10000,
        allow_blank=True,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )
    employeur = serializers.CharField(
        max_length=3000,
        allow_blank=True,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )
    complements = serializers.CharField(
        max_length=5000,
        allow_blank=True,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )
    conditions_exercice = serializers.CharField(
        max_length=10000,
        allow_blank=True,
        required=False,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )
    descriptif_service = serializers.CharField(
        max_length=10000,
        allow_blank=True,
        required=False,
        help_text=_MARKDOWN_HELP_TEXT,
        validators=[_validate_markdown],
    )


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
        child=serializers.ChoiceField(
            choices=[(c.name, c.value) for c in RequiredDocument]
        ),
        required=False,
        help_text="Documents à transmettre pour candidater, sans doublon.",
    )
    competences_requises = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    langues = LanguageInputSerializer(many=True, required=False)

    def validate_documents_requis(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Chaque document ne peut être cité qu'une fois."
            )
        return value


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
    note_ouverture_poste_url = serializers.URLField(
        required=False,
        help_text="Lien vers l'avis de vacance publié au Journal officiel, "
        "en `https` sur `legifrance.gouv.fr`.",
    )

    def validate_note_ouverture_poste_url(self, value):
        url = urlparse(value)
        if url.scheme != "https" or url.hostname not in LEGIFRANCE_HOSTS:
            raise serializers.ValidationError(
                "Le lien doit être en https et pointer vers l'avis de vacance "
                "publié sur legifrance.gouv.fr."
            )
        return value


class ContactsInputSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=CONTACT_ROLES,
        help_text="`principal` pour la personne à contacter, `autre` pour une "
        "autre personne à contacter. Au plus un contact par rôle.",
    )
    texte = serializers.CharField(
        max_length=100,
        help_text="Contact en texte libre (nom, fonction, e-mail, téléphone…).",
    )
    emails = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=True,
        help_text="E-mails présents dans `texte`, dans l'ordre d'apparition. "
        "Liste vide si aucun.",
    )

    def validate_texte(self, value):
        if not any(char.isalnum() for char in value):
            raise serializers.ValidationError(
                "Le texte doit contenir au moins une lettre ou un chiffre."
            )
        return value

    def validate_emails(self, value):
        return list(dict.fromkeys(value))


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
    url_candidature = serializers.URLField(allow_null=True, required=False)
    email_candidature = serializers.EmailField(allow_null=True, required=False)

    # classification
    profession = ProfessionInputSerializer()
    categories = serializers.MultipleChoiceField(
        choices=[(c.name, c.value) for c in Category]
    )
    nature_offre = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in OfferNature]
    )
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractKind],
        allow_blank=True,
        allow_null=True,
        required=False,
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

    def validate_contacts(self, value):
        if value is None:
            return None
        roles = [contact["role"] for contact in value]
        if len(roles) != len(set(roles)):
            raise serializers.ValidationError("Au plus un contact par rôle.")
        return sorted(value, key=lambda contact: CONTACT_ROLES.index(contact["role"]))

    def validate(self, data):
        if bool(data.get("url_candidature")) == bool(data.get("email_candidature")):
            raise serializers.ValidationError(
                "Renseigner soit url_candidature, soit email_candidature, "
                "mais pas les deux."
            )
        return data


class UpsertOffersRequestSerializer(serializers.Serializer):
    source_id = serializers.UUIDField()
    offres = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
    )


class UpsertOfferStatusSerializer(serializers.Serializer):
    index = serializers.IntegerField(
        help_text="Position de l'offre dans `offres` du payload (à partir de 0)"
    )
    reference = serializers.CharField(
        help_text="Référence de l'offre, fournie ou générée"
    )
    statut = serializers.ChoiceField(
        choices=["creee", "mise_a_jour"],
        help_text="`creee` si l'offre a été créée, "
        "`mise_a_jour` si elle a été mise à jour",
    )


class UpsertOfferErrorSerializer(serializers.Serializer):
    index = serializers.IntegerField(
        help_text="Position de l'offre dans `offres` du payload (à partir de 0)"
    )
    offre = IdentityInputSerializer(help_text="Identification de l'offre rejetée")
    error = serializers.DictField(help_text="Détail de l'erreur de validation")


class UpsertOffersResponseSerializer(serializers.Serializer):
    creees = serializers.IntegerField(help_text="Nombre d'offres créées")
    mises_a_jour = serializers.IntegerField(help_text="Nombre d'offres mises à jour")
    offres = serializers.ListField(
        child=UpsertOfferStatusSerializer(),
        help_text=(
            "Offres créées ou mises à jour, avec leur référence finale "
            "(générée si `identification.reference` vaut `auto`)"
        ),
    )
    errors = serializers.ListField(
        child=UpsertOfferErrorSerializer(),
        help_text="Offres rejetées avec le détail de l'erreur",
    )


class OrganismeLocalisationInputSerializer(serializers.Serializer):
    zone_geographique = serializers.ChoiceField(
        choices=[(c.value, c.name) for c in GeographicalArea]
    )
    pays = serializers.CharField(
        max_length=3,
        min_length=3,
        help_text="Code pays ISO 3166-1 alpha-3, en majuscules (ex. `FRA`).",
    )
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

    def validate_pays(self, value: str) -> str:
        return validate_country_code(value)


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
    date_creation = serializers.DateTimeField(required=False, allow_null=True)
    date_derniere_activite = serializers.DateTimeField(required=False, allow_null=True)
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


class ListOrganismesFiltersSerializer(serializers.Serializer):
    versant = _CommaSeparatedEnumField(
        Verse,
        "versant",
        help_text="Valeurs séparées par une virgule (ex. `FPE,FPT`).",
        source="versants",
    )
    siret = serializers.CharField(
        required=False,
        min_length=14,
        max_length=14,
        help_text="SIRET exact de l'organisme (14 caractères).",
    )
    nom = serializers.CharField(
        required=False,
        max_length=255,
        help_text=(
            "Recherche partielle sur le nom, insensible à la casse et aux accents."
        ),
        source="name",
    )
    departement = serializers.ChoiceField(
        choices=sorted(Department.VALID_CODES),
        required=False,
        help_text="Code du département de l'organisme (ex. `75`, `2A`, `971`).",
        source="department",
    )
    referentiel = serializers.ChoiceField(
        choices=PUBLIC_ORGANISME_REFERENTIELS,
        required=False,
        help_text="Référentiel source de l'organisme.",
    )


class OrganismeLocalisationPublicSerializer(serializers.Serializer):
    zone_geographique = serializers.CharField(source="area")
    pays = serializers.CharField(source="country")
    region = serializers.CharField()
    departement = serializers.CharField(source="department")


class OrganismePublicSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(
        help_text="Nom de référence, à reprendre dans `organisation.nom` de l'API "
        "d'ingestion d'offres."
    )
    siret = serializers.CharField(
        help_text="SIRET à renseigner dans `organisation.siret` de l'API "
        "d'ingestion d'offres."
    )
    parent_id = serializers.UUIDField(
        allow_null=True, help_text="Identifiant de l'organisme parent."
    )
    referentiel = serializers.ChoiceField(
        choices=PUBLIC_ORGANISME_REFERENTIELS,
        help_text="Référentiel source. Avec "
        "`external_id`, identifie l'organisme pour la création, la mise à jour et "
        "la suppression.",
    )
    external_id = serializers.CharField(
        allow_null=True, help_text="Identifiant dans le référentiel source."
    )
    millesime = serializers.CharField(
        allow_null=True,
        help_text="Version du référentiel source dont provient l'organisme.",
    )
    localisation = OrganismeLocalisationPublicSerializer(allow_null=True)

    class Meta:
        model = OrganismeModel
        fields = [
            "id",
            "nom",
            "versant",
            "siret",
            "parent_id",
            "referentiel",
            "external_id",
            "millesime",
            "localisation",
        ]
        read_only_fields = fields


class OrganismeDeleteInputSerializer(serializers.Serializer):
    referentiel = serializers.CharField(max_length=50)
    external_id = serializers.CharField(max_length=50)


class SupprimerOrganismesRequestSerializer(serializers.Serializer):
    organismes = serializers.ListField(
        child=OrganismeDeleteInputSerializer(),
        min_length=1,
        max_length=100,
    )


class SupprimerOrganismesResponseSerializer(serializers.Serializer):
    deleted = serializers.IntegerField()
    not_found = serializers.ListField(child=serializers.DictField())


class TalentsoftOrganismeUpsertInputSerializer(serializers.Serializer):
    organisme_id = serializers.UUIDField(required=False, allow_null=True, default=None)
    entity_code = serializers.CharField(max_length=50)
    code = serializers.IntegerField()
    parent_code = serializers.IntegerField(required=False, allow_null=True)
    has_children = serializers.BooleanField(required=False, default=False)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    url = serializers.URLField(
        required=False, allow_null=True, allow_blank=True, max_length=500
    )
    phone_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=50
    )
    post_code = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=20
    )
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    parent_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=255
    )
    logo_url = serializers.URLField(
        required=False, allow_null=True, allow_blank=True, max_length=500
    )
    max_delay_for_consent = serializers.IntegerField(required=False, allow_null=True)
    retention_period = serializers.IntegerField(required=False, allow_null=True)
    general_conditions = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    personal_data_consent = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


@extend_schema_field(TalentsoftOrganismeUpsertInputSerializer(many=True))
class _TalentsoftOrganismeListField(serializers.ListField):
    pass


class UpsertTalentsoftOrganismesRequestSerializer(serializers.Serializer):
    talentsoft_organismes = _TalentsoftOrganismeListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
        help_text=(
            "Liste d'organismes Talentsoft à créer ou mettre à jour (min: 1, max: 100)."
        ),
    )


class UpsertTalentsoftOrganismesResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField(help_text="Nombre d'organismes Talentsoft créés")
    updated = serializers.IntegerField(
        help_text="Nombre d'organismes Talentsoft mis à jour"
    )
    errors = serializers.ListField(
        child=serializers.DictField(),
        help_text="Organismes Talentsoft rejetés avec le détail de l'erreur",
    )
