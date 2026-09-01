import type { RecrutementKey } from '../types'

export const RECRUTEMENT_TAB_LABELS = {
  actifs: 'Recrutements en cours',
  archives: 'Offres archivées',
} as const satisfies Record<RecrutementKey, string>
