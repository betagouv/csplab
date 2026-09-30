import httpx
from pytest_httpx import HTTPXMock


def test_flower_proxy_returns_503_when_not_configured(test_client, monkeypatch):
    monkeypatch.delenv("FLOWER_PORT", raising=False)

    response = test_client.get("/flower/")

    assert response.status_code == 503


def test_flower_proxy_returns_502_when_flower_is_down(
    test_client, monkeypatch, httpx_mock: HTTPXMock
):
    monkeypatch.setenv("FLOWER_PORT", "5555")
    httpx_mock.add_exception(httpx.ConnectError("All connection attempts failed"))

    response = test_client.get("/flower/")

    assert response.status_code == 502
    assert response.json() == {"detail": "Flower is unavailable"}


def test_flower_proxy_forwards_flower_response(
    test_client, monkeypatch, httpx_mock: HTTPXMock
):
    monkeypatch.setenv("FLOWER_PORT", "5555")
    httpx_mock.add_response(
        url="http://localhost:5555/flower/api/workers?refresh=1",
        status_code=401,
        text="Unauthorized",
    )

    response = test_client.get("/flower/api/workers?refresh=1")

    assert response.status_code == 401
    assert response.text == "Unauthorized"
