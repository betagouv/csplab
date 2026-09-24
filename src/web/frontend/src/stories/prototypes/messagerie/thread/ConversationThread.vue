<script setup lang="ts">
import type { Viewer } from '../shared/thread'
import type { Conversation, Message, PersonId, Settings, Waiting } from '../shared/types'
import { computed, nextTick, onMounted, ref, useId, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { PEOPLE } from '../data/scenario'
import { formatDay, formatDayWithYear, formatSlot, fullName } from '../shared/format'
import ReplyZone from './ReplyZone.vue'
import ThreadBubbles from './ThreadBubbles.vue'
import ThreadLetters from './ThreadLetters.vue'
import ThreadPile from './ThreadPile.vue'

const props = withDefaults(defineProps<{
  conversation: Conversation
  messages: Message[]
  viewerId: PersonId
  viewer: Viewer
  settings: Settings
  now: Date
  waiting: Waiting | null
  previousPeek?: number
}>(), {
  previousPeek: 0,
})

const emit = defineEmits<{
  send: [text: string]
  choose: [messageId: string, slotId: string]
  markUnread: []
}>()

const LAYOUTS = {
  bulles: ThreadBubbles,
  pile: ThreadPile,
  correspondance: ThreadLetters,
}

const titleId = useId()
const scroller = ref<HTMLElement | null>(null)

const ordered = computed(() =>
  props.settings.order === 'chronologique' ? props.messages : [...props.messages].reverse(),
)

const candidateName = fullName(PEOPLE.camille)

const waitingText = computed(() => {
  const waiting = props.waiting
  if (!props.settings.waitingLine || !waiting)
    return null
  const since = formatDay(waiting.since)
  if (props.viewer === 'recruteur') {
    if (waiting.kind === 'equipe')
      return `${candidateName} attend une réponse de l’équipe depuis le ${since}.`
    return waiting.deadline
      ? `En attente de la réponse de ${candidateName}, attendue avant le ${formatSlot(waiting.deadline)}.`
      : `En attente de la réponse de ${candidateName} depuis le ${since}.`
  }
  if (waiting.kind === 'equipe') {
    const delay = props.settings.indicativeDelay ? ' L’équipe répond en général sous 5 jours ouvrés.' : ''
    return `Votre message du ${since} a été transmis à l’équipe de recrutement. Un courriel vous préviendra de sa réponse.${delay}`
  }
  return waiting.deadline
    ? `L’équipe de recrutement attend votre réponse avant le ${formatSlot(waiting.deadline)}.`
    : 'L’équipe de recrutement attend votre réponse.'
})

const menuSections = computed(() => [{
  items: [{ label: 'Marquer comme non lue', icon: 'ri:mail-unread-line', onSelect: () => emit('markUnread') }],
}])

async function scrollToNewest(): Promise<void> {
  await nextTick()
  const element = scroller.value
  if (!element)
    return
  if (props.settings.order !== 'chronologique') {
    element.scrollTop = 0
    return
  }
  const newest = element.querySelector<HTMLElement>(':scope > ol > li:last-child')
  element.scrollTop = props.previousPeek && newest
    ? newest.offsetTop - props.previousPeek
    : element.scrollHeight
}

onMounted(scrollToNewest)
watch(() => [props.messages.length, props.settings.order, props.settings.presentation], scrollToNewest)
</script>

<template>
  <section
    class="conversation-thread"
    :aria-labelledby="titleId"
  >
    <header class="conversation-thread__header">
      <div class="conversation-thread__heading">
        <h3
          :id="titleId"
          class="conversation-thread__title"
        >
          {{ conversation.objet }}
        </h3>
        <p class="conversation-thread__origin">
          Conversation créée par {{ fullName(PEOPLE[conversation.createdBy]) }} le {{ formatDayWithYear(conversation.createdAt) }}
        </p>
      </div>
      <CspDropdownMenu
        v-if="viewer === 'recruteur'"
        :sections="menuSections"
        align="end"
        side="bottom"
      >
        <template #trigger>
          <CspButton
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:more-fill"
            aria-label="Actions sur la conversation"
          />
        </template>
      </CspDropdownMenu>
    </header>

    <ReplyZone
      v-if="settings.order === 'recent-en-haut'"
      :mode="settings.composer"
      :button-label="viewer === 'candidat' ? 'Répondre à l’équipe' : 'Répondre'"
      class="conversation-thread__reply conversation-thread__reply--top"
      @send="text => emit('send', text)"
    />

    <div
      ref="scroller"
      class="conversation-thread__scroll"
    >
      <p
        v-if="waitingText && settings.order === 'recent-en-haut'"
        class="conversation-thread__waiting"
      >
        <CspIcon
          name="ri:time-line"
          :size="16"
        />
        {{ waitingText }}
      </p>
      <component
        :is="LAYOUTS[settings.presentation]"
        :messages="ordered"
        :viewer-id="viewerId"
        :viewer="viewer"
        :settings="settings"
        :now="now"
        @choose="(messageId: string, slotId: string) => emit('choose', messageId, slotId)"
      />
      <p
        v-if="waitingText && settings.order === 'chronologique'"
        class="conversation-thread__waiting"
      >
        <CspIcon
          name="ri:time-line"
          :size="16"
        />
        {{ waitingText }}
      </p>
    </div>

    <ReplyZone
      v-if="settings.order === 'chronologique'"
      :mode="settings.composer"
      :button-label="viewer === 'candidat' ? 'Répondre à l’équipe' : 'Répondre'"
      class="conversation-thread__reply"
      @send="text => emit('send', text)"
    />
  </section>
</template>

<style scoped>
.conversation-thread {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  height: 100%;
}

.conversation-thread__header {
  display: flex;
  gap: var(--csp-space-4);
  align-items: flex-start;
  justify-content: space-between;
  padding: var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);
}

.conversation-thread__heading {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.conversation-thread__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  line-height: var(--csp-line-height-tight);
  color: var(--text-title-grey);
}

.conversation-thread__origin {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.conversation-thread__scroll {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.conversation-thread__waiting {
  display: flex;
  gap: var(--csp-space-2);
  align-items: flex-start;
  margin: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-4);
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-info);
  background: var(--background-contrast-info);
}

.conversation-thread__waiting :deep(svg) {
  flex-shrink: 0;
  margin-top: 0.15em;
}

.conversation-thread__reply--top {
  border-bottom: 1px solid var(--border-default-grey);
}
</style>
