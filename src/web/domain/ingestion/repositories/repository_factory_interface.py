from typing import Protocol, TypeVar, Union

from referentiel.repositories.concours_repository_interface import IConcoursRepository
from referentiel.repositories.corps_repository_interface import ICorpsRepository
from referentiel.repositories.metier_repository_interface import IMetierRepository

from domain.ingestion.entities.document import DocumentType
from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
)

TRepository = TypeVar("TRepository")


class IRepositoryFactory(Protocol):
    def get_repository(
        self, document_type: DocumentType
    ) -> Union[
        ICorpsRepository,
        IConcoursRepository,
        IIngestionOffersRepository,
        IMetierRepository,
    ]: ...
