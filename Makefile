# -- General
SHELL := /bin/bash

# -- Docker
COMPOSE                 = docker compose
COMPOSE_UP              = $(COMPOSE) up -d --remove-orphans

WEB_PNPM = cd src/web && pnpm
WEB_UV = cd src/web && direnv exec .
WEB_INTERNAL_API_UV = cd src/web && DJANGO_SETTINGS_MODULE=config.settings.schema_internal direnv exec .
OCR_UV = cd src/ocr && direnv exec .
INGESTION_UV = cd src/ingestion && direnv exec .
NOTEBOOK_UV = cd src/notebook && direnv exec .
DEV_UV = cd dev && direnv exec .
DDD_UV = cd libs/ddd &&
REFERENTIEL_UV = cd libs/referentiel &&

default: help

## -- Files
.pre-commit-cache:
	mkdir .pre-commit-cache

.git/hooks/pre-commit:
	cp bin/git-pre-commit-hook .git/hooks/pre-commit

.git/hooks/commit-msg:
	cp bin/git-commit-msg-hook .git/hooks/commit-msg

### BOOTSTRAP
setup: ## copy example env files to local files
	@cp src/web/.envrc.sample src/web/.envrc
	@cp src/notebook/.envrc.sample src/notebook/.envrc
	@cp src/ocr/.envrc.sample src/ocr/.envrc
	@cp src/ingestion/.envrc.sample src/ingestion/.envrc
	@cp env.d/web-example env.d/web
	@cp env.d/ocr-example env.d/ocr
	@cp env.d/notebook-example env.d/notebook
	@cp env.d/ingestion-example env.d/ingestion
	@cp env.d/postgresql-example env.d/postgresql
	@cp env.d/redis-example env.d/redis
	@cd src/web && direnv allow
	@cd src/ocr && direnv allow
	@cd src/notebook && direnv allow
	@cd src/ingestion && direnv allow
	@echo "✅ Environment files copied. Please edit env.d/* with your actual values."
.PHONY: setup

bootstrap: ## setup development environment (build dev service and install git hooks)
bootstrap: \
  run-postgres \
  run-redis \
  run-qdrant \
  build \
  frontend-install \
  setup-qdrant \
  migrate \
  migrate-ingestion \
  create-ingestion-test-db \
  create-superuser \
  jupytext--to-ipynb \
  playwright-install
.PHONY: bootstrap

git-hooks: ## install pre-commit hook
git-hooks: \
  .pre-commit-cache \
  .git/hooks/pre-commit \
  .git/hooks/commit-msg
.PHONY: git-hooks

### BUILD
build: ## build services image
build: \
  build-ddd \
  build-referentiel \
  build-dev \
  build-web \
  build-ocr \
  build-notebook \
  build-ingestion
.PHONY: build

build-ddd: ## setup ddd package
	@$(DDD_UV) uv sync --group dev --locked
.PHONY: build-ddd

build-referentiel: ## setup referentiel package
	@$(REFERENTIEL_UV) uv sync --group dev
.PHONY: build-referentiel

build-dev: ## build development environment image
	@$(DEV_UV) uv sync --locked
.PHONY: build-dev

build-notebook: ### setup notebook kernels natively
	@$(NOTEBOOK_UV) uv sync --locked
.PHONY: build-notebook

build-ingestion: ### setup ingestion API
	@$(INGESTION_UV) uv sync --locked
.PHONY: build-ingestion

build-web: ## build web image
	# not using @ which suppress the command's echoing in terminal
	$(WEB_UV) uv sync --group dev --locked
.PHONY: build-web

build-ocr:
	$(OCR_UV) uv sync --group dev --locked
.PHONY: build-ocr
playwright-install: ## install Playwright browsers
	@echo 'Installing Playwright browsers…'
	$(WEB_UV) uv run playwright install chromium
.PHONY: playwright-install

jupytext--to-md: ## convert local ipynb files into md
	cd src/notebook && uv run jupytext --to md *.ipynb && cd ../..
.PHONY: jupytext--to-md

jupytext--to-ipynb: ## convert remote md files into ipynb
	cd src/notebook && uv run jupytext --to ipynb *.md && cd ../..
.PHONY: jupytext--to-ipynb

NOTEBOOK ?=  ## optional: path to a .ipynb file to export (exports all src/notebook/*.ipynb if unset)
FORMAT ?= html  ## output format: html (default, interactive Plotly) | markdown

publish-notebooks: ## export notebooks to docs/notebook/ (usage: make publish-notebooks [NOTEBOOK=src/notebook/name.ipynb] [FORMAT=html|markdown])
	@bin/publish-notebooks $(NOTEBOOK) $(FORMAT)
.PHONY: publish-notebooks

### LOGS
logs: ## display all services logs (follow mode)
	@$(COMPOSE) logs -f
.PHONY: logs

migrate: ## migrate web database
	@echo "Migrating web database…"
	@bin/manage migrate
.PHONY: migrate

create-ingestion-db: ## create the ingestion PostgreSQL user and database
	@echo "Creating ingestion database and user…"
	@set -a && source env.d/postgresql && docker exec -i csp_postgresql psql -U $$POSTGRES_USER < infra/postgres/create-ingestion-db.sql
.PHONY: create-ingestion-db

create-ingestion-test-db: ## create the ingestion_test PostgreSQL database
create-ingestion-test-db: \
  create-ingestion-db
	@echo "Creating ingestion_test database…"
	@set -a && source env.d/postgresql && docker exec -i csp_postgresql psql -U $$POSTGRES_USER < infra/postgres/create-ingestion-test-db.sql
.PHONY: create-ingestion-test-db

DUMP ?=  ## optional: path to a .tar.gz dump file (auto-picks latest in dumps/ if unset)

restore-web-db: ## restore web database from a Scalingo dump — auto-picks latest if DUMP is unset (usage: make restore-web-db [DUMP=dumps/myfile.tar.gz])
	@bin/restore-web-db $(DUMP)
.PHONY: restore-web-db

migrate-ingestion: ## run ingestion database migrations (alembic upgrade head)
migrate-ingestion: \
  create-ingestion-db
	@echo "Migrating ingestion database…"
	@$(INGESTION_UV) uv run alembic upgrade head
.PHONY: migrate-ingestion

migration-ingestion: ## generate a new ingestion migration (ARGS="description of change")
	@$(INGESTION_UV) uv run alembic revision --autogenerate -m "$(ARGS)"
.PHONY: migration-ingestion

create-superuser: ## create web super user
	@echo "Creating web super user…"
	@bin/manage createsuperuser --noinput || true
.PHONY: create-superuser

setup-qdrant: ## setup qdrant collection if not exists
	@echo "Setting up Qdrant collection…"
	@$(WEB_UV) python config/setup-qdrant.py
.PHONY: setup-qdrant

### SASS
sass-compile: ## compile SCSS files to CSS
	@bin/sass compile
.PHONY: sass-compile

sass-watch: ## watch and compile SCSS files on changes
	@bin/sass watch
.PHONY: sass-watch

### FRONTEND (Vue/Vite)
FRONTEND_FILTER = csplab-frontend

frontend-install: ## install frontend dependencies (pnpm)
	$(WEB_PNPM) install
.PHONY: frontend-install

frontend-dev: ## run frontend dev server (Vite HMR)
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) dev
.PHONY: frontend-dev

frontend-build: ## build frontend for production
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) build
.PHONY: frontend-build

frontend-lint: ## lint frontend sources
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) lint
.PHONY: frontend-lint

frontend-lint-fix: ## lint and fix frontend sources
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) lint:fix
.PHONY: frontend-lint-fix

storybook: ## run Storybook dev server (port 6006)
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) storybook
.PHONY: storybook

storybook-build: ## build Storybook static output
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) build-storybook
.PHONY: storybook-build

frontend-types: ## generate TypeScript types from OpenAPI schema
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) generate-types
.PHONY: frontend-types

### RUN
run-notebook: ## run the notebook service
	$(NOTEBOOK_UV) jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
.PHONY: run-notebook

run-postgres: ## run the DB service
	set -a && source env.d/postgresql && $(COMPOSE_UP) postgresql
.PHONY: run-postgres

run-qdrant: ## run the Qdrant vector database service
	$(COMPOSE_UP) qdrant
.PHONY: run-qdrant

run-redis: ## run the redis service
	set -a && source env.d/redis && $(COMPOSE_UP) redis
.PHONY: run-redis

run-web: ## run the web service
	@bin/manage runserver
.PHONY: run-web

run-huey: ## run the task queue
	@bin/manage run_huey
.PHONY: run-huey

run-ocr: ## run the ocr service
	$(OCR_UV) uvicorn api.main:app --reload --port=8001
.PHONY: run-ocr

run-ingestion: ## run the ingestion service (web + celery worker + flower)
	@trap 'kill 0' EXIT; \
	$(INGESTION_UV) uvicorn api.main:app --reload --port=8002 & \
	$(INGESTION_UV) bin/start_worker.sh & \
	$(INGESTION_UV) bin/start_flower.sh & \
	wait
.PHONY: run-ingestion

dev: ## run web with sass watch and browser auto-reload
	@rm -rf src/web/static_collected/
	@echo "🚀 Starting development server with auto-reload…"
	@echo "   Press Ctrl+C to stop all processes"
	@trap 'kill 0' EXIT; \
	bin/sass watch & \
	bin/manage runserver
.PHONY: dev

run-mvp: ## run web + ocr + ingestion + huey with unified logs
	@echo "🚀 Démarrage des services frontend web + ocr + ingestion…"
	@echo "   Huey is immediate, without periodic task in dev"
	@echo "   Appuyez sur Ctrl+C pour arrêter tous les services"
	@echo "   Web: http://localhost:8000"
	@echo "   OCR: http://localhost:8001"
	@echo "   Ingestion: http://localhost:8002"
	@echo "   Celery Flower: http://localhost:8002/flower"
	@trap 'kill 0' EXIT; \
	bin/manage runserver & \
	make run-ocr & \
	echo "⏳ En attente que le service web soit prêt sur :8000…"; \
	until curl -s http://localhost:8000/ > /dev/null 2>&1; do sleep 0.5; done; \
	echo "✅ Service web prêt, démarrage de l'ingestion…"; \
	make run-ingestion & \
	wait
.PHONY: run-mvp

## LINT
# -- Global linting
lint: ## lint all sources
lint: \
  lint-ddd \
  lint-referentiel \
  lint-notebook \
  lint-web \
  lint-ocr \
  lint-ingestion \
  lint-schema \
  lint-internal-schema \
  frontend-lint
.PHONY: lint

lint-fix: ## lint and fix all sources
lint-fix: \
  lint-ddd-fix \
  lint-referentiel-fix \
  lint-notebook-fix \
  lint-web-fix \
  lint-ocr-fix \
  lint-ingestion-fix
.PHONY: lint-fix

lint-ddd: ## lint ddd python sources with ruff
	@echo 'lint:ddd started…'
	$(DDD_UV) uv run ruff check .
	$(DDD_UV) uv run ruff format --check .
.PHONY: lint-ddd

lint-ddd-fix: ## lint and fix ddd python sources with ruff
	@echo 'lint:ddd-fix started…'
	$(DDD_UV) uv run ruff check --fix .
	$(DDD_UV) uv run ruff format .
.PHONY: lint-ddd-fix

lint-referentiel: ## lint referentiel python sources with ruff
	@echo 'lint:referentiel started…'
	$(REFERENTIEL_UV) uv run ruff check .
	$(REFERENTIEL_UV) uv run ruff format --check .
.PHONY: lint-referentiel

lint-referentiel-fix: ## lint and fix referentiel python sources with ruff
	@echo 'lint:referentiel-fix started…'
	$(REFERENTIEL_UV) uv run ruff check --fix .
	$(REFERENTIEL_UV) uv run ruff format .
.PHONY: lint-referentiel-fix

# -- Per-service linting
lint-notebook: ## lint notebook python sources
	@echo 'lint:notebook started (warnings only)…'
	$(NOTEBOOK_UV) ruff check . || true
	$(NOTEBOOK_UV) ruff format --check . || true
.PHONY: lint-notebook

lint-notebook-fix: ## lint and fix notebook python sources
	@echo 'lint:notebook-fix started (warnings only)…'
	$(NOTEBOOK_UV) ruff check --fix . || true
	$(NOTEBOOK_UV) ruff format . || true
.PHONY: lint-notebook-fix

lint-web: ## lint web python sources
lint-web: \
	lint-web-candidate-js \
	lint-web-styles \
  lint-web-ruff \
  lint-web-djlint \
  lint-web-mypy \
  lint-web-migrations
.PHONY: lint-web

lint-web-fix: ## lint and fix web python sources
lint-web-fix: \
	lint-web-styles-fix \
	lint-web-candidate-js-fix \
  lint-web-ruff-fix \
  lint-web-djlint-fix \
  lint-web-mypy
.PHONY: lint-web-fix

lint-web-candidate-js: ## lint candidate app JS sources with ESLint
	@echo 'lint:web-candidate-js started…'
	$(WEB_PNPM) run lint:candidate-js
.PHONY: lint-web-candidate-js

lint-web-candidate-js-fix: ## lint and fix candidate app JS sources with ESLint
	@echo 'lint:web-candidate-js-fix started…'
	$(WEB_PNPM) run lint:candidate-js:fix || true
.PHONY: lint-web-candidate-js-fix

lint-web-styles: ## lint Django app SCSS sources with ESLint
	@echo 'lint:web-styles started…'
	$(WEB_PNPM) run lint:styles
.PHONY: lint-web-styles

lint-web-styles-fix: ## lint, fix, and compile Django app SCSS sources
	@echo 'lint:web-styles-fix started…'
	$(WEB_PNPM) run lint:styles:fix
	@bin/sass compile
.PHONY: lint-web-styles-fix

lint-web-ruff: ## lint web python sources with ruff (check only, like CI)
	@echo 'lint:web-ruff started…'
	$(WEB_UV) ruff check .
	$(WEB_UV) ruff format --check .
.PHONY: lint-web-ruff

lint-web-ruff-fix: ## lint and fix web python sources with ruff
	@echo 'lint:web-ruff-fix started…'
	$(WEB_UV) ruff check --fix .
	$(WEB_UV) ruff format .
.PHONY: lint-web-ruff-fix

lint-web-djlint: ## lint web template sources with djlint
	@echo 'lint:web-djlint started…'
	$(WEB_UV) djlint presentation/templates --check
.PHONY: lint-web-djlint

lint-web-djlint-fix: ## lint and fix web template sources with djlint
	@echo 'lint:web-djlint-fix started…'
	$(WEB_UV) djlint presentation/templates --reformat
.PHONY: lint-web-djlint-fix

lint-web-mypy: ## lint web python sources with mypy
	@echo 'lint:web-mypy started…'
	$(WEB_UV) mypy .
.PHONY: lint-web-mypy

lint-web-migrations: ## check no Django migrations are missing
	@echo 'lint:web-migrations started…'
	$(WEB_UV) python manage.py makemigrations --check
.PHONY: lint-web-migrations

lint-ocr: ## lint ocr python sources
lint-ocr: \
  lint-ocr-ruff \
  lint-ocr-mypy
.PHONY: lint-ocr

lint-ingestion: ## lint ingestion python sources
lint-ingestion: \
  lint-ingestion-ruff \
  lint-ingestion-mypy \
  lint-ingestion-migrations
.PHONY: lint-ingestion

lint-ocr-fix: ## lint and fix ocr python sources
lint-ocr-fix: \
  lint-ocr-ruff-fix \
  lint-ocr-mypy
.PHONY: lint-ocr-fix

lint-ocr-ruff: ## lint ocr python sources with ruff (check only, like CI)
	@echo 'lint:ocr-ruff started…'
	$(OCR_UV) ruff check .
	$(OCR_UV) ruff format --check .
.PHONY: lint-ocr-ruff

lint-ocr-ruff-fix: ## lint and fix ocr python sources with ruff
	@echo 'lint:ocr-ruff-fix started…'
	$(OCR_UV) ruff check --fix .
	$(OCR_UV) ruff format .
.PHONY: lint-ocr-ruff-fix

lint-ocr-mypy: ## lint ocr python sources with mypy
	@echo 'lint:ocr-mypy started…'
	$(OCR_UV) mypy .
.PHONY: lint-ocr-mypy

lint-ingestion-fix: ## lint and fix ingestion python sources
lint-ingestion-fix: \
  lint-ingestion-ruff-fix \
  lint-ingestion-mypy
.PHONY: lint-ingestion-fix

lint-ingestion-ruff: ## lint ingestion python sources with ruff (check only, like CI)
	@echo 'lint:ingestion-ruff started…'
	$(INGESTION_UV) ruff check .
	$(INGESTION_UV) ruff format --check .
.PHONY: lint-ingestion-ruff

lint-ingestion-ruff-fix: ## lint and fix ingestion python sources with ruff
	@echo 'lint:ingestion-ruff-fix started…'
	$(INGESTION_UV) ruff check --fix .
	$(INGESTION_UV) ruff format .
.PHONY: lint-ingestion-ruff-fix

lint-ingestion-mypy: ## lint ingestion python sources with mypy
	@echo 'lint:ingestion-mypy started…'
	$(INGESTION_UV) mypy .
.PHONY: lint-ingestion-mypy

lint-ingestion-migrations: ## check no ingestion migrations are missing
	@echo 'lint:ingestion-migrations started…'
	$(INGESTION_UV) uv run alembic upgrade head
	$(INGESTION_UV) uv run alembic check
.PHONY: lint-ingestion-migrations

lint-schema: ## generate and check API schema is up to date
	@echo 'lint:schema started…'
	$(WEB_UV) python manage.py spectacular --file presentation/static/api/schema.yaml --validate --fail-on-warn
	git diff --exit-code src/web/presentation/static/api/schema.yaml
.PHONY: lint-schema

lint-internal-schema:
	@echo 'lint:internal schema started…'
	$(WEB_INTERNAL_API_UV) python manage.py spectacular --file presentation/static/api/internal-schema.yaml --validate --fail-on-warn
	git diff --exit-code src/web/presentation/static/api/internal-schema.yaml
.PHONY: lint-internal-schema

lint-frontend-types: ## check frontend TypeScript types are in sync with OpenAPI schema
	@echo 'lint:frontend-types started…'
	$(WEB_PNPM) --filter $(FRONTEND_FILTER) generate-types
	git diff --exit-code src/web/presentation/frontend/src/types/api.d.ts
.PHONY: lint-frontend-types

## TEST
test: ## test all services
test: \
  test-ddd \
  test-referentiel \
  test-web \
  test-ocr \
  test-ingestion
.PHONY: test

test-ddd: ## test ddd package
	@echo 'test:ddd started…'
	$(DDD_UV) uv run pytest --no-cov $(ARGS)
.PHONY: test-ddd

test-referentiel: ## test referentiel package
	@echo 'test:referentiel started…'
	$(REFERENTIEL_UV) uv run pytest --no-cov $(ARGS)
.PHONY: test-referentiel

test-web: ## test web python sources
	@echo 'test:web started…'
	$(WEB_UV) pytest --numprocesses=logical --create-db -m "not accessibility and not e2e" --no-cov --exitfirst $(ARGS)
	$(WEB_UV) pytest --numprocesses=logical -m "e2e" --no-cov --exitfirst $(ARGS)
.PHONY: test-web

test-ocr: ## test ocr python sources
	@echo 'test:ocr started…'
	$(OCR_UV) pytest --no-cov $(ARGS)
.PHONY: test-ocr

test-ingestion: ## test ingestion python sources
test-ingestion: \
  create-ingestion-db \
  create-ingestion-test-db
	@echo 'test:ingestion started…'
	$(INGESTION_UV) env DATABASE=$${TEST_DATABASE_URL:-psql://ingestion:pass@localhost:5432/ingestion_test} pytest $(ARGS)
.PHONY: test-ingestion

test-a11y: ## run a11y tests with Playwright and axe-playwright-python
	@echo 'test:a11y started…'
	$(WEB_UV) pytest -m "accessibility" --create-db --no-cov $(ARGS)
.PHONY: test-a11y

test-e2e: ## run e2e tests with Playwright (live_server + browser)
	@echo 'test:e2e started…'
	$(WEB_UV) pytest -m "e2e" --create-db --no-cov $(ARGS)
.PHONY: test-e2e

test-cov-web: ## run web tests with detailed HTML coverage report
	@echo 'test:cov-web started…'
	@echo 'Generating detailed HTML coverage report for web…'
	@if [ ! -f "src/web/tests/cov_html/index.html" ]; then \
		echo '⚠️  Coverage report not found. Creating directory structure...'; \
		mkdir -p src/web/tests/cov_html; \
	fi
	# Run tests in two phases like test-web to avoid event loop conflicts
	$(WEB_UV) pytest --cov=application --cov=domain --cov=infrastructure --cov=presentation --numprocesses=logical --create-db -m "not accessibility and not e2e" --cov-append --exitfirst $(ARGS)
	$(WEB_UV) pytest --cov=application --cov=domain --cov=infrastructure --cov=presentation --numprocesses=logical -m "e2e" --cov-append --cov-report=html:tests/cov_html --cov-report=term-missing --exitfirst $(ARGS)
	@echo '✅ Coverage report generated in src/web/tests/cov_html/'
	@open src/web/tests/cov_html/index.html
.PHONY: test-cov-web

test-cov-ocr: ## run ocr tests with detailed HTML coverage report
	@echo 'test:cov-ocr started…'
	@echo 'Generating detailed HTML coverage report for ocr…'
	@if [ ! -f "src/ocr/tests/cov_html/index.html" ]; then \
		echo '⚠️  Coverage report not found. Creating directory structure...'; \
		mkdir -p src/ocr/tests/cov_html; \
	fi
	$(OCR_UV) pytest --cov=. --cov-report=html:tests/cov_html --cov-report=term-missing $(ARGS)
	@echo '✅ Coverage report generated in src/ocr/tests/cov_html/'
	@open src/ocr/tests/cov_html/index.html
.PHONY: test-cov-ocr

test-cov-ingestion: ## run ingestion tests with detailed HTML coverage report
	@echo 'test:cov-ingestion started…'
	@echo 'Generating detailed HTML coverage report for ingestion…'
	@if [ ! -f "src/ingestion/tests/cov_html/index.html" ]; then \
		echo '⚠️  Coverage report not found. Creating directory structure...'; \
		mkdir -p src/ingestion/tests/cov_html; \
	fi
	$(INGESTION_UV) pytest --cov=. --cov-report=html:tests/cov_html --cov-report=term-missing $(ARGS)
	@echo '✅ Coverage report generated in src/ingestion/tests/cov_html/'
	@open src/ingestion/tests/cov_html/index.html
.PHONY: test-cov-ingestion

test-cov: ## run tests with detailed HTML coverage report for all services
test-cov: \
  test-cov-web \
  test-cov-ocr \
  test-cov-ingestion
.PHONY: test-cov

## MANAGE docker services
status: ## an alias for "docker compose ps"
	@$(COMPOSE) ps
.PHONY: status

down: ## stop and remove containers but keep volumes (data persists)
	@$(COMPOSE) down
.PHONY: down

down-all: ## stop and remove containers AND volumes (⚠️ data loss!)
	@$(COMPOSE) down -v
.PHONY: down-all

volumes: ## show docker volumes info
	@echo "=== DOCKER VOLUMES ==="
	@docker volume ls | grep csplab || echo "No csplab volumes found"
	@echo ""
	@echo "=== POSTGRES DATA SIZE ==="
	@docker volume inspect csplab_postgres_data --format '{{.Mountpoint}}' 2>/dev/null | xargs -I {} du -sh {} 2>/dev/null || echo "Volume not found or not accessible"
.PHONY: volumes

stop: ## stop all servers
	@$(COMPOSE) stop
.PHONY: stop

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
