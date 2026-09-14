import type { MembreEquipe, RecrutementRole } from './types'
import { RECRUTEMENT_ROLE_LABELS } from './constants/equipe-recrutement'

export function formatMembreNameAlphabetical(membre: MembreEquipe): string {
  return `${membre.nom} ${membre.prenom}`.trim()
}

export function formatRecrutementRole(role: RecrutementRole): string {
  return RECRUTEMENT_ROLE_LABELS[role] ?? role
}
