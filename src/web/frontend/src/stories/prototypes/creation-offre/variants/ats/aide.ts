// Aide à la rédaction, simulée par des règles simples (pas d'IA) : un conseil par champ,
// et au plus une alerte discrète quand une information essentielle manque ou qu'un texte est difficile.

import type { Offre } from './store'
import { CHAMPS_DETERMINANTS } from './store'

export type Champ = 'titre' | 'categorie' | 'motif' | 'presentation' | 'missions' | 'profil' | 'indispensables' | 'souhaitables' | 'modalites' | 'nbPostes' | 'lieu' | 'remuneration' | 'dateLimite'

export const CONSEILS: Record<Champ, { conseil: string, exemple?: string }> = {
  titre: {
    conseil: 'Un intitulé compris hors de l\'administration, sans sigle ni code interne.',
    exemple: '« Gestionnaire de paie (H/F) » plutôt que « Gest. paie BRH/SG ».',
  },
  categorie: {
    conseil: 'Catégorie statutaire du poste (A, B ou C).',
  },
  motif: {
    conseil: 'Vacance, remplacement, création… Quelques mots évitent aux valideurs de rappeler le service.',
    exemple: '« Remplacement d\'un départ à la retraite au 1er janvier. »',
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
  indispensables: {
    conseil: 'Ce sans quoi la candidature ne peut pas aboutir. 2 à 4 suffisent.',
  },
  souhaitables: {
    conseil: 'Ce qui est un plus et départage, sans décourager.',
  },
  modalites: {
    conseil: 'À qui le poste est ouvert (fonctionnaires, contractuels) et type de contrat.',
  },
  nbPostes: {
    conseil: 'Une seule offre, et une seule validation, peut couvrir plusieurs postes identiques.',
  },
  lieu: {
    conseil: 'Ville et site, accès, télétravail : des informations décisives pour les candidats.',
  },
  remuneration: {
    conseil: 'Une fourchette ou une indication : c\'est l\'une des informations les plus recherchées.',
  },
  dateLimite: {
    conseil: 'Nécessaire pour publier.',
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
    case 'indispensables':
      return o.indispensables.length > 5 ? { niveau: 'info', texte: `${o.indispensables.length} compétences indispensables : vous risquez d'écarter de bons profils.` } : null
    case 'souhaitables':
      return !o.souhaitables.length && o.indispensables.length > 3 ? { niveau: 'info', texte: 'Certaines compétences indispensables sont peut-être seulement souhaitables ?' } : null
    case 'nbPostes':
      return Number(o.nbPostes) >= 1 ? null : { niveau: 'attention', texte: 'Indiquez au moins 1 poste.' }
    case 'lieu':
      return o.lieu.trim() ? null : { niveau: 'attention', texte: 'Le lieu est nécessaire.' }
    case 'remuneration':
      return o.remuneration.trim() ? null : { niveau: 'info', texte: 'Information très attendue par les candidats.' }
    case 'dateLimite':
      return o.dateLimite ? null : { niveau: 'info', texte: 'À renseigner avant de publier.' }
    default:
      return null
  }
}

/**
 * Ce qui empêche d'envoyer pour validation (organisme avec DAR : tous les champs déterminants)
 * ou de créer l'offre (sans DAR : titre, missions, lieu).
 */
export function manquesCreation(o: Offre): string[] {
  const vide = {
    titre: !o.titre.trim(),
    categorie: !o.categorie,
    nbPostes: !(Number(o.nbPostes) >= 1),
    lieu: !o.lieu.trim(),
    missions: !o.missions.trim(),
  }
  const requis = o.dar === 'requise' ? Object.keys(CHAMPS_DETERMINANTS) as (keyof typeof vide)[] : ['titre', 'missions', 'lieu'] as const
  return requis.filter(c => vide[c]).map(c => CHAMPS_DETERMINANTS[c])
}

/** Ce qui empêche de publier : préparation (modalités, date limite) et au moins un support. */
export function manquesPublication(o: Offre): string[] {
  return [
    !o.modalites.trim() && 'modalités de recrutement',
    !o.dateLimite && 'date limite de candidature',
    !o.canaux.length && 'au moins un support de publication',
  ].filter(Boolean) as string[]
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
