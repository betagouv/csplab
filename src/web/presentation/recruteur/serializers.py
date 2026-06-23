from referentiel.value_objects.contract_type import ContractKind, ContractType
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


class UpdateEtapeRecrutementSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField(required=False)
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )


class OrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField()


class RecrutementsFiltersSerializer(serializers.Serializer):
    filtre = serializers.ChoiceField(
        choices=["actifs", "archives"],
        default="actifs",
        required=False,
    )
    page = serializers.IntegerField(default=1, min_value=1, required=False)
    size = serializers.IntegerField(
        default=10, min_value=1, max_value=100, required=False
    )


class ResponsableSerializer(serializers.Serializer):
    nom = serializers.CharField()


class CandidaturesActivesSerializer(serializers.Serializer):
    total = serializers.IntegerField(allow_null=True)
    a_traiter = serializers.IntegerField(allow_null=True)
    en_cours = serializers.IntegerField(allow_null=True)


class RecrutementActifSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    reference_csp = serializers.CharField()
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractType],
        allow_null=True,
    )
    kind_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractKind],
        allow_null=True,
    )
    date_publication = serializers.DateTimeField()
    responsables = ResponsableSerializer(many=True)
    derniere_activite = serializers.DateTimeField()
    candidatures = CandidaturesActivesSerializer(allow_null=True)


class RecrutementArchiveSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    reference_csp = serializers.CharField()
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractType],
        allow_null=True,
    )
    kind_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractKind],
        allow_null=True,
    )
    date_publication = serializers.DateTimeField()
    responsables = ResponsableSerializer(many=True)
    derniere_activite = serializers.DateTimeField()
    finalise = serializers.BooleanField()
    recrute = serializers.CharField(allow_null=True)


class RecrutementActifPageSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = RecrutementActifSerializer(many=True)


class RecrutementArchivePageSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = RecrutementArchiveSerializer(many=True)
