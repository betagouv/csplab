from dependency_injector import containers, providers

from application.identite.usecases.get_utilisateur_details import (
    GetUtilisateurDetailUsecase,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)


class IdentiteContainer(containers.DeclarativeContainer):
    app_config: providers.Dependency = providers.Dependency()
    logger_service: providers.Dependency = providers.Dependency()

    postgres_utilisateur_repository = providers.Singleton(PostgresUtilisateurRepository)

    get_utilisateur_details_usecase = providers.Factory(
        GetUtilisateurDetailUsecase,
        utilisateur_repository=postgres_utilisateur_repository,
    )
