import type { components } from '@/types/api'

export type AuthorizedAction = components['schemas']['AuthorizedActionsEnum']

export function can(
  authorizedActions: readonly AuthorizedAction[] | null | undefined,
  action: AuthorizedAction,
): boolean {
  return authorizedActions?.includes(action) ?? false
}
