<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useSidebar } from '@/composables/ui/useSidebar'

withDefaults(defineProps<{
  title: string
  description?: string
  static?: boolean
}>(), {
  description: undefined,
  static: false,
})

const { showLabels } = useSidebar()
</script>

<template>
  <component
    :is="static ? 'div' : 'button'"
    :type="static ? undefined : 'button'"
    class="csp-sidebar-button"
    :class="{ 'csp-sidebar-button--static': static }"
  >
    <span class="csp-sidebar-button__leading">
      <slot name="leading" />
    </span>
    <template v-if="showLabels">
      <span class="csp-sidebar-button__text">
        <span class="csp-sidebar-button__title">{{ title }}</span>
        <span
          v-if="description"
          class="csp-sidebar-button__description"
        >{{ description }}</span>
      </span>
      <CspIcon
        v-if="!static"
        name="ri:expand-up-down-line"
        :size="16"
        class="csp-sidebar-button__chevron"
      />
    </template>
    <span
      v-else-if="static"
      class="sr-only"
    >{{ title }}</span>
  </component>
</template>

<style scoped lang="scss">
.csp-sidebar-button {
  display: flex;
  align-items: center;
  gap: var(--sidebar-leading-gap);
  min-width: 0;
  padding-block: var(--csp-space-2);
  padding-inline: var(--sidebar-item-padding-inline);
  cursor: pointer;
  background-color: var(--background-alt-grey);
  transition: background-color var(--csp-motion-duration-state);

  &:hover {
    background-color: var(--background-alt-grey-hover);
  }

  &:active {
    background-color: var(--background-alt-grey-active);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

.csp-sidebar-button--static {
  cursor: default;

  &:hover,
  &:active {
    background-color: var(--background-alt-grey);
  }
}

.csp-sidebar-button__leading {
  display: flex;
  flex-shrink: 0;
}

.csp-sidebar-button__text {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  text-align: left;
  line-height: 1.2;
}

.csp-sidebar-button__title {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  overflow-wrap: anywhere;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.csp-sidebar-button__description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.csp-sidebar-button__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
