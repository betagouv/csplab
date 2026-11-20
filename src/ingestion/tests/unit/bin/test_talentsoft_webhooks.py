import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from bin.talentsoft_webhooks import CALLBACK_URLS, DEFAULT_EVENTS, main
from domain.value_objects.talentsoft_credential import TalentsoftCredential

BASE_URL = "https://talentsoft.example.com/"
TOKEN_URL = "https://talentsoft.example.com/api/token"
WEBHOOKS_URL = "https://talentsoft.example.com/api/system/v1/webhooks"
SECRET = "back-secret"
BACK = TalentsoftCredential("back-id", SECRET, BASE_URL, "back")
FRONT = TalentsoftCredential("front-id", SECRET, BASE_URL, "front")


@pytest.fixture
def answers(monkeypatch):
    def set_answers(*values: str) -> None:
        iterator = iter(values)
        monkeypatch.setattr("builtins.input", lambda _question: next(iterator))

    return set_answers


@pytest.fixture
def client():
    with httpx.Client() as client:
        yield client


@pytest.fixture
def token(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url=TOKEN_URL, json={"access_token": "token"})


@pytest.mark.usefixtures("token")
def test_creates_default_events_and_prints_hook_ids(
    answers, client, httpx_mock: HTTPXMock, capsys
):
    for index in range(len(DEFAULT_EVENTS)):
        httpx_mock.add_response(
            url=WEBHOOKS_URL, json={"data": {"hookId": f"h{index}"}}
        )
    answers("1", "1", "1", "", "o")

    assert main(client, [FRONT, BACK]) == 0

    requests = httpx_mock.get_requests(url=WEBHOOKS_URL)
    assert [json.loads(r.content)["event"] for r in requests] == DEFAULT_EVENTS
    assert json.loads(requests[0].content)["callbackUrl"] == CALLBACK_URLS[0]
    assert requests[0].headers["Authorization"] == "Bearer token"
    output = capsys.readouterr().out
    assert "  vacancy_status : h3" in output
    assert "Client ID back : back-id" in output
    assert SECRET not in output


@pytest.mark.usefixtures("token")
def test_stops_at_first_failure_and_still_prints_created_hook_ids(
    answers, client, httpx_mock: HTTPXMock, capsys
):
    httpx_mock.add_response(url=WEBHOOKS_URL, json={"data": {"hookId": "h1"}})
    httpx_mock.add_response(url=WEBHOOKS_URL, status_code=400)
    answers("1", "1", "3", "https://callback", "a b c", "o")

    assert main(client, [BACK]) == 1

    assert len(httpx_mock.get_requests(url=WEBHOOKS_URL)) == 2
    output = capsys.readouterr().out
    assert "b : HTTP 400" in output
    assert "  a : h1" in output
    assert "Callback URL : https://callback" in output


@pytest.mark.usefixtures("token")
def test_deletes_hook_ids_with_manual_credentials(
    answers, client, httpx_mock: HTTPXMock, monkeypatch, capsys
):
    httpx_mock.add_response(method="DELETE", url=f"{WEBHOOKS_URL}/h1")
    httpx_mock.add_response(method="DELETE", url=f"{WEBHOOKS_URL}/h2")
    monkeypatch.setattr("getpass.getpass", lambda _question: "manual-secret")
    answers("2", "1", BASE_URL, "manual-id", "h1, h2", "oui")

    assert main(client, []) == 0

    token_request = httpx_mock.get_request(url=TOKEN_URL)
    assert token_request is not None
    assert b"client_secret=manual-secret" in token_request.content
    assert "  h1\n  h2\n" in capsys.readouterr().out


def test_aborts_without_confirmation(answers, client, httpx_mock: HTTPXMock):
    answers("1", "1", "2", "", "n")

    assert main(client, [BACK]) == 0

    assert httpx_mock.get_requests() == []
