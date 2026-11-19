<script setup lang="ts">
import {
  PopoverAnchor,
  PopoverContent,
  PopoverPortal,
  PopoverRoot,
  PopoverTrigger,
} from 'reka-ui'
import { ref, useSlots } from 'vue'

defineOptions({ inheritAttrs: false })

withDefaults(defineProps<{
  side?: 'top' | 'right' | 'bottom' | 'left'
  align?: 'start' | 'center' | 'end'
  padding?: 'default' | 'menu'
  collisionPadding?: number
}>(), {
  side: 'bottom',
  align: 'start',
  padding: 'default',
  collisionPadding: 16,
})

const open = defineModel<boolean | undefined>('open')

const slots = useSlots()

const anchor = ref<InstanceType<typeof PopoverAnchor> | null>(null)
const interactedOutside = ref(false)

function rememberOutsideInteraction(event: Event): void {
  if (!event.defaultPrevented) {
    interactedOutside.value = true
  }
}

function focusAnchor(event: Event): void {
  if (slots.trigger || !slots.anchor) {
    return
  }
  event.preventDefault()
  if (interactedOutside.value) {
    return
  }
  const element: unknown = anchor.value?.$el
  if (element instanceof HTMLElement) {
    element.querySelector<HTMLElement>('button, [href], input, [tabindex]:not([tabindex="-1"])')?.focus()
  }
}
</script>

<template>
  <PopoverRoot
    :open="open"
    @update:open="value => open = value"
  >
    <PopoverTrigger
      v-if="$slots.trigger"
      as-child
    >
      <slot name="trigger" />
    </PopoverTrigger>

    <PopoverAnchor
      v-if="$slots.anchor"
      ref="anchor"
      as-child
    >
      <slot name="anchor" />
    </PopoverAnchor>

    <PopoverPortal>
      <PopoverContent
        v-bind="$attrs"
        class="csp-popover"
        :class="{ 'csp-popover--menu': padding === 'menu' }"
        :side="side"
        :align="align"
        :side-offset="6"
        :collision-padding="collisionPadding"
        @open-auto-focus="interactedOutside = false"
        @interact-outside="rememberOutsideInteraction"
        @close-auto-focus="focusAnchor"
      >
        <slot />
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>

<style lang="scss">
.csp-popover {
  min-width: 12rem;
  max-width: min(var(--csp-popover-width), var(--reka-popover-content-available-width));
  background-color: var(--background-overlap-grey);
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-overlap-shadow);
  padding: var(--csp-space-4);
  z-index: var(--csp-z-dropdown);
  outline: none;
  transform-origin: var(--reka-popper-transform-origin);

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

.csp-popover--menu {
  padding: var(--csp-menu-padding);
}
</style>
