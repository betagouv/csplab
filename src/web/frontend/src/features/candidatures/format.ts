import type { CandidatureListe } from './types'

export function formatCandidatName(candidat: CandidatureListe['candidat']): string {
  return `${candidat.prenom} ${candidat.nom}`
}
