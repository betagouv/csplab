<script setup lang="ts">
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  label: string
  requis?: boolean
  fileName?: string | null
  formats?: string
}>(), {
  requis: false,
  fileName: null,
  formats: 'PDF, jusqu\'à 5 Mo',
})

const emit = defineEmits<{
  select: [fileName: string]
  remove: []
}>()

const inputRef = ref<HTMLInputElement>()

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    emit('select', file.name)
  }
}

function ouvrirSelecteur() {
  inputRef.value?.click()
}
</script>

<template>
  <div class="file-field">
    <p class="file-field__label">
      {{ label }}
      <span
        v-if="requis"
        class="file-field__requis"
      >Obligatoire</span>
      <span
        v-else
        class="file-field__facultatif"
      >Facultatif</span>
    </p>

    <div
      v-if="!fileName"
      class="file-field__empty"
    >
      <CspButton
        variant="secondary"
        size="lg"
        icon="ri:upload-2-line"
        is-icon-left
        label="Ajouter un fichier"
        class="file-field__add-button"
        @click="ouvrirSelecteur"
      />
      <p class="file-field__hint">
        {{ formats }}
      </p>
    </div>

    <div
      v-else
      class="file-field__filled"
    >
      <CspIcon
        name="ri:file-text-line"
        :size="22"
        class="file-field__file-icon"
      />
      <span class="file-field__file-name">{{ fileName }}</span>
      <div class="file-field__actions">
        <CspButton
          variant="tertiary"
          size="sm"
          label="Remplacer"
          @click="ouvrirSelecteur"
        />
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:delete-bin-line"
          aria-label="Supprimer le fichier"
          @click="$emit('remove')"
        />
      </div>
    </div>

    <input
      ref="inputRef"
      type="file"
      class="file-field__input"
      accept=".pdf"
      @change="onFileChange"
    >
  </div>
</template>

<style scoped lang="scss">
.file-field {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.file-field__label {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.file-field__requis,
.file-field__facultatif {
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-mention-grey);
}

.file-field__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-5) var(--csp-space-4);
  border: 1px dashed var(--border-default-grey);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
}

.file-field__add-button {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}

.file-field__hint {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.file-field__filled {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.file-field__file-icon {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}

.file-field__file-name {
  flex: 1;
  min-width: 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-default-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-field__actions {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
}

.file-field__input {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  opacity: 0;
}
</style>
