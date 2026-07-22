from typing import Protocol
from uuid import UUID

from ddd.page_interface import IPage

from application.recruteur.dtos.recrutement_read_models import (
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
)


class IRecrutementQueryService(Protocol):
    def get_actifs_by_organisme(
        self, organisme_id: UUID, agent_id: UUID | None = None
    ) -> IPage[RecrutementActifsReadModel]: ...
    def get_archives_by_organisme(
        self, organisme_id: UUID, agent_id: UUID | None = None
    ) -> IPage[RecrutementArchivesReadModel]: ...
