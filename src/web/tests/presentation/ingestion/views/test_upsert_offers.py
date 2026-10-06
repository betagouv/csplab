import re
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.offer_payload_factory import (
    PayloadOfferFactory,
    fake_datetime,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)
from infrastructure.mappers.offer_mapper import OfferMapper

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
    type_contrat="CDD_CDI",
    vacance_poste="OUI",
    description={
        "profil": "",
        "mission": "",
        "employeur": "",
        "conditions_exercice": fake.text(max_nb_chars=1500),
        "descriptif_service": fake.text(max_nb_chars=1500),
    },
    publication={"fin_candidature": fake_datetime(future=True)},
    localisation=[
        {
            "zone_geographique": "EU",
            "pays": "FRA",
            "region": "03",
            "departement": "14",
            "localisation_label": fake.text(max_nb_chars=500),
            "latitude": fake.pyfloat(min_value=-90, max_value=90),
            "longitude": fake.pyfloat(min_value=-180, max_value=180),
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
    nature_offre="ABC",  # invalid enum value
)


COMPARABLE_OFFER_ATTRS = [
    "reference",
    "title",
    "profile",
    "mission",
    "organization",
    "publication_date",
    "verse",
    "category",
    "offer_nature",
    "offer_url",
    "localisation",
    "beginning_date",
    "family_code",
    "job_family_referential",
    "functional_area_code",
    "source_id",
    "long_title",
    "application_url",
    "contract_kind",
    "job_vacancy",
    "employer",
    "complements",
    "exercise_conditions",
    "service_description",
    "application_deadline",
    "criteria",
    "conditions",
    "contacts",
]


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

    type_contrat = payload.get("type_contrat")

    criteres = payload.get("criteres")
    criteria = (
        OfferCriteria(
            diploma_level=Diploma(criteres["diplome_niveau"])
            if criteres.get("diplome_niveau") is not None
            else None,
            diploma=criteres.get("diplome") or None,
            experience_level=ExperienceLevel[criteres["experience"]]
            if criteres.get("experience")
            else None,
            specialisations=list(criteres.get("specialisations") or []),
            documents_requis=list(criteres.get("documents_requis") or []),
            competences_requises=list(criteres.get("competences_requises") or []),
            languages=[
                OfferLanguage(
                    iso_code=langue["iso_code"], level=LanguageLevel[langue["niveau"]]
                )
                for langue in criteres.get("langues") or []
            ],
        )
        if criteres
        else None
    )

    return Offer(
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
        offer_nature=OfferNature(payload["nature_offre"]),
        offer_url=payload.get("url_offre"),
        localisation=localisation,
        beginning_date=debut_contrat,
        family_code=payload["profession"]["metier"],
        job_family_referential=payload["profession"].get("referentiel"),
        functional_area_code=payload["profession"].get("domaine"),
        source_id=source_id,
        long_title=payload.get("titre_long") or None,
        application_url=payload.get("url_candidature"),
        contract_kind=ContractKind[type_contrat] if type_contrat else None,
        job_vacancy=payload.get("vacance_poste") or None,
        employer=payload["description"].get("employeur") or None,
        complements=payload["description"].get("complements") or None,
        exercise_conditions=payload["description"].get("conditions_exercice") or None,
        service_description=payload["description"].get("descriptif_service") or None,
        application_deadline=parse_datetime(fin_candidature)
        if (fin_candidature := payload["publication"].get("fin_candidature"))
        else None,
        criteria=criteria,
        conditions=conditions,
        contacts=list(payload["contacts"]) if payload.get("contacts") else None,
    )


@pytest.fixture
def use_case():
    mock = MagicMock()
    mock.execute.return_value = {"created": 0, "updated": 0, "errors": [], "offres": []}
    return mock


@pytest.fixture(autouse=True)
def mock_container(mock_offers_container, use_case):
    mock_offers_container.upsert_offers_usecase.return_value = use_case


@pytest.fixture
def source():
    return SourceDjangoFactory(source_id=UUID(SOURCE_UUID))


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
    use_case.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": [],
        "offres": [{"reference": "REF-001", "statut": "created"}],
    }
    response = api_key_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_get_method_not_allowed(jwt_client):
    response = jwt_client.get(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "num_offers,expected_msg",
    [
        (101, "Assurez-vous que ce champ n'a pas plus de 100 éléments."),
        (0, "Assurez-vous que ce champ a au moins 1 éléments."),
    ],
)
def test_invalid_payload_returns_error_400(jwt_client, num_offers, expected_msg):
    response = jwt_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER] * num_offers},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"offres": [expected_msg]}


def test_jwt_forbidden_source_id_returns_403(jwt_client, use_case):
    use_case.execute.side_effect = SourceAuthorizationError({UUID(SOURCE_UUID)})
    response = jwt_client.post(
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
        "offres": [
            {"reference": p["identification"]["reference"], "statut": "created"}
            for p in offers_payload
        ],
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
        for attr in COMPARABLE_OFFER_ATTRS:
            assert getattr(offer, attr) == getattr(expected, attr)


def test_mixed_valid_invalid_offers_in_payload(
    authenticated_client_with_source, use_case
):
    offers_payload = [MINIMAL_VALID_OFFER, INVALID_PAYLOAD_OFFER, INVALID_DATA_OFFER]

    use_case.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": ["db error on offer xxx"],
        "offres": [{"reference": "REF-001", "statut": "created"}],
    }
    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": offers_payload},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["offres"] == [
        {"index": 0, "reference": "REF-001", "statut": "created"}
    ]
    errors = response.json()["errors"]
    assert errors == [
        "db error on offer xxx",
        {
            "offer": {"reference": "REF-004", "versant": "FPT"},
            "error": {"titre": ["Ce champ ne peut être nul."]},
        },
        {
            "offer": {"reference": "REF-005", "versant": "FPT"},
            "error": {"nature_offre": ["«\xa0ABC\xa0» n'est pas un choix valide."]},
        },
    ]


def test_unknown_metier_returns_error_in_payload(
    authenticated_client_with_source, use_case, mock_offers_container
):
    mock_offers_container.metiers_repository.return_value.get_filtered.return_value = []

    use_case.execute.return_value = {
        "created": 0,
        "updated": 0,
        "errors": [],
        "offres": [],
    }
    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    errors = response.json()["errors"]
    assert errors == [
        {
            "offer": {"reference": "REF-001", "versant": "FPT"},
            "error": {
                "profession": {
                    "metier": ["Code métier inconnu : ERNUM001."],
                }
            },
        }
    ]


def test_returns_error_500(authenticated_client_with_source, use_case):
    use_case.execute.side_effect = Exception("db error")

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestOffersUpsertViewDbVerified:
    @pytest.fixture(autouse=True)
    def mock_container(self):
        return None

    def test_creates_and_persists_the_offer(self, authenticated_client_with_source):
        MetierDjangoFactory(offer_family_code="ERNUM001")

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "created": 1,
            "updated": 0,
            "errors": [],
            "offres": [{"index": 0, "reference": "REF-001", "statut": "created"}],
        }

        offer_model = OfferModel.objects.get(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        )
        persisted = OfferMapper().to_domain(offer_model)
        expected = parse_offer_from_payload(
            MINIMAL_VALID_OFFER, source_id=UUID(SOURCE_UUID)
        )
        for attr in COMPARABLE_OFFER_ATTRS:
            assert getattr(persisted, attr) == getattr(expected, attr)

    def test_auto_references_are_generated_and_returned_with_their_index(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(offer_family_code="ERNUM001")
        auto_offer = PayloadOfferFactory.create(
            identification={"reference": "auto", "versant": "FPT"}
        )

        response = authenticated_client_with_source.post(
            URL,
            data={
                "source_id": SOURCE_UUID,
                "offres": [
                    auto_offer,
                    INVALID_PAYLOAD_OFFER,
                    MINIMAL_VALID_OFFER,
                    auto_offer,
                ],
            },
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        offres = response.json()["offres"]
        assert [o["index"] for o in offres] == [0, 2, 3]
        assert all(o["statut"] == "created" for o in offres)
        assert offres[1]["reference"] == "REF-001"
        generated = [offres[0]["reference"], offres[2]["reference"]]
        assert len(set(generated)) == len(generated)
        for reference in generated:
            assert re.fullmatch(r"CSP-\d{4}-\d{6}", reference)
            assert OfferModel.objects.filter(
                reference=reference, source_id=UUID(SOURCE_UUID)
            ).exists()
        assert not OfferModel.objects.filter(reference="auto").exists()

    def test_generated_reference_can_be_used_to_update_the_offer(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(offer_family_code="ERNUM001")
        auto_offer = PayloadOfferFactory.create(
            identification={"reference": "auto", "versant": "FPT"}
        )
        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [auto_offer]},
            content_type="application/json",
        )
        reference = response.json()["offres"][0]["reference"]

        update = {
            **auto_offer,
            "identification": {"reference": reference, "versant": "FPT"},
            "titre": "Nouveau titre",
        }
        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [update]},
            content_type="application/json",
        )

        assert response.json()["offres"] == [
            {"index": 0, "reference": reference, "statut": "updated"}
        ]
        offer = OfferModel.objects.get(source_id=UUID(SOURCE_UUID))
        assert offer.reference == reference
        assert offer.title == "Nouveau titre"

    def test_sources_share_the_reference_sequence(
        self, authenticated_client_with_source, test_user
    ):
        MetierDjangoFactory(offer_family_code="ERNUM001")
        other_source = SourceDjangoFactory()
        test_user.sources.add(other_source)
        auto_offer = PayloadOfferFactory.create(
            identification={"reference": "auto", "versant": "FPT"}
        )

        references = []
        for source_id in [SOURCE_UUID, str(other_source.source_id)]:
            response = authenticated_client_with_source.post(
                URL,
                data={"source_id": source_id, "offres": [auto_offer]},
                content_type="application/json",
            )
            references.append(response.json()["offres"][0]["reference"])

        assert references[0] != references[1]
