<script setup lang="ts">
import type { PersonId, Settings } from '../shared/types'
import type { Messagerie } from '../shared/useMessagerie'
import { useMessagesView } from '../shared/useMessagesView'
import ConversationThread from '../thread/ConversationThread.vue'

const props = defineProps<{
  label: string
  messagerie: Messagerie
  viewerId: Extract<PersonId, 'jean-marc' | 'karim'>
  settings: Settings
}>()

const view = useMessagesView(props.messagerie, () => props.viewerId)
</script>

<template>
  <section class="thread-column">
    <h2 class="thread-column__label">
      {{ label }}
    </h2>
    <div class="thread-column__frame">
      <ConversationThread
        v-if="view.current.value"
        :conversation="view.current.value"
        :messages="view.currentMessages.value"
        :viewer-id="viewerId"
        viewer="recruteur"
        :settings="settings"
        :now="messagerie.clock.value"
        :waiting="view.currentWaiting.value"
        @send="view.send"
        @choose="view.choose"
        @mark-unread="view.markUnread"
      />
    </div>
  </section>
</template>

<style scoped>
.thread-column {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  gap: var(--csp-space-2);
  width: 30.5rem;
}

.thread-column__label {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
}

.thread-column__frame {
  height: var(--thread-column-height, 46rem);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
}
</style>
