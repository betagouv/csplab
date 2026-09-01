export const CANDIDATURE_TAB_LABELS = {
  'candidatures': 'Candidatures',
  'activites-et-taches': 'Activités et tâches',
} as const

export type CandidatureTabKey = keyof typeof CANDIDATURE_TAB_LABELS
