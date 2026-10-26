from rest_framework import serializers

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from presentation.commons.serializers import authorized_actions_field


# TODO(#1930): remove OrganismeRoleSerializer once the Vue front reads `organismes`
class OrganismeRoleSerializer(serializers.ModelSerializer):
    organisme_uuid = serializers.UUIDField(source="organisme_id")
    nom = serializers.CharField(source="organisme.nom")
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )

    class Meta:
        model = OrganismeAgentModel
        fields = ["organisme_uuid", "nom", "role"]


class UtilisateurOrganismeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    authorized_actions = authorized_actions_field()


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")
    # TODO(#1930): remove is_staff and organisme_roles once the Vue front reads
    # authorized_actions and organismes
    is_staff = serializers.BooleanField(source="utilisateur.is_staff")
    organisme_roles = OrganismeRoleSerializer(many=True)
    authorized_actions = authorized_actions_field()
    organismes = UtilisateurOrganismeSerializer(many=True)
