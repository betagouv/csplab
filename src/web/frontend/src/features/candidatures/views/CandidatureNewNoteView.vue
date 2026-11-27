<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import { useRouter } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CandidatureNoteEditor from '../components/CandidatureNoteEditor.vue'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'
import { useSubmitNewNote } from '../composables/useSubmitNewNote'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const TITLE = 'Nouvelle note'

const { submit, creating } = useSubmitNewNote(() => props.candidature)

const { names } = useCandidaturePanelRoutes()
const router = useRouter()

function backToNotes(): void {
  void router.push({ name: names.value.notes.notes, params: { ...props.candidature } })
}
</script>

<template>
  <CspCard as="li">
    <template #start>
      <span class="candidature-new-note__title">{{ TITLE }}</span>
    </template>
    <CandidatureNoteEditor
      :label="TITLE"
      :submitting="creating"
      :submit="submit"
      @cancel="backToNotes"
      @saved="backToNotes"
    />
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-new-note__title {
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
