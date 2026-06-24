from unittest.mock import Mock
from uuid import uuid4

import pytest
from django.contrib import admin
from django.test import RequestFactory
from referentiel.value_objects.verse import Verse

from domain.identite.errors.organisme_errors import SiretInvalide
from infrastructure.django_apps.recruteur.admin import OrganismeAdmin
from infrastructure.django_apps.recruteur.models import OrganismeModel

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

    with pytest.raises(SiretInvalide):
        organisme_admin.save_model(request_, organisme, form=None, change=True)

    organisme.save.assert_not_called()
