<script setup lang="ts">
import {
  PopoverContent,
  PopoverPortal,
  PopoverRoot,
  PopoverTrigger,
} from 'reka-ui'
import { useSlots } from 'vue'

defineOptions({ inheritAttrs: false })

withDefaults(defineProps<{
  side?: 'top' | 'right' | 'bottom' | 'left'
  align?: 'start' | 'center' | 'end'
}>(), {
  side: 'bottom',
  align: 'start',
})

const open = defineModel<boolean | undefined>('open')

const slots = useSlots()
const hasTrigger = Boolean(slots.trigger)
</script>

<template>
  <PopoverRoot
    :open="open"
    @update:open="value => open = value"
  >
    <!-- $attrs go to the trigger: a tooltip that wraps the popover passes the props of its own trigger this way -->
    <PopoverTrigger
      v-if="hasTrigger"
      as-child
      v-bind="$attrs"
    >
      <slot name="trigger" />
    </PopoverTrigger>

    <PopoverPortal>
      <PopoverContent
        class="csp-popover"
        :side="side"
        :align="align"
        :side-offset="6"
      >
        <slot />
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>

<style lang="scss">
.csp-popover {
  min-width: 12rem;
  max-width: 22rem;
  background-color: var(--background-overlap-grey);
  border-radius: var(--csp-overlap-radius, 0);
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-overlap-shadow, var(--csp-shadow-lg));
  padding: var(--csp-space-4);
  z-index: var(--csp-z-dropdown);
  outline: none;

  &[data-state='open'] {
    animation: var(--csp-motion-overlap-enter);
  }

  &[data-state='closed'] {
    animation: var(--csp-motion-overlap-exit);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
