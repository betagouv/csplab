// Statut unique et « action à faire » pour la liste des offres, du point de vue de la personne
// qui suit l'offre (pas du valideur). Le statut réunit état de publication et état de la validation.

import type { Ecran } from './nav'
import type { Offre } from './store'
import { manquesAnnonce } from './aide'
import { aValiderParMoi, joursRestants, termineBientot, validationManquante } from './store'

export type StatutListe = 'brouillon' | 'validation_attente' | 'validation_refusee' | 'validee' | 'prete' | 'publiee' | 'retiree' | 'archivee'

export const STATUTS: Record<StatutListe, { label: string, type: 'info' | 'new' | 'warning' | 'error' | 'success', contour?: boolean }> = {
  brouillon: { label: 'Brouillon', type: 'info' },
  validation_attente: { label: 'Validation en attente', type: 'warning' },
  validation_refusee: { label: 'Validation refusée', type: 'error' },
  // « Validée » : la validation peut être demandée à tout moment, une offre validée n'est donc pas forcément complète.
  validee: { label: 'Validée', type: 'success' },
  // Organisme sans circuit de validation : annonce complète, il ne reste qu'à publier.
  prete: { label: 'Prête à publier', type: 'new' },
  publiee: { label: 'Publiée', type: 'success' },
  retiree: { label: 'Retirée', type: 'warning', contour: true },
  archivee: { label: 'Archivée', type: 'info', contour: true },
}

export function statutListe(o: Offre): StatutListe {
  if (o.etat !== 'brouillon') {
    return o.etat
  }
  if (o.validationEtat === 'en_attente') {
    return 'validation_attente'
  }
  if (o.validationEtat === 'refusee') {
    return 'validation_refusee'
  }
  if (o.validationEtat === 'validee') {
    return 'validee'
  }
  return !validationManquante(o) && !manquesAnnonce(o).length ? 'prete' : 'brouillon'
}

export interface ActionAFaire {
  label: string
  /** Absent : simple information, sans lien. */
  ecran?: Ecran
}

export function actionAFaire(o: Offre): ActionAFaire | null {
  const offre = { nom: 'offre' as const, id: o.id }
  if (aValiderParMoi(o)) {
    return { label: 'Valider ou refuser', ecran: offre }
  }
  switch (statutListe(o)) {
    case 'brouillon':
      // Annonce en cours de rédaction : pas d'action à mettre en avant, le statut suffit.
      return null
    case 'validation_attente':
      // Rien à faire pour le demandeur : le statut suffit, le détail des réponses est sur la page de l'offre.
      return null
    case 'validation_refusee':
      return { label: 'Corriger l\'offre', ecran: offre }
    case 'validee':
      return manquesAnnonce(o).length ? { label: 'Compléter l\'offre', ecran: offre } : { label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true } }
    case 'prete':
      return { label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true } }
    case 'publiee': {
      if (termineBientot(o)) {
        const j = joursRestants(o.dateFin)
        return { label: `Prolonger (fin ${j <= 0 ? 'aujourd\'hui' : `dans ${j} j`})`, ecran: offre }
      }
      // Publication en cours sans échéance proche : rien à faire.
      return null
    }
    case 'retiree':
      return { label: 'Archiver', ecran: offre }
    default:
      return null
  }
}

/** « 12 nov. 2026 » */
export function dateCourte(date: string): string {
  return date ? new Date(`${date}T12:00:00`).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' }) : '-'
}

/** La référence Choisir le Service Public n'existe qu'une fois l'offre publiée. */
export function referenceCsp(o: Offre): string {
  return o.etat === 'brouillon' ? '-' : `CSP-${o.id.slice(4).replace('-', '')}`
}
