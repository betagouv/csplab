from uuid import UUID

from referentiel.repositories.offers_repository_interface import IOffersRepository

from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)


class CandidatureActorsValidator:
    def __init__(
        self,
        candidat_repo: ICandidatRepository,
        offers_repo: IOffersRepository,
    ) -> None:
        self.candidat_repo = candidat_repo
        self.offers_repo = offers_repo

    def validate(self, candidat_id: UUID, offre_id: UUID) -> None:
        # Raises CandidatInexistant if the candidat does not exist
        self.candidat_repo.get_by_id(candidat_id)
        # Raises OfferDoesNotExist if the offer does not exist
        self.offers_repo.get_by_id(offre_id)
