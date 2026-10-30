import type { DocumentParams } from './params'
import { api } from './client'

export function candidatureDocumentUrl(
  { organismeUuid, recrutementUuid, candidatureUuid, documentUuid }: DocumentParams,
): string {
  return `/recruteur/organismes/${organismeUuid}/recrutements/${recrutementUuid}/candidatures/${candidatureUuid}/documents/${documentUuid}`
}

export async function checkCandidatureDocument(
  { organismeUuid, recrutementUuid, candidatureUuid, documentUuid }: DocumentParams,
): Promise<void> {
  const { response } = await api.GET(
    '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/documents/{document_uuid}',
    {
      params: {
        path: {
          organisme_uuid: organismeUuid,
          recrutement_uuid: recrutementUuid,
          candidature_uuid: candidatureUuid,
          document_uuid: documentUuid,
        },
      },
      parseAs: 'stream',
    },
  )
  await response.body?.cancel()
}
