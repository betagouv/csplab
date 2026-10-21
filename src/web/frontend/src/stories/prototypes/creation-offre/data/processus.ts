// Le processus d'un recrutement : fiche de poste → validation (DAR ou création directe) → offre → publication.

import type { OffreState } from './types'

export type PhaseId = 'besoin' | 'validation' | 'offre' | 'publication'

export interface Phase {
  id: PhaseId
  libelle: string
  etat: 'fait' | 'en_cours' | 'a_venir' | 'sans_objet'
  detail: string
}

/** L'offre peut être rédigée : DAR soumise ou validée, ou besoin sans DAR. */
export function pretPourOffre(s: OffreState): boolean {
  const b = s.besoin
  if (b.darApplicable === 'non') {
    return true
  }
  return b.darApplicable === 'oui' && ['en_cours', 'validee'].includes(b.darStatut)
}

export function phases(s: OffreState): Phase[] {
  const b = s.besoin
  const avecDar = b.darApplicable === 'oui'
  const besoinFait = Boolean(s.ficheId) || s.offreDemarree || (avecDar && ['en_cours', 'validee'].includes(b.darStatut))

  let validation: Phase
  if (b.darApplicable === 'non') {
    validation = { id: 'validation', libelle: 'Validation', etat: 'sans_objet', detail: 'Création directe' }
  }
  else if (!avecDar) {
    validation = { id: 'validation', libelle: 'Validation', etat: 'a_venir', detail: 'DAR ou non, à choisir' }
  }
  else if (b.darStatut === 'validee') {
    validation = { id: 'validation', libelle: 'DAR', etat: 'fait', detail: 'Validée' }
  }
  else if (b.darStatut === 'en_cours') {
    validation = { id: 'validation', libelle: 'DAR', etat: 'en_cours', detail: 'Soumise, en validation' }
  }
  else {
    validation = { id: 'validation', libelle: 'DAR', etat: 'en_cours', detail: 'Brouillon à soumettre' }
  }

  const offreCreee = ['creee', 'publiee'].includes(s.statut)
  return [
    { id: 'besoin', libelle: 'Fiche de poste', etat: besoinFait ? 'fait' : 'en_cours', detail: s.ficheId || b.ficheRef || 'En rédaction' },
    validation,
    {
      id: 'offre',
      libelle: 'Offre',
      etat: offreCreee ? 'fait' : s.offreDemarree ? 'en_cours' : 'a_venir',
      detail: offreCreee ? 'Créée' : s.offreDemarree ? 'En rédaction' : pretPourOffre(s) ? 'À rédiger' : '—',
    },
    {
      id: 'publication',
      libelle: 'Publication',
      etat: s.statut === 'publiee' ? 'fait' : 'a_venir',
      detail: s.statut === 'publiee' ? 'Publiée' : offreCreee ? 'Non publiée' : '—',
    },
  ]
}

export function etatOffre(s: OffreState): string {
  if (!s.offreDemarree) {
    return '—'
  }
  return {
    brouillon: 'En rédaction',
    a_valider: 'En validation',
    a_corriger: 'À corriger',
    validee: 'Validée',
    creee: 'Créée, non publiée',
    publiee: 'Publiée',
  }[s.statut]
}

/** « le 15 octobre 2026 » ou « aujourd'hui à 10:20 » selon la forme de la date. */
export function quand(date: string | undefined): string {
  if (!date) {
    return ''
  }
  const m = date.match(/^(Aujourd'hui|Hier), (\d{2}:\d{2})$/)
  if (m) {
    return `${m[1]!.toLowerCase()} à ${m[2]}`
  }
  return /^(?:Aujourd'hui|Hier)$/.test(date) ? date.toLowerCase() : `le ${date}`
}
