from uuid import UUID

from application.exceptions import ApplicationError


class RecrutementEtapeIncoherents(ApplicationError):
    def __init__(self, recrutement_id: UUID, etape_id: UUID):
        super().__init__(
            f"L'étape {etape_id} ne correspond pas au recrutement {recrutement_id}"
        )
