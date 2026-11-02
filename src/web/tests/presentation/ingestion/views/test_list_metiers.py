from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)
from infrastructure.factories.referentiel.metier_factory import MetierFactory

fake = Faker()
URL = reverse("ingestion:metiers_list")

NOMBRE_REQUETES_ATTENDU = (
    1  # authentification JWT
    + 2  # pagination : count + page
    + 1  # ApiRequestLoggerMiddleware redecode JWT token for logging
    # TODO: refactor ADR-009 : simplify UPDATE/INSERT
    + 2  # logging : UPDATE (manually assigned pk) then INSERT
)


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(jwt_client):
    response = jwt_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def _make_paginated_mock(mock_metiers_container, metiers):
    mock_usecase = MagicMock()
    mock_usecase.execute.return_value = metiers
    mock_metiers_container.list_metiers_usecase.return_value = mock_usecase

    return mock_usecase


def test_empty_result(mock_metiers_container, jwt_client):
    _make_paginated_mock(mock_metiers_container, metiers=[])

    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_call_without_arg(mock_metiers_container, jwt_client):
    metiers = [MetierFactory.create_entity() for _ in range(2)]

    _make_paginated_mock(mock_metiers_container, metiers=metiers)

    response = jwt_client.get(URL, {})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["count"] == len(metiers)
    assert data["next"] is None
    assert data["previous"] is None

    for result, metier in zip(data["results"], metiers, strict=True):
        assert result["libelle"] == metier.libelle
        assert result["description"] == metier.description
        assert result["domaine_fonctionnel_code"] == metier.domaine_fonctionnel_code
        assert result["code_emploi_csp"] == metier.offer_family_code
        assert result["versants"] == [versant.value for versant in metier.versants]
        assert result["activites"] == metier.activites
        assert result["conditions_particulieres"] == metier.conditions_particulieres


@pytest.mark.parametrize("domain", [None, "TRE"])
def test_call_with_args(mock_metiers_container, jwt_client, domain):
    _make_paginated_mock(mock_metiers_container, metiers=[])

    params = {"domaine": domain} if domain else {}
    jwt_client.get(URL, params)

    mock_metiers_container.list_metiers_usecase.return_value.execute.assert_called_once_with(
        GetFilteredMetiersInput(domain=domain)
    )


def test_returns_error_500(mock_metiers_container, jwt_client):
    mock_usecase = MagicMock()
    mock_usecase.execute.side_effect = Exception("db error")
    mock_metiers_container.list_metiers_usecase.return_value = mock_usecase

    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_pagination_page_arg(mock_metiers_container, jwt_client):
    metiers = [MetierFactory.create_entity() for _ in range(5)]
    _make_paginated_mock(mock_metiers_container, metiers=metiers)

    response = jwt_client.get(URL, {"page": 2, "taille": 2, "dummy": "arg"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == len(metiers)
    assert len(data["results"]) == 2  # noqa

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "dummy": ["arg"],
        "taille": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "taille": ["2"],
    }


def test_pagination_out_of_bounds_returns_404(mock_metiers_container, jwt_client):
    _make_paginated_mock(
        mock_metiers_container,
        metiers=[MetierFactory.create_entity() for _ in range(3)],
    )

    response = jwt_client.get(URL, {"page": 3, "taille": 2})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.parametrize("page", ["0", "-1", "abc"])
def test_pagination_invalid_page_returns_404(mock_metiers_container, jwt_client, page):
    _make_paginated_mock(mock_metiers_container, metiers=[])

    response = jwt_client.get(URL, {"page": page})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("taille", ["0", "-5", "abc"])
def test_pagination_invalid_taille_falls_back_to_default(
    mock_metiers_container, jwt_client, taille
):
    _make_paginated_mock(
        mock_metiers_container,
        metiers=[MetierFactory.create_entity() for _ in range(3)],
    )

    response = jwt_client.get(URL, {"taille": taille})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa


def test_pagination_taille_is_capped(mock_metiers_container, jwt_client):
    _make_paginated_mock(
        mock_metiers_container,
        metiers=[MetierFactory.create_entity() for _ in range(3)],
    )

    response = jwt_client.get(URL, {"taille": 1_000_000, "page": 1})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa


def test_invalid_payload(mock_metiers_container, jwt_client):
    _make_paginated_mock(mock_metiers_container, metiers=[])

    response = jwt_client.get(URL, {"domaine": "ABCD"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.json().keys()


class TestMetiersListViewDbVerified:
    def test_response_matches_db_record_field_by_field(self, jwt_client):
        metier = MetierDjangoFactory(
            domaine_fonctionnel_code="TRA",
            versants=["FPE"],
            activites=["Rédiger des actes"],
            conditions_particulieres=["Habilitation"],
        )

        response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"] == [
            {
                "libelle": metier.libelle_long,
                "description": metier.definition_synthetique,
                "domaine_fonctionnel_code": metier.domaine_fonctionnel_code,
                "versants": metier.versants,
                "activites": metier.activites,
                "conditions_particulieres": metier.conditions_particulieres,
                "code_emploi_csp": metier.offer_family_code,
            }
        ]

    def test_does_not_trigger_n_plus_one_queries(
        self, jwt_client, django_assert_num_queries
    ):
        MetierDjangoFactory.create_batch(5)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
