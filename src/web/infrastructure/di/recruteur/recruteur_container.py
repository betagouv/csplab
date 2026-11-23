from dependency_injector import containers, providers

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_agent_repository import (  # noqa: E501
    PostgresRecrutementAgentRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=postgres_audit_log_repository,
    )
    postgres_recrutement_agent_repository = providers.Singleton(
        PostgresRecrutementAgentRepository
    )
    organisme_permission_service = providers.Factory(OrganismePermissionService)
