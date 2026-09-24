import type { ScenarioKey } from '../data/scenario'
import type { Block, Conversation, Message, PersonId, Waiting } from './types'
import { computed, reactive, ref } from 'vue'
import { buildScenario, PEOPLE } from '../data/scenario'
import { formatSlot, fullName } from './format'

export interface ConversationSummary {
  id: string
  objet: string
  preview: string
  authorId: PersonId
  authorName: string
  at: string
}

function toLocalIso(date: Date): string {
  const pad = (value: number) => String(value).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}:00`
}

function textOf(content: Block[]): string {
  return content
    .map(block => block.type === 'p' ? block.text : block.items.join(' '))
    .join(' ')
    .replace(/\s+/g, ' ')
}

function isTeam(id: PersonId): boolean {
  return PEOPLE[id].equipe
}

export function useMessagerie(scenarioKey: ScenarioKey) {
  const scenario = buildScenario(scenarioKey)
  const conversations = reactive<Conversation[]>(scenario.conversations)
  const messages = reactive<Message[]>(scenario.messages)
  const clock = ref(new Date(scenario.now))
  let sentCount = 0

  function tick(): string {
    clock.value = new Date(clock.value.getTime() + 60 * 1000)
    return toLocalIso(clock.value)
  }

  function messagesOf(conversationId: string): Message[] {
    return messages
      .filter(message => message.conversationId === conversationId)
      .sort((a, b) => a.createdAt.localeCompare(b.createdAt))
  }

  function lastMessage(conversationId: string): Message | undefined {
    return messagesOf(conversationId).at(-1)
  }

  function summary(conversation: Conversation): ConversationSummary {
    const last = lastMessage(conversation.id)
    const choice = last?.slotRequest?.chosenAt && last.slotRequest.chosenSlotId
      ? last.slotRequest.slots.find(slot => slot.id === last.slotRequest?.chosenSlotId)
      : undefined
    if (last?.slotRequest?.chosenAt && choice) {
      return {
        id: conversation.id,
        objet: conversation.objet,
        preview: `Créneau retenu : ${formatSlot(choice.start)}`,
        authorId: 'camille',
        authorName: fullName(PEOPLE.camille),
        at: last.slotRequest.chosenAt,
      }
    }
    return {
      id: conversation.id,
      objet: conversation.objet,
      preview: last ? textOf(last.content) : '',
      authorId: last?.authorId ?? conversation.createdBy,
      authorName: fullName(PEOPLE[last?.authorId ?? conversation.createdBy]),
      at: last?.createdAt ?? conversation.createdAt,
    }
  }

  const summaries = computed(() =>
    conversations.map(summary).sort((a, b) => b.at.localeCompare(a.at)),
  )

  const selectedId = ref(summaries.value[0]?.id ?? '')

  function isUnread(conversationId: string, viewerId: PersonId): boolean {
    return messagesOf(conversationId).some(message => isTeam(viewerId)
      ? !isTeam(message.authorId) && !message.readByTeam[viewerId]
      : isTeam(message.authorId) && !message.readByCandidateAt)
  }

  function markRead(conversationId: string, viewerId: PersonId): void {
    const at = toLocalIso(clock.value)
    for (const message of messagesOf(conversationId)) {
      if (isTeam(viewerId) && !isTeam(message.authorId) && !message.readByTeam[viewerId])
        message.readByTeam[viewerId] = at
      if (!isTeam(viewerId) && isTeam(message.authorId) && !message.readByCandidateAt)
        message.readByCandidateAt = at
    }
  }

  function markUnread(conversationId: string, viewerId: PersonId): void {
    const received = messagesOf(conversationId).filter(message => isTeam(message.authorId) !== isTeam(viewerId))
    const last = received.at(-1)
    if (!last)
      return
    if (isTeam(viewerId))
      delete last.readByTeam[viewerId]
    else
      delete last.readByCandidateAt
  }

  function waiting(conversationId: string): Waiting | null {
    const last = lastMessage(conversationId)
    if (!last)
      return null
    if (!isTeam(last.authorId))
      return { kind: 'equipe', since: last.createdAt }
    if (last.slotRequest && !last.slotRequest.chosenSlotId)
      return { kind: 'candidat', since: last.createdAt, deadline: last.slotRequest.deadline }
    if (last.awaitsReply)
      return { kind: 'candidat', since: last.createdAt }
    return null
  }

  function send(conversationId: string, authorId: PersonId, text: string): void {
    sentCount += 1
    const content: Block[] = text
      .split(/\n{2,}/)
      .map(paragraph => paragraph.trim())
      .filter(Boolean)
      .map(paragraph => ({ type: 'p', text: paragraph }))
    messages.push({
      id: `envoi-${sentCount}`,
      conversationId,
      authorId,
      createdAt: tick(),
      content,
      documents: [],
      readByTeam: {},
    })
  }

  function chooseSlot(messageId: string, slotId: string): void {
    const message = messages.find(item => item.id === messageId)
    if (!message?.slotRequest)
      return
    message.slotRequest.chosenSlotId = slotId
    message.slotRequest.chosenAt = tick()
    message.awaitsReply = false
  }

  return {
    clock,
    selectedId,
    summaries,
    conversations,
    messagesOf,
    isUnread,
    markRead,
    markUnread,
    waiting,
    send,
    chooseSlot,
  }
}

export type Messagerie = ReturnType<typeof useMessagerie>
