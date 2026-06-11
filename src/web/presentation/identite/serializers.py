from rest_framework import serializers


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField()
    prenom = serializers.CharField()
    nom = serializers.CharField()
