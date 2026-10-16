import type { AgentRecherche } from '@/features/agents/types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { organismeKeys, recrutementKeys } from '@/api/queryKeys'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { recrutementsActifsQuery } from '../queries'
import { useAssignResponsable } from './useAssignResponsable'

const mockGetRecrutementsActifs = vi.fn()
const mockSetRecrutementsResponsable = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()
const mockGetEquipe = vi.fn()
const mockGetAgentsOrganisme = vi.fn()

vi.mock('../api', () => ({
  getRecrutementDetail: vi.fn(),
  getRecrutementsActifs: (...args: unknown[]) => mockGetRecrutementsActifs(...args),
  getRecrutementsArchives: vi.fn(),
  setRecrutementsResponsable: (...args: unknown[]) => mockSetRecrutementsResponsable(...args),
}))

vi.mock('@/features/agents/api', () => ({
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'
const NOUVEL_AGENT_ID = 'bbbbbbbb-0002-0002-0002-000000000002'
const EMAIL = 'jeanne.dupont@example.gouv.fr'

const AGENT: AgentRecherche = {
  uuid: AGENT_ID,
  email: EMAIL,
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Chargée de recrutement',
}

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAssignation() {
  let result!: ReturnType<typeof useAssignResponsable>
  mount(defineComponent({
    setup() {
      result = useAssignResponsable(ORGANISME_UUID)
      useQuery(() => recrutementsActifsQuery({ organismeUuid: ORGANISME_UUID }))
      useQuery({
        key: recrutementKeys.equipe({ organismeUuid: ORGANISME_UUID, recrutementUuid: 'rec-1' }),
        query: mockGetEquipe,
      })
      useQuery({
        key: organismeKeys.agents({ organismeUuid: ORGANISME_UUID }),
        query: mockGetAgentsOrganisme,
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

describe('useAssignResponsable', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetRecrutementsActifs.mockResolvedValue({ results: RECRUTEMENTS_ACTIFS })
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockCreateAgent.mockResolvedValue({ ...AGENT, uuid: NOUVEL_AGENT_ID, prenom: '', nom: '' })
    mockSetRecrutementsResponsable.mockResolvedValue({ reussites: ['rec-1'], echecs: [] })
    mockGetEquipe.mockResolvedValue([])
    mockGetAgentsOrganisme.mockResolvedValue([])
  })

  it('refreshes the active recrutements once the found agent has been assigned', async () => {
    const result = mountAssignation()
    await flush()
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(1)

    await result.search(EMAIL)
    await result.assign(['rec-1'])
    await flush()

    expect(result.status.value).toBe('found')
    expect(mockCreateAgent).not.toHaveBeenCalled()
    expect(mockSetRecrutementsResponsable).toHaveBeenCalledWith(ORGANISME_UUID, {
      recrutement_ids: ['rec-1'],
      agent_id: AGENT_ID,
    })
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(2)
  })

  it('refreshes the team of each recrutement and the agents of the organisme', async () => {
    const result = mountAssignation()
    await flush()
    expect(mockGetEquipe).toHaveBeenCalledTimes(1)
    expect(mockGetAgentsOrganisme).toHaveBeenCalledTimes(1)

    await result.search(EMAIL)
    await result.assign(['rec-1'])
    await flush()

    expect(mockGetEquipe).toHaveBeenCalledTimes(2)
    expect(mockGetAgentsOrganisme).toHaveBeenCalledTimes(2)
  })
})
