<script setup lang="ts">
import type { CspFileListItem } from '@/components/base/CspFileList/CspFileList.vue'
import { computed, useTemplateRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspFileList from '@/components/base/CspFileList/CspFileList.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { countValidAttachments, validateAttachments } from '../attachments'
import { MESSAGE_DOCUMENT_CONTENT_TYPES, MESSAGE_MAX_DOCUMENTS } from '../constants/message'

const props = withDefaults(defineProps<{
  disabled?: boolean
  serverErrors?: string[]
}>(), {
  serverErrors: () => [],
})

const files = defineModel<File[]>({ default: () => [] })

const items = computed<CspFileListItem[]>(() =>
  validateAttachments(files.value).map(({ file, error }, index) => ({
    key: String(index),
    name: file.name,
    size: file.size,
    error: error ?? undefined,
  })),
)

const canAttach = computed(() => countValidAttachments(files.value) < MESSAGE_MAX_DOCUMENTS && !props.disabled)

const input = useTemplateRef('input')
const attachButton = useTemplateRef('attachButton')

function pick(): void {
  input.value?.click()
}

function add(event: Event): void {
  const target = event.target as HTMLInputElement
  files.value = [...files.value, ...(target.files ?? [])]
  target.value = ''
}

function remove(key: string): void {
  const remaining = files.value.filter((_, position) => position !== Number(key))
  files.value = remaining
  if (remaining.length === 0) {
    attachButton.value?.$el.focus()
  }
}
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
    <div>
      <CspFileList
        v-if="items.length > 0"
        :items="items"
        label="Pièces jointes"
        :disabled="disabled"
        @remove="remove"
      />
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
    <div class="message-attachments__actions">
      <CspButton
        ref="attachButton"
        type="button"
        variant="tertiary-no-outline"
        icon="ri:file-add-line"
        is-icon-left
        label="Pièce jointe"
        :disabled="!canAttach"
        @click="pick"
      />
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.message-attachments {
  display: contents;
}

.message-attachments__error {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  margin: 0;
  color: var(--text-default-error);
  font-size: var(--csp-font-size-xs);
}

.message-attachments__actions {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
}
</style>
