<script setup lang="ts" generic="V extends string = string">
import { useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspSegmentedControlOption<V extends string = string> {
  value: V
  label: string
  icon?: string
  disabled?: boolean
}

export interface CspSegmentedControlProps<V extends string = string> {
  options: CspSegmentedControlOption<V>[]
  legend: string
  hideLegend?: boolean
  inlineLegend?: boolean
  size?: 'sm' | 'md'
  name?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<CspSegmentedControlProps<V>>(), {
  hideLegend: false,
  inlineLegend: false,
  size: 'md',
  name: undefined,
  disabled: false,
})

const model = defineModel<V>({ required: true })

const groupName = props.name ?? useId()
</script>

<template>
  <fieldset
    class="csp-segmented"
    :class="[`csp-segmented--${size}`, { 'csp-segmented--no-legend': hideLegend }]"
    :disabled="disabled"
  >
    <legend
      class="csp-segmented__legend"
      :class="{ 'csp-segmented__legend--inline': inlineLegend }"
    >
      {{ legend }}
    </legend>
    <div class="csp-segmented__elements">
      <div
        v-for="option in options"
        :key="option.value"
        class="csp-segmented__element"
      >
        <input
          :id="`${groupName}-${option.value}`"
          v-model="model"
          type="radio"
          :name="groupName"
          :value="option.value"
          :disabled="option.disabled"
        >
        <label :for="`${groupName}-${option.value}`">
          <CspIcon
            v-if="option.icon"
            :name="option.icon"
            class="csp-segmented__icon"
          />
          {{ option.label }}
        </label>
      </div>
    </div>
  </fieldset>
</template>

<style scoped lang="scss">
.csp-segmented {
  display: inline-flex;
  align-items: center;
  margin: 0;
  padding: 0;
  border: 0;
  --csp-segmented-font-size: 1rem;
  --csp-segmented-padding: 0.5rem 1rem;
  --csp-segmented-icon-size: 1.5rem;
}

.csp-segmented--sm {
  --csp-segmented-font-size: 0.875rem;
  --csp-segmented-padding: 0.25rem 0.75rem;
  --csp-segmented-icon-size: 1.25rem;
}

.csp-segmented__legend {
  margin-bottom: var(--csp-space-3);
  padding: 0;
  font-size: var(--csp-segmented-font-size);
  color: var(--text-default-grey);
}

.csp-segmented__legend--inline {
  float: left;
  display: contents;

  ~ .csp-segmented__elements {
    margin-left: var(--csp-space-4);
  }
}

.csp-segmented--no-legend .csp-segmented__legend {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}

.csp-segmented__elements {
  display: flex;
  border-radius: 0.25rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.csp-segmented__element {
  position: relative;
  isolation: isolate;
}

.csp-segmented__element input {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  opacity: 0;
  z-index: -1;
}

.csp-segmented__element label {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: var(--csp-segmented-padding);
  border-radius: 0.25rem;
  font-size: var(--csp-segmented-font-size);
  font-weight: 500;
  line-height: 1.5rem;
  color: var(--text-action-high-grey);
  white-space: nowrap;
  cursor: pointer;
}

.csp-segmented__element label::before {
  content: '';
  position: absolute;
  inset: 0.25rem;
  border-radius: 0.25rem;
  z-index: -1;
}

.csp-segmented__icon {
  width: var(--csp-segmented-icon-size);
  height: var(--csp-segmented-icon-size);
  flex-shrink: 0;
}

.csp-segmented__element input:not(:disabled):not(:checked) ~ label:hover::before {
  background-color: var(--background-default-grey-hover);
}

.csp-segmented__element input:not(:disabled):not(:checked) ~ label:active::before {
  background-color: var(--background-default-grey-active);
}

.csp-segmented__element input:checked ~ label {
  box-shadow: inset 0 0 0 1px var(--border-active-blue-france);
  color: var(--text-active-blue-france);
}

.csp-segmented__element input:disabled ~ label,
.csp-segmented:disabled label {
  color: var(--text-disabled-grey);
  cursor: not-allowed;
}

.csp-segmented__element input:checked:disabled ~ label,
.csp-segmented:disabled input:checked ~ label {
  box-shadow: inset 0 0 0 1px var(--border-disabled-grey);
}

.csp-segmented__element input:focus-visible ~ label {
  outline: var(--focus-ring);
  outline-offset: var(--csp-focus-ring-offset);
}
</style>
