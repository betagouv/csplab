from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

from domain.identite.errors.identite_errors import UtilisateurDoesNotExist
from tests.factories.identite.utilisateur_factory import UtilisateurFactory

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
    entity = UtilisateurFactory.create_entity()

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
    }


@pytest.mark.parametrize(
    "exception,status_code",
    [
        (UtilisateurDoesNotExist("unknown"), status.HTTP_404_NOT_FOUND),
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
