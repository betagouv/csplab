<script setup lang="ts">
import type { CreateNotePayload, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useToast } from '@/composables/ui/useToast'
import { useCreateCandidatureNote } from '../composables/useCandidatureNotes'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
}>()

const { create, creating } = useCreateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

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
  <CandidatureNoteEditor
    title="Ajouter une note"
    :routes="routes"
    :submitting="creating"
    :submit="submit"
  />
</template>
