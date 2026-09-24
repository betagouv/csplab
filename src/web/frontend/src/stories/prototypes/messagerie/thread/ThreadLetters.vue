<script setup lang="ts">
import type { ThreadProps } from '../shared/thread'
import type { Message } from '../shared/types'
import { ref, watch } from 'vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { PEOPLE } from '../data/scenario'
import { formatStamp, fullName } from '../shared/format'
import { authorLabel, readLine, receptionLine } from '../shared/thread'
import MessageContent from './MessageContent.vue'
import MessageDocuments from './MessageDocuments.vue'
import SlotRequestBlock from './SlotRequestBlock.vue'

const props = defineProps<ThreadProps>()

const emit = defineEmits<{
  choose: [messageId: string, slotId: string]
}>()

function isUnreadForViewer(message: Message): boolean {
  const authorIsTeam = PEOPLE[message.authorId].equipe
  return props.viewer === 'recruteur'
    ? !authorIsTeam && !message.readByTeam[props.viewerId]
    : authorIsTeam && !message.readByCandidateAt
}

function newest(): Message | undefined {
  return props.settings.order === 'chronologique' ? props.messages.at(-1) : props.messages[0]
}

const expanded = ref(new Set<string>(
  props.messages.filter(isUnreadForViewer).map(message => message.id),
))

watch(() => newest()?.id, (id) => {
  if (id)
    expanded.value.add(id)
}, { immediate: true })

function toggle(id: string): void {
  if (expanded.value.has(id))
    expanded.value.delete(id)
  else
    expanded.value.add(id)
}

function snippet(message: Message): string {
  return message.content
    .map(block => block.type === 'p' ? block.text : block.items.join(' '))
    .join(' ')
    .replace(/\s+/g, ' ')
}

function footOf(message: Message): string {
  return [receptionLine(message, props), readLine(message, props)].filter(Boolean).join(' · ')
}
</script>

<template>
  <ol class="thread-letters">
    <li
      v-for="message in messages"
      :key="message.id"
      class="thread-letters__item"
      :class="{
        'thread-letters__item--candidate': !authorLabel(message, viewerId, viewer).isTeam,
        'thread-letters__item--collapsed': !expanded.has(message.id),
      }"
    >
      <article :aria-labelledby="`${message.id}-auteur`">
        <h4 class="thread-letters__heading">
          <button
            :id="`${message.id}-auteur`"
            type="button"
            class="thread-letters__toggle"
            :aria-expanded="expanded.has(message.id)"
            @click="toggle(message.id)"
          >
            <span
              class="thread-letters__avatar"
              aria-hidden="true"
            >
              <CspAvatar
                :name="fullName(PEOPLE[message.authorId])"
                size="sm"
              />
            </span>
            <span class="thread-letters__who">
              <span class="thread-letters__name">{{ authorLabel(message, viewerId, viewer).name }}</span>
              <span
                v-if="authorLabel(message, viewerId, viewer).role"
                class="thread-letters__role"
              >{{ authorLabel(message, viewerId, viewer).role }}</span>
            </span>
            <span
              v-if="!expanded.has(message.id)"
              class="thread-letters__snippet"
            >{{ snippet(message) }}</span>
            <span class="thread-letters__date">
              <CspIcon
                v-if="message.documents.length && !expanded.has(message.id)"
                name="ri:attachment-2"
                :size="14"
              />
              <time :datetime="message.createdAt">{{ formatStamp(message.createdAt, now, settings.dates) }}</time>
            </span>
          </button>
        </h4>
        <div
          v-if="expanded.has(message.id)"
          class="thread-letters__body"
        >
          <MessageContent
            :content="message.content"
            class="thread-letters__content"
          />
          <SlotRequestBlock
            v-if="message.slotRequest"
            :request="message.slotRequest"
            :viewer="viewer"
            :candidate-name="fullName(PEOPLE.camille)"
            @choose="slotId => emit('choose', message.id, slotId)"
          />
          <MessageDocuments
            v-if="message.documents.length"
            :documents="message.documents"
          />
          <p
            v-if="footOf(message)"
            class="thread-letters__foot"
          >
            <CspIcon
              :name="readLine(message, props) ? 'ri:check-double-line' : 'ri:check-line'"
              :size="14"
            />
            {{ footOf(message) }}
          </p>
        </div>
      </article>
    </li>
  </ol>
</template>

<style scoped>
.thread-letters {
  display: flex;
  flex-direction: column;
  container: letters / inline-size;
}

.thread-letters__item {
  border-bottom: 1px solid var(--border-default-grey);
}

.thread-letters__item--candidate {
  background: var(--background-alt-grey);
}

.thread-letters__heading {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-regular);
}

.thread-letters__toggle {
  display: grid;
  grid-template-areas:
    'avatar who date'
    'avatar snippet snippet';
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 0 var(--csp-space-3);
  align-items: start;
  width: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  text-align: left;
  cursor: pointer;
  background: transparent;
}

.thread-letters__item:not(.thread-letters__item--collapsed) .thread-letters__toggle {
  padding-bottom: var(--csp-space-2);
}

.thread-letters__toggle:hover {
  background: var(--background-default-grey-hover);
}

.thread-letters__item--candidate .thread-letters__toggle:hover {
  background: var(--background-alt-grey-hover);
}

.thread-letters__toggle:focus-visible {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}

.thread-letters__avatar {
  grid-area: avatar;
}

.thread-letters__who {
  display: flex;
  flex-wrap: wrap;
  grid-area: who;
  gap: 0 var(--csp-space-2);
}

.thread-letters__name {
  font-weight: var(--csp-font-weight-bold);
}

.thread-letters__role {
  color: var(--text-mention-grey);
}

.thread-letters__snippet {
  grid-area: snippet;
  overflow: hidden;
  color: var(--text-mention-grey);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.thread-letters__date {
  display: inline-flex;
  grid-area: date;
  gap: var(--csp-space-1);
  align-items: center;
  padding-top: 0.1em;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.thread-letters__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: 0 var(--csp-space-4) var(--csp-space-5) calc(var(--csp-space-4) + 1.5rem + var(--csp-space-3));
}

.thread-letters__content {
  max-inline-size: 28rem;
}

.thread-letters__foot {
  display: flex;
  gap: var(--csp-space-1);
  align-items: center;
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
@container letters (max-width: 26rem) {
  .thread-letters__toggle {
    grid-template-areas:
      'avatar who'
      'avatar date'
      'avatar snippet';
    grid-template-columns: auto minmax(0, 1fr);
  }

  .thread-letters__body {
    padding-left: var(--csp-space-4);
  }
}
</style>
