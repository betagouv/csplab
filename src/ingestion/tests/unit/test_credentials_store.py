import pytest

from infrastructure.credentials_store import CredentialsStore


@pytest.fixture
def store() -> CredentialsStore:
    return CredentialsStore()


def test_empty_store_has_length_zero(store):
    assert len(store) == 0


def test_register_increases_length(store):
    store.register("client_a", "secret_a")
    assert len(store) == 1


def test_get_secret_returns_registered_secret(store):
    store.register("client_a", "secret_a")
    assert store.get_secret("client_a") == "secret_a"


def test_get_secret_returns_none_for_unknown_client(store):
    assert store.get_secret("unknown") is None


def test_register_multiple_clients(store):
    store.register("client_a", "secret_a")
    store.register("client_b", "secret_b")
    assert len(store) == 2
    assert store.get_secret("client_a") == "secret_a"
    assert store.get_secret("client_b") == "secret_b"


def test_register_overwrites_existing_secret(store):
    store.register("client_a", "old_secret")
    store.register("client_a", "new_secret")
    assert len(store) == 1
    assert store.get_secret("client_a") == "new_secret"
