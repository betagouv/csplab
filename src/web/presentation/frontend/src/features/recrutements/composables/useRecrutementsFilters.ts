import type { MaybeRefOrGetter } from 'vue'
import type { RecrutementBase } from '../types'
import { computed, toValue } from 'vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useDraft } from '@/composables/storage/useDraft'
import {
  responsableOptions as buildResponsableOptions,
  countActiveFilters,
  emptyRecrutementsFilters,
  matchesFilters,
  recrutementSearchableText,
  withAllOption,
} from '../utils/filters'

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

  const { search, filtered: searchedRows } = useTextSearch(rows, recrutementSearchableText)

  const filtered = computed(() =>
    searchedRows.value.filter(row => matchesFilters(row, applied)),
  )

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
