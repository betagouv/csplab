from functools import lru_cache
from typing import Any

import jsonschema
from drf_spectacular.generators import SchemaGenerator


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
    resolver = jsonschema.RefResolver.from_schema(schema)
    jsonschema.validate(instance=data, schema=response_schema, resolver=resolver)
