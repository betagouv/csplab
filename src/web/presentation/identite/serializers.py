from rest_framework import serializers

from presentation.commons.serializers import authorized_actions_field


class UtilisateurOrganismeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    authorized_actions = authorized_actions_field()


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")
    authorized_actions = authorized_actions_field()
    organismes = UtilisateurOrganismeSerializer(many=True)
