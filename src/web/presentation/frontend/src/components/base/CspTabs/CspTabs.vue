<script setup lang="ts">
import { TabsContent, TabsList, TabsRoot, TabsTrigger } from 'reka-ui'

export interface CspTabItem {
  value: string
  label: string
  disabled?: boolean
}

export interface CspTabsProps {
  tabs: CspTabItem[]
  defaultValue?: string
  orientation?: 'horizontal' | 'vertical'
  activationMode?: 'automatic' | 'manual'
}

withDefaults(defineProps<CspTabsProps>(), {
  defaultValue: undefined,
  orientation: 'horizontal',
  activationMode: 'automatic',
})

const model = defineModel<string>()
</script>

<template>
  <TabsRoot
    v-model="model"
    class="csp-tabs"
    :class="`csp-tabs--${orientation}`"
    :default-value="defaultValue"
    :orientation="orientation"
    :activation-mode="activationMode"
  >
    <TabsList class="csp-tabs__list">
      <TabsTrigger
        v-for="tab in tabs"
        :key="tab.value"
        :value="tab.value"
        :disabled="tab.disabled"
        class="csp-tabs__trigger"
      >
        {{ tab.label }}
      </TabsTrigger>
    </TabsList>

    <div class="csp-tabs__panels">
      <TabsContent
        v-for="tab in tabs"
        :key="tab.value"
        :value="tab.value"
        class="csp-tabs__content"
      >
        <slot :name="tab.value" />
      </TabsContent>
    </div>
  </TabsRoot>
</template>

<style scoped lang="scss">
.csp-tabs {
  display: flex;
  flex-direction: column;
}

.csp-tabs--vertical {
  flex-direction: row;

  .csp-tabs__list {
    flex-direction: column;
    border-bottom: none;
    border-right: 1px solid var(--border-default-grey);
  }

  .csp-tabs__trigger {
    border-bottom: none;
    border-right: 2px solid transparent;
    justify-content: flex-start;

    &[data-state='active'] {
      border-bottom-color: transparent;
      border-right-color: var(--border-action-high-blue-france);
    }
  }

  .csp-tabs__panels {
    padding-left: var(--csp-space-4, 1rem);
  }
}

.csp-tabs__list {
  display: flex;
  border-bottom: 1px solid var(--border-default-grey);
  gap: var(--csp-space-1, 0.25rem);
}

.csp-tabs__trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--csp-space-3, 0.75rem) var(--csp-space-4, 1rem);
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.25;
  color: var(--text-action-high-grey);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background-color 0.2s ease;

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
}

.csp-tabs__panels {
  padding-top: var(--csp-space-4, 1rem);
}

.csp-tabs__content {
  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
