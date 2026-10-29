import type { QueryCache } from '@pinia/colada'
import type { ConversationMessage, PaginatedConversationMessageList } from '../types'
import type { ConversationParams } from '@/api/params'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { flushPromises, mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { candidatureKeys, organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { getConversationMessages, replyToConversation } from '../api'
import { useConversationMessages, useReplyConversation } from './useConversationMessages'

vi.mock('../api', () => ({
  getConversationMessages: vi.fn(),
  replyToConversation: vi.fn(),
}))

const CANDIDATURE = {
  organismeUuid: '00000000-0000-0000-0000-000000000000',
  recrutementUuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  candidatureUuid: 'dddddddd-0001-0001-0001-000000000001',
}
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
  const params = ref<ConversationParams>({ ...CANDIDATURE, conversationUuid })
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

function mountConversationMessages() {
  let queryCache!: QueryCache

  mount(defineComponent({
    setup() {
      queryCache = useQueryCache()
      vi.spyOn(queryCache, 'invalidateQueries')
      useConversationMessages({ ...CANDIDATURE, conversationUuid: CONVERSATION_A })
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  return { queryCache }
}

describe('useConversationMessages', () => {
  it('refreshes the unread counters once the thread is loaded, since loading it marks it as read', async () => {
    vi.mocked(getConversationMessages).mockResolvedValue(EMPTY_THREAD)
    const { queryCache } = mountConversationMessages()
    expect(queryCache.invalidateQueries).not.toHaveBeenCalled()

    await flushPromises()

    expect(vi.mocked(queryCache.invalidateQueries).mock.calls.map(([filters]) => filters?.key)).toEqual([
      recrutementKeys.liste(CANDIDATURE),
      recrutementKeys.kanban(CANDIDATURE),
      organismeKeys.recrutementsActifs(CANDIDATURE),
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
    const threadA = candidatureKeys.conversation({ ...CANDIDATURE, conversationUuid: CONVERSATION_A })
    const threadB = candidatureKeys.conversation({ ...CANDIDATURE, conversationUuid: CONVERSATION_B })
    queryCache.setQueryData(threadA, EMPTY_THREAD)
    queryCache.setQueryData(threadB, EMPTY_THREAD)

    const sending = context.reply({ content: 'Bonjour' })
    params.value = { ...CANDIDATURE, conversationUuid: CONVERSATION_B }
    resolve(MESSAGE)
    await sending

    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadA)?.results).toEqual([MESSAGE])
    expect(queryCache.getQueryData<PaginatedConversationMessageList>(threadB)?.results).toEqual([])
  })
})
