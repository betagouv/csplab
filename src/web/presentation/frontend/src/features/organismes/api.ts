import type { CreateOrganismePayload, OrganismeAdmin, UpdateOrganismePayload } from './types'

// In-memory implementation until the organisme admin endpoints land (#1145-#1147).

export class SiretConflictError extends Error {
  constructor() {
    super('Ce SIRET est déjà utilisé par un autre organisme')
  }
}

const FIXTURE_ORGANISMES: OrganismeAdmin[] = [
  {
    uuid: '00000000-0000-0000-0000-000000000000',
    nom: 'Ministère de la Transition Écologique',
    siret: '11004601800013',
    versant: 'FPE',
    gestion_candidatures: true,
    gestionnaire: null,
  },
  {
    uuid: '22222222-2222-2222-2222-222222222222',
    nom: 'Fabrique Numérique de l\'Écologie',
    siret: '11004601800021',
    versant: 'FPE',
    gestion_candidatures: true,
    gestionnaire: { prenom: 'Camille', nom: 'Farce' },
  },
  {
    uuid: '33333333-3333-3333-3333-333333333333',
    nom: 'Région Nouvelle-Aquitaine',
    siret: '20005375900014',
    versant: 'FPT',
    gestion_candidatures: true,
    gestionnaire: { prenom: 'Marie', nom: 'Noel' },
  },
  {
    uuid: '44444444-4444-4444-4444-444444444444',
    nom: 'CHU de Bordeaux',
    siret: '26330582800017',
    versant: 'FPH',
    gestion_candidatures: false,
    gestionnaire: { prenom: 'Samir', nom: 'Marlot' },
  },
]

let organismes = [...FIXTURE_ORGANISMES]

function delay(ms = 300): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export async function getOrganismes(): Promise<OrganismeAdmin[]> {
  await delay()
  return [...organismes]
}

export async function createOrganisme(payload: CreateOrganismePayload): Promise<OrganismeAdmin> {
  await delay()
  if (organismes.some(o => o.siret === payload.siret)) {
    throw new SiretConflictError()
  }
  const organisme: OrganismeAdmin = {
    uuid: crypto.randomUUID(),
    ...payload,
    gestionnaire: null,
  }
  organismes = [...organismes, organisme]
  return organisme
}

export async function updateOrganisme(
  uuid: string,
  payload: UpdateOrganismePayload,
): Promise<OrganismeAdmin> {
  await delay()
  const current = organismes.find(o => o.uuid === uuid)
  if (!current) {
    throw new Error('Organisme introuvable')
  }
  const updated: OrganismeAdmin = { ...current, ...payload }
  organismes = organismes.map(o => (o.uuid === uuid ? updated : o))
  return updated
}
