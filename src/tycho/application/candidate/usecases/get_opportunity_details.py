from typing import Tuple
from uuid import UUID

from domain.entities.concours import Concours
from domain.entities.metier import Metier
from domain.entities.offer import Offer
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.services.logger_interface import ILogger
from domain.value_objects.opportunity_type import OpportunityType


class GetOpportunityDetails(
    IUseCase[Tuple[OpportunityType, UUID], Tuple[Offer, list[Metier]] | Concours]
):
    def __init__(
        self,
        offer_repository: IOffersRepository,
        concours_repository: IConcoursRepository,
        metier_repository: IMetierRepository,
        logger: ILogger,
    ):
        self.offer_repository = offer_repository
        self.concours_repository = concours_repository
        self.metier_repository = metier_repository
        self.logger = logger

    def execute(
        self, opportunity_type: OpportunityType, opportunity_id: UUID
    ) -> Tuple[Offer, list[Metier]] | Concours:

        if opportunity_type == OpportunityType.CONCOURS:
            return self.concours_repository.get_by_id(opportunity_id)

        offer = self.offer_repository.get_by_id(opportunity_id)
        if offer.family_code is None:
            self.logger.warning(
                f"Offer with id {offer.id} has no family code"
                f"cannot fetch related metiers"
            )
            return offer, []
        metiers = self.metier_repository.filter_by(
            {"offer_family_code": offer.family_code}
        )
        return offer, metiers
