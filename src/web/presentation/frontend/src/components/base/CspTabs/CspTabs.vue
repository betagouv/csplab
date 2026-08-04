<script setup lang="ts" generic="T extends string = string">
import { TabsRoot } from 'reka-ui'
import CspTabsList from './CspTabsList.vue'
import CspTabsPanels from './CspTabsPanels.vue'

export interface CspTabItem<V extends string = string> {
  value: V
  label: string
  icon?: string
  disabled?: boolean
}

export interface CspTabsProps<V extends string = string> {
  /** When omitted, compose CspTabsList and CspTabsPanels in the default slot. */
  tabs?: CspTabItem<V>[]
  defaultValue?: V
  orientation?: 'horizontal' | 'vertical'
  activationMode?: 'automatic' | 'manual'
  fill?: boolean
}

withDefaults(defineProps<CspTabsProps<T>>(), {
  tabs: undefined,
  defaultValue: undefined,
  orientation: 'horizontal',
  activationMode: 'automatic',
  fill: false,
})

const model = defineModel<T>()
</script>

<template>
  <TabsRoot
    v-model="model"
    class="csp-tabs"
    :class="[`csp-tabs--${orientation}`, { 'csp-tabs--fill': fill }]"
    :default-value="defaultValue"
    :orientation="orientation"
    :activation-mode="activationMode"
  >
    <slot>
      <template v-if="tabs">
        <CspTabsList :tabs="tabs" />
        <CspTabsPanels :tabs="tabs">
          <template
            v-for="tab in tabs"
            #[tab.value]
          >
            <slot :name="tab.value" />
          </template>
        </CspTabsPanels>
      </template>
    </slot>
  </TabsRoot>
</template>

<style scoped lang="scss">
.csp-tabs {
  display: flex;
  flex-direction: column;
}

.csp-tabs--fill {
  flex: 1;
  min-height: 0;
}

.csp-tabs--vertical {
  flex-direction: row;
}
</style>
