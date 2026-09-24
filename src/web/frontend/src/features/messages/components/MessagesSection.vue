<script setup lang="ts">
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useConversations } from '../composables/useConversations'
import ConversationsList from './ConversationsList.vue'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}>()

const SKELETON_ROWS = 4

const { conversations, count, pending, error } = useConversations(() => ({
  organismeUuid: props.organismeUuid,
  recrutementUuid: props.recrutementUuid,
  candidatureUuid: props.candidatureUuid,
}))

const showSkeleton = useMinimumPending(pending)
</script>

<template>
  <div class="messages-section">
    <section
      class="messages-section__pane messages-section__conversations"
      aria-label="Conversations de la candidature"
    >
      <header class="messages-section__header">
        <h2 class="messages-section__title">
          Conversations <span class="messages-section__count">({{ count }})</span>
        </h2>
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:chat-new-line"
          disabled
          aria-label="Nouvelle conversation"
        />
      </header>

      <CspAsyncSection
        :pending="showSkeleton"
        :error="error"
        fill
        loading-label="Chargement des conversations"
        error-title="Impossible de charger les conversations"
      >
        <template #skeleton>
          <div class="messages-section__skeleton">
            <CspSkeleton
              v-for="row in SKELETON_ROWS"
              :key="row"
              height="4rem"
            />
          </div>
        </template>

        <CspEmptyState
          v-if="conversations.length === 0"
          icon="ri:question-answer-line"
          title="Aucune conversation"
          description="Aucun échange n'a encore eu lieu avec ce candidat."
        />
        <ConversationsList
          v-else
          :conversations="conversations"
        />
      </CspAsyncSection>
    </section>

    <section
      class="messages-section__pane messages-section__thread"
      aria-label="Fil de discussion"
    >
      <CspEmptyState
        icon="ri:chat-3-line"
        title="Sélectionnez une conversation"
        description="Choisissez une conversation pour lire les messages échangés avec le candidat."
      />
    </section>
  </div>
</template>

<style scoped lang="scss">
.messages-section {
  display: grid;
  flex: 1;
  grid-template-columns: minmax(0, 22rem) minmax(0, 1fr);
  min-height: 0;
  border: 1px solid var(--border-default-grey);
}

.messages-section__pane {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
}

.messages-section__conversations {
  border-right: 1px solid var(--border-default-grey);
}

.messages-section__thread {
  justify-content: center;
}

.messages-section__header {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);
}

.messages-section__title {
  margin: 0;
  font-size: 1rem;
}

.messages-section__count {
  color: var(--text-mention-grey);
  font-weight: 400;
}

.messages-section__skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-4);
}

@container panel (max-width: 48rem) {
  .messages-section {
    grid-template-columns: minmax(0, 1fr);
  }

  .messages-section__conversations {
    border-right: 0;
    border-bottom: 1px solid var(--border-default-grey);
  }
}
</style>
