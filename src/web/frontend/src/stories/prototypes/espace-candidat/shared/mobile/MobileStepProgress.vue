<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  steps: string[]
  currentIndex: number
}>()

const pourcentage = computed(() => ((props.currentIndex + 1) / props.steps.length) * 100)
</script>

<template>
  <div class="progress">
    <p class="progress__label">
      Étape {{ currentIndex + 1 }} sur {{ steps.length }} — {{ steps[currentIndex] }}
    </p>
    <div
      class="progress__track"
      role="progressbar"
      :aria-valuenow="currentIndex + 1"
      :aria-valuemin="1"
      :aria-valuemax="steps.length"
    >
      <div
        class="progress__fill"
        :style="{ width: `${pourcentage}%` }"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.progress {
  padding: var(--csp-space-3) var(--csp-space-4) var(--csp-space-2);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.progress__label {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-mention-grey);
}

.progress__track {
  height: 0.375rem;
  border-radius: 999px;
  background-color: var(--background-contrast-grey);
  overflow: hidden;
}

.progress__fill {
  height: 100%;
  border-radius: 999px;
  background-color: var(--background-action-high-blue-france);
  transition: width 0.2s ease;
}
</style>
