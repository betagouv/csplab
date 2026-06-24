from drf_spectacular.utils import extend_schema_field
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_conditions import (
    JobVacancy,
    Management,
    OpenToMilitary,
    WorkingPlace,
    WorkingTime,
)
from referentiel.value_objects.verse import Verse
from rest_framework import serializers

from presentation.api.serializers import GenericErrorSerializer
from presentation.commons.serializers import LocalisationSerializer, OrganismeSerializer


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
    active = serializers.BooleanField(default=True)
    external_id_contains = serializers.CharField(default=None)


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
    criteria = serializers.DictField(allow_null=True)
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
    domain = serializers.CharField(default=None, max_length=3)


class IdentityInputSerializer(serializers.Serializer):
    reference = serializers.CharField()
    versant = serializers.ChoiceField(choices=[v.value for v in Verse])


class OrganismeInputSerializer(OrganismeSerializer):
    siret = serializers.CharField(max_length=14, allow_blank=True)


class ProfessionInputSerializer(serializers.Serializer):
    domaine = serializers.CharField(max_length=3)  # code domaine fonctionnel
    metier = serializers.CharField(max_length=8)


class DescriptionInputSerializer(serializers.Serializer):
    mission = serializers.CharField(max_length=10000)
    profil = serializers.CharField(max_length=10000)
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
        choices=[(c.name, c.value) for c in Management],
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
