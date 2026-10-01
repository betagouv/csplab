<script setup lang="ts">
import { ref, useTemplateRef } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { validateAttachments } from '../attachments'
import { MESSAGE_DOCUMENT_CONTENT_TYPES } from '../constants/message'

const files = defineModel<File[]>({ default: () => [] })

const errors = ref<string[]>([])
const input = useTemplateRef('input')

function pick(): void {
  input.value?.click()
}

function add(event: Event): void {
  const target = event.target as HTMLInputElement
  const { accepted, errors: rejections } = validateAttachments(files.value, [...(target.files ?? [])])
  files.value = [...files.value, ...accepted]
  errors.value = rejections
  target.value = ''
}

function remove(index: number): void {
  files.value = files.value.filter((_, position) => position !== index)
  errors.value = []
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
      v-if="files.length > 0"
      class="message-attachments__files"
      aria-label="Pièces jointes"
    >
      <li
        v-for="(file, index) in files"
        :key="`${index}-${file.name}`"
      >
        <CspTag
          variant="dismissible"
          size="sm"
          :label="file.name"
          :dismiss-label="`Retirer ${file.name}`"
          @dismiss="remove(index)"
        />
      </li>
    </ul>
    <div aria-live="polite">
      <p
        v-for="error in errors"
        :key="error"
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
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
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
