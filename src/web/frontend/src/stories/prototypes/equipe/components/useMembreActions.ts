import type { ProtoAgent } from '../data/mock'
import { ref } from 'vue'

export interface RetraitDemande {
  recrutementUuid: string
  agent: ProtoAgent
}

const retraitDemande = ref<RetraitDemande | null>(null)
const revocationDemande = ref<ProtoAgent | null>(null)

export function useMembreActions() {
  return {
    retraitDemande,
    demanderRetrait(demande: RetraitDemande): void {
      retraitDemande.value = demande
    },
    annulerRetrait(): void {
      retraitDemande.value = null
    },
    revocationDemande,
    demanderRevocation(agent: ProtoAgent): void {
      revocationDemande.value = agent
    },
    annulerRevocation(): void {
      revocationDemande.value = null
    },
  }
}
