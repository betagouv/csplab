import type { AgentRecherche } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useAjoutMembre } from './useAjoutMembre'
import { useOrganismeAgents } from './useOrganismeAgents'

const mockGetOrganismeAgents = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockSetAgentRole = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  setAgentRole: (...args: unknown[]) => mockSetAgentRole(...args),
  updateAgentRole: vi.fn(),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

const AGENT: AgentRecherche = {
  agent_id: 'aaaaaaaa-0001-0001-0001-000000000001',
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

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

  it('exposes the agent when the email matches', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    const { search, status, foundAgent } = mountAjoutMembre()

    await search(AGENT.email)

    expect(mockSearchAgentByEmail).toHaveBeenCalledWith(ORGANISME_UUID, AGENT.email)
    expect(status.value).toBe('found')
    expect(foundAgent.value).toEqual(AGENT)
  })

  it('reports an unknown email without raising', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, status, foundAgent } = mountAjoutMembre()

    await search('inconnu@example.gouv.fr')

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('clears the previous result before a new search', async () => {
    mockSearchAgentByEmail.mockResolvedValueOnce(AGENT).mockResolvedValueOnce(null)
    const { search, status, foundAgent } = mountAjoutMembre()

    await search(AGENT.email)
    await search('inconnu@example.gouv.fr')

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('attaches the found agent and refetches the list', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockSetAgentRole.mockResolvedValue({})
    const { search, attach } = mountAjoutMembre()
    await flush()

    await search(AGENT.email)
    await attach('membre')
    await flush()

    expect(mockSetAgentRole).toHaveBeenCalledWith(ORGANISME_UUID, {
      agent_id: AGENT.agent_id,
      role: 'membre',
    })
    expect(mockGetOrganismeAgents).toHaveBeenCalledTimes(2)
  })

  it('propagates attach errors to the caller', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockSetAgentRole.mockRejectedValue(new Error('boom'))
    const { search, attach } = mountAjoutMembre()
    await flush()

    await search(AGENT.email)

    await expect(attach('membre')).rejects.toThrow('boom')
  })
})
