// Modèle de l'espace candidat connecté (spec « strict nécessaire »). Volontairement séparé de
// candidatMock.ts, qui alimente les parcours de candidature et les itérations précédentes.

// Statut vu par le candidat — distinct des étapes internes du recrutement, qu'il ne révèle pas.
export type StatutCandidat = 'recue' | 'en_cours_examen' | 'non_retenue' | 'retenue' | 'offre_close' | 'retiree'

export interface StatutMeta {
  label: string
  phrase: string
  // Sémantique alignée sur la doctrine des badges (CspBadge) ; undefined = neutre.
  ton: 'info' | 'success' | 'error' | undefined
  icon: string
  enCours: boolean
}

export const statutMeta: Record<StatutCandidat, StatutMeta> = {
  recue: {
    label: 'Reçue',
    phrase: 'Votre candidature a bien été reçue.',
    ton: undefined,
    icon: 'ri:inbox-2-line',
    enCours: true,
  },
  en_cours_examen: {
    label: 'En cours d\'examen',
    phrase: 'Votre dossier est à l\'étude.',
    ton: 'info',
    icon: 'ri:progress-4-line',
    enCours: true,
  },
  non_retenue: {
    label: 'Non retenue',
    phrase: 'Votre candidature n\'a pas été retenue.',
    ton: 'error',
    icon: 'ri:close-circle-line',
    enCours: false,
  },
  retenue: {
    label: 'Retenue',
    phrase: 'Votre candidature a été retenue. L\'équipe vous contactera.',
    ton: 'success',
    icon: 'ri:checkbox-circle-line',
    enCours: false,
  },
  offre_close: {
    label: 'Offre close',
    phrase: 'Ce recrutement est terminé.',
    ton: undefined,
    icon: 'ri:archive-line',
    enCours: false,
  },
  retiree: {
    label: 'Retirée',
    phrase: 'Vous avez retiré cette candidature.',
    ton: undefined,
    icon: 'ri:arrow-go-back-line',
    enCours: false,
  },
}

export interface PieceJointe {
  id: string
  nom: string
  type: 'image' | 'document'
  url?: string
}

export interface MessageEspace {
  id: string
  auteur: 'candidat' | 'recruteur'
  auteurNom?: string
  texte: string
  date: Date
  lu: boolean
  pieces: PieceJointe[]
}

export interface ConversationEspace {
  id: string
  sujet: string
  messages: MessageEspace[]
}

export interface OffreResume {
  lieu: string
  typeContrat: string
  categorie: string
  description: string
}

export interface PieceDeposee {
  id: string
  libelle: string
  nom: string
}

export interface EvenementJournal {
  date: Date
  texte: string
  motif?: string
}

export interface CandidatureEspace {
  id: string
  intitule: string
  organisme: string
  statut: StatutCandidat
  dateDepot: Date
  // Plus récente parmi : dépôt, changement de statut candidat, message reçu, message envoyé, retrait.
  derniereActivite: Date
  offre: OffreResume
  conversations: ConversationEspace[]
  piecesDeposees: PieceDeposee[]
  journal: EvenementJournal[]
}

export type JeuDonnees = 'complet' | 'sansTerminees' | 'vide'

export interface Utilisateur {
  prenom: string
  nom: string
  email: string
  telephone: string
  methode: 'franceconnect' | 'formulaire'
}

function piecesStandard(cv: string, lettre?: string): PieceDeposee[] {
  return [
    { id: 'p-cv', libelle: 'CV', nom: cv },
    ...(lettre ? [{ id: 'p-lm', libelle: 'Lettre de motivation', nom: lettre }] : []),
  ]
}

const d = (jour: number, heure = 9, minute = 0, mois = 8) => new Date(2026, mois, jour, heure, minute)

export function creerCandidaturesMock(jeu: JeuDonnees): CandidatureEspace[] {
  if (jeu === 'vide') {
    return []
  }

  const enCours: CandidatureEspace[] = [
    {
      id: 'cand-instructeur',
      intitule: 'Instructeur·rice administratif·ve',
      organisme: 'Préfecture de la Gironde',
      statut: 'recue',
      dateDepot: d(24, 8, 12),
      derniereActivite: d(24, 8, 12),
      offre: {
        lieu: 'Bordeaux (33)',
        typeContrat: 'Contractuel CDD',
        categorie: 'Catégorie B',
        description: 'Au sein du bureau des étrangers, vous instruisez les demandes de titres de séjour, '
          + 'vérifiez la complétude des dossiers et orientez les usagers. Vous travaillez en lien étroit '
          + 'avec les agents d\'accueil et le service juridique.',
      },
      conversations: [],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf'),
      journal: [{ date: d(24, 8, 12), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-innovation-numerique',
      intitule: 'Chargé·e de mission innovation numérique',
      organisme: 'Ministère de la Transformation et de la Fonction Publiques',
      statut: 'en_cours_examen',
      dateDepot: d(12),
      derniereActivite: d(23, 9, 5),
      offre: {
        lieu: 'Paris 7ᵉ (télétravail partiel possible)',
        typeContrat: 'Contractuel CDD, 3 ans renouvelable',
        categorie: 'Catégorie A',
        description: 'Au sein de la direction interministérielle du numérique, vous rejoignez une équipe '
          + 'chargée d\'accompagner les administrations dans la conception de services publics numériques '
          + 'plus simples et plus rapides à utiliser. Vous animez des ateliers de recherche utilisateur, '
          + 'rédigez des recommandations d\'usage et contribuez à la doctrine interministérielle sur '
          + 'l\'accessibilité numérique.',
      },
      conversations: [
        {
          id: 'conv-entretien',
          sujet: 'Proposition d\'entretien',
          messages: [
            {
              id: 'm1',
              auteur: 'recruteur',
              auteurNom: 'Sophie Nguyen',
              texte: 'Bonjour, nous avons étudié votre dossier avec attention et souhaiterions vous rencontrer. '
                + 'Seriez-vous disponible le 30 septembre à 10h, en visioconférence ?',
              date: d(22, 14, 20),
              lu: true,
              pieces: [],
            },
            {
              id: 'm2',
              auteur: 'candidat',
              texte: 'Bonjour, oui, je suis disponible. Je vous remercie pour cette proposition.',
              date: d(22, 16, 2),
              lu: true,
              pieces: [],
            },
            {
              id: 'm3',
              auteur: 'recruteur',
              auteurNom: 'Sophie Nguyen',
              texte: 'Parfait, l\'entretien est confirmé le 30 septembre à 10h. Vous recevrez le lien de '
                + 'visioconférence par courriel. Avez-vous besoin d\'un aménagement particulier ?',
              date: d(23, 9, 5),
              lu: false,
              pieces: [],
            },
          ],
        },
        {
          id: 'conv-justificatif',
          sujet: 'Justificatif de titularisation',
          messages: [
            {
              id: 'm1',
              auteur: 'recruteur',
              auteurNom: 'Sophie Nguyen',
              texte: 'Pour finaliser l\'examen de votre dossier, pourriez-vous nous transmettre votre dernier '
                + 'arrêté de titularisation (PDF ou photo lisible) ?',
              date: d(18, 11, 0),
              lu: true,
              pieces: [],
            },
            {
              id: 'm2',
              auteur: 'candidat',
              texte: 'Bonjour, voici l\'arrêté demandé.',
              date: d(18, 18, 40),
              lu: true,
              pieces: [{ id: 'pj1', nom: 'arrete-titularisation.pdf', type: 'document' }],
            },
            {
              id: 'm3',
              auteur: 'recruteur',
              auteurNom: 'Sophie Nguyen',
              texte: 'Bien reçu, merci.',
              date: d(19, 8, 50),
              lu: true,
              pieces: [],
            },
          ],
        },
      ],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf', 'Lettre_motivation_DINUM.pdf'),
      journal: [{ date: d(12), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-chef-projet-si',
      intitule: 'Chef·fe de projet SI',
      organisme: 'Direction interministérielle du numérique',
      statut: 'en_cours_examen',
      dateDepot: new Date(2026, 7, 28, 10, 0),
      derniereActivite: d(22, 14, 20),
      offre: {
        lieu: 'Paris 7ᵉ',
        typeContrat: 'Titulaire (mutation, détachement)',
        categorie: 'Catégorie A',
        description: 'Vous pilotez des projets de systèmes d\'information interministériels, de la '
          + 'définition du besoin à la mise en production, en lien avec les équipes produit et les '
          + 'prestataires. Vous garantissez le respect des budgets, des délais et des exigences de sécurité.',
      },
      conversations: [
        {
          id: 'conv-disponibilite',
          sujet: 'Disponibilité pour une prise de poste',
          messages: [
            {
              id: 'm1',
              auteur: 'recruteur',
              auteurNom: 'Marc Delattre',
              texte: 'Bonjour, nous avons été convaincus par votre entretien. Avant de finaliser notre '
                + 'décision, pourriez-vous nous préciser votre disponibilité pour une prise de poste ?',
              date: d(22, 14, 20),
              lu: false,
              pieces: [],
            },
          ],
        },
      ],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf', 'Lettre_motivation_SI.pdf'),
      journal: [{ date: new Date(2026, 7, 28, 10, 0), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-rh',
      intitule: 'Responsable ressources humaines',
      organisme: 'Conseil départemental du Rhône',
      statut: 'en_cours_examen',
      dateDepot: d(3),
      // Dernière activité = passage de « Reçue » à « En cours d'examen » ; les changements d'étape
      // internes ultérieurs, sans effet sur le statut candidat, ne comptent pas.
      derniereActivite: d(8, 10, 0),
      offre: {
        lieu: 'Lyon (69)',
        typeContrat: 'Titulaire (mutation, détachement)',
        categorie: 'Catégorie A',
        description: 'Vous dirigez la direction des ressources humaines du département (250 agents) : '
          + 'gestion prévisionnelle des emplois et compétences, dialogue social, pilotage de la masse salariale.',
      },
      conversations: [],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf', 'Lettre_motivation_RH.pdf'),
      journal: [{ date: d(3), texte: 'Candidature déposée' }],
    },
  ]

  if (jeu === 'sansTerminees') {
    return enCours
  }

  const terminees: CandidatureEspace[] = [
    {
      id: 'cand-occitanie',
      intitule: 'Directeur·rice de projet transformation',
      organisme: 'Région Occitanie',
      statut: 'retenue',
      dateDepot: d(1),
      derniereActivite: d(21, 16, 30),
      offre: {
        lieu: 'Toulouse (31)',
        typeContrat: 'Contractuel CDI',
        categorie: 'Catégorie A+',
        description: 'Vous pilotez le programme de transformation numérique de la région et animez un '
          + 'réseau de correspondants dans chaque direction.',
      },
      conversations: [
        {
          id: 'conv-contact',
          sujet: 'Prise de contact',
          messages: [
            {
              id: 'm1',
              auteur: 'recruteur',
              auteurNom: 'Antoine Leroy',
              texte: 'Félicitations, votre candidature a été retenue. Nous souhaiterions convenir d\'un '
                + 'rendez-vous pour finaliser les modalités de prise de poste.',
              date: d(21, 16, 30),
              lu: false,
              pieces: [],
            },
          ],
        },
      ],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf', 'Lettre_motivation_Occitanie.pdf'),
      journal: [{ date: d(1), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-paie',
      intitule: 'Gestionnaire de paie',
      organisme: 'Centre hospitalier de Valence',
      statut: 'non_retenue',
      dateDepot: new Date(2026, 7, 28, 15, 0),
      derniereActivite: d(18, 15, 0),
      offre: {
        lieu: 'Valence (26)',
        typeContrat: 'Contractuel CDD',
        categorie: 'Catégorie B',
        description: 'Vous assurez la paie de 1 800 agents hospitaliers et le suivi des déclarations sociales.',
      },
      conversations: [
        {
          id: 'conv-reponse',
          sujet: 'Réponse à votre candidature',
          messages: [
            {
              id: 'm1',
              auteur: 'recruteur',
              auteurNom: 'Julie Ferrand',
              texte: 'Bonjour, merci pour l\'intérêt porté à ce poste. Après examen, nous ne pouvons pas '
                + 'donner suite à votre candidature. Nous vous souhaitons une belle réussite.',
              date: d(18, 15, 0),
              lu: true,
              pieces: [],
            },
          ],
        },
      ],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf'),
      journal: [{ date: new Date(2026, 7, 28, 15, 0), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-nantes',
      intitule: 'Chargé·e de communication',
      organisme: 'Ville de Nantes',
      statut: 'offre_close',
      dateDepot: new Date(2026, 7, 20, 9, 0),
      derniereActivite: d(10, 9, 0),
      offre: {
        lieu: 'Nantes (44)',
        typeContrat: 'Titulaire (mutation, détachement)',
        categorie: 'Catégorie B',
        description: 'Vous concevez et diffusez les contenus de la direction de la communication '
          + '(magazine, réseaux sociaux, événements).',
      },
      conversations: [],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf', 'Lettre_motivation_Nantes.pdf'),
      journal: [{ date: new Date(2026, 7, 20, 9, 0), texte: 'Candidature déposée' }],
    },
    {
      id: 'cand-insee',
      intitule: 'Analyste données',
      organisme: 'Insee',
      statut: 'retiree',
      dateDepot: new Date(2026, 7, 25, 11, 0),
      derniereActivite: d(5, 18, 0),
      offre: {
        lieu: 'Montrouge (92)',
        typeContrat: 'Contractuel CDD',
        categorie: 'Catégorie A',
        description: 'Vous exploitez et documentez des sources statistiques pour les enquêtes de l\'institut.',
      },
      conversations: [],
      piecesDeposees: piecesStandard('CV_Camille_Rousseau.pdf'),
      journal: [
        { date: new Date(2026, 7, 25, 11, 0), texte: 'Candidature déposée' },
        { date: d(5, 18, 0), texte: 'Candidature retirée par le candidat', motif: 'J\'ai trouvé un autre poste' },
      ],
    },
  ]

  return [...enCours, ...terminees]
}

export function creerUtilisateurMock(methode: Utilisateur['methode']): Utilisateur {
  return {
    prenom: 'Camille',
    nom: 'Rousseau',
    email: 'camille.rousseau@example.com',
    telephone: '06 12 34 56 78',
    methode,
  }
}
