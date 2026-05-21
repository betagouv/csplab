# Frontend Vue.js (ATS)

## Architecture

Le frontend est une SPA Vue.js encapsulée dans un template Django (architecture **AppShell**). Le code Vue est découplé de la logique métier Django.

```
src/web/presentation/
├── ats/                          # Bounded context Django
│   ├── views.py                  # Vue base() servant l'AppShell
│   ├── urls.py                   # Routes /ats/*
│   └── templatetags/vite_tags.py # Tags Django pour assets Vite
│
├── frontend/                     # Code source Vue/Vite
│   ├── src/
│   │   ├── app/                  # Point d'entrée (main.ts, App.vue)
│   │   ├── features/             # Modules métier (ats/, ...)
│   │   ├── components/           # Composants UI réutilisables
│   │   ├── composables/          # Hooks Vue
│   │   ├── types/                # Types TypeScript
│   │   └── utils/                # Helpers
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── templates/ats/base.html       # Template Django AppShell
└── static/frontend/              # Build output (gitignored)
```

## Développement local

### Prérequis

- Node.js 22.x
- pnpm (`brew install pnpm` ou `npm install -g pnpm`)

### Installation

```bash
make frontend-install
```

### Lancer le dev server

Deux terminaux nécessaires :

```bash
# Terminal 1 : Django
make run-web

# Terminal 2 : Vite (HMR)
make frontend-dev
```

Accéder à http://localhost:8000/ats/

### Hot Module Replacement (HMR)

En mode dev, le template Django charge les assets depuis le serveur Vite (`localhost:5173`). Les modifications dans `src/` sont reflétées instantanément sans refresh.

## Build production

```bash
make frontend-build
```

Génère les assets dans `presentation/static/frontend/` avec cache-busting (hash dans les noms de fichiers).

## Lint & TypeScript

```bash
make frontend-lint      # Vérifier
make frontend-lint-fix  # Corriger automatiquement
```

Le build inclut une vérification TypeScript (`vue-tsc --noEmit`).

## Déploiement (Scalingo)

Le déploiement utilise le **multi-buildpack** :

1. **Node.js buildpack** : détecte `pnpm-lock.yaml`, exécute `pnpm install` + `pnpm run build`
2. **Python buildpack** : installe Django, lance gunicorn

Fichiers de config :
- `src/web/.buildpacks` : liste des buildpacks
- `src/web/package.json` : script `build` pour Scalingo
- `src/web/pnpm-workspace.yaml` : config workspaces

Le build frontend s'exécute avant `collectstatic`, les assets sont donc inclus dans les fichiers statiques Django.

## pnpm Workspaces

Le projet utilise pnpm workspaces pour gérer les dépendances :

```
src/web/
├── package.json          # Workspace root (config Scalingo)
├── pnpm-workspace.yaml   # Config workspaces
├── pnpm-lock.yaml        # Lockfile unique
└── presentation/frontend/
    └── package.json      # Workspace (deps Vue/Vite)
```

Toutes les commandes pnpm s'exécutent depuis `src/web/` avec `--filter csplab-frontend`.

**Sécurité :** pnpm bloque les scripts postinstall par défaut. Pour approuver un build (ex: esbuild) : `pnpm approve-builds <package>`.

## Template Django et Vite

Le template `ats/base.html` utilise des tags Django personnalisés pour charger les assets Vite :

```html
{% load vite_tags %}

{% if debug %}
  <!-- Dev : charge depuis Vite HMR -->
  <script type="module" src="http://localhost:5173/src/app/main.ts"></script>
{% else %}
  <!-- Prod : charge depuis static avec hash -->
  {% vite_css 'src/app/main.ts' %}
  <script type="module" src="{% vite_asset 'src/app/main.ts' %}"></script>
{% endif %}
```

Les tags `{% vite_asset %}` et `{% vite_css %}` lisent le `manifest.json` généré par Vite pour résoudre les noms de fichiers avec hash.

## CSP (Content Security Policy)

En mode dev, la CSP autorise `localhost:5173` pour le HMR. Configuration dans `config/settings/dev.py`.

## Structure des features

Chaque feature métier est un module dans `src/features/` :

```
src/features/
└── ats/
    ├── HomeView.vue
    ├── components/       # Composants spécifiques ATS
    └── composables/      # Hooks spécifiques ATS
```

Les composants partagés vont dans `src/components/`.
