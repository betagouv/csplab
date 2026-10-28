<script setup lang="ts">
import type { MotifRefus } from '../types'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { useQuery } from '@pinia/colada'
import { computed, ref, toRef } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { pluralize } from '@/utils/format'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
import ChangerEtapeDrawer from '../components/ChangerEtapeDrawer.vue'
import RefusCandidatureDialog from '../components/RefusCandidatureDialog.vue'
import { useCandidatureLinkFocus } from '../composables/useCandidatureLinkFocus'
import { provideCandidatureSequence } from '../composables/useCandidatureNavigation'
import { useCandidaturesFilters } from '../composables/useCandidaturesFilters'
import { publishCandidaturesToolbar } from '../composables/useCandidaturesToolbar'
import { useEtapeChangeMutation } from '../composables/useEtapeChangeMutation'
import { useKanbanSelection } from '../composables/useKanbanSelection'
import { useRefusCandidature } from '../composables/useRefusCandidature'
import { recrutementKanbanQuery } from '../queries'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const kanban = useQuery(() => recrutementKanbanQuery(props))
const candidatureKanban = computed(() => kanban.data.value?.etapes ?? [])

const { etapes: recrutementEtapes } = useRecrutementDetail(() => props)

const { changeEtape } = useEtapeChangeMutation(() => props)

const filters = useCandidaturesFilters()
const filteredEtapes = computed(() => filters.filterEtapes(candidatureKanban.value))

function findCandidature(uuid: string) {
  for (const etape of candidatureKanban.value) {
    const found = etape.candidatures.find(candidature => candidature.uuid === uuid)
    if (found) {
      return found
    }
  }
  return null
}

provideCandidatureSequence(candidatureUuid =>
  filteredEtapes.value
    .find(etape => etape.candidatures.some(({ uuid }) => uuid === candidatureUuid))
    ?.candidatures
    .map(({ uuid }) => uuid) ?? [])

useCandidatureLinkFocus()

const showSkeleton = useMinimumPending(kanban.isPending)

const {
  selectedCandidatures,
  selectedCount,
  currentEtapeUuid,
  isColumnSelected,
  toggleColumnSelection,
  toggleCandidatureSelection,
  clearSelection,
} = useKanbanSelection(toRef(() => filteredEtapes.value))

const boardId = computed(() => `kanban-${props.recrutementUuid}`)
const isDrawerOpen = ref(false)
const drawerInitialEtapeUuid = ref<string | null>(null)
const refus = useRefusCandidature(() => props.organismeUuid, recrutementEtapes)

const refusEtapeUuid = computed(() => {
  return recrutementEtapes.value.find(e => e.categorie === 'REFUS')?.uuid ?? null
})

const sourceEtape = computed(() => {
  if (!currentEtapeUuid.value) {
    return null
  }
  return filteredEtapes.value.find(e => e.uuid === currentEtapeUuid.value) ?? null
})

const selectedCandidats = computed(() =>
  selectedCandidatures.value.map(({ candidature }) => candidature.candidat),
)

const selectedCandidatureUuids = computed(() =>
  new Set(selectedCandidatures.value.map(({ candidature }) => candidature.uuid)),
)

function handleMove({ sourceColumnId, targetColumnId, cardId }: KanbanDropEvent) {
  if (sourceColumnId === targetColumnId) {
    return
  }

  const candidature = findCandidature(cardId)
  if (!candidature) {
    return
  }
  refus.moveOrAskRejectionReason(
    targetColumnId,
    [candidature.candidat],
    motifRefus => void changeEtape({ etapeCibleUuid: targetColumnId, candidatureUuids: [cardId], motifRefus }),
  )
}

function handleOpenChangerEtape(): void {
  drawerInitialEtapeUuid.value = null
  isDrawerOpen.value = true
}

function handleRefuser(): void {
  drawerInitialEtapeUuid.value = refusEtapeUuid.value
  isDrawerOpen.value = true
}

function handleConfirmBatchMove(targetEtapeUuid: string): void {
  refus.moveOrAskRejectionReason(
    targetEtapeUuid,
    selectedCandidats.value,
    motifRefus => applyBatchMove(targetEtapeUuid, motifRefus),
  )
}

function applyBatchMove(targetEtapeUuid: string, motifRefus?: MotifRefus): void {
  const candidatureUuids = [...selectedCandidatureUuids.value]
  if (candidatureUuids.length > 0) {
    void changeEtape({ etapeCibleUuid: targetEtapeUuid, candidatureUuids, motifRefus })
  }

  clearSelection()
  isDrawerOpen.value = false
}

const countLabel = computed(() => {
  const count = filteredEtapes.value.reduce((sum, etape) => sum + etape.candidatures.length, 0)
  return `${count} ${pluralize(count, 'candidature')}`
})

const selectionLabel = computed(() =>
  `${selectedCount.value} ${pluralize(selectedCount.value, 'candidat')} ${pluralize(selectedCount.value, 'sélectionné')}`,
)

publishCandidaturesToolbar(() => ({
  count: kanban.error.value ? '' : countLabel.value,
  pending: showSkeleton.value,
  selectionCount: selectedCount.value,
  selectionLabel: selectionLabel.value,
  selectionActions: [
    { label: 'Changer d\'étape', icon: 'ri:arrow-left-right-line', onClick: handleOpenChangerEtape },
    { label: 'Refuser', icon: 'ri:close-line', onClick: handleRefuser },
  ],
}))
</script>

<template>
  <CspAsyncSection
    fill
    :pending="showSkeleton"
    :error="kanban.error.value"
    loading-label="Chargement des candidatures"
    error-title="Une erreur est survenue lors du chargement des candidatures."
  >
    <template #skeleton>
      <CspSkeletonKanban />
    </template>

    <CandidaturesKanbanBoard
      :etapes="filteredEtapes"
      :board-id="boardId"
      :is-column-selected="isColumnSelected"
      @move="handleMove"
      @toggle-column-selection="toggleColumnSelection"
    />

    <ChangerEtapeDrawer
      :open="isDrawerOpen && !refus.isOpen.value"
      :source-etape="sourceEtape"
      :selected-candidature-uuids="selectedCandidatureUuids"
      :etapes="recrutementEtapes"
      :initial-etape-uuid="drawerInitialEtapeUuid"
      @update:open="isDrawerOpen = $event"
      @confirm="handleConfirmBatchMove"
      @toggle-candidature="toggleCandidatureSelection"
    />

    <RefusCandidatureDialog
      :open="refus.isOpen.value"
      :candidats="refus.candidats.value"
      :motifs="refus.motifs.value"
      :motifs-unavailable="refus.motifsUnavailable.value"
      @confirm="refus.confirm"
      @cancel="refus.cancel"
    />
  </CspAsyncSection>

  <router-view />
</template>
