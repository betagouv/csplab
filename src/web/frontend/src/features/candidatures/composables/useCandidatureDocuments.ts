import type { MaybeRefOrGetter } from 'vue'
import type { DocumentListe } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { candidatureDocumentUrl } from '@/api/documents'
import { candidatureDocumentCheckQuery, candidatureDocumentsQuery } from '../queries'

const PDF_CONTENT_TYPE = 'application/pdf'

export function useCandidatureDocuments(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const query = useQuery(() => candidatureDocumentsQuery(toValue(candidature)))

  const documents = computed<DocumentListe[]>(() => query.data.value?.results ?? [])

  function documentUrl(document: DocumentListe): string {
    return candidatureDocumentUrl({ ...toValue(candidature), documentUuid: document.uuid })
  }

  function pdfUrl(document: DocumentListe): string | null {
    return document.content_type === PDF_CONTENT_TYPE ? documentUrl(document) : null
  }

  return {
    documents,
    total: computed(() => query.data.value?.count ?? 0),
    pending: computed(() => query.isPending.value),
    error: computed(() => query.error.value),
    documentUrl,
    pdfUrl,
  }
}

export function useCandidatureDocumentCheck(
  candidature: MaybeRefOrGetter<CandidatureParams>,
  documentUuid: MaybeRefOrGetter<string | null>,
) {
  const query = useQuery(() => ({
    ...candidatureDocumentCheckQuery({ ...toValue(candidature), documentUuid: toValue(documentUuid) ?? '' }),
    enabled: toValue(documentUuid) !== null,
  }))

  return {
    pending: computed(() => toValue(documentUuid) !== null && query.isPending.value),
    error: computed(() => query.error.value),
  }
}
