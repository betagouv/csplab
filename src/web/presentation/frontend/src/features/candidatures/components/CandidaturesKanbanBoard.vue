<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import CandidatureKanbanColumn from './CandidatureKanbanColumn.vue'

defineProps<{
  etapes: EtapeRecrutementDetailedCandidatures[]
}>()
</script>

<template>
  <div class="candidatures-kanban-board">
    <CandidatureKanbanColumn
      v-for="etape in etapes"
      :key="etape.etape_uuid"
      :etape="etape"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-kanban-board {
  display: flex;
  gap: var(--csp-space-4);
  overflow-x: auto;
  padding: var(--csp-space-4);
  background-color: var(--background-alt-grey);
  border-radius: 0.25rem;
}
</style>
