import type { ConversationMessagesParams } from '../queries'
import type { ConversationMessage, PaginatedConversationMessageList } from '../types'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { replyToConversation } from '../api'
import { MESSAGES_QUERY_KEYS } from '../queries'
import { useReplyConversation } from './useConversationMessages'

vi.mock('../api', () => ({
  replyToConversation: vi.fn(),
}))

const CANDIDATURE = {
  organismeUuid: '00000000-0000-0000-0000-000000000000',
  recrutementUuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  candidatureUuid: 'dddddddd-0001-0001-0001-000000000001',
}
const CONVERSATION_A = 'ffffffff-0001-0001-0001-000000000001'
const CONVERSATION_B = 'ffffffff-0001-0001-0001-000000000002'

const EMPTY_THREAD: PaginatedConversationMessageList = { count: 0, results: [] }

const MESSAGE: ConversationMessage = {
  content: 'Bonjour',
  author: 'Camille Durand',
  created_at: '2026-10-01T10:00:00Z',
  documents: [],
}

function mountReplyConversation(conversationUuid: string) {
  const params = ref<ConversationMessagesParams>({ candidature: CANDIDATURE, conversationUuid })
  let context!: ReturnType<typeof useReplyConversation>
  let queryCache!: ReturnType<typeof useQueryCache>

  mount(defineComponent({
    setup() {
      queryCache = useQueryCache()
      context = useReplyConversation(params)
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  return { context, params, queryCache }
}

describe('useReplyConversation', () => {
  it('appends the reply to the conversation it was sent from, even after switching conversation', async () => {
    let resolve!: (message: ConversationMessage) => void
    vi.mocked(replyToConversation).mockReturnValue(new Promise((r) => {
      resolve = r
    }))
    const { context, params, queryCache } = mountReplyConversation(CONVERSATION_A)
    const threadA = MESSAGES_QUERY_KEYS.conversation(CANDIDATURE, CONVERSATION_A)
    const threadB = MESSAGES_QUERY_KEYS.conversation(CANDIDATURE, CONVERSATION_B)
    queryCache.setQueryData(threadA, EMPTY_THREAD)
    queryCache.setQueryData(threadB, EMPTY_THREAD)

    const sending = context.reply({ content: 'Bonjour' })
    params.value = { candidature: CANDIDATURE, conversationUuid: CONVERSATION_B }
    resolve(MESSAGE)
    await sending

    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadA)?.results).toEqual([MESSAGE])
    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadB)?.results).toEqual([])
  })
})
