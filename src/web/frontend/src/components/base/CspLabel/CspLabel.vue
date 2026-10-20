<script setup lang="ts">
import type { PaletteColor } from '@/styles/palette'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { paletteVar } from '@/styles/palette'

const props = withDefaults(defineProps<{
  label: string
  color?: PaletteColor
  size?: 'sm' | 'md'
  removable?: boolean
  removeLabel?: string
}>(), {
  color: 'grey',
  size: 'sm',
  removable: false,
  removeLabel: undefined,
})

const emit = defineEmits<{
  remove: []
}>()

// Optional palette variables: when a palette leaves them undefined, the remove button keeps its translucent states
const colorStyle = computed(() => ({
  '--csp-label-background': paletteVar(props.color, 'background'),
  '--csp-label-text': paletteVar(props.color, 'text'),
  '--csp-label-dot': paletteVar(props.color, 'dot'),
  '--csp-label-remove-hover-background': `var(--csp-palette-${props.color}-background-hover)`,
  '--csp-label-remove-active-background': `var(--csp-palette-${props.color}-background-active)`,
}))
</script>

<template>
  <span
    class="csp-label"
    :class="`csp-label--${size}`"
    :data-color="color"
    :style="colorStyle"
  >
    <span
      class="csp-label__dot"
      aria-hidden="true"
    />
    <span class="csp-label__text">{{ label }}</span>
    <button
      v-if="removable"
      type="button"
      class="csp-label__remove"
      :aria-label="removeLabel ?? `Retirer l’étiquette ${label}`"
      @click="emit('remove')"
    >
      <CspIcon
        name="ri:close-line"
        size="1em"
      />
    </button>
  </span>
</template>

<style scoped lang="scss">
/*
 * Variables a theme may set on an ancestor: --csp-label-radius, --csp-label-border-color, --csp-label-padding-start,
 * --csp-label-white-space, the dot ones --csp-label-dot-display, --csp-label-dot-size, --csp-label-dot-radius and
 * --csp-label-dot-border-width, and --csp-label-remove-state-color for the icon of the remove button on hover and when pressed.
 */
.csp-label {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-label-gap);
  min-width: 0;
  max-width: 100%;
  padding: var(--csp-label-padding-y) var(--csp-label-padding-x);
  padding-inline-start: var(--csp-label-padding-start, var(--csp-label-padding-x));
  border-radius: var(--csp-label-radius, var(--csp-badge-radius));
  box-shadow: inset 0 0 0 1px var(--csp-label-border-color, transparent);
  background-color: var(--csp-label-background);
  color: var(--csp-label-text);
  font-size: var(--csp-label-font-size);
  font-weight: var(--csp-font-weight-medium);
  line-height: var(--csp-line-height-tight);
  white-space: var(--csp-label-white-space, nowrap);
}

.csp-label--sm {
  --csp-label-font-size: 0.75rem;
  --csp-label-padding-y: 0.125rem;
  --csp-label-padding-x: 0.5rem;
  --csp-label-gap: 0.3125rem;
}

.csp-label--md {
  --csp-label-font-size: 0.875rem;
  --csp-label-padding-y: 0.1875rem;
  --csp-label-padding-x: 0.625rem;
  --csp-label-gap: 0.375rem;
}

.csp-label__dot {
  display: var(--csp-label-dot-display, none);
  flex-shrink: 0;
  width: var(--csp-label-dot-size, 0.5rem);
  height: var(--csp-label-dot-size, 0.5rem);
  /* centered on the first line of the text, which wraps when the label allows it */
  margin-block: calc((var(--csp-line-height-tight) * 1em - var(--csp-label-dot-size, 0.5rem)) / 2);
  border-radius: var(--csp-label-dot-radius, 50%);
  /* With --csp-label-dot-border-width undefined, the declaration is invalid at computed-value time and the dot draws no shadow */
  box-shadow: inset 0 0 0 var(--csp-label-dot-border-width) var(--csp-label-text);
  background-color: var(--csp-label-dot);
}

.csp-label__text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-label__remove {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-inline-end: calc(-1 * var(--csp-space-1));
  padding: 0.125rem;
  border: none;
  border-radius: 2px;
  background: transparent;
  color: inherit;
  cursor: pointer;

  /* 24 px target (WCAG 2.5.8) around the smaller drawn button */
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 1.5rem;
    height: 1.5rem;
    transform: translate(-50%, -50%);
  }

  &:hover {
    background-color: var(--csp-label-remove-hover-background, color-mix(in srgb, currentColor 12%, transparent));
    color: var(--csp-label-remove-state-color, currentColor);
  }

  &:active {
    background-color: var(--csp-label-remove-active-background, color-mix(in srgb, currentColor 20%, transparent));
    color: var(--csp-label-remove-state-color, currentColor);
  }

  &:focus-visible {
    outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
    outline-offset: 1px;
  }
}
</style>
