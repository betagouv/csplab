from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.identite.errors.identite_errors import UtilisateurNexistePas
from domain.identite.value_objects.organisme_role import OrganismeRole
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory

URL = reverse("identite:user-details")


@pytest.fixture
def mock_container():
    with patch("presentation.identite.views.create_identite_container") as mock:
        yield mock


def test_anonymous_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logged_access(api_client, test_user):
    api_client.force_login(test_user)
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_authentified_access(authenticated_client):
    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_returned_payload(mock_container, authenticated_client, test_user):
    organisme_role = OrganismeRole(
        organisme_uuid=uuid4(), nom="Organisme de test", role="responsable"
    )
    entity = UtilisateurFactory.create_entity(organismes=[organisme_role])

    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = entity
    mock_container.return_value.get_utilisateur_details_usecase.return_value = (
        mock_usecase
    )
    mock_container.return_value.logger_service.return_value = MagicMock()

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": entity.email,
        "prenom": entity.prenom,
        "nom": entity.nom,
        "is_staff": entity.is_staff,
        "organisme_roles": [
            {
                "organisme_uuid": str(organisme_role.organisme_uuid),
                "nom": organisme_role.nom,
                "role": organisme_role.role,
            }
        ],
    }


def test_returned_payload_from_db(authenticated_client, test_user):
    AgentFactory.create_model(username=test_user.username)
    organisme = OrganismeFactory.create_model(
        agent_id=test_user.username, role=AgentOrganismeRole.MEMBRE
    )

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": test_user.email,
        "prenom": test_user.first_name,
        "nom": test_user.last_name,
        "is_staff": test_user.is_staff,
        "organisme_roles": [
            {
                "organisme_uuid": str(organisme.id),
                "nom": organisme.nom,
                "role": AgentOrganismeRole.MEMBRE.value,
            }
        ],
    }


def test_returned_payload_for_staff_user(authenticated_client, test_user):
    test_user.is_staff = True
    test_user.save()

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_staff"] is True


@pytest.mark.parametrize(
    "exception,status_code",
    [
        (UtilisateurNexistePas("unknown"), status.HTTP_404_NOT_FOUND),
        (Exception("db connection error"), status.HTTP_500_INTERNAL_SERVER_ERROR),
    ],
)
def test_returns_500_on_error(
    mock_container, authenticated_client, exception, status_code
):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = exception
    mock_container.return_value.get_utilisateur_details_usecase.return_value = (
        mock_usecase
    )
    mock_container.return_value.logger_service.return_value = MagicMock()

    response = authenticated_client.get(URL)

    assert response.status_code == status_code
