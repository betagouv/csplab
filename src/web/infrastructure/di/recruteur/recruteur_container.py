from dependency_injector import containers, providers

from application.recruteur.usecases.creer_note import CreerNoteUsecase
from application.recruteur.usecases.editer_note import EditerNoteUsecase
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from application.recruteur.usecases.supprimer_note import SupprimerNoteUsecase
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.repositories.candidate.postgres_candidature_repository import (
    PostgresCandidatureRepository,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
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

    postgres_audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=postgres_audit_log_repository,
    )
    postgres_organisme_repository = providers.Singleton(PostgresOrganismeRepository)
    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )
    postgres_note_repository = providers.Singleton(PostgresNoteRepository)
    postgres_candidature_repository = providers.Singleton(PostgresCandidatureRepository)
    postgres_agent_repository = providers.Singleton(PostgresAgentRepository)

    creer_note_usecase = providers.Factory(
        CreerNoteUsecase,
        note_repository=postgres_note_repository,
        candidature_repository=postgres_candidature_repository,
        agent_repository=postgres_agent_repository,
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

    get_organisme_recruteur_usecase = providers.Factory(
        GetOrganismeRecruteurUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    update_organisme_steps_usecase = providers.Factory(
        UpdateOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_repository,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
    )
