from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.department import Department
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
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import serializers


class GenericErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class ValidationErrorSerializer(GenericErrorSerializer):
    row = serializers.IntegerField()


class NoValidRowsErrorSerializer(GenericErrorSerializer):
    validation_errors = ValidationErrorSerializer(many=True)


class TokenErrorMessageSerializer(serializers.Serializer):
    token_class = serializers.CharField()
    token_type = serializers.CharField()
    message = serializers.CharField()


class TokenErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    messages = TokenErrorMessageSerializer(many=True)


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


class ListOffersErrorSerializer(serializers.Serializer):
    error = serializers.CharField


class ApiKeyErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class SourceSerializer(serializers.Serializer):
    source_id = serializers.UUIDField()
    type = serializers.CharField(source="type.value")
    client_id_front = serializers.CharField()
    client_id_back = serializers.CharField()
    base_url_front = serializers.URLField()
    base_url_back = serializers.URLField()


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
    source = serializers.CharField()
    versant = serializers.ChoiceField(choices=[v.value for v in Verse])


class OrganizationInputSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField(max_length=15, allow_blank=True)


class ProfessionInputSerializer(serializers.Serializer):
    domaine = serializers.CharField(max_length=3)  # code domaine fonctionnel
    metier = serializers.CharField(max_length=8)


class DescriptionInputSerializer(serializers.Serializer):
    mission = serializers.CharField(max_length=3000)
    profil = serializers.CharField(max_length=3000)
    employeur = serializers.CharField(max_length=3000)
    complements = serializers.CharField(max_length=1500, allow_blank=True)


class LocalisationInputSerializer(serializers.Serializer):
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
    localisation_label = serializers.CharField(max_length=500, allow_blank=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)

    def validate(self, data):
        if data.get("pays") == "FRA" and not (
            data.get("region") and data.get("departement")
        ):
            raise serializers.ValidationError(
                "La région et le département sont obligatoires"
                "pour une offre localisée en France."
            )
        return data


class LanguageInputSerializer(serializers.Serializer):
    iso_code = serializers.CharField(max_length=2)
    niveau = serializers.ChoiceField(choices=[(c.name, c.value) for c in LanguageLevel])


class CriteriaInputSerializer(serializers.Serializer):
    diplome_niveau = serializers.IntegerField(
        min_value=Diploma.MIN_DIPLOMA_LEVEL, max_value=Diploma.MAX_DIPLOMA_LEVEL
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
        choices=[(c.name, c.value) for c in OpenToMilitary]
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
    organisation = OrganizationInputSerializer()
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
    offres = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
    )


class UpsertOffersResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.DictField())
