from ddd.domain_errors import DomainError


class OrganismeNexistePas(DomainError):
    def __init__(self, identifier: str):
        super().__init__(f"Organisme introuvable : {identifier}")
        self.identifier = identifier


class OrganismeSiretConflict(DomainError):
    def __init__(self, organisme, holder):
        super().__init__(
            f"SIRET {holder.siret} of organisme {organisme.referentiel} "
            f"{organisme.external_id} is already held by organisme {holder.id} "
            f"({holder.referentiel} {holder.external_id})"
        )
