# ADR-003: DDD Aggregate Root Pattern

**Status:** Accepted
**Date:** 2026.05.28
**Deciders:** Élodie R
**Tags:** ddd, domain, architecture

---

## Context

The ATS involves strong business complexity: legal hiring priorities, multi-actor
validation workflows, and strict traceability requirements.

---

## Decision Drivers

- Protect invariants at the closest point to the data
- Make every mutation explicit and traceable via Domain Events
- Prevent silent external mutations
- Prevent business rule leaking into the application layer
- No external DDD framework dependency
- Avoid callback (or event handling) hell

---

## Considered Options

1. **Option A** — Plain `@dataclass` entities (current pattern for `Offer`, `Concours`…)
2. **Option B** — `AggregateRoot` base class with Domain Events + factory method for instantiation
3. **Option C** — Full Event Sourcing (state rebuilt from event log)

---

## Decision Outcome

**Chosen option: Option B.**

Option A has no mechanism to protect invariants or emit events.
Option C requires an event store — out of scope for MVP.

### Positive Consequences

- Invariants are protected at the source
- Every mutation produces a traceable Domain Event
- `build()` makes intent explicit and testable
- `__init_subclass__` enforces the pattern at class-definition time (see Rule 6)

### Negative Consequences / Trade-offs

- More boilerplate than plain dataclasses
- Python's weak encapsulation requires convention + tests; `_private` attributes can
  still be accessed from outside

---

## Guidelines

### Rule 1 — Never instantiate an aggregate root directly, use a factory method

```python
@classmethod
def build(cls, ...) -> "MyAggregate":
    """Restores an existing aggregate from persistence. MUST NOT emit any event."""
    ...
```

`build()` is called by repositories when loading from the database.

### Rule 2 — Every mutation must be decorated with `@mutate`

Every state-changing method must be decorated with `@mutate(EventType)`.
The decorator:

1. Verifies at runtime that the received event is of the declared type
2. Calls the method body (which applies the state change)
3. Automatically calls `self.add_event(event)` — no need to do it manually

```python
from domain.entities.aggregate_root import mutate

@mutate(OrganismeRenomme)
def rename(self, event: OrganismeRenomme) -> None:
    self._name = event.new_name
```

The caller (use case) is responsible for constructing the event:

```python
organisme.rename(OrganismeRenomme(new_name="Ministère X"))
```

### Rule 3 — Public attributes are read-only

Mutable attributes are stored as `_private` and exposed via `@property` without setter.
Direct assignment `aggregate.attribute = value` from outside raises `AttributeError`.

### Rule 4 — All aggregate root events are collected by the application layer

The aggregate accumulates events internally. The use case calls `aggregate.collect_events()`
after `repository.save()` and dispatches all collected events. This enables fine-grained
orchestration and makes use cases easy to test in isolation.

### Rule 5 — Test that events are emitted

Every aggregate must have unit tests verifying:

```python
# example: mutation OrganismeRenomme on Organisme aggregate
def test_rename_emits_event():
    organisme = OrganismeFactory.build_aggregate()
    organisme.rename(OrganismeRenomme(new_name="New name"))
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeRenomme)
```

### Rule 6 — Every public method must be decorated with `@mutate` or `@query`

`AggregateRoot.__init_subclass__` enforces this at class-definition time.
Any public method (not a `@classmethod`, `@staticmethod`, `@property`, or `build`) that
lacks one of these decorators raises a `TypeError` immediately when the module is imported.

Use `@query` for read-only methods that cannot be expressed as a `@property`
(e.g. methods with parameters):

```python
from domain.entities.aggregate_root import query

@query
def has_priority_grade(self, grade: Grade) -> bool:
    return grade in self._priority_grades
```

This makes the public API of every aggregate self-documenting:

- `@mutate` → changes state, emits a Domain Event
- `@query` → reads state, no side effect
- `@property` → read-only attribute projection
- `_private` → internal helper

---

## Domain Building Blocks

| File                                | Description                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| `domain/events/domain_event.py`     | `DomainEventMetadata`, `DomainEvent` frozen dataclasses                             |
| `domain/entities/entity.py`         | `Entity` base class (`entity_id: UUID`)                                             |
| `domain/entities/aggregate_root.py` | `AggregateRoot(Entity)` with `add_event()`, `collect_events()`, `__init_subclass__` |

**Note:** existing entities (`Offer`, `Concours`…) are NOT migrated. This pattern applies
only to new aggregates with meaningful business behaviour for the ATS.
