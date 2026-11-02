import type { RecrutementRole } from './types'
import { RECRUTEMENT_ROLE_LABELS } from './constants/equipe-recrutement'

export function formatRecrutementRole(role: RecrutementRole): string {
  return RECRUTEMENT_ROLE_LABELS[role] ?? role
}
