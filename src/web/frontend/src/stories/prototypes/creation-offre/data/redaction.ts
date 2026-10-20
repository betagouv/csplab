// Préremplissage des sections de l'offre à partir des informations du poste (sans IA : simple mise en forme).

import type { OffreState, SectionOffreId } from './types'
import { ORGANISMES } from './referentiels'
import { OFFRE_REDIGEE } from './scenario'

export function texteDepuisPoste(s: OffreState, id: SectionOffreId): string {
  const b = s.besoin
  const p = s.poste
  switch (id) {
    case 'organisme':
      return b.organisme === 'dreal-occ' ? OFFRE_REDIGEE.organisme : ''
    case 'poste':
      return [p.environnement, b.service ? `Poste rattaché au ${b.service}.` : ''].filter(Boolean).join(' ')
    case 'missions':
      return [p.missions, ...p.activites.map(a => `- ${a}`)].filter(Boolean).join('\n')
    case 'profil':
      return [p.qualifications, p.profil, ...p.competences.map(c => `- ${c}`)].filter(Boolean).join('\n')
    case 'conditions': {
      if (!b.statuts.length) {
        return ''
      }
      const statuts = b.statuts.length === 2 ? 'aux fonctionnaires et aux contractuels' : b.statuts[0] === 'titulaire' ? 'aux fonctionnaires' : 'aux contractuels'
      const contrat = b.statuts.includes('contractuel') && b.typeContrat === 'cdd' ? ` (CDD${b.dureeContrat ? ` de ${b.dureeContrat}` : ''})` : ''
      return `Poste de catégorie ${b.categories.join(' ou ') || '—'} ouvert ${statuts}${contrat}.`
    }
    case 'pratique':
      return [b.localisation && `Poste basé à ${b.localisation}.`, b.teletravail && `Télétravail : ${b.teletravail}.`, p.aDesConditions && p.conditionsParticulieres].filter(Boolean).join(' ')
    case 'candidature':
      return OFFRE_REDIGEE.candidature
  }
}

export function nomOrganisme(s: OffreState): string {
  return ORGANISMES.find(o => o.value === s.besoin.organisme)?.label ?? ''
}

/** Le texte ressemble-t-il à une liste brute (« ; », retours à la ligne en milieu de phrase) ? */
export function aMettreEnForme(texte: string): boolean {
  return /;\s*(?:\n|$)|;\s+\S/.test(texte) && !/^- /m.test(texte)
}

/**
 * Mise en forme déterministe d'un texte repris tel quel : la première phrase reste un paragraphe,
 * les éléments séparés par « ; » deviennent des puces. Aucun mot n'est changé.
 */
export function mettreEnForme(texte: string): string {
  const morceaux = texte.split(/\s*;\s*|\n/).map(m => m.trim().replace(/[.;]$/, '')).filter(Boolean)
  if (morceaux.length < 2) {
    return texte
  }
  const majuscule = (m: string) => m.charAt(0).toUpperCase() + m.slice(1)
  const [premier, ...reste] = morceaux
  return [`${majuscule(premier!)} :`, ...reste.map(m => `- ${majuscule(m)}`)].join('\n')
}
