import type { AgentRecherche } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { useAgentParEmail } from './useAgentParEmail'

const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: vi.fn(),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  setAgentRole: vi.fn(),
  updateAgentRole: vi.fn(),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const EMAIL_INCONNU = 'nouvelle.agente@example.gouv.fr'

const AGENT: AgentRecherche = {
  agent_id: 'aaaaaaaa-0001-0001-0001-000000000001',
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

const AGENT_CREE: AgentRecherche = {
  ...AGENT,
  agent_id: 'aaaaaaaa-0002-0002-0002-000000000002',
  email: EMAIL_INCONNU,
  prenom: '',
  nom: '',
  intitule_poste: '',
}

function mountAgentParEmail() {
  let result!: ReturnType<typeof useAgentParEmail>
  mount(defineComponent({
    setup() {
      result = useAgentParEmail(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAgentParEmail', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockCreateAgent.mockResolvedValue(AGENT_CREE)
  })

  it('exposes the agent when the email matches', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    const { search, status, foundAgent } = mountAgentParEmail()

    await search(AGENT.email)

    expect(mockSearchAgentByEmail).toHaveBeenCalledWith(ORGANISME_UUID, AGENT.email)
    expect(status.value).toBe('found')
    expect(foundAgent.value).toEqual(AGENT)
  })

  it('reports an unknown email without raising', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, status, foundAgent } = mountAgentParEmail()

    await search(EMAIL_INCONNU)

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('clears the previous result before a new search', async () => {
    mockSearchAgentByEmail.mockResolvedValueOnce(AGENT).mockResolvedValueOnce(null)
    const { search, status, foundAgent } = mountAgentParEmail()

    await search(AGENT.email)
    await search(EMAIL_INCONNU)

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('returns the found agent without creating an account', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    const { search, resolve } = mountAgentParEmail()

    await search(AGENT.email)

    expect(await resolve()).toEqual(AGENT)
    expect(mockCreateAgent).not.toHaveBeenCalled()
  })

  it('creates the account when the email matches nobody', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, resolve, status, foundAgent } = mountAgentParEmail()

    await search(EMAIL_INCONNU)

    expect(await resolve()).toEqual(AGENT_CREE)
    expect(mockCreateAgent).toHaveBeenCalledWith({
      email: EMAIL_INCONNU,
      organisme_id: ORGANISME_UUID,
    })
    expect(status.value).toBe('found')
    expect(foundAgent.value).toEqual(AGENT_CREE)
  })

  it('does not create a second account when resolved twice', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, resolve } = mountAgentParEmail()

    await search(EMAIL_INCONNU)
    await resolve()
    await resolve()

    expect(mockCreateAgent).toHaveBeenCalledTimes(1)
  })
})
