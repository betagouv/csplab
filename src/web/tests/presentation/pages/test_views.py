from http import HTTPStatus

from django.test import Client
from django.urls import reverse


class TestApiGuideView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:api_guide"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/api_guide.html" in [t.name for t in response.templates]


class TestTermsView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:terms"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/terms.html" in [t.name for t in response.templates]


class TestAccessibilityView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:accessibility"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/accessibility.html" in [t.name for t in response.templates]


class TestPrivacyView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:privacy"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/privacy.html" in [t.name for t in response.templates]


class TestLegalNoticesView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:legal_notices"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/legal_notices.html" in [t.name for t in response.templates]
