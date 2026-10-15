from dependency_injector import containers, providers

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.identite.usecases.create_organisme import CreateOrganismeUsecase
from application.identite.usecases.get_organisme import GetOrganismeUsecase
from application.identite.usecases.update_organisme import UpdateOrganismeUsecase
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)


class IdentiteContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_utilisateur_repository = providers.Singleton(PostgresUtilisateurRepository)
    postgres_audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=postgres_audit_log_repository,
    )
    postgres_organisme_repository = providers.Singleton(PostgresOrganismeRepository)

    organisme_permission_service = providers.Factory(OrganismePermissionService)

    create_organisme_usecase = providers.Factory(
        CreateOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
        audit_log_writer=audit_log_writer,
    )

    get_organisme_usecase = providers.Factory(
        GetOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
    )

    update_organisme_usecase = providers.Factory(
        UpdateOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
        audit_log_writer=audit_log_writer,
    )
