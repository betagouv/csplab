import type { RecrutementActif, RecrutementArchive } from './types'
import { computed } from 'vue'
import { useDraft } from '@/composables/useDraft'
import {
  responsableOptions as buildResponsableOptions,
  countActiveFilters,
  emptyRecrutementsFilters,
  matchesFilters,
  withAllOption,
} from './utils/filters'

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
    reset,
  } = useDraft(emptyRecrutementsFilters)

  const filteredActifs = computed(() =>
    recrutements.actifs.filter(row => matchesFilters(row, applied)),
  )

  const filteredArchives = computed(() =>
    recrutements.archives.filter(row => matchesFilters(row, applied)),
  )

  const activeFiltersCount = computed(() => countActiveFilters(applied))

  const responsableOptions = computed(() =>
    withAllOption('Tous les responsables', buildResponsableOptions([
      ...recrutements.actifs,
      ...recrutements.archives,
    ])),
  )

  return {
    draft,
    applied,
    canReset,
    syncDraft,
    apply,
    reset,
    filteredActifs,
    filteredArchives,
    activeFiltersCount,
    responsableOptions,
  }
}
