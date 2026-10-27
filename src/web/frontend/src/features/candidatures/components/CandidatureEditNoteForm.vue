<script setup lang="ts">
import type { Note, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useToast } from '@/composables/ui/useToast'
import { useUpdateCandidatureNote } from '../composables/useCandidatureNotes'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
  routes: NoteRouteNames
  note: Note
}>()

const { update, updating } = useUpdateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

async function submit(message: string): Promise<void> {
  try {
    await update({ noteUuid: props.note.uuid, message, est_privee: props.note.est_privee })
  }
  catch (error) {
    addToast({ variant: 'error', title: 'La modification de la note a échoué' })
    throw error
  }
  addToast({ variant: 'success', title: 'Note modifiée' })
}
</script>

<template>
  <CandidatureNoteEditor
    title="Modifier la note"
    :routes="routes"
    :submitting="updating"
    :submit="submit"
    :initial-message="note.message"
  />
</template>
