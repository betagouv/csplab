<script setup lang="ts">
import type { ThreadProps } from '../shared/thread'
import type { Message } from '../shared/types'
import { PEOPLE } from '../data/scenario'
import { formatStamp, fullName } from '../shared/format'
import { authorLabel, readLine, receptionLine, side } from '../shared/thread'
import MessageContent from './MessageContent.vue'
import MessageDocuments from './MessageDocuments.vue'
import SlotRequestBlock from './SlotRequestBlock.vue'

const props = defineProps<ThreadProps>()

const emit = defineEmits<{
  choose: [messageId: string, slotId: string]
}>()

function metaOf(message: Message): string {
  return [
    formatStamp(message.createdAt, props.now, props.settings.dates),
    receptionLine(message, props),
    readLine(message, props),
  ].filter(Boolean).join(' · ')
}
</script>

<template>
  <ol class="thread-bubbles">
    <li
      v-for="message in messages"
      :key="message.id"
      class="thread-bubbles__item"
      :class="`thread-bubbles__item--${side(message, props)}`"
    >
      <article
        class="thread-bubbles__bubble"
        :class="authorLabel(message, viewerId, viewer).isTeam ? 'thread-bubbles__bubble--team' : 'thread-bubbles__bubble--candidate'"
        :aria-labelledby="`${message.id}-auteur`"
      >
        <h4
          :id="`${message.id}-auteur`"
          class="thread-bubbles__author"
        >
          <span class="thread-bubbles__name">{{ authorLabel(message, viewerId, viewer).name }}</span>
          <span
            v-if="authorLabel(message, viewerId, viewer).role"
            class="thread-bubbles__role"
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
      </article>
      <p class="thread-bubbles__meta">
        <time :datetime="message.createdAt">{{ metaOf(message) }}</time>
      </p>
    </li>
  </ol>
</template>

<style scoped>
.thread-bubbles {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  padding: var(--csp-space-4);
  container: bubbles / inline-size;
}

.thread-bubbles__item {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  max-width: 80%;
}

.thread-bubbles__item--left {
  align-self: flex-start;
}

.thread-bubbles__item--right {
  align-items: flex-end;
  align-self: flex-end;
}

@container bubbles (max-width: 26rem) {
  .thread-bubbles__item {
    max-width: 100%;
  }
}

.thread-bubbles__bubble {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
}

.thread-bubbles__bubble--team {
  background: var(--background-alt-blue-france);
}

.thread-bubbles__bubble--candidate {
  background: var(--background-contrast-grey);
}

.thread-bubbles__author {
  display: flex;
  flex-wrap: wrap;
  gap: 0 var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-default-grey);
}

.thread-bubbles__name {
  font-weight: var(--csp-font-weight-bold);
}

.thread-bubbles__role {
  color: var(--text-mention-grey);
}

.thread-bubbles__meta {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
