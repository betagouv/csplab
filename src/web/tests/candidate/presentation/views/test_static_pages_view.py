from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


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
