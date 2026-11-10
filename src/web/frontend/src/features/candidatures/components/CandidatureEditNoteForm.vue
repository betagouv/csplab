<script setup lang="ts">
import type { CreateNotePayload, Note } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useToast } from '@/composables/ui/useToast'
import { useUpdateCandidatureNote } from '../composables/useCandidatureNotes'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const props = defineProps<{
  candidature: CandidatureParams
  note: Note
}>()

const emit = defineEmits<{
  close: []
}>()

const { update, updating } = useUpdateCandidatureNote(() => props.candidature)
const { addToast } = useToast()

async function submit(payload: CreateNotePayload): Promise<void> {
  try {
    await update({ noteUuid: props.note.uuid, ...payload })
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
    label="Modifier la note"
    :submitting="updating"
    :submit="submit"
    :initial-message="note.message"
    :initial-est-privee="note.est_privee"
    cancel-label="Annuler sans sauvegarder"
    submit-label="Enregistrer les modifications"
    @cancel="emit('close')"
    @saved="emit('close')"
  />
</template>
