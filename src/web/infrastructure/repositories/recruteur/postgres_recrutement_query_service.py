from datetime import datetime
from typing import cast
from uuid import UUID

from django.db.models import Count, F, Max, Prefetch, Q
from django.db.models.functions import Coalesce

from application.recruteur.dtos.recrutement_read_models import (
    CandidaturesCompteurDto,
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
    ResponsableDto,
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
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.mappers.queryset_page_mapper import QuerySetPageMapper


class PostgresRecrutementQueryService(IRecrutementQueryService):
    def get_actifs_by_organisme(
        self, organisme_id: UUID
    ) -> QuerySetPageMapper[RecrutementActifsReadModel]:
        qs = (
            RecrutementModel.objects.filter(
                organisme_id=organisme_id,
                offre__archived_at__isnull=True,
            )
            .select_related("offre")
            .prefetch_related(
                Prefetch(
                    "responsables_liaisons",
                    queryset=RecrutementAgentModel.objects.select_related(
                        "agent__utilisateur"
                    ),
                )
            )
            .annotate(
                derniere_activite=Coalesce(
                    Max("etapes__candidatures__updated_at"),
                    F("offre__publication_date"),
                ),
                candidatures_total=Count("etapes__candidatures"),
                candidatures_a_traiter=Count(
                    "etapes__candidatures",
                    filter=Q(etapes__categorie=CategorieEtapeRecrutement.ENTREE.value),
                ),
                candidatures_en_cours=Count(
                    "etapes__candidatures",
                    filter=Q(
                        etapes__categorie=CategorieEtapeRecrutement.EN_COURS.value
                    ),
                ),
            )
        )

        def _mapper(model: RecrutementModel) -> RecrutementActifsReadModel:
            responsables = [
                ResponsableDto(
                    nom=(
                        f"{liaison.agent.utilisateur.first_name} "
                        f"{liaison.agent.utilisateur.last_name}"
                    ).strip()
                )
                for liaison in model.responsables_liaisons.all()  # type: ignore[attr-defined]
            ]
            return RecrutementActifsReadModel(
                offer_id=model.offre_id,  # type: ignore[attr-defined]
                intitule=model.offre.title,
                reference_csp=model.offre.code_emploi_csp or "",
                type_contrat=model.offre.contract_type or "",
                date_publication=model.offre.publication_date,
                responsables=responsables,
                derniere_activite=cast(datetime, model.derniere_activite),  # type: ignore[attr-defined]
                candidatures=CandidaturesCompteurDto(
                    total=cast(int, model.candidatures_total) or 0,  # type: ignore[attr-defined]
                    a_traiter=cast(int, model.candidatures_a_traiter) or 0,  # type: ignore[attr-defined]
                    en_cours=cast(int, model.candidatures_en_cours) or 0,  # type: ignore[attr-defined]
                ),
            )

        return QuerySetPageMapper(qs, mapper=_mapper)

    def get_archives_by_organisme(
        self, organisme_id: UUID
    ) -> QuerySetPageMapper[RecrutementArchivesReadModel]:
        qs = (
            RecrutementModel.objects.filter(
                organisme_id=organisme_id,
                offre__archived_at__isnull=False,
            )
            .select_related("offre")
            .prefetch_related(
                Prefetch(
                    "responsables_liaisons",
                    queryset=RecrutementAgentModel.objects.select_related(
                        "agent__utilisateur"
                    ),
                ),
                Prefetch(
                    "etapes",
                    queryset=EtapeModel.objects.filter(
                        categorie=CategorieEtapeRecrutement.ACCEPTE.value
                    ).prefetch_related(
                        Prefetch(
                            "candidatures",
                            queryset=CandidatureModel.objects.select_related(
                                "candidat__utilisateur"
                            ),
                        )
                    ),
                    to_attr="etapes_acceptees",
                ),
            )
            .annotate(
                nb_candidatures_acceptees=Count(
                    "etapes__candidatures",
                    filter=Q(etapes__categorie=CategorieEtapeRecrutement.ACCEPTE.value),
                ),
            )
        )

        def _mapper(model: RecrutementModel) -> RecrutementArchivesReadModel:
            responsables = [
                ResponsableDto(
                    nom=(
                        f"{liaison.agent.utilisateur.first_name} "
                        f"{liaison.agent.utilisateur.last_name}"
                    ).strip()
                )
                for liaison in model.responsables_liaisons.all()  # type: ignore[attr-defined]
            ]
            finalise = cast(int, model.nb_candidatures_acceptees) > 0  # type: ignore[attr-defined]
            etapes_acceptees = model.etapes_acceptees  # type: ignore[attr-defined]
            recrute = None
            if etapes_acceptees:
                candidatures = etapes_acceptees[0].candidatures.all()
                if candidatures:
                    candidat = candidatures[0].candidat
                    recrute = (
                        f"{candidat.utilisateur.first_name} "
                        f"{candidat.utilisateur.last_name}"
                    ).strip()

            return RecrutementArchivesReadModel(
                offer_id=model.offre_id,  # type: ignore[attr-defined]
                intitule=model.offre.title,
                reference_csp=model.offre.code_emploi_csp or "",
                type_contrat=model.offre.contract_type or "",
                date_archivage=cast(datetime, model.offre.archived_at),
                responsables=responsables,
                finalise=finalise,
                recrute=recrute,
            )

        return QuerySetPageMapper(qs, mapper=_mapper)
