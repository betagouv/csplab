from dataclasses import dataclass, field
from functools import wraps
from typing import Callable

from ddd.domain_event import DomainEvent
from ddd.entity import Entity


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
                if attr.fset is not None:
                    raise TypeError(
                        f"{cls.__name__}.{name} is a property with a setter,"
                        f" which is not allowed in an AggregateRoot."
                        f" Use @mutate(EventType) to mutate state."
                    )
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
        if not isinstance(event, DomainEvent):
            raise TypeError(
                f"add_event() expected a DomainEvent, got {type(event).__name__}."
            )
        self._pending_events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = list(self._pending_events)
        self._pending_events.clear()
        return events


# todo: what if several events can create the same aggregate?
# @factory does not allow for that
def factory(event_type: type) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(cls: type, **kwargs: object) -> "AggregateRoot":
            instance: AggregateRoot = method(cls, **kwargs)
            event = event_type(
                aggregate_id=instance.entity_id,
                aggregate=cls.__name__,
                event_name=event_type.__name__,
                **kwargs,
            )
            instance.add_event(event)
            return instance

        wrapper.__is_factory__ = True  # type: ignore[attr-defined]
        return wrapper

    return decorator


def mutate(event_type: type) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self: "AggregateRoot", **kwargs: object) -> None:
            method(self, **kwargs)
            event = event_type(
                aggregate_id=self.entity_id,
                aggregate=self.__class__.__name__,
                event_name=event_type.__name__,
                **kwargs,
            )
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
