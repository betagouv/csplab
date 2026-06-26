from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
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


class RecrutementSerializer(serializers.Serializer):
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


class RecrutementActifSerializer(RecrutementSerializer):
    candidatures = CandidaturesActivesSerializer(allow_null=True)


class RecrutementArchiveSerializer(RecrutementSerializer):
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
    etape = EtapeRecrutementSerializer()


# ---------------------------------------------------------------------------
# Serializers pour les notes attachées à une candidature
# ---------------------------------------------------------------------------


class NoteSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    candidature_uuid = serializers.UUIDField()
    message = serializers.CharField()
    mis_a_jour_le = serializers.DateTimeField()
    mis_a_jour_par_id = serializers.UUIDField()


class CreerNoteSerializer(serializers.Serializer):
    message = serializers.CharField()


class EditerNoteSerializer(serializers.Serializer):
    message = serializers.CharField()
