from http import HTTPStatus

from django.test import Client


class TestATSBase:
    def test_base_view_returns_200(self, db, client: Client):
        response = client.get("/ats/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_uses_correct_template(self, db, client: Client):
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_catches_subroutes(self, db, client: Client):
        response = client.get("/ats/candidates/123/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_sets_csrf_cookie(self, db, client: Client):
        response = client.get("/ats/")
        assert "csrftoken" in response.cookies

    def test_base_view_sets_no_shape_by_default(self, db, client: Client, settings):
        settings.UI_SHAPE = ""
        response = client.get("/ats/")
        assert "data-csp-shape" not in response.content.decode()

    def test_base_view_sets_the_density(self, db, client: Client, settings):
        settings.UI_DENSITY = "compact"
        response = client.get("/ats/")
        assert 'data-csp-density="compact"' in response.content.decode()

    def test_base_view_sets_the_shape_alone(self, db, client: Client, settings):
        settings.UI_SHAPE = "rounded"
        settings.UI_DENSITY = ""
        content = client.get("/ats/").content.decode()
        assert 'data-csp-shape="rounded"' in content
        assert "data-csp-density" not in content

    def test_base_view_opens_the_preview_outside_production(
        self, db, client: Client, monkeypatch
    ):
        monkeypatch.setenv("SCALEWAY_ENV", "demo")
        response = client.get("/ats/")
        assert "data-csp-ui-preview" in response.content.decode()

    def test_base_view_opens_the_preview_without_scaleway_env(
        self, db, client: Client, monkeypatch
    ):
        monkeypatch.delenv("SCALEWAY_ENV", raising=False)
        response = client.get("/ats/")
        assert "data-csp-ui-preview" in response.content.decode()

    def test_base_view_refuses_the_preview_in_production(
        self, db, client: Client, monkeypatch
    ):
        monkeypatch.setenv("SCALEWAY_ENV", "prod")
        response = client.get("/ats/")
        assert "data-csp-ui-preview" not in response.content.decode()
