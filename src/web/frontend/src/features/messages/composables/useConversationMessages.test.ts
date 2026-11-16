import type { QueryCache } from '@pinia/colada'
import type { Conversation, ConversationMessage, PaginatedConversationList, PaginatedConversationMessageList } from '../types'
import type { ConversationParams } from '@/api/params'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { flushPromises, mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { candidatureKeys, organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { getConversationMessages, replyToConversation } from '../api'
import { useConversationMessages, useReplyConversation } from './useConversationMessages'

vi.mock('../api', () => ({
  getConversationMessages: vi.fn(),
  replyToConversation: vi.fn(),
}))

const CONVERSATION_A = 'ffffffff-0001-0001-0001-000000000001'
const CONVERSATION_B = 'ffffffff-0001-0001-0001-000000000002'

const EMPTY_THREAD: PaginatedConversationMessageList = { results: [] }

const MESSAGE: ConversationMessage = {
  content: 'Bonjour',
  author: 'Camille Durand',
  created_at: '2026-10-01T10:00:00Z',
  documents: [],
}

function mountReplyConversation(conversationUuid: string) {
  const params = ref<ConversationParams>({ ...CANDIDATURE_PARAMS, conversationUuid })
  let context!: ReturnType<typeof useReplyConversation>
  let queryCache!: QueryCache

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

function unreadConversation(uuid: string): Conversation {
  return {
    uuid,
    objet: 'Convocation',
    creator: 'Camille Durand',
    created_at: '2026-10-01T09:00:00Z',
    last_message_content: 'Bonjour',
    last_message_author: 'Alice Dupont',
    last_message_created_at: '2026-10-01T10:00:00Z',
    is_unread: true,
  }
}

function mountConversationMessages(conversations: Conversation[]) {
  let queryCache!: QueryCache

  mount(defineComponent({
    setup() {
      queryCache = useQueryCache()
      queryCache.setQueryData(candidatureKeys.conversations(CANDIDATURE_PARAMS), { count: conversations.length, results: conversations })
      vi.spyOn(queryCache, 'invalidateQueries')
      useConversationMessages({ ...CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_A })
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  return { queryCache }
}

describe('useConversationMessages', () => {
  it('marks the loaded conversation as read, since loading it marks it as read on the server', async () => {
    vi.mocked(getConversationMessages).mockResolvedValue(EMPTY_THREAD)
    const { queryCache } = mountConversationMessages([unreadConversation(CONVERSATION_A), unreadConversation(CONVERSATION_B)])
    expect(queryCache.invalidateQueries).not.toHaveBeenCalled()

    await flushPromises()

    const list = queryCache.getQueryData<PaginatedConversationList>(candidatureKeys.conversations(CANDIDATURE_PARAMS))
    expect(list?.results.map(({ uuid, is_unread }) => [uuid, is_unread])).toEqual([[CONVERSATION_A, false], [CONVERSATION_B, true]])
    expect(vi.mocked(queryCache.invalidateQueries).mock.calls.map(([filters]) => filters?.key)).toEqual([
      recrutementKeys.liste(CANDIDATURE_PARAMS),
      organismeKeys.recrutementsActifs(CANDIDATURE_PARAMS),
    ])
  })
})

describe('useReplyConversation', () => {
  it('appends the reply to the conversation it was sent from, even after switching conversation', async () => {
    let resolve!: (message: ConversationMessage) => void
    vi.mocked(replyToConversation).mockReturnValue(new Promise((r) => {
      resolve = r
    }))
    const { context, params, queryCache } = mountReplyConversation(CONVERSATION_A)
    const threadA = candidatureKeys.conversation({ ...CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_A })
    const threadB = candidatureKeys.conversation({ ...CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_B })
    queryCache.setQueryData(threadA, EMPTY_THREAD)
    queryCache.setQueryData(threadB, EMPTY_THREAD)

    const sending = context.reply({ content: 'Bonjour' })
    params.value = { ...CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_B }
    resolve(MESSAGE)
    await sending

    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadA)?.results).toEqual([MESSAGE])
    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadB)?.results).toEqual([])
  })
})
