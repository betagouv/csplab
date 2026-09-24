import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { useAjoutMembre } from './useAjoutMembre'
import { useOrganismeAgents } from './useOrganismeAgents'

const mockGetOrganismeAgents = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockSetAgentRole = vi.fn()
const mockCreateAgent = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  setAgentRole: (...args: unknown[]) => mockSetAgentRole(...args),
  updateAgentRole: vi.fn(),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAjoutMembre() {
  let result!: ReturnType<typeof useAjoutMembre>
  mount(defineComponent({
    setup() {
      useOrganismeAgents(ORGANISME_UUID)
      result = useAjoutMembre(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAjoutMembre', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetOrganismeAgents.mockResolvedValue([])
  })

  it('attaches the found agent and refetches the list', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT_RECHERCHE)
    mockSetAgentRole.mockResolvedValue({})
    const { search, add } = mountAjoutMembre()
    await flush()

    await search(AGENT_RECHERCHE.email)
    await add('agent')
    await flush()

    expect(mockCreateAgent).not.toHaveBeenCalled()
    expect(mockSetAgentRole).toHaveBeenCalledWith(ORGANISME_UUID, {
      agent_id: AGENT_RECHERCHE.agent_id,
      role: 'agent',
    })
    expect(mockGetOrganismeAgents).toHaveBeenCalledTimes(2)
  })

  it('creates the agent then attaches it when no account matches', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    mockCreateAgent.mockResolvedValue({ ...AGENT_RECHERCHE, prenom: '', nom: '', intitule_poste: '' })
    mockSetAgentRole.mockResolvedValue({})
    const { search, add } = mountAjoutMembre()
    await flush()

    await search('nouvelle.agente@example.gouv.fr')
    await add('superviseur')

    expect(mockCreateAgent).toHaveBeenCalledWith({
      email: 'nouvelle.agente@example.gouv.fr',
      organisme_id: ORGANISME_UUID,
    })
    expect(mockSetAgentRole).toHaveBeenCalledWith(ORGANISME_UUID, {
      agent_id: AGENT_RECHERCHE.agent_id,
      role: 'superviseur',
    })
  })
})
