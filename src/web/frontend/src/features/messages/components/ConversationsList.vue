<script setup lang="ts">
import type { Conversation } from '../types'
import { RouterLink, useRoute } from 'vue-router'
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

.conversations-list__item {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  width: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);
  text-align: left;
  text-decoration: none;
  color: inherit;

  &:hover {
    background-color: var(--background-alt-grey);
  }
}

.conversations-list__item[aria-current='page'] {
  background-color: var(--background-alt-blue-france);
}

.conversations-list__objet {
  font-weight: 700;
}

.conversations-list__preview {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.conversations-list__meta {
  color: var(--text-mention-grey);
  font-size: 0.75rem;
}
</style>
