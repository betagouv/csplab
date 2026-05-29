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
        for name, attr in cls.__dict__.items():
            if name.startswith("_"):
                continue
            if isinstance(attr, classmethod):
                if name == "build":
                    continue
                if name == "create":
                    if not getattr(attr.__func__, "__is_factory__", False):
                        raise TypeError(
                            f"{cls.__name__}.create() must be decorated"
                            f" with @factory(EventType) to ensure the"
                            f" domain event is always emitted."
                        )
                    continue
                raise TypeError(
                    f"{cls.__name__}.{name}() is a public classmethod"
                    f" but is not allowed. Only 'build' (reconstitution)"
                    f" and 'create' (decorated with @factory) are permitted."
                )
            if isinstance(attr, property):
                continue
            if isinstance(attr, staticmethod):
                raise TypeError(
                    f"{cls.__name__}.{name}() is a public staticmethod"
                    f" which is not allowed in an AggregateRoot."
                    f" Use @factory(EventType) on a @classmethod instead."
                )
            if not callable(attr):
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


def factory(event_type: type) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(
            cls: type, event: DomainEvent, *args: object, **kwargs: object
        ) -> "AggregateRoot":
            if not isinstance(event, event_type):
                raise TypeError(
                    f"{method.__name__}() expected {event_type.__name__}, "
                    f"got {type(event).__name__}."
                )
            instance: AggregateRoot = method(cls, event, *args, **kwargs)
            instance.add_event(event)
            return instance

        wrapper.__is_factory__ = True  # type: ignore[attr-defined]
        return wrapper

    return decorator


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
