import type * as Api from '@/features/messages/api'
import type { Conversation, ConversationMessage } from '@/features/messages/types'
import { DEMO_CANDIDATURE, DEMO_UTILISATEUR, demoDate, paginated } from '@/api/__mocks__/demo'

export const CONVERSATIONS_LIMIT = 100
export const MESSAGES_LIMIT = 100

const RECRUTEUR = `${DEMO_UTILISATEUR.prenom} ${DEMO_UTILISATEUR.nom}`
const CANDIDAT = `${DEMO_CANDIDATURE.prenom} ${DEMO_CANDIDATURE.nom}`

const MESSAGES: ConversationMessage[] = [
  {
    author: RECRUTEUR,
    created_at: demoDate(2, 14, 0),
    content: `Bonjour Madame ${DEMO_CANDIDATURE.nom},\n\nNous avons bien reçu votre candidature au poste de gestionnaire des ressources humaines et souhaitons vous rencontrer. Pourriez-vous nous indiquer vos disponibilités pour un entretien la semaine prochaine ?\n\nCordialement,\n${RECRUTEUR}`,
    documents: [],
  },
  {
    author: CANDIDAT,
    created_at: demoDate(1, 18, 2),
    content: `Bonjour Madame ${DEMO_UTILISATEUR.nom},\n\nMerci pour votre message. Je suis disponible jeudi après-midi ou vendredi matin.\n\nBien cordialement,\n${CANDIDAT}`,
    documents: [],
  },
]

function conversation(): Conversation {
  const last = MESSAGES.at(-1)!
  return {
    uuid: '80000000-0000-4000-8000-000000000001',
    objet: 'Entretien pour le poste de gestionnaire des ressources humaines',
    creator: RECRUTEUR,
    created_at: MESSAGES[0]!.created_at,
    last_message_content: last.content,
    last_message_author: last.author,
    last_message_created_at: last.created_at,
    is_unread: false,
  }
}

export const getConversations: typeof Api.getConversations = async ({ candidatureUuid }) =>
  paginated(candidatureUuid === DEMO_CANDIDATURE.uuid ? [conversation()] : [])

export const getConversationMessages: typeof Api.getConversationMessages = async () => paginated(MESSAGES)

export const replyToConversation: typeof Api.replyToConversation = async (_candidature, _conversationUuid, { content }) => {
  const message = { author: RECRUTEUR, created_at: new Date().toISOString(), content, documents: [] }
  MESSAGES.push(message)
  return message
}

export const createConversation: typeof Api.createConversation = async (_candidature, { objet }) => ({
  ...conversation(),
  uuid: crypto.randomUUID(),
  objet,
})
