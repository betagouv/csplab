from datetime import datetime, timezone
from uuid import uuid4

import pytest
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage

from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from presentation.ingestion.mappers import (
    OfferDetailOutputMapper,
    OfferInputMapper,
    OfferSummaryOutputMapper,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        (datetime(2024, 1, 15, tzinfo=timezone.utc), "2024-01-15T00:00:00"),
        (
            datetime(2026, 7, 30, 10, 8, 39, 230000, tzinfo=timezone.utc),
            "2026-07-30T10:08:39.23",
        ),
    ],
    ids=[
        "none-value-returns-none",
        "no-microsecond-has-no-fractional-part",
        "microsecond-truncated-to-centiseconds-and-drops-timezone",
    ],
)
def test_isoformat(value, expected):
    assert OfferSummaryOutputMapper._isoformat(value) == expected


def test_offer_input_mapper_maps_profession_referentiel_to_job_family_referential():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        profession={"domaine": "NUM", "metier": "ERNUM001", "referentiel": "RMFPv2"},
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.job_family_referential == "RMFPv2"


def test_offer_input_mapper_maps_profession_domaine_to_functional_area_code():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        profession={"domaine": "NUM", "metier": "ERNUM001", "referentiel": "RMFPv2"},
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.functional_area_code == "NUM"


def test_offer_input_mapper_maps_criteres_to_offer_criteria():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        criteres={
            "diplome_niveau": 5,
            "diplome": "Master",
            "experience": "CONFIRME",
            "specialisations": ["Droit public"],
            "documents_requis": ["CV"],
            "competences_requises": ["Rigueur"],
            "langues": [{"iso_code": "en", "niveau": "B2"}],
        },
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.criteria == OfferCriteria(
        diploma_level=Diploma(5),
        diploma="Master",
        experience_level=ExperienceLevel.CONFIRME,
        specialisations=["Droit public"],
        documents_requis=["CV"],
        competences_requises=["Rigueur"],
        languages=[OfferLanguage(iso_code="en", level=LanguageLevel.B2)],
    )


def test_offer_input_mapper_maps_absent_criteres_to_none():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        criteres=None,
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.criteria is None


class TestOfferDetailOutputMapper:
    def test_criteria_fields_are_absent_when_no_criteria(self):
        offer = OfferFactory.create_entity(criteria=None)

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["educationLevel"] is None
        assert result["diploma"] is None
        assert result["experienceLevel"] is None
        assert result["languages"] == []
        assert result["specialisations"] == []

    def test_education_level_is_mapped_from_diplome_niveau(self):
        offer = OfferFactory.create_entity(
            criteria=OfferCriteria(diploma_level=Diploma(5))
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["educationLevel"] == {
            "code": None,
            "clientCode": "5",
            "label": "5",
            "active": True,
            "parentCode": None,
            "type": "educationLevel",
            "parentType": "",
            "hasChildren": False,
        }

    def test_diploma_is_mapped_from_diplome(self):
        offer = OfferFactory.create_entity(criteria=OfferCriteria(diploma="Master"))

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["diploma"] == {
            "code": None,
            "clientCode": "Master",
            "label": "Master",
            "active": True,
            "parentCode": None,
            "type": "diploma",
            "parentType": "",
            "hasChildren": False,
        }

    def test_experience_level_is_mapped_from_experience(self):
        offer = OfferFactory.create_entity(
            criteria=OfferCriteria(experience_level=ExperienceLevel.CONFIRME)
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["experienceLevel"] == {
            "code": None,
            "clientCode": "CONFIRME",
            "label": "Confirmé",
            "active": True,
            "parentCode": None,
            "type": "experienceLevel",
            "parentType": "",
            "hasChildren": False,
        }

    def test_languages_are_mapped_from_langues(self):
        offer = OfferFactory.create_entity(
            criteria=OfferCriteria(
                languages=[
                    OfferLanguage(iso_code="en", level=LanguageLevel.B2),
                    OfferLanguage(iso_code="de", level=LanguageLevel.A1),
                ]
            )
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["languages"] == [
            {
                "languageName": {
                    "code": None,
                    "clientCode": "en",
                    "label": "en",
                    "active": True,
                    "parentCode": None,
                    "type": "language",
                    "parentType": "",
                    "hasChildren": False,
                },
                "languageLevel": {
                    "code": None,
                    "clientCode": "B2",
                    "label": "B2",
                    "active": True,
                    "parentCode": None,
                    "type": "languageLevel",
                    "parentType": "",
                    "hasChildren": False,
                },
            },
            {
                "languageName": {
                    "code": None,
                    "clientCode": "de",
                    "label": "de",
                    "active": True,
                    "parentCode": None,
                    "type": "language",
                    "parentType": "",
                    "hasChildren": False,
                },
                "languageLevel": {
                    "code": None,
                    "clientCode": "A1",
                    "label": "A1",
                    "active": True,
                    "parentCode": None,
                    "type": "languageLevel",
                    "parentType": "",
                    "hasChildren": False,
                },
            },
        ]

    def test_specialisations_are_mapped(self):
        offer = OfferFactory.create_entity(
            criteria=OfferCriteria(specialisations=["Droit public", "Finances"])
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["specialisations"] == [
            {
                "code": None,
                "clientCode": "Droit public",
                "label": "Droit public",
                "active": True,
                "parentCode": None,
                "type": "specialisation",
                "parentType": "",
                "hasChildren": False,
            },
            {
                "code": None,
                "clientCode": "Finances",
                "label": "Finances",
                "active": True,
                "parentCode": None,
                "type": "specialisation",
                "parentType": "",
                "hasChildren": False,
            },
        ]
