<script setup lang="ts">
import type { TooltipContentProps } from 'reka-ui'
import {
  TooltipArrow,
  TooltipContent,
  TooltipPortal,
  TooltipProvider,
  TooltipRoot,
  TooltipTrigger,
} from 'reka-ui'
import { computed } from 'vue'

interface CspTooltipProps {
  content?: string
  side?: TooltipContentProps['side']
  align?: TooltipContentProps['align']
  sideOffset?: number
  delayDuration?: number
  disabled?: boolean
}

const props = withDefaults(defineProps<CspTooltipProps>(), {
  content: undefined,
  side: 'right',
  align: 'center',
  sideOffset: 8,
  delayDuration: 200,
  disabled: false,
})

const open = defineModel<boolean | undefined>('open')

const isDisabled = computed(() => props.disabled || !props.content)
</script>

<template>
  <TooltipProvider
    v-if="!isDisabled"
    :delay-duration="delayDuration"
  >
    <TooltipRoot
      :open="open"
      @update:open="value => open = value"
    >
      <TooltipTrigger as-child>
        <slot />
      </TooltipTrigger>
      <TooltipPortal>
        <!-- aria-label: assistive technologies read the content text, whatever the content slot draws -->
        <TooltipContent
          :side="side"
          :align="align"
          :side-offset="sideOffset"
          :aria-label="content"
        >
          <div class="csp-tooltip">
            <slot name="content">
              {{ content }}
            </slot>
          </div>
          <TooltipArrow class="csp-tooltip__arrow" />
        </TooltipContent>
      </TooltipPortal>
    </TooltipRoot>
  </TooltipProvider>
  <slot v-else />
</template>

<style scoped lang="scss">
.csp-tooltip {
  z-index: var(--csp-z-tooltip);
  max-width: 16rem;
  padding: var(--csp-space-1) var(--csp-space-2);
  border-radius: var(--csp-tooltip-radius);
  background-color: var(--csp-tooltip-background);
  color: var(--csp-tooltip-color);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-medium);
  line-height: var(--csp-line-height-tight);
  box-shadow:
    var(--csp-overlap-shadow, var(--csp-shadow-md)),
    inset 0 0 0 1px var(--csp-tooltip-border-color);
  outline: none;
  pointer-events: none;
  user-select: none;
  overflow-wrap: anywhere;
  transform-origin: var(--reka-popper-transform-origin);
  animation: var(--csp-motion-overlap-enter, csp-fade-in 0.12s ease-out);

  &[data-state='closed'] {
    animation: var(--csp-motion-overlap-exit);
  }
}

:deep(.csp-tooltip__arrow) {
  fill: var(--csp-tooltip-background);
}
</style>
