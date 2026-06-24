from polyfactory.factories.dataclass_factory import DataclassFactory
from referentiel.entities.source import Source
from referentiel.value_objects.source_type import SourceType

from domain.entities.webhook import Webhook


class SourceFactory(DataclassFactory[Source]):
    __model__ = Source
    type = SourceType.TALENTSOFT
    client_id_front = "client_front"
    client_id_back = "client_back"
    base_url_front = "https://front.example.com"
    base_url_back = "https://back.example.com"


class WebhookFactory(DataclassFactory[Webhook]):
    __model__ = Webhook
    status_id = None
