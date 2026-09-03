export interface RecrutementDashboard {
  id: string
  intitule: string
  referenceRenoiRH: string
  service: string
  typeContrat: string
  datePublicationLabel: string
  nouveauxCV: number
  candidaturesTotal: number
  candidaturesEnAttente: number
  entretiensAPreparer: number
}

export type EcheanceStatut = 'retard' | 'aujourdhui' | 'venir'

export interface TacheDashboard {
  id: string
  libelle: string
  recrutementId: string | null
  recrutementIntitule: string | null
  candidatNom: string | null
  echeanceStatut: EcheanceStatut
  echeanceLabel: string
  assigneA: string
  fait: boolean
}

// Réf. RenoiRH plutôt que la référence interne CSP : c'est le repère cité en
// test utilisateur, à ne pas confondre avec `reference_csp` du vrai schéma API.
export function createRecrutements(): RecrutementDashboard[] {
  return [
    {
      id: 'rec-1',
      intitule: 'Chargé·e de mission RH',
      referenceRenoiRH: 'RH-2026-0412',
      service: 'Direction des ressources humaines',
      typeContrat: 'Titulaire et contractuel',
      datePublicationLabel: 'Publiée il y a 2 jours',
      nouveauxCV: 12,
      candidaturesTotal: 34,
      candidaturesEnAttente: 4,
      entretiensAPreparer: 1,
    },
    {
      id: 'rec-2',
      intitule: 'Gestionnaire administratif·ve',
      referenceRenoiRH: 'GA-2026-0298',
      service: 'Direction des affaires générales',
      typeContrat: 'Contractuel',
      datePublicationLabel: 'Publiée il y a 5 jours',
      nouveauxCV: 5,
      candidaturesTotal: 19,
      candidaturesEnAttente: 2,
      entretiensAPreparer: 0,
    },
    {
      id: 'rec-3',
      intitule: 'Chef·fe de projet numérique',
      referenceRenoiRH: 'NUM-2026-0087',
      service: 'Direction du numérique',
      typeContrat: 'Titulaire et contractuel',
      datePublicationLabel: 'Publiée il y a 1 jour',
      nouveauxCV: 3,
      candidaturesTotal: 8,
      candidaturesEnAttente: 0,
      entretiensAPreparer: 2,
    },
    {
      id: 'rec-4',
      intitule: 'Responsable administratif·ve',
      referenceRenoiRH: 'ADM-2026-0155',
      service: 'Secrétariat général',
      typeContrat: 'Titulaire',
      datePublicationLabel: 'Publiée il y a 40 jours',
      nouveauxCV: 0,
      candidaturesTotal: 61,
      candidaturesEnAttente: 1,
      entretiensAPreparer: 0,
    },
    {
      id: 'rec-5',
      intitule: 'Assistant·e de direction',
      referenceRenoiRH: 'DIR-2026-0033',
      service: 'Direction générale',
      typeContrat: 'Contractuel',
      datePublicationLabel: 'Publiée il y a 3 jours',
      nouveauxCV: 1,
      candidaturesTotal: 4,
      candidaturesEnAttente: 0,
      entretiensAPreparer: 0,
    },
    {
      id: 'rec-6',
      intitule: 'Chargé·e de communication',
      referenceRenoiRH: 'COM-2026-0071',
      service: 'Direction de la communication',
      typeContrat: 'Contractuel',
      datePublicationLabel: 'Publiée il y a 10 jours',
      nouveauxCV: 0,
      candidaturesTotal: 15,
      candidaturesEnAttente: 3,
      entretiensAPreparer: 1,
    },
    {
      id: 'rec-7',
      intitule: 'Technicien·ne informatique',
      referenceRenoiRH: 'NUM-2026-0102',
      service: 'Direction du numérique',
      typeContrat: 'Titulaire et contractuel',
      datePublicationLabel: 'Publiée il y a 60 jours',
      nouveauxCV: 0,
      candidaturesTotal: 2,
      candidaturesEnAttente: 0,
      entretiensAPreparer: 0,
    },
  ]
}

export function createTaches(): TacheDashboard[] {
  return [
    {
      id: 'tache-1',
      libelle: 'Évaluer la candidature de Camille Dupont',
      recrutementId: 'rec-1',
      recrutementIntitule: 'Chargé·e de mission RH',
      candidatNom: 'Camille Dupont',
      echeanceStatut: 'retard',
      echeanceLabel: 'Hier',
      assigneA: 'Alice Gourbat',
      fait: false,
    },
    {
      id: 'tache-2',
      libelle: 'Planifier l\'entretien pour Chef·fe de projet numérique',
      recrutementId: 'rec-3',
      recrutementIntitule: 'Chef·fe de projet numérique',
      candidatNom: null,
      echeanceStatut: 'retard',
      echeanceLabel: 'Il y a 2 jours',
      assigneA: 'Léa Fontaine',
      fait: false,
    },
    {
      id: 'tache-3',
      libelle: 'Préparer l\'entretien avec Nadia Benali',
      recrutementId: 'rec-3',
      recrutementIntitule: 'Chef·fe de projet numérique',
      candidatNom: 'Nadia Benali',
      echeanceStatut: 'aujourdhui',
      echeanceLabel: 'Aujourd\'hui',
      assigneA: 'Alice Gourbat',
      fait: false,
    },
    {
      id: 'tache-4',
      libelle: 'Vérifier les références de Thomas Girard',
      recrutementId: 'rec-2',
      recrutementIntitule: 'Gestionnaire administratif·ve',
      candidatNom: 'Thomas Girard',
      echeanceStatut: 'aujourdhui',
      echeanceLabel: 'Aujourd\'hui',
      assigneA: 'Léa Fontaine',
      fait: false,
    },
    {
      id: 'tache-5',
      libelle: 'Rédiger le retour à Chloé Marchand',
      recrutementId: 'rec-6',
      recrutementIntitule: 'Chargé·e de communication',
      candidatNom: 'Chloé Marchand',
      echeanceStatut: 'venir',
      echeanceLabel: 'Demain',
      assigneA: 'Alice Gourbat',
      fait: false,
    },
    {
      id: 'tache-6',
      libelle: 'Relancer l\'équipe recrutement sur le poste Assistant·e de direction',
      recrutementId: 'rec-5',
      recrutementIntitule: 'Assistant·e de direction',
      candidatNom: null,
      echeanceStatut: 'venir',
      echeanceLabel: 'Dans 3 jours',
      assigneA: 'Karim Haddad',
      fait: false,
    },
  ]
}

// Journée calme : plus aucun nouveau CV à traiter, l'équipe est à jour.
// Sert à vérifier que le bloc dominant ne devient pas un vide gênant.
export function createRecrutementsJourneeCalme(): RecrutementDashboard[] {
  return createRecrutements().map(r => ({ ...r, nouveauxCV: 0, entretiensAPreparer: 0 }))
}

export function createTachesJourneeCalme(): TacheDashboard[] {
  return [
    {
      id: 'tache-calme-1',
      libelle: 'Relancer l\'équipe recrutement sur le poste Assistant·e de direction',
      recrutementId: 'rec-5',
      recrutementIntitule: 'Assistant·e de direction',
      candidatNom: null,
      echeanceStatut: 'venir',
      echeanceLabel: 'Dans 3 jours',
      assigneA: 'Karim Haddad',
      fait: false,
    },
  ]
}
