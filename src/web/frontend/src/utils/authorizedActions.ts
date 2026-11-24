import type { components } from '@/types/api'

export type AuthorizedAction = components['schemas']['AuthorizedActionsEnum']

export type EtapeAction = components['schemas']['EtapeActionsEnum']

export function can<Action extends AuthorizedAction | EtapeAction>(
  authorizedActions: readonly Action[] | null | undefined,
  action: NoInfer<Action>,
): boolean {
  return authorizedActions?.includes(action) ?? false
}
