<script setup lang="ts">
import type { ConversationMessagesParams } from '../queries'
import { computed, ref, useTemplateRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'
import { useToast } from '@/composables/ui/useToast'
import { useReplyConversation } from '../composables/useConversationMessages'
import { MESSAGE_CONTENT_MAX_LENGTH, MESSAGE_MAX_DOCUMENTS } from '../constants/message'
import MessageAttachments from './MessageAttachments.vue'

const props = defineProps<ConversationMessagesParams>()

const { reply, replying } = useReplyConversation(() => ({
  candidature: props.candidature,
  conversationUuid: props.conversationUuid,
}))
const { addToast } = useToast()

const content = ref('')
const documents = ref<File[]>([])
const attachments = useTemplateRef('attachments')

useUnsavedChanges(() => content.value !== '' || documents.value.length > 0, () => {
  content.value = ''
  documents.value = []
}, {
  isLeftBy: (to, from) => to.params.conversationUuid !== from.params.conversationUuid,
})

const canSend = computed(() => content.value.trim() !== '' && !replying.value)

const canAttach = computed(() => documents.value.length < MESSAGE_MAX_DOCUMENTS && !replying.value)

async function send(): Promise<void> {
  if (!canSend.value)
    return
  try {
    await reply({ content: content.value })
    content.value = ''
  }
  catch {
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
      class="message-composer__field"
    />
    <MessageAttachments
      ref="attachments"
      v-model="documents"
    />
    <div class="message-composer__actions">
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

.message-composer__actions {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
}
</style>
