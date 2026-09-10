<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  steps: string[]
  currentIndex: number
}>()
</script>

<template>
  <ol
    class="stepper"
    aria-label="Étapes de la candidature"
  >
    <li
      v-for="(step, index) in steps"
      :key="step"
      class="stepper__item"
      :class="{
        'stepper__item--done': index < currentIndex,
        'stepper__item--current': index === currentIndex,
      }"
      :aria-current="index === currentIndex ? 'step' : undefined"
    >
      <span class="stepper__marker">
        <CspIcon
          v-if="index < currentIndex"
          name="ri:check-line"
          :size="14"
        />
        <span v-else>{{ index + 1 }}</span>
      </span>
      <span class="stepper__label">{{ step }}</span>
    </li>
  </ol>
</template>

<style scoped lang="scss">
.stepper {
  display: flex;
  align-items: flex-start;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--csp-space-2);
}

.stepper__item {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  text-align: center;
  position: relative;
  min-width: 0;

  &:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 0.75rem;
    left: calc(50% + 1.25rem);
    right: calc(-50% + 1.25rem);
    height: 2px;
    background-color: var(--border-default-grey);
  }

  &--done:not(:last-child)::after {
    background-color: var(--text-action-high-blue-france);
  }
}

.stepper__marker {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  background-color: var(--background-contrast-grey);
  color: var(--text-mention-grey);
  z-index: 1;
}

.stepper__item--current .stepper__marker {
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-grey);
}

.stepper__item--done .stepper__marker {
  background-color: var(--text-action-high-blue-france);
  color: var(--text-inverted-grey);
}

.stepper__label {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  line-height: 1.3;
}

.stepper__item--current .stepper__label {
  color: var(--text-default-grey);
  font-weight: 600;
}
</style>
