import logging
from typing import Literal

import pytest

from domain.value_objects.talentsoft_credential import TalentsoftCredential
from infrastructure.di.container import (
    Container,
    _build_credentials_store,
    register_talentsoft_front_clients,
)

_logger = logging.getLogger(__name__)


def _credential(client_id: str, role: Literal["front", "back"]) -> TalentsoftCredential:
    return TalentsoftCredential(
        client_id=client_id,
        client_secret=f"secret-{client_id}",
        base_url=f"https://{client_id}.example.com",
        role=role,
    )


class TestBuildCredentialsStore:
    def test_registers_every_credential_regardless_of_role(self):
        credentials = [
            _credential("front_a", "front"),
            _credential("front_b", "front"),
            _credential("back_a", "back"),
        ]

        store = _build_credentials_store(credentials)

        assert len(store) == 3
        for credential in credentials:
            assert store.get_secret(credential.client_id) == credential.client_secret

    def test_raises_on_duplicate_client_id_across_roles(self):
        credentials = [
            _credential("shared", "front"),
            _credential("shared", "back"),
        ]

        with pytest.raises(ValueError, match="Duplicate client_id"):
            _build_credentials_store(credentials)


class TestRegisterTalentsoftFrontClients:
    def test_registers_only_front_credentials_as_active_clients(self):
        container = Container()
        credentials = [
            _credential("front_a", "front"),
            _credential("front_b", "front"),
            _credential("back_a", "back"),
        ]

        register_talentsoft_front_clients(container, credentials, _logger)

        repository = container.talentsoft_client_repository()
        assert repository.get("front_a") is not None
        assert repository.get("front_b") is not None
        assert repository.get("back_a") is None

    def test_registers_no_clients_when_no_front_credentials(self):
        container = Container()
        credentials = [_credential("back_a", "back")]

        register_talentsoft_front_clients(container, credentials, _logger)

        repository = container.talentsoft_client_repository()
        assert repository.get("back_a") is None
