<script setup lang="ts">
import { AccordionRoot } from 'reka-ui'

export interface CspAccordionProps {
  type?: 'single' | 'multiple'
  collapsible?: boolean
  defaultValue?: string | string[]
}

withDefaults(defineProps<CspAccordionProps>(), {
  type: 'multiple',
  collapsible: true,
  defaultValue: undefined,
})
</script>

<template>
  <AccordionRoot
    class="csp-accordion"
    :type="type"
    :collapsible="collapsible"
    :default-value="defaultValue"
  >
    <slot />
  </AccordionRoot>
</template>

<style scoped lang="scss">
.csp-accordion {
  border-top: 1px solid var(--border-default-grey);
}
</style>
