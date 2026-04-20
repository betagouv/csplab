from typing import Dict, List
from uuid import NAMESPACE_DNS, UUID, uuid5

from domain.entities.document import Document, DocumentType
from domain.entities.metier import Metier
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.services.document_cleaner_interface import CleaningResult, IDocumentCleaner
from domain.services.logger_interface import ILogger
from infrastructure.django_apps.shared.models.metier import MetierModel
from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    IngresMetiersDocument,
)


class MetierCleaner(IDocumentCleaner[Metier]):
    def __init__(self, logger: ILogger, metier_repository: IMetierRepository):
        self.logger = logger
        self.metier_repository = metier_repository
        self._domaine_fonctionnel_cache: Dict[str, UUID] = {}

    def _get_domaine_fonctionnel_uuid(self, code_domaine: str) -> UUID:
        if code_domaine not in self._domaine_fonctionnel_cache:
            # generate determinist UUID based on code_fonctionnel and a fixed namespace
            namespace = uuid5(NAMESPACE_DNS, "csplab.domaines-fonctionnels")
            domain_uuid = uuid5(namespace, code_domaine)
            self._domaine_fonctionnel_cache[code_domaine] = domain_uuid

        return self._domaine_fonctionnel_cache[code_domaine]

    def clean(self, raw_documents: List[Document]) -> CleaningResult[Metier]:
        for document in raw_documents:
            if document.type != DocumentType.METIERS:
                raise InvalidDocumentTypeError(document.type.value)

        all_metiers_data = []
        cleaning_errors = []

        for document in raw_documents:
            try:
                parsed_data = self._parse_metier_data(document.raw_data)
                all_metiers_data.extend(parsed_data)  # Aplatir les listes
            except Exception as e:
                error_msg = f"Error parsing document {document.id}: {str(e)}"
                self.logger.error(error_msg)
                cleaning_errors.append(
                    {"error": error_msg, "document_id": str(document.id)}
                )

        metier_entities, entity_errors = self._create_metier_entities(all_metiers_data)

        # Convertir les erreurs en format dict
        for error in entity_errors:
            cleaning_errors.append({"error": error, "type": "entity_creation"})

        return CleaningResult(entities=metier_entities, cleaning_errors=cleaning_errors)

    def _parse_metier_data(self, raw_data: dict) -> List[IngresMetiersDocument]:
        document = IngresMetiersDocument(**raw_data)
        return [document]

    def _create_metier_entities(
        self, metiers_data: List[IngresMetiersDocument]
    ) -> tuple[List[Metier], List[str]]:
        entities = []
        errors = []

        for document in metiers_data:
            try:
                model_data = MetierModel._dto_to_model_data(document)
                model = MetierModel(**model_data)
                entity = model.to_entity()
                entities.append(entity)
            except Exception as e:
                error_msg = (
                    f"Error creating Metier entity for {document.identifiant}: {e}"
                )
                self.logger.error(error_msg)
                errors.append(error_msg)

        return entities, errors
