# Frontend Vue.js (ATS)

## Architecture

The frontend is a Vue.js SPA embedded in a Django template (**AppShell** architecture). Vue code is decoupled from Django business logic.

```
src/web/
├── frontend/                         # Vue/Vite source code
│   ├── src/
│   │   ├── app/                      # Bootstrap & app config (main.ts, App.vue, navigation.ts)
│   │   ├── router/                   # App-level routes + feature routes aggregation
│   │   ├── views/                    # App-level pages without business logic (Home, Parametres, ...)
│   │   ├── features/                 # Business modules (recrutements, etapes-recrutement, ...)
│   │   ├── components/               # Design system (base/, layout/)
│   │   ├── composables/              # Technical hooks (async/, ui/, dnd/)
│   │   ├── stores/                   # Global Pinia stores
│   │   ├── api/                      # HTTP client + cross-cutting API modules
│   │   ├── types/                    # Global TypeScript types
│   │   ├── utils/                    # Pure helpers
│   │   ├── constants/                # Global constants
│   │   └── styles/                   # Global CSS
│   ├── .storybook/
│   └── tsconfig.json
│
├── presentation/
│   ├── ats/                          # Django bounded context
│   │   ├── views.py                  # base() view serving the AppShell
│   │   ├── urls.py                   # Routes /ats/*
│   │   └── templatetags/vite_tags.py # Django tags for Vite assets
│   ├── templates/ats/base.html       # Django AppShell template
│   └── static/frontend/              # Build output (gitignored)
│
├── package.json                      # csplab-web: SPA + candidate assets
├── vite.config.ts                    # root: 'frontend'
└── eslint.config.mjs
```

## Local Development

### Prerequisites

- [mise](https://mise.jdx.dev/getting-started.html) — provisions node and pnpm
  at the pinned versions, nothing to install manually

### Installation

```bash
mise run install
```

### Run the dev server

Two terminals required:

```bash
# Terminal 1: Django
mise run web:dev

# Terminal 2: Vite (HMR)
mise run front:dev
```

Open http://localhost:8000/ats/

### Hot Module Replacement (HMR)

In dev mode, the Django template loads assets from the Vite server. Changes in `src/` are reflected instantly without a full page refresh.

### Changing the dev server origin

The Vite dev origin is a single environment variable, `WEB_VITE_DEV_ORIGIN`
(default `http://localhost:5173`), read by both Vite (port, HMR) and Django
(template, CSP). Set it in `env.d/web` to use another port:

```
WEB_VITE_DEV_ORIGIN=http://localhost:5200
```

An `https://` origin switches Vite to reverse-proxy mode (HMR over `wss`), for
setups that serve the dev server behind a named host. The origin's host and
port then drive the HMR client; Django's CSP follows the same variable.

## Production Build

```bash
mise run front:build
```

Outputs assets to `presentation/static/frontend/` with cache-busting (hashed filenames).

## Lint & TypeScript

```bash
mise run front:lint       # Check
mise run front:lint:fix   # Auto-fix
```

The build includes a TypeScript check (`vue-tsc --noEmit`).

## Deployment (Scalingo)

Deployment uses the **multi-buildpack** setup:

1. **Node.js buildpack**: detects `pnpm-lock.yaml`, runs `pnpm install` + `pnpm run build`
2. **Python buildpack**: installs Django, runs gunicorn

Config files:
- `src/web/.buildpacks`: buildpack list
- `src/web/package.json`: dependencies and scripts of the SPA and of the candidate assets, `build` script for Scalingo
- `src/web/pnpm-workspace.yaml`: pnpm settings (approved build scripts)

The frontend build runs before `collectstatic`, so assets are included in Django static files.

## JavaScript package

`src/web` is a single pnpm package, `csplab-web`, shared by the SPA (`frontend/`) and the candidate assets (`presentation/`): one `node_modules`, one lockfile, one ESLint config. Vite runs with `root: 'frontend'`, so pnpm commands run from `src/web/` and the frontend tasks of `frontend/mise.toml` run from there too.

**Security:** pnpm blocks postinstall scripts by default. To approve a build (e.g. esbuild): `pnpm approve-builds <package>`.

## Django Template and Vite

The `ats/base.html` template uses custom Django tags to load Vite assets:

```html
{% load vite_tags %}

{% if debug %}
  <!-- Dev: load from the Vite dev server (WEB_VITE_DEV_ORIGIN) -->
  <script type="module" src="{% vite_dev_asset 'src/app/main.ts' %}"></script>
{% else %}
  <!-- Prod: load from static with hash -->
  {% vite_css 'src/app/main.ts' %}
  <script type="module" src="{% vite_asset 'src/app/main.ts' %}"></script>
{% endif %}
```

The `{% vite_asset %}` and `{% vite_css %}` tags read Vite's `manifest.json` to resolve hashed filenames.

## CSP (Content Security Policy)

In dev mode, CSP allows the Vite dev origin (`WEB_VITE_DEV_ORIGIN`, including its `ws`/`wss` variant for HMR). Derived in `config/settings/dev.py`.

## Feature Structure

The project **is** the ATS: there is no top-level `ats/` feature. Each business domain is a self-contained module under `src/features/`:

```
src/features/
└── recrutements/
    ├── views/           # Route-level pages (*View.vue)
    ├── components/       # Feature-specific components
    ├── composables/      # Feature-specific hooks
    ├── stores/           # Feature Pinia stores (if needed)
    ├── routes.ts         # Feature routes (aggregated by src/router/)
    ├── api.ts            # Feature API calls
    └── types.ts          # Feature types
```

- A feature owns its routes (`routes.ts`), aggregated in `src/router/index.ts`.
- Cross-feature business code is **not** dumped in a `shared/` folder: it either becomes its own feature or is imported from the owning feature.
- The design system lives in `src/components/` (`base/` for `Csp*` primitives, `layout/` for app chrome).
- Only business-agnostic, reusable code belongs in root folders (`components/`, `composables/`, `utils/`…).

For coding conventions and the full structure, see [frontend_conventions.md](./frontend_conventions.md).
