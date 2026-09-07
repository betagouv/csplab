from datetime import datetime, timezone
from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from infrastructure.django_apps.commons.models import AuditLogModel


class AuditLogDjangoFactory(DjangoModelFactory):
    class Meta:
        model = AuditLogModel

    id = factory.LazyFunction(uuid4)
    event_id = factory.LazyFunction(uuid4)
    occurred_at = factory.LazyFunction(lambda: datetime.now(tz=timezone.utc))
    utilisateur_id = factory.LazyFunction(uuid4)
    event_name = "ProfilAgentCree"
    ressource_kind = "Agent"
    ressource_id = factory.LazyFunction(uuid4)
