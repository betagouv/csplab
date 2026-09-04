PUBLIC_PATH = "/api"

_RATE_LIMIT_HEADERS = {
    "X-RateLimit-Limit": {
        "schema": {"type": "integer"},
        "description": "Nombre maximal d'appels autorisés sur la fenêtre courante.",
    },
    "X-RateLimit-Remaining": {
        "schema": {"type": "integer"},
        "description": "Nombre d'appels restants sur la fenêtre courante.",
    },
    "X-RateLimit-Reset": {
        "schema": {"type": "integer"},
        "description": (
            "Timestamp Unix (secondes) auquel la fenêtre courante se réinitialise."
        ),
    },
}


def postprocess_add_rate_limit_headers(result, **kwargs):
    """Document the `X-RateLimit-*` headers set by RateLimitHeadersMiddleware.

    These headers are added dynamically by a middleware rather than by the
    views themselves, so drf-spectacular cannot pick them up automatically.
    """
    for path in result.get("paths", {}).values():
        for operation in path.values():
            for response in operation.get("responses", {}).values():
                headers = response.setdefault("headers", {})
                for name, spec in _RATE_LIMIT_HEADERS.items():
                    headers.setdefault(name, dict(spec))
    return result


def preprocess_public_only(endpoints, **kwargs):
    selected_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if path.startswith(PUBLIC_PATH):
            selected_endpoints.append((path, path_regex, method, callback))
    return selected_endpoints


def preprocess_internal_only(endpoints, **kwargs):
    selected_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if not path.startswith(PUBLIC_PATH):
            selected_endpoints.append((path, path_regex, method, callback))
    return selected_endpoints
