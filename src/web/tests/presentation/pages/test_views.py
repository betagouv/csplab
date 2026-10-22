import re
from http import HTTPStatus

from django.test import Client
from django.urls import reverse
from dsfr.models import DsfrConfig

from presentation.pages.views import _render_guide


class TestApiGuideView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:api_guide"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/api_guide.html" in [t.name for t in response.templates]

    def test_renders_guide_with_side_menu(self, db, client: Client):
        response = client.get(reverse("pages:api_guide"))

        assert response.context["toc_items"]
        assert 'class="fr-h1"' in response.content.decode()


class TestRenderGuide:
    def test_adds_anchor_and_dsfr_class_to_headings(self):
        html, _ = _render_guide("# L'API — POST /api/token/")

        assert '<h1 id="lapi-post-apitoken" class="fr-h1">' in html

    def test_builds_nested_side_menu_from_headings(self):
        _, toc_items = _render_guide(
            "# Guide\n\n## Authentification\n\n### Obtenir un `jeton`\n\n# Annexe"
        )

        assert toc_items == [
            {
                "label": "Guide",
                "link": "#guide",
                "items": [
                    {
                        "label": "Authentification",
                        "link": "#authentification",
                        "items": [
                            {"label": "Obtenir un jeton", "link": "#obtenir-un-jeton"}
                        ],
                    }
                ],
            },
            {"label": "Annexe", "link": "#annexe"},
        ]

    def test_suffixes_duplicate_anchors(self):
        html, toc_items = _render_guide("## Réponses\n\n## Réponses\n\n## Réponses")

        assert [item["link"] for item in toc_items] == [
            "#reponses",
            "#reponses_1",
            "#reponses_2",
        ]
        assert '<h2 id="reponses_1" class="fr-h2">' in html

    def test_adds_anchor_without_menu_entry_below_level_3(self):
        html, toc_items = _render_guide("## Titre\n\n#### Détail")

        assert toc_items == [{"label": "Titre", "link": "#titre"}]
        assert '<h4 id="detail">Détail</h4>' in html

    def test_adds_dsfr_class_to_horizontal_rules(self):
        html, _ = _render_guide("Avant\n\n---\n\nAprès")

        assert '<hr class="fr-hr fr-my-4w" />' in html

    def test_wraps_tables_in_dsfr_containers(self):
        html, _ = _render_guide("| Code | Sens |\n| --- | --- |\n| 200 | OK |")

        assert '<div class="fr-table__content"><table>' in html


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
