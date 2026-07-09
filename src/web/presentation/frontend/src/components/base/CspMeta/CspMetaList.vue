<script setup lang="ts">
import type { CspMetaItem } from './types'
import { computed } from 'vue'
import CspMeta from '@/components/base/CspMeta/CspMeta.vue'

const props = withDefaults(defineProps<{
  items: CspMetaItem[]
  size?: 'sm' | 'md' | 'lg'
  layout?: 'inline' | 'stacked'
}>(), {
  layout: 'inline',
  size: 'md',
})

const classes = computed(() => [
  'csp-meta-list',
  `csp-meta-list--${props.layout}`,
  `csp-meta-list--${props.size}`,
])
</script>

<template>
  <ul
    v-if="items.length"
    :class="classes"
  >
    <li
      v-for="(item, index) in items"
      :key="`${item.label}-${index}`"
      class="csp-meta-list__item"
    >
      <CspMeta
        v-bind="item"
        :size="size"
      />
    </li>
  </ul>
</template>

<style scoped lang="scss">
.csp-meta-list {
  display: flex;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--text-mention-grey);

  --csp-meta-list-font-size: 0.875rem;
  --csp-meta-list-inline-gap-x: 1rem;
  --csp-meta-list-inline-gap-y: 0.75rem;
  --csp-meta-list-stacked-gap: 0.5rem;
  --csp-meta-list-item-gap: 0.375rem;

  font-size: var(--csp-meta-list-font-size);
}

.csp-meta-list--sm {
  --csp-meta-list-font-size: 0.75rem;
  --csp-meta-list-inline-gap-x: 1rem;
  --csp-meta-list-inline-gap-y: 0.5rem;
  --csp-meta-list-stacked-gap: 0.375rem;
  --csp-meta-list-item-gap: 0.25rem;
}

.csp-meta-list--md {
  --csp-meta-list-font-size: 0.875rem;
  --csp-meta-list-inline-gap-x: 1.5rem;
  --csp-meta-list-inline-gap-y: 0.75rem;
  --csp-meta-list-stacked-gap: 0.5rem;
  --csp-meta-list-item-gap: 0.375rem;
}

.csp-meta-list--lg {
  --csp-meta-list-font-size: 1rem;
  --csp-meta-list-inline-gap-x: 1.75rem;
  --csp-meta-list-inline-gap-y: 0.875rem;
  --csp-meta-list-stacked-gap: 0.625rem;
  --csp-meta-list-item-gap: 0.5rem;
}

.csp-meta-list--inline {
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-meta-list-inline-gap-y) var(--csp-meta-list-inline-gap-x);
}

.csp-meta-list--stacked {
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-meta-list-stacked-gap);
}

.csp-meta-list__item {
  min-width: 0;
}
</style>
