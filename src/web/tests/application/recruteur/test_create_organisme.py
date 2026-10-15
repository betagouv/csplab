import pytest
from faker import Faker
from pydantic import ValidationError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.recruteur.services.create_organisme import create_organisme
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

fake = Faker("fr_FR")

VALID_SIRET = fake.siret().replace(" ", "")
INVALID_CHECKSUM_SIRET = VALID_SIRET[:-1] + str((int(VALID_SIRET[-1]) + 1) % 10)


@pytest.fixture(name="staff")
def staff_fixture(db):
    return UtilisateurDjangoFactory(is_staff=True)


def _create(utilisateur, **overrides):
    return create_organisme(
        **{
            "nom": "Commune de Paris",
            "versant": Verse.FPT,
            "siret": VALID_SIRET,
            "utilisateur": utilisateur,
            **overrides,
        }
    )


def test_refuses_non_staff_and_persists_nothing(db):
    utilisateur = UtilisateurDjangoFactory(is_staff=False)

    with pytest.raises(OperationOrganismeRefusee):
        _create(utilisateur)

    assert not OrganismeModel.objects.filter(siret=VALID_SIRET).exists()
    assert not AuditLogModel.objects.exists()


def test_refuses_existing_siret(staff):
    OrganismeDjangoFactory(siret=VALID_SIRET)

    with pytest.raises(OrganismeSiretExisteDeja):
        _create(staff)

    assert OrganismeModel.objects.filter(siret=VALID_SIRET).count() == 1


def test_refuses_siret_with_invalid_checksum(staff):
    with pytest.raises(ValidationError):
        _create(staff, siret=INVALID_CHECKSUM_SIRET)

    assert not OrganismeModel.objects.exists()


def test_writes_an_audit_log(staff):
    organisme = _create(staff)

    logs = PostgresAuditLogRepository().get_logs_for_ressource(
        "Organisme", organisme.id
    )
    assert [(log.event_name, log.utilisateur_id) for log in logs] == [
        ("OrganismeCree", staff.username)
    ]


def test_defaults_to_no_ats_and_no_localisation(staff):
    organisme = _create(staff)

    organisme.refresh_from_db()
    assert organisme.gestion_ats is False
    assert organisme.localisation is None


def test_stores_the_localisation_as_json(staff):
    localisation = Localisation(
        area=GeographicalArea("AF"),
        country=Country("FRA"),
        region=Region(code="04"),
        department=Department(code="76"),
    )

    organisme = _create(staff, localisation=localisation)

    organisme.refresh_from_db()
    assert organisme.localisation == {
        "area": "AF",
        "country": "FRA",
        "region": "04",
        "department": "76",
    }
