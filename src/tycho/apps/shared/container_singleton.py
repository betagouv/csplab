"""Singleton container for shared services with auto-configuration."""

from typing import cast

import environ
from pydantic import HttpUrl

from apps.shared.config import OpenAIConfig, SharedConfig
from apps.shared.containers import SharedContainer


class SharedContainerSingleton:
    """Singleton wrapper for SharedContainer with auto-configuration."""

    _instance = None
    _container = None

    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_container(self) -> SharedContainer:
        """Get configured container instance."""
        if self._container is None:
            self._container = self._create_configured_container()
        return self._container

    def _create_configured_container(self) -> SharedContainer:
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


_shared_singleton = SharedContainerSingleton()


def get_shared_container() -> SharedContainer:
    """Get the configured shared container singleton."""
    return _shared_singleton.get_container()
