import type { MaybeRefOrGetter } from 'vue'
import type { CandidatureParams, DocumentListe } from '../types'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureDocumentUrl } from '../api'
import { candidatureDocumentCheckQuery, candidatureDocumentsQuery } from '../queries'

const PDF_CONTENT_TYPE = 'application/pdf'

export function useCandidatureDocuments(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => candidatureDocumentsQuery(toValue(candidature)))

  const documents = computed<DocumentListe[]>(() => query.data.value?.results ?? [])

  function pdfUrl(document: DocumentListe): string | null {
    if (document.content_type !== PDF_CONTENT_TYPE) {
      return null
    }
    return candidatureDocumentUrl(toValue(candidature), document.uuid)
  }

  return {
    documents,
    total: computed(() => query.data.value?.count ?? 0),
    pending: computed(() => query.isPending.value),
    error: computed(() => query.error.value),
    pdfUrl,
  }
}

export function useCandidatureDocumentCheck(
  candidature: MaybeRefOrGetter<CandidatureParams>,
  documentUuid: MaybeRefOrGetter<string | null>,
) {
  const query = useQuery(() => ({
    ...candidatureDocumentCheckQuery({ candidature: toValue(candidature), documentUuid: toValue(documentUuid) ?? '' }),
    enabled: toValue(documentUuid) !== null,
  }))

  return {
    pending: computed(() => toValue(documentUuid) !== null && query.isPending.value),
    error: computed(() => query.error.value),
  }
}
