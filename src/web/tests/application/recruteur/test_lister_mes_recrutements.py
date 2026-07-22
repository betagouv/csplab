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
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
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


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="usecase")
def usecase_fixture(service, organisme_repository, organisme_permission_service):
    return ListerMesRecrutementsUsecase(
        recrutement_query_service=service,
        organisme_repository=organisme_repository,
        organisme_permission_service=organisme_permission_service,
        logger=MagicMock(),
    )


class TestListerMesRecrutements:
    def test_lister_mes_recrutements_actifs(
        self, service, organisme_repository, usecase
    ):
        organisme_id = uuid4()
        recrutements_actifs = [
            RecrutementFactory.create_actif_read_model(
                derniere_activite=datetime.now(timezone.utc)
            )
        ]
        service.get_actifs_by_organisme = MagicMock(return_value=recrutements_actifs)

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme_id,
                statut=StatutRecrutement.ACTIF,
                utilisateur_id=uuid4(),
            )
        )

        assert result == recrutements_actifs
        service.get_actifs_by_organisme.assert_called_once_with(organisme_id, None)
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_lister_mes_recrutements_archives(
        self, service, organisme_repository, usecase
    ):
        organisme_id = uuid4()
        recrutements_archives = [RecrutementFactory.create_archive_read_model()]
        service.get_archives_by_organisme = MagicMock(
            return_value=recrutements_archives
        )

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme_id,
                statut=StatutRecrutement.ARCHIVE,
                utilisateur_id=uuid4(),
            )
        )

        assert result == recrutements_archives
        service.get_archives_by_organisme.assert_called_once_with(organisme_id, None)
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_raise_organisme_not_found(self, service, organisme_repository, usecase):
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                ListerMesRecrutementsQuery(
                    organisme_id=organisme_id,
                    statut=StatutRecrutement.ACTIF,
                    utilisateur_id=uuid4(),
                )
            )

    def test_raises_when_not_responsable(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                ListerMesRecrutementsQuery(
                    organisme_id=organisme_id,
                    statut=StatutRecrutement.ACTIF,
                    utilisateur_id=uuid4(),
                )
            )
