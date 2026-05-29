from dataclasses import dataclass, field, replace
from functools import wraps
from typing import Callable

from domain.ddd.domain_event import DomainEvent, DomainEventMetadata
from domain.entities.entity import Entity


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    _pending_events: list[DomainEvent] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        excluded = {"build"}
        for name, attr in cls.__dict__.items():
            if name.startswith("_") or name in excluded:
                continue
            is_descriptor = isinstance(attr, (classmethod, staticmethod, property))
            if is_descriptor or not callable(attr):
                continue
            is_mutation = getattr(attr, "__is_mutation__", False)
            is_query = getattr(attr, "__is_query__", False)
            if not (is_mutation or is_query):
                raise TypeError(
                    f"{cls.__name__}.{name}() is a public method but has no decorator. "
                    f"Use @mutate(EventType) for state-changing methods "
                    f"or @query for read-only methods."
                )

    def add_event(self, event: DomainEvent) -> None:
        enriched = replace(
            event,
            metadata=DomainEventMetadata(
                aggregate_id=self.entity_id,
                aggregate=self.__class__.__name__,
                event_name=event.__class__.__name__,
                bounded_context=self.__module__,
            ),
        )
        self._pending_events.append(enriched)

    def collect_events(self) -> list[DomainEvent]:
        events = list(self._pending_events)
        self._pending_events.clear()
        return events


def mutate(event_type: type) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self: "AggregateRoot", event: DomainEvent, *args, **kwargs) -> None:
            if not isinstance(event, event_type):
                raise TypeError(
                    f"{method.__name__}() expected {event_type.__name__}, "
                    f"got {type(event).__name__}."
                )
            method(self, event, *args, **kwargs)
            self.add_event(event)

        wrapper.__is_mutation__ = True  # type: ignore[attr-defined]
        return wrapper

    return decorator


def query(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(*args: object, **kwargs: object) -> object:
        return method(*args, **kwargs)

    wrapper.__is_query__ = True  # type: ignore[attr-defined]
    return wrapper
