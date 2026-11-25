// Étapes de l'offre (retour Alice du 25/11/2026) : deux grandes parties, chacune découpée en étapes.
// Les mêmes étapes servent au formulaire de création (une page par étape) et aux blocs de la page de l'offre.
// Retirées : « Informations internes » (France Travail, référence interne), « Étapes de recrutement » et
// « Équipe de recrutement ».

export type PartieOffre = 'poste' | 'metier' | 'cadre' | 'profil' | 'lieu' | 'formulaire' | 'documents'
export type GroupeOffre = 'annonce' | 'candidature'

export const GROUPES: { id: GroupeOffre, titre: string, aide: string, icone: string }[] = [
  { id: 'annonce', titre: 'Annonce visible du candidat', aide: 'Ce que liront les candidats sur Choisir le Service Public.', icone: 'ri:eye-line' },
  { id: 'candidature', titre: 'Paramétrage des candidatures', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.', icone: 'ri:settings-3-line' },
]

export const ETAPES_OFFRE: { id: PartieOffre, groupe: GroupeOffre, titre: string, aide: string }[] = [
  { id: 'poste', groupe: 'annonce', titre: 'Le poste', aide: 'Intitulé, nombre de postes et descriptif du poste.' },
  { id: 'metier', groupe: 'annonce', titre: 'Le métier', aide: 'Un métier du référentiel RMFP+ : ses compétences sont proposées, vous pouvez en retirer ou en ajouter.' },
  { id: 'cadre', groupe: 'annonce', titre: 'Cadre du recrutement', aide: 'À qui l\'emploi est ouvert, statut du poste, catégorie, corps et grade.' },
  { id: 'profil', groupe: 'annonce', titre: 'Profil et conditions', aide: 'La personne recherchée et les conditions de travail.' },
  { id: 'lieu', groupe: 'annonce', titre: 'Employeur et lieux', aide: 'Qui recrute, et où se trouve le poste.' },
  { id: 'formulaire', groupe: 'candidature', titre: 'Formulaire', aide: 'Les questions posées aux candidats au moment de postuler.' },
  { id: 'documents', groupe: 'candidature', titre: 'Documents', aide: 'Les pièces que les candidats joignent à leur candidature.' },
]

export function groupeDe(partie: PartieOffre) {
  return GROUPES.find(g => g.id === ETAPES_OFFRE.find(e => e.id === partie)!.groupe)!
}
