from typing import Iterator, Protocol

from domain.value_objects.organisme import OrganismeData, OrganismeImportResource


class IOrganismeGateway(Protocol):
    def find_resource(self) -> OrganismeImportResource: ...

    def stream_organismes(
        self, resource: OrganismeImportResource
    ) -> Iterator[OrganismeData]: ...
