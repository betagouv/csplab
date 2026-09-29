import type { RecrutementKey } from '../types'

export const RECRUTEMENT_TAB_LABELS = {
  actifs: 'Recrutements en cours',
  archives: 'Recrutements terminés',
} as const satisfies Record<RecrutementKey, string>

export const RECRUTEMENT_TAB_ICONS = {
  actifs: 'ri:briefcase-line',
  archives: 'ri:archive-line',
} as const satisfies Record<RecrutementKey, string>
