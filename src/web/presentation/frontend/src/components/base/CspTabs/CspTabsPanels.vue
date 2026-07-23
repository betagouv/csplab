<script setup lang="ts">
import type { CspTabItem } from './CspTabs.vue'
import { TabsContent } from 'reka-ui'

defineProps<{
  tabs: CspTabItem[]
  fill?: boolean
}>()
</script>

<template>
  <div
    class="csp-tabs__panels"
    :class="{ 'csp-tabs__panels--fill': fill }"
  >
    <TabsContent
      v-for="tab in tabs"
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
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
