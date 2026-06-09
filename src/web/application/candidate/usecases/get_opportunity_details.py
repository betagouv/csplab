from typing import Tuple
from uuid import UUID

from ddd.services.logger_interface import ILogger
from referentiel.entities.concours import Concours
from referentiel.entities.metier import Metier
from referentiel.entities.offer import Offer
from referentiel.repositories.concours_repository_interface import IConcoursRepository
from referentiel.repositories.metier_repository_interface import IMetierRepository
from referentiel.repositories.offers_repository_interface import IOffersRepository

from domain.candidate.value_objects.opportunity_type import OpportunityType


class GetOpportunityDetailsUsecase:
    def __init__(
        self,
        offers_repository: IOffersRepository,
        concours_repository: IConcoursRepository,
        metiers_repository: IMetierRepository,
        logger: ILogger,
    ):
        self.offers_repository = offers_repository
        self.concours_repository = concours_repository
        self.metiers_repository = metiers_repository
        self.logger = logger

    def execute(
        self, opportunity_type: OpportunityType, opportunity_id: UUID
    ) -> Tuple[Offer, list[Metier]] | Concours:

        if opportunity_type == OpportunityType.CONCOURS:
            return self.concours_repository.get_by_id(opportunity_id)

        offer = self.offers_repository.get_by_id(opportunity_id)
        metiers = self.metiers_repository.get_for_offer(offer)
        return offer, metiers
