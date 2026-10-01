<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { MESSAGE_CONTENT_MAX_LENGTH } from '../constants/message'

const content = ref('')

const canSend = computed(() => content.value.trim() !== '')
</script>

<template>
  <div class="message-composer">
    <CspTextarea
      v-model="content"
      :rows="3"
      :maxlength="MESSAGE_CONTENT_MAX_LENGTH"
      resize="none"
      placeholder="Écrivez votre message…"
      aria-label="Écrivez votre message"
      class="message-composer__field"
    />
    <div class="message-composer__actions">
      <CspButton
        variant="tertiary-no-outline"
        icon="ri:file-add-line"
        is-icon-left
        label="Pièce jointe"
        disabled
      />
      <CspButton
        icon="ri:send-plane-fill"
        is-icon-left
        label="Envoyer"
        :disabled="!canSend"
      />
    </div>
  </div>
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
