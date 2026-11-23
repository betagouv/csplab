<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import type { NavigationPredicate } from '@/composables/navigation/useUnsavedChanges'
import { useId } from 'vue'
import { useSubmitNewNote } from '../composables/useSubmitNewNote'
import CandidatureAsideTitle from './CandidatureAsideTitle.vue'
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
    <CandidatureAsideTitle :id="titleId">
      {{ TITLE }}
    </CandidatureAsideTitle>
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
.candidature-note-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}
</style>
