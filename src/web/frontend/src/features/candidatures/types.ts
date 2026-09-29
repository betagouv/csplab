import type { components } from '@/types/api'

export interface Candidature {
  uuid: string
  date_soumission: string
  date_derniere_activite: string
  candidat: Candidat
}

export interface EtapeRecrutementDetailedCandidatures {
  etape_uuid: string
  nom: string
  categorie: EtapeRecrutement['categorie']
  candidatures: Candidature[]
}

export type Candidat = components['schemas']['Candidat']

export type CandidatureDetail = components['schemas']['CandidatureDetail']

export interface CandidatureParams {
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}

export type PaginatedCandidatureListeList = components['schemas']['PaginatedCandidatureListeList']

export type CandidatureListe = components['schemas']['CandidatureListe']

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

export type ChangerEtapeResultat = components['schemas']['ChangerEtapeResultat']

export type MotifRefus = components['schemas']['MotifRefusEnum']

export type MotifRefusOption = components['schemas']['MotifRefus'] & { value: MotifRefus }

export type DocumentListe = components['schemas']['DocumentListe']

export type PaginatedDocumentListeList = components['schemas']['PaginatedDocumentListeList']

export type Note = components['schemas']['Note']

export type PaginatedNoteList = components['schemas']['PaginatedNoteList']

export interface CandidatureParams {
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}
