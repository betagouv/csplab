from unittest.mock import MagicMock

from django.urls import reverse
from referentiel.exceptions.offer_errors import OfferDoesNotExist
from rest_framework import status

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from presentation.ingestion.serializers import (
    FakeTsCodedObjectSerializer,
    FakeTsOfferDetailSerializer,
    FakeTsOrganisationSerializer,
)
from tests.utils.openapi_test_utils import assert_matches_openapi_schema

URL = reverse("ingestion_fake_ts:offer_detail")


def _make_usecase(mock_container, offer=None, exception=None):
    mock_usecase = MagicMock()
    if exception:
        mock_usecase.execute.side_effect = exception
    else:
        mock_usecase.execute.return_value = offer
    mock_container.get_offer_by_reference_usecase.return_value = mock_usecase
    return mock_usecase


def test_unauthenticated_access(api_client):
    response = api_client.get(URL, {"reference": "REF-1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_valid_api_key_no_longer_grants_access(api_key_client):
    response = api_key_client.get(URL, {"reference": "REF-1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_allowed(authenticated_client):
    response = authenticated_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_missing_reference_returns_400(
    mock_offer_detail_container, authenticated_client
):
    _make_usecase(mock_offer_detail_container)

    response = authenticated_client.get(URL)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unknown_reference_returns_404(
    mock_offer_detail_container, authenticated_client
):
    _make_usecase(mock_offer_detail_container, exception=OfferDoesNotExist("REF-1"))

    response = authenticated_client.get(URL, {"reference": "REF-1"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_reference_is_forwarded_to_usecase(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity(reference="REF-1")
    mock_usecase = _make_usecase(mock_offer_detail_container, offer=offer)

    authenticated_client.get(URL, {"reference": "REF-1"})

    mock_usecase.execute.assert_called_once_with(
        GetOfferByReferenceInput(reference="REF-1")
    )


def test_returns_offer_detail(mock_offer_detail_container, authenticated_client):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["reference"] == offer.reference
    assert data["title"] == offer.title
    assert data["organisation"]["name"] == offer.organization
    assert data["isAnonymousOrganisation"] is False


def test_response_matches_openapi_schema(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})

    assert_matches_openapi_schema(
        response.json(), "/api/fake-ts/offers/getoffer", method="get"
    )


def test_response_has_no_undeclared_fields(
    mock_offer_detail_container, authenticated_client
):
    offer = OfferFactory.create_entity()
    _make_usecase(mock_offer_detail_container, offer=offer)

    response = authenticated_client.get(URL, {"reference": offer.reference})
    data = response.json()

    assert set(data.keys()) == set(FakeTsOfferDetailSerializer().fields.keys())
    assert set(data["organisation"].keys()) == set(
        FakeTsOrganisationSerializer().fields.keys()
    )
    assert set(data["offerFamilyCategory"].keys()) == set(
        FakeTsCodedObjectSerializer().fields.keys()
    )


def test_returns_error_500(mock_offer_detail_container, authenticated_client):
    _make_usecase(mock_offer_detail_container, exception=Exception("db error"))

    response = authenticated_client.get(URL, {"reference": "REF-1"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
