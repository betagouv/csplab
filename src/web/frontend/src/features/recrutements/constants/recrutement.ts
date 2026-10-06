import type { RecrutementKey } from '../types'

export const RECRUTEMENT_TAB_LABELS = {
  actifs: 'Recrutements en cours',
  archives: 'Recrutements terminés',
} as const satisfies Record<RecrutementKey, string>

export const RECRUTEMENT_TAB_ICONS = {
  actifs: 'ri:briefcase-line',
  archives: 'ri:archive-line',
} as const satisfies Record<RecrutementKey, string>

export const RECRUTEMENT_DETAIL_TAB_LABELS = {
  'candidatures': 'Candidatures',
  'activites-et-taches': 'Activités et tâches',
  'equipe': 'Équipe de recrutement',
} as const

export type RecrutementDetailTabKey = keyof typeof RECRUTEMENT_DETAIL_TAB_LABELS

export const RECRUTEMENT_DETAIL_TAB_ICONS = {
  'candidatures': 'ri:group-line',
  'activites-et-taches': 'ri:list-check',
  'equipe': 'ri:team-line',
} as const satisfies Record<RecrutementDetailTabKey, string>
