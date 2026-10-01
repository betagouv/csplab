import { MESSAGE_DOCUMENT_CONTENT_TYPES, MESSAGE_DOCUMENT_MAX_SIZE_MB, MESSAGE_MAX_DOCUMENTS } from './constants/message'

export interface AttachmentsValidation {
  accepted: File[]
  errors: string[]
}

const MAX_SIZE_BYTES = MESSAGE_DOCUMENT_MAX_SIZE_MB * 1024 * 1024

function attachmentError(file: File): string | null {
  if (!MESSAGE_DOCUMENT_CONTENT_TYPES.includes(file.type))
    return `Format non supporté pour ${file.name}. Formats acceptés : PDF, PNG, JPEG.`
  if (file.size > MAX_SIZE_BYTES)
    return `Le fichier ${file.name} dépasse la taille maximale de ${MESSAGE_DOCUMENT_MAX_SIZE_MB} Mo.`
  return null
}

export function validateAttachments(current: File[], added: File[]): AttachmentsValidation {
  const accepted: File[] = []
  const errors: string[] = []
  for (const file of added) {
    const error = attachmentError(file)
    if (error)
      errors.push(error)
    else
      accepted.push(file)
  }
  const remaining = MESSAGE_MAX_DOCUMENTS - current.length
  if (accepted.length > remaining) {
    errors.push(`Vous pouvez joindre ${MESSAGE_MAX_DOCUMENTS} fichiers au maximum.`)
    accepted.splice(remaining)
  }
  return { accepted, errors }
}
