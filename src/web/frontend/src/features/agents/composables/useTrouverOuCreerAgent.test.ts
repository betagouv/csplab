import type { AgentRecherche } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useTrouverOuCreerAgent } from './useTrouverOuCreerAgent'

const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()
const mockAction = vi.fn()

vi.mock('../api', () => ({
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const EMAIL_INCONNU = 'nouvelle.agente@example.gouv.fr'

const AGENT: AgentRecherche = {
  uuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

const AGENT_CREE: AgentRecherche = {
  ...AGENT,
  uuid: 'aaaaaaaa-0002-0002-0002-000000000002',
  email: EMAIL_INCONNU,
  prenom: '',
  nom: '',
  intitule_poste: '',
}

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountTrouverOuCreerAgent() {
  let result!: ReturnType<typeof useTrouverOuCreerAgent<string, unknown>>
  mount(defineComponent({
    setup() {
      result = useTrouverOuCreerAgent(ORGANISME_UUID, {
        action: (agent, variables: string) => mockAction(agent, variables),
        onSettled: () => undefined,
      })
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useTrouverOuCreerAgent', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockCreateAgent.mockResolvedValue(AGENT_CREE)
    mockAction.mockResolvedValue({})
  })

  it('exposes the agent when the email matches', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    const { search, status, foundAgent } = mountTrouverOuCreerAgent()

    await search(AGENT.email)

    expect(mockSearchAgentByEmail).toHaveBeenCalledWith(ORGANISME_UUID, AGENT.email)
    expect(status.value).toBe('found')
    expect(foundAgent.value).toEqual(AGENT)
  })

  it('reports an unknown email without raising', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, status, foundAgent } = mountTrouverOuCreerAgent()

    await search(EMAIL_INCONNU)

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('clears the previous result before a new search', async () => {
    mockSearchAgentByEmail.mockResolvedValueOnce(AGENT).mockResolvedValueOnce(null)
    const { search, status, foundAgent } = mountTrouverOuCreerAgent()

    await search(AGENT.email)
    await search(EMAIL_INCONNU)

    expect(status.value).toBe('not-found')
    expect(foundAgent.value).toBeNull()
  })

  it('acts on the found agent without creating an account', async () => {
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    const { search, run } = mountTrouverOuCreerAgent()

    await search(AGENT.email)
    await run('variables')

    expect(mockCreateAgent).not.toHaveBeenCalled()
    expect(mockAction).toHaveBeenCalledWith(AGENT, 'variables')
  })

  it('creates the account then acts on it when the email matches nobody', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, run, status, foundAgent } = mountTrouverOuCreerAgent()

    await search(EMAIL_INCONNU)
    await run('variables')

    expect(mockCreateAgent).toHaveBeenCalledWith({
      email: EMAIL_INCONNU,
      organisme_id: ORGANISME_UUID,
    })
    expect(mockAction).toHaveBeenCalledWith(AGENT_CREE, 'variables')
    expect(status.value).toBe('found')
    expect(foundAgent.value).toEqual(AGENT_CREE)
  })

  it('does not create a second account when run twice', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const { search, run } = mountTrouverOuCreerAgent()

    await search(EMAIL_INCONNU)
    await run('variables')
    await run('variables')

    expect(mockCreateAgent).toHaveBeenCalledTimes(1)
  })

  it('stays submitting from the account creation until the action is done', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    let acheverCreation!: (agent: AgentRecherche) => void
    let acheverAction!: (resultat: unknown) => void
    mockCreateAgent.mockReturnValue(new Promise((resolve) => {
      acheverCreation = resolve
    }))
    mockAction.mockReturnValue(new Promise((resolve) => {
      acheverAction = resolve
    }))

    const result = mountTrouverOuCreerAgent()
    await result.search(EMAIL_INCONNU)

    const enCours = result.run('variables')
    await flush()
    expect(result.submitting.value).toBe(true)

    acheverCreation(AGENT_CREE)
    await flush()
    expect(result.submitting.value).toBe(true)

    acheverAction({})
    await enCours
    await flush()
    expect(result.submitting.value).toBe(false)
  })
})
