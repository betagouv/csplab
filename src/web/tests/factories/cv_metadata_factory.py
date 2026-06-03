from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from ddd.types import JsonDataType
from polyfactory.factories import DataclassFactory

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.value_objects.cv_processing_status import CVStatus


class CVMetadataFactory(DataclassFactory[CVMetadata]):
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        filename: str = "cv_test.pdf",
        status: CVStatus = CVStatus.PENDING,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        extracted_text: Optional[JsonDataType] = None,
        search_query: Optional[str] = None,
    ) -> CVMetadata:
        if entity_id is None:
            entity_id = uuid4()
        if created_at is None:
            created_at = datetime.now(tz=UTC)
        if updated_at is None:
            updated_at = datetime.now(tz=UTC)

        return CVMetadata(
            entity_id=entity_id,
            filename=filename,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            extracted_text=extracted_text,
            search_query=search_query,
        )
