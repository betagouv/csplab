import type { MembreEquipe } from '../types'
import type { AgentOrganisme } from '@/features/organismes/types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useAjoutMembreEquipe } from './useAjoutMembreEquipe'

const mockGetEquipeRecrutement = vi.fn()
const mockAddMembreEquipe = vi.fn()
const mockGetOrganismeAgents = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
  addMembreEquipe: (...args: unknown[]) => mockAddMembreEquipe(...args),
}))

vi.mock('@/features/organismes/api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

const MEMBRE_ID = 'bbbbbbbb-0001-0001-0001-000000000001'
const NON_MEMBRE_ID = 'bbbbbbbb-0002-0002-0002-000000000002'

const MEMBRES: MembreEquipe[] = [
  {
    agent_id: MEMBRE_ID,
    nom: 'Dupont',
    prenom: 'Jeanne',
    poste: 'Responsable recrutement',
    email: 'jeanne.dupont@example.gouv.fr',
    recrutement_role: 'responsable',
  },
]

function agentOrganisme(agentId: string, nom: string): AgentOrganisme {
  return {
    agent_id: agentId,
    organisme_id: ORGANISME_UUID,
    nom,
    prenom: 'Jeanne',
    email: `${nom.toLowerCase()}@example.gouv.fr`,
    poste: 'Chargée de recrutement',
    role: 'agent',
    date_derniere_activite: null,
    date_creation_compte: '2026-01-01T00:00:00Z',
  }
}

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAjoutMembre() {
  let result!: ReturnType<typeof useAjoutMembreEquipe>
  mount(defineComponent({
    setup() {
      result = useAjoutMembreEquipe(ORGANISME_UUID, RECRUTEMENT_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAjoutMembreEquipe', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetEquipeRecrutement.mockResolvedValue(MEMBRES)
    mockGetOrganismeAgents.mockResolvedValue([
      agentOrganisme(MEMBRE_ID, 'Dupont'),
      agentOrganisme(NON_MEMBRE_ID, 'Martin'),
    ])
  })

  it('excludes the agents already in the team from the selectable agents', async () => {
    const result = mountAjoutMembre()
    await flush()

    expect(result.agentsDisponibles.value.map(agent => agent.agent_id)).toEqual([
      NON_MEMBRE_ID,
    ])
  })

  it('refreshes the team once a member has been added', async () => {
    const result = mountAjoutMembre()
    await flush()
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(1)

    await result.add({ agent_id: NON_MEMBRE_ID, recrutement_role: 'recruteur' })
    await flush()

    expect(mockAddMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: NON_MEMBRE_ID,
      recrutement_role: 'recruteur',
    })
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
  })
})
