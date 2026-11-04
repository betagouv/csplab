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


class TalentsoftOfferWithSeveralLocations(InfrastructureError):
    """Only the first location is kept (see #1793)."""

    def __init__(self, reference: str, source_id: str | None, fields: list[str]):
        self.reference = reference
        self.source_id = source_id
        self.fields = fields
        super().__init__(
            f"Offer {reference} from source {source_id} has several locations "
            f"({', '.join(fields)}): only the first one is kept",
            details={"reference": reference, "source_id": source_id, "fields": fields},
        )


class TalentsoftOfferWithMisfiledStateDiploma(InfrastructureError):
    """`customFields.offerCustomBlock1.customCodeTable3` holds another repository
    than « Diplômes d'Etat » (the working time quota so far): the value is
    dropped (see #2284)."""

    def __init__(
        self,
        reference: str,
        source_id: str | None,
        organisme_entity_code: str | None,
        type: str | None,
        client_code: str,
    ):
        self.reference = reference
        self.source_id = source_id
        self.organisme_entity_code = organisme_entity_code
        self.type = type
        self.client_code = client_code
        super().__init__(
            f"Offer {reference} from source {source_id} (organisme "
            f"{organisme_entity_code}) has {type!r} ({client_code}) in the state "
            "diploma field: the value is dropped",
            details={
                "reference": reference,
                "source_id": source_id,
                "organisme_entity_code": organisme_entity_code,
                "type": type,
                "client_code": client_code,
            },
        )
