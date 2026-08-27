from uuid import UUID

from application.exceptions import ApplicationError


class OrganismeRecrutementIncoherents(ApplicationError):
    def __init__(self, organisme_id: UUID, recrutement_id: UUID):
        super().__init__(
            f"Le recrutement {recrutement_id} ne correspond pas"
            f"à l'organisme {organisme_id}"
        )


class RecrutementEtapeIncoherents(ApplicationError):
    def __init__(self, recrutement_id: UUID, etape_id: UUID):
        super().__init__(
            f"L'étape {etape_id} ne correspond pas au recrutement {recrutement_id}"
        )
