import type { PersonId } from './types'
import type { Messagerie } from './useMessagerie'
import { computed, onBeforeUnmount, watch } from 'vue'

const READ_DELAY = 1500

export function useMessagesView(messagerie: Messagerie, viewerId: () => PersonId) {
  const { selectedId } = messagerie
  let timer: ReturnType<typeof setTimeout> | undefined

  const unreadIds = computed(() =>
    messagerie.summaries.value
      .filter(summary => messagerie.isUnread(summary.id, viewerId()))
      .map(summary => summary.id),
  )

  const current = computed(() =>
    messagerie.conversations.find(conversation => conversation.id === selectedId.value),
  )

  const currentMessages = computed(() => current.value ? messagerie.messagesOf(current.value.id) : [])

  const currentWaiting = computed(() => current.value ? messagerie.waiting(current.value.id) : null)

  function scheduleRead(): void {
    clearTimeout(timer)
    timer = setTimeout(() => messagerie.markRead(selectedId.value, viewerId()), READ_DELAY)
  }

  watch([selectedId, viewerId], scheduleRead, { immediate: true })
  onBeforeUnmount(() => clearTimeout(timer))

  function select(id: string): void {
    selectedId.value = id
  }

  function send(text: string): void {
    messagerie.markRead(selectedId.value, viewerId())
    messagerie.send(selectedId.value, viewerId(), text)
  }

  function choose(messageId: string, slotId: string): void {
    messagerie.chooseSlot(messageId, slotId)
  }

  function markUnread(): void {
    clearTimeout(timer)
    messagerie.markUnread(selectedId.value, viewerId())
  }

  return { unreadIds, current, currentMessages, currentWaiting, select, send, choose, markUnread }
}
