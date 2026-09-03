# ADR-002: Testing Strategy and Repository Mocking

## Status
Accepted — Amended by ADR-009

> ⚠️ **Amendée par [ADR-009](./ADR-009-idiomatic-django-switch.md)**. Voir la section « Impact sur les ADR existantes » d'ADR-009.

## Context

In our Clean Architecture and Domain-Driven Design (DDD) implementation, we need a comprehensive testing strategy that properly isolates different layers and concerns. The challenge is to maintain test reliability while minimizing maintenance overhead, particularly for repository mocking in unit tests.

## Decision

We adopt a three-tier testing strategy aligned with Clean Architecture principles:

### 1. Unit Tests (`tests/*/unit/`)
**Purpose**: Test business logic in isolation (Use Cases from Application layer)

**Scope**:
- Focus exclusively on Use Case testing
- Mock ALL external dependencies (repositories, gateways, services)
- Verify business rules and domain logic

**Repository Mocking Strategy**:
- Use interface-aware mock generation instead of manual in-memory repositories
- Leverage `create_interface_aware_mock()` utility that automatically generates mocks from domain interfaces
- Eliminates maintenance overhead of hand-written in-memory repositories
- Ensures mocks always respect interface contracts through introspection

> 🔗 **Strategy abandoned.** No more repository `Protocol` to mock: use case tests
> become service tests against a real database — see
> [ADR-009 §2 "The Django Model is the entity"](./ADR-009-idiomatic-django-switch.md#2-le-model-django-est-lentité)
> and the ["Impact" table](./ADR-009-idiomatic-django-switch.md#impact-sur-les-adr-existantes).

**Test Data Strategy**:
- Use factory classes exclusively for test data creation
- Avoid JSON fixtures to prevent "magic" data dependencies
- Factories provide explicit, type-safe entity creation
- Enable easy customization of test data per test case

### 2. Integration Tests (`tests/*/integration/`)
**Purpose**: Test integration between layers and external systems

**Scope**:
- Test with real database connections
- Test with mock gateways and external services with httpx_mock
- Verify data persistence and retrieval with DB

### 3. Presentation Tests (`tests/*/presentation/`)
**Purpose**: Test user-facing interfaces and delivery mechanisms

**Scope**:
- Views and templates
- HTTP endpoints and API contracts
- Management commands and CLI tools
- Task queues and background jobs
- User interface behavior and validation
- Usecase are mocked here
  _(obsolete: no more use case/DI to mock, direct call to the service — see ADR-009 §6)_

## Rationale

> 🔗 See [ADR-009 §6 "Removal of dependency injection"](./ADR-009-idiomatic-django-switch.md#6-suppression-de-linjection-de-dépendances)
> for what replaces the interface mocking described below.

### Clean Architecture Alignment
This strategy respects Clean Architecture's dependency inversion principle:
- **Unit tests** focus on the Application layer (Use Cases) without depending on Infrastructure
- **Integration tests** verify that Infrastructure implementations correctly fulfill domain contracts
- **Presentation tests** ensure the outer layer properly. Usecases are mocked here.

### Interface-Aware Mock Generation

> 🔗 **Obsolete.** `create_interface_aware_mock()` is removed by
> [ADR-009 §2](./ADR-009-idiomatic-django-switch.md#2-le-model-django-est-lentité): without
> a repository `Protocol`, there is no interface left to introspect.

Traditional in-memory repositories require significant maintenance:
- Manual implementation of each repository interface
- Keeping mocks synchronized with interface changes
- Duplicated logic across similar repositories

Our `create_interface_aware_mock()` solution:
- **Automatic generation**: Analyzes Protocol interfaces using Python introspection
- **Type safety**: Respects return types, async/sync methods, and Optional types
- **Zero maintenance**: Automatically adapts to interface changes
- **Domain-driven**: Generated directly from domain repository interfaces

```python
# Before: Manual maintenance
class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._storage = {}

    def save(self, user: User) -> User:
        self._storage[user.id] = user
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self._storage.get(user_id)

# After: Zero maintenance
user_repo: IUserRepository = cast(
    IUserRepository,
    create_interface_aware_mock(IUserRepository)
)
```

## Consequences

### Positive
- **Faster unit tests**: No database or I/O operations
- **Reliable isolation**: Business logic tested independently
- **Reduced maintenance**: Automatic mock generation eliminates manual repository maintenance
- **Type safety**: Interface-driven mocks ensure contract compliance
- **Clear separation**: Each test type has a distinct purpose and scope
- **Domain focus**: Unit tests concentrate on business rules without infrastructure concerns

### Negative
- **Learning curve**: Developers need to understand the three-tier distinction
- **Test categorization**: Requires discipline to place tests in correct categories
- **Mock limitations**: Generated mocks may not cover all edge cases that manual implementations could handle
- **Coverage variability**: Factory-generated random data may cause slight coverage fluctuations as some edge cases might not always be covered in randomized scenarios

### Neutral
- **Test organization**: Clear directory structure reflects architectural layers
- **Tooling dependency**: Relies on introspection-based mock generation utility
