<script setup lang="ts">
import type { CandidatureParams } from '@/features/candidatures/types'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatDateTime } from '@/utils/date'
import { useConversationMessages } from '../composables/useConversationMessages'
import MessageComposer from './MessageComposer.vue'

const props = defineProps<{
  candidature: CandidatureParams
  conversationUuid: string
}>()

const SKELETON_ROWS = 3

const { messages, pending, error } = useConversationMessages(() => ({
  candidature: props.candidature,
  conversationUuid: props.conversationUuid,
}))

const showSkeleton = useMinimumPending(pending)
</script>

<template>
  <div class="conversation-thread">
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      fill
      loading-label="Chargement des messages"
      error-title="Impossible de charger les messages"
      class="conversation-thread__messages"
    >
      <template #skeleton>
        <div class="conversation-thread__skeleton">
          <CspSkeleton
            v-for="row in SKELETON_ROWS"
            :key="row"
            height="6rem"
          />
        </div>
      </template>

      <ol class="conversation-thread__list">
        <li
          v-for="message in messages"
          :key="`${message.author}-${message.created_at}`"
        >
          <div class="conversation-thread__meta">
            <span class="conversation-thread__author">{{ message.author }}</span>
            <span class="conversation-thread__date">le {{ formatDateTime(message.created_at) }}</span>
          </div>
          <p class="conversation-thread__body">
            {{ message.content }}
          </p>
        </li>
      </ol>
    </CspAsyncSection>

    <MessageComposer />
  </div>
</template>

<style scoped lang="scss">
.conversation-thread {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.conversation-thread__messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.conversation-thread__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin: 0;
  padding: var(--csp-space-4);
  list-style: none;
}

.conversation-thread__meta {
  display: flex;
  gap: var(--csp-space-4);
  align-items: baseline;
  justify-content: space-between;
  padding: var(--csp-space-2) var(--csp-space-4);
  background-color: var(--background-alt-grey);
}

.conversation-thread__author {
  font-weight: 700;
}

.conversation-thread__date {
  flex-shrink: 0;
  color: var(--text-mention-grey);
  font-size: 0.75rem;
}

.conversation-thread__body {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4) 0;
  white-space: pre-wrap;
}

.conversation-thread__skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4);
}
</style>
