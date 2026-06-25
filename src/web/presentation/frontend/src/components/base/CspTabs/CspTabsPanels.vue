<script setup lang="ts">
import type { CspTabItem } from './CspTabs.vue'
import { TabsContent } from 'reka-ui'

defineProps<{
  tabs: CspTabItem[]
}>()
</script>

<template>
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
</template>

<style scoped lang="scss">
.csp-tabs__content {
  padding-top: 1rem;

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
