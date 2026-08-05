import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementBase } from '../types'
import { computed, ref, toValue } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { useDraft } from '@/composables/storage/useDraft'
import {
  responsableOptions as buildResponsableOptions,
  countActiveFilters,
  emptyRecrutementsFilters,
  matchesFilters,
  matchesSearch,
  withAllOption,
} from '../utils/filters'

const SEARCH_DEBOUNCE_MS = 250

export function useRecrutementsFilters<T extends RecrutementBase>(
  rows: MaybeRefOrGetter<T[]>,
) {
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

  function matches(row: T): boolean {
    return matchesFilters(row, applied) && matchesSearch(row, debouncedSearch.value)
  }

  const filtered = computed(() => toValue(rows).filter(matches))

  const activeFiltersCount = computed(() => countActiveFilters(applied))

  const responsableOptions = computed(() =>
    withAllOption('Tous les responsables', buildResponsableOptions(toValue(rows))),
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
    filtered,
    activeFiltersCount,
    responsableOptions,
  }
}
