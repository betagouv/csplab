import pytest
from referentiel.value_objects.verse import Verse

from domain.identite.errors.organisme_errors import EtablissementInvalideError
from infrastructure.external_gateways.dtos.finess_dtos import EtablissementDTO
from infrastructure.mappers.organisme_finess_mapper import (
    REFERENTIEL_FINESS,
    OrganismeFinessMapper,
)

LATITUDE = 46.211257
LONGITUDE = 5.254203


@pytest.fixture(name="mapper")
def mapper_fixture():
    return OrganismeFinessMapper()


def _make_dto(**overrides):
    defaults = {
        "nom": "Clinique du Docteur Convert",
        "external_id": "010780195",
        "siret": "77220148900022",
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "departement": "01",
        "millesime": "2026-08-18",
    }
    return EtablissementDTO(**{**defaults, **overrides})


def test_to_domain_builds_organisme_with_localisation(mapper):
    organisme = mapper.to_domain(_make_dto())

    assert organisme.nom == "Clinique du Docteur Convert"
    assert organisme.versant == Verse.FPH
    assert organisme.siret.value == "77220148900022"
    assert organisme.external_id == "010780195"
    assert organisme.referentiel == REFERENTIEL_FINESS
    assert organisme.millesime == "2026-08-18"
    # A freshly imported FINESS etablissement is known but not yet managed
    # through the ATS.
    assert organisme.gestion_ats is False
    assert organisme.localisation is not None
    assert organisme.localisation.latitude == LATITUDE
    assert organisme.localisation.longitude == LONGITUDE
    assert organisme.localisation.department.code == "01"
    assert organisme.localisation.region.code == "84"


def test_to_domain_without_departement_has_no_localisation(mapper):
    organisme = mapper.to_domain(_make_dto(departement=None))

    assert organisme.localisation is None


def test_to_domain_with_invalid_departement_code_has_no_localisation(mapper):
    organisme = mapper.to_domain(_make_dto(departement="99"))

    assert organisme.localisation is None


def test_to_domain_with_unmapped_departement_has_no_localisation(mapper):
    # Saint-Pierre-et-Miquelon: code de département valide, non couvert par
    # la table de correspondance région/zone.
    organisme = mapper.to_domain(_make_dto(departement="975"))

    assert organisme.localisation is None


def test_to_domain_raises_on_invalid_siret(mapper):
    with pytest.raises(EtablissementInvalideError) as exc_info:
        mapper.to_domain(_make_dto(siret="1234567890123"))

    assert exc_info.value.external_id == "010780195"
