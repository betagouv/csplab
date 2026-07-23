from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeQuery,
    GetRecrutementListeUsecase,
)
from application.recruteur.usecases.recrutement_detail_static_data import (
    STATIC_RECRUTEMENT_DETAIL,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_repository, organisme_permission_service):
    return GetRecrutementListeUsecase(
        organisme_repository=organisme_repository,
        organisme_permission_service=organisme_permission_service,
    )


class TestGetRecrutementListe:
    @pytest.mark.parametrize(
        "role",
        [
            pytest.param(AgentOrganismeRole.RESPONSABLE, id="responsable"),
            pytest.param(AgentOrganismeRole.MEMBRE, id="membre"),
        ],
    )
    def test_returns_detail_when_authorized(
        self, organisme_repository, organisme_permission_service, usecase, role
    ):
        organisme_permission_service.est_autorise.return_value = role
        organisme_id = uuid4()
        recrutement_id = UUID(STATIC_RECRUTEMENT_DETAIL["offer_id"])

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur_id=uuid4(),
            )
        )

        assert result == STATIC_RECRUTEMENT_DETAIL
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_returns_none_for_unknown_recrutement(
        self, organisme_repository, organisme_permission_service, usecase
    ):
        organisme_permission_service.est_autorise.return_value = (
            AgentOrganismeRole.RESPONSABLE
        )
        organisme_id = uuid4()

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme_id,
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
            )
        )

        assert result is None
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_raises_when_not_authorized(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )

    def test_raises_when_organisme_not_found(
        self, organisme_repository, organisme_permission_service, usecase
    ):
        organisme_permission_service.est_autorise.return_value = (
            AgentOrganismeRole.RESPONSABLE
        )
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )
