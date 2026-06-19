from dependency_injector import containers, providers

from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )
