from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.exceptions.cv_errors import CVNotFoundError
from domain.candidate.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


class AsyncPostgresCVMetadataRepository(IAsyncCVMetadataRepository):
    async def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        model = CVMetadataModel.from_entity(cv_metadata)
        await model.asave()
        return model.to_entity()

    async def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        try:
            model = await CVMetadataModel.objects.aget(id=cv_id)
            return model.to_entity()
        except ObjectDoesNotExist as e:
            raise CVNotFoundError(str(cv_id)) from e

    def count(self) -> int:
        return CVMetadataModel.objects.count()
