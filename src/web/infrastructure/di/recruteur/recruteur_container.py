from dependency_injector import containers, providers

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurUsecase,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsUsecase,
)
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsUsecase,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_repository import (
    PostgresOrganismeRecruteurRepository,
)


class RecruteurContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_organisme_repository = providers.Singleton(PostgresOrganismeRepository)
    postgres_organisme_recruteur_repository = providers.Singleton(
        PostgresOrganismeRecruteurRepository
    )

    get_organisme_recruteur_usecase = providers.Factory(
        GetOrganismeRecruteurUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    initialize_organisme_steps_usecase = providers.Factory(
        InitializeOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_recruteur_repository,
    )

    update_organisme_steps_usecase = providers.Factory(
        UpdateOrganismeStepsUsecase,
        organisme_repository=postgres_organisme_repository,
        organisme_recruteur_repository=postgres_organisme_recruteur_repository,
    )
