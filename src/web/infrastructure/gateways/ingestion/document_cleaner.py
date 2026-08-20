from typing import List

from ddd.entity import Entity
from ddd.services.logger_interface import ILogger
from referentiel.repositories.concours_repository_interface import IConcoursRepository
from referentiel.repositories.corps_repository_interface import ICorpsRepository
from referentiel.repositories.metier_repository_interface import IMetierRepository

from domain.ingestion.entities.document import Document, DocumentType
from domain.ingestion.exceptions.document_error import (
    MixedDocumentTypesError,
    UnsupportedDocumentTypeError,
)
from domain.ingestion.services.document_cleaner_interface import (
    CleaningResult,
    IDocumentCleaner,
)
from infrastructure.gateways.ingestion.concours_cleaner import ConcoursCleaner
from infrastructure.gateways.ingestion.corps_cleaner import CorpsCleaner
from infrastructure.gateways.ingestion.metier_cleaner import MetierCleaner


class DocumentCleaner(IDocumentCleaner[Entity]):
    def __init__(
        self,
        logger: ILogger,
        corps_repository: ICorpsRepository,
        concours_repository: IConcoursRepository,
        metiers_repository: IMetierRepository,
    ):
        self._cleaners = {
            DocumentType.CORPS: CorpsCleaner(logger, corps_repository),
            DocumentType.CONCOURS: ConcoursCleaner(logger, concours_repository),
            DocumentType.METIERS: MetierCleaner(logger, metiers_repository),
        }

    def clean(self, raw_documents: List[Document]) -> CleaningResult[Entity]:
        if not raw_documents:
            return CleaningResult(entities=[], cleaning_errors=[])

        document_types = {doc.type for doc in raw_documents}
        if len(document_types) > 1:
            raise MixedDocumentTypesError(document_types)

        document_type = next(iter(document_types))

        # Get the appropriate cleaner
        if document_type not in self._cleaners:
            raise UnsupportedDocumentTypeError(document_type.value)

        cleaner = self._cleaners[document_type]
        return cleaner.clean(raw_documents)
