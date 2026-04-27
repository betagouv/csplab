from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from faker import Faker
from pydantic import HttpUrl

from config.app_config import TalentsoftBackConfig, TalentsoftConfig
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftBackClient,
    TalentsoftFrontClient,
)
from tests.ingestion.unit.external_gateways.utils import (
    cached_token,
    detail_offer_response,
    mocked_response,
    offers_response,
)

fake = Faker()


def _make_client(client_class, config_class):
    logger_service = Mock()
    logger_service.get_logger.return_value = Mock()
    config = config_class(
        base_url=HttpUrl(fake.url()),
        client_id=fake.uuid4(),
        client_secret=fake.uuid4(),
    )
    return client_class(config=config, logger_service=logger_service, timeout=30)


@pytest.fixture(name="talentsoft_client")
def talentsoft_client_fixture():
    return _make_client(TalentsoftFrontClient, TalentsoftConfig)


@pytest.fixture(name="talentsoft_back_client")
def talentsoft_back_client_fixture():
    return _make_client(TalentsoftBackClient, TalentsoftBackConfig)


CLIENT_API_NAMES = [
    ("talentsoft_client", "Talentsoft Front API"),
    ("talentsoft_back_client", "Talentsoft Back API"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_fixture,api_name", CLIENT_API_NAMES)
class TestGetAccessToken:
    async def test_cached_token_is_valid(self, client_fixture, api_name, request):
        client = request.getfixturevalue(client_fixture)
        valid_token = cached_token()
        client.cached_token = valid_token
        result = await client.get_access_token()
        assert result == valid_token.access_token

    @pytest.mark.parametrize("initial_token", [None, cached_token(expire_in=-3600)])
    async def test_new_cached_token_has_to_be_fetched(
        self, client_fixture, api_name, request, initial_token
    ):
        client = request.getfixturevalue(client_fixture)
        client.cached_token = initial_token
        expected_token = fake.uuid4()
        mock_response = mocked_response(
            return_value={
                "access_token": expected_token,
                "token_type": fake.word(),
                "expires_in": 3600,
            },
        )

        with patch.object(client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await client.get_access_token()

            assert result == expected_token
            assert client.cached_token.access_token == expected_token
            mock_post.assert_called_once()

    async def test_fetching_token_raises_403(self, client_fixture, api_name, request):
        client = request.getfixturevalue(client_fixture)
        client.cached_token = None
        mock_response = mocked_response(status_code=403)
        mock_response.raise_for_status.side_effect = Exception("403 Forbidden")

        with patch.object(client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Token request failed"
            ) as exc_info:
                await client.get_access_token()

            assert exc_info.value.api_name == api_name

    async def test_fetching_returns_malformed_token(
        self, client_fixture, api_name, request
    ):
        client = request.getfixturevalue(client_fixture)
        client.cached_token = None
        mock_response = mocked_response(
            return_value={"invalid": "response"},
        )

        with patch.object(client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid token response"
            ) as exc_info:
                await client.get_access_token()

            assert exc_info.value.api_name == api_name


@pytest.mark.asyncio
class TestGetOffers:
    async def test_get_all_handles_empty_data(self, talentsoft_client):
        mock_response = mocked_response(return_value={})

        talentsoft_client.cached_token = cached_token()

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid response structure"
            ) as exc_info:
                await talentsoft_client.get_all()

            assert exc_info.value.api_name == "Talentsoft Front API"

    async def test_get_all_fails_due_to_unauthorized_token(self, talentsoft_client):
        response_data = offers_response()

        unauthorized_response = mocked_response(status_code=401)
        unauthorized_response.raise_for_status.side_effect = Exception(
            "401 Unauthorized"
        )

        success_response = mocked_response(return_value=response_data)

        new_token_response = mocked_response(
            return_value={
                "access_token": fake.uuid4(),
                "token_type": fake.word(),
                "expires_in": 3600,
            }
        )

        talentsoft_client.cached_token = cached_token()

        with (
            patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get,
            patch.object(
                talentsoft_client, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            mock_get.side_effect = [unauthorized_response, success_response]
            mock_post.return_value = new_token_response

            offers, has_more = await talentsoft_client.get_all()

            # Compare the number of offers and their references
            assert len(offers) == len(response_data["data"])
            # Verify that we get TalentsoftOffer objects with correct references
            expected_references = {
                offer["reference"] for offer in response_data["data"]
            }
            actual_references = {offer.reference for offer in offers}
            assert actual_references == expected_references
            assert mock_get.call_count == 2  # noqa - First failed, second succeeded
            mock_post.assert_called_once()  # Token refresh called

    async def test_get_all_fails_after_max_retries_attempts(self, talentsoft_client):
        failed_response = mocked_response(status_code=500)
        failed_response.raise_for_status.side_effect = Exception(
            "500 Internal Server Error"
        )

        talentsoft_client.cached_token = cached_token()

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = failed_response

            with pytest.raises(
                ExternalApiError, match="Request failed after retries"
            ) as exc_info:
                await talentsoft_client.get_all()

            assert exc_info.value.api_name == "Talentsoft Front API"
            assert mock_get.call_count == talentsoft_client.max_retries + 1


@pytest.mark.asyncio
class TestGetDetailOffer:
    async def test_get_detail_raises_error_if_reference_is_missing(
        self, talentsoft_client
    ):
        with pytest.raises(ExternalApiError, match="Reference is required") as exc_info:
            await talentsoft_client.get_detail(reference="")

        assert exc_info.value.api_name == "Talentsoft Front API"

    async def test_get_detail_raises_error_if_reference_is_unknown(
        self, talentsoft_client
    ):
        mock_response = mocked_response(status_code=404)
        talentsoft_client.cached_token = cached_token()

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Offer not found for reference"
            ) as exc_info:
                await talentsoft_client.get_detail(reference=fake.uuid4())

            assert exc_info.value.api_name == "Talentsoft Front API"

    async def test_get_detail_raises_error_if_response_is_malformed(
        self, talentsoft_client
    ):
        talentsoft_client.cached_token = cached_token()
        mock_response = mocked_response(return_value={"invalid": "response"})

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid response structure"
            ) as exc_info:
                await talentsoft_client.get_detail(reference=fake.uuid4())

            assert exc_info.value.api_name == "Talentsoft Front API"

    async def test_get_detail_fails_due_to_unauthorized_token(self, talentsoft_client):
        response_data = detail_offer_response()

        unauthorized_response = mocked_response(status_code=401)
        unauthorized_response.raise_for_status.side_effect = Exception(
            "401 Unauthorized"
        )

        success_response = mocked_response(return_value=response_data)

        new_token_response = mocked_response(
            return_value={
                "access_token": fake.uuid4(),
                "token_type": fake.word(),
                "expires_in": 3600,
            }
        )

        talentsoft_client.cached_token = cached_token()

        with (
            patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get,
            patch.object(
                talentsoft_client, "post", new_callable=AsyncMock
            ) as mock_post,
        ):
            mock_get.side_effect = [unauthorized_response, success_response]
            mock_post.return_value = new_token_response

            offer = await talentsoft_client.get_detail(
                reference=response_data["reference"]
            )

            assert offer.reference == response_data["reference"]
            assert mock_get.call_count == 2  # noqa - First failed, second succeeded
            mock_post.assert_called_once()  # Token refresh called

    async def test_get_detail_fails_after_max_retries_attempts(self, talentsoft_client):
        failed_response = mocked_response(status_code=500)
        failed_response.raise_for_status.side_effect = Exception(
            "500 Internal Server Error"
        )

        talentsoft_client.cached_token = cached_token()

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = failed_response

            with pytest.raises(
                ExternalApiError, match="Request failed after retries"
            ) as exc_info:
                await talentsoft_client.get_detail(reference=fake.uuid4())

            assert exc_info.value.api_name == "Talentsoft Front API"
            assert mock_get.call_count == talentsoft_client.max_retries + 1


@pytest.mark.asyncio
class TestGetVacancies:
    @pytest.mark.parametrize(
        "kwargs,limit, offset, filter",
        [
            (
                {"update_date": datetime(2026, 5, 17, 10, 30, 0)},
                1000,
                1,
                "vacancyStatus::Archived,Suspended|updateDate:gt:2026-05-17T10:30:00.00",
            ),
            (
                {
                    "update_date": datetime(2025, 7, 16, 10, 30, 0),
                    "limit": 20,
                    "offset": 3,
                    "date_operator": "lt",
                    "status": "Published",
                },
                20,
                3,
                "vacancyStatus::Published|updateDate:lt:2025-07-16T10:30:00.00",
            ),
        ],
    )
    async def test_request_contains_default_params(
        self, talentsoft_back_client, kwargs, limit, offset, filter
    ):
        return_value = {
            "code": 200,
            "status": "success",
            "data": [],
            "contentRange": "1000-10/500",
        }
        talentsoft_back_client.cached_token = cached_token()
        mock_response = mocked_response(return_value=return_value)

        with patch.object(
            talentsoft_back_client, "get", new_callable=AsyncMock
        ) as mock_get:
            mock_get.return_value = mock_response
            await talentsoft_back_client.get_vacancies(**kwargs)

            mock_get.assert_called_once()
            call_args = mock_get.call_args

            assert call_args.args[0].endswith("/api/v1/vacancies")
            assert call_args.kwargs["params"] == {
                "limit": limit,
                "offset": offset,
                "filter": filter,
            }

    @pytest.mark.parametrize(
        "contentRange,expected",
        [("1000-10/1001", True), ("1000-10/1000", False)],
    )
    async def test_has_more(self, talentsoft_back_client, contentRange, expected):
        return_value = {
            "code": 200,
            "status": "success",
            "data": [],
            "contentRange": contentRange,
        }
        talentsoft_back_client.cached_token = cached_token()
        mock_response = mocked_response(return_value=return_value)

        with patch.object(
            talentsoft_back_client, "get", new_callable=AsyncMock
        ) as mock_get:
            mock_get.return_value = mock_response
            offers, has_more = await talentsoft_back_client.get_vacancies(
                update_date=datetime.now()
            )
            assert has_more is expected

    @pytest.mark.parametrize("contentRange", ["100-10/invalid", "invalid"])
    async def test_get_vacancies_raises_error_if_count_range_is_malformed(
        self, talentsoft_back_client, contentRange
    ):
        return_value = {
            "code": 200,
            "status": "success",
            "data": [],
            "contentRange": contentRange,
        }
        talentsoft_back_client.cached_token = cached_token()
        mock_response = mocked_response(return_value=return_value)

        with patch.object(
            talentsoft_back_client, "get", new_callable=AsyncMock
        ) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid contentRange structure"
            ) as exc_info:
                await talentsoft_back_client.get_vacancies(update_date=datetime.now())

            assert exc_info.value.api_name == "Talentsoft Back API"

    async def test_get_vacancies_raises_error_if_response_is_malformed(
        self, talentsoft_back_client
    ):
        talentsoft_back_client.cached_token = cached_token()
        mock_response = mocked_response(return_value={"invalid": "response"})

        with patch.object(
            talentsoft_back_client, "get", new_callable=AsyncMock
        ) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid response structure"
            ) as exc_info:
                await talentsoft_back_client.get_vacancies(update_date=datetime.now())

            assert exc_info.value.api_name == "Talentsoft Back API"
