from unittest.mock import MagicMock

import pytest
from authlib.integrations.base_client.errors import OAuthError
from joserfc import jwt
from joserfc.jwk import KeySet, OctKey

from infrastructure.authentication.proconnect_client import fetch_userinfo_claims, oauth


def _signed_jwt(claims: dict, key: OctKey) -> str:
    return jwt.encode({"alg": "HS256", "kid": key.kid}, claims, key)


class TestFetchUserinfoClaims:
    def test_returns_plain_json_body(self, monkeypatch):
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"email": "user@example.com"}
        monkeypatch.setattr(oauth.proconnect, "get", MagicMock(return_value=response))

        claims = fetch_userinfo_claims({"access_token": "fake-access-token"})

        assert claims == {"email": "user@example.com"}

    def test_decodes_signed_jwt_body(self, monkeypatch):
        key = OctKey.generate_key(parameters={"kid": "test-key"})
        claims = {"email": "user@example.com"}
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("Expecting value")
        response.text = _signed_jwt(claims, key)
        monkeypatch.setattr(oauth.proconnect, "get", MagicMock(return_value=response))
        monkeypatch.setattr(
            oauth.proconnect,
            "fetch_jwk_set",
            MagicMock(return_value=KeySet([key]).as_dict()),
        )

        result = fetch_userinfo_claims({"access_token": "fake-access-token"})

        assert result == claims

    def test_raises_oautherror_on_unverifiable_body(self, monkeypatch):
        wrong_key = OctKey.generate_key(parameters={"kid": "other-key"})
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("Expecting value")
        response.text = "not-a-jwt"
        monkeypatch.setattr(oauth.proconnect, "get", MagicMock(return_value=response))
        monkeypatch.setattr(
            oauth.proconnect,
            "fetch_jwk_set",
            MagicMock(return_value=KeySet([wrong_key]).as_dict()),
        )

        with pytest.raises(OAuthError):
            fetch_userinfo_claims({"access_token": "fake-access-token"})
