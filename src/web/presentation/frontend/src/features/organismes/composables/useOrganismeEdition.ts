import type { OrganismeAdmin } from '../types'
import { ref } from 'vue'

const editedOrganisme = ref<OrganismeAdmin | null>(null)

function openEdition(organisme: OrganismeAdmin): void {
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
