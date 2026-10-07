import logging
from datetime import UTC, datetime
from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from referentiel.value_objects.contract_kind import ContractKind

from config.logger_names import LoggerName
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
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


@pytest.fixture
def agent_user(db, source):
    return AgentDjangoFactory(utilisateur__sources=[source]).utilisateur


class TestSourceListView:
    url = reverse("fret:sources")

    def test_anonymous_is_redirected_to_login(self, client):
        response = client.get(self.url)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("identite:login"))

    @pytest.mark.parametrize(
        "make_user",
        [
            lambda source: UtilisateurDjangoFactory(),
            lambda source: UtilisateurDjangoFactory(is_staff=True),
            lambda source: UtilisateurDjangoFactory(is_staff=True, sources=[source]),
        ],
        ids=[
            "user_without_agent_profile",
            "staff_without_agent_profile",
            "staff_with_source_without_agent_profile",
        ],
    )
    def test_user_without_access_is_forbidden(self, client, source, make_user):
        client.force_login(make_user(source))

        assert client.get(self.url).status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.parametrize(
        "make_user",
        [
            lambda source: UtilisateurDjangoFactory(sources=[source]),
            lambda source: (
                AgentDjangoFactory(utilisateur__sources=[source]).utilisateur
            ),
        ],
        ids=["user_without_agent_profile", "agent"],
    )
    def test_sees_only_own_sources(self, client, source, make_user):
        other = SourceDjangoFactory()
        client.force_login(make_user(source))

        response = client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/sources.html")
        assert list(response.context["sources"]) == [source]
        assert other.slug not in response.content.decode()

    def test_agent_with_several_sources_sees_all_of_them(
        self, client, agent_user, source
    ):
        second = SourceDjangoFactory()
        agent_user.sources.add(second)
        client.force_login(agent_user)

        response = client.get(self.url)

        assert set(response.context["sources"]) == {source, second}

    def test_agent_without_source_sees_empty_list(self, client, db):
        client.force_login(AgentDjangoFactory().utilisateur)

        response = client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assert list(response.context["sources"]) == []

    @pytest.mark.parametrize(
        "make_user",
        [
            lambda: AgentDjangoFactory(utilisateur__is_staff=True).utilisateur,
            lambda: UtilisateurDjangoFactory(is_superuser=True),
        ],
        ids=["staff_agent", "superuser_without_agent_profile"],
    )
    def test_staff_and_superuser_see_all_sources(self, client, source, make_user):
        other = SourceDjangoFactory()
        client.force_login(make_user())

        response = client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assert set(response.context["sources"]) == {source, other}

    def test_sources_are_paginated(self, client, db):
        sources = SourceDjangoFactory.create_batch(PAGINATE_BY + 1)
        client.force_login(AgentDjangoFactory(utilisateur__sources=sources).utilisateur)

        first = client.get(self.url)
        second = client.get(self.url, {"page": 2})

        assert len(first.context["sources"]) == PAGINATE_BY
        assert len(second.context["sources"]) == 1

    def test_each_source_links_to_its_offers(self, client, agent_user, source):
        client.force_login(agent_user)

        response = client.get(self.url)

        assert reverse("fret:offres", args=[source.source_id]) in (
            response.content.decode()
        )


class TestOffreListView:
    @staticmethod
    def url(source):
        return reverse("fret:offres", args=[source.source_id])

    def test_anonymous_is_redirected_to_login(self, client, source):
        response = client.get(self.url(source))

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("identite:login"))

    def test_staff_without_agent_profile_is_forbidden(self, client, source):
        client.force_login(UtilisateurDjangoFactory(is_staff=True))

        assert client.get(self.url(source)).status_code == HTTPStatus.FORBIDDEN

    def test_user_linked_to_source_without_agent_profile_sees_its_active_offers(
        self, client, source
    ):
        offer = OfferDjangoFactory(source=source)
        OfferDjangoFactory(source=source, archived_at=datetime(2024, 2, 1, tzinfo=UTC))
        OfferDjangoFactory()
        client.force_login(UtilisateurDjangoFactory(sources=[source]))

        response = client.get(self.url(source))

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/offres.html")
        assert [o.id for o in response.context["page_obj"]] == [offer.id]

    def test_offers_are_listed_most_recently_updated_first(
        self, client, agent_user, source
    ):
        old = OfferDjangoFactory(
            source=source, updated_at=datetime(2024, 1, 1, tzinfo=UTC)
        )
        recent = OfferDjangoFactory(
            source=source, updated_at=datetime(2024, 3, 1, tzinfo=UTC)
        )
        client.force_login(agent_user)

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
        self, client, agent_user, source, term, expected
    ):
        OfferDjangoFactory(source=source, reference="ABC-123", title="Développeur")
        OfferDjangoFactory(source=source, reference="XYZ-999", title="Juriste")
        client.force_login(agent_user)

        response = client.get(self.url(source), {"q": term})

        assert response.status_code == HTTPStatus.OK
        assert sorted(o.reference for o in response.context["page_obj"]) == expected

    def test_search_does_not_reach_the_offers_of_other_sources(
        self, client, agent_user, source
    ):
        OfferDjangoFactory(source=source, reference="ABC-123")
        OfferDjangoFactory(reference="ABC-456")
        client.force_login(agent_user)

        response = client.get(self.url(source), {"q": "ABC"})

        assert [o.reference for o in response.context["page_obj"]] == ["ABC-123"]

    def test_search_form_keeps_the_term_and_escapes_it(
        self, client, agent_user, source
    ):
        client.force_login(agent_user)

        content = client.get(self.url(source), {"q": '"><script>'}).content.decode()

        assert "<script>" not in content
        assert "Aucune offre ne correspond à votre recherche." in content

    def test_agent_with_several_sources_accesses_each_of_them(
        self, client, agent_user, source
    ):
        second = SourceDjangoFactory()
        agent_user.sources.add(second)
        client.force_login(agent_user)

        assert client.get(self.url(source)).status_code == HTTPStatus.OK
        assert client.get(self.url(second)).status_code == HTTPStatus.OK

    @pytest.mark.parametrize(
        "make_user",
        [
            lambda: AgentDjangoFactory(utilisateur__is_staff=True).utilisateur,
            lambda: UtilisateurDjangoFactory(is_superuser=True),
        ],
        ids=["staff_agent", "superuser_without_agent_profile"],
    )
    def test_staff_and_superuser_see_the_offers_of_any_source(
        self, client, db, make_user
    ):
        other = SourceDjangoFactory()
        offer = OfferDjangoFactory(source=other)
        client.force_login(make_user())

        response = client.get(self.url(other))

        assert response.status_code == HTTPStatus.OK
        assert [o.id for o in response.context["page_obj"]] == [offer.id]

    def test_source_not_linked_to_the_user_gets_not_found_and_is_logged(
        self, client, agent_user, ingestion_logs
    ):
        other = SourceDjangoFactory()
        OfferDjangoFactory(source=other)
        client.force_login(agent_user)

        response = client.get(self.url(other))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(other.source_id) in ingestion_logs.text
        assert str(agent_user.username) in ingestion_logs.text

    def test_unknown_source_gets_not_found(self, client, db):
        client.force_login(UtilisateurDjangoFactory(is_superuser=True))

        response = client.get(reverse("fret:offres", args=[uuid4()]))

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_source_without_offer_shows_empty_message(self, client, agent_user, source):
        client.force_login(agent_user)

        response = client.get(self.url(source))

        assert response.status_code == HTTPStatus.OK
        assert "Aucune offre pour cette source." in response.content.decode()

    def test_offers_are_paginated(self, client, agent_user, source):
        OfferDjangoFactory.create_batch(PAGINATE_BY + 1, source=source)
        client.force_login(agent_user)

        first = client.get(self.url(source))
        second = client.get(self.url(source), {"page": 2})

        assert len(first.context["page_obj"]) == PAGINATE_BY
        assert len(second.context["page_obj"]) == 1

    def test_each_offer_links_to_its_detail(self, client, agent_user, source):
        offer = OfferDjangoFactory(source=source)
        client.force_login(agent_user)

        content = client.get(self.url(source)).content.decode()

        assert reverse("fret:offre", args=[source.source_id, offer.id]) in content


class TestOffreDetailView:
    @staticmethod
    def url(source, offer):
        return reverse("fret:offre", args=[source.source_id, offer.id])

    def test_anonymous_is_redirected_to_login(self, client, source):
        offer = OfferDjangoFactory(source=source)

        response = client.get(self.url(source, offer))

        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(reverse("identite:login"))

    def test_staff_without_agent_profile_is_forbidden(self, client, source):
        offer = OfferDjangoFactory(source=source)
        client.force_login(UtilisateurDjangoFactory(is_staff=True))

        assert client.get(self.url(source, offer)).status_code == HTTPStatus.FORBIDDEN

    def test_user_linked_to_source_without_agent_profile_sees_the_offer(
        self, client, source
    ):
        offer = OfferDjangoFactory(source=source)
        client.force_login(UtilisateurDjangoFactory(sources=[source]))

        response = client.get(self.url(source, offer))

        assert response.status_code == HTTPStatus.OK
        assertTemplateUsed(response, "fret/offre_detail.html")
        assert response.context["offre"] == offer

    @pytest.mark.parametrize(
        "make_user",
        [
            lambda: AgentDjangoFactory(utilisateur__is_staff=True).utilisateur,
            lambda: UtilisateurDjangoFactory(is_superuser=True),
        ],
        ids=["staff_agent", "superuser_without_agent_profile"],
    )
    def test_staff_and_superuser_see_the_offer_of_any_source(
        self, client, db, make_user
    ):
        other = SourceDjangoFactory()
        offer = OfferDjangoFactory(source=other)
        client.force_login(make_user())

        assert client.get(self.url(other, offer)).status_code == HTTPStatus.OK

    def test_shows_all_known_data_of_the_offer(self, client, agent_user, source):
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
            contacts=[{"email": "jean.dupont@exemple.gouv.fr"}],
            location_label="Paris",
            application_deadline=datetime(2024, 5, 15, tzinfo=UTC),
        )
        client.force_login(agent_user)

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
            'href="mailto:jean.dupont@exemple.gouv.fr"',
            "Paris",
            "15/05/2024",
            f"Mairie de Test ({organisme.entity_code})",
            offer.mission,
            offer.profile,
        ):
            assert expected in content, expected

    def test_shows_contacts_as_mailto_links(self, client, agent_user, source):
        offer = OfferDjangoFactory(
            source=source,
            contacts=[{"email": "a@exemple.gouv.fr"}, {"email": "b@exemple.gouv.fr"}],
        )
        client.force_login(agent_user)

        content = client.get(self.url(source, offer)).content.decode()

        assert '<a href="mailto:a@exemple.gouv.fr">a@exemple.gouv.fr</a>, ' in content
        assert '<a href="mailto:b@exemple.gouv.fr">b@exemple.gouv.fr</a>' in content
        assert "&quot;email&quot;" not in content  # plus de JSON brut

    def test_shows_criteria_in_readable_rows(self, client, agent_user, source):
        offer = OfferDjangoFactory(
            source=source,
            criteria={
                "diplome_niveau": 5,
                "experience": "CONFIRME",
                "specialisations": ["informatique", "droit"],
                "langues": [{"iso_code": "en", "niveau": "B2"}],
            },
        )
        client.force_login(agent_user)

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

    def test_shows_conditions_in_readable_rows(self, client, agent_user, source):
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
        client.force_login(agent_user)

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
        self, client, agent_user, source
    ):
        offer = OfferDjangoFactory(source=source, criteria=None, conditions=None)
        client.force_login(agent_user)

        content = client.get(self.url(source, offer)).content.decode()

        assert "Critères — Diplôme" in content
        assert "Conditions — Management" in content

    def test_shows_empty_fields_as_not_provided(self, client, agent_user, source):
        offer = OfferDjangoFactory(source=source, long_title=None, employer=None)
        client.force_login(agent_user)

        response = client.get(self.url(source, offer))

        content = response.content.decode()
        assert "Titre long" in content
        assert "Employeur" in content
        assert "Non renseigné" in content

    def test_escapes_html(self, client, agent_user, source):
        offer = OfferDjangoFactory(
            source=source, title="<script>alert(1)</script>", organization="Org & Co"
        )
        client.force_login(agent_user)

        content = client.get(self.url(source, offer)).content.decode()

        assert "<script>alert(1)</script>" not in content
        assert "Org &amp; Co" in content

    def test_source_not_linked_to_the_user_gets_not_found_and_is_logged(
        self, client, agent_user, ingestion_logs
    ):
        other = SourceDjangoFactory()
        offer = OfferDjangoFactory(source=other)
        client.force_login(agent_user)

        response = client.get(self.url(other, offer))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(other.source_id) in ingestion_logs.text

    def test_offer_of_another_source_gets_not_found_and_is_logged(
        self, client, agent_user, source, ingestion_logs
    ):
        offer = OfferDjangoFactory(source=SourceDjangoFactory())
        client.force_login(agent_user)

        response = client.get(self.url(source, offer))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert str(offer.id) in ingestion_logs.text
