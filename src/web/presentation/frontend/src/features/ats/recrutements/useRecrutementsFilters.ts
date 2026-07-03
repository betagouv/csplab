import type { RecrutementActif, RecrutementArchive } from './types'
import { computed, ref } from 'vue'
import { useDebounce } from '@/composables/useDebounce'
import { useDraft } from '@/composables/useDraft'
import {
  responsableOptions as buildResponsableOptions,
  countActiveFilters,
  emptyRecrutementsFilters,
  matchesFilters,
  matchesSearch,
  withAllOption,
} from './utils/filters'

const SEARCH_DEBOUNCE_MS = 250

export function useRecrutementsFilters(recrutements: {
  actifs: RecrutementActif[]
  archives: RecrutementArchive[]
}) {
  const {
    draft,
    applied,
    canReset,
    syncDraft,
    apply,
    reset: resetDraft,
  } = useDraft(emptyRecrutementsFilters)

  const search = ref('')
  const debouncedSearch = useDebounce(search, SEARCH_DEBOUNCE_MS)

  function matches(row: RecrutementActif | RecrutementArchive): boolean {
    return matchesFilters(row, applied) && matchesSearch(row, debouncedSearch.value)
  }

  const filteredActifs = computed(() => recrutements.actifs.filter(matches))
  const filteredArchives = computed(() => recrutements.archives.filter(matches))

  const activeFiltersCount = computed(() => countActiveFilters(applied))

  const responsableOptions = computed(() =>
    withAllOption('Tous les responsables', buildResponsableOptions([
      ...recrutements.actifs,
      ...recrutements.archives,
    ])),
  )

  function reset(): void {
    resetDraft()
    search.value = ''
  }

  return {
    draft,
    applied,
    canReset,
    syncDraft,
    apply,
    reset,
    search,
    filteredActifs,
    filteredArchives,
    activeFiltersCount,
    responsableOptions,
  }
}
