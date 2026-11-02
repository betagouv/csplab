from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from referentiel.entities.talentsoft_organisme import TalentsoftOrganisme
from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from referentiel.value_objects.required_document import RequiredDocument

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


@pytest.mark.parametrize(
    "job_vacancy,expected_client_code,expected_label",
    [
        ("OUI", "STATUT01", "Poste vacant"),
        ("NON", "STATUT02", "Poste susceptible d'être vacant"),
    ],
)
def test_summary_output_mapper_maps_job_vacancy_to_professional_category(
    job_vacancy, expected_client_code, expected_label
):
    offer = replace(OfferFactory.create_entity(), job_vacancy=job_vacancy)

    result = OfferSummaryOutputMapper().to_dict(offer)

    assert result["professionalCategory"] == {
        "code": None,
        "clientCode": expected_client_code,
        "label": expected_label,
        "active": True,
        "parentCode": None,
        "type": "professionalCategory",
        "parentType": "",
        "hasChildren": False,
    }


@pytest.mark.parametrize("job_vacancy", [None, "", "1"])
def test_summary_output_mapper_maps_unknown_job_vacancy_to_null(job_vacancy):
    offer = replace(OfferFactory.create_entity(), job_vacancy=job_vacancy)

    result = OfferSummaryOutputMapper().to_dict(offer)

    assert result["professionalCategory"] is None


def test_summary_output_mapper_maps_organisation_description_from_organisme():
    offer = replace(
        OfferFactory.create_entity(),
        employer="Présentation de l'employeur",
        talentsoft_organisme=TalentsoftOrganisme(
            entity_code="ENT-1",
            code=1,
            name="Commune de Paris",
            description="Description de la commune",
        ),
    )

    result = OfferSummaryOutputMapper().to_dict(offer)

    assert result["organisationDescription"] == "Description de la commune"


def test_summary_output_mapper_maps_null_organisation_description_without_organisme():
    offer = replace(
        OfferFactory.create_entity(), employer="Présentation de l'employeur"
    )

    result = OfferSummaryOutputMapper().to_dict(offer)

    assert result["organisationDescription"] is None


@pytest.mark.parametrize(
    "markdown,expected",
    [
        (None, None),
        ("", None),
        ("**Activités :**", "<p><strong>Activités :</strong></p>"),
        (
            "- adapter\n- créer",
            "<ul>\n<li>adapter</li>\n<li>créer</li>\n</ul>",
        ),
        (
            "[Site](https://exemple.gouv.fr)",
            (
                '<p><a href="https://exemple.gouv.fr" target="_blank" '
                'rel="noopener noreferrer">Site</a></p>'
            ),
        ),
        ("## Missions", "<p><strong>Missions</strong></p>"),
        ("<b>gras</b>", "<p>&lt;b&gt;gras&lt;/b&gt;</p>"),
    ],
)
def test_summary_output_mapper_renders_descriptions_in_html(markdown, expected):
    offer = replace(OfferFactory.create_entity(), mission=markdown, profile=markdown)

    result = OfferSummaryOutputMapper().to_dict(offer)

    assert result["description1"] == markdown
    assert result["description2"] == markdown
    assert result["description1Formatted"] == expected
    assert result["description2Formatted"] == expected


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
            "competences_requises": "- Rigueur\n- Autonomie",
            "langues": [{"iso_code": "en", "niveau": "B2"}],
        },
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.criteria == OfferCriteria(
        diploma_level=Diploma(5),
        diploma="Master",
        experience_level=ExperienceLevel.CONFIRME,
        specialisations=["Droit public"],
        documents_requis=[RequiredDocument.CV],
        competences_requises="- Rigueur\n- Autonomie",
        languages=[OfferLanguage(iso_code="en", level=LanguageLevel.B2)],
    )


def test_offer_input_mapper_maps_export_unif_fields():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        description={
            "conditions_exercice": "Télétravail possible",
            "descriptif_service": "Service des ressources humaines",
        },
        publication={
            "fin_publication": datetime(2026, 12, 31, tzinfo=timezone.utc),
            "fin_candidature": datetime(2026, 11, 30, tzinfo=timezone.utc),
            "debut_vacance_poste": datetime(2027, 1, 1, tzinfo=timezone.utc),
        },
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.exercise_conditions == "Télétravail possible"
    assert offer.service_description == "Service des ressources humaines"
    assert offer.end_publication_date == datetime(2026, 12, 31, tzinfo=timezone.utc)
    assert offer.application_deadline == datetime(2026, 11, 30, tzinfo=timezone.utc)
    assert offer.job_vacancy_date == datetime(2027, 1, 1, tzinfo=timezone.utc)


def test_offer_input_mapper_maps_blank_or_absent_export_unif_fields_to_none():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        description={"employeur": "", "conditions_exercice": ""},
    )
    del payload["description"]["descriptif_service"]

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.employer is None
    assert offer.exercise_conditions is None
    assert offer.service_description is None
    assert offer.application_deadline is None
    assert offer.job_vacancy_date is None


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

    def test_organisation_is_mapped_from_talentsoft_organisme(self):
        talentsoft_organisme = TalentsoftOrganisme(
            entity_code="ENT-1",
            code=1,
            name="Commune de Paris",
            description="Description de la commune",
            url="https://paris.fr",
            phone_number="0102030405",
            post_code="75001",
            latitude=48.8566,
            longitude=2.3522,
            parent_name="Métropole du Grand Paris",
            logo_url="https://paris.fr/logo.png",
            max_delay_for_consent=30,
            retention_period=24,
            general_conditions="Conditions générales",
            personal_data_consent="Consentement",
        )

        offer = replace(
            OfferFactory.create_entity(), talentsoft_organisme=talentsoft_organisme
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["organisation"] == {
            "entityCode": "ENT-1",
            "name": "Commune de Paris",
            "description": "Description de la commune",
            "url": "https://paris.fr",
            "phoneNumber": "0102030405",
            "postCode": "75001",
            "geolocation": {"latitude": 48.8566, "longitude": 2.3522},
            "parentName": "Métropole du Grand Paris",
            "logoUrl": "https://paris.fr/logo.png",
            "maxDelayForConsent": 30,
            "retentionPeriod": 24,
            "generalConditions": "Conditions générales",
            "personalDataConsent": "Consentement",
        }

    def test_organisation_geolocation_is_none_without_talentsoft_coordinates(self):
        talentsoft_organisme = TalentsoftOrganisme(
            entity_code="ENT-1", code=1, name="Commune de Paris"
        )

        offer = replace(
            OfferFactory.create_entity(), talentsoft_organisme=talentsoft_organisme
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["organisation"]["geolocation"] is None

    def test_organisation_is_null_without_talentsoft_organisme(self):
        offer = OfferFactory.create_entity()

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["organisation"] == {}

    def test_application_email_is_mapped_to_origin_short_text1(self):
        offer = replace(
            OfferFactory.create_entity(), application_email="rh@exemple.gouv.fr"
        )

        result = OfferDetailOutputMapper().to_dict(offer)

        assert result["customFields"]["origin"]["shortText1"] == "rh@exemple.gouv.fr"
        assert result["applicationUrl"] is None
        assert result["urlRedirectionApplicant"] is None

    def test_custom_field_descriptions_are_rendered_in_html(self):
        offer = replace(
            OfferFactory.create_entity(),
            employer="**Employeur**",
            exercise_conditions="- télétravail",
            service_description="## Service RH",
            complements="[Site](https://exemple.gouv.fr)",
        )

        custom_fields = OfferDetailOutputMapper().to_dict(offer)["customFields"]

        assert custom_fields["description"]["longText1"] == "**Employeur**"
        assert custom_fields["description"]["longText2"] == "- télétravail"
        assert custom_fields["description"]["longText3"] == "## Service RH"
        assert custom_fields["offerCustomBlock1"]["longText1"] == (
            "[Site](https://exemple.gouv.fr)"
        )
        assert custom_fields["description"]["longText1Formatted"] == (
            "<p><strong>Employeur</strong></p>"
        )
        assert custom_fields["description"]["longText2Formatted"] == (
            "<ul>\n<li>télétravail</li>\n</ul>"
        )
        assert custom_fields["description"]["longText3Formatted"] == (
            "<p><strong>Service RH</strong></p>"
        )
        assert custom_fields["offerCustomBlock1"]["longText1Formatted"] == (
            '<p><a href="https://exemple.gouv.fr" target="_blank" '
            'rel="noopener noreferrer">Site</a></p>'
        )

    def test_fields_without_offer_equivalent_are_null(self):
        custom_fields = OfferDetailOutputMapper().to_dict(OfferFactory.create_entity())[
            "customFields"
        ]

        assert custom_fields["offerCustomBlock1"]["longText3Formatted"] is None

    def test_bases_legales_are_mapped_to_offer_custom_block(self):
        offer = replace(
            OfferFactory.create_entity(),
            conditions={"bases_legales": "Ouvert :\n\n- 1° aux fonctionnaires"},
        )

        offer_custom_block = OfferDetailOutputMapper().to_dict(offer)["customFields"][
            "offerCustomBlock1"
        ]

        assert offer_custom_block["longText2"] == "Ouvert :\n\n- 1° aux fonctionnaires"
        assert offer_custom_block["longText2Formatted"] == (
            "<p>Ouvert :</p>\n<ul>\n<li>1° aux fonctionnaires</li>\n</ul>"
        )

    @pytest.mark.parametrize("conditions", [None, {}, {"bases_legales": ""}])
    def test_bases_legales_are_null_when_missing(self, conditions):
        offer = replace(OfferFactory.create_entity(), conditions=conditions)

        offer_custom_block = OfferDetailOutputMapper().to_dict(offer)["customFields"][
            "offerCustomBlock1"
        ]

        assert offer_custom_block["longText2"] is None
        assert offer_custom_block["longText2Formatted"] is None

    def test_competences_requises_are_mapped_to_applicant_criteria(self):
        offer = replace(
            OfferFactory.create_entity(),
            criteria=OfferCriteria(competences_requises="- Rigueur\n- Autonomie"),
        )

        applicant_criteria = OfferDetailOutputMapper().to_dict(offer)["customFields"][
            "applicantCriteria"
        ]

        assert applicant_criteria["longText1"] == "- Rigueur\n- Autonomie"
        assert applicant_criteria["longText1Formatted"] == (
            "<ul>\n<li>Rigueur</li>\n<li>Autonomie</li>\n</ul>"
        )

    def test_competences_requises_are_null_without_criteria(self):
        offer = replace(OfferFactory.create_entity(), criteria=None)

        applicant_criteria = OfferDetailOutputMapper().to_dict(offer)["customFields"][
            "applicantCriteria"
        ]

        assert applicant_criteria["longText1"] is None
        assert applicant_criteria["longText1Formatted"] is None

    def test_empty_custom_field_descriptions_are_null(self):
        offer = replace(
            OfferFactory.create_entity(),
            employer=None,
            exercise_conditions=None,
            service_description=None,
            complements=None,
        )

        custom_fields = OfferDetailOutputMapper().to_dict(offer)["customFields"]

        assert custom_fields["description"]["longText1Formatted"] is None
        assert custom_fields["description"]["longText2Formatted"] is None
        assert custom_fields["description"]["longText3Formatted"] is None
        assert custom_fields["offerCustomBlock1"]["longText1Formatted"] is None

    @pytest.mark.parametrize(
        "documents,client_code,label",
        [
            (
                [RequiredDocument.CV],
                "Doc_CV",
                "L'envoi du CV est obligatoire",
            ),
            (
                [RequiredDocument.LETTRE_MOTIVATION, RequiredDocument.CV],
                "Doc_CV_LM",
                "L'envoi du CV et d'une lettre de motivation est obligatoire",
            ),
            (
                [RequiredDocument.CV, RequiredDocument.PORTFOLIO],
                "Doc_CV_PF",
                "L'envoi du CV et d'un portfolio est obligatoire",
            ),
            (
                [
                    RequiredDocument.CV,
                    RequiredDocument.LETTRE_MOTIVATION,
                    RequiredDocument.PORTFOLIO,
                ],
                "Doc_CV_LM_PF",
                (
                    "L'envoi du CV, d'une lettre de motivation et d'un portfolio est "
                    "obligatoire"
                ),
            ),
        ],
        ids=["cv", "cv-lm-in-any-order", "cv-pf", "cv-lm-pf"],
    )
    def test_required_documents_are_mapped_to_talentsoft_value(
        self, documents, client_code, label
    ):
        offer = OfferFactory.create_entity(
            criteria=OfferCriteria(documents_requis=documents)
        )

        custom_fields = OfferDetailOutputMapper().to_dict(offer)["customFields"]

        assert custom_fields["applicantCriteria"]["customCodeTable1"] == {
            "code": None,
            "clientCode": client_code,
            "label": label,
            "active": True,
            "parentCode": None,
            "type": "Documents à transmettre",
            "parentType": "",
            "hasChildren": False,
        }

    @pytest.mark.parametrize(
        "criteria",
        [
            None,
            OfferCriteria(),
            OfferCriteria(documents_requis=[RequiredDocument.LETTRE_MOTIVATION]),
            OfferCriteria(
                documents_requis=[
                    RequiredDocument.LETTRE_MOTIVATION,
                    RequiredDocument.PORTFOLIO,
                ]
            ),
        ],
        ids=["no-criteria", "no-documents", "lm-without-cv", "lm-pf-without-cv"],
    )
    def test_required_documents_without_talentsoft_value_are_null(self, criteria):
        offer = OfferFactory.create_entity(criteria=criteria)

        custom_fields = OfferDetailOutputMapper().to_dict(offer)["customFields"]

        assert custom_fields["applicantCriteria"]["customCodeTable1"] is None
