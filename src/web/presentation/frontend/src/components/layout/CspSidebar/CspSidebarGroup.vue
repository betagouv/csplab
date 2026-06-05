<script setup lang="ts">
import type { ComputedRef } from 'vue'
import { inject } from 'vue'

interface CspSidebarGroupProps {
  label: string
}

defineProps<CspSidebarGroupProps>()

const isExpanded = inject<ComputedRef<boolean>>('sidebar-expanded')
</script>

<template>
  <div
    class="csp-sidebar-group"
    role="group"
    :aria-label="label"
  >
    <span
      v-if="isExpanded"
      class="csp-sidebar-group__label"
    >
      {{ label }}
    </span>
    <div class="csp-sidebar-group__items">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-sidebar-group {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
}

.csp-sidebar-group__label {
  padding: 0 var(--sidebar-inset-x, 0.5rem);
  margin-bottom: 0.125rem;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.csp-sidebar-group__items {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  align-items: stretch;
}
</style>
