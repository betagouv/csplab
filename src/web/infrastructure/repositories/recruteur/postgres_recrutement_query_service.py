from datetime import datetime
from typing import cast
from uuid import UUID

from django.db.models import Count, F, Max, Prefetch, Q
from django.db.models.functions import Coalesce

from application.recruteur.dtos.recrutement_read_models import (
    AgentDto,
    CandidatDto,
    CandidatureKanbanDto,
    CandidatureListeReadModel,
    CandidaturesCompteurDto,
    EtapeDto,
    EtapeKanbanReadModel,
    LocalisationDto,
    OrganismeRecruteurDto,
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
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
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.mappers.queryset_page import QuerySetPage


class PostgresRecrutementQueryService(IRecrutementQueryService):
    def get_actifs_by_organisme(
        self, organisme_id: UUID, agent_id: UUID | None = None
    ) -> QuerySetPage[RecrutementActifsReadModel]:
        filters: dict = {
            "organisme_id": organisme_id,
            "offre__archived_at__isnull": True,
        }
        if agent_id is not None:
            filters["agents_liaisons__agent_id"] = str(agent_id)

        qs = (
            RecrutementModel.objects.filter(**filters)
            .select_related("offre")
            .prefetch_related(
                Prefetch(
                    "agents_liaisons",
                    queryset=RecrutementAgentModel.objects.select_related(
                        "agent__utilisateur"
                    ),
                )
            )
            .annotate(
                derniere_activite=Coalesce(  # todo extract business rules
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
            agents = [
                AgentDto(
                    nom=(
                        f"{liaison.agent.utilisateur.first_name} "
                        f"{liaison.agent.utilisateur.last_name}"
                    ).strip()
                )
                for liaison in model.agents_liaisons.all()  # type: ignore[attr-defined]
            ]
            return RecrutementActifsReadModel(
                offer_id=model.offre_id,  # type: ignore[attr-defined]
                intitule=model.offre.title,
                reference_csp=model.offre.code_emploi_csp or "",
                type_contrat=model.offre.contract_type or "",
                date_publication=model.offre.publication_date,
                agents=agents,
                derniere_activite=cast(datetime, model.derniere_activite),  # type: ignore[attr-defined]
                candidatures=CandidaturesCompteurDto(
                    total=cast(int, model.candidatures_total) or 0,  # type: ignore[attr-defined]
                    a_traiter=cast(int, model.candidatures_a_traiter) or 0,  # type: ignore[attr-defined]
                    en_cours=cast(int, model.candidatures_en_cours) or 0,  # type: ignore[attr-defined]
                ),
            )

        return QuerySetPage(qs, mapper=_mapper)

    def get_archives_by_organisme(
        self, organisme_id: UUID, agent_id: UUID | None = None
    ) -> QuerySetPage[RecrutementArchivesReadModel]:
        filters: dict = {
            "organisme_id": organisme_id,
            "offre__archived_at__isnull": False,
        }
        if agent_id is not None:
            filters["agents_liaisons__agent_id"] = str(agent_id)

        qs = (
            RecrutementModel.objects.filter(**filters)
            .select_related("offre")
            .prefetch_related(
                Prefetch(
                    "agents_liaisons",
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
            agents = [
                AgentDto(
                    nom=(
                        f"{liaison.agent.utilisateur.first_name} "
                        f"{liaison.agent.utilisateur.last_name}"
                    ).strip()
                )
                for liaison in model.agents_liaisons.all()  # type: ignore[attr-defined]
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
                agents=agents,
                finalise=finalise,
                recrute=recrute,
            )

        return QuerySetPage(qs, mapper=_mapper)

    def get_candidatures_by_recrutement(
        self, organisme_id: UUID, recrutement_id: UUID
    ) -> QuerySetPage[CandidatureListeReadModel] | None:
        if not RecrutementModel.objects.filter(
            pk=recrutement_id, organisme_id=organisme_id
        ).exists():
            return None

        qs = (
            CandidatureModel.objects.filter(etape__recrutement_id=recrutement_id)
            .select_related("candidat__utilisateur", "etape")
            .order_by("etape__updated_at", "created_at")
        )

        def _mapper(candidature: CandidatureModel) -> CandidatureListeReadModel:
            return CandidatureListeReadModel(
                uuid=candidature.id,
                date_soumission=candidature.created_at,
                date_derniere_activite=candidature.updated_at,
                candidat=CandidatDto(
                    uuid=UUID(candidature.candidat_id),
                    nom=candidature.candidat.utilisateur.last_name,
                    prenom=candidature.candidat.utilisateur.first_name,
                ),
                etape=EtapeDto(
                    etape_uuid=candidature.etape.id,
                    nom=candidature.etape.nom,
                    categorie=CategorieEtapeRecrutement(
                        candidature.etape.categorie
                    ).name,
                ),
            )

        return QuerySetPage(qs, mapper=_mapper)

    def get_kanban_by_recrutement(
        self, organisme_id: UUID, recrutement_id: UUID
    ) -> RecrutementKanbanReadModel | None:
        recrutement = (
            RecrutementModel.objects.filter(
                pk=recrutement_id, organisme_id=organisme_id
            )
            .select_related("offre", "organisme")
            .prefetch_related(
                Prefetch(
                    "etapes",
                    queryset=EtapeModel.objects.prefetch_related(
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

        offre = recrutement.offre
        organisme = recrutement.organisme

        return RecrutementKanbanReadModel(
            offer_id=recrutement.offre_id,
            intitule=offre.title,
            date_publication=offre.publication_date,
            localisation=LocalisationDto(
                zone_geographique=offre.area or "",
                pays=offre.country or "",
                region=offre.region or "",
                departement=offre.department or "",
                localisation_label=offre.location_label or "",
                latitude=offre.latitude,
                longitude=offre.longitude,
            ),
            organisme_recruteur=OrganismeRecruteurDto(
                nom=organisme.nom,
                siret=organisme.siret,
            ),
            categorie_offre=offre.category or "",
            etapes=[
                EtapeKanbanReadModel(
                    etape_uuid=etape.id,
                    nom=etape.nom,
                    categorie=CategorieEtapeRecrutement(etape.categorie).name,
                    candidatures=[
                        CandidatureKanbanDto(
                            uuid=candidature.id,
                            date_soumission=candidature.created_at,
                            date_derniere_activite=candidature.updated_at,
                            candidat=CandidatDto(
                                uuid=UUID(candidature.candidat_id),
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
