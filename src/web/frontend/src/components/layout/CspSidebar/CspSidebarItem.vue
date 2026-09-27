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
  --sidebar-item-icon-size: 1rem;
  --sidebar-item-icon-start: calc((var(--sidebar-item-size) - var(--sidebar-item-icon-size)) / 2);
  --sidebar-item-marker-width: 2px;

  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sidebar-leading-gap);
  width: var(--sidebar-item-size);
  height: var(--sidebar-item-size);
  padding: 0;
  border: none;
  background: var(--background-alt-grey);
  text-decoration: none;
  cursor: pointer;
  flex-shrink: 0;

  &--expanded {
    justify-content: flex-start;
    width: 100%;
    padding-inline: var(--sidebar-item-padding-inline);
    --sidebar-item-icon-start: calc(
      var(--sidebar-item-padding-inline) + (var(--sidebar-leading-size) - var(--sidebar-item-icon-size)) / 2
    );
  }

  &:hover {
    background: var(--background-alt-grey-hover);
  }

  &:active {
    background: var(--background-alt-grey-active);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

.csp-sidebar-item__icon {
  flex-shrink: 0;

  .csp-sidebar-item--expanded & {
    margin-left: calc(var(--sidebar-item-icon-start) - var(--sidebar-item-padding-inline));
  }
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
  left: calc(var(--sidebar-item-icon-start) - var(--sidebar-leading-gap) - var(--sidebar-item-marker-width));
  top: var(--csp-space-2);
  bottom: var(--csp-space-2);
  width: var(--sidebar-item-marker-width);
  border-radius: 1px;
  background: var(--border-active-blue-france);
}

.csp-sidebar-item--active .csp-sidebar-item__label {
  font-weight: var(--csp-font-weight-medium);
}
</style>
