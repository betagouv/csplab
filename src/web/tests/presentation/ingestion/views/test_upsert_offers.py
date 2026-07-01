from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from tests.factories.ingestion.offer_payload_factory import (
    PayloadOfferFactory,
    fake_datetime,
)
from tests.factories.ingestion.source_factory import SourceFactory

fake = Faker("fr_FR")

SOURCE_UUID = fake.uuid4()
URL = reverse("ingestion:offers_upsert")


MINIMAL_VALID_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-001", "versant": "FPT"}
)

PARTIAL_VALID_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-002", "versant": "FPE"},
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

COMPLETE_VALID_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-003", "versant": "FPH"},
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

INVALID_PAYLOAD_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-004", "versant": "FPT"},
    titre=None,  # missing required field
)

INVALID_DATA_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-005", "versant": "FPT"},
    type_contrat="ABC",  # invalid enum value
)


def parse_offer_from_payload(payload: dict, source_id: UUID) -> Offer:
    reference = payload["identification"]["reference"]
    versant = payload["identification"]["versant"]

    def parse_datetime(raw: str) -> datetime:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))

    conditions = payload.get("conditions") or None
    debut_contrat_raw = conditions.get("debut_contrat") if conditions else None
    debut_contrat = (
        LimitDate(parse_datetime(debut_contrat_raw)) if debut_contrat_raw else None
    )

    # mirrors how ConditionsInputSerializer parses datetime fields into validated_data
    if conditions:
        conditions = {
            key: parse_datetime(value)
            if key in ("debut_contrat", "fin_contrat") and value
            else value
            for key, value in conditions.items()
        }

    categories = payload.get("categories")
    category = Category(sorted(categories)[0]) if categories else None

    loc_data = payload.get("localisation")
    localisation = (
        Localisation(
            area=GeographicalArea(loc_data[0]["zone_geographique"]),
            country=Country(loc_data[0]["pays"]),
            region=Region(code=loc_data[0]["region"]),
            department=Department(code=loc_data[0]["departement"]),
            label=loc_data[0].get("localisation_label") or None,
            latitude=loc_data[0].get("latitude"),
            longitude=loc_data[0].get("longitude"),
        )
        if loc_data
        else None
    )

    forme_contrat = payload.get("forme_contrat")

    return Offer(
        external_id=f"{versant}-{reference}",
        reference=reference,
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
        source_id=source_id,
        long_title=payload.get("titre_long") or None,
        application_url=payload.get("url_candidature"),
        contract_kind=sorted(forme_contrat) if forme_contrat else None,
        job_vacancy=payload.get("vacance_poste") or None,
        employer=payload["description"].get("employeur") or None,
        complements=payload["description"].get("complements") or None,
        criteria=payload.get("criteres") or None,
        conditions=conditions,
        contacts=list(payload["contacts"]) if payload.get("contacts") else None,
    )


@pytest.fixture
def use_case():
    mock = MagicMock()
    mock.execute.return_value = {"created": 0, "updated": 0, "errors": []}
    return mock


@pytest.fixture(autouse=True)
def mock_container(mock_offers_container, use_case):
    mock_offers_container.upsert_offers_usecase.return_value = use_case


@pytest.fixture
def source():
    return SourceFactory.create_model(source_id=UUID(SOURCE_UUID))


@pytest.fixture
def authenticated_client_with_source(api_client, test_user, source):
    test_user.sources.add(source)
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


def test_unauthenticated_access(api_client):
    response = api_client.post(URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_key_authentication(api_key_client, use_case):
    use_case.execute.return_value = {"created": 1, "updated": 0, "errors": []}
    response = api_key_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED


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
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER] * num_offers},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"offres": [expected_msg]}


def test_jwt_forbidden_source_id_returns_403(authenticated_client, use_case):
    use_case.execute.side_effect = SourceAuthorizationError({UUID(SOURCE_UUID)})
    response = authenticated_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_valid_payload_returns_201_and_valid_offers_to_usecase(
    authenticated_client_with_source, use_case
):
    offers_payload = [MINIMAL_VALID_OFFER, PARTIAL_VALID_OFFER, COMPLETE_VALID_OFFER]

    use_case.execute.return_value = {
        "created": len(offers_payload),
        "updated": 0,
        "errors": [],
    }
    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": offers_payload},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    upsert_input = use_case.execute.call_args[0][0]
    for payload, offer in zip(offers_payload, upsert_input.offers, strict=True):
        expected = parse_offer_from_payload(payload, source_id=UUID(SOURCE_UUID))
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
            "source_id",
            "long_title",
            "application_url",
            "contract_kind",
            "job_vacancy",
            "employer",
            "complements",
            "criteria",
            "conditions",
            "contacts",
        ]:
            assert getattr(offer, attr) == getattr(expected, attr)


def test_mixed_valid_invalid_offers_in_payload(
    authenticated_client_with_source, use_case
):
    offers_payload = [MINIMAL_VALID_OFFER, INVALID_PAYLOAD_OFFER, INVALID_DATA_OFFER]

    use_case.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": ["db error on offer xxx"],
    }
    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": offers_payload},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    errors = response.json()["errors"]
    assert errors == [
        "db error on offer xxx",
        {
            "offer": {"reference": "REF-004", "versant": "FPT"},
            "error": {"titre": ["Ce champ ne peut être nul."]},
        },
        {
            "offer": {"reference": "REF-005", "versant": "FPT"},
            "error": {"type_contrat": ["«\xa0ABC\xa0» n'est pas un choix valide."]},
        },
    ]


def test_returns_error_500(authenticated_client_with_source, use_case):
    use_case.execute.side_effect = Exception("db error")

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
