from uuid import UUID

from referentiel.entities.source import Source

from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient
from infrastructure.talentsoft_client_repository import TalentsoftClientRepository


def resolve_source_and_client(
    source_id: UUID,
    sources_repository: ISourcesRepository,
    talentsoft_client_repository: TalentsoftClientRepository,
) -> tuple[Source, TalentsoftFrontClient]:
    source = sources_repository.get_by_source_id(source_id)
    if source is None:
        raise ValueError(f"Source {source_id} not found")

    client = talentsoft_client_repository.get(source.client_id_front)
    if client is None:
        raise ValueError(f"No Talentsoft client found for source {source_id}")

    return source, client
