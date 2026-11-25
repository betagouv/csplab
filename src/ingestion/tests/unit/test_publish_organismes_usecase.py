from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.usecases.publish_organismes import (
    BATCH_SIZE,
    PublishOrganismesCommand,
    PublishOrganismesUsecase,
)
from domain.gateways.publish_organismes_gateway import IPublishOrganismesGateway
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository


def _organisme(
    external_id: str = "ext-1",
    referentiel: str = "FINESS",
    parent_id=None,
    entity_id=None,
) -> Organisme:
    return Organisme.build(
        entity_id=entity_id or uuid4(),
        parent_id=parent_id,
        nom="Mairie de Test",
        versant=Verse.FPT,
        localisation=None,
        siret=SIRET(code="26060047300342"),
        external_id=external_id,
        referentiel=referentiel,
    )


@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=IPublishOrganismesGateway)
    gateway.publish = AsyncMock()
    return gateway


@pytest.fixture
def mock_raw_organisme_repository():
    repository = MagicMock(spec=IRawOrganismeRepository)
    repository.mark_as_upserted_batch = AsyncMock()
    return repository


@pytest.fixture
def usecase(mock_gateway, mock_raw_organisme_repository):
    return PublishOrganismesUsecase(
        publish_organismes_gateway=mock_gateway,
        raw_organisme_repository=mock_raw_organisme_repository,
    )


@pytest.mark.asyncio
async def test_execute_publishes_single_batch_below_batch_size(usecase, mock_gateway):
    organismes = [_organisme() for _ in range(50)]

    await usecase.execute(PublishOrganismesCommand(organismes=organismes))

    mock_gateway.publish.assert_awaited_once_with(
        organismes, {o.entity_id: o.external_id for o in organismes}
    )


@pytest.mark.asyncio
async def test_execute_splits_into_batches_of_100(usecase, mock_gateway):
    organismes = [_organisme() for _ in range(250)]

    await usecase.execute(PublishOrganismesCommand(organismes=organismes))

    assert mock_gateway.publish.await_count == 3
    calls = mock_gateway.publish.await_args_list
    assert len(calls[0].args[0]) == 100
    assert len(calls[1].args[0]) == 100
    assert len(calls[2].args[0]) == 50


@pytest.mark.asyncio
async def test_execute_does_nothing_when_no_organismes(usecase, mock_gateway):
    await usecase.execute(PublishOrganismesCommand(organismes=[]))

    mock_gateway.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_execute_propagates_gateway_error(usecase, mock_gateway):
    mock_gateway.publish.side_effect = RuntimeError("API down")

    with pytest.raises(RuntimeError, match="API down"):
        await usecase.execute(PublishOrganismesCommand(organismes=[_organisme()]))


@pytest.mark.asyncio
async def test_execute_marks_raw_organismes_as_upserted(
    usecase, mock_raw_organisme_repository
):
    organisme = _organisme(external_id="ext-1", referentiel="FINESS")

    await usecase.execute(PublishOrganismesCommand(organismes=[organisme]))

    mock_raw_organisme_repository.mark_as_upserted_batch.assert_awaited_once()
    args = mock_raw_organisme_repository.mark_as_upserted_batch.await_args.args
    assert args[0] == [("FINESS", "ext-1")]


@pytest.mark.asyncio
async def test_execute_does_not_mark_upserted_when_publish_fails(
    usecase, mock_gateway, mock_raw_organisme_repository
):
    mock_gateway.publish.side_effect = RuntimeError("API down")

    with pytest.raises(RuntimeError):
        await usecase.execute(PublishOrganismesCommand(organismes=[_organisme()]))

    mock_raw_organisme_repository.mark_as_upserted_batch.assert_not_awaited()


@pytest.mark.asyncio
async def test_execute_publishes_parents_before_their_children(usecase, mock_gateway):
    root = _organisme("root")
    child = _organisme("child", parent_id=root.entity_id)
    grandchild = _organisme("grandchild", parent_id=child.entity_id)

    await usecase.execute(
        PublishOrganismesCommand(organismes=[grandchild, child, root])
    )

    published = mock_gateway.publish.await_args.args[0]
    assert [o.external_id for o in published] == ["root", "child", "grandchild"]


@pytest.mark.asyncio
async def test_execute_passes_parents_of_previous_batches_to_the_gateway(
    usecase, mock_gateway
):
    parent = _organisme("parent")
    roots = [_organisme(f"root-{i}") for i in range(BATCH_SIZE - 1)]
    child = _organisme("child", parent_id=parent.entity_id)

    await usecase.execute(PublishOrganismesCommand(organismes=[child, parent, *roots]))

    first_batch, second_batch = mock_gateway.publish.await_args_list
    assert parent in first_batch.args[0]
    assert second_batch.args[0] == [child]
    assert second_batch.args[1][parent.entity_id] == "parent"


@pytest.mark.asyncio
async def test_execute_sorts_organismes_whose_parent_is_not_published_as_roots(
    usecase, mock_gateway
):
    orphan = _organisme("orphan", parent_id=uuid4())
    root = _organisme("root")

    await usecase.execute(PublishOrganismesCommand(organismes=[orphan, root]))

    published = mock_gateway.publish.await_args.args[0]
    assert [o.external_id for o in published] == ["orphan", "root"]


@pytest.mark.asyncio
async def test_execute_publishes_organismes_in_a_cycle(usecase, mock_gateway):
    first_id, second_id = uuid4(), uuid4()
    first = _organisme("first", parent_id=second_id, entity_id=first_id)
    second = _organisme("second", parent_id=first_id, entity_id=second_id)

    await usecase.execute(PublishOrganismesCommand(organismes=[first, second]))

    published = mock_gateway.publish.await_args.args[0]
    assert [o.external_id for o in published] == ["first", "second"]
