<script setup lang="ts">
import type { EtapeTimeline } from '../data/candidatMock'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  etapes: EtapeTimeline[]
}>()
</script>

<template>
  <ol class="resume">
    <li
      v-for="(etape, index) in etapes"
      :key="etape.id"
      class="resume__item"
      :class="`resume__item--${etape.statut}`"
    >
      <span class="resume__puce">
        <CspIcon
          v-if="etape.statut === 'fait'"
          name="ri:check-line"
          :size="12"
        />
        <span v-else-if="etape.statut === 'en_cours'">●</span>
        <span v-else>○</span>
      </span>
      <span class="resume__label">{{ etape.label }}</span>
      <CspIcon
        v-if="index < etapes.length - 1"
        name="ri:arrow-right-s-line"
        :size="16"
        class="resume__chevron"
      />
    </li>
  </ol>
</template>

<style scoped lang="scss">
.resume {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--csp-space-1);
}

.resume__item {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
}

.resume__puce {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
  font-size: 0.625rem;
  color: var(--text-disabled-grey);
}

.resume__item--fait .resume__puce,
.resume__item--fait .resume__label {
  color: var(--text-action-high-blue-france);
}

.resume__item--en_cours .resume__puce,
.resume__item--en_cours .resume__label {
  color: var(--text-default-grey);
  font-weight: 600;
}

.resume__label {
  font-size: 0.8125rem;
  color: var(--text-disabled-grey);
  white-space: nowrap;
}

.resume__chevron {
  color: var(--text-disabled-grey);
  margin: 0 0.125rem;
}
</style>
