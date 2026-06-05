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

const isDisabled = computed(() => props.disabled || !props.content)
</script>

<template>
  <TooltipProvider
    v-if="!isDisabled"
    :delay-duration="delayDuration"
  >
    <TooltipRoot>
      <TooltipTrigger as-child>
        <slot />
      </TooltipTrigger>
      <TooltipPortal>
        <TooltipContent
          :side="side"
          :align="align"
          :side-offset="sideOffset"
        >
          <div class="csp-tooltip">
            {{ content }}
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
  --csp-tooltip-bg: var(--background-action-high-grey);
  --csp-tooltip-text: var(--text-inverted-grey);

  z-index: var(--csp-z-tooltip);
  max-width: 16rem;
  padding: var(--csp-space-1) var(--csp-space-2);
  border-radius: 0.25rem;
  background-color: var(--csp-tooltip-bg);
  color: var(--csp-tooltip-text);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-medium);
  line-height: var(--csp-line-height-tight);
  box-shadow: var(--csp-shadow-md);
  outline: none;
  pointer-events: none;
  user-select: none;
  overflow-wrap: anywhere;
  animation: csp-tooltip-fade-in 0.12s ease-out;
}

:deep(.csp-tooltip__arrow) {
  fill: var(--background-action-high-grey);
  animation: csp-tooltip-fade-in 0.12s ease-out;
}

@keyframes csp-tooltip-fade-in {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>
