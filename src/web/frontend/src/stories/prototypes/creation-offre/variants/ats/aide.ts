// Aide à la rédaction, simulée par des règles simples (pas d'IA) : un conseil par champ,
// et au plus une alerte discrète quand une information essentielle manque ou qu'un texte est difficile.

import type { Offre } from './store'
import { plusUnMois } from './store'

export type EtapeFormulaire = 'annonce' | 'candidature' | 'parametres' | 'publication'

export type Champ = 'titre' | 'categorie' | 'presentation' | 'missions' | 'profil' | 'competences' | 'conditions' | 'lieu' | 'remuneration' | 'metier' | 'commentaireValideurs' | 'cycleTravail'

export const CONSEILS: Record<Champ, { conseil: string, exemple?: string }> = {
  titre: {
    conseil: 'Un intitulé compris hors de l\'administration, sans sigle ni code interne.',
    exemple: '« Gestionnaire de paie (H/F) » plutôt que « Gest. paie BRH/SG ».',
  },
  categorie: {
    conseil: 'Catégorie statutaire du poste (A, B ou C).',
  },
  presentation: {
    conseil: '2 ou 3 phrases : l\'équipe, la finalité du poste, ce qui le rend intéressant.',
    exemple: '« Rejoignez la cellule paie : 5 personnes qui garantissent chaque mois la rémunération de 900 agents. »',
  },
  missions: {
    conseil: 'Décrivez le quotidien concret, une mission par ligne, en commençant par un verbe.',
    exemple: '« - Vous préparez et contrôlez les éléments de paie »',
  },
  profil: {
    conseil: 'Décrivez la personne recherchée plutôt que la fiche de poste ; restez ouvert aux parcours variés.',
  },
  competences: {
    conseil: 'Proposées par le métier choisi : retirez celles qui ne s\'appliquent pas, ajoutez les autres.',
  },
  conditions: {
    conseil: 'Horaires, déplacements, et toute sujétion liée au cycle de travail (nuit, week-end, astreintes).',
  },
  metier: {
    conseil: 'Un seul métier, choisi dans le référentiel RMFP+. Ses compétences s\'ajoutent à l\'annonce.',
  },
  commentaireValideurs: {
    conseil: 'Contexte utile aux valideurs ; il n\'est jamais publié.',
    exemple: '« Remplacement à l\'identique, poste budgété sur le BOP 217. »',
  },
  cycleTravail: {
    conseil: 'Reste interne. S\'il crée des sujétions (nuit, week-end, astreintes), indiquez-les aussi dans les conditions particulières de l\'annonce.',
  },
  lieu: {
    conseil: 'Ville et site, accès, télétravail : des informations décisives pour les candidats.',
  },
  remuneration: {
    conseil: 'Une fourchette ou une indication : c\'est l\'une des informations les plus recherchées.',
  },
}

const SIGLES = /\b[A-Z]{2}[A-Za-z]*\b/g

function sigles(texte: string): string[] {
  return [...new Set((texte.match(SIGLES) ?? []).filter(s => !['H/F', 'CDD', 'CDI'].includes(s)))]
}

function phrasesLongues(texte: string): boolean {
  return texte.split(/[.!?\n]/).some(p => p.trim().split(/\s+/).length > 35)
}

/** Une seule alerte par champ, la plus utile. `info` = rappel, `attention` = à corriger avant publication. */
export function alerte(o: Offre, champ: Champ): { niveau: 'info' | 'attention', texte: string } | null {
  switch (champ) {
    case 'titre': {
      if (!o.titre.trim()) {
        return { niveau: 'attention', texte: 'Le titre est nécessaire.' }
      }
      const s = sigles(o.titre)
      if (s.length) {
        return { niveau: 'info', texte: `Sigle peu compréhensible : ${s.join(', ')}.` }
      }
      return o.titre.length > 70 ? { niveau: 'info', texte: 'Titre long : il risque d\'être tronqué sur les sites d\'emploi.' } : null
    }
    case 'presentation': {
      if (!o.presentation.trim()) {
        return { niveau: 'info', texte: 'Une courte présentation aide le candidat à se projeter.' }
      }
      const s = sigles(o.presentation)
      return s.length ? { niveau: 'info', texte: `Sigles à expliciter pour un candidat : ${s.join(', ')}.` } : null
    }
    case 'profil': {
      const s = sigles(o.profil)
      return s.length ? { niveau: 'info', texte: `Sigles à expliciter : ${s.join(', ')}.` } : null
    }
    case 'missions': {
      if (!o.missions.trim()) {
        return { niveau: 'attention', texte: 'Les missions sont nécessaires.' }
      }
      const s = sigles(o.missions)
      if (s.length) {
        return { niveau: 'info', texte: `Texte repris d'un document interne ? Sigles à expliciter : ${s.join(', ')}.` }
      }
      return phrasesLongues(o.missions) ? { niveau: 'info', texte: 'Phrase très longue : découpez-la en missions courtes.' } : null
    }
    case 'competences':
      return o.competences.length > 8 ? { niveau: 'info', texte: `${o.competences.length} compétences : gardez les plus importantes pour ne pas décourager.` } : null
    case 'lieu':
      return o.lieu.trim() ? null : { niveau: 'attention', texte: 'Le lieu est nécessaire.' }
    case 'remuneration':
      return o.remuneration.trim() ? null : { niveau: 'info', texte: 'Information très attendue par les candidats.' }
    default:
      return null
  }
}

/**
 * Ce qui empêche de publier : l'annonce complète (article D311-8), le mode de candidature et des dates
 * valides. C'est le seul moment où les champs obligatoires sont contrôlés.
 */
export function manquesPublication(o: Offre): { etape: EtapeFormulaire, label: string }[] {
  const annonce: [boolean, string][] = [
    [!o.titre.trim(), 'intitulé'],
    [!o.categorie, 'catégorie'],
    [!o.statutPoste, 'statut du poste'],
    [!o.metier, 'métier'],
    [!o.missions.trim(), 'missions'],
    [!o.profil.trim(), 'profil recherché'],
    [!o.tempsTravail, 'temps de travail'],
    [!o.lieu.trim(), 'lieu'],
    [!o.dateVacance, 'date de vacance'],
    [o.ouvertA.includes('contractuel') && !o.fondementJuridique, 'fondement juridique (emploi ouvert aux contractuels)'],
  ]
  const candidature: [boolean, string][] = [
    [o.modeCandidature === 'courriel' && !o.courrielCandidature.trim(), 'adresse de réception des candidatures'],
    [o.modeCandidature === 'externe' && !o.urlCandidature.trim(), 'lien du site de candidature'],
  ]
  return [
    ...annonce.filter(([vide]) => vide).map(([, label]) => ({ etape: 'annonce' as const, label })),
    ...candidature.filter(([vide]) => vide).map(([, label]) => ({ etape: 'candidature' as const, label })),
    ...manquesDates(o).map(label => ({ etape: 'publication' as const, label })),
  ]
}

/** Ce qui manque à l'offre elle-même (annonce, candidature). Les dates se choisissent en publiant. */
export function manquesAnnonce(o: Offre): { etape: EtapeFormulaire, label: string }[] {
  return manquesPublication(o).filter(m => m.etape !== 'publication')
}

/** Date de fin au moins un mois après le début, sauf urgence (D311-2). */
export function manquesDates(o: Offre): string[] {
  if (!o.dateDebut || !o.dateFin) {
    return ['dates de publication']
  }
  if (!o.urgence && o.dateFin < plusUnMois(o.dateDebut)) {
    return ['date de fin au moins un mois après le début (sauf urgence)']
  }
  return []
}

/** Mise en forme sans changer les mots : éléments séparés par « ; » → puces. */
export function aMettreEnForme(texte: string): boolean {
  return /;\s*(?:\n|$)|;\s+\S/.test(texte) && !/^- /m.test(texte)
}

export function mettreEnForme(texte: string): string {
  const morceaux = texte.split(/\s*;\s*|\n/).map(m => m.trim().replace(/^- /, '').replace(/[.;]$/, '')).filter(Boolean)
  if (morceaux.length < 2) {
    return texte
  }
  const maj = (m: string) => m.charAt(0).toUpperCase() + m.slice(1)
  return morceaux.map(m => `- ${maj(m)}`).join('\n')
}
