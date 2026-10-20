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
