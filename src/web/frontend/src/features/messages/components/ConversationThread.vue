<script setup lang="ts">
import type { CandidatureParams } from '@/features/candidatures/types'
import { useTemplateRef, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatFileSize } from '@/features/candidatures/utils/file'
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

const messagesSection = useTemplateRef('messagesSection')

watch(
  () => [props.conversationUuid, messages.value.length, showSkeleton.value],
  () => {
    const container = messagesSection.value?.$el as HTMLElement | undefined
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  },
  { flush: 'post' },
)
</script>

<template>
  <div class="conversation-thread">
    <CspAsyncSection
      ref="messagesSection"
      :pending="showSkeleton"
      :error="error"
      fill
      loading-label="Chargement des messages"
      error-title="Impossible de charger les messages"
      class="conversation-thread__messages"
    >
      <template #skeleton>
        <div
          class="conversation-thread__list"
          aria-hidden="true"
        >
          <div
            v-for="row in SKELETON_ROWS"
            :key="row"
          >
            <div class="conversation-thread__meta">
              <CspSkeleton
                width="8rem"
                variant="text"
              />
              <CspSkeleton
                width="7rem"
                variant="text"
                class="conversation-thread__date"
              />
            </div>
            <div class="conversation-thread__body">
              <CspSkeleton
                width="75%"
                variant="text"
              />
            </div>
          </div>
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
          <ul
            v-if="message.documents.length > 0"
            class="conversation-thread__documents"
            aria-label="Pièces jointes"
          >
            <li
              v-for="document in message.documents"
              :key="document.uuid"
              class="conversation-thread__document"
            >
              <CspIcon
                name="ri:file-text-fill"
                :size="16"
                aria-hidden="true"
              />
              <span class="conversation-thread__document-name">{{ document.nom }}</span>
              <span class="conversation-thread__document-size">{{ formatFileSize(document.taille) }}</span>
              <CspButton
                variant="tertiary-no-outline"
                size="sm"
                label="Ouvrir"
                :aria-label="`Ouvrir ${document.nom}`"
                disabled
                class="conversation-thread__document-open"
              />
            </li>
          </ul>
          <p class="conversation-thread__body">
            {{ message.content }}
          </p>
        </li>
      </ol>
    </CspAsyncSection>

    <MessageComposer
      :key="conversationUuid"
      :candidature="candidature"
      :conversation-uuid="conversationUuid"
    />
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

  :deep(.csp-skeleton) {
    background: var(--background-contrast-grey);
  }
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

.conversation-thread__documents {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4) 0;
  list-style: none;
}

.conversation-thread__document {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  padding: var(--csp-space-2) var(--csp-space-4);
  border-left: 2px solid var(--border-default-grey);
}

.conversation-thread__document-name {
  overflow: hidden;
  min-width: 0;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-thread__document-size {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.conversation-thread__document-open {
  flex-shrink: 0;
  margin-left: auto;
}
</style>
