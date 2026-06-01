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
- `build()` and `create()` make intent explicit and testable
- `__init_subclass__` enforces the pattern at class-definition time (see Rules 6 & 7)

### Negative Consequences / Trade-offs

- More boilerplate than plain dataclasses
- Python's weak encapsulation requires convention + tests; `_private` attributes can
  still be accessed from outside

---

## Guidelines

### Rule 1 — Two factory classmethods: `build()` for reconstitution, `create()` for creation

```python
@classmethod
def build(cls, ...) -> "MyAggregate":
    """Restores an existing aggregate from persistence. MUST NOT emit any event."""
    return cls(...)

@classmethod
@factory(MyAggregateCree)
def create(cls, event: MyAggregateCree) -> "MyAggregate":
    """Creates a new aggregate. Automatically emits the event via @factory."""
    return cls(...)
```

- `build()` is called by repositories when rehydrating from the database. It is silent:
  no event is emitted.
- `create()` is the business creation entry point. It **must** be decorated with
  `@factory(EventType)`, which automatically calls `instance.add_event(event)` after
  construction. Forgetting the decorator raises `TypeError` at import time (see Rule 7).

### Rule 2 — Every mutation must be decorated with `@mutate`

Every state-changing method must be decorated with `@mutate(EventType)`.
The decorator:

1. Verifies at runtime that the received event is of the declared type
2. Calls the method body (which applies the state change)
3. Automatically calls `self.add_event(event)` — no need to do it manually

```python
from domain.ddd.aggregate_root import mutate

@mutate(OrganismeRenomme)
def rename(self, event: OrganismeRenomme) -> None:
    self._name = event.new_name
```

The caller (use case) is responsible for constructing the event:

```python
organisme.rename(OrganismeRenomme(new_name="Ministère X"))
```

### Rule 3 — Public attributes are read-only; property setters are banned

Mutable attributes are stored as `_private` and exposed via `@property` **without setter**.
`__init_subclass__` raises `TypeError` at class-definition time if a property has a setter.
Direct assignment `aggregate.attribute = value` from outside raises `AttributeError`.

```python
# ✅ OK
@property
def nom(self) -> str:
    return self._nom

# ❌ Raises TypeError at import time
@nom.setter
def nom(self, value: str) -> None:
    self._nom = value  # silent mutation, no event
```

To change a value, use `@mutate` instead.

### Rule 4 — All aggregate root events are collected by the application layer

The aggregate accumulates events internally. The use case calls `aggregate.collect_events()`
after `repository.save()` and dispatches all collected events. This enables fine-grained
orchestration and makes use cases easy to test in isolation.

### Rule 5 — Test that events are emitted

Every aggregate must have unit tests verifying:

```python
# example: creation of Organisme
def test_create_emits_event():
    event = OrganismeCree(nom="DRH Centrale", ...)
    organisme = Organisme.create(event)
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)

# example: mutation OrganismeRenomme on Organisme aggregate
def test_rename_emits_event():
    organisme = OrganismeFactory.build()
    organisme.rename(OrganismeRenomme(new_name="New name"))
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeRenomme)
```

### Rule 6 — Every public instance method must be decorated with `@mutate` or `@query`

`AggregateRoot.__init_subclass__` enforces this at class-definition time.
Any public method that lacks one of these decorators raises a `TypeError` immediately
when the module is imported.

Use `@query` for read-only methods that cannot be expressed as a `@property`
(e.g. methods with parameters):

```python
from domain.ddd.aggregate_root import query

@query
def has_priority_grade(self, grade: Grade) -> bool:
    return grade in self._priority_grades
```

This makes the public API of every aggregate self-documenting:

- `@mutate` → changes state, emits a Domain Event
- `@query` → reads state, no side effect
- `@property` → read-only attribute projection
- `_private` → internal helper

### Rule 7 — Only `build` and `create` are allowed as public classmethods; `@staticmethod` is banned

`__init_subclass__` enforces the following constraints at class-definition time:

| Member type     | Allowed names     | Additional constraint                                     |
| --------------- | ----------------- | --------------------------------------------------------- |
| `@classmethod`  | `build`, `create` | `create` **must** be decorated with `@factory(EventType)` |
| `@staticmethod` | _(none)_          | Always raises `TypeError`                                 |
| `@property`     | any               | Setter (`fset`) raises `TypeError`                        |
| Instance method | any public name   | Must have `@mutate` or `@query`                           |

**Why ban `@staticmethod`?** A `@staticmethod` has no access to `cls` or `self`, so it
cannot call `add_event`. It would be a silent factory without event emission guarantee.

**Why require `@factory` on `create`?** Without the decorator, nothing prevents a developer
from forgetting `add_event`. The `@factory(EventType)` decorator enforces the contract:
it verifies the event type, constructs the instance, and calls `add_event` automatically.

---

## Domain Building Blocks

| File                           | Description                                                          |
| ------------------------------ | -------------------------------------------------------------------- |
| `domain/ddd/domain_event.py`   | `DomainEventMetadata`, `DomainEvent` frozen dataclasses              |
| `domain/entities/entity.py`    | `Entity` base class (`entity_id: UUID`)                              |
| `domain/ddd/aggregate_root.py` | `AggregateRoot(Entity)` + `@factory`, `@mutate`, `@query` decorators |

**Note:** existing entities (`Offer`, `Concours`…) are NOT migrated. This pattern applies
only to new aggregates with meaningful business behaviour for the ATS.
