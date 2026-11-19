// Étapes du formulaire de l'offre (retour PO, F1) : un parcours en étapes successives plutôt qu'une longue page.
// L'ancienne partie « Annonce » est découpée en quatre. Processus, Équipe et Journal n'en font plus partie (F2) :
// ce sont les écrans existants de la plateforme, accessibles depuis la page de l'offre.

export type PartieOffre = 'poste' | 'cadre' | 'profil' | 'lieu' | 'interne' | 'candidature'

export const ETAPES_OFFRE: { id: PartieOffre, titre: string, aide: string }[] = [
  { id: 'poste', titre: 'Le poste', aide: 'Ce que liront les candidats sur Choisir le Service Public : intitulé, métier, missions.' },
  { id: 'cadre', titre: 'Cadre du recrutement', aide: 'À qui l\'emploi est ouvert, statut du poste, catégorie, corps et grade.' },
  { id: 'profil', titre: 'Profil et conditions', aide: 'La personne recherchée et les conditions de travail.' },
  { id: 'lieu', titre: 'Employeur et lieux', aide: 'Qui recrute, et où se trouve le poste.' },
  { id: 'interne', titre: 'Informations internes', aide: 'Ce qui sert à l\'organisme et n\'est jamais publié.' },
  { id: 'candidature', titre: 'Candidature', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.' },
]
