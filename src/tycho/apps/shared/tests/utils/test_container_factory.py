"""Test container factory for creating isolated test containers."""

from apps.shared.containers import SharedContainer
from apps.shared.tests.utils.in_memory_corps_repository import (
    InMemoryCorpsRepository,
)
from apps.shared.tests.utils.in_memory_vector_repository import (
    InMemoryVectorRepository,
)
from apps.shared.tests.utils.mock_embedding_generator import MockEmbeddingGenerator


def create_test_shared_container(embedding_fixtures=None):
    """Create SharedContainer configured for testing with in-memory implementations."""
    shared_container = SharedContainer()

    mock_config = type(
        "MockConfig",
        (),
        {
            "openai": type(
                "OpenAIConfig",
                (),
                {"api_key": "test-key", "model": "text-embedding-ada-002"},
            )()
        },
    )()

    shared_container.config.override(mock_config)
    shared_container.corps_repository.override(InMemoryCorpsRepository())
    shared_container.vector_repository.override(InMemoryVectorRepository())

    if embedding_fixtures:
        shared_container.embedding_generator.override(
            MockEmbeddingGenerator(embedding_fixtures)
        )
    else:
        shared_container.embedding_generator.override(MockEmbeddingGenerator({}))

    return shared_container
