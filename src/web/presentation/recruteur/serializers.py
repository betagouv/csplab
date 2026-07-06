from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from rest_framework import serializers

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from presentation.commons.serializers import LocalisationSerializer, OrganismeSerializer


class EtapeRecrutementSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )


class UpdateEtapeRecrutementSerializer(EtapeRecrutementSerializer):
    etape_uuid = serializers.UUIDField(required=False)


class ResponsableSerializer(serializers.Serializer):
    nom = serializers.CharField()


class CandidaturesActivesSerializer(serializers.Serializer):
    total = serializers.IntegerField(allow_null=True)
    a_traiter = serializers.IntegerField(allow_null=True)
    en_cours = serializers.IntegerField(allow_null=True)


class RecrutementsSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    reference_csp = serializers.CharField()
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractType],
        allow_null=True,
    )
    responsables = ResponsableSerializer(many=True)


class RecrutementsActifsSerializer(RecrutementsSerializer):
    date_publication = serializers.DateTimeField()
    candidatures = CandidaturesActivesSerializer(allow_null=True)
    derniere_activite = serializers.DateTimeField()


class RecrutementsArchivesSerializer(RecrutementsSerializer):
    date_archivage = serializers.DateTimeField()
    finalise = serializers.BooleanField()
    recrute = serializers.CharField(allow_null=True)


# ---------------------------------------------------------------------------
# Serializers pour la vue détail d'un recrutement (kanban / liste)
# ---------------------------------------------------------------------------


class CandidatSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()


class CandidatureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    date_derniere_activite = serializers.DateTimeField()
    candidat = CandidatSerializer()


class EtapeRecrutementDetailedCandidaturesSerializer(EtapeRecrutementSerializer):
    candidatures = CandidatureSerializer(many=True)


class RecrutementDetailKanbanSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    date_publication = serializers.DateTimeField()
    localisation = LocalisationSerializer()
    organisme_recruteur = OrganismeSerializer()
    categorie_offre = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in Category]
    )
    etapes = EtapeRecrutementDetailedCandidaturesSerializer(many=True)


class CandidatureListeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    candidat = CandidatSerializer()
    date_derniere_activite = serializers.DateTimeField()
    etape = EtapeRecrutementSerializer()
