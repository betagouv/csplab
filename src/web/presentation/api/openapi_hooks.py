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


_TOO_MANY_REQUESTS_RESPONSE = {
    "description": "Nombre maximal d'appels autorisés dépassé.",
    "content": {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": (
                            "Request was throttled. Expected available in 42 seconds."
                        ),
                    },
                },
            },
        },
    },
    "headers": {
        "Retry-After": {
            "schema": {"type": "integer"},
            "description": "Nombre de secondes à attendre avant de pouvoir réessayer.",
        },
        **{name: dict(spec) for name, spec in _RATE_LIMIT_HEADERS.items()},
    },
}


def postprocess_add_too_many_requests_response(result, **kwargs):
    """Document the `429` response returned once an endpoint's rate limit is hit.

    Every endpoint goes through DRF's DEFAULT_THROTTLE_CLASSES (see
    REST_FRAMEWORK settings), which can raise a 429 regardless of what the
    view itself declares, so drf-spectacular cannot pick it up automatically.
    """
    for path in result.get("paths", {}).values():
        for operation in path.values():
            responses = operation.get("responses")
            if responses is None:
                continue
            responses.setdefault("429", dict(_TOO_MANY_REQUESTS_RESPONSE))
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
