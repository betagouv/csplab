# Updating the API Schema

## Why CI failed

The route `api/schema/redoc` reads reads `presentation/static/api/schema.yaml` directly to prevent dynamic DB introspection. This file is static and must be regenerated manually whenever API endpoints change. CI fails when the file is out of sync with the codebase.

## When to regenerate it

Regenerate the schema whenever you:
- Add or remove an endpoint
- Change a serializer (fields, types, validators)
- Change a view's HTTP methods or permissions
- Add or modify `@extend_schema` decorators

## How to regenerate

Run this command from the project root:

```bash
python manage.py spectacular --file presentation/static/api/schema.yaml --validate
```

## Validation

The `--validate` flag checks that the output is valid OpenAPI 3 before writing.
If it reports errors, fix them before committing.
