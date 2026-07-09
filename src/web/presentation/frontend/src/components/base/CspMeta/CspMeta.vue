<script setup lang="ts">
import type { CspMetaItem } from './types'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<CspMetaItem & {
  size?: 'sm' | 'md' | 'lg'
}>(), {
  icon: undefined,
  size: 'md',
})
</script>

<template>
  <span
    class="csp-meta"
    :class="[
      `csp-meta--${size}`,
    ]"
  >
    <CspIcon
      v-if="icon"
      :name="icon"
      :size="12"
      class="csp-meta__icon"
    />
    <span class="sr-only">{{ srLabel }} :</span>
    <span class="csp-meta__label">{{ label }}</span>
  </span>
</template>

<style scoped lang="scss">
.csp-meta {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-meta-gap);
  min-width: 0;
  color: var(--text-mention-grey);
  font-size: var(--csp-meta-font-size);
  line-height: 1.4;

  --csp-meta-font-size: 0.75rem;
  --csp-meta-gap: 0.25rem;
}

.csp-meta__icon {
  width: 1em;
  height: 1em;
}

.csp-meta--sm {
  --csp-meta-font-size: 0.625rem;
  --csp-meta-gap: 0.125rem;
}

.csp-meta--md {
  --csp-meta-font-size: 0.875rem;
  --csp-meta-gap: 0.25rem;
}

.csp-meta--lg {
  --csp-meta-font-size: 1rem;
  --csp-meta-gap: 0.375rem;
}

.csp-meta__icon {
  flex: none;
}

.csp-meta__label {
  min-width: 0;
}
</style>
