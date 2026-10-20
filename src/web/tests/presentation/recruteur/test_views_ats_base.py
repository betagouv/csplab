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

    def test_base_view_sets_the_default_theme(self, db, client: Client, settings):
        settings.UI_THEME = "greige"
        response = client.get("/ats/")
        assert 'data-csp-theme-default="greige"' in response.content.decode()

    def test_base_view_sets_no_theme_by_default(self, db, client: Client, settings):
        settings.UI_THEME = ""
        response = client.get("/ats/")
        assert "data-csp-theme-default" not in response.content.decode()
