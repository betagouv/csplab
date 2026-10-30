from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from application.usecases.import_organismes import ImportOrganismesResult
from bin.organismes_pipeline import _run
from domain.value_objects.organisme_referentiel import OrganismeReferentiel


def _make_container():
    container = MagicMock()
    container.clean_raw_organismes_usecase.return_value.execute = AsyncMock(
        return_value=[]
    )
    container.publish_organismes_usecase.return_value.execute = AsyncMock()
    return container


def _make_import_usecase(referentiel: OrganismeReferentiel | None):
    usecase = MagicMock()
    usecase.execute = AsyncMock(
        return_value=ImportOrganismesResult(
            referentiel=referentiel,
            millesime="millesime",
            total_imported=0,
            total_deleted=0,
        )
    )
    return usecase


@pytest.mark.asyncio
@patch("bin.organismes_pipeline.import_organismes_usecase_for")
@patch("bin.organismes_pipeline.create_container")
async def test_run_with_referentiel_only_imports_that_referentiel(
    mock_create_container, mock_import_organismes_usecase_for
):
    container = _make_container()
    mock_create_container.return_value = container
    use_case = _make_import_usecase(OrganismeReferentiel.DILA)
    mock_import_organismes_usecase_for.return_value = use_case

    await _run(OrganismeReferentiel.DILA)

    mock_import_organismes_usecase_for.assert_called_once_with(
        container, OrganismeReferentiel.DILA
    )
    use_case.execute.assert_awaited_once()


@pytest.mark.asyncio
@patch("bin.organismes_pipeline.import_organismes_usecase_for")
@patch("bin.organismes_pipeline.create_container")
async def test_run_without_referentiel_imports_all_referentiels(
    mock_create_container, mock_import_organismes_usecase_for
):
    container = _make_container()
    mock_create_container.return_value = container
    mock_import_organismes_usecase_for.return_value = _make_import_usecase(None)

    await _run(None)

    assert mock_import_organismes_usecase_for.call_args_list == [
        call(container, referentiel) for referentiel in OrganismeReferentiel
    ]
