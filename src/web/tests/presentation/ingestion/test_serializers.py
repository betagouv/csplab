from unittest.mock import MagicMock

import pytest

from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory
from presentation.ingestion.serializers import (
    ConditionsInputSerializer,
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
        "employeur": "",
        "complements": "",
        "conditions_exercice": "",
        "descriptif_service": "",
    }

    serializer = DescriptionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors

    assert serializer.validated_data["mission"] == ""
    assert serializer.validated_data["profil"] == ""
    assert serializer.validated_data["employeur"] == ""
    assert serializer.validated_data["complements"] == ""
    assert serializer.validated_data["conditions_exercice"] == ""
    assert serializer.validated_data["descriptif_service"] == ""


def test_description_input_serializer_new_fields_are_optional():
    payload = {
        "mission": "Mission",
        "profil": "Profil",
        "employeur": "Employeur",
        "complements": "",
    }

    serializer = DescriptionInputSerializer(data=payload)

    assert serializer.is_valid(), serializer.errors
    assert "conditions_exercice" not in serializer.validated_data
    assert "descriptif_service" not in serializer.validated_data


@pytest.mark.parametrize(
    "field,limit",
    [
        ("mission", 10000),
        ("profil", 10000),
        ("employeur", 3000),
        ("complements", 5000),
        ("conditions_exercice", 10000),
        ("descriptif_service", 10000),
    ],
)
def test_description_input_serializer_counts_markdown_syntax_in_the_limit(field, limit):
    base = {"mission": "", "profil": "", "employeur": "", "complements": ""}
    at_limit = "**gras**" + "a" * (limit - len("**gras**"))

    assert DescriptionInputSerializer(data={**base, field: at_limit}).is_valid()

    serializer = DescriptionInputSerializer(data={**base, field: at_limit + "a"})
    assert not serializer.is_valid()
    assert field in serializer.errors


@pytest.mark.parametrize(
    "field",
    [
        "mission",
        "profil",
        "employeur",
        "complements",
        "conditions_exercice",
        "descriptif_service",
    ],
)
def test_description_input_serializer_rejects_html(field):
    base = {"mission": "", "profil": "", "employeur": "", "complements": ""}

    serializer = DescriptionInputSerializer(data={**base, field: "<b>gras</b>"})

    assert not serializer.is_valid()
    assert field in serializer.errors


CONDITIONS = {"temps_travail": "TEMPS_PLEIN", "lieu_de_travail": "SUR_SITE"}


@pytest.mark.parametrize(
    "url",
    [
        "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050000000",
        "https://legifrance.gouv.fr/jorf/id/JORFTEXT000050000000",
        "http://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050000000",
    ],
)
def test_conditions_input_serializer_accepts_legifrance_vacancy_notice(url):
    serializer = ConditionsInputSerializer(
        data={**CONDITIONS, "note_ouverture_poste_url": url}
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["note_ouverture_poste_url"] == url


@pytest.mark.parametrize(
    "url",
    [
        "https://exemple.teamtailor.com/jobs/123-gestionnaire-rh",
        "https://www.legifrance.gouv.fr.exemple.com/jorf/id/JORFTEXT000050000000",
        "https://exemple.com/?u=https://www.legifrance.gouv.fr/jorf",
    ],
)
def test_conditions_input_serializer_rejects_vacancy_notice_outside_legifrance(url):
    serializer = ConditionsInputSerializer(
        data={**CONDITIONS, "note_ouverture_poste_url": url}
    )

    assert not serializer.is_valid()
    assert serializer.errors == {
        "note_ouverture_poste_url": [
            (
                "Le lien doit pointer vers l'avis de vacance publié sur "
                "legifrance.gouv.fr."
            )
        ]
    }


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
