<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

withDefaults(defineProps<{
  submitLabel?: string
  cancelable?: boolean
  block?: boolean
}>(), {
  submitLabel: 'Enregistrer la note',
  cancelable: false,
  block: false,
})

const emit = defineEmits<{
  submit: []
  cancel: []
}>()

const message = defineModel<string>('message', { default: '' })
const privee = defineModel<boolean>('privee', { default: false })
</script>

<template>
  <form
    class="note-form"
    @submit.prevent="emit('submit')"
  >
    <CspTextarea
      v-model="message"
      :rows="3"
      placeholder="Votre note sur cette candidature…"
      aria-label="Note"
    />
    <div class="note-form__privee">
      <CspCheckbox
        v-model="privee"
        label="Note privée"
      />
      <p class="note-form__hint">
        Visible par vous uniquement
      </p>
    </div>
    <div
      class="note-form__actions"
      :class="{ 'note-form__actions--block': block }"
    >
      <CspButton
        v-if="cancelable"
        label="Annuler"
        variant="tertiary"
        size="sm"
        type="button"
        @click="emit('cancel')"
      />
      <CspButton
        :label="submitLabel"
        variant="secondary"
        size="sm"
        type="submit"
        :disabled="message.trim().length === 0"
      />
    </div>
  </form>
</template>

<style scoped lang="scss">
.note-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.note-form__privee {
  display: flex;
  flex-direction: column;
}

.note-form__hint {
  margin: 0 0 0 1.75rem;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--text-mention-grey);
}

.note-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}

.note-form__actions--block :deep(.csp-btn) {
  width: 100%;
}
</style>
