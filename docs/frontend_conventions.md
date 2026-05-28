# Frontend Conventions

Vue.js guidelines. For technical setup, see [frontend_vue.md](./frontend_vue.md).

## Feature Structure

```
src/
├── app/                    # Bootstrap (main.ts, App.vue, router)
├── features/               # Business modules
│   └── candidates/
│       ├── CandidateList.vue
│       ├── CandidateDetail.vue
│       ├── components/     # Feature-specific components
│       ├── composables/    # Feature-specific hooks
│       ├── types.ts        # Feature types
│       └── api.ts          # Feature API calls
├── components/             # Shared UI components
├── composables/            # Shared hooks
├── types/                  # Global types
└── utils/                  # Pure helpers
```

**Rule**: all business code lives in its feature. Root folders (`components/`, `composables/`) are for truly reusable code only.

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
| Feature component    | `PascalCase.vue` | `CandidateCard.vue`               |
| Generic UI component | `Base` prefix    | `BaseButton.vue`, `BaseModal.vue` |

### Props & Emits

- Always type with `defineProps<T>()` and `defineEmits<T>()`
- Optional props with `?` and default value if needed
- Emits: name the action, not the DOM event (`save` not `click`)

## Composables

A composable encapsulates reusable logic with reactive state.

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

## API Calls

### Where to Place Code

- Feature-specific calls → `features/xxx/api.ts`
- Shared HTTP client → `utils/http.ts`

### Convention

```ts
// features/candidates/api.ts
import { http } from '@/utils/http';
import type { Candidate } from './types';

export const candidatesApi = {
  getAll: () => http.get<Candidate[]>('/api/candidates/'),
  getById: (id: string) => http.get<Candidate>(`/api/candidates/${id}/`),
  create: (data: CreateCandidateDto) => http.post<Candidate>('/api/candidates/', data),
};
```

- Group by entity in an object
- Type the returns
- Relative URLs (Vite proxy handles dev)

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
