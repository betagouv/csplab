// Statut unique et « action à faire » pour la liste des offres, du point de vue de la personne
// qui suit l'offre (pas du valideur). Le statut réunit état de publication et état de la validation.

import type { Ecran } from './nav'
import type { Offre } from './store'
import { manquesAnnonce } from './aide'
import { aValiderParMoi, dateTri, joursRestants, termineBientot, validationManquante } from './store'

export type StatutListe = 'brouillon' | 'validation_attente' | 'validation_refusee' | 'validee' | 'prete' | 'publiee' | 'retiree' | 'archivee'

export const STATUTS: Record<StatutListe, { label: string, type: 'info' | 'new' | 'warning' | 'error' | 'success', contour?: boolean }> = {
  brouillon: { label: 'Brouillon', type: 'info' },
  validation_attente: { label: 'Validation en attente', type: 'warning' },
  validation_refusee: { label: 'Validation refusée', type: 'error' },
  // « Validée » : la validation peut être demandée à tout moment, une offre validée n'est donc pas forcément complète.
  validee: { label: 'Validée', type: 'success' },
  // Organisme sans circuit de validation : annonce complète, il ne reste qu'à publier.
  prete: { label: 'Prête à publier', type: 'new' },
  publiee: { label: 'En ligne', type: 'success' },
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

// --- Tableau « Mes offres d'emploi » : offres en préparation et en ligne ---

export type CategorieOffre = 'a_valider' | 'validation_refusee' | 'validee' | 'prete' | 'brouillon' | 'en_attente' | 'en_ligne'

/** Libellés des puces de filtre et des badges de statut, dans l'ordre d'urgence. */
export const CATEGORIES_OFFRE: { id: CategorieOffre, label: string, badge: 'info' | 'new' | 'warning' | 'error' | 'success' }[] = [
  { id: 'a_valider', label: 'À valider par vous', badge: 'info' },
  { id: 'validation_refusee', label: 'À corriger', badge: 'error' },
  { id: 'validee', label: 'Validée', badge: 'success' },
  { id: 'prete', label: 'Prête à publier', badge: 'new' },
  { id: 'brouillon', label: 'En rédaction', badge: 'new' },
  { id: 'en_attente', label: 'En attente de validation', badge: 'warning' },
  { id: 'en_ligne', label: 'En ligne', badge: 'success' },
]

export function categorieOffre(o: Offre): CategorieOffre {
  if (aValiderParMoi(o)) {
    return 'a_valider'
  }
  const s = statutListe(o)
  return s === 'validation_attente' ? 'en_attente' : s === 'publiee' ? 'en_ligne' : s as CategorieOffre
}

/** « 15 octobre 2026 », « Aujourd'hui, 11:27 », « Hier » ou « 2026-10-15 » → nombre de jours écoulés. */
function joursDepuis(date: string | undefined): number | null {
  if (!date) {
    return null
  }
  if (date.startsWith('Aujourd')) {
    return 0
  }
  if (date.startsWith('Hier')) {
    return 1
  }
  const iso = /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : dateTri(date)
  return /^\d{4}-\d{2}-\d{2}$/.test(iso) ? Math.max(0, -joursRestants(iso)) : null
}

/** Temps passé dans le statut : « depuis 6 jours ». */
export function depuis(o: Offre): string {
  const c = categorieOffre(o)
  const refus = [...(o.validations ?? [])].reverse().find(v => v.decision === 'refus')?.le
  const date = {
    a_valider: o.validationDemandeeLe,
    en_attente: o.validationDemandeeLe,
    validation_refusee: refus,
    validee: o.validationObtenueLe,
    prete: o.modifieLe,
    brouillon: o.creeLe,
    en_ligne: o.dateDebut,
  }[c]
  const j = joursDepuis(date)
  if (j === null) {
    return ''
  }
  return j === 0 ? 'depuis aujourd\'hui' : `depuis ${j} jour${j > 1 ? 's' : ''}`
}

/** Prochaine étape : un lien quand il y a quelque chose à faire, sinon un texte. Jamais vide. */
export function prochaineEtape(o: Offre): ActionAFaire {
  const offre = { nom: 'offre' as const, id: o.id }
  const recrutements = { nom: 'recrutements' as const }
  switch (categorieOffre(o)) {
    case 'a_valider':
      return { label: 'Valider ou refuser', ecran: offre }
    case 'validation_refusee':
      return { label: 'Corriger l\'offre', ecran: offre }
    case 'validee':
      return manquesAnnonce(o).length ? { label: 'Compléter l\'offre', ecran: offre } : { label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true } }
    case 'prete':
      return { label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true } }
    case 'brouillon':
      if (manquesAnnonce(o).length) {
        return { label: 'Compléter l\'annonce', ecran: offre }
      }
      return validationManquante(o) ? { label: 'Demander la validation', ecran: offre } : { label: 'Publier', ecran: { nom: 'apercu', id: o.id, publier: true } }
    case 'en_attente': {
      const attente = (o.validations ?? []).filter(v => v.decision === 'attente').map(v => v.nom)
      return { label: attente.length ? `Réponse attendue : ${attente.join(', ')}` : 'Réponse des valideurs attendue' }
    }
    case 'en_ligne':
      return termineBientot(o) ? { label: 'Prolonger la publication', ecran: recrutements } : { label: 'Suivre les candidatures', ecran: recrutements }
  }
}

/** Responsable du recrutement (ou, à défaut, la personne qui a créé l'offre). */
export function responsable(o: Offre): string {
  return o.responsables?.join(', ') || o.equipe.find(m => m.role === 'Responsable')?.nom || o.creePar || '—'
}
