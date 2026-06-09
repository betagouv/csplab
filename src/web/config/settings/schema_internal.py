from config.settings.base import *  # noqa: F403

SPECTACULAR_SETTINGS = {
    **SPECTACULAR_SETTINGS,  # noqa: F405
    "TITLE": "CSPLab Internal API",
    "DESCRIPTION": "",
    "TAGS": [
        {"name": "utilisateurs", "description": "Gestion des utilisateurs"},
    ],
    "PREPROCESSING_HOOKS": [
        "drf_spectacular.hooks.preprocess_exclude_path_format",
        "presentation.api.openapi_hooks.preprocess_internal_only",
    ],
}
