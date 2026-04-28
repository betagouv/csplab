from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.repositories.cv_metadata_repository_interface import (
    ICVMetadataRepository,
)
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


class PostgresCVMetadataRepository(ICVMetadataRepository):
    def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        model = CVMetadataModel.from_entity(cv_metadata)
        model.save()
        return model.to_entity()

    def get_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        try:
            model = CVMetadataModel.objects.get(id=cv_id)
            return model.to_entity()
        except ObjectDoesNotExist as e:
            raise CVNotFoundError(str(cv_id)) from e
