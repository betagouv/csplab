from unittest.mock import Mock
from uuid import uuid4

import pytest
from django.contrib import admin
from django.test import RequestFactory
from pydantic import ValidationError
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.recruteur.admin import (
    CreateOrganismeAdminForm,
    OrganismeAdmin,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

VALID_SIRET = "19754687200015"


@pytest.fixture
def organisme_admin():
    return OrganismeAdmin(OrganismeModel, admin.site)


@pytest.fixture
def request_():
    return RequestFactory().get("/")


def _organisme(siret):
    obj = OrganismeModel(
        id=uuid4(),
        nom="Ministère X",
        versant=Verse.FPE.value,
        siret=siret,
        localisation=None,
    )
    obj.save = Mock()  # guard: must never reach persistence
    return obj


def test_edit_with_invalid_siret_is_rejected(organisme_admin, request_):
    organisme = _organisme(siret="siret-invalide")

    with pytest.raises(ValidationError):
        organisme_admin.save_model(request_, organisme, form=None, change=True)

    organisme.save.assert_not_called()


def test_create_persists_the_organisme_through_the_service(
    organisme_admin, request_, db
):
    staff = UtilisateurDjangoFactory(is_staff=True)
    request_.user = staff
    form = Mock(
        cleaned_data={
            "nom": "Ministère X",
            "versant": Verse.FPE.value,
            "siret": VALID_SIRET,
            "parent_id": None,
            "area": "AF",
            "country": "FRA",
            "region": "04",
            "department": "76",
        }
    )
    organisme = OrganismeModel()

    organisme_admin.save_model(request_, organisme, form=form, change=False)

    created = OrganismeModel.objects.get(siret=VALID_SIRET)
    assert organisme.id == created.id
    assert created.localisation == {
        "area": "AF",
        "country": "FRA",
        "region": "04",
        "department": "76",
    }
    logs = PostgresAuditLogRepository().get_logs_for_ressource("Organisme", created.id)
    assert [(log.event_name, log.utilisateur_id) for log in logs] == [
        ("OrganismeCree", staff.username)
    ]


def test_create_abroad_persists_the_organisme_without_region_nor_department(
    organisme_admin, request_, db
):
    request_.user = UtilisateurDjangoFactory(is_staff=True)
    form = Mock(
        cleaned_data={
            "nom": "Lycée français de Berlin",
            "versant": Verse.FPE.value,
            "siret": VALID_SIRET,
            "parent_id": None,
            "area": "EU",
            "country": "DEU",
            "region": "",
            "department": "",
        }
    )

    organisme_admin.save_model(request_, OrganismeModel(), form=form, change=False)

    assert OrganismeModel.objects.get(siret=VALID_SIRET).localisation == {
        "area": "EU",
        "country": "DEU",
        "region": None,
        "department": None,
    }


def _create_form(**localisation) -> CreateOrganismeAdminForm:
    return CreateOrganismeAdminForm(
        data={
            "nom": "Ministère X",
            "versant": Verse.FPE.value,
            "siret": VALID_SIRET,
            "area": "EU",
            **localisation,
        }
    )


@pytest.mark.parametrize(
    ("localisation", "error"),
    [
        (
            {"country": "FRA", "region": "11", "department": ""},
            "La région et le département sont obligatoires en France.",
        ),
        (
            {"country": "DEU", "region": "11", "department": "75"},
            "La région et le département doivent être vides hors de France.",
        ),
    ],
)
def test_create_form_rejects_a_subdivision_that_does_not_match_the_country(
    db, localisation, error
):
    form = _create_form(**localisation)

    assert not form.is_valid()
    assert form.non_field_errors() == [error]


@pytest.mark.parametrize(
    "localisation",
    [
        {"country": "FRA", "region": "11", "department": "75"},
        {"country": "DEU", "region": "", "department": ""},
    ],
)
def test_create_form_accepts_a_subdivision_that_matches_the_country(db, localisation):
    form = _create_form(**localisation)

    assert form.is_valid(), form.errors
