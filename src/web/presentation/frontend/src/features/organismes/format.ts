import type { AgentOrganisme } from './types'
import { ROLE_LABELS } from './constants/organisme'

export function formatAgentName(agent: AgentOrganisme): string {
  return `${agent.prenom} ${agent.nom}`.trim()
}

export function formatAgentNameAlphabetical(agent: AgentOrganisme): string {
  return `${agent.nom} ${agent.prenom}`.trim()
}

export function formatAgentRole(role: string): string {
  return ROLE_LABELS[role as keyof typeof ROLE_LABELS] ?? role
}
