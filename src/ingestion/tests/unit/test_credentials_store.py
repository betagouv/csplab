import pytest

from domain.value_objects.credentials import Credentials
from infrastructure.credentials_store import CredentialsStore


@pytest.fixture
def store() -> CredentialsStore:
    return CredentialsStore()


def _credentials(client_id: str, client_secret: str, base_url: str) -> Credentials:
    return Credentials(
        client_id=client_id, client_secret=client_secret, base_url=base_url
    )


def test_empty_store_has_length_zero(store):
    assert len(store) == 0


def test_register_increases_length(store):
    store.register(_credentials("client_a", "secret_a", "https://a.example.com"))
    assert len(store) == 1


def test_get_secret_returns_registered_secret(store):
    store.register(_credentials("client_a", "secret_a", "https://a.example.com"))
    assert store.get_secret("client_a") == "secret_a"


def test_get_secret_returns_none_for_unknown_client(store):
    assert store.get_secret("unknown") is None


def test_register_multiple_clients(store):
    store.register(_credentials("client_a", "secret_a", "https://a.example.com"))
    store.register(_credentials("client_b", "secret_b", "https://b.example.com"))
    assert len(store) == 2
    assert store.get_secret("client_a") == "secret_a"
    assert store.get_secret("client_b") == "secret_b"


def test_register_overwrites_existing_secret(store):
    store.register(_credentials("client_a", "old_secret", "https://a.example.com"))
    store.register(_credentials("client_a", "new_secret", "https://a.example.com"))
    assert len(store) == 1
    assert store.get_secret("client_a") == "new_secret"


def test_get_credentials_returns_full_credentials(store):
    store.register(_credentials("client_a", "secret_a", "https://a.example.com"))
    creds = store.get_credentials("client_a")
    assert creds is not None
    assert creds.client_id == "client_a"
    assert creds.client_secret == "secret_a"
    assert creds.base_url == "https://a.example.com"


def test_get_credentials_returns_none_for_unknown_client(store):
    assert store.get_credentials("unknown") is None
