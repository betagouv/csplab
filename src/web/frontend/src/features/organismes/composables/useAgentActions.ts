import type { AgentOrganisme, Role } from '../types'
import { ref } from 'vue'

const roleChange = ref<{ agent: AgentOrganisme, role: Role } | null>(null)
const revocationAgent = ref<AgentOrganisme | null>(null)

function requestRoleChange(agent: AgentOrganisme, role: Role): void {
  roleChange.value = { agent, role }
}

function clearRoleChange(): void {
  roleChange.value = null
}

function requestRevocation(agent: AgentOrganisme): void {
  revocationAgent.value = agent
}

function clearRevocation(): void {
  revocationAgent.value = null
}

export function useAgentActions() {
  return {
    roleChange,
    requestRoleChange,
    clearRoleChange,
    revocationAgent,
    requestRevocation,
    clearRevocation,
  }
}
