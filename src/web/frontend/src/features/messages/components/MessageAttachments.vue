<script setup lang="ts">
import { computed, useTemplateRef } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { validateAttachments } from '../attachments'
import { MESSAGE_DOCUMENT_CONTENT_TYPES } from '../constants/message'

withDefaults(defineProps<{
  disabled?: boolean
  serverErrors?: string[]
}>(), {
  serverErrors: () => [],
})

const files = defineModel<File[]>({ default: () => [] })

const attachments = computed(() => validateAttachments(files.value))
const input = useTemplateRef('input')

function pick(): void {
  input.value?.click()
}

function add(event: Event): void {
  const target = event.target as HTMLInputElement
  files.value = [...files.value, ...(target.files ?? [])]
  target.value = ''
}

function remove(index: number): void {
  files.value = files.value.filter((_, position) => position !== index)
}

defineExpose({ pick })
</script>

<template>
  <div class="message-attachments">
    <input
      ref="input"
      type="file"
      multiple
      hidden
      :accept="MESSAGE_DOCUMENT_CONTENT_TYPES.join(',')"
      @change="add"
    >
    <ul
      v-if="attachments.length > 0"
      class="message-attachments__files"
      aria-label="Pièces jointes"
      aria-live="polite"
    >
      <li
        v-for="(attachment, index) in attachments"
        :key="`${index}-${attachment.file.name}`"
        class="message-attachments__file"
      >
        <CspTag
          variant="dismissible"
          size="sm"
          :label="attachment.file.name"
          :dismiss-label="`Retirer ${attachment.file.name}`"
          :disabled="disabled"
          @dismiss="remove(index)"
        />
        <p
          v-if="attachment.error"
          class="message-attachments__error"
        >
          <CspIcon
            name="ri:error-warning-fill"
            :size="14"
          />
          {{ attachment.error }}
        </p>
      </li>
    </ul>
    <div aria-live="polite">
      <p
        v-for="(error, index) in serverErrors"
        :key="index"
        class="message-attachments__error"
      >
        <CspIcon
          name="ri:error-warning-fill"
          :size="14"
        />
        {{ error }}
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.message-attachments__files {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.message-attachments__file {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  align-items: flex-start;
}

.message-attachments__error {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  margin: 0;
  color: var(--text-default-error);
  font-size: 0.75rem;
}
</style>
