<script setup lang="ts">
import type { PaletteColor } from '@/styles/palette'
import { computed } from 'vue'
import { paletteVar } from '@/styles/palette'

const props = withDefaults(defineProps<{
  label: string
  color?: PaletteColor
  size?: 'sm' | 'md'
  bordered?: boolean
  clickable?: boolean
}>(), {
  color: 'grey',
  size: 'sm',
  bordered: true,
  clickable: false,
})

const colorStyle = computed(() => ({
  '--csp-label-background': paletteVar(props.color, 'background'),
  '--csp-label-text': paletteVar(props.color, 'text'),
  '--csp-label-dot': paletteVar(props.color, 'dot'),
}))
</script>

<template>
  <component
    :is="clickable ? 'button' : 'span'"
    :type="clickable ? 'button' : undefined"
    class="csp-label"
    :class="[`csp-label--${size}`, { 'csp-label--bordered': bordered, 'csp-label--clickable': clickable }]"
    :style="colorStyle"
  >
    <span
      class="csp-label__dot"
      aria-hidden="true"
    />
    <span class="csp-label__text">{{ label }}</span>
  </component>
</template>

<style scoped lang="scss">
.csp-label {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-label-gap);
  min-width: 0;
  max-width: 100%;
  padding: var(--csp-label-padding-y) var(--csp-label-padding-x);
  padding-inline-start: var(--csp-label-padding-start);
  border-radius: 0.25rem;
  background-color: var(--csp-label-background);
  color: var(--csp-label-text);
  font-size: var(--csp-label-font-size);
  font-weight: var(--csp-font-weight-medium);
  line-height: var(--csp-line-height-tight);
  white-space: nowrap;
}

.csp-label--bordered {
  box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--csp-label-dot) 26%, transparent);
}

.csp-label--clickable {
  margin: 0;
  border: none;
  font-family: inherit;
  cursor: pointer;
  transition: background-color var(--csp-motion-duration-state);

  &:hover {
    background-color: color-mix(in oklab, var(--csp-label-background), var(--csp-label-text) 10%);
  }

  &:active {
    background-color: color-mix(in oklab, var(--csp-label-background), var(--csp-label-text) 18%);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

.csp-label--sm {
  --csp-label-font-size: var(--csp-font-size-xs);
  --csp-label-padding-y: 0.3125rem;
  --csp-label-padding-x: var(--csp-space-2);
  --csp-label-padding-start: 0.375rem;
  --csp-label-gap: 0.3125rem;
}

.csp-label--md {
  --csp-label-font-size: var(--csp-font-size-base);
  --csp-label-padding-y: 0.4375rem;
  --csp-label-padding-x: 0.625rem;
  --csp-label-padding-start: var(--csp-space-2);
  --csp-label-gap: 0.375rem;
}

.csp-label__dot {
  flex-shrink: 0;
  width: 0.5em;
  height: 0.5em;
  border-radius: 50%;
  background-color: var(--csp-label-dot);
}

.csp-label__text {
  /* the vertical padding centers the capitals; accents and descenders overflow the trimmed box */
  text-box: trim-both cap alphabetic;
  min-width: 0;
  overflow-x: clip;
  overflow-y: visible;
  text-overflow: ellipsis;
}
</style>
