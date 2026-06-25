from unittest.mock import Mock
from uuid import uuid4

import pytest
from django.contrib import admin
from django.test import RequestFactory
from referentiel.exceptions.source_errors import MissingTalentsoftFieldsError
from referentiel.value_objects.source_type import SourceType

from infrastructure.django_apps.ingestion.admin import SourceAdmin
from infrastructure.django_apps.ingestion.models.source import SourceModel


@pytest.fixture
def source_admin():
    return SourceAdmin(SourceModel, admin.site)


@pytest.fixture
def request_():
    return RequestFactory().get("/")


def _source(**overrides):
    fields = {
        "id": uuid4(),
        "source_id": uuid4(),
        "slug": "talentsoft",
        "type": SourceType.TALENTSOFT.value,
        "client_id_front": "client_front",
        "client_id_back": "client_back",
        "base_url_front": "https://front.example.com",
        "base_url_back": "https://back.example.com",
    }
    fields.update(overrides)
    obj = SourceModel(**fields)
    obj.save = Mock()  # guard: must never reach persistence
    return obj


@pytest.mark.parametrize(
    "missing_field",
    [
        "client_id_front",
        "client_id_back",
        "base_url_front",
        "base_url_back",
    ],
)
def test_save_with_missing_talentsoft_field_is_rejected(
    source_admin, request_, missing_field
):
    source = _source(**{missing_field: None})

    with pytest.raises(MissingTalentsoftFieldsError):
        source_admin.save_model(request_, source, form=None, change=False)

    source.save.assert_not_called()


@pytest.mark.parametrize(
    "overrides",
    [
        pytest.param({}, id="valid-talentsoft"),
        pytest.param(
            {
                "type": SourceType.API.value,
                "client_id_front": None,
                "client_id_back": None,
                "base_url_front": None,
                "base_url_back": None,
            },
            id="api-with-missing-values",
        ),
    ],
)
def test_save_valid_source_is_persisted(source_admin, request_, overrides):
    source = _source(**overrides)

    source_admin.save_model(request_, source, form=None, change=False)

    source.save.assert_called_once()
