import base64
import hashlib
import hmac
import json
import time
import urllib.parse

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from api.main import create_app

TALENTSOFT_CLIENT_ID = "test_client_id"
TALENTSOFT_CLIENT_SECRET = "test_client_secret"
WEB_BASE_URL = "https://web.example.com"
WEB_API_KEY = "test-web-api-key"
WEBHOOK_PATH = "/webhooks/talentsoft"


@pytest.fixture
def test_client(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.delenv("TALENTSOFT_CLIENT_ID", raising=False)
    monkeypatch.delenv("TALENTSOFT_CLIENT_SECRET", raising=False)
    app = create_app()
    return TestClient(app)


@pytest.fixture
def talentsoft_client(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_CLIENT_ID", TALENTSOFT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_CLIENT_SECRET", TALENTSOFT_CLIENT_SECRET)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    return TestClient(app)


def make_signature(
    path: str,
    query_items: list[tuple[str, str]],
    content_type: str = "",
    body: bytes = b"",
    ts_rec_headers: dict[str, str] | None = None,
) -> str:
    all_ts_rec = ts_rec_headers or {}
    expires = next(v for k, v in all_ts_rec.items() if k.lower() == "x-ts-rec-expires")

    content_md5 = (
        base64.b64encode(hashlib.md5(body).digest()).decode()  # noqa: S324
        if body
        else ""
    )

    canonicalized_headers_list = sorted(
        (name.lower(), value.strip())
        for name, value in all_ts_rec.items()
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
    return base64.b64encode(digest).decode("utf-8")


def valid_query_items() -> list[tuple[str, str]]:
    return [("client_id", TALENTSOFT_CLIENT_ID)]


def valid_ts_rec_headers(expires: int | None = None) -> dict[str, str]:
    if expires is None:
        expires = int(time.time()) + 300
    return {"X-TS-REC-Expires": str(expires)}


def make_signed_request(client: TestClient, body: dict) -> Response:
    body_bytes = json.dumps(body).encode()
    content_type = "application/json"
    ts_rec_headers = valid_ts_rec_headers()

    query_items = valid_query_items()
    signature = make_signature(
        WEBHOOK_PATH,
        query_items,
        content_type=content_type,
        ts_rec_headers=ts_rec_headers,
    )
    query_items.append(("signature", signature))

    return client.post(
        WEBHOOK_PATH,
        params=dict(query_items),
        content=body_bytes,
        headers={"Content-Type": content_type, **ts_rec_headers},
    )
