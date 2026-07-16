import type { Ref, ShallowRef } from 'vue'
import type {
  EtapeRecrutementDetailedCandidatures,
  PaginatedCandidatureListeList,
} from '../types'
import type { CspCheckboxGroupOption } from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import { computed, ref, watch } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { useDraft } from '@/composables/storage/useDraft'
import {
  countActiveFilters,
  emptyCandidaturesFilters,
  matchesEtape,
  matchesSearch,
} from '../utils/filters'

const SEARCH_DEBOUNCE_MS = 500

export type CandidaturesFiltersContext = ReturnType<typeof useCandidaturesFilters>

export function useCandidaturesFilters(
  etapes: ShallowRef<EtapeRecrutementDetailedCandidatures[]>,
  candidatureListe: Ref<PaginatedCandidatureListeList | undefined>,
) {
  const {
    draft,
    applied,
    canReset,
    syncDraft,
    apply,
    reset: resetDraft,
  } = useDraft(emptyCandidaturesFilters)

  const search = ref('')
  const appliedSearch = ref('')
  const debouncedSearch = useDebounce(search, SEARCH_DEBOUNCE_MS)

  watch(debouncedSearch, (value) => {
    appliedSearch.value = value
  })

  function flushSearch(): void {
    appliedSearch.value = search.value
  }

  const filteredEtapes = computed(() =>
    etapes.value
      .filter(etape => matchesEtape(etape.etape_uuid, applied))
      .map(etape => ({
        ...etape,
        candidatures: etape.candidatures.filter(
          candidature => matchesSearch(candidature.candidat, appliedSearch.value),
        ),
      })),
  )

  const filteredCandidatures = computed(() =>
    (candidatureListe.value?.results ?? []).filter(row =>
      matchesEtape(row.etape.etape_uuid, applied)
      && matchesSearch(row.candidat, appliedSearch.value),
    ),
  )

  const etapeOptions = computed<CspCheckboxGroupOption[]>(() =>
    etapes.value.map(etape => ({ value: etape.etape_uuid, label: etape.nom })),
  )

  const activeFiltersCount = computed(() => countActiveFilters(applied))

  function reset(): void {
    resetDraft()
    search.value = ''
    appliedSearch.value = ''
  }

  return {
    draft,
    canReset,
    syncDraft,
    apply,
    reset,
    search,
    flushSearch,
    filteredEtapes,
    filteredCandidatures,
    etapeOptions,
    activeFiltersCount,
  }
}
