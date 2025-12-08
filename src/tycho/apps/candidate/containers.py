"""Candidate dependency injection container."""

from dependency_injector import containers, providers

from apps.candidate.application.usecases.retrieve_corps import RetrieveCorpsUsecase


class CandidateContainer(containers.DeclarativeContainer):
    """Candidate services container."""

    logger_service: providers.Dependency = providers.Dependency()

    shared_container = providers.DependenciesContainer()

    corps_repository = shared_container.corps_repository
    embedding_generator = shared_container.embedding_generator
    vector_repository = shared_container.vector_repository

    retrieve_corps_usecase = providers.Factory(
        RetrieveCorpsUsecase,
        vector_repository=vector_repository,
        embedding_generator=embedding_generator,
        corps_repository=corps_repository,
        logger=logger_service,
    )
