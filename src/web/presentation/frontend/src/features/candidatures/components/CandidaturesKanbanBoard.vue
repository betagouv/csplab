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
  gap: var(--csp-space-3);
  overflow-x: auto;
  padding-bottom: var(--csp-space-2);
}
</style>
