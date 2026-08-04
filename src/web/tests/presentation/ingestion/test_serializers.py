from unittest.mock import MagicMock

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
    payload = {"domaine": "NUM", "metier": "ERNUM001"}

    serializer = ProfessionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["referentiel"] == "RMFPv2"


def test_profession_input_serializer_rejects_null_referentiel():
    payload = {"domaine": "NUM", "metier": "ERNUM001", "referentiel": None}

    serializer = ProfessionInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "referentiel" in serializer.errors


def test_profession_input_serializer_rejects_invalid_referentiel():
    payload = {"domaine": "NUM", "metier": "ERNUM001", "referentiel": "AUTRE"}

    serializer = ProfessionInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "referentiel" in serializer.errors


def test_profession_input_serializer_skips_metier_check_without_repository_in_context():
    payload = {"domaine": "NUM", "metier": "INCONNU"}

    serializer = ProfessionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors


def test_profession_input_serializer_accepts_metier_known_by_repository():
    metiers_repository = MagicMock()
    metiers_repository.get_filtered.return_value = [MagicMock()]
    payload = {"domaine": "NUM", "metier": "ERNUM001"}

    serializer = ProfessionInputSerializer(
        data=payload, context={"metiers_repository": metiers_repository}
    )

    assert serializer.is_valid(), serializer.errors
    metiers_repository.get_filtered.assert_called_once_with(
        {"offer_family_code": "ERNUM001"}
    )


def test_profession_input_serializer_rejects_metier_unknown_by_repository():
    metiers_repository = MagicMock()
    metiers_repository.get_filtered.return_value = []
    payload = {"domaine": "NUM", "metier": "ERNUM999"}

    serializer = ProfessionInputSerializer(
        data=payload, context={"metiers_repository": metiers_repository}
    )

    assert not serializer.is_valid()
    assert "metier" in serializer.errors


def test_profession_input_serializer_rejects_invalid_domaine_for_rmfpv2():
    payload = {"domaine": "ZZZ", "metier": "ERNUM001"}

    serializer = ProfessionInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "domaine" in serializer.errors


def test_profession_input_serializer_skips_checks_for_other_referentiel():
    # JobFamilyReferential only exposes RMFPv2 today, so the "referentiel" field
    # itself blocks any other value before reaching validate() through the public
    # API. Calling validate() directly exercises the skip branch that protects
    # future referentiels from being checked against RMFP-specific data.
    metiers_repository = MagicMock()
    serializer = ProfessionInputSerializer(
        context={"metiers_repository": metiers_repository}
    )
    data = {"referentiel": "AUTRE", "domaine": "ZZZ", "metier": "INCONNU"}

    validated = serializer.validate(data)

    assert validated == data
    metiers_repository.get_filtered.assert_not_called()
