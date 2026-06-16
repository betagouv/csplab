from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.entities.webhook import Webhook
from domain.value_objects.source import Source


class SourceFactory(DataclassFactory[Source]):
    __model__ = Source


class WebhookFactory(DataclassFactory[Webhook]):
    __model__ = Webhook
    status_id = None
