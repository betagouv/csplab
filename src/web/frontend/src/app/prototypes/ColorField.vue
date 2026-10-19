<script setup lang="ts">
import type { PaletteColor } from '@/styles/palette'
import { RadioGroupRoot } from 'reka-ui'
import CspRadio from '@/components/base/CspRadio/CspRadio.vue'
import { PALETTE_COLOR_NAMES, PALETTE_COLORS, paletteVar } from '@/styles/palette'

const model = defineModel<PaletteColor>({ required: true })
</script>

<template>
  <RadioGroupRoot
    :model-value="model"
    as="fieldset"
    class="color-field"
    @update:model-value="value => model = value as PaletteColor"
  >
    <legend class="color-field__legend">
      Couleur
    </legend>
    <div class="color-field__options">
      <CspRadio
        v-for="color in PALETTE_COLORS"
        :key="color"
        class="color-field__option"
        :style="{
          '--color-field-swatch': paletteVar(color, 'dot'),
          '--color-field-background': paletteVar(color, 'background'),
          '--color-field-text': paletteVar(color, 'text'),
        }"
        :value="color"
        :label="PALETTE_COLOR_NAMES[color]"
      />
    </div>
  </RadioGroupRoot>
</template>

<style scoped lang="scss">
.color-field {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: none;
}

.color-field__legend {
  margin-bottom: var(--csp-field-legend-gap);
  padding: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.color-field__options {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3) var(--csp-space-4);
}

.color-field__option :deep(.csp-radio__label)::before {
  content: '';
  display: inline-block;
  width: 0.875rem;
  height: 0.875rem;
  margin-inline-end: var(--csp-space-2);
  border-radius: var(--csp-label-dot-radius, 50%);
  /* With --csp-label-dot-border-width undefined, the declaration is invalid at computed-value time and the swatch draws no shadow */
  box-shadow: inset 0 0 0 var(--csp-label-dot-border-width) var(--color-field-text);
  background-color: var(--color-field-swatch);
  vertical-align: -0.125rem;
}
</style>
