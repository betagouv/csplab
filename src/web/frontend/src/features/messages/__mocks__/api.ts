import type * as Api from '@/features/messages/api'
import type { Conversation, ConversationMessage } from '@/features/messages/types'
import { DEMO_CANDIDATURE, DEMO_UTILISATEUR, demoDate, paginated } from '@/api/__mocks__/demo'
// Demo data only: the conversations follow the unread counts of the demo candidatures
// eslint-disable-next-line no-restricted-imports
import { demoCandidatureDetail, demoListe } from '@/features/candidatures/__mocks__/demo'

export const CONVERSATIONS_LIMIT = 100
export const MESSAGES_LIMIT = 100

const RECRUTEUR = `${DEMO_UTILISATEUR.prenom} ${DEMO_UTILISATEUR.nom}`

function demoMessages(candidatureUuid: string): ConversationMessage[] {
  const { prenom, nom } = demoCandidatureDetail(candidatureUuid)?.candidat ?? DEMO_CANDIDATURE
  return [
    {
      author: RECRUTEUR,
      created_at: demoDate(2, 14, 0),
      content: `Bonjour ${prenom} ${nom},\n\nNous avons bien reçu votre candidature au poste de gestionnaire des ressources humaines et souhaitons vous rencontrer. Pourriez-vous nous indiquer vos disponibilités pour un entretien la semaine prochaine ?\n\nCordialement,\n${RECRUTEUR}`,
      documents: [],
    },
    {
      author: `${prenom} ${nom}`,
      created_at: demoDate(1, 18, 2),
      content: `Bonjour Madame ${DEMO_UTILISATEUR.nom},\n\nMerci pour votre message. Je suis disponible jeudi après-midi ou vendredi matin.\n\nBien cordialement,\n${prenom} ${nom}`,
      documents: [],
    },
  ]
}

const messagesByCandidature = new Map<string, ConversationMessage[]>()

function messagesOf(candidatureUuid: string): ConversationMessage[] {
  let messages = messagesByCandidature.get(candidatureUuid)
  if (!messages) {
    messages = demoMessages(candidatureUuid)
    messagesByCandidature.set(candidatureUuid, messages)
  }
  return messages
}

function conversation(candidatureUuid: string): Conversation {
  const messages = messagesOf(candidatureUuid)
  const last = messages.at(-1)!
  return {
    uuid: '80000000-0000-4000-8000-000000000001',
    objet: 'Entretien pour le poste de gestionnaire des ressources humaines',
    creator: RECRUTEUR,
    created_at: messages[0]!.created_at,
    last_message_content: last.content,
    last_message_author: last.author,
    last_message_created_at: last.created_at,
    is_unread: last.author !== RECRUTEUR,
  }
}

function hasConversation(candidatureUuid: string): boolean {
  return candidatureUuid === DEMO_CANDIDATURE.uuid
    || demoListe().some(({ uuid, unread_conversations }) => uuid === candidatureUuid && unread_conversations > 0)
}

export const getConversations: typeof Api.getConversations = async ({ candidatureUuid }) =>
  paginated(hasConversation(candidatureUuid) ? [conversation(candidatureUuid)] : [])

export const getConversationMessages: typeof Api.getConversationMessages = async ({ candidatureUuid }) =>
  paginated(messagesOf(candidatureUuid))

export const replyToConversation: typeof Api.replyToConversation = async ({ candidatureUuid }, _conversationUuid, { content }) => {
  const message = { author: RECRUTEUR, created_at: new Date().toISOString(), content, documents: [] }
  messagesOf(candidatureUuid).push(message)
  return message
}

export const createConversation: typeof Api.createConversation = async ({ candidatureUuid }, { objet }) => ({
  ...conversation(candidatureUuid),
  uuid: crypto.randomUUID(),
  objet,
})
