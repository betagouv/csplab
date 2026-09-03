export const CANDIDATURE_TAB_LABELS = {
  'candidatures': 'Candidatures',
  'activites-et-taches': 'Activités et tâches',
} as const

export type CandidatureTabKey = keyof typeof CANDIDATURE_TAB_LABELS

export const CANDIDATURE_TAB_ICONS = {
  'candidatures': 'ri:group-line',
  'activites-et-taches': 'ri:list-check',
} as const satisfies Record<CandidatureTabKey, string>
