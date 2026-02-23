"""Test container factory for creating isolated test containers."""

from faker import Faker

from config.app_config import AppConfig
from infrastructure.di.shared.shared_container import SharedContainer
from tests.utils.in_memory_corps_repository import InMemoryCorpsRepository
from tests.utils.in_memory_vector_repository import InMemoryVectorRepository
from tests.utils.mock_embedding_generator import MockEmbeddingGenerator

fake = Faker()


def create_test_shared_container(embedding_fixtures=None):
    """Create SharedContainer configured for testing with in-memory implementations."""
    shared_container = SharedContainer()

    # Create test AppConfig
    test_app_config = AppConfig.from_django_settings()

    shared_container.app_config.override(test_app_config)
    shared_container.corps_repository.override(InMemoryCorpsRepository())
    shared_container.vector_repository.override(InMemoryVectorRepository())

    if embedding_fixtures:
        shared_container.embedding_generator.override(
            MockEmbeddingGenerator(embedding_fixtures)
        )
    else:
        shared_container.embedding_generator.override(MockEmbeddingGenerator({}))

    return shared_container
