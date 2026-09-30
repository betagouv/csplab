import re
from http import HTTPStatus

from django.test import Client
from django.urls import reverse
from dsfr.models import DsfrConfig


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


CHOISIR_LE_SERVICE_PUBLIC_URL = "https://choisirleservicepublic.gouv.fr/"
CHOISIR_LE_SERVICE_PUBLIC_LINKS = 2  # bandeau + bouton principal


class TestHomeView:
    def test_displays_product_paused_notice(self, db, client: Client):
        content = client.get(reverse("pages:home")).content.decode()

        assert "Produit en pause" in content

    def test_ctas_open_choisir_le_service_public_in_new_tab(self, db, client: Client):
        content = client.get(reverse("pages:home")).content.decode()

        links = [
            tag
            for tag in re.findall(r"<a\b[^>]*>", content)
            if f'href="{CHOISIR_LE_SERVICE_PUBLIC_URL}"' in tag
        ]

        assert "Visiter Choisir le Service Public" in content
        assert len(links) == CHOISIR_LE_SERVICE_PUBLIC_LINKS
        assert all('target="_blank"' in tag for tag in links)
        assert all(re.search(r'rel="[^"]*\bnoopener\b', tag) for tag in links)

    def test_no_longer_links_to_cv_upload(self, db, client: Client):
        content = client.get(reverse("pages:home")).content.decode()

        assert f'href="{reverse("candidate:cv_upload")}"' not in content
        for label in (
            "Analyser mon CV",
            "Découvrir toutes les opportunités",
            "Voir les opportunités faites pour moi",
        ):
            assert label not in content

    def test_notice_is_not_displayed_on_other_pages(self, db, client: Client):
        content = client.get(reverse("pages:legal_notices")).content.decode()

        assert "Produit en pause" not in content

    def test_keeps_admin_notice_alongside_product_paused_notice(
        self, db, client: Client
    ):
        DsfrConfig.objects.create(notice_title="Maintenance programmée")

        content = client.get(reverse("pages:home")).content.decode()

        assert "Maintenance programmée" in content
        assert "Produit en pause" in content
