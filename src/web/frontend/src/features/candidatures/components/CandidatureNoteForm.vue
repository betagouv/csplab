<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import type { NavigationPredicate } from '@/composables/navigation/useUnsavedChanges'
import { useId } from 'vue'
import { useSubmitNewNote } from '../composables/useSubmitNewNote'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const TITLE = 'Ajouter une note'

const { submit, creating } = useSubmitNewNote(() => props.candidature)

const titleId = useId()

const leavesCandidature: NavigationPredicate = (to, from) => to.params.candidatureUuid !== from.params.candidatureUuid
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
      {{ TITLE }}
    </h3>
    <CandidatureNoteEditor
      :label="TITLE"
      :submitting="creating"
      :submit="submit"
      :cancellable="false"
      :autofocus="false"
      :rows="3"
      size="sm"
      submit-variant="secondary"
      :is-left-by="leavesCandidature"
    />
  </section>
</template>

<style scoped lang="scss">
.candidature-note-form__title {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
