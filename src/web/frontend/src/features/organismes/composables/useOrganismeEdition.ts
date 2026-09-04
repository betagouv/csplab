import type { OrganismesList } from '../types'
import { ref } from 'vue'

const editedOrganisme = ref<OrganismesList | null>(null)

function openEdition(organisme: OrganismesList): void {
  editedOrganisme.value = organisme
}

function closeEdition(): void {
  editedOrganisme.value = null
}

export function useOrganismeEdition() {
  return {
    editedOrganisme,
    openEdition,
    closeEdition,
  }
}
