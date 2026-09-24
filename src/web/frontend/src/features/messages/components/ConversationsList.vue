<script setup lang="ts">
import type { Conversation } from '../types'
import { RouterLink, useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { CANDIDATURE_CONVERSATION_ROUTE_NAME } from '@/features/candidatures/routes'
import { formatElapsedTime } from '@/utils/date'

defineProps<{
  conversations: Conversation[]
}>()

const route = useRoute()

function conversationLocation(conversationUuid: string) {
  return {
    name: CANDIDATURE_CONVERSATION_ROUTE_NAME,
    params: { ...route.params, conversationUuid },
  }
}
</script>

<template>
  <ul class="conversations-list">
    <li
      v-for="conversation in conversations"
      :key="conversation.uuid"
      class="conversations-list__row"
    >
      <RouterLink
        :to="conversationLocation(conversation.uuid)"
        class="conversations-list__item"
      >
        <span class="conversations-list__objet">{{ conversation.objet }}</span>
        <span class="conversations-list__preview">{{ conversation.last_message_content }}</span>
        <span class="conversations-list__meta">
          {{ conversation.last_message_author }} • {{ formatElapsedTime(conversation.last_message_created_at) }}
        </span>
      </RouterLink>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:more-fill"
        disabled
        class="conversations-list__actions"
        :aria-label="`Actions sur la conversation ${conversation.objet}`"
      />
    </li>
  </ul>
</template>

<style scoped lang="scss">
.conversations-list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}

.conversations-list__row {
  position: relative;
  border-bottom: 1px solid var(--border-default-grey);
}

.conversations-list__actions {
  position: absolute;
  top: var(--csp-space-2);
  right: var(--csp-space-2);
}

.conversations-list__item {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-3) var(--csp-space-4);
  padding-right: var(--csp-space-8);
  color: inherit;
  text-decoration: none;
  background-image: none;

  &:hover {
    background-color: var(--background-alt-grey);
  }
}

.conversations-list__item[aria-current='page'] {
  background-color: var(--background-open-blue-france);
  box-shadow: inset 0.25rem 0 0 var(--border-active-blue-france);
}

.conversations-list__objet {
  overflow: hidden;
  font-weight: 700;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.conversations-list__preview,
.conversations-list__meta {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.conversations-list__meta {
  color: var(--text-mention-grey);
  font-size: 0.75rem;
}
</style>
