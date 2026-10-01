<script setup lang="ts">
import type { CspTabItem } from './CspTabs.vue'
import { TabsList, TabsTrigger } from 'reka-ui'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  tabs: CspTabItem[]
}>()
</script>

<template>
  <TabsList class="csp-tabs__list">
    <TabsTrigger
      v-for="tab in tabs"
      :key="tab.value"
      :value="tab.value"
      :disabled="tab.disabled"
      class="csp-tabs__trigger"
    >
      <CspIcon
        v-if="tab.icon"
        :name="tab.icon"
        class="csp-tabs__icon"
      />
      {{ tab.label }}
    </TabsTrigger>
  </TabsList>
</template>

<style scoped lang="scss">
.csp-tabs__list {
  --csp-tabs-trigger-padding-inline: var(--csp-space-4);

  display: flex;
  gap: var(--csp-space-1, 0.25rem);
  // Aligns the trigger labels with content inset by --csp-tabs-content-padding-inline
  padding-inline: max(0px, var(--csp-tabs-content-padding-inline, 0px) - var(--csp-tabs-trigger-padding-inline));
  overflow-x: auto;
  scrollbar-width: thin;
  border-bottom: 1px solid var(--border-default-grey);

  &[data-orientation='vertical'] {
    flex-direction: column;
    padding-inline: 0;
    border-bottom: none;
    border-right: 1px solid var(--border-default-grey);
  }
}

.csp-tabs__trigger {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  gap: 0.5rem;
  padding: var(--csp-space-3) var(--csp-tabs-trigger-padding-inline);
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.25;
  color: var(--text-action-high-grey);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;

  &:hover:not([data-disabled]) {
    background-color: var(--background-default-grey-hover);
  }

  &:active:not([data-disabled]) {
    background-color: var(--background-default-grey-active);
  }

  &[data-state='active'] {
    color: var(--text-action-high-blue-france);
    border-bottom-color: var(--border-action-high-blue-france);
  }

  &[data-disabled] {
    color: var(--text-disabled-grey);
    cursor: not-allowed;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }

  &[data-orientation='vertical'] {
    justify-content: flex-start;
    border-bottom: none;
    border-right: 2px solid transparent;

    &[data-state='active'] {
      border-bottom-color: transparent;
      border-right-color: var(--border-action-high-blue-france);
    }
  }
}

.csp-tabs__icon {
  width: 1.125em;
  height: 1.125em;
  flex-shrink: 0;
}
</style>
