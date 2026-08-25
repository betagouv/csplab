import type { AgentOrganisme } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useOrganismeAgents } from './useOrganismeAgents'

const mockGetOrganismeAgents = vi.fn()
const mockUpdateOrganismeAgent = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
  updateAgentRole: (...args: unknown[]) => mockUpdateOrganismeAgent(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

const AGENTS: AgentOrganisme[] = [
  {
    agent_id: 'aaaaaaaa-0001-0001-0001-000000000001',
    organisme_id: ORGANISME_UUID,
    nom: 'Dupont',
    prenom: 'Jeanne',
    email: 'jeanne.dupont@example.gouv.fr',
    poste: 'Responsable recrutement',
    role: 'responsable',
    date_derniere_activite: '2026-08-18T00:00:00Z',
    date_creation_compte: '2026-01-10T00:00:00Z',
  },
]

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAgents() {
  let result!: ReturnType<typeof useOrganismeAgents>
  mount(defineComponent({
    setup() {
      result = useOrganismeAgents(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useOrganismeAgents', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetOrganismeAgents.mockResolvedValue(AGENTS)
  })

  it('exposes the organisme agents', async () => {
    const { agents, pending } = mountAgents()
    expect(pending.value).toBe(true)
    await flush()
    expect(pending.value).toBe(false)
    expect(agents.value).toEqual(AGENTS)
  })

  it('updates an agent and refetches the list', async () => {
    mockUpdateOrganismeAgent.mockResolvedValue({ ...AGENTS[0], role: 'membre' })
    const { updateAgent } = mountAgents()
    await flush()

    await updateAgent({ agent_id: AGENTS[0].agent_id, role: 'membre' })
    await flush()

    expect(mockUpdateOrganismeAgent).toHaveBeenCalledWith(ORGANISME_UUID, {
      agent_id: AGENTS[0].agent_id,
      role: 'membre',
    })
    expect(mockGetOrganismeAgents).toHaveBeenCalledTimes(2)
  })

  it('propagates update errors to the caller', async () => {
    mockUpdateOrganismeAgent.mockRejectedValue(new Error('boom'))
    const { updateAgent } = mountAgents()
    await flush()

    await expect(
      updateAgent({ agent_id: AGENTS[0].agent_id, role: 'membre' }),
    ).rejects.toThrow('boom')
  })
})
