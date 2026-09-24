import type { InjectionKey } from 'vue'
import type { AgentOrganisme, Role } from '../types'
import type { Request } from '@/composables/ui/useRequest'
import { inject, provide } from 'vue'
import { createRequest } from '@/composables/ui/useRequest'

export interface AgentActions {
  roleChange: Request<{ agent: AgentOrganisme, role: Role }>
  revocation: Request<AgentOrganisme>
}

const KEY: InjectionKey<AgentActions> = Symbol('agent-actions')

export function provideAgentActions(): AgentActions {
  const actions: AgentActions = {
    roleChange: createRequest(),
    revocation: createRequest(),
  }
  provide(KEY, actions)
  return actions
}

export function useAgentActions(): AgentActions {
  const actions = inject(KEY)
  if (!actions)
    throw new Error('useAgentActions must be used within provideAgentActions')
  return actions
}
