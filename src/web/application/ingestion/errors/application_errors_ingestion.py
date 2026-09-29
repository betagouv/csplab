from application.exceptions import ApplicationError


class TalentsoftOrganismeInexistant(ApplicationError):
    def __init__(self, entity_code: str):
        super().__init__(f"Organisation inconnue : {entity_code}.")
