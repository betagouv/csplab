import type { InjectionKey, Ref } from 'vue'
import type { MembreEquipe } from '../types'
import type { Request } from '@/composables/ui/useRequest'
import { inject, provide } from 'vue'
import { createRequest } from '@/composables/ui/useRequest'

export interface MembreEquipeActions {
  revocation: Request<MembreEquipe>
  roleChange: Request<MembreEquipe>
  canRevoke: Readonly<Ref<boolean>>
  canChangeRole: Readonly<Ref<boolean>>
}

const KEY: InjectionKey<MembreEquipeActions> = Symbol('membre-equipe-actions')

export function provideMembreEquipeActions(
  permissions: Pick<MembreEquipeActions, 'canRevoke' | 'canChangeRole'>,
): MembreEquipeActions {
  const actions: MembreEquipeActions = {
    revocation: createRequest(),
    roleChange: createRequest(),
    ...permissions,
  }
  provide(KEY, actions)
  return actions
}

export function useMembreEquipeActions(): MembreEquipeActions {
  const actions = inject(KEY)
  if (!actions) {
    throw new Error('useMembreEquipeActions must be used within provideMembreEquipeActions')
  }
  return actions
}
