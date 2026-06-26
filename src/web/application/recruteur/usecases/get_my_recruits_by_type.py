from dataclasses import dataclass
from uuid import UUID

from ddd.page_interface import IPage
from ddd.usecase_interface import IUseCase
from referentiel.entities.offer import Offer
from referentiel.repositories.offers_repository_interface import IOffersRepository

from application.recruteur.dtos.my_recruits_dtos import PaginatedResult
from application.recruteur.errors import ErreurPaginationQuery
from application.recruteur.mappers.my_recruits_mapper import RecrutementMapper
from domain.identite.entities.agent import Agent
from domain.identite.entities.candidat import Candidat
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus


@dataclass
class GetMyRecruitsByTypeQuery:
    organisme_id: UUID
    recrutement_status: RecrutementStatus = RecrutementStatus.ACTIF
    page: int = 1
    size: int = 10

    def __post_init__(self):
        if self.page < 1:
            raise ErreurPaginationQuery(f"page must be >= 1, got {self.page}")
        if self.size < 1:
            raise ErreurPaginationQuery(f"size must be >= 1, got {self.size}")


class GetMyRecruitsByTypeUsecase(IUseCase[GetMyRecruitsByTypeQuery, PaginatedResult]):
    def __init__(
        self,
        recrutements_repository: IRecrutementRepository,
        offers_repository: IOffersRepository,
        agents_repository: IAgentRepository,
        candidat_repository: ICandidatRepository,
    ) -> None:
        self.recrutements_repository = recrutements_repository
        self.offers_repository = offers_repository
        self.agents_repository = agents_repository
        self.candidat_repository = candidat_repository

    def execute(self, query: GetMyRecruitsByTypeQuery) -> PaginatedResult:
        page: IPage[Recrutement] = self.recrutements_repository.filter_by_status(
            query.organisme_id, query.recrutement_status
        )
        total: int = page.count()
        recrutements: list[Recrutement] = list(
            page.slice((query.page - 1) * query.size, query.size)
        )

        offer_ids: list[UUID] = [r.offre_id for r in recrutements]
        offers: dict[UUID, Offer] = {
            o.id: o for o in self.offers_repository.get_by_ids(offer_ids)
        }

        responsable_ids: list[UUID] = [
            uid for r in recrutements for uid in r.responsables_ids
        ]
        agents: dict[UUID, Agent] = {
            a.entity_id: a for a in self.agents_repository.get_by_ids(responsable_ids)
        }

        candidats: dict[UUID, Candidat] = {}
        if query.recrutement_status == RecrutementStatus.ARCHIVE:
            candidat_ids: list[UUID] = [
                r.candidat_recrute_id
                for r in recrutements
                if r.candidat_recrute_id is not None
            ]
            if candidat_ids:
                candidats = {
                    c.entity_id: c
                    for c in self.candidat_repository.get_by_ids(candidat_ids)
                }

        mapper = RecrutementMapper(
            offers=offers,
            agents=agents,
            candidats=candidats,
            status=query.recrutement_status,
        )

        return PaginatedResult(
            total=total,
            items=[mapper.from_domain(r) for r in recrutements],
        )
