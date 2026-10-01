from collections.abc import Iterator

from django.urls import URLPattern, URLResolver, get_resolver


def _route_names(patterns, namespace: str = "") -> Iterator[str]:
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            child_namespace = (
                f"{namespace}{pattern.namespace}:" if pattern.namespace else namespace
            )
            yield from _route_names(pattern.url_patterns, child_namespace)
        elif isinstance(pattern, URLPattern) and pattern.name:
            yield f"{namespace}{pattern.name}"


def test_route_names_use_snake_case():
    invalid = sorted(
        name for name in _route_names(get_resolver().url_patterns) if "-" in name
    )
    assert invalid == [], f"Noms de routes à écrire en snake_case : {invalid}"
