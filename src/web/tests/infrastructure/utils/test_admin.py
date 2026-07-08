import pytest
from django.contrib import admin
from django.db import models
from django.test import RequestFactory

import config.urls  # noqa: F401  # side effect: ensures admin modules are registered
from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.referentiel.models.concours import ConcoursModel
from infrastructure.django_apps.referentiel.models.corps import CorpsModel
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel

READONLY_MODELS = [
    OfferModel,
    CorpsModel,
    ConcoursModel,
    MetierModel,
    ApiLogModel,
    ApiLogDailyAggregationModel,
    RawDocument,
]


@pytest.fixture
def request_():
    return RequestFactory().get("/")


@pytest.mark.parametrize("model", READONLY_MODELS)
class TestReadOnlyAdmin:
    def _admin(self, model):
        return admin.site._registry[model]

    def test_add_is_forbidden(self, model, request_):
        assert self._admin(model).has_add_permission(request_) is False

    def test_change_is_forbidden(self, model, request_):
        assert self._admin(model).has_change_permission(request_) is False

    def test_delete_is_forbidden(self, model, request_):
        assert self._admin(model).has_delete_permission(request_) is False

    def test_all_fields_are_readonly(self, model, request_):
        admin_obj = self._admin(model)
        expected = [
            f.name for f in model._meta.get_fields() if isinstance(f, models.Field)
        ]
        assert list(admin_obj.get_readonly_fields(request_)) == expected
