<script setup lang="ts">
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed } from 'vue'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
import { useCandidatures } from '../composables/useCandidatures'

const {
  recrutementUuid,
  moveCandidature,
  filters,
} = useCandidatures()

const { filteredEtapes } = filters

const boardId = computed(() => `kanban-${recrutementUuid}`)

function handleMove(event: KanbanDropEvent) {
  moveCandidature({
    sourceColumnId: event.sourceColumnId,
    targetColumnId: event.targetColumnId,
    cardId: event.cardId,
  })
}

const countLabel = computed(() => {
  const count = filteredEtapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0)
  return `${count} candidature${count > 1 ? 's' : ''}`
})
</script>

<template>
  <div class="candidatures-kanban-content">
    <p class="candidatures-kanban-content__count">
      {{ countLabel }}
    </p>
    <CandidaturesKanbanBoard
      :etapes="filteredEtapes"
      :board-id="boardId"
      @move="handleMove"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-kanban-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.candidatures-kanban-content__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}
</style>
