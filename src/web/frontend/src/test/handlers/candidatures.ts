import type {
  Activite,
  CandidatureDetail,
  ChangerEtapeResultat,
  CreateNotePayload,
  DocumentListe,
  MotifRefusOption,
  Note,
  NoteVisibilitePayload,
  RecrutementListe,
} from '@/features/candidatures/types'
import type { components } from '@/types/api'
import { HttpResponse } from 'msw'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_LISTE,
  candidatureDetail,
  MOTIFS_REFUS,
  NOTE,
} from '@/test/fixtures/candidatures'
import { failure, http } from './http'

type EtapeChangePayload = components['schemas']['PatchedChangerEtapeCandidatures'] | undefined
type NoteChangePayload = components['schemas']['PatchedUpdateNote'] | undefined

const LISTE = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/liste'
const ETAPE = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/etape'
const MOTIFS = '/recruteur/organismes/{organisme_uuid}/parametres/motifs-refus'
const CANDIDATURE = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}'
const DOCUMENTS = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents'
const DOCUMENT = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents/{document_uuid}'
const NOTES = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes'
const NOTE_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes/{note_uuid}'
const VISIBILITE = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes/{note_uuid}/visibilite'
const DEFAULT_PAGE_SIZE = 100
const ACTIVITES = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/logs'

function noteDetail(candidatureUuid: string, noteUuid: string, { message, est_privee }: { message: string, est_privee: boolean }) {
  return { uuid: noteUuid, candidature_id: candidatureUuid, message, publie_par_id: NOTE.publie_par_id, est_privee, tags: [] }
}

export function candidatureListe(liste: RecrutementListe = CANDIDATURE_LISTE, onRequest?: () => void | Promise<void>) {
  return http.get(LISTE, async ({ response }) => {
    await onRequest?.()
    return response(200).json(liste)
  })
}

export function candidatureListePages(rows: RecrutementListe['results'], onRequest?: () => void) {
  return http.get(LISTE, ({ query, response }) => {
    onRequest?.()
    const taille = Number(query.get('taille') ?? DEFAULT_PAGE_SIZE)
    return response(200).json({ ...CANDIDATURE_LISTE, count: rows.length, results: rows.slice(0, taille) })
  })
}

export function candidatureListeFailure(status: number) {
  return http.get(LISTE, ({ response }) => response.untyped(failure(status)))
}

export function candidature(detail: (candidatureUuid: string) => CandidatureDetail = candidatureDetail) {
  return http.get(CANDIDATURE, ({ params, response }) => response(200).json(detail(params.candidature_uuid)))
}

export function candidatureFailure(candidatureUuid: string, status: number) {
  return http.get(CANDIDATURE, ({ params, response }) =>
    params.candidature_uuid === candidatureUuid ? response.untyped(failure(status)) : undefined)
}

export function etapeChange(
  resultat: ChangerEtapeResultat = { reussites: [CANDIDATURE_ALICE], echecs: [] },
  onRequest?: (organismeUuid: string, recrutementUuid: string, payload: EtapeChangePayload) => void | Promise<void>,
) {
  return http.patch(ETAPE, async ({ params, request, response }) => {
    await onRequest?.(params.organisme_uuid, params.recrutement_uuid, await request.json())
    return response(200).json(resultat)
  })
}

export function etapeChangeFailure(status: number, onRequest?: (payload: EtapeChangePayload) => Promise<void>) {
  return http.patch(ETAPE, async ({ request, response }) => {
    await onRequest?.(await request.json())
    return response.untyped(failure(status))
  })
}

export function motifsRefus(motifs: MotifRefusOption[] = MOTIFS_REFUS) {
  return http.get(MOTIFS, ({ response }) => response(200).json(motifs))
}

export function candidatureDocuments(results: DocumentListe[] = []) {
  return http.get(DOCUMENTS, ({ response }) => response(200).json({ count: results.length, results }))
}

export function candidatureDocumentsFailure(status: number) {
  return http.get(DOCUMENTS, ({ response }) => response.untyped(failure(status)))
}

export function candidatureDocumentFile(onRequest?: (documentUuid: string) => void) {
  return http.get(DOCUMENT, ({ params, response }) => {
    onRequest?.(params.document_uuid)
    return response.untyped(new HttpResponse(null, { headers: { 'Content-Type': 'application/pdf' } }))
  })
}

export function candidatureDocumentFileFailure(status: number) {
  return http.get(DOCUMENT, ({ response }) => response.untyped(failure(status)))
}

export function candidatureNotes(results: Note[] = [NOTE]) {
  return http.get(NOTES, ({ response }) => response(200).json({ count: results.length, results }))
}

export function candidatureNotesFailure(status: number) {
  return http.get(NOTES, ({ response }) => response.untyped(failure(status)))
}

export function noteCreation(onRequest?: (candidatureUuid: string, payload: CreateNotePayload) => void) {
  return http.post(NOTES, async ({ params, request, response }) => {
    const payload = await request.json()
    onRequest?.(params.candidature_uuid, payload)
    return response(201).json(noteDetail(params.candidature_uuid, NOTE.uuid, payload))
  })
}

export function noteCreationFailure(status: number) {
  return http.post(NOTES, ({ response }) => response.untyped(failure(status)))
}

export function noteUpdate(onRequest?: (noteUuid: string, payload: NoteChangePayload) => void) {
  return http.patch(NOTE_PATH, async ({ params, request, response }) => {
    const payload = await request.json()
    onRequest?.(params.note_uuid, payload)
    return response(200).json(noteDetail(params.candidature_uuid, params.note_uuid, { ...NOTE, ...payload }))
  })
}

export function noteVisibiliteUpdate(onRequest?: (noteUuid: string, payload: NoteVisibilitePayload) => void) {
  return http.put(VISIBILITE, async ({ params, request, response }) => {
    const payload = await request.json()
    onRequest?.(params.note_uuid, payload)
    return response(200).json(noteDetail(params.candidature_uuid, params.note_uuid, { message: NOTE.message, ...payload }))
  })
}

export function noteDeletion(onRequest?: (noteUuid: string) => void) {
  return http.delete(NOTE_PATH, ({ params, response }) => {
    onRequest?.(params.note_uuid)
    return response(204).empty()
  })
}

export function candidatureActivites(
  results: Activite[] = [],
  onRequest?: (candidatureUuid: string, limit: string | null) => void,
) {
  return http.get(ACTIVITES, ({ params, query, response }) => {
    onRequest?.(params.candidature_uuid, query.get('limit'))
    return response(200).json({ count: results.length, results })
  })
}

export function candidatureActivitesFailure(status: number) {
  return http.get(ACTIVITES, ({ response }) => response.untyped(failure(status)))
}

export const candidaturesHandlers = [
  candidatureListe(),
  candidature(),
  etapeChange(),
  motifsRefus(),
  candidatureDocuments(),
  candidatureDocumentFile(),
  candidatureNotes(),
  noteCreation(),
  noteUpdate(),
  noteVisibiliteUpdate(),
  noteDeletion(),
  candidatureActivites(),
]
