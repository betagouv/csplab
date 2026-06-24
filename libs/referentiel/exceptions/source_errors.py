from ddd.domain_errors import DomainError


class MissingTalentsoftFieldsError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "client_id_front, client_id_back, base_url_front et base_url_back "
            "sont obligatoires pour une source de type TALENTSOFT"
        )
