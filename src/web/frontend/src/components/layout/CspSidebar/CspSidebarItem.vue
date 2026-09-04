<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import { Primitive } from 'reka-ui'
import { RouterLink } from 'vue-router'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { useSidebar } from '@/composables/ui/useSidebar'

interface CspSidebarItemProps {
  icon: string
  label: string
  to?: RouteLocationRaw
  isActive?: boolean
}

defineOptions({
  inheritAttrs: false,
})

withDefaults(defineProps<CspSidebarItemProps>(), {
  isActive: false,
})

const { isExpanded, isMobile } = useSidebar()
</script>

<template>
  <CspTooltip
    :content="label"
    :disabled="isExpanded || isMobile"
    side="right"
    :side-offset="12"
  >
    <Primitive
      :as="to ? RouterLink : 'button'"
      :to="to"
      :type="to ? undefined : 'button'"
      class="csp-sidebar-item"
      :class="{
        'csp-sidebar-item--active': isActive,
        'csp-sidebar-item--expanded': isExpanded || isMobile,
      }"
      :aria-current="isActive ? 'page' : undefined"
    >
      <CspIcon
        class="csp-sidebar-item__icon"
        :name="icon"
        :size="16"
      />
      <span
        v-if="isExpanded || isMobile"
        class="csp-sidebar-item__label"
      >
        {{ label }}
      </span>
    </Primitive>
  </CspTooltip>
</template>

<style scoped lang="scss">
.csp-sidebar-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: var(--sidebar-item-size, 2.5rem);
  height: var(--sidebar-item-size, 2.5rem);
  padding: 0;
  border: none;
  background: var(--background-alt-grey);
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
    background: var(--background-alt-grey-hover);
  }

  &:active {
    background: var(--background-alt-grey-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-sidebar-item__icon {
  flex-shrink: 0;
  margin-left: 0.125rem;
}

.csp-sidebar-item__label {
  font-size: 0.875rem;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-item--active,
.csp-sidebar-item--active:hover,
.csp-sidebar-item--active:active {
  cursor: default;
  background: transparent;
  color: var(--text-active-blue-france);
}

.csp-sidebar-item--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: var(--csp-space-2);
  bottom: var(--csp-space-2);
  width: 2px;
  border-radius: 1px;
  background: var(--border-active-blue-france);
}

.csp-sidebar-item--active .csp-sidebar-item__label {
  font-weight: var(--csp-font-weight-medium);
}
</style>
