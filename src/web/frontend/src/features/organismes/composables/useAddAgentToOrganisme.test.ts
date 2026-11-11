import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { AGENT_RECHERCHE } from '@/test/fixtures/agents'
import { agentCreation } from '@/test/handlers/agents'
import { server } from '@/test/server'
import { useAddAgentToOrganisme } from './useAddAgentToOrganisme'
import { useOrganismeAgents } from './useOrganismeAgents'

const mockGetOrganismeAgents = vi.fn()
const mockSetAgentRole = vi.fn()

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
  setAgentRole: (...args: unknown[]) => mockSetAgentRole(...args),
  updateAgentRole: vi.fn(),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAjoutMembre() {
  let result!: ReturnType<typeof useAddAgentToOrganisme>
  mount(defineComponent({
    setup() {
      useOrganismeAgents(ORGANISME_UUID)
      result = useAddAgentToOrganisme(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAddAgentToOrganisme', () => {
  beforeEach(() => {
    mockGetOrganismeAgents.mockResolvedValue([])
  })

  it('attaches the found agent and refetches the list', async () => {
    const onCreation = vi.fn()
    server.use(agentCreation(undefined, onCreation))
    mockSetAgentRole.mockResolvedValue({})
    const { search, add } = mountAjoutMembre()
    await flush()

    await search(AGENT_RECHERCHE.email)
    await add('agent')
    await flush()

    expect(onCreation).not.toHaveBeenCalled()
    expect(mockSetAgentRole).toHaveBeenCalledWith(ORGANISME_UUID, {
      agent_id: AGENT_RECHERCHE.uuid,
      role: 'agent',
    })
    expect(mockGetOrganismeAgents).toHaveBeenCalledTimes(2)
  })
})
