import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { AGENT_RECHERCHE } from '@/test/fixtures/agents'
import { agentCreation } from '@/test/handlers/agents'
import { server } from '@/test/server'
import { equipeRecrutementQuery } from '../queries'
import { useAddAgentToRecrutement } from './useAddAgentToRecrutement'

const mockGetEquipeRecrutement = vi.fn()
const mockAddMembreEquipe = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
  addMembreEquipe: (...args: unknown[]) => mockAddMembreEquipe(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAjoutMembre() {
  let result!: ReturnType<typeof useAddAgentToRecrutement>
  mount(defineComponent({
    setup() {
      result = useAddAgentToRecrutement(ORGANISME_UUID, RECRUTEMENT_UUID)
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

describe('useAddAgentToRecrutement', () => {
  beforeEach(() => {
    mockGetEquipeRecrutement.mockResolvedValue([])
    mockAddMembreEquipe.mockResolvedValue({})
  })

  it('adds the found agent then refreshes the team', async () => {
    const onCreation = vi.fn()
    server.use(agentCreation(undefined, onCreation))
    const result = mountAjoutMembre()
    await flush()
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(1)

    await result.search(AGENT_RECHERCHE.email)
    await result.add('recruteur')
    await flush()

    expect(onCreation).not.toHaveBeenCalled()
    expect(mockAddMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: AGENT_RECHERCHE.uuid,
      recrutement_role: 'recruteur',
    })
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
  })
})
