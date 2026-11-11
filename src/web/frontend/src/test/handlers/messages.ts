import type { Conversation, ConversationMessage } from '@/features/messages/types'
import { CONVERSATION, CONVERSATIONS, MESSAGES, REPLY } from '@/test/fixtures/messages'
import { failure, http } from './http'

const CONVERSATIONS_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations'
const CONVERSATION_PATH = '/recruteur/organismes/{organisme_uuid}/recrutements/{recrutement_uuid}/candidatures/{candidature_uuid}/conversations/{conversation_uuid}'

export function conversations(
  results: Conversation[] = CONVERSATIONS,
  onRequest?: (candidatureUuid: string) => void,
) {
  return http.get(CONVERSATIONS_PATH, ({ params, response }) => {
    onRequest?.(params.candidature_uuid)
    return response(200).json({ count: results.length, results })
  })
}

export function conversationsFailure(status: number) {
  return http.get(CONVERSATIONS_PATH, ({ response }) => response.untyped(failure(status)))
}

export function conversationCreation(
  conversation: Conversation = CONVERSATION,
  onRequest?: (candidatureUuid: string, payload: FormData) => void,
) {
  return http.post(CONVERSATIONS_PATH, async ({ params, request, response }) => {
    onRequest?.(params.candidature_uuid, await request.formData())
    return response(201).json(conversation)
  })
}

export function conversationCreationFailure(status: number) {
  return http.post(CONVERSATIONS_PATH, ({ response }) => response.untyped(failure(status)))
}

export function conversationMessages(
  results: ConversationMessage[] = MESSAGES,
  onRequest?: (conversationUuid: string) => void,
) {
  return http.get(CONVERSATION_PATH, ({ params, response }) => {
    onRequest?.(params.conversation_uuid)
    return response(200).json({ results })
  })
}

export function conversationMessagesFailure(status: number) {
  return http.get(CONVERSATION_PATH, ({ response }) => response.untyped(failure(status)))
}

export function reply(
  message: ConversationMessage = REPLY,
  onRequest?: (conversationUuid: string, payload: FormData) => void | Promise<void>,
) {
  return http.post(CONVERSATION_PATH, async ({ params, request, response }) => {
    await onRequest?.(params.conversation_uuid, await request.formData())
    return response(201).json(message)
  })
}

export function replyFailure(status: number) {
  return http.post(CONVERSATION_PATH, ({ response }) => response.untyped(failure(status)))
}

export const messagesHandlers = [
  conversations(),
  conversationCreation(),
  conversationMessages(),
  reply(),
]
