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

export function formatAgentLabel(agent: AgentIdentite & { email: string }): string {
  return formatAgentName(agent) || agent.email
}
