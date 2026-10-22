from datetime import datetime, timezone
from uuid import UUID

import pytest
from pydantic import HttpUrl, ValidationError
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language import Language
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.offer_conditions import (
    JobVacancy,
    Management,
    WorkingPlace,
    WorkingTime,
)
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse

from domain.entities.raw_offer import RawOffer
from domain.value_objects.contact import Contact, ContactRole
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftDynamicField,
    TalentsoftLanguage,
)
from infrastructure.gateways.offers_cleaner import OffersCleaner
from infrastructure.gateways.transcoding import SourceTranscoder
from infrastructure.sources_repository import SourcesRepository
from tests.factories.domain_factories import SourceFactory
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftCustomCodeTableFactory,
    TalentsoftCustomFieldsFactory,
    TalentsoftDetailOfferFactory,
    TalentsoftDynamicFieldFactory,
    TalentsoftGeolocationFactory,
    TalentsoftOrganisationFactory,
)

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"
OTHER_SOURCE_ID = "99999999-8888-7777-6666-555555555555"
_SOURCE_ID_BY_SLUG = {"ars": SOURCE_ID, "talentsoft-main": OTHER_SOURCE_ID}


@pytest.fixture
def sources_repository() -> SourcesRepository:
    repository = SourcesRepository()
    repository.load(
        [
            SourceFactory.build(
                source_id=UUID(SOURCE_ID),
                slug="ars",
                client_id_front="ars-front",
                client_id_back="ars-back",
                base_url_front="https://ars.example.com",
                base_url_back="https://ars.example.com",
            ),
            SourceFactory.build(
                source_id=UUID(OTHER_SOURCE_ID),
                slug="talentsoft-main",
                client_id_front="main-front",
                client_id_back="main-back",
                base_url_front="https://main.example.com",
                base_url_back="https://main.example.com",
            ),
        ]
    )
    return repository


@pytest.fixture
def cleaner(sources_repository: SourcesRepository) -> OffersCleaner:
    return OffersCleaner(sources_repository=sources_repository)


def _make_raw_offer(
    reference: str = REFERENCE, slug: str = "ars", **offer_kwargs
) -> RawOffer:
    offer_dto = TalentsoftDetailOfferFactory.build(reference=reference, **offer_kwargs)
    return RawOffer(
        reference=reference,
        source_id=_SOURCE_ID_BY_SLUG[slug],
        data=offer_dto.model_dump(),
    )


def test_clean_returns_offer_with_correct_reference(cleaner):
    raw_offer = _make_raw_offer()

    offer = cleaner.clean(raw_offer)

    assert REFERENCE in offer.external_id


def test_clean_raises_when_no_data(cleaner):
    raw_offer = RawOffer(reference=REFERENCE, source_id=SOURCE_ID, data=None)

    with pytest.raises(ValueError, match="no data"):
        cleaner.clean(raw_offer)


def test_clean_raises_on_invalid_data(cleaner):
    raw_offer = RawOffer(
        reference=REFERENCE, source_id=SOURCE_ID, data={"invalid": "data"}
    )

    with pytest.raises(ValidationError):
        cleaner.clean(raw_offer)


@pytest.mark.parametrize(
    "salary_range_client_code, expected_verse",
    [
        ("Versant_FPT", Verse.FPT),
        ("Versant_FPH", Verse.FPH),
        ("Versant_FPE", Verse.FPE),
        ("_TS_CO_SalaryRange_FPE", Verse.FPE),
        (None, None),
    ],
)
def test_clean_maps_verse_from_salary_range(
    cleaner, salary_range_client_code, expected_verse
):
    salary_range = (
        TalentsoftCodedObjectFactory.build(clientCode=salary_range_client_code)
        if salary_range_client_code
        else None
    )
    raw_offer = _make_raw_offer(salaryRange=salary_range)

    offer = cleaner.clean(raw_offer)

    assert offer.verse == expected_verse


def test_clean_maps_verse_fph_from_aphp_reference(cleaner):
    raw_offer = _make_raw_offer(reference="APHP-2024-001")

    offer = cleaner.clean(raw_offer)

    assert offer.verse == Verse.FPH


@pytest.mark.parametrize("reference", ["MENJ-2024-001", "OFII_2026-271"])
def test_clean_maps_verse_fpe_from_reference(cleaner, reference):
    raw_offer = _make_raw_offer(reference=reference)

    offer = cleaner.clean(raw_offer)

    assert offer.verse == Verse.FPE


@pytest.mark.parametrize(
    "category_code, expected_category",
    [
        ("CAT-AEF", Category.APLUS),
        ("CAT-ESD", Category.APLUS),
        ("CAT-ES", Category.APLUS),
        ("CAT-A", Category.A),
        ("CAT-B", Category.B),
        ("CAT-C", Category.C),
        ("UNKNOWN", None),
    ],
)
def test_clean_maps_category_from_custom_fields(
    cleaner, category_code, expected_category
):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDynamicFieldFactory.build(
                customCodeTable1=TalentsoftCustomCodeTableFactory.build(
                    clientCode=category_code
                )
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.category == expected_category


@pytest.mark.parametrize(
    "area, country, region, department, "
    "expected_area, expected_region, expected_department",
    [
        (
            "_TS_CO_GeographicalArea_Europe",
            "FRA",
            "R24",
            "41",
            "EU",
            "24",
            "41",
        ),
        (
            "_TS_CO_GeographicalArea_Europe",
            "FRA",
            "R11",
            "75",
            "EU",
            "11",
            "75",
        ),
        (
            "_TS_CO_GeographicalArea_Afrique",
            "FRA",
            "_TS_CO_Region_DOM",
            "971",
            "AF",
            "DOM",
            "971",
        ),
        (
            "_TS_CO_GeographicalArea_AmriquesCaraibe",
            "FRA",
            "_TS_CO_Region_TOM",
            "987",
            "AM",
            "TOM",
            "987",
        ),
        (
            "_TS_CO_GeographicalArea_Ocanie",
            "FRA",
            "R84",
            "_TS_CO_Department_NouvelleCaldonie988",
            "OC",
            "84",
            "988",
        ),
        (
            "_TS_CO_GeographicalArea_MoyenOrientAfriqueduNord",
            "FRA",
            "R11",
            "75",
            "MO",
            "11",
            "75",
        ),
    ],
)
def test_clean_maps_geographical_area(
    cleaner,
    area,
    country,
    region,
    department,
    expected_area,
    expected_region,
    expected_department,
):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode=area, type="offerGeographicalLocation"
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode=country, type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode=region, type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(
                clientCode=department, type="offerDepartment"
            )
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.area.value == expected_area
    assert offer.localisation.region.code == expected_region
    assert offer.localisation.department.code == expected_department


def test_clean_maps_ars_raw_country_region_and_department_codes(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_Country_France", type="offerCountry"
            )
        ],
        region=[
            TalentsoftCodedObjectFactory.build(
                clientCode="ARS_CO_Region_Bretagne", type="offerRegion"
            )
        ],
        department=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_Department_IlleetVilaine35",
                type="offerDepartment",
            )
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert str(offer.localisation.country) == "FRA"
    assert offer.localisation.region.code == "53"
    assert offer.localisation.department.code == "35"


def test_clean_maps_ars_overseas_region_code(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Afrique",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(
                clientCode="ARS_CO_Region_Guadeloupe", type="offerRegion"
            )
        ],
        department=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_Department_Guadeloupe971",
                type="offerDepartment",
            )
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.region.code == "DOM"
    assert offer.localisation.department.code == "971"


def test_clean_returns_none_localisation_when_area_missing(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode="R24", type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="41", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is None


def test_clean_maps_title_and_organization(cleaner):
    offer_dto = TalentsoftDetailOfferFactory.build(
        reference=REFERENCE,
        title="INGÉNIEUR LOGICIEL",
        organisationName="Mairie de Paris",
    )
    raw_offer = RawOffer(
        reference=REFERENCE, source_id=SOURCE_ID, data=offer_dto.model_dump()
    )

    offer = cleaner.clean(raw_offer)

    assert offer.title == "INGÉNIEUR LOGICIEL"
    assert offer.organization == "Mairie de Paris"


def test_clean_external_id_uses_salary_range_client_code_as_prefix(cleaner):
    salary_range = TalentsoftCodedObjectFactory.build(clientCode="Versant_FPT")
    raw_offer = _make_raw_offer(reference=REFERENCE, salaryRange=salary_range)

    offer = cleaner.clean(raw_offer)

    assert offer.external_id == f"Versant_FPT-{REFERENCE}"


@pytest.mark.parametrize(
    "contract_code, expected",
    [
        ("TITULAIRE_CODE", OfferNature.TITULAIRE_CONTRACTUEL),
        ("CONTRACTUEL_CDD", OfferNature.CONTRACTUEL),
        ("TERRITORIAL_TIT", OfferNature.TERRITORIAL),
        ("UNKNOWN_TYPE", None),
        (None, None),
        ("ACCOMP", OfferNature.CONTRACTUEL),
        ("ACCOMPCDI", OfferNature.TITULAIRE_CONTRACTUEL),
        ("APP7", OfferNature.CONTRACTUEL),
        ("APPCDD", OfferNature.CONTRACTUEL),
        ("APPREN", OfferNature.CONTRACTUEL),
        ("AUTCDD", OfferNature.CONTRACTUEL),
        ("CCNCDINE", OfferNature.TITULAIRE_CONTRACTUEL),
        ("CDI", OfferNature.TITULAIRE_CONTRACTUEL),
        ("CES", OfferNature.CONTRACTUEL),
        ("CONTRCDD", OfferNature.CONTRACTUEL),
        ("CUICDD", OfferNature.CONTRACTUEL),
        ("GRH", OfferNature.CONTRACTUEL),
        ("PROCDD", OfferNature.CONTRACTUEL),
        ("REMPLA", OfferNature.CONTRACTUEL),
        ("RENOIRH", OfferNature.CONTRACTUEL),
        ("STA", OfferNature.CONTRACTUEL),
        ("STAGE", OfferNature.CONTRACTUEL),
        ("SURCHA", OfferNature.CONTRACTUEL),
        ("TC01", OfferNature.CONTRACTUEL),
        ("TC02", OfferNature.TITULAIRE_CONTRACTUEL),
        ("TITULAIRE FONCTION PUBLIQUE", OfferNature.TITULAIRE_CONTRACTUEL),
        (
            "TITULAIRE FONCTION PUBLIQUE / UCANSS",
            OfferNature.TITULAIRE_CONTRACTUEL,
        ),
        ("TITULAIRE UCANSS", OfferNature.CONTRACTUEL),
        # "TC21" is present in the ARS transcoding table but has no
        # DGAFP mapping configured; the untranscoded heuristic can't
        # match it either, so it should resolve to None rather than
        # raise.
        ("TC21", None),
    ],
)
def test_clean_maps_offer_nature(cleaner, contract_code, expected):

    offer_nature = (
        TalentsoftCodedObjectFactory.build(clientCode=contract_code)
        if contract_code
        else None
    )
    raw_offer = _make_raw_offer(contractType=offer_nature)

    offer = cleaner.clean(raw_offer)

    assert offer.offer_nature == expected


def test_clean_raises_when_offer_nature_csv_maps_to_unknown_code(
    sources_repository,
):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={"types_de_contrat": {"TC02": "NOT_A_REAL_CONTRACT_TYPE"}}
            )
        },
    )
    raw_offer = _make_raw_offer(
        contractType=TalentsoftCodedObjectFactory.build(clientCode="TC02")
    )

    with pytest.raises(ValueError, match="NOT_A_REAL_CONTRACT_TYPE"):
        cleaner.clean(raw_offer)


@pytest.mark.parametrize(
    "contract_kind_code, expected",
    [
        ("CDD_1A", ContractKind.CDD),
        ("CDD_2A", ContractKind.CDD),
        ("CDD_3A", ContractKind.CDD),
        ("CDD_6M", ContractKind.CDD),
        ("CDI", ContractKind.CDI),
        ("STAGE", None),
        ("UNKNOWN_KIND", None),
        (None, None),
    ],
)
def test_clean_maps_contract_kind(cleaner, contract_kind_code, expected):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            offer=TalentsoftDynamicField(
                customCodeTable2=TalentsoftCustomCodeTableFactory.build(
                    clientCode=contract_kind_code
                )
                if contract_kind_code
                else None
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.contract_kind == expected


@pytest.mark.parametrize(
    "working_place_code, expected",
    [
        ("reponse_oui", WorkingPlace.TELETRAVAIL),
        ("reponse_non", WorkingPlace.SUR_SITE),
        ("UNKNOWN_CODE", WorkingPlace.NON_DEFINI),
        (None, WorkingPlace.NON_DEFINI),
    ],
)
def test_clean_maps_working_place(cleaner, working_place_code, expected):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            offerCustomBlock1=TalentsoftDynamicField(
                customCodeTable2=TalentsoftCustomCodeTableFactory.build(
                    clientCode=working_place_code
                )
                if working_place_code
                else None
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.working_place == expected


@pytest.mark.parametrize(
    "working_time_code, expected",
    [
        ("reponse_oui", WorkingTime.TEMPS_PLEIN),
        ("reponse_non", WorkingTime.TEMPS_PARTIEL),
        ("UNKNOWN_CODE", WorkingTime.NON_DEFINI),
        (None, WorkingTime.NON_DEFINI),
    ],
)
def test_clean_maps_working_time(cleaner, working_time_code, expected):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDynamicFieldFactory.build(
                customCodeTable3=TalentsoftCustomCodeTableFactory.build(
                    clientCode=working_time_code
                )
                if working_time_code
                else None
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.working_time == expected


@pytest.mark.parametrize(
    "management_code, expected",
    [
        ("reponse_oui", Management.AVEC),
        ("reponse_non", Management.SANS),
        ("UNKNOWN_CODE", None),
        (None, None),
    ],
)
def test_clean_maps_management(cleaner, management_code, expected):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            offerCustomBlock1=TalentsoftDynamicField(
                customCodeTable1=TalentsoftCustomCodeTableFactory.build(
                    clientCode=management_code
                )
                if management_code
                else None
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.management == expected


@pytest.mark.parametrize(
    "professional_category_code, expected",
    [
        ("STATUT01", JobVacancy.OUI),
        ("STATUT02", JobVacancy.NON),
        ("_TS_CO_ProfessionalCategory_Cadre", None),
        (None, None),
    ],
)
def test_clean_maps_job_vacancy(cleaner, professional_category_code, expected):
    raw_offer = _make_raw_offer(
        professionalCategory=TalentsoftCodedObjectFactory.build(
            clientCode=professional_category_code
        )
        if professional_category_code
        else None
    )

    offer = cleaner.clean(raw_offer)

    assert offer.job_vacancy == expected


def test_clean_returns_none_url_on_invalid_offer_url(cleaner):
    raw_offer = _make_raw_offer(offerUrl="not-a-valid-url")

    offer = cleaner.clean(raw_offer)

    assert offer.offer_url is None


def test_clean_maps_application_url(cleaner):
    raw_offer = _make_raw_offer(applicationUrl="https://apply.example.com/job/123")

    offer = cleaner.clean(raw_offer)

    assert str(offer.application_url) == "https://apply.example.com/job/123"


def test_clean_returns_none_application_url_when_absent(cleaner):
    raw_offer = _make_raw_offer(applicationUrl=None)

    offer = cleaner.clean(raw_offer)

    assert offer.application_url is None


def test_clean_returns_none_beginning_date_on_invalid_format(cleaner):
    raw_offer = _make_raw_offer(beginningDate="not-a-date")

    offer = cleaner.clean(raw_offer)

    assert offer.beginning_date is None


def test_clean_returns_none_beginning_date_when_absent(cleaner):
    raw_offer = _make_raw_offer(beginningDate=None)

    offer = cleaner.clean(raw_offer)

    assert offer.beginning_date is None


def test_clean_maps_end_publication_date(cleaner):
    raw_offer = _make_raw_offer(endPublicationDate="2025-06-30T00:00:00Z")

    offer = cleaner.clean(raw_offer)

    assert offer.end_publication_date == datetime(2025, 6, 30, tzinfo=timezone.utc)


def test_clean_returns_none_end_publication_date_when_absent(cleaner):
    raw_offer = _make_raw_offer(endPublicationDate=None)

    offer = cleaner.clean(raw_offer)

    assert offer.end_publication_date is None


@pytest.mark.parametrize(
    "client_code, expected",
    [
        ("A", 1),
        ("B", 2),
        ("C", 3),
        ("D", 4),
        ("E", 5),
        ("F", 6),
        ("G", 7),
        ("H", 8),
        ("NIV_DIPL1", 1),
        ("NIV_DIPL6", 6),
        ("NIV_DIPL7", 6),
        ("NIV_DIPL8", 7),
        ("NIV_DIPL9", 8),
    ],
)
def test_clean_maps_education_level(cleaner, client_code, expected):
    education = TalentsoftCodedObjectFactory.build(clientCode=client_code)
    raw_offer = _make_raw_offer(educationLevel=education)

    offer = cleaner.clean(raw_offer)

    assert offer.education_level == expected


@pytest.mark.parametrize("client_code", ["UNKNOWN_CODE", "NIV_DIPL0", "NIV_DIPL10"])
def test_clean_maps_unknown_education_level_to_none(cleaner, client_code):
    education = TalentsoftCodedObjectFactory.build(clientCode=client_code)
    raw_offer = _make_raw_offer(educationLevel=education)

    offer = cleaner.clean(raw_offer)

    assert offer.education_level is None


def test_clean_returns_none_education_level_when_absent(cleaner):
    raw_offer = _make_raw_offer(educationLevel=None)

    offer = cleaner.clean(raw_offer)

    assert offer.education_level is None


@pytest.mark.parametrize(
    "client_code, expected",
    [
        ("_TS_CO_ExperienceLevel_Nonrenseign", None),
        ("debutant", ExperienceLevel.DEBUTANT),
        ("confirme", ExperienceLevel.CONFIRME),
        ("expert", ExperienceLevel.EXPERT),
        ("_TS_CO_ExperienceLevel_jeunediplm", ExperienceLevel.DEBUTANT),
        ("_TS_CO_ExperienceLevel_1anouplus", ExperienceLevel.DEBUTANT),
        ("_TS_CO_ExperienceLevel_3ansouplus", ExperienceLevel.CONFIRME),
        ("_TS_CO_ExperienceLevel_6ansouplus", ExperienceLevel.EXPERT),
        ("UNKNOWN_CODE", None),
    ],
)
def test_clean_maps_experience(cleaner, client_code, expected):
    experience = TalentsoftCodedObjectFactory.build(clientCode=client_code)
    raw_offer = _make_raw_offer(experienceLevel=experience)

    offer = cleaner.clean(raw_offer)

    assert offer.experience == expected


def test_clean_returns_none_experience_when_absent(cleaner):
    raw_offer = _make_raw_offer(experienceLevel=None)

    offer = cleaner.clean(raw_offer)

    assert offer.experience is None


def test_clean_raises_when_experience_levels_csv_maps_to_unknown_code(
    sources_repository,
):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={
                    "niveaux_d_experience": {"debutant": "NOT_A_REAL_EXPERIENCE_LEVEL"}
                }
            )
        },
    )
    raw_offer = _make_raw_offer(
        experienceLevel=TalentsoftCodedObjectFactory.build(clientCode="debutant")
    )

    with pytest.raises(ValueError, match="NOT_A_REAL_EXPERIENCE_LEVEL"):
        cleaner.clean(raw_offer)


def test_clean_raises_when_niveaux_de_diplome_csv_maps_to_unknown_code(
    sources_repository,
):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={"niveaux_de_diplome": {"NIV_DIPL1": "NOT_A_REAL_LEVEL"}}
            )
        },
    )
    raw_offer = _make_raw_offer(
        educationLevel=TalentsoftCodedObjectFactory.build(clientCode="NIV_DIPL1")
    )

    with pytest.raises(ValueError, match="NOT_A_REAL_LEVEL"):
        cleaner.clean(raw_offer)


def test_clean_maps_specialisations(cleaner):
    raw_offer = _make_raw_offer(
        specialisations=[
            TalentsoftCodedObjectFactory.build(clientCode="_TS_CO_Specialisation_1"),
            TalentsoftCodedObjectFactory.build(clientCode="_TS_CO_Specialisation_2"),
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == [
        "Formations générales",
        "Spécialités pluriscientifiques",
    ]


def test_clean_skips_specialisation_with_unmapped_code(cleaner):
    raw_offer = _make_raw_offer(
        specialisations=[
            TalentsoftCodedObjectFactory.build(clientCode="UNKNOWN_CODE"),
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == []


def test_clean_returns_empty_specialisations_when_absent(cleaner):
    raw_offer = _make_raw_offer(specialisations=[])

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == []


def test_clean_translates_specialisations_via_source_transcoder(sources_repository):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={"specialisations": {"RAW_SPEC": "_TS_CO_Specialisation_1"}}
            )
        },
    )
    raw_offer = _make_raw_offer(
        specialisations=[TalentsoftCodedObjectFactory.build(clientCode="RAW_SPEC")]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == ["Formations générales"]


def test_clean_raises_when_specialisations_csv_maps_to_unknown_code(
    sources_repository,
):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={"specialisations": {"RAW_SPEC": "NOT_A_REAL_SPECIALISATION"}}
            )
        },
    )
    raw_offer = _make_raw_offer(
        specialisations=[TalentsoftCodedObjectFactory.build(clientCode="RAW_SPEC")]
    )

    with pytest.raises(ValueError, match="NOT_A_REAL_SPECIALISATION"):
        cleaner.clean(raw_offer)


def test_clean_maps_diploma(cleaner):
    diploma = TalentsoftCodedObjectFactory.build(clientCode="LICENCE")
    raw_offer = _make_raw_offer(diploma=diploma)

    offer = cleaner.clean(raw_offer)

    assert offer.diploma == "LICENCE"


def test_clean_returns_none_diploma_when_absent(cleaner):
    raw_offer = _make_raw_offer(diploma=None)

    offer = cleaner.clean(raw_offer)

    assert offer.diploma is None


def test_clean_maps_ars_raw_family_code_to_metier_code(cleaner):
    raw_offer = _make_raw_offer(
        offerFamilyCategory=TalentsoftCodedObjectFactory.build(clientCode="TCOM000012")
    )

    offer = cleaner.clean(raw_offer)

    assert offer.family_code == "ERDOC010"


def test_clean_keeps_unmapped_family_code_as_is(cleaner):
    raw_offer = _make_raw_offer(
        offerFamilyCategory=TalentsoftCodedObjectFactory.build(
            clientCode="UNKNOWN_METIER"
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.family_code == "UNKNOWN_METIER"


def test_clean_maps_languages(cleaner):
    raw_offer = _make_raw_offer(
        languages=[
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="EN"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="B2"),
            )
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.languages == [Language(iso_code="EN", language_level=LanguageLevel.B2)]


def test_clean_returns_empty_languages_when_absent(cleaner):
    raw_offer = _make_raw_offer(languages=[])

    offer = cleaner.clean(raw_offer)

    assert offer.languages == []


def test_clean_maps_ars_raw_language_level(cleaner):
    raw_offer = _make_raw_offer(
        languages=[
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="EN"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="LANG4"),
            )
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.languages == [Language(iso_code="EN", language_level=LanguageLevel.B2)]


def test_clean_skips_language_with_unmapped_level(cleaner):
    raw_offer = _make_raw_offer(
        languages=[
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="EN"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="LANG0"),
            ),
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="FR"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="LANG5"),
            ),
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.languages == [Language(iso_code="FR", language_level=LanguageLevel.C1)]


def test_clean_raises_when_niveaux_de_langue_csv_maps_to_unknown_code(
    sources_repository,
):
    cleaner = OffersCleaner(
        sources_repository=sources_repository,
        transcoders_by_slug={
            "ars": SourceTranscoder(
                tables={"niveaux_de_langue": {"LANG4": "NOT_A_REAL_LANGUAGE_LEVEL"}}
            )
        },
    )
    raw_offer = _make_raw_offer(
        languages=[
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="EN"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="LANG4"),
            )
        ]
    )

    with pytest.raises(ValueError, match="NOT_A_REAL_LANGUAGE_LEVEL"):
        cleaner.clean(raw_offer)


def test_clean_maps_raw_region_code_without_prefix(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode="11", type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="75", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.region.code == "11"


def _valid_localisation_kwargs() -> dict:
    return {
        "geographicalLocation": [
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        "country": [
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        "region": [
            TalentsoftCodedObjectFactory.build(clientCode="R24", type="offerRegion")
        ],
        "department": [
            TalentsoftCodedObjectFactory.build(clientCode="41", type="offerDepartment")
        ],
    }


def test_clean_maps_coordinates_from_offer_geolocation(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        geolocation=TalentsoftGeolocationFactory.build(latitude=48.85, longitude=2.35),
        latitude=None,
        longitude=None,
        organisation=TalentsoftOrganisationFactory.build(geolocation=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.latitude == 48.85
    assert offer.localisation.longitude == 2.35


def test_clean_maps_coordinates_from_flat_fields_when_geolocation_absent(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        geolocation=None,
        latitude=45.75,
        longitude=4.85,
        organisation=TalentsoftOrganisationFactory.build(geolocation=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.latitude == 45.75
    assert offer.localisation.longitude == 4.85


def test_clean_prefers_offer_geolocation_over_flat_fields(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        geolocation=TalentsoftGeolocationFactory.build(latitude=48.85, longitude=2.35),
        latitude=45.75,
        longitude=4.85,
        organisation=TalentsoftOrganisationFactory.build(geolocation=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.latitude == 48.85
    assert offer.localisation.longitude == 2.35


def test_clean_maps_coordinates_from_organisation_geolocation_as_last_resort(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        geolocation=None,
        latitude=None,
        longitude=None,
        organisation=TalentsoftOrganisationFactory.build(
            geolocation=TalentsoftGeolocationFactory.build(
                latitude=43.29, longitude=5.37
            )
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.latitude == 43.29
    assert offer.localisation.longitude == 5.37


def test_clean_returns_none_coordinates_when_no_source_available(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        geolocation=None,
        latitude=None,
        longitude=None,
        organisation=TalentsoftOrganisationFactory.build(geolocation=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.latitude is None
    assert offer.localisation.longitude is None


def test_clean_ars_offer_nature_transcoding_is_scoped_to_ars_source(cleaner):
    raw_offer = _make_raw_offer(
        slug="talentsoft-main",
        contractType=TalentsoftCodedObjectFactory.build(clientCode="TC02"),
    )

    offer = cleaner.clean(raw_offer)

    # "TC02" is an ARS-specific code; without the ARS transcoding table it
    # doesn't match the generic TITULAIRE/CONTRACTUEL/TERRITORIAL fallback.
    assert offer.offer_nature is None


def test_clean_returns_none_localisation_on_invalid_region_code(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(
                clientCode="INVALID_REGION", type="offerRegion"
            )
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="75", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is None


def test_clean_maps_talentsoft_organisme_entity_code_from_organisation(cleaner):
    raw_offer = _make_raw_offer(
        organisation=TalentsoftOrganisationFactory.build(entityCode="12345"),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.talentsoft_organisme_entity_code == "12345"


@pytest.mark.parametrize(
    "entity_code, expected",
    [
        ("011A270001", "735"),
        ("011A440001", "_TS_424e953f-150e-47d3-9c17-95f4da4793c7"),
        ("PPC2A38EFDE-D61B-4ED6-9354-9A1314EA0B6F", "741"),
    ],
)
def test_clean_transcodes_talentsoft_organisme_entity_code(
    cleaner, entity_code, expected
):
    raw_offer = _make_raw_offer(
        organisation=TalentsoftOrganisationFactory.build(entityCode=entity_code),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.talentsoft_organisme_entity_code == expected


def test_clean_raises_when_no_organisation(cleaner):
    raw_offer = _make_raw_offer(organisation=None)

    with pytest.raises(ValueError, match="has no organisation"):
        cleaner.clean(raw_offer)


def test_clean_prefers_url_redirection_applicant_as_application_url(cleaner):
    raw_offer = _make_raw_offer(
        urlRedirectionApplicant="https://redirect.example.com/job/123",
        applicationUrl="https://apply.example.com/job/123",
        customFields=TalentsoftCustomFieldsFactory.build(
            origin=TalentsoftDynamicField(shortText1="candidature@exemple.gouv.fr")
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert str(offer.application_url) == "https://redirect.example.com/job/123"
    assert offer.application_email is None


def test_clean_prefers_application_email_over_application_url(cleaner):
    raw_offer = _make_raw_offer(
        urlRedirectionApplicant=None,
        applicationUrl="https://apply.example.com/job/123",
        customFields=TalentsoftCustomFieldsFactory.build(
            origin=TalentsoftDynamicField(
                shortText1="Madame la Directrice ; rh@exemple.gouv.fr, dg@exemple.fr"
            )
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.application_email == "rh@exemple.gouv.fr"
    assert offer.application_url is None


@pytest.mark.parametrize(
    "short_text_1",
    [None, "", "Madame la Directrice", "recrutement@chu-clermont ferrand.fr"],
)
def test_clean_falls_back_to_application_url_without_redirection_nor_email(
    cleaner, short_text_1
):
    raw_offer = _make_raw_offer(
        urlRedirectionApplicant=None,
        applicationUrl="https://apply.example.com/job/123",
        customFields=TalentsoftCustomFieldsFactory.build(
            origin=TalentsoftDynamicField(shortText1=short_text_1)
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert str(offer.application_url) == "https://apply.example.com/job/123"
    assert offer.application_email is None


def test_clean_returns_no_application_channel_when_all_absent(cleaner):
    raw_offer = _make_raw_offer(
        urlRedirectionApplicant=None,
        applicationUrl=None,
        customFields=TalentsoftCustomFieldsFactory.build(origin=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.application_url is None
    assert offer.application_email is None


def test_clean_maps_contract_duration(cleaner):
    raw_offer = _make_raw_offer(contractDuration="12 mois")

    offer = cleaner.clean(raw_offer)

    assert offer.contract_duration == "12 mois"


def test_clean_returns_none_contract_duration_when_absent(cleaner):
    raw_offer = _make_raw_offer(contractDuration=None)

    offer = cleaner.clean(raw_offer)

    assert offer.contract_duration is None


def test_clean_maps_custom_field_texts(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDynamicField(
                longText1="Présentation de l'employeur",
                longText2="Conditions d'exercice",
                longText3="Descriptif du service",
            ),
            offerCustomBlock1=TalentsoftDynamicField(longText1="Compléments"),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.employer_description == "Présentation de l'employeur"
    assert offer.exercise_conditions == "Conditions d'exercice"
    assert offer.service_description == "Descriptif du service"
    assert offer.complements == "Compléments"


def test_clean_returns_empty_custom_field_texts_when_absent(cleaner):
    raw_offer = _make_raw_offer(customFields=None)

    offer = cleaner.clean(raw_offer)

    assert offer.employer_description == ""
    assert offer.exercise_conditions == ""
    assert offer.service_description == ""
    assert offer.complements == ""
    assert offer.application_deadline is None


def test_clean_maps_applicant_criteria_and_offer_block_texts(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            applicantCriteria=TalentsoftDynamicField(
                longText1="  Savoir-faire : Travailler en équipe  "
            ),
            offerCustomBlock1=TalentsoftDynamicField(
                longText2="Art. L332-2 du code général de la fonction publique",
                longText3="https://www.legifrance.gouv.fr/jorf/id/1",
            ),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.required_skills == "Savoir-faire : Travailler en équipe"
    assert offer.legal_basis == "Art. L332-2 du code général de la fonction publique"
    assert offer.vacancy_notice_url == HttpUrl(
        "https://www.legifrance.gouv.fr/jorf/id/1"
    )


def test_clean_keeps_required_skills_as_raw_text(cleaner):
    raw_text = (
        "Savoir-faire :\n"
        "- Travailler en équipe\n"
        "\n"
        "•\tFiabilité, rigueur et ponctualité."
    )
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            applicantCriteria=TalentsoftDynamicField(longText1=raw_text),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.required_skills == raw_text


@pytest.mark.parametrize("value", [None, "", "   "])
def test_clean_returns_empty_applicant_criteria_and_offer_block_texts_when_blank(
    cleaner, value
):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            applicantCriteria=TalentsoftDynamicField(longText1=value),
            offerCustomBlock1=TalentsoftDynamicField(longText2=value, longText3=value),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.required_skills is None
    assert offer.legal_basis is None
    assert offer.vacancy_notice_url is None


@pytest.mark.parametrize(
    "value",
    [
        (
            "L'avis de vacance de cet emploi est publié au Journal Officiel en date "
            "du 25/09/2026 et peut être consulté à l'adresse suivante :"
            "https://www.legifrance.gouv.fr/jorf/id/1"
        ),
        "Avis publié au JO : https://www.legifrance.gouv.fr/jorf/id/1.",
        "http://www.legifrance.gouv.fr/jorf/id/1",
    ],
)
def test_clean_extracts_legifrance_url_from_vacancy_notice_text(cleaner, value):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            offerCustomBlock1=TalentsoftDynamicField(longText3=value),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.vacancy_notice_url == HttpUrl(
        "https://www.legifrance.gouv.fr/jorf/id/1"
    )


@pytest.mark.parametrize(
    "value",
    [
        "JO du 12 mars 2025, texte n° 45",
        "https://univ-reims.nous-recrutons.fr/nos-offres-demploi/",
        "https://legifrance.example.com/jorf/id/1",
    ],
)
def test_clean_ignores_vacancy_notice_that_is_not_a_legifrance_url(cleaner, value):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            offerCustomBlock1=TalentsoftDynamicField(longText3=value),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.vacancy_notice_url is None


def test_clean_ignores_vacancy_notice_when_legifrance_url_is_invalid(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            offerCustomBlock1=TalentsoftDynamicField(
                longText3="https://www.legifrance.gouv.fr/jorf/id/" + "A" * 2100
            ),
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.vacancy_notice_url is None


def test_clean_prefers_formatted_texts_converted_to_markdown(cleaner):
    raw_offer = _make_raw_offer(
        description1="Missions brut",
        description1Formatted="<p><strong>Missions</strong></p><ul><li>Une</li></ul>",
        description2="Profil brut",
        description2Formatted='<p><u style="color: red">Profil</u></p>',
        customFields=TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDynamicField(
                longText1="Employeur brut",
                longText1Formatted=(
                    '<p>Voir <a href="https://www.ac-dijon.fr">le site</a></p>'
                ),
                longText2="Conditions brut",
                longText2Formatted="<p><em>Conditions</em></p>",
                longText3="Service brut",
                longText3Formatted='<p>Service</p><img src="https://x.force.com/a.png">',
            ),
            offerCustomBlock1=TalentsoftDynamicField(
                longText1="Compléments brut",
                longText1Formatted="<p>Ligne 1<br>Ligne 2</p>",
            ),
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.mission == "**Missions**\n\n- Une"
    assert offer.profile == "**Profil**"
    assert offer.employer_description == "Voir [le site](https://www.ac-dijon.fr)"
    assert offer.exercise_conditions == "*Conditions*"
    assert offer.service_description == "Service"
    assert offer.complements == "Ligne 1\\\nLigne 2"


@pytest.mark.parametrize("formatted", [None, "", "<p> </p>", "<p>&nbsp;</p>"])
def test_clean_falls_back_on_raw_texts_when_formatted_is_blank(cleaner, formatted):
    raw_offer = _make_raw_offer(
        description1="Missions brut",
        description1Formatted=formatted,
        description2="Profil brut",
        description2Formatted=formatted,
        customFields=TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDynamicField(
                longText1="Employeur brut",
                longText1Formatted=formatted,
                longText2="Conditions brut",
                longText2Formatted=formatted,
                longText3="Service brut",
                longText3Formatted=formatted,
            ),
            offerCustomBlock1=TalentsoftDynamicField(
                longText1="Compléments brut", longText1Formatted=formatted
            ),
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.mission == "Missions brut"
    assert offer.profile == "Profil brut"
    assert offer.employer_description == "Employeur brut"
    assert offer.exercise_conditions == "Conditions brut"
    assert offer.service_description == "Service brut"
    assert offer.complements == "Compléments brut"


def test_clean_returns_empty_texts_when_formatted_and_raw_are_blank(cleaner):
    raw_offer = _make_raw_offer(
        description1=None,
        description1Formatted="<p> </p>",
        description2=None,
        description2Formatted=None,
    )

    offer = cleaner.clean(raw_offer)

    assert offer.mission == ""
    assert offer.profile == ""


def test_clean_maps_application_deadline(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            offer=TalentsoftDynamicField(date1="2025-06-30T00:00:00Z")
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.application_deadline == datetime(2025, 6, 30, tzinfo=timezone.utc)


def test_clean_returns_none_application_deadline_on_invalid_format(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            offer=TalentsoftDynamicField(date1="not-a-date")
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.application_deadline is None


def test_clean_maps_localisation_label(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        customFields=TalentsoftCustomFieldsFactory.build(
            location=TalentsoftDynamicField(shortText1="Blois (41)")
        ),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.label == "Blois (41)"


def test_clean_returns_none_localisation_label_when_absent(cleaner):
    raw_offer = _make_raw_offer(
        **_valid_localisation_kwargs(),
        customFields=TalentsoftCustomFieldsFactory.build(location=None),
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.label is None


def test_clean_maps_contacts_from_origin(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            origin=TalentsoftDynamicField(
                shortText1="candidature@exemple.gouv.fr",
                shortText2=" Camille Martin : camille.martin@exemple.gouv.fr ",
                shortText3="Service RH",
            )
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.contacts == [
        Contact(
            role=ContactRole.PRINCIPAL,
            text="Camille Martin : camille.martin@exemple.gouv.fr",
            emails=["camille.martin@exemple.gouv.fr"],
        ),
        Contact(role=ContactRole.AUTRE, text="Service RH"),
    ]


def test_clean_ignores_contacts_without_letter_or_digit(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            origin=TalentsoftDynamicField(shortText2=".", shortText3="rh@exemple.fr")
        )
    )

    offer = cleaner.clean(raw_offer)

    assert offer.contacts == [
        Contact(role=ContactRole.AUTRE, text="rh@exemple.fr", emails=["rh@exemple.fr"])
    ]


def test_clean_returns_no_contacts_when_origin_absent(cleaner):
    raw_offer = _make_raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(origin=None)
    )

    offer = cleaner.clean(raw_offer)

    assert offer.contacts == []
