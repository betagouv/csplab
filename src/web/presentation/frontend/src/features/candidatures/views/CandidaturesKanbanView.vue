<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
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

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  { label: kanban.value?.intitule ?? 'Candidatures' },
])

const countLabel = computed(() => {
  const count = totalCount.value
  return `${count} candidature${count > 1 ? 's' : ''}`
})

const isNotFound = computed(() => !pending.value && (Boolean(error.value) || !kanban.value))
</script>

<template>
  <div class="candidatures-kanban-view">
    <CspPageHeader
      :title="kanban?.intitule ?? 'Candidatures'"
      :breadcrumb="breadcrumb"
      class="candidatures-kanban-view__header"
    />

    <div
      v-if="pending"
      class="candidatures-kanban-view__status"
    >
      Chargement des candidatures...
    </div>

    <div
      v-else-if="isNotFound"
      class="candidatures-kanban-view__status candidatures-kanban-view__status--error"
    >
      Recrutement introuvable.
    </div>

    <template v-else>
      <p class="candidatures-kanban-view__count">
        {{ countLabel }}
      </p>
      <CandidaturesKanbanBoard
        :etapes="etapes"
        :board-id="boardId"
        @move="handleMove"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.candidatures-kanban-view {
  padding: 2rem;
}

.candidatures-kanban-view__header {
  margin-bottom: var(--csp-space-4);
}

.candidatures-kanban-view__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.candidatures-kanban-view__status {
  padding: 1rem 0;
  color: var(--text-mention-grey);
}

.candidatures-kanban-view__status--error {
  color: var(--text-default-error);
}
</style>
