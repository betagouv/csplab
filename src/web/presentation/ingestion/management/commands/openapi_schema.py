from drf_spectacular.management.commands.spectacular import (
    Command as SpectacularCommand,
)

from presentation.api.openapi_renderers import Yaml12SafeOpenApiRenderer


class Command(SpectacularCommand):
    help = "Like `spectacular`, but quotes digit-only strings for YAML 1.2 readers."

    def get_renderer(self, format):
        if format == "openapi":
            return Yaml12SafeOpenApiRenderer()
        return super().get_renderer(format)
