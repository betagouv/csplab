<script setup lang="ts">
import type { ComputedRef } from 'vue'
import type { PrimitiveProps } from 'reka-ui'
import { Primitive } from 'reka-ui'
import { inject } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

interface CspSidebarItemProps extends PrimitiveProps {
  icon: string
  label: string
  isActive?: boolean
}

withDefaults(defineProps<CspSidebarItemProps>(), {
  as: 'button',
  isActive: false,
})

const isExpanded = inject<ComputedRef<boolean>>('sidebar-expanded')
</script>

<template>
  <Primitive
    :as="as"
    :as-child="asChild"
    class="csp-sidebar-item"
    :class="{
      'csp-sidebar-item--active': isActive,
      'csp-sidebar-item--expanded': isExpanded,
    }"
    :title="isExpanded ? undefined : label"
    :aria-current="isActive ? 'page' : undefined"
  >
    <CspIcon
      class="csp-sidebar-item__icon"
      :name="icon"
      :size="20"
    />
    <span
      v-if="isExpanded"
      class="csp-sidebar-item__label"
    >
      {{ label }}
    </span>
  </Primitive>
</template>

<style scoped lang="scss">
.csp-sidebar-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: var(--sidebar-item-size, 2.5rem);
  height: var(--sidebar-item-size, 2.5rem);
  padding: 0;
  border: none;
  border-radius: 0.5rem;
  background: transparent;
  color: var(--text-mention-grey);
  text-decoration: none;
  cursor: pointer;
  flex-shrink: 0;

  &--expanded {
    justify-content: flex-start;
    width: 100%;
    height: var(--sidebar-item-size, 2.5rem);
    padding: 0 var(--sidebar-inset-x, 0.5rem);
  }

  &:hover {
    background: var(--background-default-grey-hover);
    color: var(--text-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-sidebar-item__icon {
  flex-shrink: 0;
}

.csp-sidebar-item__label {
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-item--active {
  background: var(--background-action-low-blue-france);
  color: var(--text-action-high-blue-france);

  &:hover {
    background: var(--background-action-low-blue-france-hover);
    color: var(--text-action-high-blue-france);
  }

  .csp-sidebar-item__label {
    font-weight: 600;
  }
}
</style>
