"""Singleton container for shared services with auto-configuration."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer


class SharedContainerSingleton:
    """Singleton wrapper for SharedContainer with auto-configuration."""

    _container = None

    @classmethod
    def get_container(cls) -> SharedContainer:
        """Get configured container instance."""
        if cls._container is None:
            cls._container = cls._create_configured_container()
        return cls._container

    @classmethod
    def _create_configured_container(cls) -> SharedContainer:
        """Create and configure the shared container."""
        container = SharedContainer()

        env = environ.Env()

        openai_config = OpenAIConfig(
            api_key=cast(str, env.str("TYCHO_OPENROUTER_API_KEY")),
            base_url=cast(HttpUrl, env.str("TYCHO_OPENROUTER_BASE_URL")),
            model=cast(str, env.str("TYCHO_OPENROUTER_EMBEDDING_MODEL")),
        )

        shared_config = SharedConfig(openai_config)
        container.config.override(shared_config)

        return container
