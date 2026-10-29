import logging
from datetime import UTC, datetime
from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from referentiel.value_objects.contract_kind import ContractKind

from config.logger_names import LoggerName
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.fret.views import PAGINATE_BY


@pytest.fixture
def source(db):
    return SourceDjangoFactory()


@pytest.fixture
def ingestion_logs(caplog):
    logger = logging.getLogger(LoggerName.INGESTION.value)
    logger.addHandler(caplog.handler)
    caplog.set_level(logging.WARNING, logger=logger.name)
    yield caplog
    logger.removeHandler(caplog.handler)


@pytest.mark.parametrize(
    "url_name",
    ["fret:sources", "fret:offres", "fret:offre"],
)
def test_pages_are_not_found_when_fret_is_disabled(client, settings, source, url_name):
    settings.FRET_ENABLED = False
    offer = OfferDjangoFactory(source=source)
    args = {
        "fret:sources": [],
        "fret:offres": [source.source_id],
        "fret:offre": [source.source_id, offer.id],
    }[url_name]

    assert client.get(reverse(url_name, args=args)).status_code == HTTPStatus.NOT_FOUND


class TestSourceListView:
    url = reverse("fret:sources")

    def test_anonymous_sees_all_sources_ordered_by_slug(self, client, db):
        second = SourceDjangoFactory(slug="b-source")
        first = SourceDjangoFactory(slug="a-source")

        response = client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/sources.html")
        assert list(response.context["sources"]) == [first, second]

    def test_no_source_shows_empty_message(self, client, db):
        response = client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assert "Aucune source disponible." in response.content.decode()

    def test_sources_are_paginated(self, client, db):
        SourceDjangoFactory.create_batch(PAGINATE_BY + 1)

        first = client.get(self.url)
        second = client.get(self.url, {"page": 2})

        assert len(first.context["sources"]) == PAGINATE_BY
        assert len(second.context["sources"]) == 1

    def test_each_source_links_to_its_offers(self, client, source):

        response = client.get(self.url)

        assert reverse("fret:offres", args=[source.source_id]) in (
            response.content.decode()
        )


class TestOffreListView:
    @staticmethod
    def url(source):
        return reverse("fret:offres", args=[source.source_id])

    def test_anonymous_sees_the_active_offers_of_the_source(self, client, source):
        offer = OfferDjangoFactory(source=source)
        OfferDjangoFactory(source=source, archived_at=datetime(2024, 2, 1, tzinfo=UTC))
        OfferDjangoFactory()

        response = client.get(self.url(source))

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/offres.html")
        assert [o.id for o in response.context["page_obj"]] == [offer.id]

    def test_offers_are_listed_most_recently_updated_first(self, client, source):
        old = OfferDjangoFactory(
            source=source, updated_at=datetime(2024, 1, 1, tzinfo=UTC)
        )
        recent = OfferDjangoFactory(
            source=source, updated_at=datetime(2024, 3, 1, tzinfo=UTC)
        )

        response = client.get(self.url(source))

        assert [o.id for o in response.context["page_obj"]] == [recent.id, old.id]

    @pytest.mark.parametrize(
        ("term", "expected"),
        [
            ("ABC-12", ["ABC-123"]),  # référence, sans casse
            ("abc-12", ["ABC-123"]),
            ("jurist", ["XYZ-999"]),  # titre, sans casse
            ("", ["ABC-123", "XYZ-999"]),
            ("   ", ["ABC-123", "XYZ-999"]),
            ("introuvable", []),
        ],
    )
    def test_search_filters_on_reference_and_title(
        self, client, source, term, expected
    ):
        OfferDjangoFactory(source=source, reference="ABC-123", title="Développeur")
        OfferDjangoFactory(source=source, reference="XYZ-999", title="Juriste")

        response = client.get(self.url(source), {"q": term})

        assert response.status_code == HTTPStatus.OK
        assert sorted(o.reference for o in response.context["page_obj"]) == expected

    def test_search_does_not_reach_the_offers_of_other_sources(self, client, source):
        OfferDjangoFactory(source=source, reference="ABC-123")
        OfferDjangoFactory(reference="ABC-456")

        response = client.get(self.url(source), {"q": "ABC"})

        assert [o.reference for o in response.context["page_obj"]] == ["ABC-123"]

    def test_search_form_keeps_the_term_and_escapes_it(self, client, source):

        content = client.get(self.url(source), {"q": '"><script>'}).content.decode()

        assert "<script>" not in content
        assert "Aucune offre ne correspond à votre recherche." in content

    def test_unknown_source_gets_not_found_and_is_logged(
        self, client, db, ingestion_logs
    ):
        source_id = uuid4()

        response = client.get(reverse("fret:offres", args=[source_id]))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(source_id) in ingestion_logs.text

    def test_source_without_offer_shows_empty_message(self, client, source):

        response = client.get(self.url(source))

        assert response.status_code == HTTPStatus.OK
        assert "Aucune offre pour cette source." in response.content.decode()

    def test_offers_are_paginated(self, client, source):
        OfferDjangoFactory.create_batch(PAGINATE_BY + 1, source=source)

        first = client.get(self.url(source))
        second = client.get(self.url(source), {"page": 2})

        assert len(first.context["page_obj"]) == PAGINATE_BY
        assert len(second.context["page_obj"]) == 1

    def test_each_offer_links_to_its_detail(self, client, source):
        offer = OfferDjangoFactory(source=source)

        content = client.get(self.url(source)).content.decode()

        assert reverse("fret:offre", args=[source.source_id, offer.id]) in content


class TestOffreDetailView:
    @staticmethod
    def url(source, offer):
        return reverse("fret:offre", args=[source.source_id, offer.id])

    def test_anonymous_sees_the_offer(self, client, source):
        offer = OfferDjangoFactory(source=source)

        response = client.get(self.url(source, offer))

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/offre_detail.html")
        assert response.context["offre"] == offer

    def test_shows_all_known_data_of_the_offer(self, client, source):
        organisme = TalentsoftOrganismeDjangoFactory(name="Mairie de Test")
        offer = OfferDjangoFactory(
            source=source,
            talentsoft_organisme_entity_code=organisme,
            long_title="Titre long de l'offre",
            employer="Employeur Test",
            contract_kind=ContractKind.CDD_CDI.name,
            job_vacancy="1",
            code_emploi_csp="ERNUM001",
            offer_url="https://exemple.gouv.fr/offres/1",
            criteria={"diplome": "Master"},
            contacts=[
                {
                    "role": "principal",
                    "texte": "jean.dupont@exemple.gouv.fr",
                    "emails": ["jean.dupont@exemple.gouv.fr"],
                }
            ],
            location_label="Paris",
            application_deadline=datetime(2024, 5, 15, tzinfo=UTC),
        )

        content = client.get(self.url(source, offer)).content.decode()

        for expected in (
            offer.reference,
            offer.title,
            "Titre long de l&#x27;offre",
            "Employeur Test",
            "Fonction publique de l&#x27;État",
            "CDD ou CDI",
            "ERNUM001",
            "https://exemple.gouv.fr/offres/1",
            "Master",
            "Personne à contacter : jean.dupont@exemple.gouv.fr",
            "Paris",
            "15/05/2024",
            f"Mairie de Test ({organisme.entity_code})",
            offer.mission,
            offer.profile,
        ):
            assert expected in content, expected

    def test_renders_markdown_descriptions(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            mission="**Mission** du poste",
            profile="# Qualités\n\n- rigueur\n- <b>autonomie</b>",
            employer="[Site](https://exemple.gouv.fr)",
            exercise_conditions="Ligne 1\nLigne 2",
            service_description="## Service",
            complements="_Compléments_",
        )

        content = client.get(self.url(source, offer)).content.decode()

        for expected in (
            "<p><strong>Mission</strong> du poste</p>",
            "<h3>Qualités</h3>",
            "<li>&lt;b&gt;autonomie&lt;/b&gt;</li>",
            (
                '<a href="https://exemple.gouv.fr" target="_blank" '
                'rel="noopener noreferrer">Site</a>'
            ),
            "<p>Ligne 1<br>\nLigne 2</p>",
            "<h2>Service</h2>",
            "<p><em>Compléments</em></p>",
        ):
            assert expected in content, expected

    def test_shows_contacts_with_their_role_raw_text_and_emails(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            contacts=[
                {
                    "role": "principal",
                    "texte": "Camille Martin <RH> : a@exemple.gouv.fr ; 01 23 45",
                    "emails": ["a@exemple.gouv.fr"],
                },
                {
                    "role": "autre",
                    "texte": "Bureau RH",
                    "emails": ["b@exemple.gouv.fr"],
                },
            ],
        )

        content = client.get(self.url(source, offer)).content.decode()

        assert (
            "Personne à contacter : Camille Martin &lt;RH&gt; : a@exemple.gouv.fr"
            " ; 01 23 45<br>"
            "E-mails : a@exemple.gouv.fr<br>"
            "Autre personne à contacter : Bureau RH<br>"
            "E-mails : b@exemple.gouv.fr"
        ) in content
        assert "mailto:" not in content
        assert "&quot;texte&quot;" not in content  # plus de JSON brut

    def test_shows_criteria_in_readable_rows(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            criteria={
                "diplome_niveau": 5,
                "experience": "CONFIRME",
                "specialisations": ["informatique", "droit"],
                "langues": [{"iso_code": "en", "niveau": "B2"}],
            },
        )

        content = client.get(self.url(source, offer)).content.decode()

        for expected in (
            "Critères — Niveau de diplôme",
            "Niveau 5",
            "Confirmé",
            "informatique, droit",
            "(B2)",
            "Critères — Documents requis",  # clé absente : ligne « Non renseigné »
        ):
            assert expected in content, expected
        assert "CONFIRME" not in content
        assert "&quot;langues&quot;" not in content  # plus de JSON brut

    def test_shows_required_skills_with_line_breaks(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            criteria={"competences_requises": "- Rigueur\n- Autonomie"},
        )

        content = client.get(self.url(source, offer)).content.decode()

        assert "- Rigueur<br>- Autonomie" in content

    def test_shows_required_documents_labels(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            criteria={"documents_requis": ["CV", "LETTRE_MOTIVATION"]},
        )

        content = client.get(self.url(source, offer)).content.decode()

        assert "CV, Lettre de motivation" in content
        assert "LETTRE_MOTIVATION" not in content

    def test_shows_conditions_in_readable_rows(self, client, source):
        offer = OfferDjangoFactory(
            source=source,
            conditions={
                "salaire_titulaire": "35000",
                "debut_contrat": "2024-06-01T00:00:00Z",
                "temps_travail": "TEMPS_PLEIN",
                "lieu_de_travail": "TELETRAVAIL",
                "note_ouverture_poste_url": "https://exemple.gouv.fr/note",
            },
        )

        content = client.get(self.url(source, offer)).content.decode()

        for expected in (
            "Conditions — Salaire (titulaire)",
            "35000",
            "01/06/2024",
            "Temps plein",
            "Télétravail",
            'href="https://exemple.gouv.fr/note"',
            "Conditions — Durée du contrat",  # clé absente : ligne « Non renseigné »
        ):
            assert expected in content, expected
        assert "TEMPS_PLEIN" not in content

    def test_shows_criteria_and_conditions_rows_when_columns_are_empty(
        self, client, source
    ):
        offer = OfferDjangoFactory(source=source, criteria=None, conditions=None)

        content = client.get(self.url(source, offer)).content.decode()

        assert "Critères — Diplôme" in content
        assert "Conditions — Management" in content

    def test_shows_empty_fields_as_not_provided(self, client, source):
        offer = OfferDjangoFactory(source=source, long_title=None, employer=None)

        response = client.get(self.url(source, offer))

        content = response.content.decode()
        assert "Titre long" in content
        assert "Employeur" in content
        assert "Non renseigné" in content

    def test_escapes_html(self, client, source):
        offer = OfferDjangoFactory(
            source=source, title="<script>alert(1)</script>", organization="Org & Co"
        )

        content = client.get(self.url(source, offer)).content.decode()

        assert "<script>alert(1)</script>" not in content
        assert "Org &amp; Co" in content

    def test_unknown_source_gets_not_found_and_is_logged(
        self, client, db, ingestion_logs
    ):
        source_id = uuid4()
        offer = OfferDjangoFactory()

        response = client.get(reverse("fret:offre", args=[source_id, offer.id]))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(source_id) in ingestion_logs.text

    def test_offer_of_another_source_gets_not_found_and_is_logged(
        self, client, source, ingestion_logs
    ):
        offer = OfferDjangoFactory(source=SourceDjangoFactory())

        response = client.get(self.url(source, offer))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(offer.id) in ingestion_logs.text
