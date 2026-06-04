from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db
class TestATSBase:
    def test_base_view_returns_200(self, client: Client):
        response = client.get("/ats/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_uses_correct_template(self, client: Client):
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_catches_subroutes(self, client: Client):
        response = client.get("/ats/candidates/123/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_sets_csrf_cookie(self, client: Client):
        response = client.get("/ats/")
        assert "csrftoken" in response.cookies
