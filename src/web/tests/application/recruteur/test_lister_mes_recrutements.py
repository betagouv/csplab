from datetime import datetime, timezone
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
    ListerMesRecrutementsUsecase,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture(name="service")
def service_fixture() -> IRecrutementQueryService:
    return cast(
        IRecrutementQueryService, create_interface_aware_mock(IRecrutementQueryService)
    )


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


class TestListerMesRecrutements:
    def test_lister_mes_recrutements_actifs(self, service, organisme_repository):
        organisme_id = uuid4()
        recrutements_actifs = [
            RecrutementFactory.create_actif_read_model(
                derniere_activite=datetime.now(timezone.utc)
            )
        ]
        service.get_actifs_by_organisme = MagicMock(return_value=recrutements_actifs)
        usecase = ListerMesRecrutementsUsecase(
            recrutement_query_service=service,
            organisme_repository=organisme_repository,
            logger=MagicMock(),
        )

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme_id, statut=StatutRecrutement.ACTIF
            )
        )

        assert result == recrutements_actifs
        service.get_actifs_by_organisme.assert_called_once_with(organisme_id)
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_lister_mes_recrutements_archives(self, service, organisme_repository):
        organisme_id = uuid4()
        recrutements_archives = [RecrutementFactory.create_archive_read_model()]
        service.get_archives_by_organisme = MagicMock(
            return_value=recrutements_archives
        )
        usecase = ListerMesRecrutementsUsecase(
            recrutement_query_service=service,
            organisme_repository=organisme_repository,
            logger=MagicMock(),
        )

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme_id, statut=StatutRecrutement.ARCHIVE
            )
        )

        assert result == recrutements_archives
        service.get_archives_by_organisme.assert_called_once_with(organisme_id)
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_raise_organisme_not_found(self, service, organisme_repository):
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )
        usecase = ListerMesRecrutementsUsecase(
            recrutement_query_service=service,
            organisme_repository=organisme_repository,
            logger=MagicMock(),
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                ListerMesRecrutementsQuery(
                    organisme_id=organisme_id, statut=StatutRecrutement.ACTIF
                )
            )
