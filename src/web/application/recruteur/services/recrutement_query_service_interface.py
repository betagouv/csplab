from typing import Protocol
from uuid import UUID

from application.recruteur.dtos.recrutement_read_models import (
    RecrutementKanbanReadModel,
)


class IRecrutementQueryService(Protocol):
    def get_kanban_by_recrutement(
        self, organisme_id: UUID, recrutement_id: UUID
    ) -> RecrutementKanbanReadModel | None: ...
