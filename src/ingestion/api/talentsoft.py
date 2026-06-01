import base64
import hashlib
import hmac
import time
import urllib.parse

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from domain.repositories.sources_repository import ISourcesRepository
from infrastructure.credentials_store import CredentialsStore
from infrastructure.di.container import Container


# Verify the TalentSoft webhook signature
# Documentation: https://developers.cegid.com/docreference/BusinessUnits/Recruiting-developer-portal/webhooks/_index.html#signature
@inject
def verify_talentsoft_signature(
    request: Request,
    sources_repository: ISourcesRepository = Depends(
        Provide[Container.sources_repository]
    ),
    credentials_store: CredentialsStore = Depends(Provide[Container.credentials_store]),
) -> None:
    client_id = request.query_params.get("client_id")
    expires = request.headers.get("x-ts-rec-expires")
    # Extract signature from the raw query string: request.query_params decodes
    # '+' as space (form-encoding), corrupting base64 signatures that contain '+'.
    signature = None
    for part in request.url.query.split("&"):
        if part.startswith("signature="):
            signature = urllib.parse.unquote(part[len("signature=") :])

    if not client_id or not expires or not signature:
        raise HTTPException(status_code=403, detail="Missing signature parameters")

    try:
        expires_ts = int(expires)
    except ValueError:
        raise HTTPException(  # noqa: B904
            status_code=403, detail="Invalid expires parameter"
        )

    if time.time() > expires_ts:
        raise HTTPException(status_code=403, detail="Signature has expired")

    if len(credentials_store) == 0:
        raise HTTPException(
            status_code=500, detail="TalentSoft credentials not configured"
        )

    source = sources_repository.get_by_client_id_back(client_id)
    if source is None:
        raise HTTPException(status_code=403, detail="Invalid client_id")

    talentsoft_client_secret = credentials_store.get_secret(client_id)
    if talentsoft_client_secret is None:
        raise HTTPException(
            status_code=500, detail="TalentSoft credentials not configured"
        )

    # CanonicalizedTsRecHeaders: x-ts-rec-* headers, lowercased, sorted
    ts_rec_headers = sorted(
        (name.lower(), value.strip())
        for name, value in request.headers.items()
        if name.lower().startswith("x-ts-rec-")
    )
    canonicalized_headers = "".join(
        f"{name}:{value}\n" for name, value in ts_rec_headers
    )

    # CanonicalizedResource: path + query string excluding the signature parameter
    query_items = [
        (k, v) for k, v in request.query_params.multi_items() if k != "signature"
    ]
    query_string = urllib.parse.urlencode(query_items)
    canonicalized_resource = request.url.path
    if query_string:
        canonicalized_resource += "?" + query_string

    content_md5 = request.headers.get("content-md5", "")
    content_type = request.headers.get("content-type", "")
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

    secret = talentsoft_client_secret.encode("utf-8")
    digest = hmac.new(secret, string_to_sign.encode("utf-8"), hashlib.sha1).digest()
    computed = base64.b64encode(digest).decode("utf-8")

    if not hmac.compare_digest(computed, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
