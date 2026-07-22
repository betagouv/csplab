# RBAC for note use cases (list/create), with DB-touching tests

## Context

`ListerNotesCandidatureUsecase` and `CreerNoteUsecase` currently have no authorization
check at all (any authenticated user can list/create notes on any candidature).
`EditerNoteUsecase`/`SupprimerNoteUsecase` already restrict to the note's author, with a
`# TODO : refactor with upcoming RBAC` marker in `editer_note.py:30` — that TODO refers to
this piece of work landing.

Goal: authorize list/create the same way commit `aabab734`/`df99eb13` authorized
organisme-level actions (`OrganismePermissionService` + `IOrganismeAgentRepository` +
`AccesOrganismeRefuse`), but scoped to a candidature's recrutement:

- **List notes / create note**: allowed if the agent is `RESPONSABLE` of the **Organisme**
  that owns the recrutement, OR holds any of `RESPONSABLE` / `RECRUTEUR` / `CONTRIBUTEUR` on
  the **Recrutement** itself. Staff bypasses.
- **Edit / delete note**: unchanged — author-only, unchanged error (`NoteIntrouvable`, 404).

Also close a gap found during investigation: no test in the repo today exercises a real
permission service wired to real Postgres repositories through a real use case (existing
organisme RBAC tests always mock the permission service in integration tests). This task
should add exactly that for notes, per the explicit ask for "touching DB RBAC tests".

## Design decisions

- No `NoteAction` enum / role-dict (unlike `OrganismeAction`): list and create share
  identical rules, so `NotePermissionService.est_autorise(*, candidature_id, agent_id,
  est_staff)` takes no action parameter — avoids introducing an abstraction only the
  organisme case needed (that one has per-action *different* required roles).
- The `candidature_id → (recrutement_id, organisme_id)` resolver lives in a **new, single-
  purpose interface** in `domain/recruteur` (`INotePermissionRepository`), not bolted onto
  `ICandidatureRepository` (which lives in `domain/candidate` — importing it from
  `domain/recruteur` would create a new cross-context domain dependency; no such dependency
  exists today, and everything else needed is already in `domain/recruteur`).
- If the resolver can't find the candidature (chain doesn't resolve), raise `AccesNoteRefuse`
  — not `CandidatureIntrouvable` (that error belongs to `domain.candidate`, and importing it
  would reintroduce the cross-context dependency just avoided above). For `CreerNoteUsecase`
  this branch is practically unreachable (existence already checked first). For
  `ListerNotesCandidatureUsecase` this is an observable behavior change: GET on a nonexistent
  `candidature_id` today silently returns `200 []`; after this change it returns `403`. This
  is intentional (secure by default, no existence-leak via status code) — flagging it here
  since it's user-visible.
- Recrutement-level role storage (`RecrutementAgentModel`, `AgentRecrutementRole`) already
  exists; only its repository/permission wiring is missing.

## Files to add

**Domain** (`src/web/domain/recruteur/`)
- `repositories/recrutement_agent_repository_interface.py` — `IRecrutementAgentRepository`
  Protocol, mirrors `organisme_agent_repository_interface.py`:
  `get_role(*, recrutement_id: UUID, agent_id: UUID) -> AgentRecrutementRole | None`.
- `repositories/note_permission_repository_interface.py` — `INotePermissionRepository`
  Protocol: `get_recrutement_et_organisme(candidature_id: UUID) -> tuple[UUID, UUID] | None`.
- `errors/note_permission_errors.py` — `NotePermissionError(DomainError)`,
  `AccesNoteRefuse(NotePermissionError)` holding `candidature_id` (mirrors
  `organisme_permission_errors.py`).
- `services/note_permission_service.py` — `NotePermissionService`, constructor takes
  `note_permission_repository`, `organisme_agent_repository`, `recrutement_agent_repository`.
  `est_autorise(*, candidature_id, agent_id, est_staff) -> None`: staff bypass → resolve
  chain (raise `AccesNoteRefuse` if unresolved) → organisme role `RESPONSABLE` passes →
  else recrutement role in `{RESPONSABLE, RECRUTEUR, CONTRIBUTEUR}` passes → else raise
  `AccesNoteRefuse`.

**Infrastructure** (`src/web/infrastructure/`)
- `repositories/recruteur/postgres_recrutement_agent_repository.py` —
  `PostgresRecrutementAgentRepository.get_role`, queries `RecrutementAgentModel` exactly like
  `postgres_organisme_agent_repository.py` queries `OrganismeAgentModel`.
- `repositories/recruteur/postgres_note_permission_repository.py` —
  `PostgresNotePermissionRepository.get_recrutement_et_organisme`, single ORM query:
  `CandidatureModel.objects.filter(id=candidature_id).values_list("etape__recrutement_id", "etape__recrutement__organisme_id").first()`.

## Files to change

**`application/recruteur/usecases/lister_notes_candidature.py`**
Add `utilisateur_id: UUID` (mandatory) and `est_staff: bool = False` to
`ListerNotesCandidatureQuery`; inject `note_permission_service: NotePermissionService`; call
`est_autorise(...)` as the first line of `execute()`.

**`application/recruteur/usecases/creer_note.py`**
Add `est_staff: bool = False` to `CreerNoteCommand` (no new identity field — `publie_par_id`
is already the acting agent). Inject `note_permission_service`. Call `est_autorise(...)`
**after** the existing `candidature_repository.exists` / `agent_repository.exists` checks
(preserves current error precedence: `CandidatureIntrouvable` / `ProfilAgentNexistePas` before
any RBAC error, so existing tests for those two errors keep passing unmodified).

**`application/recruteur/usecases/editer_note.py`**
Delete the `# TODO : refactor with upcoming RBAC` comment on line 30. No other change —
author-only check and `NoteIntrouvable` stay as-is.

**`application/recruteur/usecases/supprimer_note.py`** — no change.

**`infrastructure/di/recruteur/recruteur_container.py`**
Add providers: `postgres_recrutement_agent_repository` (Singleton),
`postgres_note_permission_repository` (Singleton), `note_permission_service` (Factory,
reusing the existing `postgres_organisme_agent_repository` provider for its organisme leg).
Wire `note_permission_service=note_permission_service` into `creer_note_usecase` and
`lister_notes_candidature_usecase`. `editer_note_usecase`/`supprimer_note_usecase` untouched.

**`presentation/recruteur/views/notes.py`**
- `CandidatureNotesView.get`: remove the `# TODO RBAC` comment; pass
  `utilisateur_id=UUID(request.user.username)`, `est_staff=request.user.is_staff` into
  `ListerNotesCandidatureQuery`; add `except AccesNoteRefuse: return Response({"detail":
  "Forbidden."}, status=403)` (mirrors `organismes.py`'s `AccesOrganismeRefuse` handling).
- `CandidatureNotesView.post`: pass `est_staff=request.user.is_staff` into
  `CreerNoteCommand`; add the same `AccesNoteRefuse` → 403 catch alongside the existing
  `CandidatureIntrouvable`/`ProfilAgentNexistePas` catches.
- `@extend_schema_view` on `CandidatureNotesView`: add `403: GenericErrorSerializer` to both
  `get` and `post` response dicts (they currently lack a 403 entry).
- `CandidatureNoteDetailView` (patch/delete) — no change.

**API schema regen** — required (new 403 response added to two documented operations changes
`schema.yaml`'s content even though request/response bodies are unchanged):
```bash
bin/manage spectacular --file presentation/static/api/schema.yaml
```
Check if `internal-schema.yaml` also documents these routes; if so regenerate that too.

## Tests

**Update existing (must not regress)**
- `tests/application/recruteur/test_note_usecases.py`: `CreerNoteUsecase` fixture needs
  `note_permission_service=MagicMock(spec=NotePermissionService)` injected.
- `tests/application/recruteur/test_lister_note_usecases.py`: inject mocked
  `note_permission_service`; add `utilisateur_id=uuid4()` to all
  `ListerNotesCandidatureQuery(...)` calls (now a mandatory field).
- `tests/infrastructure/recruteur/test_notes_usecases.py`: in the
  `recruteur_integration_container` fixture, add
  `container.note_permission_service.override(MagicMock(spec=NotePermissionService))`
  (bypasses RBAC, consistent with how this fixture already bypasses
  `organisme_permission_service` for organisme-step tests); add `utilisateur_id=uuid4()` to
  the existing `ListerNotesCandidatureQuery` call.
- `tests/presentation/recruteur/test_views_notes.py`: existing assertions on
  `CreerNoteCommand(...)` still hold since `est_staff` defaults to `False`; add two new cases
  asserting 403 when the mocked usecase raises `AccesNoteRefuse` (GET and POST), mirroring
  `test_views_organismes.py`.

**New — pure unit (mocked, no DB)**
- `tests/domain/recruteur/test_note_permission_service.py`: mock all three repository
  Protocols. Cases: organisme role `RESPONSABLE` passes; recrutement role `RESPONSABLE`/
  `RECRUTEUR`/`CONTRIBUTEUR` each pass (parametrized); organisme `MEMBRE` + no recrutement
  role raises `AccesNoteRefuse`; unresolved candidature raises `AccesNoteRefuse`; `est_staff`
  bypasses without calling either role repository (`assert_not_called()`).

**New — touching DB (the core deliverable)**
- `tests/infrastructure/recruteur/test_recrutement_agent_repository.py`: mirrors
  `test_organisme_agent_repository.py`. Uses `db` fixture + `PostgresRecrutementAgentRepository()`
  + `RecrutementFactory.create_model(agent_ids=(agent.utilisateur_id,), agent_roles={agent.utilisateur_id: AgentRecrutementRole.X})`.
  Cases: returns `RESPONSABLE`/`RECRUTEUR`/`CONTRIBUTEUR`; returns `None` when no liaison.
- `tests/infrastructure/recruteur/test_note_permission_repository.py`: `db` fixture +
  `PostgresNotePermissionRepository()`. Build via `OfferFactory` → `RecrutementFactory.create_model(offre_id=offer.id, organisme_id=organisme.id)`
  → `CandidatureFactory.create_model(offre_id=offer.id)`. Assert resolver returns
  `(recrutement.offre_id, organisme.id)`; returns `None` for an unknown `candidature_id`.
- `tests/infrastructure/recruteur/test_notes_rbac.py` (new file — the explicit "touching DB
  RBAC test" ask): wires the **real** `RecruteurContainer` with **no** override of
  `note_permission_service` — exercises `NotePermissionService` +
  `PostgresOrganismeAgentRepository` + `PostgresRecrutementAgentRepository` +
  `PostgresNotePermissionRepository` against real Postgres, through the real
  `creer_note_usecase()` / `lister_notes_candidature_usecase()`. Build fixtures using
  `OrganismeFactory.create_model(agent_id=..., role=...)` +
  `RecrutementFactory.create_model(offre_id=..., organisme_id=..., agent_ids=(...,),
  agent_roles={...})` + `CandidatureFactory.create_model(offre_id=...)`, reusing the same
  `offre_id` across both factories so the candidature lands on the recrutement being tested.
  Cases (for both list and create):
  - organisme `RESPONSABLE` → authorized
  - recrutement `RESPONSABLE` / `RECRUTEUR` / `CONTRIBUTEUR` (parametrized) → authorized
  - organisme `MEMBRE` + no recrutement liaison → `AccesNoteRefuse`
  - no relationship at all → `AccesNoteRefuse`
  - `est_staff=True` with zero liaisons → authorized (bypass)
  - `ListerNotesCandidatureUsecase` with a nonexistent `candidature_id` → `AccesNoteRefuse`

## Verification

- `make lint-web-fix` (ruff, mypy, djlint, migrations check) — no migration expected (no
  model changes, only new repository/service classes over existing tables).
- Run the affected test modules: `bin/manage test` (or the project's pytest invocation) over
  `tests/domain/recruteur/`, `tests/application/recruteur/`, `tests/infrastructure/recruteur/`,
  `tests/presentation/recruteur/test_views_notes.py`.
- Confirm `bin/manage spectacular --file presentation/static/api/schema.yaml` produces a diff
  limited to the new `403` entries on the notes-list/create operations, and commit it.
