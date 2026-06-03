# ats-ddd

Pure technical DDD scaffolding for the CSPLab monorepo.

**No Django, no external libraries — stdlib Python only.**

## Contents

- `AggregateRoot` — base class with `@factory`, `@mutate`, `@query` decorators
- `DomainEvent` / `DomainEventMetadata` — immutable domain event base classes
- `Entity` — base dataclass with `entity_id: UUID`
- `IRepository` - repositories protocols
- `IUseCase` / `IAsyncUseCase` — use case protocols
- `IFromDomainMapper` / `IToDomainMapper` — mapper protocols

## Dependency rules

This package depends **only on the Python standard library**.
No Django, no DRF, no ORM, no external packages.
