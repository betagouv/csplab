# Frontend Conventions

Vue.js guidelines. For technical setup, see [frontend_vue.md](./frontend_vue.md).

## Project Structure

The project **is** the ATS, so there is no top-level `ats/` feature. Business code is split into features; reusable business-agnostic code lives in root folders.

```
src/
├── app/                    # Bootstrap & app config (main.ts, App.vue, navigation.ts, icons)
├── router/                 # index.ts — app-level routes + aggregates feature routes
├── views/                  # App-level pages WITHOUT business logic (Home, ParametresView, NotFound)
│
├── features/               # Business modules (self-contained) — business views & components ONLY
│   ├── recrutements/
│   │   ├── views/          # Route-level pages (*View.vue)
│   │   ├── components/     # Feature-specific components
│   │   ├── composables/    # Feature-specific hooks
│   │   ├── stores/         # Feature Pinia stores (if needed)
│   │   ├── utils/          # Feature-specific helpers
│   │   ├── routes.ts       # Feature routes (optional — a feature may have none)
│   │   ├── api.ts          # Feature API calls
│   │   └── types.ts        # Feature types
│   └── etapes-recrutement/ # Config feature mounted inside views/ParametresView.vue (no route)
│
├── components/             # Reusable UI components
│   ├── base/               # UI primitives (CspButton, CspInput…)
│   ├── layout/             # Layout blocks + concrete app shell (CspAppShell, CspSidebar, CspPageContainer…)
│   └── ErrorBoundary.vue   # Generic technical components (non-Csp) live at the root
│
├── composables/            # Global TECHNICAL composables
│   ├── async/              # useAsyncState, useDebounce
│   ├── ui/                 # useDisclosure, useSidebar, useToast, useColorMode
│   └── dnd/                # Drag & drop
│
├── stores/                 # Global Pinia stores (session, ui)
├── api/                    # HTTP client
├── utils/                  # Pure helpers
├── types/                  # Global technical types
├── constants/              # Global constants
├── styles/                 # Global CSS (tokens, reset)
└── assets/                 # Static assets (images, fonts)
```

### Where does the code go?

| Code                                | Location                              |
| ----------------------------------- | ------------------------------------- |
| Business route-level page           | `features/<feature>/views/*View.vue`  |
| App-level page (no business logic)  | `views/*View.vue`                     |
| Feature-specific component          | `features/<feature>/components/`       |
| Feature-specific hook               | `features/<feature>/composables/`      |
| Feature API calls                   | `features/<feature>/api.ts`            |
| Feature store                       | `features/<feature>/stores/`           |
| Concrete app shell                  | `components/layout/AppShell.vue`      |
| App config (navigation…)            | `app/` (e.g. `navigation.ts`)         |
| Generic UI ingredient (`Csp*`)      | `components/base/`                     |
| Generic layout block (`Csp*`)       | `components/layout/`                   |
| Generic technical component         | `components/` (e.g. `ErrorBoundary`)  |
| Technical reusable hook             | `composables/<category>/`             |
| Global store                        | `stores/`                             |

**Rule**: business code lives in its feature. Root folders hold only reusable, business-agnostic code. App config (navigation) lives in `app/`. The concrete app shell lives in `components/layout/` alongside the layout blocks it composes.

### What is (and isn't) a feature

A feature is a **business domain** (`recrutements`, `etapes-recrutement`, `candidatures`). It contains only business views and business components (with their composables, api, types, stores). A feature does **not** need to own a route — it may just expose a component mounted by a page (e.g. `etapes-recrutement` lives inside `ParametresView`).

The following are **not** features:

| Not a feature            | Where it goes                          |
| ------------------------ | -------------------------------------- |
| A page with no business logic (Home, 404) | `views/`                  |
| A container page hosting several features (Parametres) | `views/`      |
| The concrete app shell (sidebar + nav + user)         | `components/layout/AppShell.vue` |
| App navigation config                     | `app/navigation.ts`       |
| Generic UI / layout building blocks       | `components/`             |
| Technical, business-agnostic logic        | `composables/`, `utils/` |

- **There is no `features/shared/`.** Cross-feature business code either becomes its own feature, or is promoted to a root folder if it is business-agnostic.
- When two features need the same *business* type, the owning feature exposes it and the other imports it (e.g. `candidatures` imports `EtapeRecrutement` from `etapes-recrutement`). A dependency between features is fine when it mirrors the domain.

### Container pages vs features

A settings/dashboard page is often just a **container**: it arranges tabs/sections, each rendering a feature component. The container page has no business logic → it lives in `views/`. The business logic of each panel lives in its feature.

```
views/ParametresView.vue                      # tabs container (no business logic)
features/etapes-recrutement/
  ├── components/EtapesRecrutementList.vue     # the actual config UI
  ├── composables/useEtapesRecrutement.ts
  ├── constants/etape-recrutement.ts
  ├── api.ts
  └── types.ts
```

### App shell

The shell wraps `<RouterView>` **once** (in `App.vue`), so views never import it themselves:

```vue
<!-- app/App.vue -->
<template>
  <CspToaster>
    <ErrorBoundary>
      <AppShell>
        <RouterView />
      </AppShell>
    </ErrorBoundary>
  </CspToaster>
</template>
```

## Routing

- A feature that owns route-level pages declares them in `features/<feature>/routes.ts`.
- App-level pages (`views/`) declare their routes directly in `router/index.ts`.
- `router/index.ts` aggregates everything. Never hardcode a feature's routes in the router.

```ts
// features/recrutements/routes.ts
import type { RouteRecordRaw } from 'vue-router';

export const recrutementsRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements',
    name: 'mes-recrutements',
    component: () => import('./views/MesRecrutementsView.vue'),
  },
];
```

```ts
// router/index.ts
import type { RouteRecordRaw } from 'vue-router';
import { recrutementsRoutes } from '@/features/recrutements/routes';

const appRoutes: RouteRecordRaw[] = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/parametres', name: 'parametres', component: () => import('@/views/ParametresView.vue') },
];

export const routes = [...appRoutes, ...recrutementsRoutes];
```

## Components

### SFC Structure

```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed } from 'vue';
import type { Candidate } from './types';

// 2. Props & Emits
const props = defineProps<{
  candidate: Candidate;
  editable?: boolean;
}>();

const emit = defineEmits<{
  save: [candidate: Candidate];
  cancel: [];
}>();

// 3. State & computed
const isLoading = ref(false);
const fullName = computed(() => `${props.candidate.firstName} ${props.candidate.lastName}`);

// 4. Functions
function handleSave() {
  emit('save', props.candidate);
}
</script>

<template>
  <!-- Template -->
</template>

<style scoped>
/* Scoped styles */
</style>
```

### Component Naming

| Type                 | Convention       | Example                           |
| -------------------- | ---------------- | --------------------------------- |
| Page/View            | `*View.vue`      | `CandidateListView.vue`           |
| UI ingredient        | `Csp` prefix     | `CspButton.vue`, `CspCandidateCard.vue` |

**Rule**: The `Csp` prefix is reserved for UI "ingredients" and design system components. This includes both generic components (base UI) and business-specific UI components (e.g., a card, a specialized input). It does NOT apply to full pages/views or technical utility components (like error boundaries).

### Props & Emits

- Always type with `defineProps<T>()` and `defineEmits<T>()`
- Optional props with `?` and default value if needed
- Emits: name the action, not the DOM event (`save` not `click`)

## Composables

A composable encapsulates reusable logic with reactive state.

### Where to Place a Composable

| Type                                            | Location                          |
| ----------------------------------------------- | --------------------------------- |
| Business logic of a feature                     | `features/<feature>/composables/` |
| Technical, business-agnostic (reused anywhere)  | `composables/<category>/`         |

Global technical composables are grouped by category to avoid a flat dumping ground:

- `composables/async/` — `useAsyncState`, `useDebounce`
- `composables/ui/` — `useDisclosure`, `useSidebar`, `useToast`, `useColorMode`
- `composables/dnd/` — drag & drop primitives

A composable is "technical" only if it contains **no** business/domain knowledge. As soon as it references a domain concept (recrutement, étape, candidature…), it belongs to a feature.

### When to Create a Composable

| Situation                                  | Solution                     |
| ------------------------------------------ | ---------------------------- |
| Logic reused in 2+ components              | **Composable**               |
| Complex logic in a single component        | **Composable** (for clarity) |
| State shared between non-parent components | **Pinia Store**              |
| Simple data transformation                 | `utils/` function            |

### Convention

```ts
// composables/useCandidate.ts
import { ref, computed } from 'vue';
import type { Candidate } from '@/features/candidates/types';

export function useCandidate(id: string) {
  const candidate = ref<Candidate | null>(null);
  const isLoading = ref(false);
  const error = ref<Error | null>(null);

  async function fetch() {
    isLoading.value = true;
    // ...
  }

  return {
    candidate,
    isLoading,
    error,
    fetch,
  };
}
```

- `use` prefix
- Return an object (no destructuring of the return)
- Expose state + actions

## Stores (Pinia)

### When to Use a Store

| Situation                                 | Solution                           |
| ----------------------------------------- | ---------------------------------- |
| Local component state                     | Local `ref()`                      |
| State shared parent → children            | Props                              |
| State shared between unrelated components | **Store**                          |
| Persistent state (user session)           | **Store**                          |
| API data cache                            | **Store** or composable with cache |

### Convention

```ts
// features/candidates/stores/candidates.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCandidatesStore = defineStore('candidates', () => {
  const items = ref<Candidate[]>([]);
  const isLoading = ref(false);

  const count = computed(() => items.value.length);

  async function fetchAll() {
    // ...
  }

  return { items, isLoading, count, fetchAll };
});
```

- Use **setup stores** (Composition API)
- One store per entity/domain, not per component
- `use*Store` prefix
- **Location**: a store tied to a feature lives in `features/<feature>/stores/`; a cross-cutting store (session, UI, current user) lives in the root `stores/`.

## API Calls

### Where to Place Code

- HTTP client + error handling → `api/client.ts`, `api/errors.ts`
- Cross-cutting API modules (e.g. current user) → `api/`
- Feature-specific calls → `features/<feature>/api.ts`

### Convention

```ts
// features/candidates/api.ts
import { api } from '@/api/client';
import type { Candidate } from './types';

export async function getCandidates(): Promise<Candidate[]> {
  const { data } = await api.GET('/candidates');
  return data!;
}

export async function getCandidate(uuid: string): Promise<Candidate> {
  const { data } = await api.GET('/candidates/{uuid}', {
    params: { path: { uuid } },
  });
  return data!;
}
```

- One exported `async` function per endpoint
- Types come from the generated OpenAPI schema (`@/types/api`)
- The client (`api`) handles CSRF, auth redirect and error mapping

## TypeScript

### Shared Types

```ts
// features/candidates/types.ts
export interface Candidate {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  status: CandidateStatus;
}

export type CandidateStatus = 'new' | 'screening' | 'interview' | 'offer' | 'hired' | 'rejected';

export interface CreateCandidateDto {
  firstName: string;
  lastName: string;
  email: string;
}
```

- `interface` for objects
- `type` for unions/aliases
- `Dto` suffix for API payloads

## CSS

- `<style scoped lang="scss">` by default
- BEM light for elements and modifiers ( `__element`, `--modifier`)
- Use `csp-` prefix for global or shared component classes (e.g., `.csp-btn`, `.csp-input`)
- CSS variables for tokens (colors, spacing)
- No global styles except reset/tokens

### SCSS Nesting

Limit nesting to **2 levels max**. Use `&` for modifiers and pseudo-classes.

```vue
<style scoped lang="scss">
// Good: 2 levels max
.candidate-card {
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);

  .header {
    display: flex;
  }

  &--highlighted {
    border: 2px solid var(--color-primary);
  }

  &:hover {
    background: var(--color-hover);
  }
}
</style>
```

```scss
// Bad: too deep
.candidate-card {
  .header {
    .title {
      .icon {
        // 4 levels
      }
    }
  }
}
```

Use BEM or flat classes instead of deep nesting:

```scss
// Prefer this
.candidate-card {
}
.candidate-card__header {
}
.candidate-card__title {
}
.candidate-card__icon {
}
```

## Naming (What ESLint Doesn't Cover)

| Element        | Convention          | Example                     |
| -------------- | ------------------- | --------------------------- |
| Vue files      | PascalCase          | `CandidateCard.vue`         |
| TS files       | camelCase           | `useCandidate.ts`, `api.ts` |
| Route names    | kebab-case          | `candidate-detail`          |
| Emitted events | camelCase verb      | `save`, `updateStatus`      |
| Boolean props  | `is/has/can` prefix | `isEditable`, `hasError`    |
