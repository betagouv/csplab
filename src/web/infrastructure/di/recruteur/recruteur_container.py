from dependency_injector import containers, providers

from application.recruteur.usecases.creer_note import CreerNoteUsecase
from application.recruteur.usecases.editer_note import EditerNoteUsecase
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from application.recruteur.usecases.lister_notes_candidature import (
    ListerNotesCandidatureUsecase,
)
from application.recruteur.usecases.supprimer_note import SupprimerNoteUsecase
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.recruteur.postgres_note_repository import (
    PostgresNoteRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )
    postgres_note_repository = providers.Singleton(PostgresNoteRepository)
    audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=audit_log_repository,
    )

    get_organisme_recruteur_usecase = providers.Factory(
        GetOrganismeRecruteurUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    creer_note_usecase = providers.Factory(
        CreerNoteUsecase,
        note_repository=postgres_note_repository,
        audit_log_writer=audit_log_writer,
    )

    editer_note_usecase = providers.Factory(
        EditerNoteUsecase,
        note_repository=postgres_note_repository,
        audit_log_writer=audit_log_writer,
    )

    supprimer_note_usecase = providers.Factory(
        SupprimerNoteUsecase,
        note_repository=postgres_note_repository,
        audit_log_writer=audit_log_writer,
    )

    lister_notes_candidature_usecase = providers.Factory(
        ListerNotesCandidatureUsecase,
        note_repository=postgres_note_repository,
    )
