import type { InjectionKey, MaybeRefOrGetter } from 'vue'
import type {
  CandidatureListe,
  EtapeRecrutement,
  EtapeRecrutementDetailedCandidatures,
} from '../types'
import type { CspCheckboxGroupOption } from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import type { CspTableSort } from '@/components/base/CspDataTable/table'
import { computed, inject, provide, ref, toValue, watch } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { useDraft } from '@/composables/storage/useDraft'
import {
  countActiveFilters,
  emptyCandidaturesFilters,
  matchesEtape,
  matchesSearch,
} from '../utils/filters'

const SEARCH_DEBOUNCE_MS = 500

export type CandidaturesFiltersContext = ReturnType<typeof createCandidaturesFilters>

const KEY: InjectionKey<CandidaturesFiltersContext> = Symbol('candidatures-filters')

export function createCandidaturesFilters(recrutementEtapes: MaybeRefOrGetter<EtapeRecrutement[]>) {
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

  function filterEtapes(etapes: EtapeRecrutementDetailedCandidatures[]): EtapeRecrutementDetailedCandidatures[] {
    return etapes
      .filter(etape => matchesEtape(etape.uuid, applied))
      .map(etape => ({
        ...etape,
        candidatures: etape.candidatures.filter(
          candidature => matchesSearch(candidature.candidat, appliedSearch.value),
        ),
      }))
  }

  function filterCandidatures(rows: CandidatureListe[]): CandidatureListe[] {
    return rows.filter(row =>
      matchesEtape(row.etape.uuid, applied)
      && matchesSearch(row.candidat, appliedSearch.value),
    )
  }

  const etapeOptions = computed<CspCheckboxGroupOption[]>(() =>
    toValue(recrutementEtapes).map(etape => ({ value: etape.uuid, label: etape.nom })),
  )

  const activeFiltersCount = computed(() => countActiveFilters(applied))

  const listeSort = ref<CspTableSort | null>(null)

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
    filterEtapes,
    filterCandidatures,
    etapeOptions,
    activeFiltersCount,
    listeSort,
  }
}

export function provideCandidaturesFilters(recrutementEtapes: MaybeRefOrGetter<EtapeRecrutement[]>): CandidaturesFiltersContext {
  const filters = createCandidaturesFilters(recrutementEtapes)
  provide(KEY, filters)
  return filters
}

export function useCandidaturesFilters(): CandidaturesFiltersContext {
  const filters = inject(KEY)
  if (!filters) {
    throw new Error('useCandidaturesFilters must be used within provideCandidaturesFilters')
  }
  return filters
}
