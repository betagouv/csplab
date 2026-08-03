from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory
from presentation.ingestion.serializers import (
    DescriptionInputSerializer,
    OffersInputSerializer,
    ProfessionInputSerializer,
)


def test_offers_input_serializer_never_exposes_archived_at():
    assert "archived_at" not in OffersInputSerializer().fields

    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        archived_at="2024-01-01T00:00:00Z",
    )
    serializer = OffersInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    assert "archived_at" not in serializer.validated_data


def test_description_input_serializer_allows_blanks():
    payload = {
        "mission": "",
        "profil": "",
        "employeur": "Employeur",
        "complements": "",
    }

    serializer = DescriptionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors

    assert serializer.validated_data["mission"] == ""
    assert serializer.validated_data["profil"] == ""
    assert serializer.validated_data["complements"] == ""


def test_profession_input_serializer_defaults_referentiel_to_rmfpv2():
    payload = {"domaine": "D01", "metier": "M0001"}

    serializer = ProfessionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["referentiel"] == "RMFPv2"


def test_profession_input_serializer_rejects_null_referentiel():
    payload = {"domaine": "D01", "metier": "M0001", "referentiel": None}

    serializer = ProfessionInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "referentiel" in serializer.errors


def test_profession_input_serializer_rejects_invalid_referentiel():
    payload = {"domaine": "D01", "metier": "M0001", "referentiel": "AUTRE"}

    serializer = ProfessionInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "referentiel" in serializer.errors
