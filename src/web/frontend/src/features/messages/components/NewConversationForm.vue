<script setup lang="ts">
import type { CandidatureParams } from '@/features/candidatures/types'
import { computed, onMounted, ref, useId, useTemplateRef, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ValidationError } from '@/api/errors'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'
import { useToast } from '@/composables/ui/useToast'
import { CANDIDATURE_CONVERSATION_ROUTE_NAME, CANDIDATURE_NEW_CONVERSATION_ROUTE_NAME, CANDIDATURE_PANEL_TAB_ROUTE_NAMES } from '@/features/candidatures/routes'
import { countValidAttachments, hasInvalidAttachment } from '../attachments'
import { useCreateConversation } from '../composables/useConversations'
import { CONVERSATION_OBJET_MAX_LENGTH, MESSAGE_CONTENT_MAX_LENGTH, MESSAGE_MAX_DOCUMENTS } from '../constants/message'
import MessageAttachments from './MessageAttachments.vue'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const route = useRoute()
const router = useRouter()
const { create, creating } = useCreateConversation(() => props.candidature)
const { addToast } = useToast()

const objet = ref('')
const content = ref('')
const documents = ref<File[]>([])
const attachments = useTemplateRef('attachments')
const titleId = useId()
const objetId = useId()

onMounted(() => document.getElementById(objetId)?.focus())

const objetErrors = ref<string[]>([])
const contentErrors = ref<string[]>([])
const documentsErrors = ref<string[]>([])

watch(objet, () => {
  objetErrors.value = []
})
watch(content, () => {
  contentErrors.value = []
})
watch(documents, () => {
  documentsErrors.value = []
})

function discard(): void {
  objet.value = ''
  content.value = ''
  documents.value = []
}

useUnsavedChanges(
  () => objet.value !== '' || content.value !== '' || documents.value.length > 0,
  discard,
  { isLeftBy: to => to.name !== CANDIDATURE_NEW_CONVERSATION_ROUTE_NAME },
)

const canSend = computed(() =>
  objet.value.trim() !== ''
  && content.value.trim() !== ''
  && !hasInvalidAttachment(documents.value)
  && !creating.value,
)

const canAttach = computed(() => countValidAttachments(documents.value) < MESSAGE_MAX_DOCUMENTS && !creating.value)

function backToConversations(): void {
  void router.push({ name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.messages, params: route.params })
}

async function send(): Promise<void> {
  if (!canSend.value)
    return
  try {
    const conversation = await create({ objet: objet.value, content: content.value, documents: documents.value })
    discard()
    void router.push({
      name: CANDIDATURE_CONVERSATION_ROUTE_NAME,
      params: { ...route.params, conversationUuid: conversation.uuid },
    })
  }
  catch (sendError) {
    const fieldErrors = sendError instanceof ValidationError ? sendError.fieldErrors : {}
    if (fieldErrors.objet || fieldErrors.content || fieldErrors.documents) {
      objetErrors.value = fieldErrors.objet ?? []
      contentErrors.value = fieldErrors.content ?? []
      documentsErrors.value = fieldErrors.documents ?? []
      return
    }
    addToast({ variant: 'error', title: 'La création de la conversation a échoué' })
  }
}
</script>

<template>
  <section
    class="new-conversation"
    :aria-labelledby="titleId"
  >
    <header class="new-conversation__header">
      <div>
        <h2
          :id="titleId"
          class="new-conversation__title"
        >
          Créer une nouvelle conversation
        </h2>
        <p class="new-conversation__description">
          Les conversations permettent d'organiser les échanges avec le candidat par sujet.
          Choisissez un objet pour cette nouvelle conversation. Vous pourrez ensuite rédiger votre premier message.
        </p>
      </div>
      <CspButton
        variant="secondary"
        size="sm"
        label="Annuler"
        @click="backToConversations"
      />
    </header>

    <form
      class="new-conversation__form"
      @submit.prevent="send"
    >
      <CspInput
        :id="objetId"
        v-model="objet"
        label="Sujet de la conversation"
        hint="L'objet ne pourra plus être modifié après la création de la conversation."
        :maxlength="CONVERSATION_OBJET_MAX_LENGTH"
        :readonly="creating"
        :error="objetErrors.length > 0"
        :error-message="objetErrors.join(' ')"
        class="new-conversation__objet"
      />

      <div class="new-conversation__message">
        <CspTextarea
          v-model="content"
          :rows="10"
          :maxlength="MESSAGE_CONTENT_MAX_LENGTH"
          :readonly="creating"
          resize="none"
          placeholder="Écrivez votre message…"
          aria-label="Écrivez votre message"
          :error="contentErrors.length > 0"
          :error-message="contentErrors.join(' ')"
        />
        <MessageAttachments
          ref="attachments"
          v-model="documents"
          :disabled="creating"
          :server-errors="documentsErrors"
        />
        <div class="new-conversation__actions">
          <CspButton
            type="button"
            variant="tertiary-no-outline"
            icon="ri:file-add-line"
            is-icon-left
            label="Pièce jointe"
            :disabled="!canAttach"
            @click="attachments?.pick()"
          />
          <CspButton
            type="submit"
            icon="ri:send-plane-fill"
            is-icon-left
            label="Envoyer"
            :disabled="!canSend"
          />
        </div>
      </div>
    </form>
  </section>
</template>

<style scoped lang="scss">
.new-conversation {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
  border: 1px solid var(--border-default-grey);
}

.new-conversation__header {
  display: flex;
  gap: var(--csp-space-4);
  align-items: flex-start;
  justify-content: space-between;
  padding: var(--csp-space-5) var(--csp-space-6) 0;
}

.new-conversation__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
}

.new-conversation__description {
  max-width: 40rem;
  margin: 0;
  font-size: var(--csp-font-size-base);
}

.new-conversation__objet {
  padding: var(--csp-space-5) var(--csp-space-6);
}

.new-conversation__message {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-5) var(--csp-space-6);
  border-top: 1px solid var(--border-default-grey);
}

.new-conversation__actions {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
}
</style>
