from rest_framework import serializers

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel


class OrganismeRoleSerializer(serializers.ModelSerializer):
    organisme_uuid = serializers.UUIDField(source="organisme_id")
    nom = serializers.CharField(source="organisme.nom")
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )

    class Meta:
        model = OrganismeAgentModel
        fields = ["organisme_uuid", "nom", "role"]


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")
    is_staff = serializers.BooleanField(source="utilisateur.is_staff")
    organisme_roles = OrganismeRoleSerializer(many=True)
