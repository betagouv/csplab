from uuid import UUID

from application.exceptions import ApplicationError


class OrganismeRecruteurSansEtapes(ApplicationError):
    def __init__(self, organisme_id: UUID):
        super().__init__(
            f"L' organisme recruteur {organisme_id} n'a pas d'étapes par defaut"
        )


class OrganismeRecrutementIncoherents(ApplicationError):
    def __init__(self, organisme_id: UUID, recrutement_id: UUID):
        super().__init__(
            f"Le recrutement {recrutement_id} ne correspond pas"
            f"à l'organisme {organisme_id}"
        )
