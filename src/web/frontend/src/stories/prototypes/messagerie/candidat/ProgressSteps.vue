<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  steps: string[]
  currentIndex: number
}>()

const next = computed(() => props.steps[props.currentIndex + 1])
</script>

<template>
  <div class="progress-steps">
    <h2 class="progress-steps__title">
      {{ steps[currentIndex] }}
      <span class="progress-steps__state">Étape {{ currentIndex + 1 }} sur {{ steps.length }}</span>
    </h2>
    <div
      class="progress-steps__bar"
      aria-hidden="true"
    >
      <span
        v-for="(step, index) in steps"
        :key="step"
        class="progress-steps__segment"
        :class="{ 'progress-steps__segment--done': index <= currentIndex }"
      />
    </div>
    <p
      v-if="next"
      class="progress-steps__next"
    >
      <span class="progress-steps__next-label">Étape suivante :</span> {{ next }}
    </p>
  </div>
</template>

<style scoped>
.progress-steps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.progress-steps__title {
  display: flex;
  flex-direction: column-reverse;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.progress-steps__state {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.progress-steps__bar {
  display: grid;
  grid-auto-columns: 1fr;
  grid-auto-flow: column;
  gap: var(--csp-space-1);
}

.progress-steps__segment {
  height: 0.5rem;
  background: var(--background-contrast-grey);
}

.progress-steps__segment--done {
  background: var(--background-active-blue-france);
}

.progress-steps__next {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.progress-steps__next-label {
  font-weight: var(--csp-font-weight-bold);
}
</style>
