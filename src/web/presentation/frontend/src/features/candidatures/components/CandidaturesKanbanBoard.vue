<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { useKanbanBoardMonitor } from '@/composables/dnd/useKanbanDnd'
import CandidatureKanbanColumn from './CandidatureKanbanColumn.vue'

const props = defineProps<{
  etapes: EtapeRecrutementDetailedCandidatures[]
  boardId: string
}>()

const emit = defineEmits<{
  move: [event: KanbanDropEvent]
}>()

useKanbanBoardMonitor({
  boardId: props.boardId,
  onDrop: (event) => {
    if (event.sourceColumnId !== event.targetColumnId) {
      emit('move', event)
    }
  },
})
</script>

<template>
  <div class="candidatures-kanban-board">
    <CandidatureKanbanColumn
      v-for="etape in etapes"
      :key="etape.etape_uuid"
      :etape="etape"
      :board-id="boardId"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-kanban-board {
  display: flex;
  flex: 1;
  gap: var(--csp-space-3);
  overflow-x: auto;
  padding-bottom: var(--csp-space-2);
  min-height: 0;
}
</style>
