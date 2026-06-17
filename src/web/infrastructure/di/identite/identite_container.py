from dependency_injector import containers, providers

from application.identite.usecases.create_agent import CreateAgentUsecase
from application.identite.usecases.create_candidat import CreateCandidatUsecase
from application.identite.usecases.get_utilisateur_details import (
    GetUtilisateurDetailUsecase,
)
from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionUsecase,
)
from domain.audit.services.audit_log_writer import AuditLogWriter
from infrastructure.repositories.audit.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.identite.postgres_candidat_repository import (
    PostgresCandidatRepository,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)


class IdentiteContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_utilisateur_repository = providers.Singleton(PostgresUtilisateurRepository)
    postgres_agent_repository = providers.Singleton(PostgresAgentRepository)
    postgres_candidat_repository = providers.Singleton(PostgresCandidatRepository)
    postgres_audit_log_repository = providers.Singleton(PostgresAuditLogRepository)

    audit_log_writer = providers.Factory(
        AuditLogWriter,
        repository=postgres_audit_log_repository,
    )

    get_utilisateur_details_usecase = providers.Factory(
        GetUtilisateurDetailUsecase,
        utilisateur_repository=postgres_utilisateur_repository,
    )

    create_agent_usecase = providers.Factory(
        CreateAgentUsecase,
        agent_repository=postgres_agent_repository,
        utilisateur_repository=postgres_utilisateur_repository,
    )

    create_candidat_usecase = providers.Factory(
        CreateCandidatUsecase,
        candidat_repository=postgres_candidat_repository,
        utilisateur_repository=postgres_utilisateur_repository,
    )

    log_utilisateur_connexion_usecase = providers.Factory(
        LogUtilisateurConnexionUsecase,
        audit_log_writer=audit_log_writer,
    )
