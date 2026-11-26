from pydantic import TypeAdapter, ValidationError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region
from rest_framework import serializers

from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.value_objects.etape_action import EtapeAction

_country_adapter = TypeAdapter(Country)

INVALID_COUNTRY_CODE = (
    "Code pays invalide, un code ISO 3166-1 alpha-3 en majuscules "
    "est attendu (ex. FRA)."
)


def validate_country_code(value: str) -> str:
    error = serializers.ValidationError(INVALID_COUNTRY_CODE)
    if value != value.upper():
        raise error
    try:
        _country_adapter.validate_python(value)
    except ValidationError as e:
        raise error from e
    return value


class LocalisationSerializer(serializers.Serializer):
    zone_geographique = serializers.ChoiceField(
        choices=[(c.value, c.name) for c in GeographicalArea]
    )
    pays = serializers.CharField(max_length=3, min_length=3)
    region = serializers.ChoiceField(
        choices=sorted(Region.VALID_CODES, key=lambda x: x),
        allow_null=True,
    )
    departement = serializers.ChoiceField(
        choices=sorted(Department.VALID_CODES, key=lambda x: x),
        allow_null=True,
    )
    localisation_label = serializers.CharField(max_length=500, allow_blank=True)
    latitude = serializers.FloatField(allow_null=True, min_value=-90, max_value=90)
    longitude = serializers.FloatField(allow_null=True, min_value=-180, max_value=180)

    def validate_pays(self, value: str) -> str:
        return validate_country_code(value)


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField(max_length=14)


def etape_actions_field() -> serializers.ListField:
    return serializers.ListField(
        child=serializers.ChoiceField(
            choices=[(action.value, action.value) for action in EtapeAction]
        ),
        read_only=True,
    )


def authorized_actions_field() -> serializers.ListField:
    return serializers.ListField(
        child=serializers.ChoiceField(
            choices=[(action.value, action.value) for action in PermissionAction]
        ),
        read_only=True,
    )
