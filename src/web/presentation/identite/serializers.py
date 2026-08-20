from rest_framework import serializers


class OrganismeRoleSerializer(serializers.Serializer):
    organisme_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    role = serializers.CharField()


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField()
    prenom = serializers.CharField()
    nom = serializers.CharField()
    organisme = OrganismeRoleSerializer(source="organismes", many=True)
