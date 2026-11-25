// Statut unique et « action à faire » pour la liste des offres, du point de vue de la personne
// qui suit l'offre (pas du valideur). Le statut réunit état de publication et état de la validation.

import type { Ecran } from './nav'
import type { Offre } from './store'
import { champsObligatoires, manquesAnnonce } from './aide'
import { aujourdhui, aValiderParMoi, dateTri, joursRestants, termineBientot, validationManquante } from './store'

export type StatutListe = 'brouillon' | 'validation_attente' | 'validation_refusee' | 'validee' | 'prete' | 'publiee' | 'retiree' | 'archivee'

export const STATUTS: Record<StatutListe, { label: string, type: 'info' | 'new' | 'warning' | 'error' | 'success', contour?: boolean }> = {
  brouillon: { label: 'En préparation', type: 'info' },
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
  /** Précision affichée sous le lien. */
  detail?: string
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
      return manquesAnnonce(o).length ? { label: 'Compléter l\'offre', ecran: offre } : { label: 'Publier', ecran: { nom: 'publier', id: o.id } }
    case 'prete':
      return { label: 'Publier', ecran: { nom: 'publier', id: o.id } }
    case 'publiee': {
      if (termineBientot(o)) {
        const j = joursRestants(o.dateFin)
        return { label: `Prolonger (fin ${j <= 0 ? 'aujourd\'hui' : `dans ${j} j`})`, ecran: offre }
      }
      // Publication en cours sans échéance proche : rien à faire.
      return null
    }
    case 'retiree':
      return { label: 'Remettre en ligne', ecran: { ...offre, section: 'remettre' } }
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

// --- Tableau « Mes offres d'emploi » (sans autorisation) : onglets par statut (Alice, 25/11/2026) ---

export type CategorieOffre = 'brouillon' | 'en_ligne' | 'en_pause' | 'archivee'

/** Libellés des badges de statut. « En pause » remplace « Dépubliée » : offre retirée, qu'on peut remettre en ligne. */
export const CATEGORIES_OFFRE: { id: CategorieOffre, label: string, badge: 'info' | 'new' | 'warning' | 'error' | 'success' }[] = [
  { id: 'brouillon', label: 'En préparation', badge: 'new' },
  { id: 'en_ligne', label: 'En ligne', badge: 'success' },
  { id: 'en_pause', label: 'En pause', badge: 'warning' },
  { id: 'archivee', label: 'Archivée', badge: 'info' },
]

/** Onglets de la liste : un par statut, puis « Toutes ». Pas de « À valider » : organisme sans autorisation. */
export const PHASES: { id: CategorieOffre, label: string }[] = CATEGORIES_OFFRE.map(c => ({ id: c.id, label: c.label }))

export function categorieOffre(o: Offre): CategorieOffre {
  return o.etat === 'publiee' ? 'en_ligne' : o.etat === 'retiree' ? 'en_pause' : o.etat === 'archivee' ? 'archivee' : 'brouillon'
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
  const date = { brouillon: o.creeLe, en_ligne: o.dateDebut, en_pause: o.dateFin && o.dateFin < aujourdhui() ? o.dateFin : o.retireeLe, archivee: o.archiveeLe }[categorieOffre(o)]
  const j = joursDepuis(date)
  if (j === null) {
    return ''
  }
  return j === 0 ? 'depuis aujourd\'hui' : `depuis ${j} jour${j > 1 ? 's' : ''}`
}

/** Prochaine étape : un lien quand il y a quelque chose à faire, sinon un texte. Jamais vide. */
export function prochaineEtape(o: Offre, peutPublier = true): ActionAFaire {
  const offre = { nom: 'offre' as const, id: o.id }
  switch (categorieOffre(o)) {
    case 'brouillon':
      if (manquesAnnonce(o).length) {
        // Retour PO (L11) : dire où on en est, pas seulement qu'il reste à faire.
        const champs = champsObligatoires(o)
        return { label: 'Compléter l\'annonce', detail: `${champs.filter(c => c.ok).length} / ${champs.length} champs obligatoires`, ecran: { nom: 'rediger', id: o.id } }
      }
      return peutPublier ? { label: 'Publier', ecran: { nom: 'publier', id: o.id } } : { label: 'À publier par un agent habilité' }
    case 'en_ligne':
      // Rien à faire tant que la fin n'approche pas : les candidatures ont leur propre colonne (retour PO, L6).
      return termineBientot(o) ? { label: 'Prolonger la publication', ecran: offre } : { label: '—' }
    case 'en_pause':
      return { label: 'Remettre en ligne', ecran: { ...offre, section: 'remettre' } }
    case 'archivee':
      return { label: '—' }
  }
}

/** Responsable du recrutement (ou, à défaut, la personne qui a créé l'offre). */
export function responsable(o: Offre): string {
  return o.responsables?.join(', ') || o.equipe.find(m => m.role === 'Responsable')?.nom || o.creePar || '—'
}

export function responsables(o: Offre): string[] {
  if (o.responsables?.length) {
    return o.responsables
  }
  const r = o.equipe.find(m => m.role === 'Responsable')?.nom || o.creePar
  return r ? [r] : []
}

/** « 20 nov. 2026 », « hier », « aujourd'hui à 09:12 », quel que soit le format stocké. */
function quand(date: string | undefined): string {
  if (!date) {
    return ''
  }
  if (date.startsWith('Aujourd')) {
    return date.includes(',') ? `aujourd'hui à ${date.slice(-5)}` : 'aujourd\'hui'
  }
  if (date.startsWith('Hier')) {
    return 'hier'
  }
  const iso = /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : dateTri(date)
  return /^\d{4}-\d{2}-\d{2}$/.test(iso) ? `le ${dateCourte(iso)}` : date
}

/** Colonne « Activité sur l'offre » : la dernière activité significative, selon le statut (Alice, 25/11/2026). */
export function activiteOffre(o: Offre): string {
  switch (categorieOffre(o)) {
    case 'brouillon':
      return `Modifiée ${quand(o.modifieLe)}`
    case 'en_ligne':
      return `Publiée ${quand(o.publieeLe ?? o.dateDebut)}`
    case 'en_pause':
      return `Mise en pause ${quand(o.retireeLe ?? o.dateFin)}`
    case 'archivee':
      return `Archivée ${quand(o.archiveeLe)}`
  }
}

// --- Actions à faire depuis « Mes offres d'emploi » (Alice, 25/11/2026) ---

export type TypeAction = 'continuer' | 'publier' | 'prolonger'

/**
 * Action à mettre en avant pour une offre, ou rien. Sans autorisation, « publier une offre validée » devient
 * « publier une offre prête » : en préparation, tous les champs obligatoires remplis.
 */
export function actionOffre(o: Offre, peutPublier = true): { type: TypeAction, label: string, ecran: Ecran } | null {
  if (o.etat === 'brouillon') {
    if (champsObligatoires(o).some(c => !c.ok)) {
      return { type: 'continuer', label: 'Continuer', ecran: { nom: 'rediger', id: o.id } }
    }
    return peutPublier ? { type: 'publier', label: 'Publier', ecran: { nom: 'publier', id: o.id } } : null
  }
  if (termineBientot(o) && peutPublier) {
    return { type: 'prolonger', label: 'Prolonger', ecran: { nom: 'offre', id: o.id, section: 'prolonger' } }
  }
  return null
}

/** Sous-statut d'une offre en préparation (colonne « Statut » de l'onglet En préparation). Plus tard : À valider, Validée… */
export function etatPreparation(o: Offre): string {
  return champsObligatoires(o).some(c => !c.ok) ? 'Brouillon' : 'Prête à publier'
}
