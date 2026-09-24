import type { InjectionKey } from 'vue'
import type { MembreEquipe, RecrutementRole } from '../types'
import type { Request } from '@/composables/ui/useRequest'
import { inject, provide } from 'vue'
import { createRequest } from '@/composables/ui/useRequest'

export interface MembreEquipeActions {
  revocation: Request<MembreEquipe>
  roleChange: Request<{ membre: MembreEquipe, role: RecrutementRole }>
}

const KEY: InjectionKey<MembreEquipeActions> = Symbol('membre-equipe-actions')

export function provideMembreEquipeActions(): MembreEquipeActions {
  const actions: MembreEquipeActions = {
    revocation: createRequest(),
    roleChange: createRequest(),
  }
  provide(KEY, actions)
  return actions
}

export function useMembreEquipeActions(): MembreEquipeActions {
  const actions = inject(KEY)
  if (!actions)
    throw new Error('useMembreEquipeActions must be used within provideMembreEquipeActions')
  return actions
}
