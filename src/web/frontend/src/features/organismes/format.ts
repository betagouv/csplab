import { ROLE_LABELS } from './constants/organisme'

interface AgentIdentite {
  prenom: string
  nom: string
}

export function formatAgentName(agent: AgentIdentite): string {
  return `${agent.prenom} ${agent.nom}`.trim()
}

export function formatAgentNameAlphabetical(agent: AgentIdentite): string {
  return `${agent.nom} ${agent.prenom}`.trim()
}

export function formatAgentRole(role: string): string {
  return ROLE_LABELS[role as keyof typeof ROLE_LABELS] ?? role
}
