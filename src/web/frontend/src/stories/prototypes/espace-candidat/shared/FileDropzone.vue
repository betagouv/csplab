<script setup lang="ts">
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  label?: string
  hint?: string
  fileName?: string | null
}>(), {
  label: 'Déposez votre CV, ou',
  hint: 'PDF, jusqu\'à 5 Mo',
  fileName: null,
})

const emit = defineEmits<{
  select: [fileName: string]
  remove: []
}>()

const isDragOver = ref(false)
const inputRef = ref<HTMLInputElement>()

function onDrop(event: DragEvent) {
  isDragOver.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    emit('select', file.name)
  }
}

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    emit('select', file.name)
  }
}

function openPicker() {
  inputRef.value?.click()
}
</script>

<template>
  <div
    v-if="!fileName"
    class="dropzone"
    :class="{ 'dropzone--over': isDragOver }"
    @dragover.prevent="isDragOver = true"
    @dragleave.prevent="isDragOver = false"
    @drop.prevent="onDrop"
  >
    <CspIcon
      name="ri:upload-cloud-2-line"
      :size="28"
      class="dropzone__icon"
    />
    <p class="dropzone__label">
      {{ label }}
      <button
        type="button"
        class="dropzone__browse"
        @click="openPicker"
      >
        parcourez vos fichiers
      </button>
    </p>
    <p class="dropzone__hint">
      {{ hint }}
    </p>
    <input
      ref="inputRef"
      type="file"
      class="dropzone__input"
      accept=".pdf"
      @change="onFileChange"
    >
  </div>

  <div
    v-else
    class="dropzone-file"
  >
    <CspIcon
      name="ri:file-text-line"
      :size="20"
      class="dropzone-file__icon"
    />
    <span class="dropzone-file__name">{{ fileName }}</span>
    <CspButton
      variant="tertiary-no-outline"
      size="sm"
      icon="ri:close-line"
      label="Retirer le fichier"
      class="dropzone-file__remove"
      @click="$emit('remove')"
    />
  </div>
</template>

<style scoped lang="scss">
.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-6);
  border: 1px dashed var(--border-default-grey);
  border-radius: 0.25rem;
  background-color: var(--background-alt-grey);
  text-align: center;

  &--over {
    border-color: var(--border-plain-blue-france);
    background-color: var(--background-alt-blue-france);
  }
}

.dropzone__icon {
  color: var(--text-mention-grey);
}

.dropzone__label {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
}

.dropzone__browse {
  border: none;
  background: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
}

.dropzone__hint {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.dropzone__input {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  opacity: 0;
}

.dropzone-file {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.dropzone-file__icon {
  color: var(--text-action-high-blue-france);
  flex-shrink: 0;
}

.dropzone-file__name {
  flex: 1;
  min-width: 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-default-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropzone-file__remove {
  flex-shrink: 0;
}
</style>
