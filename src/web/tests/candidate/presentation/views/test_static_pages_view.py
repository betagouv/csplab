from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


class TestSecurityTxtView:
    def test_security_txt(self, client, db):
        response = client.get("/.well-known/security.txt")
        assert response.status_code == HTTPStatus.OK
        assert "text/plain" in response["Content-Type"]
        content = response.content.decode()
        assert "Contact: mailto:ops.csplab@beta.gouv.fr" in content
        assert "Preferred-Languages: fr, en" in content


@pytest.mark.parametrize(
    ("url_name", "template_name"),
    [
        ("pages:home", "pages/home.html"),
        ("pages:terms", "pages/terms.html"),
        ("pages:accessibility", "pages/accessibility.html"),
        ("pages:privacy", "pages/privacy.html"),
        ("pages:legal_notices", "pages/legal_notices.html"),
    ],
)
class TestStaticPagesView:
    def test_static_page(self, client, db, url_name, template_name):
        response = client.get(reverse(url_name))
        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, template_name)
