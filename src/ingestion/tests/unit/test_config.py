import pytest
from pydantic import ValidationError
from pydantic_settings import SettingsError

from api.config import TestSettings


class TestTalentsoftCredentialsParsing:
    def test_invalid_json_fails_closed(self, monkeypatch):
        monkeypatch.setenv("TALENTSOFT_CREDENTIALS", "not-json")

        with pytest.raises(SettingsError):
            TestSettings()

    def test_invalid_role_fails_closed(self, monkeypatch):
        monkeypatch.setenv(
            "TALENTSOFT_CREDENTIALS",
            '[{"client_id":"a","client_secret":"b",'
            '"base_url":"https://x.example.com","role":"bogus"}]',
        )

        with pytest.raises(ValidationError):
            TestSettings()

    def test_missing_field_fails_closed(self, monkeypatch):
        monkeypatch.setenv(
            "TALENTSOFT_CREDENTIALS",
            '[{"client_id":"a","base_url":"https://x.example.com","role":"front"}]',
        )

        with pytest.raises(ValidationError):
            TestSettings()

    def test_valid_credentials_are_parsed(self, monkeypatch):
        monkeypatch.setenv(
            "TALENTSOFT_CREDENTIALS",
            '[{"client_id":"a","client_secret":"b",'
            '"base_url":"https://x.example.com","role":"front"}]',
        )

        settings = TestSettings()

        assert len(settings.talentsoft_credentials) == 1
        assert settings.talentsoft_credentials[0].client_id == "a"
        assert settings.talentsoft_credentials[0].role == "front"
