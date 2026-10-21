import re
from http import HTTPStatus

from django.test import Client
from django.urls import reverse
from dsfr.models import DsfrConfig

from presentation.pages.views import _add_heading_ids_and_dsfr_classes, _markdown


class TestApiGuideView:
    def test_page_loads_successfully(self, db, client: Client):
        response = client.get(reverse("pages:api_guide"))

        assert response.status_code == HTTPStatus.OK
        assert "pages/api_guide.html" in [t.name for t in response.templates]

    def test_keeps_heading_anchors(self, db, client: Client):
        content = client.get(reverse("pages:api_guide")).content.decode()

        for heading in (
            '<h1 id="les-fonctionnalites-de-lapi" class="fr-h1">',
            '<h2 id="a-qui-sadresse-cette-api" class="fr-h2">',
            '<h3 id="obtenir-un-jeton-post-apitoken" class="fr-h3">',
            (
                '<h1 id="annexe-correspondance-entre-le-format-talentsoft-et-lapi-v1" '
                'class="fr-h1">'
            ),
        ):
            assert heading in content

    def test_builds_side_menu_from_headings(self, db, client: Client):
        toc_items = client.get(reverse("pages:api_guide")).context["toc_items"]

        guide = toc_items[0]
        assert guide["label"] == "Guide de l'API CSPLab — Version non technique"
        assert guide["link"] == "#guide-de-lapi-csplab-version-non-technique"
        authentification = next(
            item
            for item in guide["items"]
            if item["link"] == "#comment-fonctionne-lauthentification"
        )
        jeton = authentification["items"][0]
        assert jeton["label"] == "Obtenir un jeton — POST /api/token/"
        assert jeton["link"] == "#obtenir-un-jeton-post-apitoken"
        assert [item["link"] for item in toc_items[1:]] == [
            "#les-fonctionnalites-de-lapi",
            "#annexe-les-codes-de-reponse-en-clair",
            "#annexe-recapitulatif-des-listes-de-valeurs-autorisees",
            "#annexe-correspondance-entre-le-format-talentsoft-et-lapi-v1",
        ]

    def test_links_to_openapi_schema(self, db, client: Client):
        content = client.get(reverse("pages:api_guide")).content.decode()

        assert '<a href="/static/api/schema.yaml">schéma OpenAPI officiel</a>' in (
            content
        )

    def test_wraps_tables_in_dsfr_containers(self, db, client: Client):
        content = client.get(reverse("pages:api_guide")).content.decode()

        assert '<div class="fr-table__content"><table>' in content


class TestGuideHeadings:
    def render(self, text: str) -> tuple[str, list[dict]]:
        tokens = _markdown.parse(text)
        toc_items = _add_heading_ids_and_dsfr_classes(tokens)
        return _markdown.renderer.render(tokens, _markdown.options, {}), toc_items

    def test_suffixes_duplicate_anchors(self):
        html, toc_items = self.render("## Réponses\n\n## Réponses\n\n## Réponses")

        assert [item["link"] for item in toc_items] == [
            "#reponses",
            "#reponses_1",
            "#reponses_2",
        ]
        assert '<h2 id="reponses_1" class="fr-h2">' in html

    def test_adds_anchor_without_menu_entry_below_level_3(self):
        html, toc_items = self.render("## Titre\n\n#### Détail")

        assert toc_items == [{"label": "Titre", "link": "#titre"}]
        assert '<h4 id="detail">Détail</h4>' in html

    def test_adds_dsfr_class_to_horizontal_rules(self):
        html, _ = self.render("Avant\n\n---\n\nAprès")

        assert '<hr class="fr-hr fr-my-4w" />' in html


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
