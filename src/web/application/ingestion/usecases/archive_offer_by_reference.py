from ddd.usecase_interface import IUseCase
from referentiel.repositories.offers_repository_interface import IOffersRepository

from application.ingestion.interfaces.archive_offer_by_reference_input import (
    ArchiveOfferByReferenceInput,
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
from domain.ingestion.repositories.vector_repository_interface import IVectorRepository


class ArchiveOfferByReferenceUseCase(IUseCase[ArchiveOfferByReferenceInput, None]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        vector_repository: IVectorRepository,
        user_source_repository: IUserSourceRepository,
        utilisateur_repository: IUtilisateurRepository,
    ) -> None:
        self.offers_repository = offers_repository
        self.vector_repository = vector_repository
        self.user_source_repository = user_source_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: ArchiveOfferByReferenceInput) -> None:
        if input_data.utilisateur_entity_id is not None:
            utilisateur = self.utilisateur_repository.get_by_entity_id(
                input_data.utilisateur_entity_id
            )
            allowed = self.user_source_repository.get_allowed_source_ids(
                utilisateur, {input_data.source_id}
            )
            if not allowed:
                raise SourceAuthorizationError({input_data.source_id})

        offer = self.offers_repository.get_by_reference_and_source_id(
            input_data.reference, input_data.source_id
        )
        self.vector_repository.delete_vectorized_documents([offer.id])
        self.offers_repository.mark_as_archived([offer])
