<script setup lang="ts">
import type { CandidatureParams, NoteRouteNames } from '../types'
import { computed, onMounted, ref, useId } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'
import { useToast } from '@/composables/ui/useToast'
import { useCreateCandidatureNote } from '../composables/useCandidatureNotes'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
}>()

const route = useRoute()
const router = useRouter()
const { create, creating } = useCreateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

const message = ref('')
const titleId = useId()
const messageId = useId()

onMounted(() => document.getElementById(messageId)?.focus())

useUnsavedChanges(
  () => message.value !== '',
  () => {
    message.value = ''
  },
  { isLeftBy: to => to.name !== props.routes.create },
)

const canSubmit = computed(() => message.value.trim() !== '' && !creating.value)

function backToNotes(): void {
  void router.push({ name: props.routes.notes, params: route.params })
}

async function submit(): Promise<void> {
  if (!canSubmit.value) {
    return
  }
  try {
    await create(message.value.trim())
    message.value = ''
    addToast({ variant: 'success', title: 'Note enregistrée' })
    backToNotes()
  }
  catch {
    addToast({ variant: 'error', title: 'L\'enregistrement de la note a échoué' })
  }
}
</script>

<template>
  <section
    class="candidature-new-note"
    :aria-labelledby="titleId"
  >
    <header class="candidature-new-note__header">
      <h3
        :id="titleId"
        class="candidature-new-note__title"
      >
        Ajouter une note
      </h3>
      <CspButton
        variant="secondary"
        size="sm"
        label="Annuler"
        @click="backToNotes"
      />
    </header>

    <form
      class="candidature-new-note__form"
      @submit.prevent="submit"
    >
      <CspTextarea
        :id="messageId"
        v-model="message"
        :rows="8"
        :readonly="creating"
        placeholder="Votre note sur cette candidature…"
        :aria-labelledby="titleId"
      />
      <CspButton
        type="submit"
        label="Enregistrer la note"
        :disabled="!canSubmit"
        class="candidature-new-note__submit"
      />
    </form>
  </section>
</template>

<style scoped lang="scss">
.candidature-new-note__header {
  display: flex;
  gap: var(--csp-space-4);
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--csp-space-4);
}

.candidature-new-note__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-new-note__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.candidature-new-note__submit {
  align-self: flex-end;
}
</style>
