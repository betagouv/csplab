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
  etapes,
  pending,
  moveCandidature,
  moveCandidaturesBatch,
  filters,
} = useCandidatures()

const { filteredEtapes } = filters

const showSkeleton = useMinimumPending(pending)

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

const sourceEtape = computed(() => {
  if (!currentEtapeUuid.value)
    return null
  return etapes.value.find(e => e.etape_uuid === currentEtapeUuid.value) ?? null
})

const selectedCandidatureUuids = computed(() => {
  if (!currentEtapeUuid.value)
    return new Set<string>()
  return selectedByEtape.value.get(currentEtapeUuid.value) ?? new Set<string>()
})

function handleMove(event: KanbanDropEvent) {
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
  isDrawerOpen.value = true
}

function handleRefuser(): void {
  isRefusDialogOpen.value = true
}

function handleConfirmRefus(): void {
  const refusEtape = etapes.value.find(e => e.categorie === 'REFUS')
  if (!refusEtape)
    return

  const candidaturesByEtape = new Map<string, string[]>()

  for (const [etapeUuid, uuids] of selectedByEtape.value) {
    candidaturesByEtape.set(etapeUuid, [...uuids])
  }

  moveCandidaturesBatch({
    candidaturesByEtape,
    targetColumnId: refusEtape.etape_uuid,
  })

  clearSelection()
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
  const n = selectedCount.value
  return `Vous êtes sur le point de refuser ${n} ${pluralize(n, 'candidature')}. `
    + `Cette action n'est pas définitive, néanmoins ${pluralize(n, 'le', 'les')} `
    + `${pluralize(n, 'candidat', 'candidats')} ${pluralize(n, 'sera', 'seront')} `
    + `${pluralize(n, 'informé', 'informés')} du changement de statut de `
    + `${pluralize(n, 'sa', 'leur')} candidature.`
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
      :etapes="etapes"
      @update:open="handleDrawerClose"
      @confirm="handleConfirmBatchMove"
      @toggle-candidature="handleToggleCandidature"
    />

    <CspDialog
      :open="isRefusDialogOpen"
      size="sm"
      title="Refus de candidature"
      :description="refusDescription"
      @update:open="isRefusDialogOpen = $event"
    >
      <template #footer>
        <div class="refus-dialog__footer">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="isRefusDialogOpen = false"
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
