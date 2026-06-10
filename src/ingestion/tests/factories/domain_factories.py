from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.value_objects.source import Source


class SourceFactory(DataclassFactory[Source]):
    __model__ = Source
