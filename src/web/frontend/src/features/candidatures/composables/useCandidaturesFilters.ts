import type { Ref } from 'vue'
import type {
  CandidatureListe,
  EtapeRecrutement,
  EtapeRecrutementDetailedCandidatures,
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

export interface CandidaturesSort {
  id: string
  desc: boolean
}

const SORT_KEYS: Record<string, (row: CandidatureListe) => string> = {
  date_soumission: row => row.date_soumission,
  derniere_activite: row => row.date_derniere_activite,
}

export type CandidaturesFiltersContext = ReturnType<typeof useCandidaturesFilters>

export interface CandidaturesFiltersSources {
  recrutementEtapes: Readonly<Ref<EtapeRecrutement[]>>
  candidatureKanban: Readonly<Ref<EtapeRecrutementDetailedCandidatures[]>>
  candidatures: Readonly<Ref<CandidatureListe[]>>
}

export function useCandidaturesFilters({
  recrutementEtapes,
  candidatureKanban,
  candidatures,
}: CandidaturesFiltersSources) {
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
    candidatureKanban.value
      .filter(etape => matchesEtape(etape.etape_uuid, applied))
      .map(etape => ({
        ...etape,
        candidatures: etape.candidatures.filter(
          candidature => matchesSearch(candidature.candidat, appliedSearch.value),
        ),
      })),
  )

  const sort = ref<CandidaturesSort | null>(null)

  const filteredCandidatures = computed(() => {
    const rows = candidatures.value.filter(row =>
      matchesEtape(row.etape.etape_uuid, applied)
      && matchesSearch(row.candidat, appliedSearch.value),
    )
    const key = sort.value && SORT_KEYS[sort.value.id]
    if (!key)
      return rows
    const direction = sort.value!.desc ? -1 : 1
    return [...rows].sort((a, b) => key(a).localeCompare(key(b)) * direction)
  })

  const etapeOptions = computed<CspCheckboxGroupOption[]>(() =>
    recrutementEtapes.value.map(etape => ({ value: etape.etape_uuid, label: etape.nom })),
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
    sort,
    filteredEtapes,
    filteredCandidatures,
    etapeOptions,
    activeFiltersCount,
  }
}
