import type { ActivitesParams, CandidatureDetail, ChangerEtapeResultat, CreateNotePayload, MotifRefus, MotifRefusOption, NoteVisibilitePayload, PaginatedActiviteList, PaginatedCandidatureListeList, PaginatedDocumentListeList, PaginatedNoteList, RecrutementDetailKanban, UpdateNotePayload } from './types'
import type { CandidatureParams, DocumentParams, NoteParams, OrganismeParams, RecrutementParams } from '@/api/params'
import { api } from '@/api/client'

export async function getRecrutementKanban({ organismeUuid, recrutementUuid }: RecrutementParams): Promise<RecrutementDetailKanban> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/kanban',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
    },
  )
  return data!
}

export async function getCandidatureDetail(candidature: CandidatureParams): Promise<CandidatureDetail> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}',
    { params: { path: candidaturePath(candidature) } },
  )
  return data!
}

export async function getCandidatureListe({ organismeUuid, recrutementUuid }: RecrutementParams): Promise<PaginatedCandidatureListeList> {
  async function fetchListe(taille?: number): Promise<PaginatedCandidatureListeList> {
    const { data } = await api.GET(
      '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/liste',
      {
        params: {
          path: {
            organisme_uuid: organismeUuid,
            recrutement_uuid: recrutementUuid,
          },
          query: { taille },
        },
      },
    )
    return data!
  }

  const firstPage = await fetchListe()
  if (firstPage.results.length >= firstPage.count) {
    return firstPage
  }
  return fetchListe(firstPage.count)
}

export interface EtapeChange {
  etapeCibleUuid: string
  candidatureUuids: string[]
  motifRefus?: MotifRefus
}

export async function patchEtapeCandidatures(
  organismeUuid: string,
  recrutementUuid: string,
  { etapeCibleUuid, candidatureUuids, motifRefus }: EtapeChange,
): Promise<ChangerEtapeResultat> {
  const { data } = await api.PATCH(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/etape',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
        },
      },
      body: {
        etape_cible_uuid: etapeCibleUuid,
        candidatures: candidatureUuids.map(uuid => ({ candidature_uuid: uuid })),
        motif_refus: motifRefus,
      },
    },
  )
  return data!
}

export async function getMotifsRefus({ organismeUuid }: OrganismeParams): Promise<MotifRefusOption[]> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/parametres/motifs-refus',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
        },
      },
    },
  )
  return data as MotifRefusOption[]
}

function candidaturePath({ organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams) {
  return {
    organisme_uuid: organismeUuid,
    recrutement_uuid: recrutementUuid,
    candidature_uuid: candidatureUuid,
  }
}

export async function getCandidatureDocuments(candidature: CandidatureParams): Promise<PaginatedDocumentListeList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents',
    { params: { path: candidaturePath(candidature) } },
  )
  return data!
}

export async function checkCandidatureDocument(params: DocumentParams): Promise<void> {
  const { response } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents/{document_uuid}',
    { params: { path: { ...candidaturePath(params), document_uuid: params.documentUuid } }, parseAs: 'stream' },
  )
  await response.body?.cancel()
}

export function candidatureDocumentUrl(
  { organismeUuid, recrutementUuid, candidatureUuid }: CandidatureParams,
  documentUuid: string,
): string {
  return `/recruteur/organismes/${organismeUuid}/recrutements/${recrutementUuid}/candidatures/${candidatureUuid}/documents/${documentUuid}`
}

export async function getCandidatureNotes(candidature: CandidatureParams): Promise<PaginatedNoteList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes',
    { params: { path: candidaturePath(candidature) } },
  )
  return data!
}

export async function createCandidatureNote(candidature: CandidatureParams, payload: CreateNotePayload): Promise<void> {
  await api.POST(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes',
    { params: { path: candidaturePath(candidature) }, body: payload },
  )
}

export async function getCandidatureActivites(params: ActivitesParams): Promise<PaginatedActiviteList> {
  const { data } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/logs',
    { params: { path: candidaturePath(params), query: { limit: params.limit } } },
  )
  return data!
}

export async function updateCandidatureNote(params: NoteParams, payload: UpdateNotePayload): Promise<void> {
  await api.PATCH(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes/{note_uuid}',
    { params: { path: { ...candidaturePath(params), note_uuid: params.noteUuid } }, body: payload },
  )
}

export async function updateCandidatureNoteVisibilite(params: NoteParams, payload: NoteVisibilitePayload): Promise<void> {
  await api.PUT(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes/{note_uuid}/visibilite',
    { params: { path: { ...candidaturePath(params), note_uuid: params.noteUuid } }, body: payload },
  )
}

export async function deleteCandidatureNote(params: NoteParams): Promise<void> {
  await api.DELETE(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/notes/{note_uuid}',
    { params: { path: { ...candidaturePath(params), note_uuid: params.noteUuid } } },
  )
}
