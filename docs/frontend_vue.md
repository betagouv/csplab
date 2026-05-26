# Frontend Vue.js (ATS)

## Architecture

The frontend is a Vue.js SPA embedded in a Django template (**AppShell** architecture). Vue code is decoupled from Django business logic.

```
src/web/presentation/
├── ats/                          # Django bounded context
│   ├── views.py                  # base() view serving the AppShell
│   ├── urls.py                   # Routes /ats/*
│   └── templatetags/vite_tags.py # Django tags for Vite assets
│
├── frontend/                     # Vue/Vite source code
│   ├── src/
│   │   ├── app/                  # Entry point (main.ts, App.vue)
│   │   ├── features/             # Business modules (ats/, ...)
│   │   ├── components/           # Reusable UI components
│   │   ├── composables/          # Vue hooks
│   │   ├── types/                # TypeScript types
│   │   └── utils/                # Helpers
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── templates/ats/base.html       # Django AppShell template
└── static/frontend/              # Build output (gitignored)
```

## Local Development

### Prerequisites

- Node.js 22.x
- pnpm (`brew install pnpm` or `npm install -g pnpm`)

### Installation

```bash
make frontend-install
```

### Run the dev server

Two terminals required:

```bash
# Terminal 1: Django
make run-web

# Terminal 2: Vite (HMR)
make frontend-dev
```

Open http://localhost:8000/ats/

### Hot Module Replacement (HMR)

In dev mode, the Django template loads assets from the Vite server (`localhost:5173`). Changes in `src/` are reflected instantly without a full page refresh.

## Production Build

```bash
make frontend-build
```

Outputs assets to `presentation/static/frontend/` with cache-busting (hashed filenames).

## Lint & TypeScript

```bash
make frontend-lint      # Check
make frontend-lint-fix  # Auto-fix
```

The build includes a TypeScript check (`vue-tsc --noEmit`).

## Deployment (Scalingo)

Deployment uses the **multi-buildpack** setup:

1. **Node.js buildpack**: detects `pnpm-lock.yaml`, runs `pnpm install` + `pnpm run build`
2. **Python buildpack**: installs Django, runs gunicorn

Config files:
- `src/web/.buildpacks`: buildpack list
- `src/web/package.json`: `build` script for Scalingo
- `src/web/pnpm-workspace.yaml`: workspace config

The frontend build runs before `collectstatic`, so assets are included in Django static files.

## pnpm Workspaces

The project uses pnpm workspaces for dependencies:

```
src/web/
├── package.json          # Workspace root (Scalingo config)
├── pnpm-workspace.yaml   # Workspace config
├── pnpm-lock.yaml        # Single lockfile
└── presentation/frontend/
    └── package.json      # Workspace (Vue/Vite deps)
```

All pnpm commands run from `src/web/` with `--filter csplab-frontend`.

**Security:** pnpm blocks postinstall scripts by default. To approve a build (e.g. esbuild): `pnpm approve-builds <package>`.

## Django Template and Vite

The `ats/base.html` template uses custom Django tags to load Vite assets:

```html
{% load vite_tags %}

{% if debug %}
  <!-- Dev: load from Vite HMR -->
  <script type="module" src="http://localhost:5173/src/app/main.ts"></script>
{% else %}
  <!-- Prod: load from static with hash -->
  {% vite_css 'src/app/main.ts' %}
  <script type="module" src="{% vite_asset 'src/app/main.ts' %}"></script>
{% endif %}
```

The `{% vite_asset %}` and `{% vite_css %}` tags read Vite's `manifest.json` to resolve hashed filenames.

## CSP (Content Security Policy)

In dev mode, CSP allows `localhost:5173` for HMR. Configured in `config/settings/dev.py`.

## Feature Structure

Each business feature is a module under `src/features/`:

```
src/features/
└── ats/
    ├── HomeView.vue
    ├── components/       # ATS-specific components
    └── composables/      # ATS-specific hooks
```

Shared components go in `src/components/`.

For coding conventions, see [frontend_conventions.md](./frontend_conventions.md).
