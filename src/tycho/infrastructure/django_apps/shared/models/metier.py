from uuid import NAMESPACE_DNS, uuid4, uuid5

from django.db import models

from domain.entities.metier import Metier
from domain.value_objects.verse import Verse
from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    IngresMetiersDocument,
)


class ReferencielMetier(models.TextChoices):
    RMFP_V1 = "RMFP_V1", "Référentiel des métiers de la fonction publique - version 1"


class MetierModel(models.Model):
    objects: models.Manager = models.Manager()

    VERSE_CHOICES = [(v.value, v.name) for v in Verse]
    REFERENCIEL_METIER = [(v.value, v.name) for v in ReferencielMetier]

    id = models.UUIDField(primary_key=True)

    external_id = models.CharField(max_length=8, unique=True, default="")
    code_emploi_csp = models.CharField(max_length=50, null=True, blank=True)

    libelle_emploi_csp = models.CharField(max_length=200, null=True, blank=True)
    referenciel_metier_id = models.CharField(
        max_length=20, choices=REFERENCIEL_METIER, null=True, blank=True
    )
    libelle_court = models.CharField(max_length=200)
    libelle_long = models.CharField(max_length=500)
    definition_synthetique = models.TextField(null=True, blank=True)

    code_domaine_fonctionnel = models.CharField(max_length=3)
    libelle_domaine_fonctionnel = models.CharField(max_length=200)
    code_famille = models.CharField(max_length=6)
    libelle_famille = models.CharField(max_length=200)

    versants = models.JSONField(default=list, null=True, blank=True)

    conditions_particulieres = models.JSONField(default=list, null=True, blank=True)

    activites = models.JSONField(default=list)

    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "metiers"
        verbose_name = "Métier"
        verbose_name_plural = "Métiers"
        indexes = [
            models.Index(fields=["external_id", "code_emploi_csp"]),
        ]

    def to_entity(self):
        versants = (
            [Verse(verse) for verse in self.versants if verse] if self.versants else []
        )

        namespace = uuid5(NAMESPACE_DNS, "csplab.domaines-fonctionnels")
        domaine_fonctionnel_uuid = uuid5(namespace, self.code_domaine_fonctionnel)

        return Metier(
            id=self.id,
            libelle=self.libelle_long,
            description=self.definition_synthetique or "",
            domaine_fonctionnel=domaine_fonctionnel_uuid,
            versants=versants,
            activites=self.activites or [],
            conditions_particulieres=self.conditions_particulieres,
        )

    @classmethod
    def from_entity(cls, metier):

        versants = (
            [verse.value for verse in metier.versants] if metier.versants else None
        )

        return cls(
            id=metier.id,
            external_id=getattr(metier, "external_id", str(metier.id)),
            libelle_court=metier.libelle,
            libelle_long=metier.libelle,
            definition_synthetique=metier.description,
            code_domaine_fonctionnel=str(metier.domaine_fonctionnel),
            versants=versants,
            activites=metier.activites,
            conditions_particulieres=metier.conditions_particulieres,
        )

    @classmethod
    def _dto_to_model_data(cls, document: IngresMetiersDocument) -> dict:
        activites = []
        if document.competences.activitesDeLEr:
            for activite in document.competences.activitesDeLEr:
                if activite.commentaire:
                    activites_list = [
                        act.strip()
                        for act in activite.commentaire.split("!N!")
                        if act.strip()
                    ]
                    activites.extend(activites_list)

        # Extraction des versants
        versants = []
        if document.definitions.fonctionPublique.PFE == "1":
            versants.append("FPE")
        if document.definitions.fonctionPublique.FPT == "1":
            versants.append("FPT")
        if document.definitions.fonctionPublique.FPH == "1":
            versants.append("FPH")

        conditions_particulieres = []
        if document.competences.conditionsParticulieresDExerciceDAcces:
            for (
                condition
            ) in document.competences.conditionsParticulieresDExerciceDAcces:
                if condition.commentaire:
                    conditions_particulieres.append(condition.commentaire)

        return {
            "id": uuid4(),
            "external_id": document.identifiant,
            "code_emploi_csp": document.definitions.emploiDeReferenceCSP.codeEmploiCSP,
            "libelle_emploi_csp": (
                document.definitions.emploiDeReferenceCSP.libelleEmploiCSP
            ),
            "referenciel_metier_id": "RMFP_V1",
            "libelle_court": document.definitions.libelles.libelleCourt,
            "libelle_long": document.definitions.libelles.libelleLong,
            "definition_synthetique": (
                document.definitions.definitionSynthetiqueDeLEr.definition
            ),
            "code_domaine_fonctionnel": (
                document.definitions.domaineFonctionnel_Famille.codeDomaineFonctionnel
            ),
            "libelle_domaine_fonctionnel": (
                document.definitions.domaineFonctionnel_Famille.libelleDomaineFonctionnel
            ),
            "code_famille": document.definitions.domaineFonctionnel_Famille.codeFamille,
            "libelle_famille": (
                document.definitions.domaineFonctionnel_Famille.libelleFamille
            ),
            "versants": versants,
            "activites": activites,
            "conditions_particulieres": conditions_particulieres,
        }
