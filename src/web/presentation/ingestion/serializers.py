from rest_framework import serializers

from domain.entities.offer import Offer
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractKind, ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.education_level import EducationLevel
from domain.value_objects.experience_level import ExperienceLevel
from domain.value_objects.language_level import LanguageLevel
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse


class GenericErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class ValidationErrorSerializer(serializers.Serializer):
    row = serializers.IntegerField()
    error = serializers.CharField()


class NoValidRowsErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
    validation_errors = ValidationErrorSerializer(many=True)


class ServerErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


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


class ArchiveOfferSuccessSerializer(serializers.Serializer):
    status = serializers.CharField()
class IdentityInputSerializer(serializers.Serializer):
    reference = serializers.CharField()
    source = serializers.CharField()
    verse = serializers.ChoiceField(choices=[v.value for v in Verse])


class OrganizationInputSerializer(serializers.Serializer):
    organization_name = serializers.CharField()
    organization_siret = serializers.CharField(max_length=15, allow_blank=True)


class ProfessionInputSerializer(serializers.Serializer):
    profession_domain = serializers.CharField(max_length=3)  # code domaine fonctionnel
    profession_detail = serializers.CharField()


class DescriptionInputSerializer(serializers.Serializer):
    mission = serializers.CharField(max_length=3000)
    profile = serializers.CharField(max_length=3000)
    employer = serializers.CharField(max_length=3000)
    additionnal = serializers.CharField(max_length=1500, allow_blank=True)


class LocalisationInputSerializer(serializers.Serializer):
    area_code = serializers.ChoiceField(
        choices=[(a.name, a.value) for a in GeographicalArea]
    )
    country_code = serializers.CharField(max_length=3, min_length=3)
    region_code = serializers.ChoiceField(
        choices=list(Region.VALID_CODES), allow_blank=True
    )
    department_code = serializers.ChoiceField(
        choices=list(Department.VALID_CODES), allow_blank=True
    )
    offer_location_label = serializers.CharField(max_length=500)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)

    def validate(self, data):
        if data.get("country_code") == "FRA" and not (
            data.get("region_code") and data.get("department_code")
        ):
            raise serializers.ValidationError(
                "Region and Department are mandatory when offer is located in France."
            )
        return data

    @staticmethod
    def to_domain_from_validated(data: dict) -> Localisation:
        return Localisation(
            area=GeographicalArea(data["area_code"]),
            region=Region(code=data["region_code"]),
            department=Department(code=data["department_code"]),
            country=Country(data["country_code"]),
        )


class LanguageInputSerializer(serializers.Serializer):
    language_iso_code = serializers.CharField(max_length=2)
    level = serializers.ChoiceField(choices=[(c.value, c.value) for c in LanguageLevel])


class CriteriaInputSerializer(serializers.Serializer):
    education_level = serializers.ChoiceField(
        choices=[(c.value, c.value) for c in EducationLevel], allow_blank=True
    )
    experience_level = serializers.ChoiceField(
        choices=[(c.value, c.value) for c in ExperienceLevel], allow_blank=True
    )
    specializations = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    national_diploma = serializers.CharField(allow_blank=True)
    required_documents = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    expected_skills = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    language = LanguageInputSerializer(many=True, allow_null=True)


class ConditionsInputSerializer(serializers.Serializer):
    salary_civil_servant = serializers.CharField(max_length=100, allow_blank=True)
    salary_contractor = serializers.CharField(max_length=100, allow_blank=True)
    job_beginning_date = serializers.DateTimeField(allow_null=True)
    job_end_date = serializers.DateTimeField(allow_null=True)
    contract_duration = serializers.CharField(allow_blank=True)
    working_time = serializers.BooleanField()  # temps plein / partiel
    open_to_military = serializers.BooleanField()
    working_place = serializers.BooleanField()  # sur site / teletravail
    management = serializers.BooleanField()
    additionnal_infos = serializers.CharField(max_length=1500, allow_blank=True)
    legal_basis = serializers.CharField(max_length=1500, allow_blank=True)
    vacancy_notice_url = serializers.URLField(allow_null=True)


class ContactsInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PublicationInputSerializer(serializers.Serializer):
    publication_start_date = serializers.DateTimeField()
    publication_end_date = serializers.DateTimeField()
    application_end_date = serializers.DateTimeField(allow_null=True)
    vacancy_start_date = serializers.DateTimeField(allow_null=True)


class OffersInputSerializer(serializers.Serializer):
    identity = IdentityInputSerializer()

    # general infos
    title = serializers.CharField(max_length=150)
    long_title = serializers.CharField(max_length=1500)
    organization = OrganizationInputSerializer()
    offer_url = serializers.URLField(allow_null=True)
    application_url = serializers.URLField(allow_null=True)

    # classification
    profession = ProfessionInputSerializer()
    category = serializers.MultipleChoiceField(
        choices=[(c.value, c.value) for c in Category], allow_blank=True
    )
    contract_type = serializers.ChoiceField(
        choices=[(c.value, c.value) for c in ContractType]
    )
    contract_kind = serializers.MultipleChoiceField(
        choices=[(c.value, c.value) for c in ContractKind], allow_blank=True
    )
    status = serializers.BooleanField()  # vacant / susceptible d'être vacant

    description = DescriptionInputSerializer()
    localisation = LocalisationInputSerializer(many=True, allow_null=True)
    criteria = CriteriaInputSerializer(allow_null=True)
    conditions = ConditionsInputSerializer(allow_null=True)
    contacts = ContactsInputSerializer(many=True, allow_null=True)
    publication = PublicationInputSerializer()

    def to_domain(self) -> Offer:
        return self.to_domain_from_validated(self.validated_data)

    @staticmethod
    def to_domain_from_validated(data: dict) -> Offer:
        localisation_data = data.get("localisation")
        return Offer(
            external_id=f"{data['identity']['verse']}-{data['identity']['reference']}",
            title=data["title"],
            profile=data["profile_description"],
            mission=data["mission_description"],
            organization=data["organization_name"],
            publication_date=data["publication_start_date"],
            verse=Verse(data["identity"]["verse"]),
            category=Category(data["category"][0]) if data.get("category") else None,
            contract_type=ContractType(data["contract_type"]),
            offer_url=data.get("offer_url"),
            localisation=LocalisationInputSerializer.to_domain_from_validated(
                localisation_data
            )
            if localisation_data
            else None,
            beginning_date=LimitDate(data["job_beginning_date"])
            if data.get("job_beginning_date")
            else None,
            family_code=data.get("profession_detail"),
        )


class UpsertOffersResponseSerializer(serializers.Serializer):
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.DictField())
