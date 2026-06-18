from dataclasses import dataclass

import pytest

from ddd.aggregate_root import AggregateRoot, factory
from ddd.domain_event import DomainEvent
from tests.example_aggregate import (
    ExampleAggregate,
    ExampleAggregateCree,
    ExampleAggregateRenomme,
)
from tests.example_aggregate_factory import ExampleAggregateFactory


def test_build_produces_no_pending_events():
    example = ExampleAggregateFactory.build()
    assert example.collect_events() == []


def test_mutate_applies_state_change_and_emits_event():
    example = ExampleAggregateFactory.build(name="Initial")
    example.rename(new_name="Updated")
    events = example.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ExampleAggregateRenomme)
    assert example.name == "Updated"


def test_mutate_enriches_event_with_aggregate_context():
    example = ExampleAggregateFactory.build(name="Initial")
    example.rename(new_name="Updated")
    event = example.collect_events()[0]
    assert event.aggregate_id == example.entity_id
    assert event.aggregate == "ExampleAggregate"
    assert event.event_name == "ExampleAggregateRenomme"


def test_public_method_without_decorator_raises():
    with pytest.raises(TypeError, match="public method but has no decorator"):

        @dataclass
        class _BadAggregate(AggregateRoot):
            def forgot_to_decorate(self) -> None: ...


def test_query_does_not_emit_event():
    example = ExampleAggregateFactory.build(name="Hello")
    example.name_starts_with("He")
    assert example.collect_events() == []


def test_create_properties_are_read_only():
    example = ExampleAggregateFactory.build(name="Hello")

    with pytest.raises(AttributeError):
        example.name = "hacked"  # type: ignore[misc]


def test_factory_emits_event_automatically():
    example = ExampleAggregate.create(name="Nouveau")
    events = example.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ExampleAggregateCree)
    assert example.name == "Nouveau"


def test_factory_enriches_event_with_aggregate_context():
    example = ExampleAggregate.create(name="Nouveau")
    event = example.collect_events()[0]
    assert event.aggregate_id == example.entity_id
    assert event.aggregate == "ExampleAggregate"
    assert event.event_name == "ExampleAggregateCree"
    assert event.name == "Nouveau"


def test_create_without_factory_decorator_raises():
    with pytest.raises(TypeError, match="must be decorated with @factory"):

        @dataclass
        class _BadAggregate(AggregateRoot):
            @classmethod
            def create(cls) -> "_BadAggregate":  # type: ignore[override]
                return cls()


def test_public_classmethod_other_than_build_or_create_raises():
    with pytest.raises(TypeError, match="public classmethod but is not allowed"):

        @dataclass
        class _BadAggregate(AggregateRoot):
            @classmethod
            def from_dict(cls, data: dict) -> "_BadAggregate":
                return cls()


def test_public_staticmethod_raises():
    with pytest.raises(TypeError, match="public staticmethod which is not allowed"):

        @dataclass
        class _BadAggregate(AggregateRoot):
            @staticmethod
            def helper() -> str:
                return "oops"


def test_property_with_setter_raises():
    with pytest.raises(TypeError, match="property with a setter"):

        @dataclass(kw_only=True)
        class BadAggregate(AggregateRoot):
            _name: str

            @property
            def name(self) -> str:
                return self._name

            @name.setter
            def name(self, value: str) -> None:
                self._name = value


def test_public_non_callable_class_attribute_is_allowed():
    # MAX_SIZE is public, non-callable
    # __init_subclass__ skip it without raising d'erreur
    @dataclass(kw_only=True)
    class AggregateWithConstant(AggregateRoot):
        MAX_SIZE = 100

    assert AggregateWithConstant.MAX_SIZE == 100  # noqa


def test_add_event_rejects_non_domain_event():
    example = ExampleAggregateFactory.build()
    with pytest.raises(TypeError, match="expected a DomainEvent"):
        example.add_event("not_an_event")  # type: ignore[arg-type]


def test_factory_missing_required_payload_param_raises():
    @dataclass(frozen=True, kw_only=True)
    class _Event(DomainEvent):
        required_field: str

    with pytest.raises(TypeError, match="miss event required field"):

        @dataclass(kw_only=True)
        class _BadAggregate(AggregateRoot):
            @classmethod
            @factory(_Event)
            def create(cls) -> "_BadAggregate":  # type: ignore[override]
                return cls()
