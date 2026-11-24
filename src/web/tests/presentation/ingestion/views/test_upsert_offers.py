import json
import re
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from pydantic import HttpUrl
from referentiel.value_objects.offer_conditions import JobVacancy
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.ingestion.offer_payload_factory import (
    PAYLOAD_SIRET,
    PayloadOfferFactory,
    fake_datetime,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.commons.serializers import INVALID_COUNTRY_CODE
from presentation.ingestion.serializers import (
    DUPLICATE_LANGUAGE,
    INVALID_LANGUAGE_CODE,
    INVALID_SIRET,
    MISSING_SIRET,
    SIRET_WITH_TALENTSOFT_ORGANISME,
    UNKNOWN_SIRET,
    ConditionsInputSerializer,
)
from presentation.ingestion.views.offers import UNKNOWN_GENERATED_REFERENCE

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
        "complements": "Retiré de l'API : ignoré",
    },
    contacts=[],
)

COMPLETE_VALID_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-003", "versant": "FPH"},
    organisation={"nom": fake.company(), "siret": fake.siret().replace(" ", "")},
    url_offre="https://example.com/offre",
    url_candidature="https://example.com/candidature",
    categories=["B", "A"],
    type_contrat="CDD_CDI",
    vacance_poste="OUI",
    description={
        "profil": "",
        "mission": "",
        "employeur": "",
        "conditions_exercice": fake.text(max_nb_chars=1500),
        "descriptif_service": fake.text(max_nb_chars=1500),
    },
    publication={
        "fin_candidature": fake_datetime(future=True),
        "debut_vacance_poste": fake_datetime(future=True),
    },
    localisation=[
        {
            "zone_geographique": "EU",
            "pays": "FRA",
            "region": "28",
            "departement": "14",
            "localisation_label": fake.text(max_nb_chars=500),
            "latitude": fake.pyfloat(min_value=-90, max_value=90),
            "longitude": fake.pyfloat(min_value=-180, max_value=180),
        },
        {
            "zone_geographique": "AM",
            "pays": "MEX",
            "region": None,
            "departement": None,
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
    contacts=[
        {
            "role": "principal",
            "texte": "Camille Martin, bureau RH : camille.martin@exemple.gouv.fr",
            "emails": ["camille.martin@exemple.gouv.fr"],
        },
        {"role": "autre", "texte": "Bureau RH", "emails": []},
    ],
)

INVALID_PAYLOAD_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-004", "versant": "FPT"},
    titre=None,  # missing required field
)

INVALID_DATA_OFFER = PayloadOfferFactory.create(
    identification={"reference": "REF-005", "versant": "FPT"},
    nature_offre="ABC",  # invalid enum value
)


LOCALISATION_FIELDS = [
    "area",
    "country",
    "region",
    "department",
    "label",
    "latitude",
    "longitude",
]


def expected_offer_fields(payload: dict, source_id: UUID) -> dict:
    def parse_datetime(raw: str) -> datetime:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))

    description = payload["description"]
    publication = payload["publication"]
    profession = payload["profession"]

    conditions = payload.get("conditions") or None
    debut_contrat = conditions.get("debut_contrat") if conditions else None
    # mirrors how ConditionsInputSerializer drops unknown fields and parses datetime
    # fields into validated_data
    if conditions:
        conditions = {
            key: parse_datetime(value)
            if key in ("debut_contrat", "fin_contrat") and value
            else value
            for key, value in conditions.items()
            if key in ConditionsInputSerializer().fields
        }
        # stored in a JSONField, where datetimes are encoded as strings
        conditions = json.loads(json.dumps(conditions, cls=DjangoJSONEncoder))

    criteres = payload.get("criteres")
    criteria = (
        {
            "diplome_niveau": criteres.get("diplome_niveau"),
            "diplome": criteres.get("diplome") or None,
            "experience": criteres.get("experience") or None,
            "specialisations": list(criteres.get("specialisations") or []),
            "documents_requis": list(criteres.get("documents_requis") or []),
            "competences_requises": criteres.get("competences_requises") or None,
            "langues": [
                {"iso_code": langue["iso_code"], "niveau": langue["niveau"]}
                for langue in criteres.get("langues") or []
            ],
        }
        if criteres
        else None
    )

    url_candidature = payload.get("url_candidature")
    fin_candidature = publication.get("fin_candidature")
    debut_vacance_poste = publication.get("debut_vacance_poste")

    return {
        "reference": payload["identification"]["reference"],
        "verse": payload["identification"]["versant"],
        "title": payload["titre"],
        "long_title": payload.get("titre_long") or None,
        "profile": description["profil"],
        "mission": description["mission"],
        "employer": description.get("employeur") or None,
        "complements": description.get("complements") or None,
        "exercise_conditions": description.get("conditions_exercice") or None,
        "service_description": description.get("descriptif_service") or None,
        "organization": payload["organisation"]["nom"],
        "categories": list(payload.get("categories") or []),
        "offer_nature": payload["nature_offre"],
        "offer_url": payload.get("url_offre") or None,
        "code_emploi_csp": profession["metier"],
        "job_family_referential": profession.get("referentiel"),
        "functional_area_code": profession.get("domaine"),
        "source_id": source_id,
        "publication_date": datetime.fromisoformat(publication["debut_publication"]),
        "end_publication_date": datetime.fromisoformat(publication["fin_publication"]),
        "application_deadline": parse_datetime(fin_candidature)
        if fin_candidature
        else None,
        "job_vacancy_date": parse_datetime(debut_vacance_poste)
        if debut_vacance_poste
        else None,
        "beginning_date": parse_datetime(debut_contrat) if debut_contrat else None,
        # pydantic normalises the URL, e.g. adds a trailing slash
        "application_url": str(HttpUrl(url_candidature)) if url_candidature else None,
        "application_email": payload.get("email_candidature"),
        "contract_kind": payload.get("type_contrat") or None,
        "job_vacancy": payload.get("vacance_poste"),
        "criteria": criteria,
        "conditions": conditions,
        "contacts": list(payload["contacts"]) if payload.get("contacts") else None,
    }


def expected_localisations(payload: dict) -> list[dict]:
    return [
        {
            "area": loc["zone_geographique"],
            "country": loc["pays"],
            "region": loc["region"] or None,
            "department": loc["departement"] or None,
            "label": loc.get("localisation_label") or "",
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude"),
        }
        for loc in payload.get("localisation") or []
    ]


@pytest.fixture(autouse=True)
def metier(db):
    return MetierDjangoFactory(
        offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
    )


@pytest.fixture(autouse=True)
def organisme(db):
    return OrganismeDjangoFactory(siret=PAYLOAD_SIRET)


def _upserted_offers() -> list[OfferModel]:
    return list(OfferModel.objects.order_by("reference"))


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


def test_api_key_authentication(api_key_client, source):
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


def test_jwt_forbidden_source_id_returns_403(jwt_client):
    response = jwt_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_valid_payload_returns_201_and_valid_offers_to_usecase(
    authenticated_client_with_source,
):
    offers_payload = [MINIMAL_VALID_OFFER, PARTIAL_VALID_OFFER, COMPLETE_VALID_OFFER]
    OrganismeDjangoFactory(siret=COMPLETE_VALID_OFFER["organisation"]["siret"])

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": offers_payload},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    offers = _upserted_offers()
    for payload, offer in zip(offers_payload, offers, strict=True):
        expected = expected_offer_fields(payload, source_id=UUID(SOURCE_UUID))
        assert {field: getattr(offer, field) for field in expected} == expected
        assert list(
            offer.localisations.values(*LOCALISATION_FIELDS)
        ) == expected_localisations(payload)
    # conditions.complements was removed from the API: sent fields are dropped
    partial_offer = offers[1]
    assert "complements" not in partial_offer.conditions


def test_mixed_valid_invalid_offers_in_payload(authenticated_client_with_source):
    offers_payload = [MINIMAL_VALID_OFFER, INVALID_PAYLOAD_OFFER, INVALID_DATA_OFFER]

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": offers_payload},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["offres"] == [
        {"index": 0, "reference": "REF-001", "statut": "creee"}
    ]
    errors = response.json()["errors"]
    assert errors == [
        {
            "index": 1,
            "offre": {"reference": "REF-004", "versant": "FPT"},
            "error": {"titre": ["Ce champ ne peut être nul."]},
        },
        {
            "index": 2,
            "offre": {"reference": "REF-005", "versant": "FPT"},
            "error": {"nature_offre": ["«\xa0ABC\xa0» n'est pas un choix valide."]},
        },
    ]


def test_unknown_metier_returns_error_in_payload(authenticated_client_with_source):
    MetierModel.objects.all().delete()

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    errors = response.json()["errors"]
    assert errors == [
        {
            "index": 0,
            "offre": {"reference": "REF-001", "versant": "FPT"},
            "error": {
                "profession": {
                    "metier": ["Code métier inconnu : ERNUM001."],
                }
            },
        }
    ]


def _offer_with_talentsoft_organisme(entity_code):
    return PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        organisation={
            "nom": fake.company(),
            "siret": "",
            "talentsoft_organisme_entity_code": entity_code,
        },
    )


def test_talentsoft_organisme_is_rejected_with_jwt_authentication(
    authenticated_client_with_source, db
):
    entity_code = TalentsoftOrganismeDjangoFactory().entity_code

    response = authenticated_client_with_source.post(
        URL,
        data={
            "source_id": SOURCE_UUID,
            "offres": [_offer_with_talentsoft_organisme(entity_code)],
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-001", "versant": "FPT"},
            "error": {
                "organisation": {
                    "talentsoft_organisme_entity_code": [
                        "Champ réservé au service ingestion de CSPLab."
                    ]
                }
            },
        }
    ]
    assert _upserted_offers() == []


def test_unknown_talentsoft_organisme_is_rejected_with_api_key_authentication(
    api_key_client, source
):
    response = api_key_client.post(
        URL,
        data={
            "source_id": SOURCE_UUID,
            "offres": [
                _offer_with_talentsoft_organisme("string"),
                MINIMAL_VALID_OFFER
                | {"identification": {"reference": "REF-002", "versant": "FPT"}},
            ],
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-001", "versant": "FPT"},
            "error": {
                "organisation": {
                    "talentsoft_organisme_entity_code": [
                        "Organisme Talentsoft inconnu : string."
                    ]
                }
            },
        }
    ]
    offers = _upserted_offers()
    assert [offer.reference for offer in offers] == ["REF-002"]


def test_known_talentsoft_organisme_is_accepted_with_api_key_authentication(
    api_key_client, source
):
    entity_code = TalentsoftOrganismeDjangoFactory().entity_code

    response = api_key_client.post(
        URL,
        data={
            "source_id": SOURCE_UUID,
            "offres": [_offer_with_talentsoft_organisme(entity_code)],
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    (offer,) = _upserted_offers()
    assert offer.talentsoft_organisme_entity_code_id == entity_code
    # The ingestion service sends no SIRET: the offer has no organisme.
    assert offer.organisme_id is None


def test_siret_with_talentsoft_organisme_is_rejected_with_api_key(
    api_key_client, source
):
    offer = _offer_with_talentsoft_organisme(
        TalentsoftOrganismeDjangoFactory().entity_code
    )
    offer["organisation"]["siret"] = PAYLOAD_SIRET

    response = api_key_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.json()["errors"][0]["error"] == {
        "organisation": {"siret": [SIRET_WITH_TALENTSOFT_ORGANISME]}
    }
    assert not OfferModel.objects.exists()


def test_blank_siret_without_talentsoft_organisme_is_rejected_with_api_key(
    api_key_client, source
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        organisation={"nom": "Mairie", "siret": ""},
    )

    response = api_key_client.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.json()["errors"][0]["error"] == {
        "organisation": {"siret": [MISSING_SIRET]}
    }
    assert not OfferModel.objects.exists()


def test_contacts_are_sorted_by_role_with_deduplicated_emails(
    authenticated_client_with_source,
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-006", "versant": "FPT"},
        contacts=[
            {
                "role": "autre",
                "texte": "  rh@exemple.gouv.fr ; rh@exemple.gouv.fr  ",
                "emails": ["rh@exemple.gouv.fr", "rh@exemple.gouv.fr"],
            },
            {"role": "principal", "texte": "Camille Martin", "emails": []},
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    offers = _upserted_offers()
    assert offers[0].contacts == [
        {"role": "principal", "texte": "Camille Martin", "emails": []},
        {
            "role": "autre",
            "texte": "rh@exemple.gouv.fr ; rh@exemple.gouv.fr",
            "emails": ["rh@exemple.gouv.fr"],
        },
    ]


@pytest.mark.parametrize(
    "contacts,expected_error",
    [
        (
            [
                {"role": "principal", "texte": "A", "emails": []},
                {"role": "principal", "texte": "B", "emails": []},
            ],
            {"contacts": ["Au plus un contact par rôle."]},
        ),
        (
            [{"role": "rh", "texte": "A", "emails": []}],
            {"contacts": {"0": {"role": ["«\xa0rh\xa0» n'est pas un choix valide."]}}},
        ),
        (
            [{"role": "principal", "texte": " . ", "emails": []}],
            {
                "contacts": {
                    "0": {
                        "texte": [
                            "Le texte doit contenir au moins une lettre ou un chiffre."
                        ]
                    }
                }
            },
        ),
        (
            [{"role": "principal", "texte": "a" * 101, "emails": []}],
            {
                "contacts": {
                    "0": {
                        "texte": [
                            (
                                "Assurez-vous que ce champ comporte au plus "
                                "100\xa0caractères."
                            )
                        ]
                    }
                }
            },
        ),
        (
            [{"role": "principal", "texte": "A", "emails": ["pas-un-email"]}],
            {
                "contacts": {
                    "0": {"emails": {"0": ["Saisissez une adresse e-mail valide."]}}
                }
            },
        ),
        (
            [{"email": "camille.martin@exemple.gouv.fr"}],
            {
                "contacts": {
                    "0": {
                        "role": ["Ce champ est obligatoire."],
                        "texte": ["Ce champ est obligatoire."],
                        "emails": ["Ce champ est obligatoire."],
                    }
                }
            },
        ),
    ],
)
def test_invalid_contacts_are_rejected(
    authenticated_client_with_source, contacts, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-007", "versant": "FPT"},
        contacts=contacts,
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-007", "versant": "FPT"},
            "error": expected_error,
        }
    ]


@pytest.mark.parametrize(
    "documents_requis,expected_error",
    [
        (
            ["CV", "Copie des diplômes"],
            {"1": ["«\xa0Copie des diplômes\xa0» n'est pas un choix valide."]},
        ),
        (
            ["CV", "LETTRE_MOTIVATION", "CV"],
            ["Chaque document ne peut être cité qu'une fois."],
        ),
    ],
    ids=["unknown-document", "duplicate-document"],
)
def test_invalid_required_documents_are_rejected(
    authenticated_client_with_source, documents_requis, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-010", "versant": "FPT"},
        criteres={"documents_requis": documents_requis},
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-010", "versant": "FPT"},
            "error": {"criteres": {"documents_requis": expected_error}},
        }
    ]


def test_competences_requises_markdown_is_passed_to_usecase(
    authenticated_client_with_source,
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-011", "versant": "FPT"},
        criteres={"competences_requises": "Connaissances :\n\n- Droit public"},
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    offers = _upserted_offers()
    assert offers[0].criteria["competences_requises"] == (
        "Connaissances :\n\n- Droit public"
    )


@pytest.mark.parametrize(
    "competences_requises,expected_error",
    [
        (["Rigueur"], ["Chaîne de caractère invalide."]),
        (
            "a" * 2001,
            ["Assurez-vous que ce champ comporte au plus 2000\xa0caractères."],
        ),
    ],
    ids=["list", "too-long"],
)
def test_invalid_competences_requises_are_rejected(
    authenticated_client_with_source, competences_requises, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-012", "versant": "FPT"},
        criteres={"competences_requises": competences_requises},
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-012", "versant": "FPT"},
            "error": {"criteres": {"competences_requises": expected_error}},
        }
    ]


def test_criteria_and_conditions_at_their_limits_are_normalized(
    authenticated_client_with_source,
):
    specialisations = ["s" * 255, *(f"Spécialisation {i}" for i in range(18))]
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-LIMITES", "versant": "FPT"},
        criteres={
            "diplome": "d" * 255,
            "specialisations": [*specialisations, specialisations[0]],
            "langues": [
                {"iso_code": "en", "niveau": "B2"},
                {"iso_code": "De", "niveau": "A1"},
            ],
        },
        conditions={
            "temps_travail": "TEMPS_PLEIN",
            "lieu_de_travail": "SUR_SITE",
            "duree_contrat": "a" * 100,
        },
    )
    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    (received,) = _upserted_offers()
    assert received.criteria["diplome"] == "d" * 255
    assert received.criteria["specialisations"] == specialisations
    assert [language["iso_code"] for language in received.criteria["langues"]] == [
        "EN",
        "DE",
    ]
    assert received.conditions["duree_contrat"] == "a" * 100


@pytest.mark.parametrize(
    "criteres,conditions,expected_error",
    [
        (
            {"diplome": "d" * 256},
            None,
            {
                "criteres": {
                    "diplome": [
                        "Assurez-vous que ce champ comporte au plus 255\xa0caractères."
                    ]
                }
            },
        ),
        (
            {"specialisations": [f"Spécialisation {i}" for i in range(21)]},
            None,
            {
                "criteres": {
                    "specialisations": [
                        "Assurez-vous que ce champ n'a pas plus de 20 éléments."
                    ]
                }
            },
        ),
        (
            {"specialisations": ["Droit public", "s" * 256]},
            None,
            {
                "criteres": {
                    "specialisations": {
                        "1": [
                            (
                                "Assurez-vous que ce champ comporte au plus "
                                "255\xa0caractères."
                            )
                        ]
                    }
                }
            },
        ),
        (
            None,
            {"duree_contrat": "a" * 101},
            {
                "conditions": {
                    "duree_contrat": [
                        "Assurez-vous que ce champ comporte au plus 100\xa0caractères."
                    ]
                }
            },
        ),
        (
            {"langues": [{"iso_code": "e", "niveau": "B2"}]},
            None,
            {"criteres": {"langues": {"0": {"iso_code": [INVALID_LANGUAGE_CODE]}}}},
        ),
        (
            {"langues": [{"iso_code": "XX", "niveau": "B2"}]},
            None,
            {"criteres": {"langues": {"0": {"iso_code": [INVALID_LANGUAGE_CODE]}}}},
        ),
        (
            {
                "langues": [
                    {"iso_code": "EN", "niveau": "B2"},
                    {"iso_code": "en", "niveau": "C1"},
                ]
            },
            None,
            {"criteres": {"langues": [DUPLICATE_LANGUAGE]}},
        ),
    ],
    ids=[
        "diplome-too-long",
        "too-many-specialisations",
        "specialisation-too-long",
        "duree-contrat-too-long",
        "iso-code-too-short",
        "iso-code-unknown",
        "duplicate-language",
    ],
)
def test_invalid_free_texts_of_criteria_and_conditions_are_rejected(
    authenticated_client_with_source, criteres, conditions, expected_error
):
    overrides = {}
    if criteres is not None:
        overrides["criteres"] = criteres
    if conditions is not None:
        overrides["conditions"] = {
            "temps_travail": "TEMPS_PLEIN",
            "lieu_de_travail": "SUR_SITE",
            **conditions,
        }
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-HORS-LIMITES", "versant": "FPT"}, **overrides
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-HORS-LIMITES", "versant": "FPT"},
            "error": expected_error,
        }
    ]


def test_bases_legales_markdown_is_passed_to_usecase(authenticated_client_with_source):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-013", "versant": "FPT"},
        conditions={
            "temps_travail": "TEMPS_PLEIN",
            "lieu_de_travail": "SUR_SITE",
            "management": "SANS",
            "bases_legales": "Ouvert :\n\n- 1° aux fonctionnaires",
        },
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    offers = _upserted_offers()
    assert offers[0].conditions["bases_legales"] == (
        "Ouvert :\n\n- 1° aux fonctionnaires"
    )


@pytest.mark.parametrize(
    "bases_legales,expected_error",
    [
        (
            "Ouvert :<br>aux fonctionnaires",
            [
                (
                    "Les balises HTML ne sont pas acceptées (<br>) : utilisez la "
                    "syntaxe Markdown, ou écrivez \\< pour afficher le caractère <."
                )
            ],
        ),
        (
            "[Loi](javascript:alert(1))",
            [
                (
                    "Lien non autorisé (javascript:alert(1)) : seuls les liens http, "
                    "https et mailto sont acceptés."
                )
            ],
        ),
        (
            "a" * 1501,
            ["Assurez-vous que ce champ comporte au plus 1500\xa0caractères."],
        ),
    ],
    ids=["html", "forbidden-link", "too-long"],
)
def test_invalid_bases_legales_are_rejected(
    authenticated_client_with_source, bases_legales, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-014", "versant": "FPT"},
        conditions={
            "temps_travail": "TEMPS_PLEIN",
            "lieu_de_travail": "SUR_SITE",
            "management": "SANS",
            "bases_legales": bases_legales,
        },
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-014", "versant": "FPT"},
            "error": {"conditions": {"bases_legales": expected_error}},
        }
    ]
    assert _upserted_offers() == []


@pytest.mark.parametrize(
    "categories,expected_error",
    [
        (None, ["Ce champ est obligatoire."]),
        ([], ["Au moins une catégorie est obligatoire."]),
        ([""], ["«\xa0\xa0» n'est pas un choix valide."]),
    ],
)
def test_invalid_categories_are_rejected(
    authenticated_client_with_source, categories, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-007", "versant": "FPT"},
    )
    if categories is None:
        del offer["categories"]
    else:
        offer["categories"] = categories

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-007", "versant": "FPT"},
            "error": {"categories": expected_error},
        }
    ]


def test_email_candidature_is_passed_to_usecase(authenticated_client_with_source):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-008", "versant": "FPT"},
        url_candidature=None,
        email_candidature="rh@exemple.gouv.fr",
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    offers = _upserted_offers()
    assert offers[0].application_email == "rh@exemple.gouv.fr"
    assert offers[0].application_url is None


APPLICATION_CHANNEL_ERROR = {
    "non_field_errors": [
        "Renseigner soit url_candidature, soit email_candidature, mais pas les deux."
    ]
}


@pytest.mark.parametrize(
    "candidature,expected_error",
    [
        (
            {
                "url_candidature": "https://exemple.gouv.fr/candidature",
                "email_candidature": "rh@exemple.gouv.fr",
            },
            APPLICATION_CHANNEL_ERROR,
        ),
        (
            {"url_candidature": None, "email_candidature": None},
            APPLICATION_CHANNEL_ERROR,
        ),
        ({"url_candidature": None}, APPLICATION_CHANNEL_ERROR),
        (
            {"url_candidature": None, "email_candidature": "pas-un-email"},
            {"email_candidature": ["Saisissez une adresse e-mail valide."]},
        ),
    ],
)
def test_invalid_application_channels_are_rejected(
    authenticated_client_with_source, candidature, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-009", "versant": "FPT"},
        **candidature,
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-009", "versant": "FPT"},
            "error": expected_error,
        }
    ]


@pytest.mark.parametrize(
    ("region", "departement", "expected_message"),
    [
        (
            "11",
            "13",
            (
                "Le département 13 (Bouches-du-Rhône) n'appartient pas à la "
                "région 11 (Île-de-France)."
            ),
        ),
        (
            "01",
            "01",
            "Le département 01 (Ain) n'appartient pas à la région 01 (Guadeloupe).",
        ),
        (
            "DOM",
            "988",
            (
                "Le département 988 (Nouvelle-Calédonie) n'appartient pas à la "
                "région DOM."
            ),
        ),
    ],
)
def test_inconsistent_region_and_department_are_rejected(
    authenticated_client_with_source, region, departement, expected_message
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-011", "versant": "FPT"},
        localisation=[
            {
                "zone_geographique": "EU",
                "pays": "FRA",
                "region": region,
                "departement": departement,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            }
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-011", "versant": "FPT"},
            "error": {"localisation": {"0": {"non_field_errors": [expected_message]}}},
        }
    ]
    assert _upserted_offers() == []


@pytest.mark.parametrize(
    ("region", "departement"),
    [("11", "75"), ("11", None), (None, "75")],
)
def test_region_or_department_abroad_is_rejected(
    authenticated_client_with_source, region, departement
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-013", "versant": "FPE"},
        localisation=[
            {
                "zone_geographique": "EU",
                "pays": "DEU",
                "region": region,
                "departement": departement,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            }
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    expected_message = (
        "La région et le département doivent être vides pour une "
        "offre localisée hors de France."
    )
    assert response.json()["errors"][0]["error"] == {
        "localisation": {"0": {"non_field_errors": [expected_message]}}
    }
    assert _upserted_offers() == []


@pytest.mark.parametrize(
    ("region", "departement"),
    [
        ("93", "13"),
        ("01", "971"),
        ("DOM", "971"),
        ("TOM", "988"),
        ("TOM", "977"),
        ("TOM", "978"),
    ],
)
def test_consistent_region_and_department_are_accepted(
    authenticated_client_with_source, region, departement
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-012", "versant": "FPT"},
        localisation=[
            {
                "zone_geographique": "EU",
                "pays": "FRA",
                "region": region,
                "departement": departement,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            }
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    assert len(_upserted_offers()) == 1


def test_description_with_html_is_rejected_with_an_explicit_message(
    authenticated_client_with_source,
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-010", "versant": "FPT"},
    )
    offer["description"]["mission"] = "Missions : <script>alert(1)</script>"
    offer["description"]["profil"] = "[Fiche](javascript:alert(1))"

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-010", "versant": "FPT"},
            "error": {
                "description": {
                    "mission": [
                        (
                            "Les balises HTML ne sont pas acceptées (<script>) : "
                            "utilisez la syntaxe Markdown, ou écrivez \\< pour "
                            "afficher le caractère <."
                        ),
                        (
                            "Les balises HTML ne sont pas acceptées (</script>) : "
                            "utilisez la syntaxe Markdown, ou écrivez \\< pour "
                            "afficher le caractère <."
                        ),
                    ],
                    "profil": [
                        (
                            "Lien non autorisé (javascript:alert(1)) : seuls les "
                            "liens http, https et mailto sont acceptés."
                        )
                    ],
                }
            },
        }
    ]
    assert _upserted_offers() == []


def test_country_code_not_in_uppercase_is_rejected(authenticated_client_with_source):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-011", "versant": "FPT"},
        localisation=[
            {
                "zone_geographique": "EU",
                "pays": "fra",
                "region": None,
                "departement": None,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            }
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer, MINIMAL_VALID_OFFER]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-011", "versant": "FPT"},
            "error": {"localisation": {"0": {"pays": [INVALID_COUNTRY_CODE]}}},
        }
    ]
    offers = _upserted_offers()
    assert [offer.reference for offer in offers] == ["REF-001"]


@pytest.mark.parametrize(
    ("pays", "territory", "region", "departement"),
    [
        ("GLP", "Guadeloupe", "DOM", "971"),
        ("REU", "La Réunion", "DOM", "974"),
        ("SPM", "Saint-Pierre-et-Miquelon", "TOM", "975"),
        ("WLF", "Wallis-et-Futuna", "TOM", "WLF"),
        ("NCL", "Nouvelle-Calédonie", "TOM", "988"),
    ],
)
def test_overseas_country_code_is_rejected(
    authenticated_client_with_source, pays, territory, region, departement
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-014", "versant": "FPT"},
        localisation=[
            _localisation_payload("76"),
            {
                "zone_geographique": "AM",
                "pays": pays,
                "region": None,
                "departement": None,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            },
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    expected_message = (
        f"{territory} : renseigner `pays` = `FRA`, `region` = `{region}`, "
        f"`departement` = `{departement}`."
    )
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-014", "versant": "FPT"},
            "error": {"localisation": {"1": {"pays": [expected_message]}}},
        }
    ]
    assert _upserted_offers() == []


@pytest.mark.parametrize("pays", ["DOM", "ATF", "DEU"])
def test_country_code_abroad_is_accepted(authenticated_client_with_source, pays):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-015", "versant": "FPT"},
        localisation=[
            {
                "zone_geographique": "AM",
                "pays": pays,
                "region": None,
                "departement": None,
                "localisation_label": "",
                "latitude": None,
                "longitude": None,
            }
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == []
    assert len(_upserted_offers()) == 1


def test_database_error_returns_500_and_saves_nothing(
    authenticated_client_with_source,
):
    response = authenticated_client_with_source.post(
        URL,
        data={
            "source_id": SOURCE_UUID,
            "offres": [MINIMAL_VALID_OFFER, MINIMAL_VALID_OFFER],
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert not OfferModel.objects.exists()


DUPLICATE_LOCALISATION_MESSAGE = (
    "Un même lieu (pays, région, département et libellé) ne peut figurer qu'une fois."
)


def _localisation_payload(departement: str, label: str = "") -> dict:
    return {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "28",
        "departement": departement,
        "localisation_label": label,
        "latitude": None,
        "longitude": None,
    }


def test_more_than_50_localisations_are_rejected(authenticated_client_with_source):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-51", "versant": "FPT"},
        localisation=[
            _localisation_payload("14", label=f"Site {i}") for i in range(51)
        ],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-51", "versant": "FPT"},
            "error": {
                "localisation": {"non_field_errors": ["Au plus 50 lieux par offre."]}
            },
        }
    ]
    assert _upserted_offers() == []


def test_duplicate_localisations_are_rejected(authenticated_client_with_source):
    first = _localisation_payload("14", label="Caen")
    duplicate = {**first, "latitude": 49.18, "longitude": -0.37}
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-DOUBLON", "versant": "FPT"},
        localisation=[first, duplicate],
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-DOUBLON", "versant": "FPT"},
            "error": {"localisation": [DUPLICATE_LOCALISATION_MESSAGE]},
        }
    ]
    assert _upserted_offers() == []


@pytest.mark.parametrize(
    "siret,expected_error",
    [
        ("", MISSING_SIRET),
        ("1234567890123", INVALID_SIRET),
        ("1234567890123A", INVALID_SIRET),
        ("12345678901234", INVALID_SIRET),
        ("73282932000074", UNKNOWN_SIRET),
    ],
    ids=["blank", "13-digits", "letter", "wrong-checksum", "unknown"],
)
def test_invalid_or_unknown_siret_is_rejected(
    authenticated_client_with_source, siret, expected_error
):
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-SIRET", "versant": "FPT"},
        organisation={"nom": "Mairie", "siret": siret},
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["errors"] == [
        {
            "index": 0,
            "offre": {"reference": "REF-SIRET", "versant": "FPT"},
            "error": {"organisation": {"siret": [expected_error]}},
        }
    ]
    assert not OfferModel.objects.exists()


def test_siret_of_a_deleted_organisme_is_rejected(authenticated_client_with_source):
    organisme = OrganismeDjangoFactory(supprime_le=timezone.now())
    offer = PayloadOfferFactory.create(
        identification={"reference": "REF-SIRET", "versant": "FPT"},
        organisation={"nom": organisme.nom, "siret": organisme.siret},
    )

    response = authenticated_client_with_source.post(
        URL,
        data={"source_id": SOURCE_UUID, "offres": [offer]},
        content_type="application/json",
    )

    assert response.json()["errors"][0]["error"] == {
        "organisation": {"siret": [UNKNOWN_SIRET]}
    }


def test_offer_is_attached_to_the_organisme_of_its_siret(
    authenticated_client_with_source, organisme
):
    other_organisme = OrganismeDjangoFactory()

    for siret, expected in (
        (organisme.siret, organisme),
        (other_organisme.siret, other_organisme),
    ):
        offer = {
            **MINIMAL_VALID_OFFER,
            "organisation": {"nom": "Mairie", "siret": siret},
        }
        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.json()["errors"] == []
        assert OfferModel.objects.get(reference="REF-001").organisme == expected


class TestOffersUpsertViewDbVerified:
    @pytest.fixture(autouse=True)
    def metier(self):
        return None

    def test_creates_and_persists_the_offer(self, authenticated_client_with_source):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [MINIMAL_VALID_OFFER]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "creees": 1,
            "mises_a_jour": 0,
            "errors": [],
            "offres": [{"index": 0, "reference": "REF-001", "statut": "creee"}],
        }

        offer_model = OfferModel.objects.get(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        )
        expected = expected_offer_fields(
            MINIMAL_VALID_OFFER, source_id=UUID(SOURCE_UUID)
        )
        assert {field: getattr(offer_model, field) for field in expected} == expected
        assert list(
            offer_model.localisations.values(*LOCALISATION_FIELDS)
        ) == expected_localisations(MINIMAL_VALID_OFFER)

    @pytest.mark.parametrize(
        "titre_long",
        [{}, {"titre_long": None}, {"titre_long": ""}],
        ids=["missing", "null", "empty"],
    )
    def test_offer_without_titre_long_is_persisted_without_long_title(
        self, authenticated_client_with_source, titre_long
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = {
            k: v for k, v in MINIMAL_VALID_OFFER.items() if k != "titre_long"
        } | titre_long

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"] == []
        offer_model = OfferModel.objects.get(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        )
        assert offer_model.long_title is None

    @pytest.mark.parametrize(
        "vacance_poste,expected",
        [({}, None), ({"vacance_poste": None}, None)]
        + [({"vacance_poste": v.name}, v.name) for v in JobVacancy],
        ids=["missing", "null"] + [v.name for v in JobVacancy],
    )
    def test_persists_vacance_poste(
        self, authenticated_client_with_source, vacance_poste, expected
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = {
            k: v for k, v in MINIMAL_VALID_OFFER.items() if k != "vacance_poste"
        } | vacance_poste

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"] == []
        offer_model = OfferModel.objects.get(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        )
        assert offer_model.job_vacancy == expected

    def test_empty_vacance_poste_is_rejected(self, authenticated_client_with_source):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = MINIMAL_VALID_OFFER | {"vacance_poste": ""}

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"][0]["error"] == {
            "vacance_poste": ["«\xa0\xa0» n'est pas un choix valide."]
        }
        assert not OfferModel.objects.filter(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        ).exists()

    def test_offer_with_titre_long_equal_to_titre_is_rejected(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = MINIMAL_VALID_OFFER | {"titre_long": MINIMAL_VALID_OFFER["titre"]}

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"][0]["error"] == {
            "titre_long": ["Le titre long doit différer du titre, sinon l'omettre."]
        }
        assert not OfferModel.objects.filter(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        ).exists()

    def test_persists_all_categories_in_sent_order(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offre = {**MINIMAL_VALID_OFFER, "categories": ["B", "A", "B"]}

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offre]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        offer_model = OfferModel.objects.get(
            reference="REF-001", source_id=UUID(SOURCE_UUID)
        )
        assert offer_model.categories == ["B", "A"]
        assert offer_model.main_category == "B"

    def test_localisation_without_coordinates_is_persisted_with_null_coordinates(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = PayloadOfferFactory.create(
            identification={"reference": "REF-SANS-GPS", "versant": "FPT"},
            localisation=[
                {
                    "zone_geographique": "EU",
                    "pays": "FRA",
                    "region": "28",
                    "departement": "14",
                    "localisation_label": "Caen",
                }
            ],
        )

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"] == []
        offer_model = OfferModel.objects.get(
            reference="REF-SANS-GPS", source_id=UUID(SOURCE_UUID)
        )
        localisation = offer_model.localisations.get(position=0)
        assert localisation.label == "Caen"
        assert localisation.latitude is None
        assert localisation.longitude is None

    def _post_localisations(self, client, reference: str, localisations: list):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = PayloadOfferFactory.create(
            identification={"reference": reference, "versant": "FPT"},
            localisation=localisations,
        )
        response = client.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"] == []
        return OfferModel.objects.get(reference=reference, source_id=UUID(SOURCE_UUID))

    def test_persists_every_localisation_in_sent_order(
        self, authenticated_client_with_source
    ):
        offer_model = self._post_localisations(
            authenticated_client_with_source,
            "REF-MULTI",
            [
                _localisation_payload("14", label="Caen"),
                _localisation_payload("50", label="Saint-Lô"),
            ],
        )

        assert list(
            offer_model.localisations.values_list(
                "position", "area", "country", "region", "department", "label"
            )
        ) == [
            (0, "EU", "FRA", "28", "14", "Caen"),
            (1, "EU", "FRA", "28", "50", "Saint-Lô"),
        ]

    def test_update_replaces_the_localisations(
        self, authenticated_client_with_source, source
    ):
        OfferDjangoFactory(
            source=source,
            reference="REF-MAJ",
            localisations=[
                {"area": "EU", "country": "FRA", "region": "28", "department": "14"},
                {"area": "EU", "country": "FRA", "region": "28", "department": "50"},
            ],
        )

        offer_model = self._post_localisations(
            authenticated_client_with_source,
            "REF-MAJ",
            [_localisation_payload("61", label="Alençon")],
        )

        assert list(
            offer_model.localisations.values_list("position", "department", "label")
        ) == [(0, "61", "Alençon")]

    def test_offer_without_localisation_has_none(
        self, authenticated_client_with_source
    ):
        offer_model = self._post_localisations(
            authenticated_client_with_source, "REF-SANS-LIEU", []
        )

        assert not offer_model.localisations.exists()

    def test_offer_abroad_is_persisted_without_region_nor_department(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        offer = PayloadOfferFactory.create(
            identification={"reference": "REF-BERLIN", "versant": "FPE"},
            localisation=[
                {
                    "zone_geographique": "EU",
                    "pays": "DEU",
                    "region": None,
                    "departement": None,
                    "localisation_label": "Ambassade de France à Berlin",
                    "latitude": 52.5163,
                    "longitude": 13.3777,
                }
            ],
        )

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["errors"] == []
        offer_model = OfferModel.objects.get(
            reference="REF-BERLIN", source_id=UUID(SOURCE_UUID)
        )
        assert list(offer_model.localisations.values(*LOCALISATION_FIELDS)) == [
            {
                "area": "EU",
                "country": "DEU",
                "region": None,
                "department": None,
                "label": "Ambassade de France à Berlin",
                "latitude": 52.5163,
                "longitude": 13.3777,
            }
        ]

    def test_auto_references_are_generated_and_returned_with_their_index(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
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
        assert all(o["statut"] == "creee" for o in offres)
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
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
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
            {"index": 0, "reference": reference, "statut": "mise_a_jour"}
        ]
        offer = OfferModel.objects.get(source_id=UUID(SOURCE_UUID))
        assert offer.reference == reference
        assert offer.title == "Nouveau titre"

    def test_sources_share_the_reference_sequence(
        self, authenticated_client_with_source, test_user
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
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

    def test_unknown_generated_reference_is_rejected(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        explicit_reference = f"CSP-{datetime.now(ZoneInfo('Europe/Paris')).year}-000001"
        auto_offer = PayloadOfferFactory.create(
            identification={"reference": "auto", "versant": "FPT"}
        )
        explicit_offer = PayloadOfferFactory.create(
            identification={"reference": explicit_reference, "versant": "FPT"}
        )

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [explicit_offer, auto_offer]},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert [o["index"] for o in body["offres"]] == [1]
        assert OfferModel.objects.filter(source_id=UUID(SOURCE_UUID)).count() == 1
        assert body["errors"] == [
            {
                "index": 0,
                "offre": {"reference": explicit_reference, "versant": "FPT"},
                "error": {"reference": [UNKNOWN_GENERATED_REFERENCE]},
            }
        ]

    def test_generated_reference_of_another_source_is_rejected(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM"
        )
        reference = OfferDjangoFactory(reference="CSP-2026-000042").reference
        offer = PayloadOfferFactory.create(
            identification={"reference": reference, "versant": "FPT"}
        )

        response = authenticated_client_with_source.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": [offer]},
            content_type="application/json",
        )

        assert response.json()["offres"] == []
        assert [e["index"] for e in response.json()["errors"]] == [0]
        assert not OfferModel.objects.filter(source_id=UUID(SOURCE_UUID)).exists()

    def _upsert(self, client, professions):
        offres = []
        for index, profession in enumerate(professions):
            offre = PayloadOfferFactory.create(
                identification={"reference": f"REF-{index}", "versant": "FPT"}
            )
            offre["profession"] = profession
            offres.append(offre)
        return client.post(
            URL,
            data={"source_id": SOURCE_UUID, "offres": offres},
            content_type="application/json",
        )

    def test_offer_without_domaine_is_created_with_metier_domaine(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERACH001", domaine_fonctionnel_code="ACH"
        )

        response = self._upsert(
            authenticated_client_with_source, [{"metier": "ERACH001"}]
        )

        assert response.json()["errors"] == []
        offre = OfferModel.objects.get(reference="REF-0")
        assert offre.functional_area_code == "ACH"

    def test_offer_with_mismatching_domaine_is_rejected_and_others_saved(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERACH001", domaine_fonctionnel_code="ACH"
        )

        response = self._upsert(
            authenticated_client_with_source,
            [
                {"domaine": "COM", "metier": "ERACH001"},
                {"domaine": "ACH", "metier": "ERACH001"},
            ],
        )

        body = response.json()
        assert body["offres"] == [{"index": 1, "reference": "REF-1", "statut": "creee"}]
        assert body["errors"] == [
            {
                "index": 0,
                "offre": {"reference": "REF-0", "versant": "FPT"},
                "error": {
                    "profession": {
                        "domaine": [
                            "Le domaine COM ne correspond pas au métier ERACH001 (ACH)."
                        ]
                    }
                },
            }
        ]

    def test_ambiguous_metier_requires_one_of_its_domaines(
        self, authenticated_client_with_source
    ):
        MetierDjangoFactory(
            offer_family_code="ERTRA007", domaine_fonctionnel_code="SEC"
        )
        MetierDjangoFactory(
            offer_family_code="ERTRA007", domaine_fonctionnel_code="TRA"
        )

        response = self._upsert(
            authenticated_client_with_source,
            [{"metier": "ERTRA007"}, {"domaine": "SEC", "metier": "ERTRA007"}],
        )

        body = response.json()
        assert body["offres"] == [{"index": 1, "reference": "REF-1", "statut": "creee"}]
        assert body["errors"][0]["error"] == {
            "profession": {
                "domaine": [
                    (
                        "Le métier ERTRA007 relève de plusieurs domaines (SEC, TRA) : "
                        "renseigner l'un d'eux."
                    )
                ]
            }
        }
        assert OfferModel.objects.get(reference="REF-1").functional_area_code == "SEC"
