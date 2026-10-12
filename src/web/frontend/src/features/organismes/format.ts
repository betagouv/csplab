import { ROLE_LABELS } from './constants/organisme'

export function formatAgentRole(role: string): string {
  return ROLE_LABELS[role as keyof typeof ROLE_LABELS] ?? role
}
