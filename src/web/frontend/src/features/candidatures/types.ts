import type { CandidatureParams } from '@/api/params'
import type { components } from '@/types/api'

export type Candidat = components['schemas']['Candidat']

export type CandidatureDetail = components['schemas']['CandidatureDetail']

export type RecrutementListe = components['schemas']['RecrutementListe']

export type CandidatureListe = components['schemas']['CandidatureListe']

export type EtapeRecrutement = components['schemas']['EtapeRecrutement']

export type KanbanCard = Omit<CandidatureListe, 'etape'>

export type KanbanColumn = EtapeRecrutement & { candidatures: KanbanCard[] }

export type ChangerEtapeResultat = components['schemas']['ChangerEtapeResultat']

export type MotifRefus = components['schemas']['MotifRefusEnum']

export type MotifRefusOption = components['schemas']['MotifRefus'] & { value: MotifRefus }

export type DocumentListe = components['schemas']['DocumentListe']

export type PaginatedDocumentListeList = components['schemas']['PaginatedDocumentListeList']

export type Note = components['schemas']['Note']

export type PaginatedNoteList = components['schemas']['PaginatedNoteList']

export type CreateNotePayload = components['schemas']['CreateNote']

export type UpdateNotePayload = Required<components['schemas']['PatchedUpdateNote']>

export type NoteVisibilitePayload = components['schemas']['NoteVisibilite']

export interface NoteRouteNames {
  notes: string
  create: string
}

export type Activite = components['schemas']['AuditLog']

export type PaginatedActiviteList = components['schemas']['PaginatedAuditLogList']

export interface ActivitesParams extends CandidatureParams {
  limit?: number
}
