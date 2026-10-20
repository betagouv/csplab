<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { ref, watch } from 'vue'
import { useKanbanBoardAutoScroll, useKanbanBoardMonitor } from '@/composables/dnd/useKanbanDnd'
import { etapesReceivingCandidatures } from '../utils/kanban'
import CandidatureKanbanColumn from './CandidatureKanbanColumn.vue'

const props = defineProps<{
  etapes: EtapeRecrutementDetailedCandidatures[]
  boardId: string
  isColumnSelected: (etapeUuid: string) => boolean
}>()

const emit = defineEmits<{
  move: [event: KanbanDropEvent]
  toggleColumnSelection: [etape: EtapeRecrutementDetailedCandidatures]
}>()

const boardRef = ref<HTMLElement | null>(null)

useKanbanBoardMonitor({
  boardId: props.boardId,
  onDrop: (event) => {
    if (event.sourceColumnId !== event.targetColumnId) {
      emit('move', event)
    }
  },
})

useKanbanBoardAutoScroll({ element: boardRef })

const columns = new Map<string, InstanceType<typeof CandidatureKanbanColumn>>()

function setColumn(etapeUuid: string, column: unknown): void {
  if (column) {
    columns.set(etapeUuid, column as InstanceType<typeof CandidatureKanbanColumn>)
  }
  else {
    columns.delete(etapeUuid)
  }
}

watch(() => props.etapes, (etapes, previousEtapes) => {
  for (const etapeUuid of etapesReceivingCandidatures(previousEtapes, etapes)) {
    columns.get(etapeUuid)?.scrollToEnd()
  }
}, { flush: 'post' })
</script>

<template>
  <div
    ref="boardRef"
    class="candidatures-kanban-board"
  >
    <CandidatureKanbanColumn
      v-for="etape in etapes"
      :key="etape.uuid"
      :ref="column => setColumn(etape.uuid, column)"
      :etape="etape"
      :board-id="boardId"
      :is-selected="isColumnSelected(etape.uuid)"
      @toggle-selection="emit('toggleColumnSelection', $event)"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-kanban-board {
  --candidatures-kanban-board-inset: calc(var(--csp-kanban-scroll-to-edge) * var(--csp-page-container-padding-inline));

  display: flex;
  flex: 1;
  gap: var(--csp-kanban-gap);
  overflow-x: auto;
  margin-inline: calc(-1 * var(--candidatures-kanban-board-inset))
    calc(-1 * (var(--candidatures-kanban-board-inset) + var(--csp-kanban-bleed-inline-end)));
  padding-inline: var(--candidatures-kanban-board-inset)
    calc(var(--candidatures-kanban-board-inset) + var(--csp-kanban-bleed-inline-end));
  scroll-padding-inline: var(--candidatures-kanban-board-inset);
  padding-bottom: var(--csp-kanban-padding-bottom);
  min-height: 0;
}
</style>
