<script setup lang="ts">
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
import CandidaturesLayout from '../components/CandidaturesLayout.vue'
import { useCandidaturesKanban } from '../composables/useCandidaturesKanban'

const route = useRoute()
const recrutementUuid = computed(() => String(route.params.recrutementUuid))

const {
  kanban,
  etapes,
  totalCount,
  pending,
  error,
  load,
  moveCandidature,
} = useCandidaturesKanban(TEMP_ORGANISME_UUID, recrutementUuid)

const boardId = computed(() => `kanban-${recrutementUuid.value}`)

function handleMove(event: KanbanDropEvent) {
  moveCandidature({
    sourceColumnId: event.sourceColumnId,
    targetColumnId: event.targetColumnId,
    cardId: event.cardId,
  })
}

onMounted(() => {
  void load()
})

watch(recrutementUuid, () => {
  void load()
})

const countLabel = computed(() => {
  const count = totalCount.value
  return `${count} candidature${count > 1 ? 's' : ''}`
})
</script>

<template>
  <CandidaturesLayout
    :recrutement-uuid="recrutementUuid"
    :recrutement-detail="kanban"
    current-view="kanban"
    :pending="pending"
    :error="error"
  >
    <p class="candidatures-kanban-view__count">
      {{ countLabel }}
    </p>
    <CandidaturesKanbanBoard
      :etapes="etapes"
      :board-id="boardId"
      @move="handleMove"
    />
  </CandidaturesLayout>
</template>

<style scoped lang="scss">
.candidatures-kanban-view__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}
</style>
