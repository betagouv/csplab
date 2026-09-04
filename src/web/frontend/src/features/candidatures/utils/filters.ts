import type { Candidat } from '../types'
import { normalizeSearchText } from '@/utils/search'

export interface CandidaturesFilters extends Record<string, unknown> {
  etapes: string[]
}

export function emptyCandidaturesFilters(): CandidaturesFilters {
  return { etapes: [] }
}

export function matchesEtape(etapeUuid: string, filters: CandidaturesFilters): boolean {
  return filters.etapes.length === 0 || filters.etapes.includes(etapeUuid)
}

export function countActiveFilters(filters: CandidaturesFilters): number {
  return filters.etapes.length > 0 ? 1 : 0
}

export function matchesSearch(candidat: Candidat, search: string): boolean {
  const term = normalizeSearchText(search.trim())
  if (!term) {
    return true
  }
  return [
    `${candidat.prenom} ${candidat.nom}`,
    `${candidat.nom} ${candidat.prenom}`,
  ].some(name => normalizeSearchText(name).includes(term))
}
