# Frontend Conventions

Vue.js guidelines. For technical setup, see [frontend_vue.md](./frontend_vue.md).

## Project Structure

The project **is** the ATS, so there is no top-level `ats/` feature. Business code is split into features; reusable business-agnostic code lives in root folders.

```
src/
├── app/                    # Bootstrap & app config (main.ts, App.vue, navigation.ts, icons)
├── router/                 # Route tree (routes.ts), shared route names (names.ts), shared breadcrumb items (breadcrumb.ts)
├── views/                  # App-level pages WITHOUT business logic (Home, NotFound)
│
├── features/               # Business modules (self-contained) — business views & components ONLY
│   ├── recrutements/
│   │   ├── views/          # Route-level pages (*View.vue)
│   │   ├── components/     # Feature-specific components
│   │   ├── composables/    # Feature-specific hooks
│   │   ├── stores/         # Feature Pinia stores (if needed)
│   │   ├── utils/          # Feature-specific helpers
│   │   ├── api.ts          # Feature API calls
│   │   └── types.ts        # Feature types
│   └── etapes-recrutement/
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
├── api/                    # HTTP client, query keys, path parameters
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

Business code lives in its feature. Root folders hold only reusable, business-agnostic code, except the query keys and path parameters of `api/`. App config (navigation) lives in `app/`. The concrete app shell lives in `components/layout/` alongside the layout blocks it composes.

### What is (and isn't) a feature

A feature is a **business domain** (`recrutements`, `etapes-recrutement`, `candidatures`). It contains only business views and business components (with their composables, api, types, stores). A feature provides views and components; `router/routes.ts` mounts them.

The following are **not** features:

| Not a feature            | Where it goes                          |
| ------------------------ | -------------------------------------- |
| A page with no business logic (Home, 404) | `views/`                  |
| The concrete app shell (sidebar + nav + user)         | `components/layout/AppShell.vue` |
| App navigation config                     | `app/navigation.ts`       |
| Generic UI / layout building blocks       | `components/`             |
| Technical, business-agnostic logic        | `composables/`, `utils/` |

- **There is no `features/shared/`.** Cross-feature business code either becomes its own feature, or is promoted to a root folder if it is business-agnostic.
- When two features need the same *business* type or component, the owning feature exposes it and the other imports it (e.g. `candidatures` imports `EtapeRecrutement` from `etapes-recrutement`).
- `FEATURE_DEPENDENCIES` in `src/web/eslint.config.mjs` declares the features each feature imports, and `no-restricted-imports` enforces it outside tests. A feature missing from it imports no other feature, and the configuration throws when the graph has a cycle. Root folders import no feature; `app/` and `router/` may import any feature. An import from another feature uses the `@/features/` alias.

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

- `router/routes.ts` holds the whole route tree. Nesting follows the URL: a parent without component groups its children under a path prefix.
- Route names live in `router/names.ts`. Views, components and the navigation import names from there.
- A set of routes mounted under several parents is built by a function called once per parent, like the candidature panel under the kanban and the list.
- When the tabs of a page are different route components, they are child routes: the page renders `<router-view />` in the `tab` slot of `CspPageContainer`, a single panel shared by all tabs that stays mounted from one tab to the next, and the route tree mounts the tab's component: a view, or a component from the `components/` folder of the tab's feature, which can differ from the page's feature. A tab whose state must survive a visit to another tab is named in the `include` of a `KeepAlive` keyed by the page's entity (`RecrutementView`).
- A view receives its route params as props: `props: true` when the location carries the params the view declares and no others, or a function that picks the declared params when the location carries others, such as the params of child routes. A props function can also build the props of a tab component; each built prop value uses `satisfies` with its prop type so that vue-tsc checks it.
- A route-level view sets the document title with `useDocumentTitle`, from the most specific part to the most general (`Notes - Alice Dupont`). It calls `useHead` from [`@unhead/vue`](https://unhead.unjs.io/docs/vue/head/api/composables/use-head); `App.vue` adds the site name through `titleTemplate`.

```ts
// router/routes.ts
{
  path: `:recrutementUuid${UUID}`,
  children: [
    {
      path: '',
      component: RecrutementView,
      props: paramsAsProps('organismeUuid', 'recrutementUuid'),
      children: [
        { path: 'activites', name: RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES['activites-et-taches'], component: ActivitesTachesView },
        { path: 'equipe', name: RECRUTEMENT_DETAIL_TAB_ROUTE_NAMES.equipe, component: EquipeRecrutementSection, props: true },
      ],
    },
  ],
}
```

## Components

### SFC Structure

```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed } from 'vue';
import type { Candidat } from './types';

// 2. Props & Emits
const props = defineProps<{
  candidat: Candidat;
  editable?: boolean;
}>();

const emit = defineEmits<{
  save: [candidat: Candidat];
  cancel: [];
}>();

// 3. State & computed
const isLoading = ref(false);
const fullName = computed(() => `${props.candidat.firstName} ${props.candidat.lastName}`);

// 4. Functions
function handleSave() {
  emit('save', props.candidat);
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
| Page/View            | `*View.vue`      | `CandidatListView.vue`            |
| UI ingredient        | `Csp` prefix     | `CspButton.vue`, `CspCandidatCard.vue` |

The `Csp` prefix is reserved for UI "ingredients" and design system components. This includes both generic components (base UI) and business-specific UI components (e.g., a card, a specialized input). It does NOT apply to full pages/views or technical utility components (like error boundaries).

### Props & Emits

- Always type with `defineProps<T>()` and `defineEmits<T>()`
- Optional props with `?` and default value if needed
- Emits: name the action, not the DOM event (`save` not `click`)

### Forms in a drawer or popover

- Put the form in its own component, placed in the slot of `CspDrawer` or `CspPopover`. The slot content is unmounted on close, so the form starts from its props at each opening.
- The parent resets the state it owns, such as a search status or a server error, in the function that opens or closes the drawer.
- Derive errors with `computed`. The parent passes a server rejection to the form as a prop (`emailError`, `rejectedSiret`).
- A test reopens the drawer and checks that the form is empty.

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
// features/candidatures/composables/useCandidat.ts
import { ref, computed } from 'vue';
import type { Candidat } from '../types';

export function useCandidat(id: string) {
  const candidat = ref<Candidat | null>(null);
  const isLoading = ref(false);
  const error = ref<Error | null>(null);

  async function fetch() {
    isLoading.value = true;
    // ...
  }

  return {
    candidat,
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
// features/candidatures/stores/candidats.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCandidatsStore = defineStore('candidats', () => {
  const items = ref<Candidat[]>([]);
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
- Query keys → `api/queryKeys.ts`, one tree that follows the API paths, split into `organismeKeys`, `recrutementKeys` and `candidatureKeys`: `recrutementKeys.kanban(params)` is `['organismes', organismeUuid, 'recrutements', recrutementUuid, 'kanban']`. At each level, `root(params)` is the prefix of the subtree and `detail(params)` the key of the detail query, so invalidating `recrutementKeys.root(params)` invalidates every query of that recrutement ([Pinia Colada](https://pinia-colada.esm.dev/guide/query-keys.html)). The queries of a feature (`features/<feature>/queries.ts`) and its invalidations take their keys from these objects.
- Path parameters → `api/params.ts`. Keys, queries and the API functions they call take the params object as is.
- Feature-specific calls → `features/<feature>/api.ts`

### Convention

```ts
// features/candidatures/api.ts
import { api } from '@/api/client';
import type { Candidat } from './types';

export async function getCandidats(): Promise<Candidat[]> {
  const { data } = await api.GET('/candidats');
  return data!;
}

export async function getCandidat(uuid: string): Promise<Candidat> {
  const { data } = await api.GET('/candidats/{uuid}', {
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
// features/candidatures/types.ts
export interface Candidat {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
}

export interface CreateCandidatDto {
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
.candidat-card {
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
.candidat-card {
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
.candidat-card {
}
.candidat-card__header {
}
.candidat-card__title {
}
.candidat-card__icon {
}
```

## Naming (What ESLint Doesn't Cover)

We write identifiers in English, except the terms that the [domain glossary](domain_glossary.md) keeps in French ([ADR-011](ADR/ADR-011-identifier-language.md)).

| Element        | Convention          | Example                     |
| -------------- | ------------------- | --------------------------- |
| Vue files      | PascalCase          | `CandidatCard.vue`          |
| TS files       | camelCase           | `useCandidat.ts`, `api.ts`  |
| Route names    | kebab-case          | `candidat-detail`           |
| Emitted events | camelCase verb      | `save`, `updateStatus`      |
| Boolean props  | `is/has/can` prefix | `isEditable`, `hasError`    |
