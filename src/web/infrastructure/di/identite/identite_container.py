from dependency_injector import containers, providers

from application.identite.usecases.create_agent import CreateAgentUsecase
from application.identite.usecases.create_candidat import CreateCandidatUsecase
from application.identite.usecases.create_organisme import CreateOrganismeUsecase
from application.identite.usecases.get_utilisateur_details import (
    GetUtilisateurDetailUsecase,
)
from application.identite.usecases.import_etablissements_finess import (
    ImportEtablissementsFinessUsecase,
)
from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.services.identite_permission_service import (
    OrganismeCreationPermissionService,
)
from infrastructure.external_gateways.finess_client import FinessClient
from infrastructure.mappers.organisme_finess_mapper import OrganismeFinessMapper
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.commons.postgres_unit_of_work import (
    PostgresUnitOfWork,
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
    postgres_unit_of_work = providers.Singleton(PostgresUnitOfWork)

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
        LogUtilisateurConnexionUsecase, audit_log_writer=audit_log_writer
    )

    organisme_creation_permission_service = providers.Factory(
        OrganismeCreationPermissionService
    )

    create_organisme_usecase = providers.Factory(
        CreateOrganismeUsecase,
        organisme_repository=postgres_organisme_repository,
        permission_service=organisme_creation_permission_service,
    )

    organisme_finess_mapper = providers.Factory(OrganismeFinessMapper)

    organisme_gateway = providers.Singleton(
        FinessClient, logger=logger_service, organisme_mapper=organisme_finess_mapper
    )

    import_etablissements_finess_usecase = providers.Factory(
        ImportEtablissementsFinessUsecase,
        organisme_gateway=organisme_gateway,
        organisme_repository=postgres_organisme_repository,
        logger=logger_service,
        unit_of_work=postgres_unit_of_work,
        audit_log_writer=audit_log_writer,
    )
