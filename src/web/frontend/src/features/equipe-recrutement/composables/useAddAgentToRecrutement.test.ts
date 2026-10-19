import type { AgentRecherche } from '@/features/agents/types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { equipeRecrutementQuery } from '../queries'
import { useAddAgentToRecrutement } from './useAddAgentToRecrutement'

const mockGetEquipeRecrutement = vi.fn()
const mockAddMembreEquipe = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
  addMembreEquipe: (...args: unknown[]) => mockAddMembreEquipe(...args),
}))

vi.mock('@/features/agents/api', () => ({
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'
const NOUVEL_AGENT_ID = 'bbbbbbbb-0002-0002-0002-000000000002'

const AGENT: AgentRecherche = {
  uuid: AGENT_ID,
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
    vi.clearAllMocks()
    mockGetEquipeRecrutement.mockResolvedValue([])
    mockAddMembreEquipe.mockResolvedValue({})
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockCreateAgent.mockResolvedValue({ ...AGENT, uuid: NOUVEL_AGENT_ID })
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
})
