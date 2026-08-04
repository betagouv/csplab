from pydantic import TypeAdapter, ValidationError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region
from rest_framework import serializers

_country_adapter = TypeAdapter(Country)


class LocalisationSerializer(serializers.Serializer):
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
    latitude = serializers.FloatField(allow_null=True, min_value=-90, max_value=90)
    longitude = serializers.FloatField(allow_null=True, min_value=-180, max_value=180)

    def validate_pays(self, value: str) -> str:
        try:
            _country_adapter.validate_python(value)
        except ValidationError as e:
            raise serializers.ValidationError(
                "Code pays invalide, un code ISO 3166-1 alpha-3 est attendu."
            ) from e
        return value


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField(max_length=14)
