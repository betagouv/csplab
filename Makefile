# -- General
SHELL := /bin/bash

# -- Docker
COMPOSE                 = bin/compose
COMPOSE_UP              = $(COMPOSE) up -d --remove-orphans
COMPOSE_RUN             = $(COMPOSE) run --rm --no-deps
COMPOSE_RUN_DEV_UV      = $(COMPOSE_RUN) dev uv run
COMPOSE_RUN_TYCHO_UV    = $(COMPOSE_RUN) tycho uv run
COMPOSE_RUN_NOTEBOOK_UV = $(COMPOSE_RUN) notebook uv run

default: help

## -- Files
.pre-commit-cache:
	mkdir .pre-commit-cache

.git/hooks/_commons.inc.sh:
	cp bin/_commons.inc.sh .git/hooks/_commons.inc.sh

.git/hooks/pre-commit:
	cp bin/git-pre-commit-hook .git/hooks/pre-commit

.git/hooks/commit-msg:
	cp bin/git-commit-msg-hook .git/hooks/commit-msg

### BOOTSTRAP
setup-env: ## copy example env files to local files
	@cp env.d/tycho-example env.d/tycho
	@cp env.d/notebook-example env.d/notebook
	@cp env.d/postgresql-example env.d/postgresql
	@echo "✅ Environment files copied. Please edit env.d/* with your actual values."
.PHONY: setup-env

bootstrap: ## setup development environment (build dev service and install git hooks)
bootstrap: \
  build \
  migrate \
  create-superuser \
  jupytext--to-ipynb
.PHONY: bootstrap

git-hooks: ## install pre-commit hook
git-hooks: \
  .pre-commit-cache \
  .git/hooks/_commons.inc.sh \
  .git/hooks/pre-commit \
  .git/hooks/commit-msg
.PHONY: git-hooks

### BUILD
build: ## build services image
	$(COMPOSE) build
.PHONY: build

build-dev: ## build development environment image
	@$(COMPOSE) build dev
.PHONY: build-dev

build-notebook: ## build custom jupyter notebook image
	@$(COMPOSE) build notebook
.PHONY: build-notebook

build-tycho: ## build tycho image
	@$(COMPOSE) build tycho
.PHONY: build-tycho

jupytext--to-md: ## convert local ipynb files into md
	bin/jupytext --to md **/*.ipynb
.PHONY: jupytext--to-md

jupytext--to-ipynb: ## convert remote md files into ipynb
	bin/jupytext --to ipynb **/*.md
.PHONY: jupytext--to-ipynb

### LOGS
logs: ## display all services logs (follow mode)
	@$(COMPOSE) logs -f
.PHONY: logs

logs-notebook: ## display notebook logs (follow mode)
	@$(COMPOSE) logs -f notebook
.PHONY: logs-notebook

logs-tycho: ## display tycho logs (follow mode)
	@$(COMPOSE) logs -f tycho
.PHONY: logs-tycho

### Setup
migrate: ## migrate tycho database
	@echo "Migrating tycho database…"
	@bin/manage migrate
.PHONY: migrate

create-superuser: ## create tycho super user
	@echo "Creating tycho super user…"
	@bin/manage createsuperuser --noinput || true
.PHONY: create-superuser

### RUN
run-all: ## run the whole stack
run-all: \
  run-notebook \
  run-es
.PHONY: run-all

run-notebook: ## run the notebook service
	$(COMPOSE_UP) notebook
.PHONY: run-notebook

run-es: ## run the elasticsearch service
	$(COMPOSE_UP) elasticsearch
.PHONY: run-es

run-tycho: ## run the tycho service
	$(COMPOSE_UP) tycho
.PHONY: run-tycho

## LINT
# -- Global linting
lint: ## lint all sources
lint: \
  lint-notebook \
  lint-tycho
.PHONY: lint

lint-fix: ## lint and fix all sources
lint-fix: \
  lint-notebook-fix \
  lint-tycho-fix
.PHONY: lint-fix

# -- Per-service linting
lint-notebook: ## lint notebook python sources
	@echo 'lint:notebook started (warnings only)…'
	$(COMPOSE_RUN_NOTEBOOK_UV) ruff check . || true
	$(COMPOSE_RUN_NOTEBOOK_UV) ruff format --check . || true
.PHONY: lint-notebook

lint-notebook-fix: ## lint and fix notebook python sources
	@echo 'lint:notebook-fix started (warnings only)…'
	$(COMPOSE_RUN_NOTEBOOK_UV) ruff check --fix . || true
	$(COMPOSE_RUN_NOTEBOOK_UV) ruff format . || true
.PHONY: lint-notebook-fix

lint-tycho: ## lint tycho python sources
lint-tycho: \
  lint-tycho-ruff \
  lint-tycho-mypy
.PHONY: lint-tycho

lint-tycho: ## lint and fix tycho python sources
lint-tycho-fix: \
  lint-tycho-ruff-fix \
  lint-tycho-mypy
.PHONY: lint-tycho

lint-tycho-ruff: ## lint tycho python sources with ruff (check only, like CI)
	@echo 'lint:tycho-ruff started…'
	$(COMPOSE_RUN_TYCHO_UV) ruff check .
	$(COMPOSE_RUN_TYCHO_UV) ruff format --check .
.PHONY: lint-tycho-ruff

lint-tycho-ruff-fix: ## lint and fix tycho python sources with ruff
	@echo 'lint:tycho-ruff-fix started…'
	$(COMPOSE_RUN_TYCHO_UV) ruff check --fix .
	$(COMPOSE_RUN_TYCHO_UV) ruff format .
.PHONY: lint-tycho-ruff-fix

lint-tycho-mypy: ## lint tycho python sources with mypy
	@echo 'lint:tycho-mypy started…'
	$(COMPOSE_RUN_TYCHO_UV) mypy .
.PHONY: lint-tycho-mypy

## TEST
test: ## test all services
test: \
  test-tycho
.PHONY: test

test-tycho: ## test tycho python sources
	@echo 'test:tychostarted…'
	$(COMPOSE_RUN_TYCHO_UV) pytest -s
.PHONY: test-tycho

## MANAGE docker services
status: ## an alias for "docker compose ps"
	@$(COMPOSE) ps
.PHONY: status

down: ## stop and remove all containers
	@$(COMPOSE) down
.PHONY: down

stop: ## stop all servers
	@$(COMPOSE) stop
.PHONY: stop

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
