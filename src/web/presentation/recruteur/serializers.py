from rest_framework import serializers

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


class EtapeRecrutementSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField()
