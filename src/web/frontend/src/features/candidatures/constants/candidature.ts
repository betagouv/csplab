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

export const CANDIDATURE_PANEL_TAB_LABELS = {
  candidature: 'Candidature',
  historique: 'Historique d\'activité',
  documents: 'Documents',
  notes: 'Notes',
  messages: 'Messages',
} as const

export type CandidaturePanelTabKey = keyof typeof CANDIDATURE_PANEL_TAB_LABELS

export const CANDIDATURE_PANEL_TAB_ICONS = {
  candidature: 'ri:user-line',
  historique: 'ri:history-line',
  documents: 'ri:file-list-line',
  notes: 'ri:sticky-note-line',
  messages: 'ri:question-answer-line',
} as const satisfies Record<CandidaturePanelTabKey, string>

export const TYPE_DOCUMENT_LABELS = {
  cv: 'Curriculum vitae',
  lettre_motivation: 'Lettre de motivation',
  piece_justificative: 'Pièce justificative',
  autre: 'Autre document',
} as const

export const LATEST_ACTIVITES_LIMIT = 3

export const ACTIVITE_LABELS = {
  CandidatureRecue: 'Candidature reçue',
  CandidatureEtapeModifiee: 'Étape modifiée',
  NoteAjoutee: 'Note ajoutée',
  NoteEditee: 'Note modifiée',
  NoteSupprimee: 'Note supprimée',
} as const

export type ActiviteEventName = keyof typeof ACTIVITE_LABELS

export const ACTIVITE_ICONS = {
  CandidatureRecue: 'ri:inbox-2-line',
  CandidatureEtapeModifiee: 'ri:arrow-left-right-line',
  NoteAjoutee: 'ri:sticky-note-line',
  NoteEditee: 'ri:edit-line',
  NoteSupprimee: 'ri:delete-bin-line',
} as const satisfies Record<ActiviteEventName, string>

export const DEFAULT_ACTIVITE = { label: 'Activité', icon: 'ri:history-line' }
