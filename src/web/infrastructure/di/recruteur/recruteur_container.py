from dependency_injector import containers, providers

from application.recruteur.usecases.creer_note import CreerNoteUsecase
from application.recruteur.usecases.editer_note import EditerNoteUsecase
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsUsecase,
)
from application.recruteur.usecases.lister_notes_candidature import (
    ListerNotesCandidatureUsecase,
)
from application.recruteur.usecases.supprimer_note import SupprimerNoteUsecase
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from infrastructure.mappers.candidature_mapper import CandidatureMapper
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
from infrastructure.repositories.recruteur.postgres_note_query_service import (
    PostgresNoteQueryService,
)
from infrastructure.repositories.recruteur.postgres_note_repository import (
    PostgresNoteRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_query_service import (
    PostgresRecrutementQueryService,
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
    postgres_organisme_agent_repository = providers.Singleton(
        PostgresOrganismeAgentRepository
    )
    organisme_permission_service = providers.Factory(
        OrganismePermissionService,
        organisme_agent_repository=postgres_organisme_agent_repository,
    )
    candidature_mapper = providers.Factory(CandidatureMapper)
    postgres_recrutement_query_service = providers.Singleton(
        PostgresRecrutementQueryService
    )
    postgres_note_repository = providers.Singleton(PostgresNoteRepository)
    postgres_note_query_service = providers.Singleton(PostgresNoteQueryService)
    postgres_candidature_repository = providers.Singleton(
        PostgresCandidatureRepository,
        mapper=candidature_mapper,
    )
    postgres_agent_repository = providers.Singleton(PostgresAgentRepository)

    creer_note_usecase = providers.Factory(
        CreerNoteUsecase,
        note_repository=postgres_note_repository,
        candidature_repository=postgres_candidature_repository,
        agent_repository=postgres_agent_repository,
        audit_log_writer=audit_log_writer,
    )

    lister_notes_candidature_usecase = providers.Factory(
        ListerNotesCandidatureUsecase,
        note_query_service=postgres_note_query_service,
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
        organisme_permission_service=organisme_permission_service,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
        organisme_permission_service=organisme_permission_service,
    )

    update_organisme_steps_usecase = providers.Factory(
        UpdateOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_repository,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
        organisme_permission_service=organisme_permission_service,
    )

    lister_mes_recrutements_usecase = providers.Factory(
        ListerMesRecrutementsUsecase,
        recrutement_query_service=postgres_recrutement_query_service,
        organisme_repository=postgres_organisme_repository,
        organisme_permission_service=organisme_permission_service,
        logger=logger_service,
    )

    get_recrutement_kanban_usecase = providers.Factory(
        GetRecrutementKanbanUsecase,
        organisme_repository=postgres_organisme_repository,
        organisme_permission_service=organisme_permission_service,
    )
