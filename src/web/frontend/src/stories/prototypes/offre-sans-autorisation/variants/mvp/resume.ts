// Lecture d'une étape dans un bloc de la page de l'offre : chaque champ avec sa valeur, ou « Non renseigné ».
// `obligatoire` signale un champ obligatoire encore vide (affiché « À renseigner »).

import type { PartieOffre } from './etapes'
import type { Offre } from './store'
import { champsObligatoires } from './aide'
import { metier, PIECES, TEMPS_TRAVAIL } from './store'

export interface LigneResume {
  label: string
  valeur?: string
  liste?: string[]
  long?: boolean
  manque?: boolean
}

const EXIGENCES: Record<string, string> = { non: 'Non demandé', facultatif: 'Facultatif', obligatoire: 'Obligatoire' }

function nature(o: Offre) {
  if (o.ouvertA.length === 2) {
    return 'Fonctionnaires et contractuels'
  }
  return o.ouvertA[0] === 'titulaire' ? 'Fonctionnaires uniquement' : o.ouvertA[0] === 'contractuel' ? 'Contractuels uniquement' : ''
}

export function resume(o: Offre, partie: PartieOffre): LigneResume[] {
  const manquants = new Set(champsObligatoires(o).filter(c => c.partie === partie && !c.ok).map(c => c.label))
  const l = (label: string, valeur?: string, extra: Partial<LigneResume> = {}, cle = label): LigneResume =>
    ({ label, valeur: valeur?.trim() || undefined, manque: manquants.has(cle), ...extra })
  const contractuels = o.ouvertA.includes('contractuel')
  switch (partie) {
    case 'poste':
      return [
        l('Intitulé de l\'offre', o.titre),
        l('Nombre de postes', o.nbPostes),
        l('Management', o.management),
        l('Descriptif du poste', o.missions, { long: true }),
      ]
    case 'metier': {
      const m = metier(o.metier)
      return [
        l('Métier', m ? `${m.libelle} — ${m.domaine}` : ''),
        { label: 'Compétences', liste: o.competences },
      ]
    }
    case 'cadre':
      return [
        l('Nature de l\'emploi', nature(o)),
        ...(contractuels ? [l('Nature du contrat', o.natureContrat), l('Fondement juridique', o.fondementJuridique)] : []),
        l('Statut du poste', o.statutPoste),
        l('Date de vacance', o.dateVacance),
        l('Catégorie', o.categorie),
        l('Corps', o.corps),
        l('Grade', o.grade),
        l('Avis de vacance au Journal officiel', o.lienJO),
      ]
    case 'profil':
      return [
        l('Profil recherché', o.profil, { long: true }),
        l('Niveau d\'expérience', o.niveauExperience),
        l('Niveau d\'études', o.niveauEtudes),
        l('Diplôme d\'État requis', o.diplomeEtat),
        l('Spécialisation', o.specialisation),
        l('Langues', o.langues, {}, 'Niveau de langue'),
        l('Temps de travail', TEMPS_TRAVAIL.find(t => t.value === o.tempsTravail)?.label),
        l('Télétravail', o.teletravail),
        l('Conditions particulières', o.conditions, { long: true }),
        l('Rémunération des fonctionnaires', o.remuneration),
        ...(contractuels ? [l('Rémunération des contractuels', o.remunerationContractuels)] : []),
        l('Informations complémentaires', o.infosComplementaires, { long: true }),
      ]
    case 'lieu':
      return [
        l('Descriptif de l\'employeur', o.descriptifEmployeur, { long: true }),
        l('Descriptif du service', o.presentation, { long: true }),
        o.sansLieuFixe
          ? l('Lieux', 'Pas de lieu fixe')
          : { label: 'Lieux', liste: (o.lieux ?? []).map(x => [x.adresse, x.affectation].filter(Boolean).join(' · ')), manque: manquants.has('Lieu (adresse géolocalisée)') },
      ]
    case 'formulaire':
      return [
        l('Mode de candidature', 'Dans l\'ATS'),
        { label: 'Questions aux candidats', liste: o.questions.filter(q => q.trim()) },
      ]
    case 'documents':
      return PIECES.map(p => l(p.label, EXIGENCES[o.pieces[p.id]]))
  }
}
