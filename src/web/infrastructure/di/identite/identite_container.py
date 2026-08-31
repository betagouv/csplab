from dependency_injector import containers, providers

from application.identite.usecases.create_agent import CreateAgentUsecase
from application.identite.usecases.create_candidat import CreateCandidatUsecase
from application.identite.usecases.create_organisme import CreateOrganismeUsecase
from application.identite.usecases.get_utilisateur_details import (
    GetUtilisateurDetailsUsecase,
)
from application.identite.usecases.list_organismes import ListOrganismesUsecase
from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionUsecase,
)
from application.identite.usecases.update_organisme import UpdateOrganismeUsecase
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.identite.postgres_candidat_repository import (
    PostgresCandidatRepository,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
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
    postgres_organisme_repository = providers.Singleton(PostgresOrganismeRepository)

    get_utilisateur_details_usecase = providers.Factory(
        GetUtilisateurDetailsUsecase,
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
        LogUtilisateurConnexionUsecase, audit_log_writer=audit_log_writer
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

    create_organisme_usecase = providers.Factory(
        CreateOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
        audit_log_writer=audit_log_writer,
    )

    list_organismes_usecase = providers.Factory(
        ListOrganismesUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
    )

    update_organisme_usecase = providers.Factory(
        UpdateOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_permission_service,
        audit_log_writer=audit_log_writer,
    )
