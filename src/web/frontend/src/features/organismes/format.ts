import type { Role } from './types'
import { ROLE_LABELS } from './constants/organisme'

export function formatAgentRole(role: Role): string {
  return ROLE_LABELS[role]
}
