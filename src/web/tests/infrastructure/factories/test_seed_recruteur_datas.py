import secrets

from django.contrib.auth import authenticate

from infrastructure.factories.seed_recruteur_datas import (
    _ADMIN_SPEC,
    _AGENTS_SPECS,
    _CANDIDATS_SPECS,
    seed_recruteur_datas,
)

SEED_EMAILS = [
    _AGENTS_SPECS[0]["email"],
    _ADMIN_SPEC["email"],
    _CANDIDATS_SPECS[0]["email"],
]


class TestSeedRecruteurDatas:
    def test_accounts_log_in_with_the_configured_password(self, db, monkeypatch):
        password = secrets.token_urlsafe()
        monkeypatch.setenv("SEED_USER_PASSWORD", password)

        seed_recruteur_datas()

        for email in SEED_EMAILS:
            assert authenticate(username=email, password=password) is not None, email

    def test_accounts_log_in_with_the_generated_password(self, db, monkeypatch):
        monkeypatch.delenv("SEED_USER_PASSWORD", raising=False)

        context = seed_recruteur_datas()

        user = authenticate(
            username=_AGENTS_SPECS[0]["email"], password=context["seed_password"]
        )
        assert user is not None
