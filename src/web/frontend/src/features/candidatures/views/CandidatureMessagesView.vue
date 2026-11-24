<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import ConversationsList from '@/features/messages/components/ConversationsList.vue'
import { useConversations } from '@/features/messages/composables/useConversations'
import { pluralize } from '@/utils/format'
import { useCandidatureDetail } from '../composables/useCandidatureDetail'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'
import { formatCandidatName } from '../format'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const SKELETON_ROWS = 4

const { candidature: detail } = useCandidatureDetail(() => props.candidature)
const candidatNom = computed(() => detail.value ? formatCandidatName(detail.value.candidat) : 'le candidat')
const { names } = useCandidaturePanelRoutes()

const { conversations, count, pending, error } = useConversations(() => props.candidature)

const showSkeleton = useMinimumPending(pending)

const title = computed(() =>
  count.value > 0
    ? `${pluralize(count.value, 'Conversation')} (${count.value})`
    : 'Conversation',
)

const isEmpty = computed(() => !showSkeleton.value && !error.value && conversations.value.length === 0)

const route = useRoute()
const isConversationOpen = computed(() => route.name === names.value.conversations.conversation)
const isCreatingConversation = computed(() => route.name === names.value.conversations.create)

const router = useRouter()

function startConversation(): void {
  void router.push({
    name: names.value.conversations.create,
    params: { ...props.candidature },
  })
}
</script>

<template>
  <router-view v-if="isCreatingConversation" />
  <div
    v-else
    class="candidature-messages"
  >
    <section
      class="candidature-messages__pane candidature-messages__conversations"
      aria-label="Conversations de la candidature"
    >
      <header class="candidature-messages__header">
        <h2 class="candidature-messages__title">
          {{ title }}
        </h2>
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:mail-add-line"
          aria-label="Démarrer une conversation"
          @click="startConversation"
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
          <ConversationsList
            :routes="names.conversations"
            :skeleton-rows="SKELETON_ROWS"
          />
        </template>

        <p
          v-if="conversations.length === 0"
          class="candidature-messages__none"
        >
          Aucune conversation pour le moment
        </p>
        <ConversationsList
          v-else
          :routes="names.conversations"
          :conversations="conversations"
        />
      </CspAsyncSection>
    </section>

    <section
      class="candidature-messages__pane candidature-messages__thread"
      aria-label="Fil de discussion"
    >
      <CspEmptyState
        v-if="isEmpty"
        icon="ri:mail-close-line"
        title="Aucune conversation pour le moment"
        :description="`Créer une conversation pour échanger avec ${candidatNom}`"
      >
        <template #action>
          <CspButton
            variant="secondary"
            icon="ri:mail-add-line"
            label="Démarrer une conversation"
            @click="startConversation"
          />
        </template>
      </CspEmptyState>
      <router-view v-else-if="isConversationOpen" />
      <CspEmptyState
        v-else-if="!showSkeleton && !error"
        icon="ri:chat-3-line"
        title="Sélectionnez une conversation"
        :description="`Choisissez une conversation pour lire les messages échangés avec ${candidatNom}.`"
      />
    </section>
  </div>
</template>

<style scoped lang="scss">
.candidature-messages {
  display: grid;
  flex: 1;
  grid-template-columns: minmax(0, 22rem) minmax(0, 1fr);
  min-height: 0;
  border: 1px solid var(--csp-surface-border-color);
  border-radius: var(--csp-surface-radius);
}

.candidature-messages__pane {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
}

.candidature-messages__conversations {
  border-right: 1px solid var(--csp-divider-color);
}

.candidature-messages__thread {
  justify-content: center;
}

.candidature-messages__thread:has(.conversation-thread) {
  justify-content: flex-start;
  overflow: hidden;
}

.candidature-messages__header {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
  padding: var(--csp-space-3) var(--csp-space-4);
}

.candidature-messages__title {
  margin: 0;
  font-size: 1rem;
  font-weight: 400;
}

.candidature-messages__none {
  margin: 0;
  padding: 0 var(--csp-space-4);
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  font-weight: 700;
}

@container panel (max-width: 48rem) {
  .candidature-messages {
    grid-template-columns: minmax(0, 1fr);
  }

  .candidature-messages__conversations {
    border-right: 0;
    border-bottom: 1px solid var(--csp-divider-color);
  }
}
</style>
