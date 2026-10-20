<script setup lang="ts">
import type { CspTabItem } from './CspTabs.vue'
import { injectTabsRootContext, TabsContent } from 'reka-ui'
import { useSlots, watch } from 'vue'

defineProps<{
  tabs: CspTabItem[]
  fill?: boolean
}>()

const slots = useSlots()
const root = injectTabsRootContext()

// TabsContent registers its value on mount only; the shared panel follows the active tab, so it registers each new value to keep the triggers' aria-controls.
watch(root.modelValue, (value, previous) => {
  if (!slots.default) {
    return
  }
  if (previous !== undefined) {
    root.unregisterContent(previous)
  }
  if (value !== undefined) {
    root.registerContent(value)
  }
})
</script>

<template>
  <div
    class="csp-tabs__panels"
    :class="{ 'csp-tabs__panels--fill': fill }"
  >
    <TabsContent
      v-if="$slots.default && root.modelValue.value !== undefined"
      :value="root.modelValue.value"
      class="csp-tabs__content"
    >
      <slot />
    </TabsContent>
    <TabsContent
      v-for="tab in tabs"
      v-else
      :key="tab.value"
      :value="tab.value"
      class="csp-tabs__content"
    >
      <slot :name="tab.value" />
    </TabsContent>
  </div>
</template>

<style scoped lang="scss">
.csp-tabs__panels--fill {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.csp-tabs__panels--fill .csp-tabs__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.csp-tabs__content {
  &[data-orientation='vertical'] {
    padding-top: 0;
    padding-left: 1rem;
  }

  &:focus-visible {
    outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
    outline-offset: var(--csp-focus-ring-offset);
  }
}
</style>
