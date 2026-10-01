import type { AssistantAdapter } from '../types'
import { useMutation } from '@pinia/colada'
import { createMotsClesAdapter } from '../utils/motsClesAdapter'

export function useAssistantAide(adapter: AssistantAdapter = createMotsClesAdapter()) {
  const mutation = useMutation({
    mutation: (question: string) => adapter.repondre(question),
  })

  return {
    poser: mutation.mutate,
    reponse: mutation.data,
    pending: mutation.isLoading,
    error: mutation.error,
  }
}
