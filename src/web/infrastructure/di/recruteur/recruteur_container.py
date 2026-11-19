from dependency_injector import containers, providers

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.usecases.change_etape_candidatures import (
    ChangeEtapeCandidaturesUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
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
from infrastructure.repositories.recruteur import (
    postgres_candidature_recruteur_repository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
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
    postgres_recrutement_agent_repository = providers.Singleton(
        PostgresRecrutementAgentRepository
    )
    organisme_permission_service = providers.Factory(OrganismePermissionService)
    recrutement_mapper = providers.Factory(RecrutementMapper)
    postgres_recrutement_repository = providers.Singleton(
        PostgresRecrutementRepository, mapper=recrutement_mapper
    )

    candidature_recruteur_mapper = providers.Factory(CandidatureRecruteurMapper)
    postgres_candidature_repository = providers.Singleton(
        postgres_candidature_recruteur_repository.PostgresCandidatureRecrutementRepository,
        mapper=candidature_recruteur_mapper,
    )

    change_etape_candidatures_usecase = providers.Factory(
        ChangeEtapeCandidaturesUsecase,
        permission_service=organisme_permission_service,
        recrutement_repository=postgres_recrutement_repository,
        candidature_recruteur_repository=postgres_candidature_repository,
        audit_log_writer=audit_log_writer,
        unit_of_work=postgres_unit_of_work,
    )
