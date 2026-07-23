<script setup lang="ts">
import { TabsRoot } from 'reka-ui'
import CspTabsList from './CspTabsList.vue'
import CspTabsPanels from './CspTabsPanels.vue'

export interface CspTabItem {
  value: string
  label: string
  icon?: string
  disabled?: boolean
}

export interface CspTabsProps {
  /** When omitted, compose CspTabsList and CspTabsPanels in the default slot. */
  tabs?: CspTabItem[]
  defaultValue?: string
  orientation?: 'horizontal' | 'vertical'
  activationMode?: 'automatic' | 'manual'
  fill?: boolean
}

withDefaults(defineProps<CspTabsProps>(), {
  tabs: undefined,
  defaultValue: undefined,
  orientation: 'horizontal',
  activationMode: 'automatic',
  fill: false,
})

const model = defineModel<string>()
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
