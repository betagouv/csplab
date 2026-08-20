from dependency_injector import containers, providers

from application.recruteur.usecases.changer_etape_candidatures import (
    ChangerEtapeCandidaturesUsecase,
)
from application.recruteur.usecases.creer_note import CreerNoteUsecase
from application.recruteur.usecases.editer_note import EditerNoteUsecase
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.get_recrutement_detail import (
    GetRecrutementDetailUsecase,
)
from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesUsecase,
)
from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanUsecase,
)
from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeUsecase,
)
from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesUsecase,
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
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from infrastructure.mappers.candidature_recruteur_mapper import (
    CandidatureRecruteurMapper,
)
from infrastructure.mappers.recrutement_mapper import RecrutementMapper
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.commons.postgres_unit_of_work import (
    PostgresUnitOfWork,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.recruteur import (
    postgres_candidature_recruteur_repository,
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
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_query_service import (
    PostgresRecrutementQueryService,
)
from infrastructure.repositories.recruteur.postgres_recrutement_repository import (
    PostgresRecrutementRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_unit_of_work = providers.Singleton(PostgresUnitOfWork)

    postgres_audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=postgres_audit_log_repository,
    )
    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )
    postgres_organisme_agent_repository = providers.Singleton(
        PostgresOrganismeAgentRepository
    )
    postgres_recrutement_agent_repository = providers.Singleton(
        PostgresRecrutementAgentRepository
    )
    organisme_permission_service = providers.Factory(
        OrganismePermissionService,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        organisme_agent_repository=postgres_organisme_agent_repository,
        recrutement_agent_repository=postgres_recrutement_agent_repository,
    )
    recrutement_mapper = providers.Factory(RecrutementMapper)
    postgres_recrutement_query_service = providers.Singleton(
        PostgresRecrutementQueryService
    )
    postgres_recrutement_repository = providers.Singleton(
        PostgresRecrutementRepository, mapper=recrutement_mapper
    )
    postgres_note_repository = providers.Singleton(PostgresNoteRepository)
    postgres_note_query_service = providers.Singleton(PostgresNoteQueryService)

    candidature_recruteur_mapper = providers.Factory(CandidatureRecruteurMapper)
    postgres_candidature_repository = providers.Singleton(
        postgres_candidature_recruteur_repository.PostgresCandidatureRecrutementRepository,
        mapper=candidature_recruteur_mapper,
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
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        organisme_permission_service=organisme_permission_service,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        organisme_permission_service=organisme_permission_service,
    )

    update_organisme_steps_usecase = providers.Factory(
        UpdateOrganismeStepsUsecase,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
        organisme_permission_service=organisme_permission_service,
    )

    lister_mes_recrutements_usecase = providers.Factory(
        ListerMesRecrutementsUsecase,
        recrutement_query_service=postgres_recrutement_query_service,
        organisme_permission_service=organisme_permission_service,
        logger=logger_service,
    )

    get_recrutement_detail_usecase = providers.Factory(
        GetRecrutementDetailUsecase,
        organisme_permission_service=organisme_permission_service,
        recrutement_query_service=postgres_recrutement_query_service,
    )

    get_recrutement_kanban_usecase = providers.Factory(
        GetRecrutementKanbanUsecase,
        organisme_permission_service=organisme_permission_service,
        recrutement_query_service=postgres_recrutement_query_service,
    )

    get_recrutement_liste_usecase = providers.Factory(
        GetRecrutementListeUsecase,
        organisme_permission_service=organisme_permission_service,
        recrutement_query_service=postgres_recrutement_query_service,
    )

    get_recrutement_etapes_usecase = providers.Factory(
        GetRecrutementEtapesUsecase,
        organisme_permission_service=organisme_permission_service,
    )

    update_recrutement_etapes_usecase = providers.Factory(
        UpdateRecrutementEtapesUsecase,
        organisme_permission_service=organisme_permission_service,
    )

    init_recrutement_etapes_usecase = providers.Factory(
        InitRecrutementEtapesUsecase,
        permission_service=organisme_permission_service,
        recrutement_repository=postgres_recrutement_repository,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
    )
    changer_etape_candidatures_usecase = providers.Factory(
        ChangerEtapeCandidaturesUsecase,
        permission_service=organisme_permission_service,
        recrutement_repository=postgres_recrutement_repository,
        candidature_recruteur_repository=postgres_candidature_repository,
        audit_log_writer=audit_log_writer,
        unit_of_work=postgres_unit_of_work,
    )
