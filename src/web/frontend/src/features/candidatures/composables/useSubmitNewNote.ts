import type { MaybeRefOrGetter } from 'vue'
import type { CreateNotePayload } from '../types'
import type { CandidatureParams } from '@/api/params'
import { useToast } from '@/composables/ui/useToast'
import { useCreateCandidatureNote } from './useCandidatureNotes'

export function useSubmitNewNote(candidature: MaybeRefOrGetter<CandidatureParams>) {
  const { create, creating } = useCreateCandidatureNote(candidature)
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

  return { submit, creating }
}
