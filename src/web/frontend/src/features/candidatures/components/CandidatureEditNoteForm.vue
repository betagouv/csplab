<script setup lang="ts">
import type { CreateNotePayload, Note, NoteRouteNames } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useRoute, useRouter } from 'vue-router'
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

const route = useRoute()
const router = useRouter()

function backToNotes(): void {
  void router.push({ name: props.routes.notes, params: route.params })
}

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
    title="Modifier la note"
    :submitting="updating"
    :submit="submit"
    :initial-message="note.message"
    :initial-est-privee="note.est_privee"
    cancel-label="Annuler sans sauvegarder"
    submit-label="Enregistrer les modifications"
    @cancel="backToNotes"
    @saved="backToNotes"
  />
</template>
