import type { OrganismeAdmin } from '../types'
import { ref } from 'vue'

const assignationOrganisme = ref<OrganismeAdmin | null>(null)

function openAssignation(organisme: OrganismeAdmin): void {
  assignationOrganisme.value = organisme
}

function closeAssignation(): void {
  assignationOrganisme.value = null
}

export function useGestionnaireAssignation() {
  return {
    assignationOrganisme,
    openAssignation,
    closeAssignation,
  }
}
