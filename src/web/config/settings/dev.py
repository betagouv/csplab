from config.settings.base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS += ["localhost", "127.0.0.1", "192.168.0.1", "0.0.0.0"]  # noqa S104

# placeholder for dev logger setup

# Debug Toolbar Settings
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS.insert(  # noqa: F405
    INSTALLED_APPS.index("django.contrib.staticfiles"),  # noqa: F405
    "whitenoise.runserver_nostatic",
)
INSTALLED_APPS.extend(  # noqa: F405
    [
        "debug_toolbar",
        "django_browser_reload",
        "django_extensions",
    ]
)

if env.bool("DEBUG_TOOLBAR", default=True):  # noqa F405
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    # https://django-debug-toolbar.readthedocs.io/en/latest/panels.html#panels
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # ProfilingPanel makes the django admin extremely slow...
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
    "SHOW_COLLAPSED": True,
}

# Use simple static files storage for development (no compression/manifest)
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

SENTRY_DNS = "example.com"

# Allow logging into the admin with a plain superuser, without a TOTP device.
ADMIN_OTP_REQUIRED = False

HUEY["immediate"] = True  # noqa: F405
HUEY["consumer"]["periodic"] = False  # noqa: F405
AUTH_PASSWORD_VALIDATORS = []
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = []  # noqa: F405

# CSP overrides for Vite dev server
_vite_origin = VITE_DEV_ORIGIN  # noqa: F405
_vite_ws_origin = _vite_origin.replace("https://", "wss://").replace("http://", "ws://")
SECURE_CSP["script-src"] = [*SECURE_CSP["script-src"], _vite_origin]  # noqa: F405
SECURE_CSP["script-src-elem"] = [  # noqa: F405
    *SECURE_CSP["script-src-elem"],  # noqa: F405
    _vite_origin,
]
SECURE_CSP["connect-src"] = [  # noqa: F405
    *SECURE_CSP["connect-src"],  # noqa: F405
    _vite_origin,
    _vite_ws_origin,
]
SECURE_CSP["style-src"] = ["'self'", "'unsafe-inline'"]  # noqa: F405
SECURE_CSP["style-src-elem"] = ["'self'", "'unsafe-inline'"]  # noqa: F405
SECURE_CSP["font-src"] = [*SECURE_CSP["font-src"], _vite_origin]  # noqa: F405
