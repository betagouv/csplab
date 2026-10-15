from unittest.mock import Mock
from uuid import uuid4

import pytest
from django.contrib import admin
from django.test import RequestFactory
from pydantic import ValidationError
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.recruteur.admin import OrganismeAdmin
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
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
    request_.user = UtilisateurDjangoFactory(is_staff=True)
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
