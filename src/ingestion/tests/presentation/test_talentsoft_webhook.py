import base64
import hashlib
import time
import urllib.parse

import pytest

from tests.conftest import (
    WEBHOOK_PATH,
    make_signature,
    valid_query_items,
    valid_ts_rec_headers,
)


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature(talentsoft_client):
    query_items = valid_query_items()
    ts_rec_headers = valid_ts_rec_headers()
    signature = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=ts_rec_headers
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature_with_content_type_and_md5(
    talentsoft_client,
):
    body = b'{"event": "candidate.created"}'
    content_type = "application/json"
    query_items = valid_query_items()
    ts_rec_headers = valid_ts_rec_headers()
    signature = make_signature(
        WEBHOOK_PATH,
        query_items,
        content_type=content_type,
        body=body,
        ts_rec_headers=ts_rec_headers,
    )
    query_items.append(("signature", signature))
    content_md5 = base64.b64encode(hashlib.md5(body).digest()).decode()  # noqa: S324

    response = talentsoft_client.post(
        WEBHOOK_PATH,
        params=query_items,
        content=body,
        headers={
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            **ts_rec_headers,
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_talentsoft_webhook_valid_signature_with_ts_rec_headers(
    talentsoft_client,
):
    query_items = valid_query_items()
    ts_rec_headers = {
        "X-TS-REC-Expires": str(int(time.time()) + 300),
        "X-TS-REC-Event": "candidate.created",
        "X-TS-REC-TraceId": "abc123",
    }
    signature = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers)
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
    query_items = valid_query_items()
    ts_rec_headers = valid_ts_rec_headers(expires=past_expires)
    signature = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=ts_rec_headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Signature has expired"


@pytest.mark.asyncio
async def test_talentsoft_webhook_invalid_client_id(talentsoft_client):
    query_items = [("client_id", "wrong_client")]
    ts_rec_headers = valid_ts_rec_headers()
    signature = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=ts_rec_headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid client_id"


@pytest.mark.asyncio
async def test_talentsoft_webhook_invalid_signature(talentsoft_client):
    query_items = valid_query_items()
    query_items.append(("signature", "invalidsignature"))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=valid_ts_rec_headers()
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid signature"


@pytest.mark.asyncio
async def test_talentsoft_webhook_signature_with_raw_plus(talentsoft_client):
    # Talentsoft sends the signature with unencoded '+' in the URL.
    # Find an expires value that produces a '+' in the base64 signature.
    query_items = valid_query_items()
    ts_rec_headers = None
    signature = None
    for offset in range(1000):
        expires = int(time.time()) + 300 + offset
        headers = valid_ts_rec_headers(expires=expires)
        sig = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=headers)
        if "+" in sig:
            ts_rec_headers = headers
            signature = sig
            break
    assert signature is not None and "+" in signature

    # Build the URL with a raw '+' (not %2B) to replicate Talentsoft's behavior.
    raw_query = urllib.parse.urlencode(query_items) + "&signature=" + signature
    response = talentsoft_client.post(
        f"{WEBHOOK_PATH}?{raw_query}", headers=ts_rec_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_talentsoft_webhook_unconfigured_credentials(test_client):
    assert len(test_client.app.state.container.credentials_store()) == 0

    query_items = valid_query_items()
    query_items.append(("signature", "any"))

    response = test_client.post(
        WEBHOOK_PATH, params=query_items, headers=valid_ts_rec_headers()
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "TalentSoft credentials not configured"


@pytest.mark.asyncio
async def test_talentsoft_webhook_invalid_expires_parameter(talentsoft_client):
    query_items = valid_query_items()
    ts_rec_headers = {"X-TS-REC-Expires": "not-a-number"}
    signature = make_signature(WEBHOOK_PATH, query_items, ts_rec_headers=ts_rec_headers)
    query_items.append(("signature", signature))

    response = talentsoft_client.post(
        WEBHOOK_PATH, params=query_items, headers=ts_rec_headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid expires parameter"
