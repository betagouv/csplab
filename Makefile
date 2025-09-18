# -- General
SHELL := /bin/bash

# -- Docker
COMPOSE                    	 = bin/compose
COMPOSE_UP                 	 = $(COMPOSE) up -d --remove-orphans
COMPOSE_RUN                	 = $(COMPOSE) run --rm --no-deps
COMPOSE_RUN_DEV_UV         	 = $(COMPOSE_RUN) dev uv run --project dev

default: help

## -- Files
.pre-commit-cache:
	mkdir .pre-commit-cache

.git/hooks/pre-commit:
	cp bin/git-pre-commit-hook .git/hooks/pre-commit

.git/hooks/commit-msg:
	cp bin/git-commit-msg-hook .git/hooks/commit-msg

### BOOTSTRAP
bootstrap: ## setup development environment (build dev service and install git hooks)
bootstrap: \
	build \
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
	$(COMPOSE) build
.PHONY: build

build-dev: ## build development environment image
	@$(COMPOSE) build dev
.PHONY: build-dev

build-notebook: ## build custom jupyter notebook image
	@$(COMPOSE) build notebook
.PHONY: build-notebook

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

### RUN
run-all: ## run the whole stack
	$(COMPOSE_UP) notebook
.PHONY: run-all

run-notebook: ## run the notebook service
	$(COMPOSE_UP) notebook
.PHONY: run-notebook

## LINT
# -- Global linting
lint: ## lint all sources
lint: \
	lint-notebook
.PHONY: lint

lint-fix: ## lint and fix all sources
lint-fix: \
	lint-notebook-fix
.PHONY: lint-fix

# -- Per-service linting
lint-notebook: ## lint notebook python sources
	@echo 'lint:notebook started…'
	$(COMPOSE_RUN_DEV_UV) ruff check src/notebook/
	$(COMPOSE_RUN_DEV_UV) ruff format --check src/notebook/
.PHONY: lint-notebook

lint-notebook-fix: ## lint and fix notebook python sources
	@echo 'lint:notebook-fix started…'
	$(COMPOSE_RUN_DEV_UV) ruff check --fix src/notebook/
	$(COMPOSE_RUN_DEV_UV) ruff format src/notebook/
.PHONY: lint-notebook-fix

### MANAGE docker services
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
