from uuid import UUID

from django.db.models import Prefetch

from application.recruteur.dtos.recrutement_read_models import (
    CandidatDto,
    CandidatureKanbanDto,
    EtapeKanbanReadModel,
    RecrutementKanbanReadModel,
)
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementModel,
)


class PostgresRecrutementQueryService(IRecrutementQueryService):
    def get_kanban_by_recrutement(
        self, organisme_id: UUID, recrutement_id: UUID
    ) -> RecrutementKanbanReadModel | None:
        recrutement = (
            RecrutementModel.objects.filter(
                pk=recrutement_id, organisme_id=organisme_id
            )
            .prefetch_related(
                Prefetch(
                    "etapes",
                    queryset=EtapeModel.objects.all().prefetch_related(
                        Prefetch(
                            "candidatures",
                            queryset=CandidatureModel.objects.select_related(
                                "candidat__utilisateur"
                            ).order_by("created_at"),
                        )
                    ),
                )
            )
            .first()
        )
        if recrutement is None:
            return None

        etapes_by_id = {str(etape.id): etape for etape in recrutement.etapes.all()}
        etapes_ordonnees = [
            etapes_by_id[etape_id]
            for etape_id in recrutement.ordre_etapes
            if etape_id in etapes_by_id
        ]

        return RecrutementKanbanReadModel(
            offer_id=recrutement.offre_id,
            etapes=[
                EtapeKanbanReadModel(
                    etape_uuid=etape.id,
                    nom=etape.nom,
                    categorie=CategorieEtapeRecrutement(etape.categorie).name,
                    candidatures=[
                        CandidatureKanbanDto(
                            uuid=candidature.id,
                            date_soumission=candidature.created_at,
                            date_derniere_activite=candidature.updated_by_recruteur
                            or candidature.updated_at,
                            candidat=CandidatDto(
                                uuid=candidature.candidat_id,
                                nom=candidature.candidat.utilisateur.last_name,
                                prenom=candidature.candidat.utilisateur.first_name,
                            ),
                        )
                        for candidature in etape.candidatures.all()
                    ],
                )
                for etape in etapes_ordonnees
            ],
        )
