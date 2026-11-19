// Étapes de l'offre (retours PO, points 4 et 10 du document original) : une suite d'écrans de gauche à droite plutôt
// qu'un long formulaire. L'ancienne partie « Annonce » est découpée en quatre. Processus et Équipe sont les deux
// derniers écrans, repris des écrans existants de la plateforme (étapes de recrutement, équipe de recrutement).
// Le journal d'activité se consulte à part, depuis le menu « … » de l'offre.

export type PartieOffre = 'poste' | 'cadre' | 'profil' | 'lieu' | 'interne' | 'candidature' | 'processus' | 'equipe'

export const ETAPES_OFFRE: { id: PartieOffre, titre: string, aide: string, facultatif?: boolean }[] = [
  { id: 'poste', titre: 'Le poste', aide: 'Ce que liront les candidats sur Choisir le Service Public : intitulé, métier, missions.' },
  { id: 'cadre', titre: 'Cadre du recrutement', aide: 'À qui l\'emploi est ouvert, statut du poste, catégorie, corps et grade.' },
  { id: 'profil', titre: 'Profil et conditions', aide: 'La personne recherchée et les conditions de travail.' },
  { id: 'lieu', titre: 'Employeur et lieux', aide: 'Qui recrute, et où se trouve le poste.' },
  { id: 'interne', titre: 'Informations internes', aide: 'Ce qui sert à l\'organisme et n\'est jamais publié.' },
  { id: 'candidature', titre: 'Candidature', aide: 'Ce que vous demandez aux candidats quand ils postulent. Les candidatures arrivent dans l\'ATS.' },
  { id: 'processus', titre: 'Étapes de recrutement', facultatif: true, aide: 'Facultatif. Sans adaptation, ce sont les étapes de recrutement de l\'organisme qui s\'appliquent.' },
  { id: 'equipe', titre: 'Équipe de recrutement', facultatif: true, aide: 'Facultatif. Vous êtes Responsable de l\'offre ; ajoutez d\'autres membres si besoin.' },
]
