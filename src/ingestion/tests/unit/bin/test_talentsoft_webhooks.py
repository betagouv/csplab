import json
from collections.abc import Iterator
from datetime import date

import httpx
import pytest
from pytest_httpx import HTTPXMock

from bin.talentsoft_webhooks import (
    CALLBACK_URLS,
    DEFAULT_EVENTS,
    CreationResult,
    DeletionResult,
    creation_summary,
    deletion_summary,
    parse_hook_ids,
    run,
)
from domain.value_objects.talentsoft_credential import TalentsoftCredential

BASE_URL = "https://talentsoft.example.com/"
TOKEN_URL = "https://talentsoft.example.com/api/token"
WEBHOOKS_URL = "https://talentsoft.example.com/api/system/v1/webhooks"
BACK_SECRET = "back-secret"
FRONT_SECRET = "front-secret"
BACK = TalentsoftCredential(
    client_id="back-id", client_secret=BACK_SECRET, base_url=BASE_URL, role="back"
)
FRONT = TalentsoftCredential(
    client_id="front-id", client_secret=FRONT_SECRET, base_url=BASE_URL, role="front"
)


def _answers(*values: str):
    iterator: Iterator[str] = iter(values)
    return lambda _question: next(iterator)


@pytest.fixture
def client() -> Iterator[httpx.Client]:
    with httpx.Client() as client:
        yield client


def _mock_token(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST", url=TOKEN_URL, json={"access_token": "token"}
    )


def test_run_creates_default_events_and_prints_hook_ids(
    httpx_mock: HTTPXMock, client: httpx.Client, capsys
):
    _mock_token(httpx_mock)
    for index, _event in enumerate(DEFAULT_EVENTS):
        httpx_mock.add_response(
            method="POST", url=WEBHOOKS_URL, json={"data": {"hookId": f"hook-{index}"}}
        )

    exit_code = run(_answers("1", "1", "1", "", "o"), client, [FRONT, BACK])

    assert exit_code == 0
    webhook_requests = httpx_mock.get_requests(method="POST", url=WEBHOOKS_URL)
    assert [json.loads(r.content) for r in webhook_requests] == [
        {
            "event": event,
            "callbackUrl": CALLBACK_URLS["prod"],
            "pingUrl": CALLBACK_URLS["prod"],
        }
        for event in DEFAULT_EVENTS
    ]
    assert all(r.headers["Authorization"] == "Bearer token" for r in webhook_requests)
    output = capsys.readouterr().out
    assert "vacancy_status : hook-3" in output
    assert "Client ID back : back-id" in output


def test_run_stops_at_first_failure_and_still_prints_created_hook_ids(
    httpx_mock: HTTPXMock, client: httpx.Client, capsys
):
    _mock_token(httpx_mock)
    httpx_mock.add_response(
        method="POST", url=WEBHOOKS_URL, json={"data": {"hookId": "hook-1"}}
    )
    httpx_mock.add_response(method="POST", url=WEBHOOKS_URL, status_code=400)

    exit_code = run(
        _answers("1", "1", "3", "https://callback", "a b c", "o"), client, [BACK]
    )

    assert exit_code == 1
    assert len(httpx_mock.get_requests(method="POST", url=WEBHOOKS_URL)) == 2
    output = capsys.readouterr().out
    assert "Création de b refusée (HTTP 400)" in output
    assert "a : hook-1" in output
    assert "Callback URL : https://callback" in output


def test_run_creation_aborts_without_confirmation(
    httpx_mock: HTTPXMock, client: httpx.Client
):
    exit_code = run(_answers("1", "1", "2", "", "n"), client, [BACK])

    assert exit_code == 0
    assert httpx_mock.get_requests() == []


def test_run_deletes_hook_ids_with_manual_credentials(
    httpx_mock: HTTPXMock, client: httpx.Client, capsys
):
    _mock_token(httpx_mock)
    httpx_mock.add_response(method="DELETE", url=f"{WEBHOOKS_URL}/hook-1")
    httpx_mock.add_response(
        method="DELETE", url=f"{WEBHOOKS_URL}/hook-2", status_code=404
    )

    exit_code = run(
        _answers("2", "1", BASE_URL, "manual-id", "hook-1, hook-2", "oui"),
        client,
        [],
        secret_prompt=_answers("manual-secret"),
    )

    assert exit_code == 1
    token_request = httpx_mock.get_request(url=TOKEN_URL)
    assert token_request is not None
    assert b"client_id=manual-id" in token_request.content
    assert b"client_secret=manual-secret" in token_request.content
    output = capsys.readouterr().out
    assert "  hook-1\n" in output
    assert "hook-2 : Suppression refusée (HTTP 404)" in output


def test_run_reports_token_failure(httpx_mock: HTTPXMock, client: httpx.Client, capsys):
    httpx_mock.add_response(method="POST", url=TOKEN_URL, status_code=401)

    exit_code = run(_answers("2", "1", "hook-1", "o"), client, [BACK])

    assert exit_code == 1
    assert "Token refusé (HTTP 401)" in capsys.readouterr().out


def test_parse_hook_ids_accepts_commas_spaces_and_newlines():
    assert parse_hook_ids("a, b\nc  d,") == ["a", "b", "c", "d"]


def test_creation_summary():
    summary = creation_summary(
        BACK,
        "https://callback",
        CreationResult(hook_ids={"vacancy_new": "hook-1"}),
        date(2026, 11, 20),
    )

    assert summary.splitlines()[1:-1] == [
        "Webhooks Talentsoft",
        "Créés le : 2026-11-20",
        f"Instance : {BASE_URL}",
        "Client ID back : back-id",
        "Callback URL : https://callback",
        "hookIds :",
        "  vacancy_new : hook-1",
    ]
    assert BACK_SECRET not in summary


def test_deletion_summary_without_deleted_hook():
    summary = deletion_summary(
        BACK,
        DeletionResult(deleted=[], failed={"hook-1": "erreur"}),
        date(2026, 11, 20),
    )

    assert summary.splitlines()[1:-1] == [
        "Webhooks Talentsoft",
        "Supprimés le : 2026-11-20",
        f"Instance : {BASE_URL}",
        "hookIds :",
        "  (aucun)",
        "Échecs :",
        "  hook-1 : erreur",
    ]
