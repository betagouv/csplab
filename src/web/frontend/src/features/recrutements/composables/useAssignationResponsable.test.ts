import type { AgentOrganisme } from '@/features/organismes/types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import { recrutementsActifsQuery } from '../queries'
import { useAssignationResponsable } from './useAssignationResponsable'

const mockGetRecrutementsActifs = vi.fn()
const mockSetRecrutementsResponsable = vi.fn()
const mockGetOrganismeAgents = vi.fn()

vi.mock('../api', () => ({
  getRecrutementDetail: vi.fn(),
  getRecrutementsActifs: (...args: unknown[]) => mockGetRecrutementsActifs(...args),
  getRecrutementsArchives: vi.fn(),
  setRecrutementsResponsable: (...args: unknown[]) => mockSetRecrutementsResponsable(...args),
}))

vi.mock('@/features/organismes/api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
  getOrganismeAgents: (...args: unknown[]) => mockGetOrganismeAgents(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'

const AGENTS: AgentOrganisme[] = [
  {
    agent_id: AGENT_ID,
    organisme_id: ORGANISME_UUID,
    nom: 'Dupont',
    prenom: 'Jeanne',
    email: 'jeanne.dupont@example.gouv.fr',
    poste: 'Chargée de recrutement',
    role: 'agent',
    date_derniere_activite: null,
    date_creation_compte: '2026-01-01T00:00:00Z',
  },
]

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAssignation() {
  let result!: ReturnType<typeof useAssignationResponsable>
  mount(defineComponent({
    setup() {
      result = useAssignationResponsable(ORGANISME_UUID)
      useQuery(() => recrutementsActifsQuery({ organismeUuid: ORGANISME_UUID }))
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAssignationResponsable', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetOrganismeAgents.mockResolvedValue(AGENTS)
    mockGetRecrutementsActifs.mockResolvedValue({ results: RECRUTEMENTS_ACTIFS })
    mockSetRecrutementsResponsable.mockResolvedValue({ reussites: ['rec-1'], echecs: [] })
  })

  it('refreshes the active recrutements once a responsable has been assigned', async () => {
    const result = mountAssignation()
    await flush()
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(1)

    await result.assigner({ recrutement_ids: ['rec-1'], agent_id: AGENT_ID })
    await flush()

    expect(mockSetRecrutementsResponsable).toHaveBeenCalledWith(ORGANISME_UUID, {
      recrutement_ids: ['rec-1'],
      agent_id: AGENT_ID,
    })
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(2)
  })

  it('rejects so that the caller can report the failure', async () => {
    mockSetRecrutementsResponsable.mockRejectedValue(new Error('403'))
    const result = mountAssignation()
    await flush()

    await expect(
      result.assigner({ recrutement_ids: ['rec-1'], agent_id: AGENT_ID }),
    ).rejects.toThrow('403')
  })
})
