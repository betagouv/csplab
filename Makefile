# CI entry points only. Every dev task lives in mise (see docs/mise.md);
# this file goes away once the CI runs the mise tasks itself (#1214).

WEB_PNPM = cd src/web && pnpm
WEB_UV = cd src/web && direnv exec .
WEB_INTERNAL_API_UV = cd src/web && DJANGO_SETTINGS_MODULE=config.settings.schema_internal direnv exec .
FRONTEND_FILTER = csplab-frontend

lint-web-migrations: ## check no Django migrations are missing
	@echo 'lint:web-migrations started…'
	$(WEB_UV) python manage.py makemigrations --check
.PHONY: lint-web-migrations

lint-schema: ## generate and check API schema is up to date
	@echo 'lint:schema started…'
	$(WEB_UV) python manage.py spectacular --file presentation/static/api/schema.yaml --validate --fail-on-warn
	git diff --exit-code src/web/presentation/static/api/schema.yaml
.PHONY: lint-schema

lint-frontend-types: ## check types are in sync with TypeScript & DRF OpenAPI schemas
	@echo 'lint:internal schema started…'
	$(WEB_INTERNAL_API_UV) python manage.py spectacular --file presentation/static/api/internal-schema.yaml --validate --fail-on-warn
	git diff --exit-code src/web/presentation/static/api/internal-schema.yaml
	@echo 'lint:frontend-types started…'
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) generate-types
	git diff --exit-code src/web/presentation/frontend/src/types/api.d.ts
.PHONY: lint-frontend-types
