<script setup lang="ts">
import type { ThreadProps } from '../shared/thread'
import type { Message } from '../shared/types'
import { PEOPLE } from '../data/scenario'
import { formatRelative, formatTime, fullName } from '../shared/format'
import { authorLabel, readLine, receptionLine } from '../shared/thread'
import MessageContent from './MessageContent.vue'
import MessageDocuments from './MessageDocuments.vue'
import SlotRequestBlock from './SlotRequestBlock.vue'

const props = defineProps<ThreadProps>()

const emit = defineEmits<{
  choose: [messageId: string, slotId: string]
}>()

const shortDay = new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: '2-digit' })

function footOf(message: Message): string {
  return [receptionLine(message, props), readLine(message, props)].filter(Boolean).join(' · ')
}
</script>

<template>
  <ol class="thread-pile">
    <li
      v-for="message in messages"
      :key="message.id"
      class="thread-pile__item"
    >
      <p class="thread-pile__time">
        <time
          v-if="settings.dates === 'relatives'"
          :datetime="message.createdAt"
        >{{ formatRelative(message.createdAt, now) }}</time>
        <time
          v-else
          :datetime="message.createdAt"
        >
          <span>{{ formatTime(message.createdAt) }}</span>
          <span>{{ shortDay.format(new Date(message.createdAt)) }}</span>
        </time>
      </p>
      <article
        class="thread-pile__message"
        :aria-labelledby="`${message.id}-auteur`"
      >
        <h4
          :id="`${message.id}-auteur`"
          class="thread-pile__author"
        >
          <span class="thread-pile__name">{{ authorLabel(message, viewerId, viewer).name }}</span>
          <span
            v-if="authorLabel(message, viewerId, viewer).role"
            class="thread-pile__role"
          >{{ authorLabel(message, viewerId, viewer).role }}</span>
        </h4>
        <MessageContent :content="message.content" />
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
          class="thread-pile__foot"
        >
          {{ footOf(message) }}
        </p>
      </article>
    </li>
  </ol>
</template>

<style scoped>
.thread-pile {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-8);
  padding: var(--csp-space-4);
}

.thread-pile__item {
  display: grid;
  grid-template-columns: 4.5rem minmax(0, 1fr);
  gap: var(--csp-space-4);
}

.thread-pile__time {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.thread-pile__time time {
  display: flex;
  flex-direction: column;
}

.thread-pile__message {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.thread-pile__author {
  display: flex;
  flex-wrap: wrap;
  gap: 0 var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-regular);
}

.thread-pile__name {
  font-weight: var(--csp-font-weight-bold);
}

.thread-pile__role {
  color: var(--text-mention-grey);
}

.thread-pile__foot {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
