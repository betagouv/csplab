from rest_framework import serializers

from domain.recruteur.value_objects.roles import AgentOrganismeRole


class OrganismeRoleSerializer(serializers.Serializer):
    organisme_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField()
    prenom = serializers.CharField()
    nom = serializers.CharField()
    is_staff = serializers.BooleanField()
    organisme_roles = OrganismeRoleSerializer(many=True)
