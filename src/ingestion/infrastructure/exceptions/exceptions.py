class InfrastructureError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ExternalApiError(InfrastructureError):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        api_name: str | None = None,
        details: dict | None = None,
    ):
        self.status_code = status_code
        self.api_name = api_name
        super().__init__(message, details)


class DilaSiretNotFound(InfrastructureError):
    """A potential employer from the DILA directory has no reliable SIRET: it
    is missing from the mapping and the Recherche Entreprises lookup found
    nothing usable. It must be reviewed and added to data/dila_sirets.csv,
    with a SIRET or as an exclusion."""

    def __init__(self, external_id: str, nom: str, type_organisme: str, reason: str):
        self.external_id = external_id
        self.nom = nom
        self.type_organisme = type_organisme
        self.reason = reason
        super().__init__(
            f"DILA SIRET not found for {nom} ({external_id}): {reason}",
            details={
                "external_id": external_id,
                "nom": nom,
                "type_organisme": type_organisme,
                "reason": reason,
            },
        )
