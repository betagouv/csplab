<script setup lang="ts">
import { computed, nextTick, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const props = defineProps<{
  mode: 'ouverte' | 'bouton'
  buttonLabel: string
}>()

const emit = defineEmits<{
  send: [text: string]
}>()

const TOOLS = [
  { icon: 'ri:bold', label: 'Gras' },
  { icon: 'ri:italic', label: 'Italique' },
  { icon: 'ri:list-unordered', label: 'Liste à puces' },
  { icon: 'ri:list-ordered', label: 'Liste numérotée' },
  { icon: 'ri:double-quotes-l', label: 'Citation' },
]

const textareaId = useId()
const opened = ref(false)
const text = ref('')

const isOpen = computed(() => props.mode === 'ouverte' || opened.value)

async function open(): Promise<void> {
  opened.value = true
  await nextTick()
  document.getElementById(textareaId)?.focus()
}

function cancel(): void {
  text.value = ''
  opened.value = false
}

function submit(): void {
  const value = text.value.trim()
  if (!value)
    return
  emit('send', value)
  text.value = ''
  opened.value = false
}
</script>

<template>
  <div
    class="reply-zone"
    :class="`reply-zone--${mode}`"
  >
    <div
      v-if="!isOpen"
      class="reply-zone__trigger"
    >
      <CspButton
        variant="secondary"
        :label="buttonLabel"
        icon="ri:reply-line"
        is-icon-left
        @click="open"
      />
    </div>
    <form
      v-else
      class="reply-zone__form"
      @submit.prevent="submit"
    >
      <div class="reply-zone__editor">
        <div
          class="reply-zone__toolbar"
          role="toolbar"
          aria-label="Mise en forme"
        >
          <CspButton
            v-for="tool in TOOLS"
            :key="tool.icon"
            type="button"
            variant="tertiary-no-outline"
            size="sm"
            :icon="tool.icon"
            :aria-label="tool.label"
          />
        </div>
        <CspTextarea
          :id="textareaId"
          v-model="text"
          :rows="mode === 'ouverte' ? 2 : 6"
          placeholder="Écrivez votre message…"
          aria-label="Votre message"
        />
      </div>
      <div class="reply-zone__actions">
        <CspButton
          type="button"
          variant="tertiary-no-outline"
          label="Pièce jointe"
          icon="ri:attachment-2"
          is-icon-left
        />
        <span class="reply-zone__spacer" />
        <CspButton
          v-if="mode === 'bouton'"
          type="button"
          variant="secondary"
          label="Annuler"
          @click="cancel"
        />
        <CspButton
          type="submit"
          label="Envoyer"
          icon="ri:send-plane-fill"
          is-icon-left
          :disabled="!text.trim()"
        />
      </div>
    </form>
  </div>
</template>

<style scoped>
.reply-zone {
  padding: var(--csp-space-4);
  background: var(--background-default-grey);
}

.reply-zone--ouverte {
  border-top: 1px solid var(--border-default-grey);
}

.reply-zone__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.reply-zone__editor {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
}

.reply-zone__editor:focus-within {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: var(--csp-focus-ring-offset);
}

.reply-zone__editor :deep(.csp-textarea) {
  box-shadow: none;
}

.reply-zone__editor :deep(.csp-textarea:focus-visible) {
  outline: 0;
}

.reply-zone__toolbar {
  display: flex;
  gap: var(--csp-space-1);
  padding: var(--csp-space-1) var(--csp-space-2);
  background: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.reply-zone__actions {
  display: flex;
  gap: var(--csp-space-3);
  align-items: center;
}

.reply-zone__spacer {
  flex: 1;
}
</style>
