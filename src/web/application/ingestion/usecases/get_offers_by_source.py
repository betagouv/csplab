from ddd.page_interface import IPage
from ddd.usecase_interface import IUseCase
from referentiel.entities.offer import Offer
from referentiel.repositories.offers_repository_interface import IOffersRepository

from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from domain.ingestion.repositories.user_source_repository_interface import (
    IUserSourceRepository,
)


class GetOffersBySourceUseCase(IUseCase[GetOffersBySourceInput, IPage[Offer]]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        user_source_repository: IUserSourceRepository,
        utilisateur_repository: IUtilisateurRepository,
    ) -> None:
        self.offers_repository = offers_repository
        self.user_source_repository = user_source_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: GetOffersBySourceInput) -> IPage[Offer]:
        if input_data.utilisateur_entity_id is not None:
            utilisateur = self.utilisateur_repository.get_by_entity_id(
                input_data.utilisateur_entity_id
            )
            allowed = self.user_source_repository.get_allowed_source_ids(
                utilisateur, {input_data.source_id}
            )
            if not allowed:
                raise SourceAuthorizationError({input_data.source_id})

        return self.offers_repository.get_by_source_id(input_data.source_id)
