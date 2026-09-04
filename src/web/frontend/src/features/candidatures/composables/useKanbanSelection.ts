import type { ComputedRef, Ref } from 'vue'
import type { Candidature, EtapeRecrutementDetailedCandidatures } from '../types'
import { computed, ref } from 'vue'

export interface SelectedCandidature {
  candidature: Candidature
  etapeUuid: string
}

export interface KanbanSelectionContext {
  selectedByEtape: Ref<Map<string, Set<string>>>
  selectedCandidatures: ComputedRef<SelectedCandidature[]>
  selectedCount: ComputedRef<number>
  currentEtapeUuid: ComputedRef<string | null>
  isColumnSelected: (etapeUuid: string) => boolean
  toggleColumnSelection: (etape: EtapeRecrutementDetailedCandidatures) => void
  toggleCandidatureSelection: (candidatureUuid: string, etapeUuid: string) => void
  clearSelection: () => void
  hasSelection: ComputedRef<boolean>
}

export function useKanbanSelection(
  etapes: Ref<EtapeRecrutementDetailedCandidatures[]>,
): KanbanSelectionContext {
  const selectedByEtape = ref<Map<string, Set<string>>>(new Map())

  const selectedCandidatures = computed<SelectedCandidature[]>(() => {
    const result: SelectedCandidature[] = []

    for (const [etapeUuid, candidatureUuids] of selectedByEtape.value) {
      const etape = etapes.value.find(e => e.etape_uuid === etapeUuid)
      if (!etape)
        continue

      for (const uuid of candidatureUuids) {
        const candidature = etape.candidatures.find(c => c.uuid === uuid)
        if (candidature) {
          result.push({ candidature, etapeUuid })
        }
      }
    }

    return result
  })

  const selectedCount = computed(() => selectedCandidatures.value.length)

  const hasSelection = computed(() => selectedCount.value > 0)

  const currentEtapeUuid = computed<string | null>(() => {
    const etapeUuids = new Set(selectedCandidatures.value.map(s => s.etapeUuid))
    if (etapeUuids.size === 1) {
      return [...etapeUuids][0] ?? null
    }
    return null
  })

  function isColumnSelected(etapeUuid: string): boolean {
    const selected = selectedByEtape.value.get(etapeUuid)
    if (!selected || selected.size === 0)
      return false

    const etape = etapes.value.find(e => e.etape_uuid === etapeUuid)
    if (!etape)
      return false

    return selected.size === etape.candidatures.length && etape.candidatures.length > 0
  }

  function toggleColumnSelection(etape: EtapeRecrutementDetailedCandidatures): void {
    const etapeUuid = etape.etape_uuid
    const currentSelection = selectedByEtape.value.get(etapeUuid)
    const isCurrentlySelected = currentSelection && currentSelection.size === etape.candidatures.length

    const newMap = new Map(selectedByEtape.value)

    if (isCurrentlySelected) {
      newMap.delete(etapeUuid)
    }
    else {
      const newSet = new Set(etape.candidatures.map(c => c.uuid))
      newMap.set(etapeUuid, newSet)
    }

    selectedByEtape.value = newMap
  }

  function toggleCandidatureSelection(candidatureUuid: string, etapeUuid: string): void {
    const newMap = new Map(selectedByEtape.value)
    const currentSet = newMap.get(etapeUuid)

    if (currentSet) {
      const newSet = new Set(currentSet)
      if (newSet.has(candidatureUuid)) {
        newSet.delete(candidatureUuid)
        if (newSet.size === 0) {
          newMap.delete(etapeUuid)
        }
        else {
          newMap.set(etapeUuid, newSet)
        }
      }
      else {
        newSet.add(candidatureUuid)
        newMap.set(etapeUuid, newSet)
      }
    }
    else {
      newMap.set(etapeUuid, new Set([candidatureUuid]))
    }

    selectedByEtape.value = newMap
  }

  function clearSelection(): void {
    selectedByEtape.value = new Map()
  }

  return {
    selectedByEtape,
    selectedCandidatures,
    selectedCount,
    currentEtapeUuid,
    isColumnSelected,
    toggleColumnSelection,
    toggleCandidatureSelection,
    clearSelection,
    hasSelection,
  }
}
