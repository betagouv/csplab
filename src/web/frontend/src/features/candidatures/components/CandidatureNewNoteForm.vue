<script setup lang="ts">
import type { NoteRouteNames } from '../types'
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

async function submit(message: string): Promise<void> {
  try {
    await create({ message, est_privee: false })
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
