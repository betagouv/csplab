# Updating the API Schema

## Why CI failed

The route `api/schema/redoc` reads `presentation/static/api/schema.yaml` directly to prevent dynamic DB introspection. This file is static and must be regenerated manually whenever API endpoints change. CI fails when the file is out of sync with the codebase.

## When to regenerate it

Regenerate the schema whenever you:
- Add or remove an endpoint
- Change a serializer (fields, types, validators)
- Change a view's HTTP methods or permissions
- Add or modify `@extend_schema` decorators

## Schema split

Endpoints are split by tag via preprocessing hooks in `presentation/api/openapi_hooks.py`:

| Route | Schema file |
|-----|-------------|
| starts with `/api` | `schema.yaml` (public) |
| does not start with `/api` | `internal-schema.yaml` (internal) |
| decorated with `@extend_schema(exclude=True)` | excluded from both |


## How to regenerate

```bash
# Public schema
bin/manage spectacular --file presentation/static/api/schema.yaml

# Internal schema
DJANGO_SETTINGS_MODULE=config.settings.schema_internal \
  bin/manage spectacular --file presentation/static/api/internal-schema.yaml --validate
```

## Validation

The `--validate` flag checks that the output is valid OpenAPI 3 before writing.
If it reports errors, fix them before committing.
