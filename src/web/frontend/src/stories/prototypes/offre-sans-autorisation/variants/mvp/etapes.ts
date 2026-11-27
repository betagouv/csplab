// Étapes de l'offre (retour Alice du 25/11/2026) : deux grandes parties, chacune découpée en étapes.
// Les mêmes étapes servent au formulaire de création (une page par étape) et aux blocs de la page de l'offre.
// Textes d'aide et ordre des étapes : retour Alice du 25/11/2026.
// Retirées : « Informations internes » (France Travail, référence interne), « Étapes de recrutement » et
// « Équipe de recrutement ».

export type PartieOffre = 'poste' | 'metier' | 'cadre' | 'profil' | 'lieu' | 'formulaire' | 'documents' | 'diffusion'
export type GroupeOffre = 'annonce' | 'candidature' | 'diffusion'

export const GROUPES: { id: GroupeOffre, titre: string, aide: string, icone: string }[] = [
  { id: 'annonce', titre: 'Annonce visible du candidat', aide: 'Ce que liront les candidats sur Choisir le Service Public.', icone: 'ri:eye-line' },
  { id: 'candidature', titre: 'Paramétrage des candidatures', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.', icone: 'ri:settings-3-line' },
  // Partie 3 (revue UI équipe, 27/11/2026) : où l'offre est diffusée et où arrivent les candidatures.
  { id: 'diffusion', titre: 'Diffusion', aide: 'Où l\'offre est publiée et où les candidats postulent.', icone: 'ri:megaphone-line' },
]

export const ETAPES_OFFRE: { id: PartieOffre, groupe: GroupeOffre, titre: string, aide: string }[] = [
  { id: 'poste', groupe: 'annonce', titre: 'Le poste', aide: 'Ce que les candidats liront en premier.' },
  { id: 'cadre', groupe: 'annonce', titre: 'Le cadre du recrutement', aide: 'Indique aux candidats les conditions d\'accès au poste.' },
  { id: 'metier', groupe: 'annonce', titre: 'Le métier', aide: 'Les compétences proposées décrivent aux candidats ce qui est attendu.' },
  { id: 'profil', groupe: 'annonce', titre: 'Le profil recherché', aide: 'Permet aux candidats de se projeter dans le poste.' },
  { id: 'lieu', groupe: 'annonce', titre: 'L\'environnement de travail', aide: 'Permet aux candidats de mieux connaître leur futur employeur.' },
  { id: 'formulaire', groupe: 'candidature', titre: 'Formulaire', aide: 'Questions posées au candidat au moment où il postule.' },
  { id: 'documents', groupe: 'candidature', titre: 'Documents', aide: 'Pièces que les candidats joignent à leur candidature.' },
  { id: 'diffusion', groupe: 'diffusion', titre: 'Diffusion de l\'offre', aide: 'D\'abord la gestion des candidatures, ensuite les sites de diffusion.' },
]

export function groupeDe(partie: PartieOffre) {
  return GROUPES.find(g => g.id === ETAPES_OFFRE.find(e => e.id === partie)!.groupe)!
}
