from dataclasses import dataclass

from ddd.aggregate_root import AggregateRoot, factory, mutate, query
from ddd.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class ExampleAggregateCree(DomainEvent):
    name: str


@dataclass(frozen=True, kw_only=True)
class ExampleAggregateRenomme(DomainEvent):
    new_name: str


@dataclass(kw_only=True)
class ExampleAggregate(AggregateRoot):
    _name: str

    @classmethod
    @factory(ExampleAggregateCree)
    def create(cls, name: str) -> "ExampleAggregate":
        return cls(_name=name)

    @classmethod
    def build(cls, name: str) -> "ExampleAggregate":
        return cls(_name=name)

    @mutate(ExampleAggregateRenomme)
    def rename(self, new_name: str) -> None:
        self._name = new_name

    @query
    def name_starts_with(self, prefix: str) -> bool:
        return self._name.startswith(prefix)

    @property
    def name(self) -> str:
        return self._name
