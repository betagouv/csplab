import { formatPersonName } from '@/utils/format'

interface AgentIdentite {
  prenom: string
  nom: string
}

export function formatAgentNameAlphabetical(agent: AgentIdentite): string {
  return `${agent.nom} ${agent.prenom}`.trim()
}

export function formatAgentLabel(agent: AgentIdentite & { email: string }): string {
  return formatPersonName(agent) || agent.email
}

export function agentSearchKeys(agent: AgentIdentite & { email: string }): string[] {
  return [formatPersonName(agent), formatAgentNameAlphabetical(agent), agent.email]
}
