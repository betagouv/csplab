from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region
from rest_framework import serializers


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
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField(max_length=14)
