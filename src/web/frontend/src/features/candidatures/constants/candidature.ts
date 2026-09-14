export const CANDIDATURE_TAB_LABELS = {
  'candidatures': 'Candidatures',
  'activites-et-taches': 'Activités et tâches',
  'equipe': 'Équipe de recrutement',
} as const

export type CandidatureTabKey = keyof typeof CANDIDATURE_TAB_LABELS

export const CANDIDATURE_TAB_ICONS = {
  'candidatures': 'ri:group-line',
  'activites-et-taches': 'ri:list-check',
  'equipe': 'ri:team-line',
} as const satisfies Record<CandidatureTabKey, string>
