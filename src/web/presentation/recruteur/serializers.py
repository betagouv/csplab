from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
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


# ---------------------------------------------------------------------------
# Serializers pour la vue détail d'un recrutement (kanban / liste)
# ---------------------------------------------------------------------------


class LocalisationSerializer(serializers.Serializer):
    area = serializers.ChoiceField(
        choices=[(a.value, a.name) for a in GeographicalArea]
    )
    country = serializers.CharField(help_text="Code ISO Alpha-3 du pays (ex: FRA)")
    region = serializers.CharField(help_text="Code INSEE de la région (ex: 11)")
    department = serializers.CharField(help_text="Code INSEE du département (ex: 75)")
    label = serializers.CharField(allow_null=True, required=False)
    latitude = serializers.FloatField(allow_null=True, required=False)
    longitude = serializers.FloatField(allow_null=True, required=False)


class OrganismeRecruteurSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField()


class CandidatSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()


class CandidatureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    candidat = CandidatSerializer()


class EtapeRecrutementDetailedCandidaturesSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )
    candidatures = CandidatureSerializer(many=True)


class RecrutementDetailKanbanSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    date_publication = serializers.DateTimeField()
    localisation = LocalisationSerializer()
    organisme_recruteur = OrganismeRecruteurSerializer()
    categorie_offre = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in Category]
    )
    etapes = EtapeRecrutementDetailedCandidaturesSerializer(many=True)


class EtapeRecrutementDetailSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )


class CandidatureListeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    candidat = CandidatSerializer()
    etape = EtapeRecrutementDetailSerializer()


class RecrutementDetailListePageSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = CandidatureListeSerializer(many=True)


class RecrutementVueFilterSerializer(serializers.Serializer):
    vue = serializers.ChoiceField(
        choices=["kanban", "liste"], default="kanban", required=False
    )


class RecrutementListeFiltersSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, min_value=1, required=False)
    size = serializers.IntegerField(
        default=10, min_value=1, max_value=100, required=False
    )
