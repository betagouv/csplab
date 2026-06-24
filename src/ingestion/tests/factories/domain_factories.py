from polyfactory.factories.dataclass_factory import DataclassFactory
from referentiel.entities.source import Source

from domain.entities.webhook import Webhook


class SourceFactory(DataclassFactory[Source]):
    __model__ = Source


class WebhookFactory(DataclassFactory[Webhook]):
    __model__ = Webhook
    status_id = None
