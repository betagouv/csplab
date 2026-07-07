import type { RecrutementBase, TypeContrat } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { TYPE_CONTRAT_LABELS } from '../format'

export interface RecrutementsFilters extends Record<string, unknown> {
  responsable: string | null
  typeContrat: TypeContrat | null
}

export function emptyRecrutementsFilters(): RecrutementsFilters {
  return { responsable: null, typeContrat: null, kindContrat: null }
}

export function matchesFilters(row: RecrutementBase, filters: RecrutementsFilters): boolean {
  if (filters.responsable && !row.responsables.some(r => r.nom === filters.responsable)) {
    return false
  }
  if (filters.typeContrat && row.type_contrat !== filters.typeContrat) {
    return false
  }
  return true
}

export function countActiveFilters(filters: RecrutementsFilters): number {
  return Object.values(filters).filter(value => value !== null).length
}

export const FILTER_ALL = 'all'

export function withAllOption(label: string, options: CspSelectOption[]): CspSelectOption[] {
  return [{ value: FILTER_ALL, label }, ...options]
}

export function responsableOptions(rows: RecrutementBase[]): CspSelectOption[] {
  const noms = [...new Set(rows.flatMap(row => row.responsables.map(r => r.nom)))]
  return noms
    .sort((a, b) => a.localeCompare(b, 'fr'))
    .map(nom => ({ value: nom, label: nom }))
}

export const TYPE_CONTRAT_OPTIONS: CspSelectOption[] = Object
  .entries(TYPE_CONTRAT_LABELS)
  .map(([value, label]) => ({ value, label }))
