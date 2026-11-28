from datetime import UTC, datetime
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.core.cache import cache
from django.urls import reverse
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.domaine_fonctionnel import DomaineFonctionnel
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import status

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.authentication.rejection import AuthRejectionRateThrottle
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

URL = reverse("ingestion:offers_list")

NOMBRE_REQUETES_ATTENDU = (
    1  # view JWT authentication
    + 1  # JWT account's allowed networks
    + 2  # pagination: count + page
    + 1  # prefetch of the offers' localisations
    + 1  # ApiRequestLoggerMiddleware re-decodes the JWT to log the request
    + 2  # logging: DJ tries an UPDATE (manually-assigned pk) then falls back to INSERT
)


def test_unauthenticated_access(api_client):
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Clear-Site-Data" not in response


def test_authenticated_access(jwt_client):
    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_logged_user_access_without_token_is_rejected(api_client, test_user):
    api_client.force_login(test_user)
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_api_key_returns_401(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Api-Key wrong-key")
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@patch.object(
    AuthRejectionRateThrottle, "THROTTLE_RATES", {"auth_rejection": "1/minute"}
)
def test_repeated_invalid_api_key_is_throttled(api_client, db):
    cache.clear()
    api_client.credentials(
        HTTP_AUTHORIZATION="Api-Key wrong-key", HTTP_X_REAL_IP="10.0.0.1"
    )
    assert api_client.get(URL).status_code == status.HTTP_401_UNAUTHORIZED

    response = api_client.get(URL)

    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert AuditLoginLogModel.objects.count() == 1


def test_api_key_authentication_access(list_offers_mock, api_key_client):
    response = api_key_client.get(URL)
    assert response.status_code == status.HTTP_200_OK


def test_post_not_allowed(jwt_client):
    response = jwt_client.post(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.fixture
def list_offers_mock():
    with patch(
        "presentation.ingestion.views.offers.list_offers",
        return_value=OfferModel.objects.none(),
    ) as mock:
        yield mock


def test_empty_result(jwt_client):
    response = jwt_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_archived_offers(jwt_client):
    offer = OfferDjangoFactory(archived_at=datetime(2024, 3, 1, 12, 30, tzinfo=UTC))
    OfferDjangoFactory()

    response = jwt_client.get(URL, {"actif": False})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert [result["reference"] for result in data["results"]] == [offer.reference]
    assert data["results"][0]["date_archivage"] == "2024-03-01T12:30:00Z"


@pytest.mark.parametrize("active", [True, False])
def test_call_with_args(list_offers_mock, jwt_client, active):
    jwt_client.get(URL, {"actif": active})

    list_offers_mock.assert_called_once_with(GetFilteredOffersInput(active=active))


def test_external_id_contains_is_not_accepted(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"external_id_contains": "123"})

    list_offers_mock.assert_called_once_with(GetFilteredOffersInput(active=True))


def test_category_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"categorie": "A,B"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            category=[Category.A, Category.B],
        )
    )


def test_invalid_category_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"categorie": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "A, APLUS, B, C" in response.json()["error"]


def test_verse_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"versant": "FPE,FPT"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            verse=[Verse.FPE, Verse.FPT],
        )
    )


def test_invalid_verse_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"versant": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "FPE, FPH, FPT" in response.json()["error"]


def test_offer_nature_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"nature_offre": "CONTRACTUEL,TERRITORIAL"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            offer_nature=[OfferNature.CONTRACTUEL, OfferNature.TERRITORIAL],
        )
    )


def test_invalid_offer_nature_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"nature_offre": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONTRACTUEL, TERRITORIAL, TITULAIRE_CONTRACTUEL" in response.json()["error"]


def test_experience_level_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"niveau_experience": "DEBUTANT,EXPERT"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
        )
    )


def test_invalid_experience_level_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"niveau_experience": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "CONFIRME, DEBUTANT, EXPERT" in response.json()["error"]


def test_management_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"management": "SANS,AVEC"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            management=[Management.SANS, Management.AVEC],
        )
    )


def test_invalid_management_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"management": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "AVEC, SANS" in response.json()["error"]


def test_working_place_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"lieu_de_travail": "SUR_SITE,TELETRAVAIL"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            working_place=[WorkingPlace.SUR_SITE, WorkingPlace.TELETRAVAIL],
        )
    )


def test_invalid_working_place_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"lieu_de_travail": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]
    assert "NON_DEFINI, SUR_SITE, TELETRAVAIL" in response.json()["error"]


def test_region_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"region": "11,84"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            region=[Region(code="11"), Region(code="84")],
        )
    )


def test_invalid_region_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"region": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_departement_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"departement": "75,69"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            department=[Department(code="75"), Department(code="69")],
        )
    )


def test_invalid_departement_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"departement": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_pays_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"pays": "fra,bel"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            country=[Country("FRA"), Country("BEL")],
        )
    )


def test_invalid_pays_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"pays": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_zone_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"zone": "EUROPE,AFRIQUE"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            area=[GeographicalArea.EUROPE, GeographicalArea.AFRIQUE],
        )
    )


def test_invalid_zone_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"zone": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_domaine_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"domaine": "NUM,ACH"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            domain=[DomaineFonctionnel.NUMERIQUE.value, DomaineFonctionnel.ACHAT.value],
        )
    )


def test_invalid_domaine_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"domaine": "INVALID"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "INVALID" in response.json()["error"]


def test_organisation_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, [("organisation", "ORG1")])

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            organization=["ORG1"],
        )
    )


def test_organisation_filter_with_multiple_values_is_forwarded_to_usecase(
    list_offers_mock, jwt_client
):
    jwt_client.get(
        URL,
        [
            ("organisation", "ORG1"),
            ("organisation", "ORG2"),
        ],
    )

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            organization=["ORG1", "ORG2"],
        )
    )


def test_keywords_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"mots_cles": "développeur informatique"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            keywords="développeur informatique",
        )
    )


def test_blank_keywords_is_treated_as_not_provided(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"mots_cles": ""})

    assert response.status_code == status.HTTP_200_OK
    list_offers_mock.assert_called_once_with(GetFilteredOffersInput(active=True))


def test_debut_publication_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"debut_publication": "-7"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            published_within_days=-7,
        )
    )


def test_positive_debut_publication_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(URL, {"debut_publication": "7"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_geo_filter_is_forwarded_to_usecase(list_offers_mock, jwt_client):
    jwt_client.get(URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10"})

    list_offers_mock.assert_called_once_with(
        GetFilteredOffersInput(
            active=True,
            latitude=48.8566,
            longitude=2.3522,
            radius_km=10,
        )
    )


@pytest.mark.parametrize(
    "params",
    [
        {"latitude": "48.8566"},
        {"longitude": "2.3522"},
        {"radius": "10"},
        {"latitude": "48.8566", "longitude": "2.3522"},
        {"latitude": "48.8566", "radius": "10"},
        {"longitude": "2.3522", "radius": "10"},
    ],
)
def test_partial_geo_filter_returns_400(list_offers_mock, jwt_client, params):
    response = jwt_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_radius_below_one_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "0"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_non_integer_radius_returns_400(list_offers_mock, jwt_client):
    response = jwt_client.get(
        URL, {"latitude": "48.8566", "longitude": "2.3522", "radius": "10.5"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "params",
    [
        {"latitude": "-91", "longitude": "2.3522", "radius": "10"},
        {"latitude": "48.8566", "longitude": "181", "radius": "10"},
    ],
)
def test_out_of_range_lat_lon_returns_400(list_offers_mock, jwt_client, params):
    response = jwt_client.get(URL, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_returns_error_500(list_offers_mock, jwt_client):
    list_offers_mock.side_effect = Exception("db error")

    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_pagination_page_arg(jwt_client):
    offers = OfferDjangoFactory.create_batch(5)

    response = jwt_client.get(URL, {"page": 2, "taille": 2, "dummy": "arg", "actif": 1})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["count"] == len(offers)
    assert len(data["results"]) == 2  # noqa

    parsed_previous = urlparse(data["previous"])
    assert parsed_previous.path == URL
    assert parse_qs(parsed_previous.query) == {
        "dummy": ["arg"],
        "actif": ["1"],
        "taille": ["2"],
    }

    parsed_next = urlparse(data["next"])
    assert parsed_next.path == URL
    assert parse_qs(parsed_next.query) == {
        "page": ["3"],
        "dummy": ["arg"],
        "actif": ["1"],
        "taille": ["2"],
    }


def test_pagination_out_of_bounds_returns_404(jwt_client):
    OfferDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"page": 3, "taille": 2})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.parametrize("page", ["0", "-1", "abc"])
def test_pagination_invalid_page_returns_404(list_offers_mock, jwt_client, page):
    response = jwt_client.get(URL, {"page": page})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("taille", ["0", "-5", "abc"])
def test_pagination_invalid_taille_falls_back_to_default(jwt_client, taille):
    OfferDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"taille": taille})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa


def test_pagination_taille_is_capped(jwt_client):
    OfferDjangoFactory.create_batch(3)

    response = jwt_client.get(URL, {"taille": 1_000_000, "page": 1})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 3  # noqa


class TestOffersListViewDbVerified:
    def test_response_matches_db_record_field_by_field(self, jwt_client):
        offer = OfferDjangoFactory(
            offer_nature=OfferNature.TERRITORIAL.value,
            offer_url="https://example.org/offre",
        )

        response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"] == [
            {
                "reference": offer.reference,
                "source_id": str(offer.source_id),
                "titre": offer.title,
                "organisation": offer.organization,
                "organisation_siret": None,
                "versant": offer.verse,
                "categories": offer.categories,
                "nature_offre": offer.offer_nature,
                "type_contrat": None,
                "vacance_poste": None,
                "profession": {
                    "referentiel": None,
                    "domaine": None,
                    "metier": None,
                    "metier_libelle": None,
                },
                "url_offre": offer.offer_url,
                "localisation": [
                    {
                        "zone_geographique": "EU",
                        "pays": "FRA",
                        "region": "11",
                        "departement": "75",
                        "localisation_label": None,
                        "latitude": None,
                        "longitude": None,
                    }
                ],
                "debut_publication": "2024-01-15T00:00:00Z",
                "fin_publication": "2025-01-15T00:00:00Z",
                "debut_contrat": "2024-12-31T00:00:00Z",
                "fin_candidature": None,
                "debut_vacance_poste": None,
                "date_archivage": None,
                "conditions": None,
            }
        ]

    def test_organisation_filter_includes_child_organizations(self, jwt_client):
        parent = TalentsoftOrganismeDjangoFactory(has_children=True)
        child_b = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        child_c = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        OfferDjangoFactory(reference="REF-A", talentsoft_organisme_entity_code=parent)
        OfferDjangoFactory(reference="REF-B", talentsoft_organisme_entity_code=child_b)
        OfferDjangoFactory(reference="REF-C", talentsoft_organisme_entity_code=child_c)
        OfferDjangoFactory(
            reference="REF-AUTRE",
            talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory(),
        )

        response = jwt_client.get(URL, {"organisation": parent.entity_code})

        assert response.status_code == status.HTTP_200_OK
        references = {offer["reference"] for offer in response.json()["results"]}
        assert references == {"REF-A", "REF-B", "REF-C"}

    def test_does_not_trigger_n_plus_one_queries(
        self, jwt_client, django_assert_num_queries
    ):
        OfferDjangoFactory.create_batch(5)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = jwt_client.get(URL)

        assert response.status_code == status.HTTP_200_OK


class TestOffersListViewFieldsMask:
    def test_returns_the_requested_fields(self, jwt_client):
        offer = OfferDjangoFactory(
            criteria={"experience": "CONFIRME", "diplome": "Master"}
        )

        response = jwt_client.get(
            URL,
            headers={
                "X-Fields": "reference, localisation{departement}, criteres{experience}"
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"] == [
            {
                "reference": offer.reference,
                "localisation": [{"departement": "75"}],
                "criteres": {"experience": "CONFIRME"},
            }
        ]

    def test_star_returns_every_exposed_field(self, jwt_client):
        OfferDjangoFactory(contacts=[{"role": "principal", "texte": "", "emails": []}])

        response = jwt_client.get(URL, headers={"X-Fields": "*"})

        assert response.status_code == status.HTTP_200_OK
        (result,) = response.json()["results"]
        assert {"mission", "criteres", "date_creation", "date_mise_a_jour"} <= set(
            result
        )
        assert "contacts" not in result
        assert "email_candidature" not in result

    @pytest.mark.parametrize(
        ("fields", "refused"),
        [
            ("reference,inconnu", "inconnu"),
            ("contacts", "contacts"),
            ("email_candidature", "email_candidature"),
            ("localisation{ville}", "localisation.ville"),
            ("titre{x}", "titre.x"),
        ],
    )
    def test_refuses_an_unknown_or_excluded_field(self, jwt_client, fields, refused):
        response = jwt_client.get(URL, headers={"X-Fields": fields})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert refused in response.json()["error"]

    @pytest.mark.parametrize("fields", ["", "reference,", "localisation{pays", "a}b"])
    def test_refuses_an_invalid_syntax(self, jwt_client, fields):
        response = jwt_client.get(URL, headers={"X-Fields": fields})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_does_not_load_the_fields_left_out(
        self, jwt_client, django_assert_num_queries
    ):
        OfferDjangoFactory.create_batch(3)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU - 1) as queries:
            response = jwt_client.get(URL, headers={"X-Fields": "reference,titre"})

        assert response.status_code == status.HTTP_200_OK
        page_query = next(
            query["sql"]
            for query in queries.captured_queries
            if 'FROM "offers"' in query["sql"] and "LIMIT" in query["sql"]
        )
        assert '"offers"."title"' in page_query
        assert '"offers"."mission"' not in page_query
        assert '"offers"."contacts"' not in page_query


def test_returns_the_salaries_by_default(jwt_client):
    OfferDjangoFactory(
        conditions={"salaire_titulaire": "Grille", "temps_travail": "TEMPS_PLEIN"}
    )

    response = jwt_client.get(URL)

    assert response.json()["results"][0]["conditions"] == {
        "salaire_titulaire": "Grille"
    }
