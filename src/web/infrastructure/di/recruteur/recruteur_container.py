from dependency_injector import containers, providers

from application.recruteur.usecases.get_my_recruits_by_type import (
    GetMyRecruitsByTypeUsecase,
)
from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.identite.postgres_candidat_repository import (
    PostgresCandidatRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)
from infrastructure.repositories.recruteur.postgres_recrutement_repository import (
    PostgresRecrutementRepository,
)
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )
    postgres_recrutement_repository = providers.Singleton(PostgresRecrutementRepository)
    postgres_offers_repository = providers.Singleton(
        PostgresOffersRepository,
        logger=logger_service,
    )
    postgres_agent_repository = providers.Singleton(PostgresAgentRepository)
    postgres_candidat_repository = providers.Singleton(PostgresCandidatRepository)

    get_organisme_recruteur_usecase = providers.Factory(
        GetOrganismeRecruteurUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    get_my_recruits_by_type_usecase = providers.Factory(
        GetMyRecruitsByTypeUsecase,
        recrutements_repository=postgres_recrutement_repository,
        offers_repository=postgres_offers_repository,
        agents_repository=postgres_agent_repository,
        candidat_repository=postgres_candidat_repository,
    )
