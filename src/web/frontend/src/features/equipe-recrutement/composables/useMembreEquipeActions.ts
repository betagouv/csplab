import type { MembreEquipe } from '../types'
import { ref } from 'vue'

const revocationMembre = ref<MembreEquipe | null>(null)

function requestRevocation(membre: MembreEquipe): void {
  revocationMembre.value = membre
}

function clearRevocation(): void {
  revocationMembre.value = null
}

export function useMembreEquipeActions() {
  return {
    revocationMembre,
    requestRevocation,
    clearRevocation,
  }
}
