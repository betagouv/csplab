from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.entities.offer import Offer
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse

fake = Faker("fr_FR")
URL = reverse("ingestion:offers_upsert")


def fake_datetime(future=True):
    if future:
        fake_datetime = fake.future_datetime(tzinfo=timezone.utc)
    else:
        fake_datetime = fake.date_time(tzinfo=timezone.utc)

    return fake_datetime.isoformat().replace("+00:00", "Z")


def deep_merge(base: dict, overrides: dict) -> dict:
    result = base.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def make_offer(**overrides) -> dict:
    base: dict[str, Any] = {
        "identification": {},
        "titre": fake.text(max_nb_chars=150),
        "titre_long": fake.text(max_nb_chars=1500),
        "organisation": {"nom": fake.company(), "siret": ""},
        "url_offre": None,
        "url_candidature": None,
        "profession": {"domaine": "INF", "metier": "INF001"},
        "categories": [],
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "forme_contrat": [],
        "vacance_poste": "",
        "description": {
            "mission": fake.text(max_nb_chars=3000),
            "profil": fake.text(max_nb_chars=3000),
            "employeur": fake.text(max_nb_chars=1500),
            "complements": "",
        },
        "localisation": None,
        "criteres": None,
        "conditions": None,
        "contacts": None,
        "publication": {
            "debut_publication": fake_datetime(future=False),
            "fin_publication": fake_datetime(),
            "fin_candidature": None,
            "debut_vacance_poste": None,
        },
    }
    return deep_merge(base, overrides)


MINIMAL_VALID_OFFER = make_offer(
    identification={"reference": "REF-001", "source": "source-abc", "versant": "FPT"}
)

PARTIAL_VALID_OFFER = make_offer(
    identification={"reference": "REF-002", "source": "source-abc", "versant": "FPE"},
    localisation=[],
    criteres={"diplome_niveau": 3},
    conditions={
        "temps_travail": "TEMPS_PLEIN",
        "ouvert_aux_militaires": "OUI",
        "lieu_de_travail": "SUR_SITE",
        "management": "SANS",
    },
    contacts=[],
)

COMPLETE_VALID_OFFER = make_offer(
    identification={"reference": "REF-003", "source": "source-abc", "versant": "FPH"},
    organisation={"nom": fake.company(), "siret": fake.siret().replace(" ", "")},
    url_offre="https://example.com/offre",
    url_candidature="https://example.com/candidature",
    categories=["A", "B"],
    forme_contrat=["CDD"],
    vacance_poste="OUI",
    localisation=[
        {
            "zone_geographique": "EU",
            "pays": "FRA",
            "region": "03",
            "departement": "14",
            "localisation_label": fake.text(max_nb_chars=500),
            "latitude": fake.pyfloat(),
            "longitude": fake.pyfloat(),
        },
        {
            "zone_geographique": "AM",
            "pays": "MEX",
            "region": "",
            "departement": "",
            "localisation_label": "",
            "latitude": None,
            "longitude": None,
        },
    ],
    conditions={
        "debut_contrat": fake_datetime(future=True),
        "temps_travail": "TEMPS_PLEIN",
        "ouvert_aux_militaires": "OUI",
        "lieu_de_travail": "SUR_SITE",
        "management": "SANS",
    },
    contacts=[{"email": fake.email()}, {"email": fake.email()}],
)

INVALID_PAYLOAD_OFFER = make_offer(
    identification={"reference": "REF-004", "source": "source-abc", "versant": "FPT"},
    titre=None,  # missing required field
)

INVALID_DATA_OFFER = make_offer(
    identification={"reference": "REF-005", "source": "source-abc", "versant": "FPT"},
    type_contrat="ABC",  # invalid enum value
)


def parse_offer_from_payload(payload: dict) -> Offer:
    reference = payload["identification"]["reference"]
    versant = payload["identification"]["versant"]

    conditions = payload.get("conditions") or {}
    debut_contrat_raw = conditions.get("debut_contrat")
    debut_contrat = (
        LimitDate(datetime.fromisoformat(debut_contrat_raw.replace("Z", "+00:00")))
        if debut_contrat_raw
        else None
    )

    categories = payload.get("categories")
    category = Category(sorted(categories)[0]) if categories else None

    loc_data = payload.get("localisation")
    localisation = (
        Localisation(
            area=GeographicalArea(loc_data[0]["zone_geographique"]),
            country=Country(loc_data[0]["pays"]),
            region=Region(code=loc_data[0]["region"]),
            department=Department(code=loc_data[0]["departement"]),
        )
        if loc_data
        else None
    )

    return Offer(
        external_id=f"{versant}-{reference}",
        title=payload["titre"],
        profile=payload["description"]["profil"],
        mission=payload["description"]["mission"],
        organization=payload["organisation"]["nom"],
        publication_date=datetime.fromisoformat(
            payload["publication"]["debut_publication"]
        ),
        verse=Verse(versant),
        category=category,
        contract_type=ContractType(payload["type_contrat"]),
        offer_url=payload.get("url_offre"),
        localisation=localisation,
        beginning_date=debut_contrat,
        family_code=payload["profession"]["metier"],
    )


@pytest.fixture
def use_case():
    mock = MagicMock()
    mock.execute.return_value = {"created": 0, "updated": 0, "errors": []}
    return mock


@pytest.fixture(autouse=True)
def mock_container(use_case):
    container = MagicMock()
    container.upsert_offers_usecase.return_value = use_case
    with patch(
        "presentation.ingestion.views.create_ingestion_container",
        return_value=container,
    ):
        yield container


def test_unauthenticated_access(api_client):
    response = api_client.post(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_method_not_allowed(authenticated_client):
    response = authenticated_client.get(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "num_offers,expected_msg",
    [
        (101, "Ensure this field has no more than 100 elements."),
        (0, "Ensure this field has at least 1 elements."),
    ],
)
def test_invalid_payload_returns_error_400(
    authenticated_client, num_offers, expected_msg
):
    response = authenticated_client.post(
        URL,
        data=[MINIMAL_VALID_OFFER] * num_offers,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"offres": [expected_msg]}


def test_valid_payload_returns_201_and_valid_offers_to_usecase(
    authenticated_client, use_case
):
    offers_payload = [MINIMAL_VALID_OFFER, PARTIAL_VALID_OFFER, COMPLETE_VALID_OFFER]

    use_case.execute.return_value = {
        "created": len(offers_payload),
        "updated": 0,
        "errors": [],
    }
    response = authenticated_client.post(
        URL,
        data=offers_payload,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    upsert_input = use_case.execute.call_args[0][0]
    for payload, offer in zip(offers_payload, upsert_input.offers, strict=True):
        expected = parse_offer_from_payload(payload)
        for attr in [
            "external_id",
            "title",
            "profile",
            "mission",
            "organization",
            "publication_date",
            "verse",
            "category",
            "contract_type",
            "offer_url",
            "localisation",
            "beginning_date",
            "family_code",
        ]:
            assert getattr(offer, attr) == getattr(expected, attr)


def test_mixed_valid_invalid_offers_in_payload(authenticated_client, use_case):
    offers_payload = [MINIMAL_VALID_OFFER, INVALID_PAYLOAD_OFFER, INVALID_DATA_OFFER]

    use_case.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": ["db error on offer xxx"],
    }
    response = authenticated_client.post(
        URL,
        data=offers_payload,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    errors = response.json()["errors"]
    assert errors == [
        "db error on offer xxx",
        {
            "offer": {"reference": "REF-004", "source": "source-abc", "versant": "FPT"},
            "error": {"titre": ["Ce champ ne peut être nul."]},
        },
        {
            "offer": {"reference": "REF-005", "source": "source-abc", "versant": "FPT"},
            "error": {"type_contrat": ["«\xa0ABC\xa0» n'est pas un choix valide."]},
        },
    ]


def test_returns_error_500(authenticated_client, use_case):
    use_case.execute.side_effect = Exception("db error")

    response = authenticated_client.post(
        URL, data=[MINIMAL_VALID_OFFER], content_type="application/json"
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
