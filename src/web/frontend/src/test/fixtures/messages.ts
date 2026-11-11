import type { Conversation, ConversationMessage } from '@/features/messages/types'

export const CONVERSATION_UUID = 'ffffffff-0001-0001-0001-000000000001'

export const CONVERSATION: Conversation = {
  uuid: CONVERSATION_UUID,
  objet: 'Convocation',
  creator: 'Camille Durand',
  created_at: '2025-06-12T09:00:00Z',
  last_message_content: 'Bonjour, je serai disponible',
  last_message_author: 'Alice Dupont',
  last_message_created_at: '2025-06-12T10:00:00Z',
  is_unread: false,
}

export const CONVERSATIONS: Conversation[] = [CONVERSATION]

export const MESSAGE: ConversationMessage = {
  content: 'Bonjour, je serai disponible',
  author: 'Alice Dupont',
  created_at: '2025-06-12T10:00:00Z',
  documents: [],
}

export const MESSAGES: ConversationMessage[] = [MESSAGE]

export const REPLY: ConversationMessage = {
  content: 'Merci, à bientôt',
  author: 'Camille Durand',
  created_at: '2025-06-12T11:00:00Z',
  documents: [],
}
