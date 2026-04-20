"""Repository factory interface for entity persistence."""

from typing import Protocol, TypeVar, Union

from domain.entities.document import DocumentType
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.repositories.offers_repository_interface import IOffersRepository

TRepository = TypeVar("TRepository")


class IRepositoryFactory(Protocol):
    def get_repository(
        self, document_type: DocumentType
    ) -> Union[
        ICorpsRepository, IConcoursRepository, IOffersRepository, IMetierRepository
    ]: ...
