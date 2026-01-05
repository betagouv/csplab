# -- General
SHELL := /bin/bash

# -- Docker
COMPOSE                 = docker compose
COMPOSE_UP              = $(COMPOSE) up -d --remove-orphans

TYCHO_UV = cd src/tycho && direnv exec .
NOTEBOOK_UV = cd src/notebook && direnv exec .
DEV_UV = cd dev && direnv exec .

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
	@cp src/tycho/.envrc.sample src/tycho/.envrc
	@cp src/notebook/.envrc.sample src/notebook/.envrc
	@cp env.d/tycho-example env.d/tycho
	@cp env.d/notebook-example env.d/notebook
	@cp env.d/postgresql-example env.d/postgresql
	@cd src/tycho && direnv allow
	@cd src/notebook && direnv allow
	@echo "✅ Environment files copied. Please edit env.d/* with your actual values."
.PHONY: setup

bootstrap: ## setup development environment (build dev service and install git hooks)
bootstrap: \
  run-postgres \
  build \
  migrate \
  create-superuser \
  jupytext--to-ipynb
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
  build-dev \
  build-tycho \
  build-notebook
.PHONY: build

build-dev: ## build development environment image
	@$(DEV_UV) uv sync
.PHONY: build-dev

build-notebook: ### setup notebook kernels natively
	@$(NOTEBOOK_UV) uv sync --locked
.PHONY: build-notebook

build-tycho: ## build tycho image
	# not using @ which suppress the command's echoing in terminal
	$(TYCHO_UV) uv sync --group dev
.PHONY: build-tycho

jupytext--to-md: ## convert local ipynb files into md
	cd src/notebook && uv run jupytext --to md *.ipynb && cd ../..
.PHONY: jupytext--to-md

jupytext--to-ipynb: ## convert remote md files into ipynb
	cd src/notebook && uv run jupytext --to ipynb *.md && cd ../..
.PHONY: jupytext--to-ipynb

### LOGS
logs: ## display all services logs (follow mode)
	@$(COMPOSE) logs -f
.PHONY: logs

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
	$(NOTEBOOK_UV) jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
.PHONY: run-notebook

run-es: ## run the elasticsearch service
	$(COMPOSE_UP) elasticsearch
.PHONY: run-es

run-postgres: ## run the DB service
	$(COMPOSE_UP) postgresql
.PHONY: run-postgres

run-tycho: ## run the tycho service
	@bin/manage runserver
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
	$(NOTEBOOK_UV) ruff check . || true
	$(NOTEBOOK_UV) ruff format --check . || true
.PHONY: lint-notebook

lint-notebook-fix: ## lint and fix notebook python sources
	@echo 'lint:notebook-fix started (warnings only)…'
	$(NOTEBOOK_UV) ruff check --fix . || true
	$(NOTEBOOK_UV) ruff format . || true
.PHONY: lint-notebook-fix

lint-tycho: ## lint tycho python sources
lint-tycho: \
  lint-tycho-ruff \
  lint-tycho-mypy
.PHONY: lint-tycho

lint-tycho-fix: ## lint and fix tycho python sources
lint-tycho-fix: \
  lint-tycho-ruff-fix \
  lint-tycho-mypy
.PHONY: lint-tycho-fix

lint-tycho-ruff: ## lint tycho python sources with ruff (check only, like CI)
	@echo 'lint:tycho-ruff started…'
	$(TYCHO_UV) ruff check .
	$(TYCHO_UV) ruff format --check .
.PHONY: lint-tycho-ruff

lint-tycho-ruff-fix: ## lint and fix tycho python sources with ruff
	@echo 'lint:tycho-ruff-fix started…'
	$(TYCHO_UV) ruff check --fix .
	$(TYCHO_UV) ruff format .
.PHONY: lint-tycho-ruff-fix

lint-tycho-mypy: ## lint tycho python sources with mypy
	@echo 'lint:tycho-mypy started…'
	$(TYCHO_UV) mypy .
.PHONY: lint-tycho-mypy

## TEST
test: ## test all services
test: \
  test-tycho
.PHONY: test

test-tycho: ## test tycho python sources
	@echo 'test:tychostarted…'
	$(TYCHO_UV) pytest -s
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
