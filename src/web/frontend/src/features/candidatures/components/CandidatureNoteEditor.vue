<script setup lang="ts">
import type { CreateNotePayload } from '../types'
import { computed, onMounted, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'

const props = withDefaults(defineProps<{
  title: string
  submitting: boolean
  submit: (payload: CreateNotePayload) => Promise<void>
  initialMessage?: string
  initialEstPrivee?: boolean
  cancelLabel?: string
  submitLabel?: string
}>(), {
  initialMessage: '',
  initialEstPrivee: false,
  cancelLabel: 'Annuler',
  submitLabel: 'Enregistrer la note',
})

const emit = defineEmits<{
  cancel: []
  saved: []
}>()

const message = ref(props.initialMessage)
const estPrivee = ref(props.initialEstPrivee)
const titleId = useId()
const messageId = useId()

onMounted(() => document.getElementById(messageId)?.focus())

const isDirty = computed(() => message.value !== props.initialMessage || estPrivee.value !== props.initialEstPrivee)

function reset(): void {
  message.value = props.initialMessage
  estPrivee.value = props.initialEstPrivee
}

useUnsavedChanges(() => isDirty.value, reset)

const canSubmit = computed(() => isDirty.value && message.value.trim() !== '' && !props.submitting)

async function save(): Promise<void> {
  if (!canSubmit.value) {
    return
  }
  try {
    await props.submit({ message: message.value.trim(), est_privee: estPrivee.value })
  }
  catch {
    return
  }
  reset()
  emit('saved')
}
</script>

<template>
  <section
    class="candidature-note-editor"
    :aria-labelledby="titleId"
  >
    <h3
      :id="titleId"
      class="candidature-note-editor__title"
    >
      {{ title }}
    </h3>

    <form
      class="candidature-note-editor__form"
      @submit.prevent="save"
    >
      <CspTextarea
        :id="messageId"
        v-model="message"
        :rows="8"
        :readonly="submitting"
        placeholder="Écrivez votre note…"
        :aria-labelledby="titleId"
      />
      <CspCheckbox
        v-model="estPrivee"
        label="Note privée"
        hint="Visible par vous uniquement"
        :disabled="submitting"
      />
      <div class="candidature-note-editor__actions">
        <CspButton
          variant="secondary"
          :label="cancelLabel"
          @click="emit('cancel')"
        />
        <CspButton
          type="submit"
          :label="submitLabel"
          :disabled="!canSubmit"
        />
      </div>
    </form>
  </section>
</template>

<style scoped lang="scss">
.candidature-note-editor__title {
  margin: 0 0 var(--csp-space-4);
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-note-editor__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.candidature-note-editor__actions {
  display: flex;
  gap: var(--csp-space-2);
  justify-content: flex-end;
}
</style>
