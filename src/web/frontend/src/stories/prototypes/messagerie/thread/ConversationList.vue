<script setup lang="ts">
import type { PersonId } from '../shared/types'
import type { ConversationSummary } from '../shared/useMessagerie'
import { useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { formatStamp } from '../shared/format'

defineProps<{
  summaries: ConversationSummary[]
  viewerId: PersonId
  selectedId: string
  unreadIds: string[]
  dates: 'relatives' | 'absolues'
  now: Date
  canCreate: boolean
}>()

const emit = defineEmits<{
  select: [id: string]
}>()

const titleId = useId()
</script>

<template>
  <nav
    class="conversation-list"
    :aria-labelledby="titleId"
  >
    <div class="conversation-list__header">
      <h3
        :id="titleId"
        class="conversation-list__title"
      >
        Conversations ({{ summaries.length }})
      </h3>
      <CspTooltip
        v-if="canCreate"
        content="Nouvelle conversation"
        side="bottom"
      >
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:chat-new-line"
          aria-label="Nouvelle conversation"
        />
      </CspTooltip>
    </div>
    <ul class="conversation-list__items">
      <li
        v-for="item in summaries"
        :key="item.id"
      >
        <button
          type="button"
          class="conversation-list__item"
          :class="{
            'conversation-list__item--current': item.id === selectedId,
            'conversation-list__item--unread': unreadIds.includes(item.id),
          }"
          :aria-current="item.id === selectedId ? 'true' : undefined"
          @click="emit('select', item.id)"
        >
          <span class="conversation-list__objet">
            <span
              v-if="unreadIds.includes(item.id)"
              class="conversation-list__dot"
              aria-hidden="true"
            />
            <span
              v-if="unreadIds.includes(item.id)"
              class="sr-only"
            >Non lue :</span>
            {{ item.objet }}
          </span>
          <span class="conversation-list__preview">{{ item.preview }}</span>
          <span class="conversation-list__meta">
            {{ item.authorId === viewerId ? 'Vous' : item.authorName }} · <span class="conversation-list__date">{{ formatStamp(item.at, now, dates) }}</span>
          </span>
        </button>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.conversation-list {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.conversation-list__header {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
  min-height: 3.5rem;
  padding: var(--csp-space-2) var(--csp-space-2) var(--csp-space-2) var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);
}

.conversation-list__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.conversation-list__items {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.conversation-list__item {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  width: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  text-align: left;
  cursor: pointer;
  background: transparent;
  border-bottom: 1px solid var(--border-default-grey);
  box-shadow: inset 3px 0 0 transparent;
}

.conversation-list__item:hover {
  background: var(--background-default-grey-hover);
}

.conversation-list__item:focus-visible {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}

.conversation-list__item--current,
.conversation-list__item--current:hover {
  background: var(--background-alt-blue-france);
  box-shadow: inset 3px 0 0 var(--border-active-blue-france);
}

.conversation-list__objet {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.conversation-list__dot {
  flex-shrink: 0;
  width: 0.5rem;
  height: 0.5rem;
  background: var(--background-action-high-blue-france);
  border-radius: 50%;
}

.conversation-list__preview {
  display: -webkit-box;
  overflow: hidden;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.conversation-list__meta {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.conversation-list__date {
  white-space: nowrap;
}
</style>
