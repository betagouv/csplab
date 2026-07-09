<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import CandidatureKanbanCard from './CandidatureKanbanCard.vue'

defineProps<{
  etape: EtapeRecrutementDetailedCandidatures
}>()
</script>

<template>
  <section class="candidature-kanban-column">
    <header class="candidature-kanban-column__header">
      <h2 class="candidature-kanban-column__title">
        {{ etape.nom }}
        <span class="candidature-kanban-column__count">{{ etape.candidatures.length }}</span>
      </h2>
    </header>
    <ul class="candidature-kanban-column__cards">
      <li
        v-for="candidature in etape.candidatures"
        :key="candidature.uuid"
        class="candidature-kanban-column__card-item"
      >
        <CandidatureKanbanCard :candidature="candidature" />
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
.candidature-kanban-column {
  display: flex;
  flex-direction: column;
  flex: 0 0 18.75rem;
  min-width: 18.75rem;
  gap: var(--csp-space-3);
}

.candidature-kanban-column__header {
  padding: 0 var(--csp-space-1);
}

.candidature-kanban-column__title {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text-title-grey);
}

.candidature-kanban-column__count {
  font-weight: 700;
}

.candidature-kanban-column__cards {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.candidature-kanban-column__card-item {
  margin: 0;
}
</style>
