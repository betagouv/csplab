<script setup lang="ts">
import type { NoteRouteNames } from '../types'
import { computed, onMounted, ref, useId } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useUnsavedChanges } from '@/composables/navigation/useUnsavedChanges'

const props = withDefaults(defineProps<{
  title: string
  routes: NoteRouteNames
  submitting: boolean
  submit: (message: string) => Promise<void>
  initialMessage?: string
}>(), {
  initialMessage: '',
})

const route = useRoute()
const router = useRouter()
const editorRouteName = route.name

const message = ref(props.initialMessage)
const titleId = useId()
const messageId = useId()

onMounted(() => document.getElementById(messageId)?.focus())

const isDirty = computed(() => message.value !== props.initialMessage)

useUnsavedChanges(
  () => isDirty.value,
  () => {
    message.value = props.initialMessage
  },
  { isLeftBy: to => to.name !== editorRouteName },
)

const canSubmit = computed(() => isDirty.value && message.value.trim() !== '' && !props.submitting)

function backToNotes(): void {
  void router.push({ name: props.routes.notes, params: route.params })
}

async function save(): Promise<void> {
  if (!canSubmit.value) {
    return
  }
  try {
    await props.submit(message.value.trim())
  }
  catch {
    return
  }
  message.value = props.initialMessage
  backToNotes()
}
</script>

<template>
  <section
    class="candidature-note-editor"
    :aria-labelledby="titleId"
  >
    <header class="candidature-note-editor__header">
      <h3
        :id="titleId"
        class="candidature-note-editor__title"
      >
        {{ title }}
      </h3>
      <CspButton
        variant="secondary"
        size="sm"
        label="Annuler"
        @click="backToNotes"
      />
    </header>

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
      <CspButton
        type="submit"
        label="Enregistrer la note"
        :disabled="!canSubmit"
        class="candidature-note-editor__submit"
      />
    </form>
  </section>
</template>

<style scoped lang="scss">
.candidature-note-editor__header {
  display: flex;
  gap: var(--csp-space-4);
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--csp-space-4);
}

.candidature-note-editor__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-note-editor__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.candidature-note-editor__submit {
  align-self: flex-end;
}
</style>
