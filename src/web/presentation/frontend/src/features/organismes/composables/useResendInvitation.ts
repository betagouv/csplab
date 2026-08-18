import type { CompteUtilisateur } from '../types'
import { ref } from 'vue'

const resendCompte = ref<CompteUtilisateur | null>(null)

function openResend(compte: CompteUtilisateur): void {
  resendCompte.value = compte
}

function closeResend(): void {
  resendCompte.value = null
}

export function useResendInvitation() {
  return {
    resendCompte,
    openResend,
    closeResend,
  }
}
