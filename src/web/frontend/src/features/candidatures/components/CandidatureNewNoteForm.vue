<script setup lang="ts">
import type { NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useRoute, useRouter } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import { useSubmitNewNote } from '../composables/useSubmitNewNote'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
}>()

const TITLE = 'Nouvelle note'

const { submit, creating } = useSubmitNewNote(() => props.candidature)

const route = useRoute()
const router = useRouter()

function backToNotes(): void {
  void router.push({ name: props.routes.notes, params: route.params })
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
