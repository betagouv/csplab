import base64
import hashlib
import hmac
import time
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from api.main import create_app

TALENTSOFT_CLIENT_ID = "test_client_id"
TALENTSOFT_CLIENT_SECRET = "test_client_secret"
WEBHOOK_PATH = "/webhooks/talentsoft"


@pytest.fixture
def test_client(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    app = create_app()
    return TestClient(app)


@pytest.fixture
def talentsoft_client(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_CLIENT_ID", TALENTSOFT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_CLIENT_SECRET", TALENTSOFT_CLIENT_SECRET)
    app = create_app()
    return TestClient(app)


def _make_signature(
    path: str,
    query_items: list[tuple[str, str]],
    content_type: str = "",
    body: bytes = b"",
    ts_rec_headers: dict[str, str] | None = None,
) -> str:
    expires = next(v for k, v in query_items if k == "expires")

    content_md5 = (
        base64.b64encode(hashlib.md5(body).digest()).decode()  # noqa: S324
        if body
        else ""
    )

    canonicalized_headers_list = sorted(
        (name.lower(), value.strip())
        for name, value in (ts_rec_headers or {}).items()
        if name.lower().startswith("x-ts-rec-")
    )
    canonicalized_headers = "".join(
        f"{name}:{value}\n" for name, value in canonicalized_headers_list
    )

    params_no_sig = [(k, v) for k, v in query_items if k != "signature"]
    query_string = urllib.parse.urlencode(params_no_sig)
    canonicalized_resource = f"{path}?{query_string}" if query_string else path

    string_to_sign = (
        "POST\n"
        + content_md5
        + "\n"
        + content_type
        + "\n"
        + expires
        + "\n"
        + canonicalized_headers
        + canonicalized_resource
    )

    secret = TALENTSOFT_CLIENT_SECRET.encode("utf-8")
    digest = hmac.new(secret, string_to_sign.encode("utf-8"), hashlib.sha1).digest()
    return urllib.parse.quote(base64.b64encode(digest).decode("utf-8"))


def _valid_query_items(expires: int | None = None) -> list[tuple[str, str]]:
    if expires is None:
        expires = int(time.time()) + 300
    return [("client_id", TALENTSOFT_CLIENT_ID), ("expires", str(expires))]


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature(talentsoft_client):
    query_items = _valid_query_items()
    signature = _make_signature(WEBHOOK_PATH, query_items)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(WEBHOOK_PATH, params=query_items)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature_with_content_type_and_md5(
    talentsoft_client,
):
    body = b'{"event": "candidate.created"}'
    content_type = "application/json"
    query_items = _valid_query_items()
    signature = _make_signature(
        WEBHOOK_PATH, query_items, content_type=content_type, body=body
    )
    query_items.append(("signature", signature))
    content_md5 = base64.b64encode(hashlib.md5(body).digest()).decode()  # noqa: S324

    response = talentsoft_client.post(
        WEBHOOK_PATH,
        params=query_items,
        content=body,
        headers={"Content-Type": content_type, "Content-MD5": content_md5},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature_with_ts_rec_headers(
    talentsoft_client,
):
    query_items = _valid_query_items()
    ts_rec_headers = {
        "X-TS-REC-Event": "candidate.created",
        "X-TS-REC-TraceId": "abc123",
    }
    signature = _make_signature(
        WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers
    )
    query_items.append(("signature", signature))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=ts_rec_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_talentsoft_webhook_missing_signature_params(talentsoft_client):
    response = talentsoft_client.post(WEBHOOK_PATH)
    assert response.status_code == 403
    assert response.json()["detail"] == "Missing signature parameters"


@pytest.mark.asyncio
async def test_talentsoft_webhook_expired_signature(talentsoft_client):
    past_expires = int(time.time()) - 60
    query_items = _valid_query_items(expires=past_expires)
    signature = _make_signature(WEBHOOK_PATH, query_items)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(WEBHOOK_PATH, params=query_items)
    assert response.status_code == 403
    assert response.json()["detail"] == "Signature has expired"


@pytest.mark.asyncio
async def test_talentsoft_webhook_invalid_client_id(talentsoft_client):
    query_items = [
        ("client_id", "wrong_client"),
        ("expires", str(int(time.time()) + 300)),
    ]
    signature = _make_signature(WEBHOOK_PATH, query_items)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(WEBHOOK_PATH, params=query_items)
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid client_id"


@pytest.mark.asyncio
async def test_talentsoft_webhook_invalid_signature(talentsoft_client):
    query_items = _valid_query_items()
    query_items.append(("signature", "invalidsignature"))

    response = talentsoft_client.post(WEBHOOK_PATH, params=query_items)
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid signature"


@pytest.mark.asyncio
async def test_talentsoft_webhook_unconfigured_credentials(test_client):
    query_items = _valid_query_items()
    query_items.append(("signature", "any"))

    response = test_client.post(WEBHOOK_PATH, params=query_items)
    assert response.status_code == 500
    assert response.json()["detail"] == "TalentSoft credentials not configured"
