from datetime import datetime, timezone
from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel


class ApiLogDjangoFactory(DjangoModelFactory):
    class Meta:
        model = ApiLogModel

    id = factory.LazyFunction(uuid4)
    path = "/api/v1/offres/"
    method = "GET"
    token_type = "jwt"  # noqa: S105
    timestamp = factory.LazyFunction(lambda: datetime.now(tz=timezone.utc))
    ip_address = "127.0.0.1"
    status_code = 200
    auth_token = "test-token"  # noqa: S105
