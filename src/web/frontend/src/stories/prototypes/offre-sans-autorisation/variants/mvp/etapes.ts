// Étapes de l'offre (retour Alice du 25/11/2026) : deux grandes parties, chacune découpée en étapes.
// Les mêmes étapes servent au formulaire de création (une page par étape) et aux blocs de la page de l'offre.
// Les textes d'aide (sous « Étape N sur 7 ») sont des propositions de Claude, à relire.
// Retirées : « Informations internes » (France Travail, référence interne), « Étapes de recrutement » et
// « Équipe de recrutement ».

export type PartieOffre = 'poste' | 'metier' | 'cadre' | 'profil' | 'lieu' | 'formulaire' | 'documents'
export type GroupeOffre = 'annonce' | 'candidature'

export const GROUPES: { id: GroupeOffre, titre: string, aide: string, icone: string }[] = [
  { id: 'annonce', titre: 'Annonce visible du candidat', aide: 'Ce que liront les candidats sur Choisir le Service Public.', icone: 'ri:eye-line' },
  { id: 'candidature', titre: 'Paramétrage des candidatures', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.', icone: 'ri:settings-3-line' },
]

export const ETAPES_OFFRE: { id: PartieOffre, groupe: GroupeOffre, titre: string, aide: string }[] = [
  { id: 'poste', groupe: 'annonce', titre: 'Le poste', aide: 'C\'est ce que le candidat lit en premier : un intitulé clair et un descriptif concret lui permettent de savoir rapidement si le poste lui correspond.' },
  { id: 'metier', groupe: 'annonce', titre: 'Le métier', aide: 'Le métier rattache l\'offre au référentiel RMFP+. Les compétences proposées décrivent ce qui est attendu : gardez celles qui comptent vraiment pour ce poste.' },
  { id: 'cadre', groupe: 'annonce', titre: 'Cadre du recrutement', aide: 'Le cadre statutaire du poste : il permet au candidat de vérifier s\'il peut postuler, selon qu\'il est fonctionnaire ou contractuel.' },
  { id: 'profil', groupe: 'annonce', titre: 'Profil et conditions', aide: 'Décrivez la personne que vous cherchez et les conditions dans lesquelles elle travaillera, pour que le candidat puisse se projeter dans le poste.' },
  { id: 'lieu', groupe: 'annonce', titre: 'Employeur et lieux', aide: 'Présentez votre structure et indiquez où se trouve le poste : le candidat se fait une idée de son futur environnement de travail.' },
  { id: 'formulaire', groupe: 'candidature', titre: 'Formulaire', aide: 'Ces questions sont posées au candidat au moment où il postule. Ses réponses vous aident à comprendre sa candidature dès la première lecture.' },
  { id: 'documents', groupe: 'candidature', titre: 'Documents', aide: 'Choisissez les pièces que le candidat joint à sa candidature. Demandez l\'essentiel : chaque pièce en plus rend la candidature plus longue à préparer.' },
]

export function groupeDe(partie: PartieOffre) {
  return GROUPES.find(g => g.id === ETAPES_OFFRE.find(e => e.id === partie)!.groupe)!
}
