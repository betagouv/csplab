import type { Ref, WritableComputedRef } from 'vue'
import type { NatureOffre, RecrutementBase } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { computed } from 'vue'
import { labelOptions } from '@/utils/options'
import { NATURE_OFFRE_LABELS } from '../format'

export interface RecrutementsFilters extends Record<string, unknown> {
  responsable: string | null
  natureOffre: NatureOffre | null
}

export function emptyRecrutementsFilters(): RecrutementsFilters {
  return { responsable: null, natureOffre: null }
}

export function matchesFilters(row: RecrutementBase, filters: RecrutementsFilters): boolean {
  if (filters.responsable && !row.responsables.some(r => r.nom === filters.responsable)) {
    return false
  }
  if (filters.natureOffre && row.nature_offre !== filters.natureOffre) {
    return false
  }
  return true
}

export function countActiveFilters(filters: RecrutementsFilters): number {
  return Object.values(filters).filter(value => value !== null).length
}

export function recrutementSearchableText(row: RecrutementBase): Array<string | null> {
  const recrute = 'recrute' in row ? (row as { recrute: string | null }).recrute : null
  return [
    row.intitule,
    row.reference_csp,
    ...row.responsables.map(r => r.nom),
    recrute,
  ]
}

export const FILTER_ALL = 'all'

export function withAllOption<T extends string>(label: string, options: CspSelectOption<T>[]): CspSelectOption<T | typeof FILTER_ALL>[] {
  return [{ value: FILTER_ALL, label }, ...options]
}

export function selectModel<T extends string>(model: Ref<T | null>): WritableComputedRef<T | typeof FILTER_ALL> {
  return computed({
    get: () => model.value ?? FILTER_ALL,
    set: (value) => {
      model.value = value === FILTER_ALL ? null : value
    },
  })
}

export function responsableOptions(rows: RecrutementBase[]): CspSelectOption[] {
  const noms = [...new Set(rows.flatMap(row => row.responsables.map(r => r.nom)))]
  return noms
    .sort((a, b) => a.localeCompare(b, 'fr'))
    .map(nom => ({ value: nom, label: nom }))
}

export const NATURE_OFFRE_OPTIONS: CspSelectOption<NatureOffre>[] = labelOptions(NATURE_OFFRE_LABELS)
