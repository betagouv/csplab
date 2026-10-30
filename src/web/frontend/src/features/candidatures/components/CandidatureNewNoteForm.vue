<script setup lang="ts">
import type { CreateNotePayload, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useRoute, useRouter } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import { useToast } from '@/composables/ui/useToast'
import { useCreateCandidatureNote } from '../composables/useCandidatureNotes'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
}>()

const TITLE = 'Nouvelle note'

const { create, creating } = useCreateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

const route = useRoute()
const router = useRouter()

function backToNotes(): void {
  void router.push({ name: props.routes.notes, params: route.params })
}

async function submit(payload: CreateNotePayload): Promise<void> {
  try {
    await create(payload)
  }
  catch (error) {
    addToast({ variant: 'error', title: 'L\'enregistrement de la note a échoué' })
    throw error
  }
  addToast({ variant: 'success', title: 'Note enregistrée' })
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
