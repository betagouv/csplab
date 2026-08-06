<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed, ref, toRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { pluralize } from '@/utils/format'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
import ChangerEtapeDrawer from '../components/ChangerEtapeDrawer.vue'
import SelectionActionBar from '../components/SelectionActionBar.vue'
import { useCandidatures } from '../composables/useCandidatures'
import { useKanbanSelection } from '../composables/useKanbanSelection'

const {
  recrutementUuid,
  recrutementEtapes,
  candidatureKanban,
  pendingKanban,
  moveCandidature,
  moveCandidaturesBatch,
  filters,
} = useCandidatures()

const { filteredEtapes } = filters

const showSkeleton = useMinimumPending(pendingKanban)

const {
  selectedByEtape,
  selectedCount,
  currentEtapeUuid,
  isColumnSelected,
  toggleColumnSelection,
  toggleCandidatureSelection,
  clearSelection,
  hasSelection,
} = useKanbanSelection(toRef(() => filteredEtapes.value))

const boardId = computed(() => `kanban-${recrutementUuid.value}`)
const isDrawerOpen = ref(false)
const isRefusDialogOpen = ref(false)
const drawerInitialEtapeUuid = ref<string | null>(null)
const pendingMove = ref<KanbanDropEvent | null>(null)

const refusEtapeUuid = computed(() => {
  return recrutementEtapes.value.find(e => e.categorie === 'REFUS')?.etape_uuid ?? null
})

const pendingCandidature = computed(() => {
  const move = pendingMove.value
  if (!move)
    return null

  const etape = candidatureKanban.value.find(e => e.etape_uuid === move.sourceColumnId)
  return etape?.candidatures.find(c => c.uuid === move.cardId) ?? null
})

const sourceEtape = computed(() => {
  if (!currentEtapeUuid.value)
    return null
  return candidatureKanban.value.find(e => e.etape_uuid === currentEtapeUuid.value) ?? null
})

const selectedCandidatureUuids = computed(() => {
  if (!currentEtapeUuid.value)
    return new Set<string>()
  return selectedByEtape.value.get(currentEtapeUuid.value) ?? new Set<string>()
})

function handleMove(event: KanbanDropEvent) {
  if (event.sourceColumnId !== event.targetColumnId && event.targetColumnId === refusEtapeUuid.value) {
    pendingMove.value = event
    isRefusDialogOpen.value = true
    return
  }

  moveCandidature({
    sourceColumnId: event.sourceColumnId,
    targetColumnId: event.targetColumnId,
    cardId: event.cardId,
  })
}

function handleToggleColumnSelection(etape: EtapeRecrutementDetailedCandidatures): void {
  toggleColumnSelection(etape)
}

function handleOpenChangerEtape(): void {
  drawerInitialEtapeUuid.value = null
  isDrawerOpen.value = true
}

function handleRefuser(): void {
  drawerInitialEtapeUuid.value = refusEtapeUuid.value
  isDrawerOpen.value = true
}

function handleConfirmRefus(): void {
  if (!pendingMove.value)
    return

  moveCandidature({
    sourceColumnId: pendingMove.value.sourceColumnId,
    targetColumnId: pendingMove.value.targetColumnId,
    cardId: pendingMove.value.cardId,
  })

  pendingMove.value = null
  isRefusDialogOpen.value = false
}

function handleCancelRefus(): void {
  pendingMove.value = null
  isRefusDialogOpen.value = false
}

function handleConfirmBatchMove(targetEtapeUuid: string): void {
  const candidaturesByEtape = new Map<string, string[]>()

  for (const [etapeUuid, uuids] of selectedByEtape.value) {
    candidaturesByEtape.set(etapeUuid, [...uuids])
  }

  moveCandidaturesBatch({
    candidaturesByEtape,
    targetColumnId: targetEtapeUuid,
  })

  clearSelection()
  isDrawerOpen.value = false
}

function handleDrawerClose(open: boolean): void {
  isDrawerOpen.value = open
}

function handleToggleCandidature(candidatureUuid: string, etapeUuid: string): void {
  toggleCandidatureSelection(candidatureUuid, etapeUuid)
}

const countLabel = computed(() => {
  const count = filteredEtapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0)
  return `${count} ${pluralize(count, 'candidature')}`
})

const refusDescription = computed(() => {
  const candidature = pendingCandidature.value
  const candidatLabel = candidature
    ? `${candidature.candidat.prenom} ${candidature.candidat.nom}`
    : 'ce candidat'

  return `Vous êtes sur le point de refuser la candidature de ${candidatLabel}. `
    + `Cette action n'est pas définitive, néanmoins le candidat sera informé du changement `
    + `de statut de sa candidature.`
})
</script>

<template>
  <div
    v-if="showSkeleton"
    class="candidatures-kanban-content"
    role="status"
    aria-label="Chargement des candidatures"
  >
    <CspSkeleton
      class="candidatures-kanban-content__count-skeleton"
      width="8rem"
      height="0.9375rem"
    />
    <CspSkeletonKanban />
  </div>

  <div
    v-else
    class="candidatures-kanban-content"
  >
    <p
      v-if="!hasSelection"
      class="candidatures-kanban-content__count"
    >
      {{ countLabel }}
    </p>
    <SelectionActionBar
      v-else
      :selected-count="selectedCount"
      @changer-etape="handleOpenChangerEtape"
      @refuser="handleRefuser"
    />
    <CandidaturesKanbanBoard
      :etapes="filteredEtapes"
      :board-id="boardId"
      :is-column-selected="isColumnSelected"
      @move="handleMove"
      @toggle-column-selection="handleToggleColumnSelection"
    />

    <ChangerEtapeDrawer
      :open="isDrawerOpen"
      :source-etape="sourceEtape"
      :selected-candidature-uuids="selectedCandidatureUuids"
      :etapes="recrutementEtapes"
      :initial-etape-uuid="drawerInitialEtapeUuid"
      @update:open="handleDrawerClose"
      @confirm="handleConfirmBatchMove"
      @toggle-candidature="handleToggleCandidature"
    />

    <CspDialog
      :open="isRefusDialogOpen"
      size="sm"
      title="Refus de candidature"
      @update:open="(open) => { if (!open) handleCancelRefus() }"
    >
      {{ refusDescription }}

      <template #footer>
        <div class="refus-dialog__footer">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="handleCancelRefus"
          />
          <CspButton
            label="Valider"
            variant="primary"
            @click="handleConfirmRefus"
          />
        </div>
      </template>
    </CspDialog>
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

.candidatures-kanban-content__count-skeleton {
  margin: var(--csp-space-1) 0 calc(var(--csp-space-4) + 0.15rem);
}

.refus-dialog__footer {
  display: flex;
  gap: var(--csp-space-3);
}
</style>
