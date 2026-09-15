import type { MembreEquipe, RecrutementRole } from '../types'
import { ref } from 'vue'

const revocationMembre = ref<MembreEquipe | null>(null)
const roleChange = ref<{ membre: MembreEquipe, role: RecrutementRole } | null>(null)

function requestRevocation(membre: MembreEquipe): void {
  revocationMembre.value = membre
}

function clearRevocation(): void {
  revocationMembre.value = null
}

function requestRoleChange(membre: MembreEquipe, role: RecrutementRole): void {
  roleChange.value = { membre, role }
}

function clearRoleChange(): void {
  roleChange.value = null
}

export function useMembreEquipeActions() {
  return {
    revocationMembre,
    requestRevocation,
    clearRevocation,
    roleChange,
    requestRoleChange,
    clearRoleChange,
  }
}
