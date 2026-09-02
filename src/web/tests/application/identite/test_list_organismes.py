from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from application.identite.services.organisme_query_service_interface import (
    IOrganismeQueryService,
    OrganismeReadModel,
)
from application.identite.usecases.list_organismes import (
    ListOrganismesCommand,
    ListOrganismesUsecase,
)
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


@pytest.fixture(name="permission_service")
def permission_service_fixture():
    service = Mock(spec=OrganismePermissionService)
    service.est_autorise.return_value = AgentRecrutementRole.RESPONSABLE
    return service


@pytest.fixture(name="organisme_read_models")
def organisme_read_models_fixture():
    organismes = OrganismeFactory.create_entity_batch(
        gestion_ats=True,
        date_creation=datetime(2025, 10, 1),
        date_derniere_activite=datetime.now(timezone.utc),
    )
    return [
        OrganismeReadModel(
            entity_id=organisme.entity_id,
            name=organisme.nom,
            siret=organisme.siret,
            verse=organisme.versant,
            managed_ats=organisme.gestion_ats,
            creation_date=organisme.date_creation,
            last_activity_date=organisme.date_derniere_activite,
            number_agents=5,
            number_published_offers=100,
        )
        for organisme in organismes
    ]


@pytest.fixture(name="organisme_query_service")
def organisme_rquery_service_fixture(organisme_read_models):
    service = Mock(spec=IOrganismeQueryService)
    service.get_all_with_counts.return_value = organisme_read_models
    return service


@pytest.fixture(name="usecase")
def usecase_fixture(
    permission_service,
    organisme_query_service,
):
    return ListOrganismesUsecase(
        organisme_query_service=organisme_query_service,
        permission_service=permission_service,
    )


def test_list_organismes_success(permission_service, organisme_read_models, usecase):
    utilisateur = UtilisateurFactory.create_entity(is_staff=True)
    command = ListOrganismesCommand(
        utilisateur=utilisateur,
    )

    result = usecase.execute(command)
    permission_service.est_autorise.assert_called_once_with(
        action=OrganismeAction.LISTER_ORGANISMES,
        utilisateur=utilisateur,
    )

    assert result == organisme_read_models


def test_list_organisme_refuse_non_staff(permission_service, usecase):
    command = ListOrganismesCommand(
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )
    permission_service.est_autorise.side_effect = OperationOrganismeRefusee()

    with pytest.raises(OperationOrganismeRefusee):
        usecase.execute(command=command)
