<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures, MotifRefus } from '../types'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { computed, nextTick, ref, toRef, watch } from 'vue'
import { useRoute } from 'vue-router'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { pluralize } from '@/utils/format'
import CandidaturesKanbanBoard from '../components/CandidaturesKanbanBoard.vue'
import ChangerEtapeDrawer from '../components/ChangerEtapeDrawer.vue'
import RefusCandidatureDialog from '../components/RefusCandidatureDialog.vue'
import SelectionActionBar from '../components/SelectionActionBar.vue'
import { useCandidatures } from '../composables/useCandidatures'
import { useKanbanSelection } from '../composables/useKanbanSelection'
import { useRefusCandidature } from '../composables/useRefusCandidature'

const {
  recrutementUuid,
  recrutementEtapes,
  candidatureKanban,
  pendingKanban,
  findCandidature,
  moveCandidature,
  moveCandidaturesBatch,
  filters,
} = useCandidatures()

const { filteredEtapes } = filters

const route = useRoute()

watch(() => route.params.candidatureUuid, async (current, previous) => {
  if (current || typeof previous !== 'string')
    return
  await nextTick()
  document.querySelector<HTMLElement>(`[data-candidature-uuid="${previous}"] a`)?.focus()
})

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
const drawerInitialEtapeUuid = ref<string | null>(null)
const refus = useRefusCandidature()

const refusEtapeUuid = computed(() => {
  return recrutementEtapes.value.find(e => e.categorie === 'REFUS')?.etape_uuid ?? null
})

const sourceEtape = computed(() => {
  if (!currentEtapeUuid.value)
    return null
  return candidatureKanban.value.find(e => e.etape_uuid === currentEtapeUuid.value) ?? null
})

const selectedCandidats = computed(() =>
  [...selectedByEtape.value.values()]
    .flatMap(uuids => [...uuids])
    .flatMap(uuid => findCandidature(uuid)?.candidat ?? []),
)

const selectedCandidatureUuids = computed(() => {
  if (!currentEtapeUuid.value)
    return new Set<string>()
  return selectedByEtape.value.get(currentEtapeUuid.value) ?? new Set<string>()
})

function handleMove(event: KanbanDropEvent) {
  const candidature = findCandidature(event.cardId)
  if (candidature && event.sourceColumnId !== event.targetColumnId && event.targetColumnId === refusEtapeUuid.value) {
    refus.request([candidature.candidat], motifRefus => void moveCandidature({ ...event, motifRefus }))
    return
  }

  void moveCandidature(event)
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

function handleConfirmBatchMove(targetEtapeUuid: string): void {
  if (targetEtapeUuid === refusEtapeUuid.value)
    refus.request(selectedCandidats.value, motifRefus => applyBatchMove(targetEtapeUuid, motifRefus))
  else
    applyBatchMove(targetEtapeUuid)
}

function applyBatchMove(targetEtapeUuid: string, motifRefus?: MotifRefus): void {
  const candidaturesByEtape = new Map<string, string[]>()

  for (const [etapeUuid, uuids] of selectedByEtape.value) {
    candidaturesByEtape.set(etapeUuid, [...uuids])
  }

  moveCandidaturesBatch({
    candidaturesByEtape,
    targetColumnId: targetEtapeUuid,
    motifRefus,
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
      :open="isDrawerOpen && !refus.isOpen.value"
      :source-etape="sourceEtape"
      :selected-candidature-uuids="selectedCandidatureUuids"
      :etapes="recrutementEtapes"
      :initial-etape-uuid="drawerInitialEtapeUuid"
      @update:open="handleDrawerClose"
      @confirm="handleConfirmBatchMove"
      @toggle-candidature="handleToggleCandidature"
    />

    <RefusCandidatureDialog
      :open="refus.isOpen.value"
      :candidats="refus.candidats.value"
      :motifs="refus.motifs.value"
      :motifs-unavailable="refus.motifsUnavailable.value"
      @confirm="refus.confirm"
      @cancel="refus.cancel"
    />
  </div>

  <router-view />
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
</style>
