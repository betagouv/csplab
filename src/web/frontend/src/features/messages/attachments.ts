import { MESSAGE_DOCUMENT_CONTENT_TYPES, MESSAGE_DOCUMENT_MAX_SIZE_MB, MESSAGE_MAX_DOCUMENTS } from './constants/message'

export interface Attachment {
  file: File
  error: string | null
}

const MAX_SIZE_BYTES = MESSAGE_DOCUMENT_MAX_SIZE_MB * 1024 * 1024

function fileError(file: File): string | null {
  if (!MESSAGE_DOCUMENT_CONTENT_TYPES.includes(file.type)) {
    return 'Format non supporté. Formats acceptés : PDF, PNG, JPEG.'
  }
  if (file.size > MAX_SIZE_BYTES) {
    return `Dépasse la taille maximale de ${MESSAGE_DOCUMENT_MAX_SIZE_MB} Mo.`
  }
  return null
}

export function validateAttachments(files: File[]): Attachment[] {
  let validCount = 0
  return files.map((file) => {
    const error = fileError(file)
    if (error) {
      return { file, error }
    }
    if (validCount === MESSAGE_MAX_DOCUMENTS) {
      return { file, error: `Limite de ${MESSAGE_MAX_DOCUMENTS} fichiers atteinte.` }
    }
    validCount++
    return { file, error: null }
  })
}

export function hasInvalidAttachment(files: File[]): boolean {
  return validateAttachments(files).some(({ error }) => error !== null)
}

export function countValidAttachments(files: File[]): number {
  return validateAttachments(files).filter(({ error }) => error === null).length
}
