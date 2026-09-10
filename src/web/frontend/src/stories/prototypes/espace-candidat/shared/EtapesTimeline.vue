<script setup lang="ts">
import type { EtapeTimeline } from '../data/candidatMock'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  etapes: EtapeTimeline[]
}>()
</script>

<template>
  <ol class="timeline">
    <li
      v-for="etape in etapes"
      :key="etape.id"
      class="timeline__item"
      :class="`timeline__item--${etape.statut}`"
    >
      <span class="timeline__marker">
        <CspIcon
          v-if="etape.statut === 'fait'"
          name="ri:check-line"
          :size="14"
        />
        <span
          v-else-if="etape.statut === 'en_cours'"
          class="timeline__pulse"
        />
      </span>
      <div class="timeline__body">
        <p class="timeline__label">
          {{ etape.label }}
        </p>
        <p
          v-if="etape.date"
          class="timeline__date"
        >
          {{ etape.date }}
        </p>
        <p
          v-else-if="etape.statut === 'en_cours'"
          class="timeline__date timeline__date--current"
        >
          En cours
        </p>
      </div>
    </li>
  </ol>
</template>

<style scoped lang="scss">
.timeline {
  list-style: none;
  margin: 0;
  padding: 0;
}

.timeline__item {
  display: flex;
  gap: var(--csp-space-4);
  position: relative;
  padding-bottom: var(--csp-space-5);

  &:not(:last-child)::before {
    content: '';
    position: absolute;
    left: 0.6875rem;
    top: 1.5rem;
    bottom: 0;
    width: 2px;
    background-color: var(--border-default-grey);
  }

  &--fait:not(:last-child)::before {
    background-color: var(--text-action-high-blue-france);
  }

  &:last-child {
    padding-bottom: 0;
  }
}

.timeline__marker {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background-color: var(--background-contrast-grey);
  color: var(--text-inverted-grey);
  z-index: 1;
}

.timeline__item--fait .timeline__marker {
  background-color: var(--text-action-high-blue-france);
}

.timeline__item--en_cours .timeline__marker {
  background-color: var(--background-action-high-blue-france);
  box-shadow: 0 0 0 4px var(--background-alt-blue-france);
}

.timeline__pulse {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--text-inverted-grey);
}

.timeline__body {
  padding-top: 0.0625rem;
}

.timeline__label {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-mention-grey);
}

.timeline__item--fait .timeline__label,
.timeline__item--en_cours .timeline__label {
  color: var(--text-title-grey);
}

.timeline__date {
  margin: 0.125rem 0 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.timeline__date--current {
  color: var(--text-action-high-blue-france);
  font-weight: 600;
}
</style>
