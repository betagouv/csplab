export type ProtoCategorie = 'ENTREE' | 'EN_COURS' | 'REFUS' | 'ACCEPTE'

export interface ProtoEtape {
  uuid: string
  nom: string
  categorie: ProtoCategorie
  candidatureUuids: string[]
}

export interface ProtoCandidat {
  prenom: string
  nom: string
  email: string
  telephone?: string
  localisation?: string
}

export type ProtoCv = 'lisible' | 'absent' | 'illisible'

export type ProtoActiviteType = 'reception' | 'etape' | 'note' | 'tag' | 'message'

export interface ProtoActivite {
  uuid: string
  type: ProtoActiviteType
  date: string
  auteur?: string
  libelle: string
  tags?: string[]
}

export interface ProtoNote {
  uuid: string
  auteur: string
  role: string
  date: string
  message: string
  privee: boolean
  mienne: boolean
}

export interface ProtoDocument {
  uuid: string
  nom: string
  type: string
  taille: string
}

export interface ProtoCandidature {
  uuid: string
  candidat: ProtoCandidat
  dateSoumission: string
  cv: ProtoCv
  tags: string[]
  notes: ProtoNote[]
  activites: ProtoActivite[]
  documents: ProtoDocument[]
}

export const UTILISATEUR = { nom: 'Jules Pommier', role: 'Recruteur' }

export const INTITULE_OFFRE = 'Chargé·e de communication'

export const TAGS_ORGANISME = [
  'Expert',
  'Expérience grand compte',
  'Softskills',
  'Disponible immédiatement',
  'Permis B',
  'Langues : anglais courant',
  'Candidat recommandé',
  'Télétravail possible',
  'Mobilité nationale',
  'Diplôme Bac+5',
]

let counter = 0

export function nextUuid(prefix = 'proto'): string {
  counter += 1
  return `${prefix}-${String(counter).padStart(4, '0')}`
}

export function minutesAgo(minutes: number): string {
  return new Date(Date.now() - minutes * 60_000).toISOString()
}

export function daysAgo(days: number, hour = 10): string {
  const date = new Date()
  date.setDate(date.getDate() - days)
  date.setHours(hour, 0, 0, 0)
  return date.toISOString()
}

function reception(date: string): ProtoActivite {
  return { uuid: nextUuid('act'), type: 'reception', date, libelle: 'Candidature reçue' }
}

function candidature(input: {
  candidat: ProtoCandidat
  jours: number
  cv?: ProtoCv
  tags?: string[]
  notes?: ProtoNote[]
  activites?: ProtoActivite[]
}): ProtoCandidature {
  const dateSoumission = daysAgo(input.jours)
  const documents: ProtoDocument[] = input.cv === 'absent'
    ? [{ uuid: nextUuid('doc'), nom: 'Lettre de motivation.pdf', type: 'Lettre de motivation', taille: '84 Ko' }]
    : [
        { uuid: nextUuid('doc'), nom: `CV ${input.candidat.nom}.${input.cv === 'illisible' ? 'pages' : 'pdf'}`, type: 'Curriculum vitae', taille: '212 Ko' },
        { uuid: nextUuid('doc'), nom: 'Lettre de motivation.pdf', type: 'Lettre de motivation', taille: '84 Ko' },
      ]
  return {
    uuid: nextUuid('cand'),
    candidat: input.candidat,
    dateSoumission,
    cv: input.cv ?? 'lisible',
    tags: input.tags ?? [],
    notes: input.notes ?? [],
    activites: [...(input.activites ?? []), reception(dateSoumission)],
    documents,
  }
}

export interface ProtoScenario {
  etapes: ProtoEtape[]
  candidatures: ProtoCandidature[]
}

export function createScenario(): ProtoScenario {
  const delacom = candidature({
    candidat: { prenom: 'Jean', nom: 'Delacom', email: 'jeandelacom@gmail.fr', telephone: '06 01 02 03 04', localisation: 'Marseille' },
    jours: 3,
    tags: ['Expert', 'Expérience grand compte', 'Softskills'],
    notes: [
      {
        uuid: nextUuid('note'),
        auteur: 'Camille Dupont',
        role: 'Responsable',
        date: minutesAgo(25),
        message: 'Le candidat a un très bon profil. Enthousiaste et motivé. Peu d\'expérience dans la fonction publique mais profil très intéressant. À approfondir.',
        privee: false,
        mienne: false,
      },
      {
        uuid: nextUuid('note'),
        auteur: UTILISATEUR.nom,
        role: 'Vous',
        date: daysAgo(1, 9),
        message: 'Profil intéressant.',
        privee: true,
        mienne: true,
      },
    ],
    activites: [
      { uuid: nextUuid('act'), type: 'note', date: minutesAgo(25), auteur: 'Camille Dupont', libelle: 'Note enregistrée' },
      { uuid: nextUuid('act'), type: 'tag', date: minutesAgo(40), auteur: 'Amélie Plat', libelle: 'a ajouté 3 tags', tags: ['Expert', 'Expérience grand compte', 'Softskills'] },
    ],
  })
  const dupont = candidature({
    candidat: { prenom: 'Marie', nom: 'Dupont', email: 'marie.dupont@example.fr', localisation: 'Paris' },
    jours: 0,
    cv: 'absent',
  })
  const martin = candidature({
    candidat: { prenom: 'Paul', nom: 'Martin', email: 'paul.martin@example.fr', telephone: '06 11 22 33 44' },
    jours: 2,
    cv: 'illisible',
  })
  const santi = candidature({
    candidat: { prenom: 'Jules', nom: 'Santi', email: 'jules.santi@example.fr', localisation: 'Lyon' },
    jours: 2,
    tags: ['Disponible immédiatement'],
  })
  const ladoque = candidature({
    candidat: { prenom: 'Amélie', nom: 'Ladoque', email: 'a.ladoque@avocat.fr', telephone: '06 12 34 56 78', localisation: 'Bordeaux' },
    jours: 6,
    tags: ['Candidat recommandé'],
    activites: [
      { uuid: nextUuid('act'), type: 'etape', date: daysAgo(1, 15), auteur: 'Amélie Plat', libelle: 'Déplacé de À traiter à Pré-qualification' },
    ],
  })
  const marceo = candidature({
    candidat: { prenom: 'Carole', nom: 'Marceo', email: 'carole.marceo@example.fr', localisation: 'Nantes' },
    jours: 8,
    activites: [
      { uuid: nextUuid('act'), type: 'etape', date: daysAgo(2, 11), auteur: 'Jean Plat', libelle: 'Déplacé de À traiter à Pré-qualification' },
      { uuid: nextUuid('act'), type: 'message', date: daysAgo(2, 12), auteur: 'Jean Plat', libelle: 'a envoyé un message' },
    ],
  })
  const benali = candidature({
    candidat: { prenom: 'Nadia', nom: 'Benali', email: 'nadia.benali@example.fr', telephone: '07 55 66 77 88', localisation: 'Lille' },
    jours: 12,
    tags: ['Langues : anglais courant', 'Diplôme Bac+5'],
    activites: [
      { uuid: nextUuid('act'), type: 'etape', date: daysAgo(4, 16), auteur: 'Camille Dupont', libelle: 'Déplacé de Pré-qualification à Entretien' },
      { uuid: nextUuid('act'), type: 'etape', date: daysAgo(9, 10), auteur: 'Camille Dupont', libelle: 'Déplacé de À traiter à Pré-qualification' },
    ],
  })
  const roux = candidature({
    candidat: { prenom: 'Thomas', nom: 'Roux', email: 'thomas.roux@example.fr' },
    jours: 15,
    activites: [
      { uuid: nextUuid('act'), type: 'etape', date: daysAgo(10, 14), auteur: 'Jean Plat', libelle: 'Déplacé de À traiter à Candidature refusée' },
    ],
  })

  const candidatures = [delacom, dupont, martin, santi, ladoque, marceo, benali, roux]

  const etapes: ProtoEtape[] = [
    { uuid: nextUuid('etape'), nom: 'À traiter', categorie: 'ENTREE', candidatureUuids: [delacom.uuid, dupont.uuid, martin.uuid, santi.uuid] },
    { uuid: nextUuid('etape'), nom: 'Pré-qualification', categorie: 'EN_COURS', candidatureUuids: [ladoque.uuid, marceo.uuid] },
    { uuid: nextUuid('etape'), nom: 'Entretien', categorie: 'EN_COURS', candidatureUuids: [benali.uuid] },
    { uuid: nextUuid('etape'), nom: 'Proposition', categorie: 'EN_COURS', candidatureUuids: [] },
    { uuid: nextUuid('etape'), nom: 'Candidature refusée', categorie: 'REFUS', candidatureUuids: [roux.uuid] },
    { uuid: nextUuid('etape'), nom: 'Candidature acceptée', categorie: 'ACCEPTE', candidatureUuids: [] },
  ]

  return { etapes, candidatures }
}
