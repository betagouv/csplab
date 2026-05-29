from unittest.mock import MagicMock

import pytest

from infrastructure.talentsoft_client_repository import TalentsoftClientRepository


@pytest.fixture
def registry() -> TalentsoftClientRepository:
    return TalentsoftClientRepository()


def test_get_returns_none_for_unknown_client(registry):
    assert registry.get("unknown") is None


def test_register_and_retrieve_client(registry):
    client = MagicMock()
    registry.register("client_a", client)
    assert registry.get("client_a") is client


def test_register_multiple_clients(registry):
    client_a = MagicMock()
    client_b = MagicMock()
    registry.register("client_a", client_a)
    registry.register("client_b", client_b)
    assert registry.get("client_a") is client_a
    assert registry.get("client_b") is client_b


def test_register_overwrites_existing_client(registry):
    old_client = MagicMock()
    new_client = MagicMock()
    registry.register("client_a", old_client)
    registry.register("client_a", new_client)
    assert registry.get("client_a") is new_client
