export interface OrganismeParams {
  organismeUuid: string
}

export interface RecrutementParams extends OrganismeParams {
  recrutementUuid: string
}

export interface CandidatureParams extends RecrutementParams {
  candidatureUuid: string
}

export interface DocumentParams extends CandidatureParams {
  documentUuid: string
}

export interface NoteParams extends CandidatureParams {
  noteUuid: string
}

export interface ConversationParams extends CandidatureParams {
  conversationUuid: string
}
