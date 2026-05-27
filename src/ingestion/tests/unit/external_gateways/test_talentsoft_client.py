import logging
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker

from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from tests.unit.external_gateways.utils import (
    cached_token,
    detail_offer_response,
    mocked_response,
)

fake = Faker()


class TestTalentsoftConfig:
    def test_base_url_trailing_slash_is_stripped(self):
        config = TalentsoftConfig(
            base_url="https://example.com/",
            client_id=fake.uuid4(),
            client_secret=fake.uuid4(),
        )
        assert config.base_url == "https://example.com"

    def test_base_url_without_trailing_slash_is_unchanged(self):
        config = TalentsoftConfig(
            base_url="https://example.com",
            client_id=fake.uuid4(),
            client_secret=fake.uuid4(),
        )
        assert config.base_url == "https://example.com"

    def test_base_url_multiple_trailing_slashes_are_stripped(self):
        config = TalentsoftConfig(
            base_url="https://example.com///",
            client_id=fake.uuid4(),
            client_secret=fake.uuid4(),
        )
        assert config.base_url == "https://example.com"


@pytest.fixture(name="talentsoft_client")
def talentsoft_client_fixture():
    config = TalentsoftConfig(
        base_url=fake.url().rstrip("/"),
        client_id=fake.uuid4(),
        client_secret=fake.uuid4(),
    )
    return TalentsoftFrontClient(
        config=config, logger=logging.getLogger("test"), timeout=30
    )


class TestGetAccessToken:
    @pytest.mark.asyncio
    async def test_cached_token_is_valid(self, talentsoft_client):
        valid_token = cached_token()
        talentsoft_client.cached_token = valid_token
        result = await talentsoft_client.get_access_token()
        assert result == valid_token.access_token

    @pytest.mark.asyncio
    @pytest.mark.parametrize("initial_token", [None, cached_token(expire_in=-3600)])
    async def test_new_cached_token_has_to_be_fetched(
        self, talentsoft_client, initial_token
    ):
        talentsoft_client.cached_token = initial_token
        expected_token = fake.uuid4()
        mock_response = mocked_response(
            return_value={
                "access_token": expected_token,
                "token_type": fake.word(),
                "expires_in": 3600,
            },
        )

        with patch.object(
            talentsoft_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response
            result = await talentsoft_client.get_access_token()

            assert result == expected_token
            assert talentsoft_client.cached_token.access_token == expected_token
            mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetching_token_raises_403(self, talentsoft_client):
        talentsoft_client.cached_token = None
        mock_response = mocked_response(status_code=403)
        mock_response.raise_for_status.side_effect = Exception("403 Forbidden")

        with patch.object(
            talentsoft_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Token request failed"
            ) as exc_info:
                await talentsoft_client.get_access_token()

            assert exc_info.value.api_name == "Talentsoft Front API"

    @pytest.mark.asyncio
    async def test_fetching_returns_malformed_token(self, talentsoft_client):
        talentsoft_client.cached_token = None
        mock_response = mocked_response(return_value={"invalid": "response"})

        with patch.object(
            talentsoft_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid token response"
            ) as exc_info:
                await talentsoft_client.get_access_token()

            assert exc_info.value.api_name == "Talentsoft Front API"


class TestGetDetailOffer:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "reference, mock_response, expected_error",
        [
            pytest.param("", None, "Reference is required", id="missing_reference"),
            pytest.param(
                None,
                mocked_response(status_code=404),
                "Offer not found for reference",
                id="unknown_reference",
            ),
            pytest.param(
                None,
                mocked_response(return_value={"invalid": "response"}),
                "Invalid response structure",
                id="malformed_response",
            ),
        ],
    )
    async def test_get_detail_raises_error(
        self, talentsoft_client, reference, mock_response, expected_error
    ):
        talentsoft_client.cached_token = cached_token()

        with patch.object(talentsoft_client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(ExternalApiError, match=expected_error) as exc_info:
                await talentsoft_client.get_detail(
                    reference=reference if reference is not None else fake.uuid4()
                )

        assert exc_info.value.api_name == "Talentsoft Front API"

    @pytest.mark.asyncio
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
            assert mock_get.call_count == 2
            mock_post.assert_called_once()  # Token refresh called

    @pytest.mark.asyncio
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
