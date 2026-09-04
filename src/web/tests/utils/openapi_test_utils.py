from functools import lru_cache
from typing import Any

import jsonschema
from drf_spectacular.generators import SchemaGenerator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


def _resolve_nullable(node: Any) -> Any:
    """Rewrite OpenAPI 3.0's `nullable: true` into a form plain JSON Schema
    (as used by the `jsonschema` package) understands, since `nullable` is an
    OpenAPI-only keyword that `jsonschema` silently ignores otherwise."""
    if isinstance(node, dict):
        rewritten = {
            k: _resolve_nullable(v) for k, v in node.items() if k != "nullable"
        }
        if node.get("nullable") is True:
            return {"anyOf": [rewritten, {"type": "null"}]}
        return rewritten
    if isinstance(node, list):
        return [_resolve_nullable(v) for v in node]
    return node


@lru_cache
def _generated_schema() -> dict:
    schema = SchemaGenerator().get_schema(request=None, public=True)
    return _resolve_nullable(schema)


@lru_cache
def _schema_resolver() -> Any:
    """Resolver used to follow the OpenAPI schema's internal `$ref`s (e.g. to
    `#/components/schemas/...`) when validating a response fragment on its own."""
    schema = _generated_schema()
    resource = Resource.from_contents(schema, default_specification=DRAFT202012)
    registry = Registry().with_resource("", resource)
    return registry.resolver()


def assert_matches_openapi_schema(
    data: Any, path: str, method: str = "get", status_code: str = "200"
) -> None:
    """Assert that `data` (a decoded JSON response body) validates against the
    OpenAPI schema generated for `method`/`path`/`status_code`.

    This is the counterpart of merely checking a few response fields by hand: it
    fails as soon as the real response drifts from what the published schema
    promises (missing/extra field, wrong type, wrong nullability...).
    """
    schema = _generated_schema()
    response_schema = schema["paths"][path][method.lower()]["responses"][
        str(status_code)
    ]["content"]["application/json"]["schema"]
    validator = jsonschema.Draft202012Validator(
        response_schema, _resolver=_schema_resolver()
    )
    validator.validate(data)
