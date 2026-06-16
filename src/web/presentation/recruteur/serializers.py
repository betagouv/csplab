from rest_framework import serializers


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.EmailField()
    siret = serializers.CharField()
