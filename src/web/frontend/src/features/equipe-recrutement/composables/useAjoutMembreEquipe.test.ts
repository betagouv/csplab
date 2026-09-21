import type { AgentRecherche } from '@/features/organismes/types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { equipeRecrutementQuery } from '../queries'
import { useAjoutMembreEquipe } from './useAjoutMembreEquipe'

const mockGetEquipeRecrutement = vi.fn()
const mockAddMembreEquipe = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
  addMembreEquipe: (...args: unknown[]) => mockAddMembreEquipe(...args),
}))

vi.mock('@/features/organismes/api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
  getOrganismeAgents: vi.fn(),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'
const NOUVEL_AGENT_ID = 'bbbbbbbb-0002-0002-0002-000000000002'
const EMAIL_INCONNU = 'nouvelle.agente@example.gouv.fr'

const AGENT: AgentRecherche = {
  agent_id: AGENT_ID,
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Chargée de recrutement',
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
      useQuery(() => equipeRecrutementQuery({
        organismeUuid: ORGANISME_UUID,
        recrutementUuid: RECRUTEMENT_UUID,
      }))
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
    mockGetEquipeRecrutement.mockResolvedValue([])
    mockAddMembreEquipe.mockResolvedValue({})
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockCreateAgent.mockResolvedValue({ ...AGENT, agent_id: NOUVEL_AGENT_ID })
  })

  it('adds the found agent then refreshes the team', async () => {
    const result = mountAjoutMembre()
    await flush()
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(1)

    await result.search(AGENT.email)
    await result.add('recruteur')
    await flush()

    expect(mockCreateAgent).not.toHaveBeenCalled()
    expect(mockAddMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: AGENT_ID,
      recrutement_role: 'recruteur',
    })
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
  })

  it('creates the account before adding when no agent matches the email', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const result = mountAjoutMembre()
    await flush()

    await result.search(EMAIL_INCONNU)
    await result.add('contributeur')

    expect(mockCreateAgent).toHaveBeenCalledWith({
      email: EMAIL_INCONNU,
      organisme_id: ORGANISME_UUID,
    })
    expect(mockAddMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: NOUVEL_AGENT_ID,
      recrutement_role: 'contributeur',
    })
  })
})
