// « Mes recrutements » : ce qui commence quand l'offre est publiée (candidatures, responsables, prolongation).
// Le nombre de candidatures est fictif, dérivé de la référence pour rester stable.

import type { Offre } from './store'
import { ref } from 'vue'
import { joursRestants } from './store'

export function candidatures(o: Offre): { total: number, nouvelles: number } {
  const n = [...o.id].reduce((s, c) => s + c.charCodeAt(0), 0)
  const jours = Math.max(1, -joursRestants(o.dateDebut))
  const total = Math.min(40, 3 + (n % 7) + jours)
  return { total, nouvelles: o.etat === 'publiee' ? Math.min(total, 1 + (n % 5)) : 0 }
}

/** « Aujourd'hui », « Il y a 3 jours » */
export function ilYa(date: string): string {
  const j = -joursRestants(date)
  return j <= 0 ? 'Aujourd\'hui' : `Il y a ${j} jour${j > 1 ? 's' : ''}`
}

/** Demandes ouvertes depuis le menu « … » d'une ligne, traitées par la page (boîtes de dialogue). */
export const aProlonger = ref<Offre | null>(null)
export const aRetirer = ref<Offre | null>(null)
