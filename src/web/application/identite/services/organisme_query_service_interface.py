from typing import List, Protocol

from application.identite.dtos.organisme_read_models import OrganismeReadModel


class IOrganismeQueryService(Protocol):
    def get_all_with_counts(self) -> List[OrganismeReadModel]: ...
