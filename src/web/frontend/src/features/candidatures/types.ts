import type { components } from '@/types/api'

export type RecrutementDetailKanban = components['schemas']['RecrutementDetailKanban']

export type EtapeRecrutementDetailedCandidatures = components['schemas']['EtapeRecrutementDetailedCandidatures']

export type Candidature = components['schemas']['Candidature']

export type Candidat = components['schemas']['Candidat']

export type PaginatedCandidatureListeList = components['schemas']['PaginatedCandidatureListeList']

export type CandidatureListe = components['schemas']['CandidatureListe']

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

export type ChangerEtapeResultat = components['schemas']['ChangerEtapeResultat']

export type MotifRefus = components['schemas']['MotifRefusEnum']

export type MotifRefusOption = components['schemas']['MotifRefus'] & { value: MotifRefus }

export type DocumentListe = components['schemas']['DocumentListe']

export type PaginatedDocumentListeList = components['schemas']['PaginatedDocumentListeList']

export interface CandidatureParams {
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}
