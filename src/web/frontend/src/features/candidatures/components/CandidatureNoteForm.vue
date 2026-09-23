<script setup lang="ts">
import type { CandidatureParams } from '../types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useToast } from '@/composables/ui/useToast'
import { useCreateCandidatureNote } from '../composables/useCandidatureNotes'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const { create, creating } = useCreateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

const titleId = useId()
const message = ref('')
const canSubmit = computed(() => message.value.trim().length > 0 && !creating.value)

async function submit(): Promise<void> {
  if (!canSubmit.value)
    return
  try {
    await create(message.value.trim())
    message.value = ''
    addToast({ variant: 'success', title: 'Note enregistrée' })
  }
  catch {
    addToast({ variant: 'error', title: 'L\'enregistrement de la note a échoué' })
  }
}
</script>

<template>
  <section
    class="candidature-note-form"
    :aria-labelledby="titleId"
  >
    <h3
      :id="titleId"
      class="candidature-note-form__title"
    >
      Ajouter une note
    </h3>
    <form
      class="candidature-note-form__form"
      @submit.prevent="submit"
    >
      <CspTextarea
        v-model="message"
        :rows="3"
        placeholder="Votre note sur cette candidature…"
        :aria-labelledby="titleId"
      />
      <CspButton
        type="submit"
        variant="secondary"
        size="sm"
        label="Enregistrer la note"
        :disabled="!canSubmit"
        class="candidature-note-form__submit"
      />
    </form>
  </section>
</template>

<style scoped lang="scss">
.candidature-note-form__title {
  margin: 0 0 var(--csp-space-3);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.candidature-note-form__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.candidature-note-form__submit {
  align-self: flex-end;
}
</style>
