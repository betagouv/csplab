<script setup lang="ts">
import { Separator } from 'reka-ui'

export interface CspSeparatorProps {
  orientation?: 'horizontal' | 'vertical'
  decorative?: boolean
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'subtle' | 'strong'
}

withDefaults(defineProps<CspSeparatorProps>(), {
  orientation: 'horizontal',
  decorative: false,
  size: 'md',
  variant: 'default',
})
</script>

<template>
  <Separator
    class="csp-separator"
    :class="[
      `csp-separator--${orientation}`,
      `csp-separator--${size}`,
      `csp-separator--${variant}`,
    ]"
    :orientation="orientation"
    :decorative="decorative"
  />
</template>

<style scoped lang="scss">
.csp-separator {
  flex-shrink: 0;
  background-color: var(--csp-separator-color);

  --csp-separator-color: var(--border-default-grey);
  --csp-separator-size: 1px;
}

.csp-separator--horizontal {
  width: 100%;
  height: var(--csp-separator-size);
}

.csp-separator--vertical {
  height: 100%;
  width: var(--csp-separator-size);
}

.csp-separator--sm {
  --csp-separator-size: 1px;
}

.csp-separator--md {
  --csp-separator-size: 1px;
}

.csp-separator--lg {
  --csp-separator-size: 2px;
}

.csp-separator--subtle {
  --csp-separator-color: var(--border-disabled-grey);
}

.csp-separator--default {
  --csp-separator-color: var(--border-default-grey);
}

.csp-separator--strong {
  --csp-separator-color: var(--border-plain-grey);
}
</style>
