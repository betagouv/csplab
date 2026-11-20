import { ref } from 'vue'
import { isHttpStatus } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'

interface TagChangesOptions {
  deletedTitle: string
  onDeleted: () => void
}

export function useTagChanges({ deletedTitle, onDeleted }: TagChangesOptions) {
  const { addToast } = useToast()
  const addingTagUuid = ref<string | null>(null)

  async function submitAdd(tagUuid: string, request: () => Promise<void>): Promise<void> {
    addingTagUuid.value = tagUuid
    try {
      await request()
    }
    catch (error) {
      if (isHttpStatus(error, 409)) {
        return
      }
      if (isHttpStatus(error, 404)) {
        addToast({ variant: 'warning', title: deletedTitle })
        onDeleted()
        return
      }
      addToast({ variant: 'error', title: 'L\'ajout de l\'étiquette a échoué' })
    }
    finally {
      addingTagUuid.value = null
    }
  }

  async function submitRemove(request: () => Promise<void>): Promise<void> {
    try {
      await request()
    }
    catch (error) {
      if (!isHttpStatus(error, 404)) {
        addToast({ variant: 'error', title: 'Le retrait de l\'étiquette a échoué' })
      }
    }
  }

  return { addingTagUuid, submitAdd, submitRemove }
}
