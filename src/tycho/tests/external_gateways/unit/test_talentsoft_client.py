"""Unit tests for TalentsoftClient."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from faker import Faker
from pydantic import HttpUrl

from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.talentsoft_config import (
    TalentsoftGatewayConfig,
)
from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient
from tests.external_gateways.utils import cached_token, mocked_response

fake = Faker()


@pytest.fixture(name="talentsoft_client")
def talentsoft_client_fixture():
    """Create a TalentsoftFrontClient instance for testing."""
    logger_service = Mock()
    logger_service.get_logger.return_value = Mock()

    config = TalentsoftGatewayConfig(
        base_url=HttpUrl(fake.url()),
        client_id=fake.uuid4(),
        client_secret=fake.uuid4(),
    )

    return TalentsoftFrontClient(
        config=config,
        logger_service=logger_service,
        timeout=30,
    )


class TestGetAccessToken:
    """Tests for get_access_token method."""

    @pytest.mark.asyncio
    async def test_cached_token_is_valid(self, talentsoft_client):
        """Test that valid cached token is returned without API call."""
        valid_token = cached_token()
        talentsoft_client.cached_token = valid_token
        result = await talentsoft_client.get_access_token()
        assert result == valid_token.access_token

    @pytest.mark.asyncio
    @pytest.mark.parametrize("cached_token", [None, cached_token(expire_in=-3600)])
    async def test_new_cached_token_has_to_be_fetched(
        self, talentsoft_client, cached_token
    ):
        """Test that new token is fetched when no cached token exists."""
        talentsoft_client.cached_token = cached_token
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
        """Test that ExternalApiError is raised."""
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
        """Test that ExternalApiError is raised when token response is malformed."""
        talentsoft_client.cached_token = None
        mock_response = mocked_response(
            return_value={"invalid": "response"},
        )

        with patch.object(
            talentsoft_client, "post", new_callable=AsyncMock
        ) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(
                ExternalApiError, match="Invalid token response"
            ) as exc_info:
                await talentsoft_client.get_access_token()

            assert exc_info.value.api_name == "Talentsoft Front API"
