import type { Candidat } from '../types'

export function formatCandidatNom(candidat: Candidat): string {
  return `${candidat.prenom} ${candidat.nom}`.trim()
}
