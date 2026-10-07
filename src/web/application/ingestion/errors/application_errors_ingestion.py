from uuid import UUID

from application.exceptions import ApplicationError


class TalentsoftOrganismeInexistant(ApplicationError):
    def __init__(self, entity_code: str):
        super().__init__(f"Organisation inconnue : {entity_code}.")


class SourceNonAutorisee(ApplicationError):
    def __init__(self, source_id: UUID):
        super().__init__(f"Accès refusé à la source {source_id}.")


class OffreIntrouvable(ApplicationError):
    def __init__(self, offer_id: UUID):
        super().__init__(f"Offre introuvable : {offer_id}.")


class AccesSourcesRefuse(ApplicationError):
    def __init__(self, username):
        super().__init__(f"Accès aux sources refusé à l'utilisateur {username}.")
