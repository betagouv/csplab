<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import { computed, ref, watch } from 'vue'
import { ValidationError } from '@/api/errors'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'
import { useToast } from '@/composables/ui/useToast'
import { hasInvalidAttachment } from '../attachments'
import { useReplyConversation } from '../composables/useConversationMessages'
import { MESSAGE_CONTENT_MAX_LENGTH } from '../constants/message'
import MessageAttachments from './MessageAttachments.vue'

const props = defineProps<{
  candidature: CandidatureParams
  conversationUuid: string
}>()

const { reply, replying } = useReplyConversation(() => ({
  ...props.candidature,
  conversationUuid: props.conversationUuid,
}))
const { addToast } = useToast()

const content = ref('')
const documents = ref<File[]>([])

useUnsavedChanges(() => content.value !== '' || documents.value.length > 0, () => {
  content.value = ''
  documents.value = []
})

const contentErrors = ref<string[]>([])
const documentsErrors = ref<string[]>([])

watch(content, () => {
  contentErrors.value = []
})
watch(documents, () => {
  documentsErrors.value = []
})

const canSend = computed(() => content.value.trim() !== '' && !hasInvalidAttachment(documents.value) && !replying.value)

async function send(): Promise<void> {
  if (!canSend.value) {
    return
  }
  try {
    await reply({ content: content.value, documents: documents.value })
    content.value = ''
    documents.value = []
    addToast({ variant: 'success', title: 'Message envoyé' })
  }
  catch (sendError) {
    if (sendError instanceof ValidationError && (sendError.fieldErrors.content || sendError.fieldErrors.documents)) {
      contentErrors.value = sendError.fieldErrors.content ?? []
      documentsErrors.value = sendError.fieldErrors.documents ?? []
      return
    }
    addToast({ variant: 'error', title: 'L\'envoi du message a échoué' })
  }
}
</script>

<template>
  <form
    class="message-composer"
    @submit.prevent="send"
  >
    <CspTextarea
      v-model="content"
      :rows="3"
      :readonly="replying"
      :maxlength="MESSAGE_CONTENT_MAX_LENGTH"
      resize="none"
      placeholder="Écrivez votre message…"
      aria-label="Écrivez votre message"
      :error="contentErrors.length > 0"
      :error-message="contentErrors.join(' ')"
      class="message-composer__field"
    />
    <MessageAttachments
      v-model="documents"
      :disabled="replying"
      :server-errors="documentsErrors"
    >
      <CspButton
        type="submit"
        icon="ri:send-plane-fill"
        is-icon-left
        label="Envoyer"
        :disabled="!canSend"
      />
    </MessageAttachments>
  </form>
</template>

<style scoped lang="scss">
.message-composer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  padding: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}
</style>
